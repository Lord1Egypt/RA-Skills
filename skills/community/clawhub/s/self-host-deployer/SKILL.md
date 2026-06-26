---
name: self-host
description: "Deploy self-hosted applications to any VPS with Docker Compose. Catalog of 18 apps with production-ready configs, Nginx reverse proxy, SSL via Certbot, automated backups, resource limits, and health checks. Use when the user says 'self-host', 'deploy supabase', 'deploy plausible', 'deploy n8n', 'self-hosted', 'host my own', 'deploy umami', 'deploy uptime kuma', 'deploy gitea', 'deploy vaultwarden', 'deploy ghost', 'deploy langfuse', 'deploy ghostfolio', 'deploy minio', 'deploy immich', 'deploy paperless', 'deploy coolify', 'deploy stirling pdf'."
---

# Self-Host Deployer

Deploy production-ready self-hosted applications to any VPS with Docker Compose, Nginx, SSL, backups, and health checks.

## When to Use

- User wants to self-host an open-source application
- User says "self-host", "deploy X", "host my own X"
- User wants a privacy-respecting alternative to a SaaS product

## When NOT to Use

- Deploying custom application code (use `/vps-deploy`)
- Deploying to managed platforms like Vercel/Netlify
- User wants the hosted/cloud version of a service

## Prerequisites

- SSH access to a VPS (Ubuntu/Debian with Docker + Docker Compose installed)
- A domain or subdomain pointed to the VPS IP (for SSL)
- Minimum 1GB RAM (some apps need more — see catalog)

---

## Phase 1: App Selection

Present the catalog and ask the user which app to deploy. If the user already named an app, skip to Phase 2.

### App Catalog

| # | App | Category | Description | Min RAM | Ports | Database |
|---|-----|----------|-------------|---------|-------|----------|
| 1 | **Supabase** | Backend/BaaS | Open-source Firebase alternative (Postgres, Auth, REST, Realtime, Storage) | 4GB | 3000, 8000 | Postgres (built-in) |
| 2 | **Plausible** | Analytics | Privacy-friendly web analytics, no cookies | 4GB | 8000 | Postgres + ClickHouse |
| 3 | **Umami** | Analytics | Lightweight privacy-focused analytics (~2KB script) | 512MB | 3000 | Postgres |
| 4 | **Uptime Kuma** | Monitoring | Self-hosted uptime monitoring (like Uptime Robot) | 256MB | 3001 | SQLite (built-in) |
| 5 | **n8n** | Automation | Workflow automation platform (like Zapier) | 1GB | 5678 | Postgres |
| 6 | **Gitea** | Dev Tools | Lightweight Git server with CI (like GitHub) | 512MB | 3000, 22 | Postgres |
| 7 | **Vaultwarden** | Security | Bitwarden-compatible password manager (Rust) | 128MB | 80 | SQLite (built-in) |
| 8 | **Ghostfolio** | Finance | Open-source wealth management dashboard | 1GB | 3333 | Postgres + Redis |
| 9 | **Langfuse** | AI/LLM | LLM observability and tracing platform | 4GB | 3000 | Postgres + ClickHouse + Redis |
| 10 | **Ghost** | CMS | Professional publishing platform with ActivityPub | 1GB | 2368 | MySQL |
| 11 | **MinIO** | Storage | S3-compatible object storage (NOTE: archived Feb 2026 — consider Garage or SeaweedFS) | 1GB | 9000, 9001 | None |
| 12 | **Immich** | Photos | Self-hosted Google Photos alternative with AI | 4GB | 2283 | Postgres + Redis |
| 13 | **Paperless-ngx** | Documents | Document management with OCR and auto-tagging | 2GB | 8000 | Postgres + Redis |
| 14 | **Coolify** | PaaS | Open-source Heroku/Netlify alternative (280+ one-click apps) | 2GB | 8000 | Built-in |
| 15 | **Stirling PDF** | Documents | All-in-one PDF tool (merge, split, OCR, convert) | 512MB | 8080 | None |
| 16 | **Nginx Proxy Manager** | Infrastructure | Visual reverse proxy manager with Let's Encrypt | 256MB | 80, 443, 81 | SQLite |
| 17 | **Portainer** | Infrastructure | Docker management GUI | 256MB | 9000, 9443 | Built-in |
| 18 | **Dockge** | Infrastructure | Docker Compose stack manager (by Uptime Kuma creator) | 256MB | 5001 | Built-in |

