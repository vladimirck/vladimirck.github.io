#!/bin/bash

# Script local Robusto para detectar enlaces rotos
# Gestiona el entorno virtual y ejecuta el motor de Python

# Colores para la terminal
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Paso 1: Compilando el sitio con Hugo...${NC}"
hugo --gc --minify > /dev/null

if [ $? -ne 0 ]; then
    echo "❌ Error al compilar el sitio. Revisa los errores de Hugo."
    exit 1
fi

# Verificar si existe el entorno virtual
if [ ! -d "scripts/.venv" ]; then
    echo -e "${BLUE}📦 Creando entorno virtual de Python...${NC}"
    python3 -m venv scripts/.venv
    scripts/.venv/bin/pip install httpx[http2] beautifulsoup4 rich --break-system-packages > /dev/null
fi

# Ejecutar el motor de Python
scripts/.venv/bin/python3 scripts/link_checker.py
