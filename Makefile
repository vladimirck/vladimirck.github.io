# Makefile para la gestión del sitio Multiverso Académico (motor propio)

ENGINE_VERSION := $(shell cat .multiverso-version)
ENGINE_REPO    := vladimirck/multiverso-engine
ENGINE_SRC     := ../multiverso-engine
BIN            := .bin/multiverso
LH_PORT        := 3000
PUBLIC_DIR     := public

.PHONY: help engine build serve check verify lighthouse clean

help:
	@echo "Comandos disponibles:"
	@echo "  make engine     - obtiene el binario del motor ($(ENGINE_VERSION))"
	@echo "  make build      - compila el sitio en $(PUBLIC_DIR)/"
	@echo "  make serve      - servidor de desarrollo en :1313 con rebuild"
	@echo "  make check      - valida contenido, citas y bibliografía"
	@echo "  make verify     - verifica DOIs contra Crossref (usa red)"
	@echo "  make lighthouse - auditoría Lighthouse del sitio compilado"
	@echo "  make clean      - elimina artefactos generados"

# Obtiene el motor: compila desde el repo hermano si existe;
# si no, descarga la release pineada (requiere gh autenticado).
engine: $(BIN)

$(BIN):
	@mkdir -p .bin
	@if [ -d "$(ENGINE_SRC)" ]; then \
		echo "Compilando el motor desde $(ENGINE_SRC)…"; \
		( cd "$(ENGINE_SRC)" && go tool templ generate >/dev/null && \
		  go build -ldflags "-s -w" -o "$(CURDIR)/$(BIN)" ./cmd/multiverso ); \
	else \
		echo "Descargando multiverso $(ENGINE_VERSION)…"; \
		gh release download "$(ENGINE_VERSION)" --repo "$(ENGINE_REPO)" \
		  --pattern '*linux_amd64.tar.gz' --output - | tar -xz -C .bin multiverso; \
	fi
	@$(BIN) version

build: engine
	$(BIN) build --content . --out $(PUBLIC_DIR)

serve: engine
	$(BIN) serve --content . --addr :1313

check: engine
	$(BIN) check --content .

verify: engine
	$(BIN) verify --content .

lighthouse: build
	python3 -m http.server $(LH_PORT) --directory $(PUBLIC_DIR) > /dev/null 2>&1 & \
	echo $$! > .serve_pid; \
	sleep 3; \
	npx -y lighthouse@12.2.1 http://localhost:$(LH_PORT) --output html --output json \
	  --output-path ./lighthouse_report --chrome-flags="--headless" \
	  --only-categories=performance,accessibility,best-practices,seo; \
	kill $$(cat .serve_pid) && rm .serve_pid; \
	mv lighthouse_report.report.html lighthouse_report.html; \
	mv lighthouse_report.report.json lighthouse_report.json; \
	python3 scripts/lighthouse_to_md.py lighthouse_report.json lighthouse_report.md

clean:
	rm -rf $(PUBLIC_DIR) .bin
	rm -f lighthouse_report.html lighthouse_report.json lighthouse_report.md .serve_pid