---

## Phase 2: Gather Information

Ask the user for:

1. **VPS IP address** and **SSH credentials** (root or sudo user)
2. **Domain/subdomain** for the app (e.g., `analytics.example.com`)
3. **Email address** for SSL certificate registration (Certbot)
4. Any **app-specific settings** (see gotchas per app below)

---

## Phase 3: Generate Docker Compose

Based on the selected app, generate a `docker-compose.yml` with:
- Proper service definitions and dependencies
- Named volumes for all persistent data
- A shared Docker network (`web` for proxy, `internal` for inter-service)
- Resource limits via `deploy.resources.limits`
- Health checks on all services
- Automatic restart policies (`unless-stopped`)
- Secure randomly-generated passwords for all secrets

### Docker Compose Templates

#### 1. Supabase

**Gotchas:** Supabase has 11+ services (Postgres, GoTrue, PostgREST, Realtime, Storage, Studio, Kong, Meta, Edge Functions, Analytics/Logflare, Imgproxy). Do NOT write a compose from scratch. Clone the official repo and customize `.env`.

```bash
# Clone official Supabase Docker setup
git clone --depth 1 https://github.com/supabase/supabase /opt/supabase
cd /opt/supabase/docker

# Copy and configure environment
cp .env.example .env
```

**Critical `.env` changes:**
```env
POSTGRES_PASSWORD=<GENERATE_STRONG_PASSWORD>
JWT_SECRET=<GENERATE_32_CHAR_SECRET>
ANON_KEY=<GENERATE_JWT_FROM_SECRET>
SERVICE_ROLE_KEY=<GENERATE_JWT_FROM_SECRET>
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=<GENERATE_STRONG_PASSWORD>
SITE_URL=https://<DOMAIN>
API_EXTERNAL_URL=https://<DOMAIN>
```

Generate JWT keys:
```bash
# Generate JWT_SECRET
openssl rand -base64 32

# Generate ANON_KEY and SERVICE_ROLE_KEY using the JWT_SECRET
# Use https://supabase.com/docs/guides/self-hosting#api-keys or:
# npm install -g jsonwebtoken && node -e "const jwt=require('jsonwebtoken'); console.log(jwt.sign({role:'anon',iss:'supabase',iat:Math.floor(Date.now()/1000),exp:Math.floor(Date.now()/1000)+315360000},process.env.JWT_SECRET))"
```

**Health check:** `curl -f http://localhost:3000` (Studio) and `curl -f http://localhost:8000/rest/v1/` (API via Kong)

---

#### 2. Plausible

**Gotchas:** Requires ClickHouse for event storage. The CE version is released twice per year. CPU must support SSE 4.2 (check with `grep -q sse4_2 /proc/cpuinfo`).

```yaml
services:
  plausible:
    image: ghcr.io/plausible/community-edition:v2-latest
    container_name: plausible
    restart: unless-stopped
    command: sh -c "sleep 10 && /entrypoint.sh db createdb && /entrypoint.sh db migrate && /entrypoint.sh run"
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      - BASE_URL=https://${DOMAIN}
      - SECRET_KEY_BASE=${SECRET_KEY_BASE}
      - DATABASE_URL=postgres://plausible:${DB_PASSWORD}@plausible-db:5432/plausible
      - CLICKHOUSE_DATABASE_URL=http://plausible-events-db:8123/plausible_events
    depends_on:
      plausible-db:
        condition: service_healthy
      plausible-events-db:
        condition: service_healthy
    networks:
      - internal
      - web
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: "2.0"

  plausible-db:
    image: postgres:16-alpine
    container_name: plausible-db
    restart: unless-stopped
    volumes:
      - plausible-db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=plausible
      - POSTGRES_USER=plausible
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U plausible"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - internal
    deploy:
      resources:
        limits:
          memory: 512M

  plausible-events-db:
    image: clickhouse/clickhouse-server:24-alpine
    container_name: plausible-events-db
    restart: unless-stopped
    volumes:
      - plausible-events-data:/var/lib/clickhouse
      - ./clickhouse/clickhouse-config.xml:/etc/clickhouse-server/config.d/logging.xml:ro
      - ./clickhouse/clickhouse-user-config.xml:/etc/clickhouse-server/users.d/logging.xml:ro
    ulimits:
      nofile:
        soft: 262144
        hard: 262144
    healthcheck:
      test: ["CMD-SHELL", "wget --no-verbose --tries=1 --spider http://localhost:8123/ping || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - internal
    deploy:
      resources:
        limits:
          memory: 1G

volumes:
  plausible-db-data:
  plausible-events-data:

networks:
  internal:
  web:
    external: true
```

