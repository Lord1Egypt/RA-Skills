#!/usr/bin/env sh
set -eu

# Keep mounted config paths predictable for the bundled router, bundled Ollama, and Dario proxy.
mkdir -p "${SAGE_ROUTER_HOME:-/config}" "${DARIO_HOME:-/config/dario}" "${OLLAMA_MODELS:-/config/ollama/models}"

ollama_ready() {
  curl -fsS --max-time 2 http://127.0.0.1:11434/api/tags >/dev/null 2>&1
}

# The image includes Ollama so a containerized router can satisfy an OpenClaw
# provider pointed at http://127.0.0.1:11434 without a separate Ollama service.
if [ "${SAGE_ROUTER_BUNDLED_OLLAMA_AUTOSTART:-1}" = "1" ] || [ "${SAGE_ROUTER_BUNDLED_OLLAMA_AUTOSTART:-1}" = "true" ]; then
  if command -v ollama >/dev/null 2>&1 && ! ollama_ready; then
    ollama serve >/tmp/ollama.log 2>&1 &
    for _i in $(seq 1 60); do
      ollama_ready && break
      sleep 0.5
    done
  fi
fi

# If caller passes a custom command, run it. Otherwise append --port from env
# only when the argument list does not already specify a port.
if [ "$#" -ge 1 ] && [ "$1" = "python3" ]; then
  for arg in "$@"; do
    if [ "$arg" = "--port" ]; then
      exec "$@"
    fi
  done
  exec "$@" --port "${PORT:-8790}"
fi
exec "$@"
