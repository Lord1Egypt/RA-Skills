---
name: vps-deploy
description: "Deploy a full-stack app to any VPS from zero to production in one command. Handles SSH hardening, firewall, Docker, Nginx reverse proxy, SSL certificates, and health verification. Works with any stack (Node.js, Python, Go, Next.js) and any VPS provider (Hostinger, DigitalOcean, Hetzner, Linode, Vultr). Use when the user says 'deploy to VPS', 'set up my server', 'deploy to production', 'configure my VPS', or needs to go from a bare Ubuntu/Debian server to a running production app."
---

# VPS Deploy

Deploy any application to any VPS — from bare server to production with SSL — in one session.

## When to Use

- User has a VPS (Ubuntu/Debian) and wants to deploy an application
- User says "deploy to VPS", "set up my server", "go to production"
- User has a running app locally and wants it live on a server
- User needs SSL, Nginx, Docker setup on a VPS

## When NOT to Use

- Deploying to Vercel, Netlify, or other managed platforms (use their CLIs)
- Deploying to Kubernetes (use `/k8s-deploy` if it exists)
- The user just wants to push code (use `git push`)

## Prerequisites

- SSH access to a VPS (IP address + root or sudo credentials)
- A domain pointed to the VPS IP (for SSL — can skip SSL if no domain)
- The app must have a Dockerfile or be deployable via Docker

## Execution Flow

### Phase 1: Gather Information

Ask the user for (skip what you can detect):

1. **VPS IP address** and **SSH credentials** (root password or key path)
2. **Domain name** (optional — needed for SSL)
3. **Application type** — detect from the current directory if possible:
   - Look for `package.json` (Node.js/Next.js)
   - Look for `requirements.txt` / `pyproject.toml` (Python)
   - Look for `go.mod` (Go)
   - Look for `Dockerfile` (any)
4. **Port** the app runs on (detect from Dockerfile EXPOSE, or ask)
5. **Environment variables** needed (check `.env.local`, `.env.example`)
6. **Database requirements** (Postgres, MySQL, Redis, MongoDB — detect from dependencies)

### Phase 2: Server Setup (SSH into VPS)

Run these via `ssh root@<IP>` commands. Chain with `&&` for safety.

#### 2a. System Update
```bash
apt update && apt upgrade -y
```

#### 2b. Create Deploy User
```bash
adduser --disabled-password --gecos "" deploy
usermod -aG sudo docker deploy
echo "deploy ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/deploy
```

#### 2c. SSH Hardening
```bash
# Copy root's authorized_keys to deploy user
mkdir -p /home/deploy/.ssh
cp ~/.ssh/authorized_keys /home/deploy/.ssh/ 2>/dev/null || true
chown -R deploy:deploy /home/deploy/.ssh
chmod 700 /home/deploy/.ssh
chmod 600 /home/deploy/.ssh/authorized_keys 2>/dev/null || true

# Harden SSH config
sed -i 's/#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/#\?PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config
systemctl restart sshd
```

**CRITICAL:** Before disabling root login, verify the deploy user can SSH in. Test in a separate connection. If the user doesn't have SSH keys set up, help them first.

#### 2d. Firewall (UFW)
```bash
apt install -y ufw
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw --force enable
```

#### 2e. Install Docker
```bash
curl -fsSL https://get.docker.com | sh
usermod -aG docker deploy
```

#### 2f. Install Docker Compose (v2)
```bash
apt install -y docker-compose-plugin
# Verify
docker compose version
```

### Phase 3: Application Deployment

#### 3a. Generate Dockerfile (if none exists)

Detect the stack and generate an appropriate multi-stage Dockerfile:

**Node.js / Next.js:**
```dockerfile
FROM node:22-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev

FROM node:22-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
```

**Python (FastAPI/Flask):**
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Adapt based on what you detect in the project.

#### 3b. Generate docker-compose.yml