Create ClickHouse config files:
```bash
mkdir -p clickhouse
cat > clickhouse/clickhouse-config.xml << 'XMLEOF'
<clickhouse>
  <logger>
    <level>warning</level>
    <console>true</console>
  </logger>
  <query_thread_log remove="remove"/>
  <query_log remove="remove"/>
  <text_log remove="remove"/>
  <trace_log remove="remove"/>
  <metric_log remove="remove"/>
  <asynchronous_metric_log remove="remove"/>
  <session_log remove="remove"/>
  <part_log remove="remove"/>
</clickhouse>
XMLEOF

cat > clickhouse/clickhouse-user-config.xml << 'XMLEOF'
<clickhouse>
  <profiles>
    <default>
      <log_queries>0</log_queries>
      <log_query_threads>0</log_query_threads>
    </default>
  </profiles>
</clickhouse>
XMLEOF
```

**Health check:** `curl -f http://localhost:8000/api/health`

---

#### 3. Umami

```yaml
services:
  umami:
    image: ghcr.io/umami-software/umami:postgresql-latest
    container_name: umami
    restart: unless-stopped
    ports:
      - "127.0.0.1:3000:3000"
    environment:
      DATABASE_URL: postgres://umami:${DB_PASSWORD}@umami-db:5432/umami
      APP_SECRET: ${APP_SECRET}
    depends_on:
      umami-db:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:3000/api/heartbeat || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - internal
      - web
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "1.0"

  umami-db:
    image: postgres:16-alpine
    container_name: umami-db
    restart: unless-stopped
    volumes:
      - umami-db-data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: umami
      POSTGRES_USER: umami
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U umami"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - internal
    deploy:
      resources:
        limits:
          memory: 256M

volumes:
  umami-db-data:

networks:
  internal:
  web:
    external: true
```

**Health check:** `curl -f http://localhost:3000/api/heartbeat`
**Default login:** admin / umami (change immediately)

---

#### 4. Uptime Kuma

```yaml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:2
    container_name: uptime-kuma
    restart: unless-stopped
    ports:
      - "127.0.0.1:3001:3001"
    volumes:
      - uptime-kuma-data:/app/data
      - /var/run/docker.sock:/var/run/docker.sock:ro
    healthcheck:
      test: ["CMD-SHELL", "extra/healthcheck"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - web
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: "0.5"

volumes:
  uptime-kuma-data:

networks:
  web:
    external: true
```

**Gotchas:** Mounting Docker socket is optional but enables container monitoring. First visit creates the admin account.
**Health check:** `curl -f http://localhost:3001/api/status-page/heartbeat`

---

#### 5. n8n

**Gotchas:** `N8N_ENCRYPTION_KEY` encrypts credentials at rest. Set before first run and NEVER lose it. Use Postgres for production, not SQLite.

```yaml
services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n
    restart: unless-stopped
    ports:
      - "127.0.0.1:5678:5678"
    environment:
      - N8N_HOST=${DOMAIN}
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://${DOMAIN}/
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=n8n-db
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=${DB_PASSWORD}
      - GENERIC_TIMEZONE=${TIMEZONE:-America/New_York}
    volumes:
      - n8n-data:/home/node/.n8n
    depends_on:
      n8n-db:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "wget --no-verbose --tries=1 --spider http://localhost:5678/healthz || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - internal
      - web
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "2.0"

  n8n-db:
    image: postgres:16-alpine
    container_name: n8n-db
    restart: unless-stopped
    volumes:
      - n8n-db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=n8n
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U n8n"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - internal
    deploy:
      resources:
        limits:
          memory: 512M

volumes:
  n8n-data:
  n8n-db-data:

networks:
  internal:
  web:
    external: true
```

