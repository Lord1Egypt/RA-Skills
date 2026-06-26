#!/bin/bash
# proxy-manager — Gerencia o nginx-proxy e a rede Docker compartilhada.
#
# O nginx-proxy (jwilder/nginx-proxy) detecta containers com label VIRTUAL_HOST
# e cria rotas automaticamente. Este script também gerencia a conexão da rede
# compartilhada entre o proxy e os containers das instâncias de desenvolvimento.
#
# Uso:
#   ./run.sh start                       # sobe o nginx-proxy e cria a rede codai_net
#   ./run.sh stop                        # para o nginx-proxy
#   ./run.sh status                      # mostra status e rotas ativas
#   ./run.sh connect <instância>         # conecta proxy à rede da instância
#   ./run.sh disconnect <instância>      # desconecta proxy da rede da instância
#   ./run.sh auto-connect                # conecta proxy a todas as redes de projeto
#   ./run.sh reload                      # recarrega config do nginx (sem restart)
#
# Variáveis de configuração (com defaults):
#   PROXY_CONTAINER  — nome do container proxy (padrão: codai_nginx_proxy)
#   CODAI_NETWORK    — nome da rede Docker compartilhada (padrão: nginx-proxy_net)
#   PROJECT_PREFIX   — prefixo dos projetos docker compose (padrão: codai-dev)

set -euo pipefail

ACTION="${1:-status}"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_FILE="$BASE_DIR/docker-compose.yml"

PROXY_CONTAINER="${PROXY_CONTAINER:-codai_nginx_proxy}"
CODAI_NETWORK="${CODAI_NETWORK:-nginx-proxy_net}"
PROJECT_PREFIX="${PROJECT_PREFIX:-codai-dev}"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

is_running() {
    docker ps --filter "name=^${PROXY_CONTAINER}$" --format '{{.Names}}' | grep -q "^${PROXY_CONTAINER}$"
}

require_running() {
    if ! is_running; then
        echo "Erro: container ${PROXY_CONTAINER} não está rodando."
        echo "      Execute: ./run.sh start"
        exit 1
    fi
}

network_for() {
    local instance="$1"
    echo "${PROJECT_PREFIX}-${instance}_default"
}

is_connected() {
    local net="$1"
    docker network inspect "$net" --format '{{range .Containers}}{{.Name}}{{"\n"}}{{end}}' 2>/dev/null \
        | grep -q "^${PROXY_CONTAINER}$"
}

reload_nginx() {
    docker exec "$PROXY_CONTAINER" nginx -s reload 2>/dev/null || true
}

# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------

case "$ACTION" in

    start)
        if is_running; then
            echo "nginx-proxy (${PROXY_CONTAINER}) já está rodando."
        else
            echo "Iniciando nginx-proxy..."
            docker compose -f "$COMPOSE_FILE" up -d
            echo "nginx-proxy iniciado. Rede: ${CODAI_NETWORK}"
        fi
        ;;

    stop)
        if ! is_running; then
            echo "nginx-proxy (${PROXY_CONTAINER}) não está rodando."
        else
            echo "Parando nginx-proxy..."
            docker compose -f "$COMPOSE_FILE" down
            echo "nginx-proxy parado."
        fi
        ;;

    status)
        if is_running; then
            echo "nginx-proxy (${PROXY_CONTAINER})  running  → localhost:80"
            echo ""
            echo "Redes conectadas:"
            for net in $(docker network ls --format '{{.Name}}'); do
                if is_connected "$net" 2>/dev/null; then
                    echo "  $net"
                fi
            done
            echo ""
            echo "Rotas ativas (VIRTUAL_HOST):"
            docker ps --filter "label=VIRTUAL_HOST" \
                --format '  {{index .Labels "com.docker.compose.project"}}  {{index .Labels "VIRTUAL_HOST"}}' \
                2>/dev/null || echo "  (nenhuma)"
        else
            echo "nginx-proxy (${PROXY_CONTAINER})  stopped"
            echo "  Execute: ./run.sh start"
        fi
        ;;

    connect)
        INSTANCE="${2:-}"
        if [ -z "$INSTANCE" ]; then
            echo "Uso: $0 connect <instância>"
            exit 1
        fi
        require_running
        NET="$(network_for "$INSTANCE")"
        if ! docker network ls --format '{{.Name}}' | grep -q "^${NET}$"; then
            echo "Rede ${NET} não encontrada."
            echo "  Inicie a instância primeiro: worktree-manager start $INSTANCE"
            exit 1
        fi
        if is_connected "$NET"; then
            echo "nginx-proxy já está conectado a ${NET}."
        else
            docker network connect "$NET" "$PROXY_CONTAINER"
            reload_nginx
            echo "Conectado: ${PROXY_CONTAINER} → ${NET}"
            echo ""
            echo "Rotas disponíveis:"
            echo "  http://${INSTANCE}.frontend.localhost"
            echo "  http://${INSTANCE}.backend.localhost"
        fi
        ;;

    disconnect)
        INSTANCE="${2:-}"
        if [ -z "$INSTANCE" ]; then
            echo "Uso: $0 disconnect <instância>"
            exit 1
        fi
        require_running
        NET="$(network_for "$INSTANCE")"
        docker network disconnect "$NET" "$PROXY_CONTAINER" 2>/dev/null || true
        reload_nginx
        echo "Desconectado: ${PROXY_CONTAINER} → ${NET}"
        ;;

    auto-connect)
        require_running
        mapfile -t nets < <(docker network ls --format '{{.Name}}' | grep "^${PROJECT_PREFIX}-.*_default$")
        if [ "${#nets[@]}" -eq 0 ]; then
            echo "Nenhuma rede '${PROJECT_PREFIX}-*_default' encontrada."
            exit 0
        fi
        echo "Redes encontradas com prefixo '${PROJECT_PREFIX}':"
        for net in "${nets[@]}"; do echo "  $net"; done
        read -r -p "Conectar proxy a essas ${#nets[@]} rede(s)? [s/N] " confirm
        if [[ ! "$confirm" =~ ^[sS]$ ]]; then
            echo "Cancelado."
            exit 0
        fi
        connected=0
        for net in "${nets[@]}"; do
            if ! is_connected "$net"; then
                docker network connect "$net" "$PROXY_CONTAINER" 2>/dev/null || true
                echo "Conectado: $net"
                ((connected++)) || true
            fi
        done
        if [ "$connected" -gt 0 ]; then
            reload_nginx
            echo "${connected} rede(s) conectada(s). Rotas ativas."
        else
            echo "Todas as redes já estavam conectadas."
        fi
        ;;

    reload)
        require_running
        reload_nginx
        echo "nginx recarregado."
        ;;

    *)
        echo "Uso: $0 {start|stop|status|connect|disconnect|auto-connect|reload} [instância]"
        exit 1
        ;;
esac
