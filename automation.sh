#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/RogerHuauya/XDrive.git}"
PROJECT_DIR="${PROJECT_DIR:-XDrive}"

print_help() {
  cat <<'HELP'
Uso: ./automation.sh <comando>

Comandos:
  clone       Clona el repositorio público definido en REPO_URL.
  test        Instala dependencias y ejecuta pruebas unitarias Django.
  run-local   Ejecuta migraciones y levanta la aplicación localmente.
  docker-up   Construye y levanta los contenedores con Docker Compose.
  help        Muestra esta ayuda.

Variables opcionales:
  REPO_URL      URL del repositorio a clonar. Valor por defecto: https://github.com/RogerHuauya/XDrive.git
  PROJECT_DIR  Carpeta destino del clone. Valor por defecto: XDrive
HELP
}

ensure_env_file() {
  if [[ ! -f .env && -f .env.example ]]; then
    cp .env.example .env
    echo "Archivo .env creado desde .env.example"
  fi
}

clone_project() {
  if [[ -d "$PROJECT_DIR" ]]; then
    echo "La carpeta $PROJECT_DIR ya existe. Actualizando con git pull..."
    git -C "$PROJECT_DIR" pull
  else
    git clone "$REPO_URL" "$PROJECT_DIR"
  fi
}

run_tests() {
  ensure_env_file
  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt
  python manage.py test upload tests
}

run_local() {
  ensure_env_file
  python manage.py migrate
  python manage.py runserver 0.0.0.0:8000
}

compose_command() {
  if docker compose version >/dev/null 2>&1; then
    docker compose "$@"
  else
    docker-compose "$@"
  fi
}

run_docker() {
  ensure_env_file
  compose_command up --build
}

case "${1:-help}" in
  clone)
    clone_project
    ;;
  test)
    run_tests
    ;;
  run-local)
    run_local
    ;;
  docker-up)
    run_docker
    ;;
  help|-h|--help)
    print_help
    ;;
  *)
    echo "Comando no reconocido: $1" >&2
    print_help
    exit 1
    ;;
esac