**Health check:** `curl -f http://localhost:5678/healthz`

---

#### 6. Gitea

**Gotchas:** Uses port 22 for SSH — change the host SSH port first (e.g., to 2222) or map Gitea SSH to another port. Forgejo is a community fork worth considering.

```yaml
services:
  gitea:
    image: gitea/gitea:latest
    container_name: gitea
    restart: unless-stopped
    ports:
      - "127.0.0.1:3000:3000"
      - "2222:22"
    environment:
      - USER_UID=1000
      - USER_GID=1000
      - GITEA__database__DB_TYPE=postgres
      - GITEA__database__HOST=gitea-db:5432
      - GITEA__database__NAME=gitea
      - GITEA__database__USER=gitea
      - GITEA__database__PASSWD=${DB_PASSWORD}
      - GITEA__server__ROOT_URL=https://${DOMAIN}/
      - GITEA__server__SSH_DOMAIN=${DOMAIN}
      - GITEA__server__SSH_PORT=2222
    volumes:
      - gitea-data:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    depends_on:
      gitea-db:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:3000/api/healthz || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - internal
      - web
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "1.0"

  gitea-db:
    image: postgres:16-alpine
    container_name: gitea-db
    restart: unless-stopped
    volumes:
      - gitea-db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=gitea
      - POSTGRES_USER=gitea
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U gitea"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - internal
    deploy:
      resources:
        limits:
          memory: 256M

volumes:
  gitea-data:
  gitea-db-data:

networks:
  internal:
  web:
    external: true
```

**Health check:** `curl -f http://localhost:3000/api/healthz`

---

#### 7. Vaultwarden

**Gotchas:** MUST be served over HTTPS or it won't work from clients. Disable signups after initial setup. Enable admin panel only temporarily.

```yaml
services:
  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden
    restart: unless-stopped
    ports:
      - "127.0.0.1:8080:80"
    environment:
      - DOMAIN=https://${DOMAIN}
      - SIGNUPS_ALLOWED=true  # Set to false after creating your account
      - ADMIN_TOKEN=${ADMIN_TOKEN}  # Generate with: openssl rand -base64 48
      - WEBSOCKET_ENABLED=true
      - LOG_LEVEL=warn
    volumes:
      - vaultwarden-data:/data
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:80/alive || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - web
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: "0.5"

volumes:
  vaultwarden-data:

networks:
  web:
    external: true
```

**Health check:** `curl -f http://localhost:8080/alive`
**Post-deploy:** Create account, then set `SIGNUPS_ALLOWED=false` and remove `ADMIN_TOKEN`

---

#### 8. Ghostfolio

```yaml
services:
  ghostfolio:
    image: ghostfolio/ghostfolio:latest
    container_name: ghostfolio
    restart: unless-stopped
    ports:
      - "127.0.0.1:3333:3333"
    environment:
      - NODE_ENV=production
      - ACCESS_TOKEN_SALT=${ACCESS_TOKEN_SALT}
      - DATABASE_URL=postgres://ghostfolio:${DB_PASSWORD}@ghostfolio-db:5432/ghostfolio
      - JWT_SECRET_KEY=${JWT_SECRET}
      - REDIS_HOST=ghostfolio-redis
      - REDIS_PORT=6379
    depends_on:
      ghostfolio-db:
        condition: service_healthy
      ghostfolio-redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:3333/api/v1/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - internal
      - web
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "1.0"

  ghostfolio-db:
    image: postgres:16-alpine
    container_name: ghostfolio-db
    restart: unless-stopped
    volumes:
      - ghostfolio-db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=ghostfolio
      - POSTGRES_USER=ghostfolio
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ghostfolio"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - internal
    deploy:
      resources:
        limits:
          memory: 256M

  ghostfolio-redis:
    image: redis:7-alpine
    container_name: ghostfolio-redis
    restart: unless-stopped
    volumes:
      - ghostfolio-redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - internal
    deploy:
      resources:
        limits:
          memory: 128M

volumes:
  ghostfolio-db-data:
  ghostfolio-redis-data:

networks:
  internal:
  web:
    external: true
```

