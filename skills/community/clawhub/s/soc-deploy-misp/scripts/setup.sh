#!/bin/bash
# Deploy MISP on any Docker-ready Linux host
# Usage: ./setup.sh [admin-email] [admin-password] [host-ram-gb]
# Run ON the target host (not remotely)

set -euo pipefail

ADMIN_EMAIL="${1:-admin@misp.local}"
PASSWORD="${2:-ChangeMe123!}"
HOST_RAM_GB="${3:-4}"
MISP_DIR=~/misp/misp-docker

echo "=== MISP Deployment ==="
echo "Admin: $ADMIN_EMAIL | RAM: ${HOST_RAM_GB}GB"
echo ""

# Calculate buffer pool size
case "$HOST_RAM_GB" in
  [1-5])  BUFFER_POOL="512M" ;;
  [6-9])  BUFFER_POOL="2048M" ;;
  1[0-9]) BUFFER_POOL="4096M" ;;
  *)      BUFFER_POOL="4096M" ;;
esac
echo "InnoDB buffer pool: $BUFFER_POOL (for ${HOST_RAM_GB}GB RAM)"

# Clone official misp-docker
echo "[1/6] Cloning misp-docker..."
mkdir -p ~/misp
if [ -d "$MISP_DIR" ]; then
  echo "  Already cloned, pulling latest..."
  cd "$MISP_DIR" && git pull --quiet
else
  git clone --quiet https://github.com/MISP/misp-docker.git "$MISP_DIR"
fi
cd "$MISP_DIR"

# Configure .env
echo "[2/6] Configuring .env..."
cp template.env .env

VM_IP=$(hostname -I | awk '{print $1}')
MYSQL_ROOT_PW=$(openssl rand -base64 24)
MYSQL_PW=$(openssl rand -base64 24)

sed -i "s|MISP_BASEURL=.*|MISP_BASEURL=http://${VM_IP}|" .env
sed -i "s|MISP_ADMIN_EMAIL=.*|MISP_ADMIN_EMAIL=${ADMIN_EMAIL}|" .env
sed -i "s|MISP_ADMIN_PASSPHRASE=.*|MISP_ADMIN_PASSPHRASE=${PASSWORD}|" .env

# Set DB passwords
grep -q "MYSQL_ROOT_PASSWORD" .env && \
  sed -i "s|MYSQL_ROOT_PASSWORD=.*|MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PW}|" .env || \
  echo "MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PW}" >> .env

grep -q "MYSQL_PASSWORD" .env && \
  sed -i "s|MYSQL_PASSWORD=.*|MYSQL_PASSWORD=${MYSQL_PW}|" .env || \
  echo "MYSQL_PASSWORD=${MYSQL_PW}" >> .env

# CRITICAL: Set InnoDB buffer pool to prevent MariaDB OOM
grep -q "INNODB_BUFFER_POOL_SIZE" .env && \
  sed -i "s|INNODB_BUFFER_POOL_SIZE=.*|INNODB_BUFFER_POOL_SIZE=${BUFFER_POOL}|" .env || \
  echo "INNODB_BUFFER_POOL_SIZE=${BUFFER_POOL}" >> .env

echo "  Configured for $VM_IP with buffer pool $BUFFER_POOL"

# Start stack
echo "[3/6] Starting Docker Compose stack..."
docker compose up -d

# Wait for MISP (5-10 min on first boot)
echo "[4/6] Waiting for MISP (first boot: 5-10 min)..."
for i in $(seq 1 60); do
  if curl -sk https://localhost/users/login 2>/dev/null | grep -q "login\|UserLoginForm"; then
    echo "  MISP is up! (~$((i * 10))s)"
    break
  fi
  if [ $i -eq 60 ]; then
    echo "  WARNING: Still not responding after 10 min."
    echo "  Check: docker compose logs misp"
  fi
  sleep 10
done

# Generate API key
echo "[5/6] Generating API key..."
sleep 5
API_KEY=$(docker compose exec -T misp /var/www/MISP/app/Console/cake user change_authkey "$ADMIN_EMAIL" 2>/dev/null | grep -oP '[a-zA-Z0-9]{40}' | head -1)

if [ -z "$API_KEY" ]; then
  echo "  WARNING: Key generation failed. Try manually:"
  echo "  docker compose exec misp /var/www/MISP/app/Console/cake user change_authkey $ADMIN_EMAIL"
  API_KEY="GENERATION_FAILED"
fi

# Verify
echo "[6/6] Verifying API..."
if [ "$API_KEY" != "GENERATION_FAILED" ]; then
  VER=$(curl -sk -H "Authorization: $API_KEY" -H "Accept: application/json" \
    https://localhost/servers/getVersion 2>/dev/null | grep -o '"version":"[^"]*"' || echo "")
  [ -n "$VER" ] && echo "  API verified! $VER" || echo "  Key generated but verify returned empty (may still be loading)"
fi

# Save credentials
cat > ~/misp/api-key.txt << EOF
=== MISP Credentials ===
Generated: $(date)

MISP URL: https://${VM_IP}
Admin: ${ADMIN_EMAIL} / ${PASSWORD}
API Key: ${API_KEY}

MCP Connection:
  MISP_URL=https://${VM_IP}
  MISP_API_KEY=${API_KEY}
  MISP_VERIFY_SSL=false

MySQL Root: ${MYSQL_ROOT_PW}
MySQL User: misp / ${MYSQL_PW}
InnoDB Buffer Pool: ${BUFFER_POOL}

Note: Self-signed HTTPS. Use curl -k for API calls.
EOF

echo ""
echo "=== MISP Deployment Complete ==="
echo ""
echo "URL:     https://${VM_IP}"
echo "Admin:   ${ADMIN_EMAIL} / ${PASSWORD}"
echo "API Key: ${API_KEY}"
echo ""
echo "Credentials saved to: ~/misp/api-key.txt"
