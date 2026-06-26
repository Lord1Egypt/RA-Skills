#!/bin/bash
# redis-commander — Gerencia o container Redis Commander via docker-compose.
#
# Uso:
#   ./run.sh start    # sobe o container Redis Commander
#   ./run.sh stop     # para o container
#   ./run.sh status   # mostra status e URL de acesso
#   ./run.sh open     # imprime URL de acesso
#
# Variáveis de configuração (com defaults):
#   COMMANDER_CONTAINER — nome do container (padrão: codai_redis_commander)
#   COMMANDER_PORT      — porta no host (padrão: 8083)
#   COMMANDER_USER      — usuário HTTP Basic Auth (padrão: admin)
#   COMMANDER_PASSWORD  — senha HTTP Basic Auth (padrão: admin)
#   REDIS_CONTAINER     — hostname do Redis na rede Docker (padrão: codai_redis)
#   REDIS_PASSWORD      — senha do Redis (padrão: redispass)
#   CODAI_NETWORK       — rede Docker compartilhada (padrão: nginx-proxy_net)

set -euo pipefail

ACTION="${1:-status}"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_FILE="$BASE_DIR/docker-compose.yml"

COMMANDER_CONTAINER="${COMMANDER_CONTAINER:-codai_redis_commander}"
COMMANDER_PORT="${COMMANDER_PORT:-8083}"
COMMANDER_USER="${COMMANDER_USER:-admin}"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

is_running() {
    docker ps --filter "name=^${COMMANDER_CONTAINER}$" --format '{{.Names}}' | grep -q "^${COMMANDER_CONTAINER}$"
}

# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------

case "$ACTION" in

    start)
        if is_running; then
            echo "Redis Commander (${COMMANDER_CONTAINER}) já está rodando → http://localhost:${COMMANDER_PORT}"
        else
            echo "Iniciando Redis Commander..."
            docker compose -f "$COMPOSE_FILE" up -d
            echo "Redis Commander iniciado → http://localhost:${COMMANDER_PORT}"
            echo "  Login: ${COMMANDER_USER} / \${COMMANDER_PASSWORD:-admin}"
        fi
        ;;

    stop)
        if ! is_running; then
            echo "Redis Commander (${COMMANDER_CONTAINER}) não está rodando."
        else
            echo "Parando Redis Commander..."
            docker compose -f "$COMPOSE_FILE" down
            echo "Redis Commander parado."
        fi
        ;;

    status)
        if is_running; then
            echo "Redis Commander (${COMMANDER_CONTAINER})  running  → http://localhost:${COMMANDER_PORT}"
        else
            echo "Redis Commander (${COMMANDER_CONTAINER})  stopped"
            echo "  Execute: ./run.sh start"
        fi
        ;;

    open)
        echo "http://localhost:${COMMANDER_PORT}"
        ;;

    *)
        echo "Uso: $0 {start|stop|status|open}"
        exit 1
        ;;
esac