**Health check:** `curl -f http://localhost:3333/api/v1/health`

---

#### 9. Langfuse

**Gotchas:** Langfuse v3 has two app containers (web + worker), plus Postgres, ClickHouse, Redis. Docker Compose is for low-scale/testing — use k8s for HA. All `# CHANGEME` secrets must be replaced.

```yaml
services:
  langfuse-web:
    image: langfuse/langfuse:2
    container_name: langfuse-web
    restart: unless-stopped
    ports:
      - "127.0.0.1:3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://langfuse:${DB_PASSWORD}@langfuse-db:5432/langfuse
      - NEXTAUTH_URL=https://${DOMAIN}
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
      - SALT=${SALT}
      - ENCRYPTION_KEY=${ENCRYPTION_KEY}
      - TELEMETRY_ENABLED=false
    depends_on:
      langfuse-db:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:3000/api/public/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s
    networks:
      - internal
      - web
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: "2.0"

  langfuse-db:
    image: postgres:16-alpine
    container_name: langfuse-db
    restart: unless-stopped
    volumes:
      - langfuse-db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=langfuse
      - POSTGRES_USER=langfuse
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U langfuse"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - internal
    deploy:
      resources:
        limits:
          memory: 512M

volumes:
  langfuse-db-data:

networks:
  internal:
  web:
    external: true
```

**Health check:** `curl -f http://localhost:3000/api/public/health`

---

#### 10. Ghost

**Gotchas:** Ghost 6 uses Docker as primary install method. Requires MySQL 8. Email must be configured or login will fail (sends verification link). For ActivityPub support, use the official Docker tooling.

```yaml
services:
  ghost:
    image: ghost:5-alpine
    container_name: ghost
    restart: unless-stopped
    ports:
      - "127.0.0.1:2368:2368"
    environment:
      url: https://${DOMAIN}
      database__client: mysql
      database__connection__host: ghost-db
      database__connection__user: ghost
      database__connection__password: ${DB_PASSWORD}
      database__connection__database: ghost
      mail__transport: SMTP
      mail__options__host: ${SMTP_HOST:-smtp.mailgun.org}
      mail__options__port: ${SMTP_PORT:-587}
      mail__options__auth__user: ${SMTP_USER}
      mail__options__auth__pass: ${SMTP_PASSWORD}
    volumes:
      - ghost-content:/var/lib/ghost/content
    depends_on:
      ghost-db:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:2368/ghost/api/v4/admin/site/ || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - internal
      - web
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "1.0"

  ghost-db:
    image: mysql:8.0
    container_name: ghost-db
    restart: unless-stopped
    volumes:
      - ghost-db-data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: ghost
      MYSQL_USER: ghost
      MYSQL_PASSWORD: ${DB_PASSWORD}
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - internal
    deploy:
      resources:
        limits:
          memory: 512M

volumes:
  ghost-content:
  ghost-db-data:

networks:
  internal:
  web:
    external: true
```

**Health check:** `curl -f http://localhost:2368/ghost/api/v4/admin/site/`
**Setup:** Visit `https://<DOMAIN>/ghost` to create admin account

---

#### 11. MinIO

**WARNING:** MinIO was archived in February 2026. The community edition lost its GUI in May 2025 and entered maintenance mode in December 2025. Consider **Garage** or **SeaweedFS** as alternatives. Including for legacy/existing deployments.

```yaml
services:
  minio:
    image: minio/minio:latest
    container_name: minio
    restart: unless-stopped
    command: server /data --console-address ":9001"
    ports:
      - "127.0.0.1:9000:9000"
      - "127.0.0.1:9001:9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER:-admin}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
    volumes:
      - minio-data:/data
    healthcheck:
      test: ["CMD", "mc", "ready", "local"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - web
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "1.0"

volumes:
  minio-data:

networks:
  web:
    external: true
```

**Health check:** `curl -f http://localhost:9000/minio/health/live`

---

#### 12. Immich