Generate a **production-grade** compose file. Include:

```yaml
services:
  app:
    build: .
    restart: unless-stopped
    ports:
      - "127.0.0.1:${APP_PORT:-3000}:${APP_PORT:-3000}"
    env_file: .env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:${APP_PORT:-3000}/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  # Add database services based on detection:
  # postgres:
  #   image: postgres:16-alpine
  #   restart: unless-stopped
  #   volumes:
  #     - pgdata:/var/lib/postgresql/data
  #   environment:
  #     POSTGRES_DB: ${DB_NAME:-app}
  #     POSTGRES_USER: ${DB_USER:-app}
  #     POSTGRES_PASSWORD: ${DB_PASSWORD}
  #   healthcheck:
  #     test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-app}"]
  #     interval: 10s
  #     timeout: 5s
  #     retries: 5

# volumes:
#   pgdata:
```

Key rules:
- **Always** bind app port to `127.0.0.1` (Nginx handles external traffic)
- **Always** include health checks
- **Always** include resource limits
- **Always** include logging limits
- **Always** use `restart: unless-stopped`
- **Never** expose database ports to the host

#### 3c. Transfer Files to VPS

```bash
# Create app directory
ssh deploy@<IP> "mkdir -p ~/apps/<app-name>"

# Copy project files (exclude node_modules, .git, etc.)
rsync -avz --exclude='node_modules' --exclude='.git' --exclude='.next' \
  ./ deploy@<IP>:~/apps/<app-name>/
```

#### 3d. Build and Start

```bash
ssh deploy@<IP> "cd ~/apps/<app-name> && docker compose up -d --build"
```

### Phase 4: Nginx Reverse Proxy

```bash
apt install -y nginx

# Generate site config
cat > /etc/nginx/sites-available/<domain> << 'EOF'
server {
    listen 80;
    server_name <domain>;

    location / {
        proxy_pass http://127.0.0.1:<APP_PORT>;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 86400;
    }
}
EOF

ln -sf /etc/nginx/sites-available/<domain> /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
```

### Phase 5: SSL Certificate (Let's Encrypt)

Skip if no domain provided.

```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d <domain> --non-interactive --agree-tos -m <email>
# Auto-renewal is configured automatically by certbot
```

### Phase 6: Verification

Run these checks and report results:

```bash
# Check Docker containers are running
docker compose ps

# Check health status
docker inspect --format='{{.State.Health.Status}}' <container-name>

# Check Nginx is serving
curl -sI https://<domain> | head -5

# Check SSL certificate
echo | openssl s_client -servername <domain> -connect <domain>:443 2>/dev/null | openssl x509 -noout -dates
```

Report to the user:
- Container status (running/healthy)
- HTTP response code
- SSL expiry date
- URL to visit

## Safety Rules

- **NEVER** disable the firewall without asking
- **NEVER** expose database ports to the internet
- **ALWAYS** verify SSH access with the deploy user BEFORE disabling root login
- **ALWAYS** back up existing Nginx configs before overwriting
- **ALWAYS** run `nginx -t` before reloading Nginx
- **ALWAYS** ask before running destructive commands (rm, drop, etc.)
- If anything fails, stop and tell the user what went wrong. Don't chain workarounds.

## Troubleshooting

- **Port already in use:** `lsof -i :<port>` to find what's using it
- **Docker build fails:** Check Dockerfile, show build logs
- **SSL fails:** Verify domain DNS points to VPS IP (`dig <domain>`)
- **App crashes:** `docker compose logs -f` to show logs
- **Can't SSH as deploy user:** Don't disable root login yet, fix keys first

## Post-Deploy Checklist

Tell the user to:
1. Set up monitoring (suggest Uptime Kuma)
2. Configure automated backups for database volumes
3. Set up log rotation (already configured in compose)
4. Consider a CI/CD pipeline (suggest `/ci-gen` skill)
5. Add the domain to their DNS if not done
