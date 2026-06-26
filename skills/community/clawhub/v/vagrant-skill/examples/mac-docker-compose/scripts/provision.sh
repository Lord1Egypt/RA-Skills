#!/usr/bin/env bash
# provision.sh — install Docker CE + Compose, build and run nginx + Python API stack
#
# WHY THIS NEEDS A VM (on Mac):
#   Docker Desktop requires a paid subscription for commercial teams. Even when
#   licensed, port 80/443 binding and /proc access go through a hyperkit shim
#   with restrictions. Docker CE inside a Parallels VM has none of these
#   limitations — full Linux kernel, real port bindings, no licensing risk.
#
# What this does:
#   1. Installs Docker CE + docker-compose-plugin (not Docker Desktop)
#   2. Writes a Python API (stdlib only — no pip, no external deps)
#   3. Writes nginx config that proxies /api/ to the Python API
#   4. Writes docker-compose.yml with nginx (port 80) + python-api (internal)
#   5. Builds the Python API image and starts the stack
set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info() { echo -e "${GREEN}[provision]${NC} $*"; }
warn() { echo -e "${YELLOW}[provision]${NC} $*"; }

# ── 1. Install Docker CE + Compose plugin ────────────────────────────────────
if command -v docker &>/dev/null; then
  info "Docker already installed: $(docker --version)"
else
  info "Installing Docker CE..."
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -qq
  apt-get install -y -qq ca-certificates curl gnupg

  install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
    -o /etc/apt/keyrings/docker.asc
  chmod a+r /etc/apt/keyrings/docker.asc

  # VERSION_CODENAME comes from /etc/os-release (noble on Ubuntu 24.04)
  # shellcheck source=/dev/null
  . /etc/os-release
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
    https://download.docker.com/linux/ubuntu ${VERSION_CODENAME} stable" \
    | tee /etc/apt/sources.list.d/docker.list > /dev/null

  apt-get update -qq
  # docker-compose-plugin is separate from docker-ce — must be listed explicitly
  apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-compose-plugin

  systemctl enable --now docker
  usermod -aG docker vagrant
  info "Docker CE installed"
fi

# Ensure compose plugin is present even if docker was pre-installed without it
if ! docker compose version &>/dev/null; then
  info "Installing docker-compose-plugin..."
  apt-get install -y -qq docker-compose-plugin
fi

# ── 2. Create stack directory ─────────────────────────────────────────────────
STACK_DIR="/opt/demo-stack"
mkdir -p "${STACK_DIR}"

# ── 3. Write Python API (stdlib only) ────────────────────────────────────────
info "Writing Python API..."
# Quoted heredoc: shellcheck does not parse the body as shell
cat > "${STACK_DIR}/api.py" << 'PYEOF'
#!/usr/bin/env python3
"""Minimal JSON API using only Python stdlib — no Flask, no pip required."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class APIHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # silence per-request stdout noise
        pass

    def do_GET(self):
        if self.path == "/healthz":
            body = json.dumps({"status": "ok"}).encode()
        elif self.path.startswith("/api"):
            body = json.dumps({"message": "hello from python-api", "path": self.path}).encode()
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "not found"}).encode())
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), APIHandler)
    server.serve_forever()
PYEOF

# ── 4. Write Dockerfile for the API ──────────────────────────────────────────
info "Writing Dockerfile.api..."
cat > "${STACK_DIR}/Dockerfile.api" << 'DFEOF'
FROM python:3.12-slim
WORKDIR /app
COPY api.py .
CMD ["python3", "api.py"]
DFEOF

# ── 5. Write nginx config ─────────────────────────────────────────────────────
info "Writing nginx.conf..."
cat > "${STACK_DIR}/nginx.conf" << 'NGINXEOF'
events {}

http {
    upstream python_api {
        server python-api:8000;
    }

    server {
        listen 80;
        server_name _;

        location /api/ {
            proxy_pass         http://python_api/api/;
            proxy_http_version 1.1;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
        }

        location /healthz {
            proxy_pass http://python_api/healthz;
        }

        location / {
            root  /usr/share/nginx/html;
            index index.html;
        }
    }
}
NGINXEOF

# ── 6. Write docker-compose.yml ───────────────────────────────────────────────
info "Writing docker-compose.yml..."
cat > "${STACK_DIR}/docker-compose.yml" << 'COMPOSEEOF'
services:
  nginx:
    image: nginx:1.27-alpine
    container_name: demo-nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      python-api:
        condition: service_healthy
    restart: unless-stopped

  python-api:
    build:
      context: .
      dockerfile: Dockerfile.api
    image: demo-python-api:local
    container_name: demo-python-api
    expose:
      - "8000"
    healthcheck:
      test: ["CMD", "python3", "-c",
             "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz')"]
      interval: 5s
      timeout: 3s
      retries: 5
      start_period: 5s
    restart: unless-stopped
COMPOSEEOF

# ── 7. Build and start the stack ─────────────────────────────────────────────
info "Building Python API image..."
cd "${STACK_DIR}"
docker compose build --quiet

info "Starting stack..."
docker compose up -d

# Wait for nginx on port 80 (up to 60s — image pull + healthcheck can be slow)
info "Waiting for nginx to be ready..."
i=0
while [ "$i" -lt 60 ]; do
  i=$((i + 1))
  if curl -sf http://localhost > /dev/null 2>&1; then
    info "Stack is ready"
    break
  fi
  if [ "$i" -eq 60 ]; then
    warn "Timeout — check: docker compose -f ${STACK_DIR}/docker-compose.yml logs"
    exit 1
  fi
  sleep 1
done

# ── 8. Confirm ────────────────────────────────────────────────────────────────
info "Running containers:"
docker compose ps

info "Done. Try:"
info "  vagrant ssh -c 'curl http://localhost'         -> nginx static page"
info "  vagrant ssh -c 'curl http://localhost/api/'    -> Python API via proxy"
info "  vagrant ssh -c 'curl http://localhost/healthz' -> health check"