**Gotchas:** Heavy app — ML models need 2GB+ RAM. Use the official `docker-compose.yml` and `.env` from the Immich repo. Do NOT write compose from scratch.

```bash
# Use official Immich setup
mkdir -p /opt/immich && cd /opt/immich
wget -O docker-compose.yml https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml
wget -O .env https://github.com/immich-app/immich/releases/latest/download/example.env
```

**Critical `.env` changes:**
```env
UPLOAD_LOCATION=/opt/immich/upload
DB_PASSWORD=<GENERATE_STRONG_PASSWORD>
IMMICH_MACHINE_LEARNING_URL=http://immich-machine-learning:3003
```

**Health check:** `curl -f http://localhost:2283/api/server/ping`

---

#### 13. Paperless-ngx

```yaml
services:
  paperless:
    image: ghcr.io/paperless-ngx/paperless-ngx:latest
    container_name: paperless
    restart: unless-stopped
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      PAPERLESS_DBHOST: paperless-db
      PAPERLESS_DBNAME: paperless
      PAPERLESS_DBUSER: paperless
      PAPERLESS_DBPASS: ${DB_PASSWORD}
      PAPERLESS_REDIS: redis://paperless-redis:6379
      PAPERLESS_URL: https://${DOMAIN}
      PAPERLESS_SECRET_KEY: ${SECRET_KEY}
      PAPERLESS_ADMIN_USER: ${ADMIN_USER:-admin}
      PAPERLESS_ADMIN_PASSWORD: ${ADMIN_PASSWORD}
      PAPERLESS_OCR_LANGUAGE: eng
      PAPERLESS_TIME_ZONE: ${TIMEZONE:-America/New_York}
    volumes:
      - paperless-data:/usr/src/paperless/data
      - paperless-media:/usr/src/paperless/media
      - paperless-export:/usr/src/paperless/export
      - paperless-consume:/usr/src/paperless/consume
    depends_on:
      paperless-db:
        condition: service_healthy
      paperless-redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8000/api/ || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - internal
      - web
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: "2.0"

  paperless-db:
    image: postgres:16-alpine
    container_name: paperless-db
    restart: unless-stopped
    volumes:
      - paperless-db-data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: paperless
      POSTGRES_USER: paperless
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U paperless"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - internal
    deploy:
      resources:
        limits:
          memory: 256M

  paperless-redis:
    image: redis:7-alpine
    container_name: paperless-redis
    restart: unless-stopped
    volumes:
      - paperless-redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - internal
    deploy:
      resources:
        limits:
          memory: 128M

volumes:
  paperless-data:
  paperless-media:
  paperless-export:
  paperless-consume:
  paperless-db-data:
  paperless-redis-data:

networks:
  internal:
  web:
    external: true
```

**Health check:** `curl -f http://localhost:8000/api/`

---

#### 14. Coolify

**Gotchas:** Coolify manages its own Docker setup. Use the official install script instead of manual compose.

```bash
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
```

Coolify will be available at `http://<VPS_IP>:8000`. It handles its own reverse proxy, SSL, and database deployment.

**Health check:** `curl -f http://localhost:8000/api/health`

---

#### 15. Stirling PDF

```yaml
services:
  stirling-pdf:
    image: frooodle/s-pdf:latest
    container_name: stirling-pdf
    restart: unless-stopped
    ports:
      - "127.0.0.1:8080:8080"
    environment:
      - DOCKER_ENABLE_SECURITY=false
      - LANGS=en_US
    volumes:
      - stirling-data:/usr/share/tessdata
      - stirling-configs:/configs
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8080/api/v1/info/status || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - web
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "1.0"

volumes:
  stirling-data:
  stirling-configs:

networks:
  web:
    external: true
```

**Health check:** `curl -f http://localhost:8080/api/v1/info/status`

---

#### 16. Nginx Proxy Manager

```yaml
services:
  npm:
    image: jc21/nginx-proxy-manager:latest
    container_name: nginx-proxy-manager
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
      - "81:81"
    volumes:
      - npm-data:/data
      - npm-letsencrypt:/etc/letsencrypt
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:81/api/ || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - web
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: "0.5"

volumes:
  npm-data:
  npm-letsencrypt:

networks:
  web:
    external: true
```

