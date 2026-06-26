#!/bin/bash
# redis-manager — Gerencia o container Redis compartilhado via docker-compose.
#
# Uso:
#   ./run.sh start                   # sobe o container Redis
#   ./run.sh stop                    # para o container (dados persistem no volume)
#   ./run.sh status                  # mostra status e métricas básicas
#   ./run.sh flush                   # limpa todos os dados (FLUSHALL — pede confirmação)
#   ./run.sh flush-db <n>            # limpa banco N do Redis (SELECT N + FLUSHDB)
#   ./run.sh list-keys [<padrão>]    # lista chaves (padrão: *)
#   ./run.sh wait                    # aguarda Redis ficar pronto
#   ./run.sh cli                     # abre redis-cli interativo
#
# Variáveis de configuração (com defaults):
#   REDIS_CONTAINER  — nome do container (padrão: codai_redis)
#   REDIS_PASSWORD   — senha (padrão: redispass)
#   REDIS_PORT       — porta no host (padrão: 6380)
#   CODAI_NETWORK    — rede Docker compartilhada (padrão: nginx-proxy_net)

set -euo pipefail

ACTION="${1:-status}"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_FILE="$BASE_DIR/docker-compose.yml"

REDIS_CONTAINER="${REDIS_CONTAINER:-codai_redis}"
REDIS_PASSWORD="${REDIS_PASSWORD:-redispass}"
if [ "$REDIS_PASSWORD" = "redispass" ] && [ "${ACTION:-}" != "status" ] && [ "${ACTION:-}" != "wait" ] && [ "${ACTION:-}" != "cli" ]; then
    echo "Aviso: usando senha Redis padrão. Defina REDIS_PASSWORD para ambientes com dados reais."
fi

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

is_running() {
    docker ps --filter "name=^${REDIS_CONTAINER}$" --format '{{.Names}}' | grep -q "^${REDIS_CONTAINER}$"
}

require_running() {
    if ! is_running; then
        echo "Erro: container ${REDIS_CONTAINER} não está rodando."
        echo "      Execute: ./run.sh start"
        exit 1
    fi
}

redis_cmd() {
    docker exec "$REDIS_CONTAINER" redis-cli -a "$REDIS_PASSWORD" --no-auth-warning "$@" 2>/dev/null
}

wait_ready() {
    echo "Aguardando Redis ficar pronto..."
    until redis_cmd ping 2>/dev/null | grep -q "PONG"; do
        sleep 2
    done
    echo "Redis pronto."
}

# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------

case "$ACTION" in

    start)
        if is_running; then
            echo "Redis (${REDIS_CONTAINER}) já está rodando."
        else
            echo "Iniciando Redis..."
            docker compose -f "$COMPOSE_FILE" up -d
            wait_ready
            echo "Redis iniciado em localhost:${REDIS_PORT:-6380}"
        fi
        ;;

    stop)
        if ! is_running; then
            echo "Redis (${REDIS_CONTAINER}) não está rodando."
        else
            echo "Parando Redis (dados persistem no volume)..."
            docker compose -f "$COMPOSE_FILE" down
            echo "Redis parado."
        fi
        ;;

    status)
        if is_running; then
            echo "Redis (${REDIS_CONTAINER})  running  → localhost:${REDIS_PORT:-6380}"
            echo ""
            keys=$(redis_cmd DBSIZE || echo "?")
            mem=$(redis_cmd INFO memory | grep "used_memory_human:" | cut -d: -f2 | tr -d '[:space:]' || echo "?")
            echo "  Chaves: $keys"
            echo "  Memória usada: $mem"
        else
            echo "Redis (${REDIS_CONTAINER})  stopped"
            echo "  Execute: ./run.sh start"
        fi
        ;;

    wait)
        require_running
        wait_ready
        ;;

    flush)
        require_running
        read -r -p "FLUSHALL: remover TODOS os dados do Redis? Esta ação é irreversível. [s/N] " confirm
        if [[ "$confirm" =~ ^[sS]$ ]]; then
            redis_cmd FLUSHALL
            echo "Redis limpo."
        else
            echo "Cancelado."
        fi
        ;;

    flush-db)
        DB_NUM="${2:-}"
        if [ -z "$DB_NUM" ]; then
            echo "Uso: $0 flush-db <número-do-banco>"
            exit 1
        fi
        if [[ ! "$DB_NUM" =~ ^[0-9]+$ ]]; then
            echo "Erro: número de banco inválido: '$DB_NUM'. Use um inteiro não-negativo."
            exit 1
        fi
        require_running
        read -r -p "Limpar banco $DB_NUM do Redis? [s/N] " confirm
        if [[ "$confirm" =~ ^[sS]$ ]]; then
            docker exec "$REDIS_CONTAINER" redis-cli -a "$REDIS_PASSWORD" --no-auth-warning -n "$DB_NUM" FLUSHDB 2>/dev/null
            echo "Banco $DB_NUM limpo."
        else
            echo "Cancelado."
        fi
        ;;

    list-keys)
        PATTERN="${2:-*}"
        require_running
        redis_cmd KEYS "$PATTERN"
        ;;

    cli)
        require_running
        docker exec -it "$REDIS_CONTAINER" redis-cli -a "$REDIS_PASSWORD" --no-auth-warning
        ;;

    *)
        echo "Uso: $0 {start|stop|status|wait|flush|flush-db|list-keys|cli}"
        exit 1
        ;;
esac
