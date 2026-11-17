#!/bin/bash
# qwencloud · Docker app bootstrap
# Placeholders:
#   __APP_ARTIFACT_URL__   OSS signed URL of app image tar.gz (docker save output) or docker-compose.yml + build context tar.gz
#   __APP_MODE__           docker-image | docker-compose
#   __APP_PORT__           App container listening port (reverse-proxied by Nginx)
#   __APP_IMAGE_NAME__     Image name:tag after docker load in docker-image mode (e.g. myapp:latest)
#   __APP_NAME__           Service name (systemd unit / container name)
set -euxo pipefail

LOG=/var/log/qwencloud-bootstrap.log
exec >> "$LOG" 2>&1
echo "[$(date -u +%FT%TZ)] === qwencloud docker bootstrap start ==="

# 1. Install Docker
if ! command -v docker >/dev/null 2>&1; then
  if command -v dnf >/dev/null 2>&1; then
    dnf install -y docker
  elif command -v yum >/dev/null 2>&1; then
    yum install -y docker
  elif command -v apt-get >/dev/null 2>&1; then
    apt-get update && apt-get install -y docker.io
  fi
fi
systemctl enable docker
systemctl start docker

APP_URL="__APP_ARTIFACT_URL__"
APP_MODE="__APP_MODE__"
APP_PORT="__APP_PORT__"
IMAGE_NAME="__APP_IMAGE_NAME__"
APP_NAME="__APP_NAME__"

mkdir -p /opt/qwencloud
cd /opt/qwencloud
curl -fsSL "$APP_URL" -o app.tar.gz

# If RDS bootstrap wrote db.env, mount it into the container at startup
DB_ENV_OPT=""
[ -f /etc/qwencloud/db.env ] && DB_ENV_OPT="--env-file /etc/qwencloud/db.env"

if [ "$APP_MODE" = "docker-image" ]; then
  # Extract and docker load
  tar -xzf app.tar.gz
  # After docker load, make sure the image tag matches IMAGE_NAME: the tag baked
  # into the artifact tar may differ from IMAGE_NAME, in which case the unit's
  # ExecStart would fail to find / run the wrong image. Retag based on the load result.
  LOAD_OUT=$(docker load -i image.tar)
  echo "$LOAD_OUT"
  LOADED_REF=$(echo "$LOAD_OUT" | sed -n 's/^Loaded image: //p' | head -1)
  [ -z "$LOADED_REF" ] && LOADED_REF=$(echo "$LOAD_OUT" | sed -n 's/^Loaded image ID: //p' | head -1)
  if [ -n "$LOADED_REF" ] && [ "$LOADED_REF" != "${IMAGE_NAME}" ]; then
    docker tag "$LOADED_REF" "${IMAGE_NAME}"
  fi
  # Write systemd unit for persistent management
  cat > /etc/systemd/system/${APP_NAME}.service <<UNIT
[Unit]
Description=${APP_NAME} app container
After=docker.service
Requires=docker.service

[Service]
Restart=always
ExecStartPre=-/usr/bin/docker rm -f ${APP_NAME}
ExecStart=/usr/bin/docker run --rm --name ${APP_NAME} -p ${APP_PORT}:${APP_PORT} ${DB_ENV_OPT} ${IMAGE_NAME}
ExecStop=/usr/bin/docker stop ${APP_NAME}

[Install]
WantedBy=multi-user.target
UNIT
  systemctl daemon-reload
  systemctl enable ${APP_NAME}
  systemctl restart ${APP_NAME}

elif [ "$APP_MODE" = "docker-compose" ]; then
  # Extract (contains docker-compose.yml and build context or pre-built image tar)
  tar -xzf app.tar.gz
  # Install docker compose plugin (if not already available)
  if ! docker compose version >/dev/null 2>&1; then
    mkdir -p /usr/local/lib/docker/cli-plugins
    curl -fsSL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
      -o /usr/local/lib/docker/cli-plugins/docker-compose
    chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
  fi
  # compose auto-loads .env from the same directory; if RDS env exists, export it to .env.
  # db.env is 0600 (holds the DB password); use install -m 600 to preserve perms,
  # otherwise a plain cp lands it as 0644 and exposes the secret to other local users.
  if [ -f /etc/qwencloud/db.env ]; then
    install -m 600 /etc/qwencloud/db.env ./.env
  fi
  docker compose -f docker-compose.yml up -d
fi

echo "[$(date -u +%FT%TZ)] docker app up"