**Default login:** admin@example.com / changeme
**Health check:** `curl -f http://localhost:81/api/`

---

#### 17. Portainer

```yaml
services:
  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    restart: unless-stopped
    ports:
      - "127.0.0.1:9443:9443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer-data:/data
    healthcheck:
      test: ["CMD-SHELL", "curl -fk https://localhost:9443/api/system/status || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - web
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: "0.5"

volumes:
  portainer-data:

networks:
  web:
    external: true
```

**Health check:** `curl -fk https://localhost:9443/api/system/status`

---

#### 18. Dockge

```yaml
services:
  dockge:
    image: louislam/dockge:1
    container_name: dockge
    restart: unless-stopped
    ports:
      - "127.0.0.1:5001:5001"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - dockge-data:/app/data
      - /opt/stacks:/opt/stacks
    environment:
      - DOCKGE_STACKS_DIR=/opt/stacks
    networks:
      - web
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: "0.5"

volumes:
  dockge-data:

networks:
  web:
    external: true
```

**Health check:** `curl -f http://localhost:5001`

---

## Phase 4: Nginx Reverse Proxy

Generate an Nginx config for the selected app. All app ports bind to `127.0.0.1` so they're only accessible through the proxy.

```bash
# Create Nginx site config
cat > /etc/nginx/sites-available/${APP_NAME} << 'NGINXEOF'
server {
    listen 80;
    server_name ${DOMAIN};

    location / {
        return 301 https://$host$request_uri;
    }

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
}

server {
    listen 443 ssl http2;
    server_name ${DOMAIN};

    ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Proxy settings
    location / {
        proxy_pass http://127.0.0.1:${APP_PORT};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support (needed for Supabase Realtime, Uptime Kuma, n8n, Vaultwarden)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Large uploads (for Ghost, Immich, Paperless, MinIO)
        client_max_body_size 100M;
    }
}
NGINXEOF

# Enable the site
ln -sf /etc/nginx/sites-available/${APP_NAME} /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

**App-specific Nginx adjustments:**
- **Immich:** Set `client_max_body_size 50G;` for photo uploads
- **MinIO:** Add separate `location /` blocks for API (port 9000) and console (port 9001)
- **Supabase:** Proxy to Kong on port 8000, Studio on port 3000 needs a separate subdomain or path
- **Gitea:** Add a stream block for SSH passthrough if using port 2222
- **Vaultwarden:** Add WebSocket location: `location /notifications/hub { proxy_pass ...; }`

---

## Phase 5: SSL via Certbot

```bash
# Install Certbot if not present
apt-get update && apt-get install -y certbot python3-certbot-nginx

# Obtain SSL certificate
certbot --nginx -d ${DOMAIN} --non-interactive --agree-tos -m ${EMAIL}

# Verify auto-renewal is set up
certbot renew --dry-run

# Check the systemd timer
systemctl status certbot.timer
```

---

## Phase 6: Backup Configuration

Create a backup script for the app's persistent data. Customize based on which databases the app uses.

```bash
cat > /opt/backups/backup-${APP_NAME}.sh << 'BACKUPEOF'
#!/bin/bash
set -euo pipefail

BACKUP_DIR="/opt/backups/${APP_NAME}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

mkdir -p "$BACKUP_DIR"

# === Postgres Backup (if applicable) ===
docker exec ${APP_NAME}-db pg_dumpall -U ${DB_USER} | gzip > "$BACKUP_DIR/db_${TIMESTAMP}.sql.gz"

# === MySQL Backup (Ghost only) ===
# docker exec ghost-db mysqldump -u ghost -p${DB_PASSWORD} ghost | gzip > "$BACKUP_DIR/db_${TIMESTAMP}.sql.gz"

# === Volume Backup ===
# Stop app briefly for consistent backup (optional — skip for near-zero-downtime)
# docker compose -f /opt/${APP_NAME}/docker-compose.yml stop ${APP_NAME}
tar czf "$BACKUP_DIR/volumes_${TIMESTAMP}.tar.gz" -C /var/lib/docker/volumes . --include="${APP_NAME}*"
# docker compose -f /opt/${APP_NAME}/docker-compose.yml start ${APP_NAME}

