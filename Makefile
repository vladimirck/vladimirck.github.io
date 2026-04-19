# Makefile para la gestión del sitio Multiverso Académico

.PHONY: build serve dev check-links lighthouse clean help

# Variables
HUGO = hugo
PORT = 1313
LH_PORT = 3000
PUBLIC_DIR = public
SCRIPTS_DIR = scripts

help:
	@echo "Comandos disponibles:"
	@echo "  make build         - Compilar el sitio para producción"
	@echo "  make serve         - Servir el sitio localmente"
	@echo "  make dev           - Servir con borradores y temas futuros"
	@echo "  make check-links   - Ejecutar la detección de enlaces rotos"
	@echo "  make lighthouse    - Ejecutar auditoría de Lighthouse (HTML y MD)"
	@echo "  make clean         - Eliminar archivos generados"

build:
	$(HUGO) --gc --minify

serve:
	$(HUGO) server -p $(PORT)

dev:
	$(HUGO) server -D -F -p $(PORT)

check-links:
	bash $(SCRIPTS_DIR)/check_links.sh

lighthouse: build
	@echo "🚀 Iniciando servidor temporal para Lighthouse..."
	python3 -m http.server $(LH_PORT) --directory $(PUBLIC_DIR) > /dev/null 2>&1 & \
	echo $$! > .serve_pid; \
	sleep 5; \
	echo "🧐 Ejecutando auditoría de Lighthouse..."; \
	npx -y lighthouse http://localhost:$(LH_PORT) --output html --output json --output-path ./lighthouse_report --chrome-flags="--headless" --only-categories=performance,accessibility,best-practices,seo; \
	echo "✅ Auditoría completada. Limpiando..."; \
	kill $$(cat .serve_pid) && rm .serve_pid; \
	mv lighthouse_report.report.html lighthouse_report.html; \
	mv lighthouse_report.report.json lighthouse_report.json; \
	echo "📝 Generando reporte en Markdown..."; \
	python3 $(SCRIPTS_DIR)/lighthouse_to_md.py lighthouse_report.json lighthouse_report.md; \
	echo "✨ Proceso finalizado. Reportes: lighthouse_report.html y lighthouse_report.md"

clean:
	rm -rf $(PUBLIC_DIR)
	rm -f lighthouse_report.html lighthouse_report.json lighthouse_report.md .serve_pid
