#!/usr/bin/env python3
import asyncio
import os
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse
import httpx
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

# Ajustes
BASE_DIR = Path("public")
IGNORE_DOMAINS = [
    "uasd.edu.do",      # Bloquea bots agresivamente
    "soft.uasd.edu.do",
    "twitter.com",       # A veces da 404/403 falsos a bots
    "linkedin.com"
]
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
CONCURRENCY_LIMIT = 25
TIMEOUT = 10.0

console = Console()

class LinkChecker:
    def __init__(self):
        self.all_links = {} # {url: [pages_found_in]}
        self.broken_links = []
        self.scanned_pages = 0

    def is_external(self, url):
        return bool(urlparse(url).netloc)

    def extract_links(self):
        """Escanea todos los archivos HTML en la carpeta public."""
        html_files = list(BASE_DIR.rglob("*.html"))
        self.scanned_pages = len(html_files)
        
        with console.status("[bold blue]Escaneando archivos locales..."):
            for html_file in html_files:
                relative_path = html_file.relative_to(BASE_DIR)
                with open(html_file, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "html.parser")
                    
                    # Buscar en etiquetas de enlace, imágenes, scripts y links de estilo
                    tags = {
                        "a": "href",
                        "img": "src",
                        "link": "href",
                        "script": "src",
                        "video": "src",
                        "audio": "src"
                    }
                    
                    for tag, attr in tags.items():
                        for element in soup.find_all(tag, **{attr: True}):
                            url = element[attr]
                            
                            # Ignorar fragmentos internos, esquemas mailto/tel, etc.
                            if url.startswith(("#", "mailto:", "tel:", "javascript:")):
                                continue
                                
                            # Normalizar URL
                            if not self.is_external(url):
                                # Convertir ruta relativa a "absoluta" respecto a la raíz del sitio
                                if url.startswith("/"):
                                    full_url = url.lstrip("/")
                                else:
                                    # Ruta relativa al archivo actual
                                    parent_dir = relative_path.parent
                                    full_url = str((parent_dir / url).resolve()).replace(os.getcwd(), "").lstrip("/")
                                    # Limpiar navegación de directorios (../)
                                    full_url = os.path.normpath(full_url).replace("\\", "/")
                                
                                # Si termina en /, Hugo suele buscar index.html
                                if full_url.endswith("/") or not "." in os.path.basename(full_url):
                                    full_url = os.path.join(full_url, "index.html").replace("\\", "/")
                            else:
                                full_url = url
                                
                            if full_url not in self.all_links:
                                self.all_links[full_url] = set()
                            self.all_links[full_url].add(str(relative_path))

    async def check_url(self, client, url, pages):
        """Valida una única URL (interna o externa)."""
        # Ignorar dominios en lista blanca
        parsed = urlparse(url)
        if any(domain in parsed.netloc for domain in IGNORE_DOMAINS):
            return

        if not self.is_external(url):
            # Verificación Interna
            path = BASE_DIR / url.split("#")[0]
            if not path.exists():
                self.broken_links.append({
                    "url": url,
                    "status": "404 (Local)",
                    "pages": list(pages)
                })
            return

        # Verificación Externa
        try:
            # Intentar primero con HEAD por eficiencia
            resp = await client.head(url, timeout=TIMEOUT, follow_redirects=True)
            
            # Algunos servidores bloquean HEAD, si falla con 405 o similar, intentar GET
            if resp.status_code in [404, 405, 403, 501]:
                resp = await client.get(url, timeout=TIMEOUT, follow_redirects=True)
                
            if resp.is_error:
                self.broken_links.append({
                    "url": url,
                    "status": resp.status_code,
                    "pages": list(pages)
                })
        except Exception as exc:
            # Capturar cualquier error (Timeout, TLS, etc.) de forma robusta
            status_text = "Error de Conexión"
            if "Timeout" in str(type(exc)):
                status_text = "Timeout"
            
            self.broken_links.append({
                "url": url,
                "status": status_text,
                "pages": list(pages)
            })

    async def validate_all(self):
        """Lanza la validación masiva de enlaces."""
        limits = httpx.Limits(max_keepalive_connections=5, max_connections=CONCURRENCY_LIMIT)
        async with httpx.AsyncClient(limits=limits, headers={"User-Agent": USER_AGENT}, http2=False) as client:
            tasks = []
            for url, pages in self.all_links.items():
                tasks.append(self.check_url(client, url, pages))
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            ) as progress:
                task = progress.add_task("[green]Validando enlaces...", total=len(tasks))
                for completed in asyncio.as_completed(tasks):
                    await completed
                    progress.update(task, advance=1)

    def generate_reports(self):
        """Genera el reporte en consola y en reporte_enlaces.md."""
        if not self.broken_links:
            console.print("\n[bold green]✅ No se encontraron enlaces rotos en ninguna página.[/bold green]")
            if os.path.exists("reporte_enlaces.md"):
                os.remove("reporte_enlaces.md")
            return

        # Reporte en Consola
        console.print(f"\n[bold red]❌ Se detectaron {len(self.broken_links)} enlaces con problemas:[/bold red]\n")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Estado", style="dim", width=12)
        table.add_column("Enlace", style="blue")
        table.add_column("Origen (Ejemplo)", style="yellow")

        for item in self.broken_links:
            table.add_row(
                str(item['status']),
                item['url'],
                item['pages'][0] # Solo mostramos uno en consola para no saturar
            )
        console.print(table)

        # Reporte Markdown
        with open("reporte_enlaces.md", "w", encoding="utf-8") as f:
            f.write("# Reporte Detallado de Enlaces Rotos\n\n")
            f.write(f"Total de páginas escaneadas: {self.scanned_pages}\n")
            f.write(f"Total de enlaces detectados: {len(self.all_links)}\n")
            f.write(f"Total de enlaces rotos: {len(self.broken_links)}\n\n")
            f.write("| Estado | Enlace Roto | Páginas donde se encontró |\n")
            f.write("| :--- | :--- | :--- |\n")
            
            for item in self.broken_links:
                pages_list = ", ".join([f"`/{p}`" for p in item['pages']])
                f.write(f"| {item['status']} | {item['url']} | {pages_list} |\n")
        
        console.print(f"\n[bold blue]📄 Reporte completo generado en: reporte_enlaces.md[/bold blue]")

async def main():
    checker = LinkChecker()
    checker.extract_links()
    await checker.validate_all()
    checker.generate_reports()

if __name__ == "__main__":
    asyncio.run(main())