# === SQLite Backup (Vaultwarden, Uptime Kuma) ===
# docker exec ${APP_NAME} sqlite3 /data/db.sqlite3 ".backup '/data/backup.sqlite3'"
# docker cp ${APP_NAME}:/data/backup.sqlite3 "$BACKUP_DIR/db_${TIMESTAMP}.sqlite3"

# === Cleanup old backups ===
find "$BACKUP_DIR" -type f -mtime +${RETENTION_DAYS} -delete

echo "[$(date)] Backup complete: $BACKUP_DIR/*_${TIMESTAMP}*"
BACKUPEOF

chmod +x /opt/backups/backup-${APP_NAME}.sh

# Add to crontab — daily at 3 AM
(crontab -l 2>/dev/null; echo "0 3 * * * /opt/backups/backup-${APP_NAME}.sh >> /var/log/backup-${APP_NAME}.log 2>&1") | crontab -
```

---

## Phase 7: Deploy and Verify

Execute these steps in order:

```bash
# 1. Create the Docker network if it doesn't exist
docker network create web 2>/dev/null || true

# 2. Create app directory and write compose file
mkdir -p /opt/${APP_NAME}
# Write docker-compose.yml and .env to /opt/${APP_NAME}/

# 3. Generate secrets
cat > /opt/${APP_NAME}/.env << ENVEOF
DOMAIN=${DOMAIN}
DB_PASSWORD=$(openssl rand -base64 24 | tr -d '/+=')
SECRET_KEY=$(openssl rand -hex 32)
# ... app-specific secrets
ENVEOF

# 4. Pull and start
cd /opt/${APP_NAME}
docker compose pull
docker compose up -d

# 5. Wait for services to be healthy
echo "Waiting for services to start..."
sleep 15

# 6. Run health check
curl -f http://localhost:${APP_PORT}/${HEALTH_ENDPOINT} && echo "HEALTHY" || echo "UNHEALTHY — check logs with: docker compose logs"

# 7. Set up Nginx and SSL (from Phases 4-5)

# 8. Final verification via HTTPS
curl -f https://${DOMAIN}/${HEALTH_ENDPOINT} && echo "DEPLOYMENT COMPLETE" || echo "SSL/PROXY ISSUE — check nginx and certbot"
```

---

## Phase 8: Post-Deploy Checklist

Present this checklist to the user after deployment:

- [ ] App is accessible at `https://${DOMAIN}`
- [ ] Admin account created (first visit for most apps)
- [ ] Default passwords changed
- [ ] Signups disabled (if applicable — Vaultwarden, Gitea)
- [ ] Email/SMTP configured (if applicable — Ghost, n8n)
- [ ] Backup cron is running (`crontab -l`)
- [ ] Firewall only exposes ports 80, 443, and SSH (`ufw status`)
- [ ] Docker auto-updates considered (Watchtower or manual update schedule)
- [ ] Monitoring set up (deploy Uptime Kuma if not already running)

---

## Quick Reference: All Health Check URLs

| App | Health Check URL |
|-----|-----------------|
| Supabase | `http://localhost:3000` + `http://localhost:8000/rest/v1/` |
| Plausible | `http://localhost:8000/api/health` |
| Umami | `http://localhost:3000/api/heartbeat` |
| Uptime Kuma | `http://localhost:3001` |
| n8n | `http://localhost:5678/healthz` |
| Gitea | `http://localhost:3000/api/healthz` |
| Vaultwarden | `http://localhost:8080/alive` |
| Ghostfolio | `http://localhost:3333/api/v1/health` |
| Langfuse | `http://localhost:3000/api/public/health` |
| Ghost | `http://localhost:2368/ghost/api/v4/admin/site/` |
| MinIO | `http://localhost:9000/minio/health/live` |
| Immich | `http://localhost:2283/api/server/ping` |
| Paperless-ngx | `http://localhost:8000/api/` |
| Coolify | `http://localhost:8000/api/health` |
| Stirling PDF | `http://localhost:8080/api/v1/info/status` |
| Nginx Proxy Mgr | `http://localhost:81/api/` |
| Portainer | `https://localhost:9443/api/system/status` |
| Dockge | `http://localhost:5001` |
