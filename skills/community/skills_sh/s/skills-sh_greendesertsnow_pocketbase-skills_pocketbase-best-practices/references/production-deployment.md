# Production & Deployment

**Impact: LOW-MEDIUM**

Backup strategies, configuration management, reverse proxy setup, and SQLite optimization.

---

## 1. Implement Proper Backup Strategies

**Impact: LOW-MEDIUM (Prevents data loss, enables disaster recovery)**

Regular backups are essential for production deployments. PocketBase provides built-in backup functionality and supports external S3 storage.

**Incorrect (no backup strategy):**

```javascript
// No backups at all - disaster waiting to happen
// Just running: ./pocketbase serve

// Manual file copy while server running - can corrupt data
// cp pb_data/data.db backup/

// Only backing up database, missing files
// sqlite3 pb_data/data.db ".backup backup.db"
```

**Correct (comprehensive backup strategy):**

```javascript
// 1. Using PocketBase Admin API for backups
const adminPb = new PocketBase('http://127.0.0.1:8090');
await adminPb.collection('_superusers').authWithPassword(admin, password);

// Create backup (includes database and files)
async function createBackup(name = '') {
  const backup = await adminPb.backups.create(name);
  console.log('Backup created:', backup.key);
  return backup;
}

// List available backups
async function listBackups() {
  const backups = await adminPb.backups.getFullList();
  backups.forEach(b => {
    console.log(`${b.key} - ${b.size} bytes - ${b.modified}`);
  });
  return backups;
}

// Download backup
async function downloadBackup(key) {
  const token = await adminPb.files.getToken();
  const url = adminPb.backups.getDownloadURL(token, key);
  // url can be used to download the backup file
  return url;
}

// Restore from backup (CAUTION: overwrites current data!)
async function restoreBackup(key) {
  await adminPb.backups.restore(key);
  console.log('Restore initiated - server will restart');
}

// Delete old backups
async function cleanupOldBackups(keepCount = 7) {
  const backups = await adminPb.backups.getFullList();

  // Sort by date, keep newest
  const sorted = backups.sort((a, b) =>
    new Date(b.modified) - new Date(a.modified)
  );

  const toDelete = sorted.slice(keepCount);
  for (const backup of toDelete) {
    await adminPb.backups.delete(backup.key);
    console.log('Deleted old backup:', backup.key);
  }
}
```

**Automated backup script (cron job):**

```bash
#!/bin/bash
# backup.sh - Run daily via cron

POCKETBASE_URL="http://127.0.0.1:8090"
ADMIN_EMAIL="admin@example.com"
ADMIN_PASSWORD="your-secure-password"
BACKUP_DIR="/path/to/backups"
KEEP_DAYS=7

# Create timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup via API
curl -X POST "${POCKETBASE_URL}/api/backups" \
  -H "Authorization: $(curl -s -X POST "${POCKETBASE_URL}/api/collections/_superusers/auth-with-password" \
    -d "identity=${ADMIN_EMAIL}&password=${ADMIN_PASSWORD}" | jq -r '.token')" \
  -d "name=backup_${TIMESTAMP}"

# Clean old local backups
find "${BACKUP_DIR}" -name "*.zip" -mtime +${KEEP_DAYS} -delete

echo "Backup completed: backup_${TIMESTAMP}"
```

**Configure S3 for backup storage:**

```javascript
// In Admin UI: Settings > Backups > S3
// Or via API:
await adminPb.settings.update({
  backups: {
    s3: {
      enabled: true,
      bucket: 'my-pocketbase-backups',
      region: 'us-east-1',
      endpoint: 's3.amazonaws.com',
      accessKey: process.env.AWS_ACCESS_KEY,
      secret: process.env.AWS_SECRET_KEY
    }
  }
});
```

**Backup best practices:**

| Aspect | Recommendation |
|--------|---------------|
| Frequency | Daily minimum, hourly for critical apps |
| Retention | 7-30 days of daily backups |
| Storage | Off-site (S3, separate server) |
| Testing | Monthly restore tests |
| Monitoring | Alert on backup failures |

**Pre-backup checklist:**
- [ ] S3 or external storage configured
- [ ] Automated schedule set up
- [ ] Retention policy defined
- [ ] Restore procedure documented
- [ ] Restore tested successfully

Reference: [PocketBase Backups](https://pocketbase.io/docs/going-to-production/#backups)

## 2. Configure Production Settings Properly

**Impact: LOW-MEDIUM (Secure and optimized production environment)**

Production deployments require proper configuration of URLs, secrets, SMTP, and security settings.

**Incorrect (development defaults in production):**

```bash
# Running with defaults - insecure!
./pocketbase serve

# Hardcoded secrets
./pocketbase serve --encryptionEnv="mySecretKey123"

# Wrong origin for CORS
# Leaving http://localhost:8090 as allowed origin
```

**Correct (production configuration):**

```bash
# Production startup with essential flags
./pocketbase serve \
  --http="0.0.0.0:8090" \
  --origins="https://myapp.com,https://www.myapp.com" \
  --encryptionEnv="PB_ENCRYPTION_KEY"

# Using environment variables
export PB_ENCRYPTION_KEY="your-32-char-encryption-key-here"
export SMTP_HOST="smtp.sendgrid.net"
export SMTP_PORT="587"
export SMTP_USER="apikey"
export SMTP_PASS="your-sendgrid-api-key"

./pocketbase serve --http="0.0.0.0:8090"
```

**Configure SMTP for emails:**

```javascript
// Via Admin UI or API
await adminPb.settings.update({
  smtp: {
    enabled: true,
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT),
    username: process.env.SMTP_USER,
    password: process.env.SMTP_PASS,
    tls: true
  },
  meta: {
    appName: 'My App',
    appURL: 'https://myapp.com',
    senderName: 'My App',
    senderAddress: 'noreply@myapp.com'
  }
});

// Test email configuration
await adminPb.settings.testEmail('users', 'test@example.com', 'verification');
```

**Configure S3 for file storage:**

```javascript
// Move file storage to S3 for scalability
await adminPb.settings.update({
  s3: {
    enabled: true,
    bucket: 'my-app-files',
    region: 'us-east-1',
    endpoint: 's3.amazonaws.com',
    accessKey: process.env.AWS_ACCESS_KEY,
    secret: process.env.AWS_SECRET_KEY,
    forcePathStyle: false
  }
});

// Test S3 connection
await adminPb.settings.testS3('storage');
```

**Systemd service file:**

```ini
# /etc/systemd/system/pocketbase.service
[Unit]
Description=PocketBase
After=network.target

[Service]
Type=simple
User=pocketbase
Group=pocketbase
LimitNOFILE=4096
Restart=always
RestartSec=5s
WorkingDirectory=/opt/pocketbase
ExecStart=/opt/pocketbase/pocketbase serve --http="127.0.0.1:8090"

# Environment variables
EnvironmentFile=/opt/pocketbase/.env

# Security hardening
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/opt/pocketbase/pb_data

[Install]
WantedBy=multi-user.target
```

**Environment file (.env):**

```bash
# /opt/pocketbase/.env
# SECURITY: Set restrictive permissions: chmod 600 /opt/pocketbase/.env
# SECURITY: Add to .gitignore - NEVER commit this file to version control
# For production, consider a secrets manager (Vault, AWS Secrets Manager, etc.)

PB_ENCRYPTION_KEY=  # Generate with: openssl rand -hex 16

# SMTP
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=           # Set your SMTP password here

# S3 (optional)
AWS_ACCESS_KEY=      # Set your AWS access key
AWS_SECRET_KEY=      # Set your AWS secret key

# OAuth (optional)
GOOGLE_CLIENT_ID=    # Set your Google client ID
GOOGLE_CLIENT_SECRET= # Set your Google client secret
```

**Protect your environment file:**

```bash
# Set restrictive permissions (owner read/write only)
chmod 600 /opt/pocketbase/.env
chown pocketbase:pocketbase /opt/pocketbase/.env

# Ensure .env is in .gitignore
echo ".env" >> .gitignore
```

**Production checklist:**

- [ ] HTTPS enabled (via reverse proxy)
- [ ] Strong encryption key set
- [ ] CORS origins configured
- [ ] SMTP configured and tested
- [ ] Superuser password changed
- [ ] S3 configured (for scalability)
- [ ] Backup schedule configured
- [ ] Rate limiting enabled (via reverse proxy)
- [ ] Logging configured

Reference: [PocketBase Going to Production](https://pocketbase.io/docs/going-to-production/)

## 3. Enable Rate Limiting for API Protection

**Impact: MEDIUM (Prevents abuse, brute-force attacks, and DoS)**

PocketBase v0.23+ includes built-in rate limiting. Enable it to protect against brute-force attacks, API abuse, and excessive resource consumption.

> **v0.36.7 behavioral change:** the built-in limiter switched from a sliding-window to a **fixed-window** strategy. This is cheaper and more predictable, but it means a client can send `2 * maxRequests` in quick succession if they straddle the window boundary. Size your limits with that worst case in mind, and put Nginx/Caddy rate limiting in front of PocketBase for defense in depth (see examples below).

**Incorrect (no rate limiting):**

```bash
# Running without rate limiting
./pocketbase serve

# Vulnerable to:
# - Brute-force password attacks
# - API abuse and scraping
# - DoS from excessive requests
# - Account enumeration attempts
```

**Correct (enable rate limiting):**

```bash
# Enable via command line flag
./pocketbase serve --rateLimiter=true

# Or configure specific limits (requests per second per IP)
./pocketbase serve --rateLimiter=true --rateLimiterRPS=10
```

**Configure via Admin Dashboard:**

Navigate to Settings > Rate Limiter:
- **Enable rate limiter**: Toggle on
- **Max requests/second**: Default 10, adjust based on needs
- **Exempt endpoints**: Optionally whitelist certain paths

**Configure programmatically (Go/JS hooks):**

```javascript
// In pb_hooks/rate_limit.pb.js
routerAdd("GET", "/api/public/*", (e) => {
  // Custom rate limit for specific endpoints
}, $apis.rateLimit(100, "10s")); // 100 requests per 10 seconds

// Stricter limit for auth endpoints
routerAdd("POST", "/api/collections/users/auth-*", (e) => {
  // Auth endpoints need stricter limits
}, $apis.rateLimit(5, "1m")); // 5 attempts per minute
```

**Rate limiting with reverse proxy (additional layer):**

```nginx
# Nginx rate limiting (defense in depth)
http {
    # Define rate limit zones
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=auth:10m rate=1r/s;

    server {
        # General API rate limit
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://pocketbase;
        }

        # Strict limit for auth endpoints
        location /api/collections/users/auth {
            limit_req zone=auth burst=5 nodelay;
            proxy_pass http://pocketbase;
        }

        # Stricter limit for superuser auth
        location /api/collections/_superusers/auth {
            limit_req zone=auth burst=3 nodelay;
            proxy_pass http://pocketbase;
        }
    }
}
```

```caddyfile
# Caddy with rate limiting plugin
myapp.com {
    rate_limit {
        zone api {
            key {remote_host}
            events 100
            window 10s
        }
        zone auth {
            key {remote_host}
            events 5
            window 1m
        }
    }

    @auth path /api/collections/*/auth*
    handle @auth {
        rate_limit { zone auth }
        reverse_proxy 127.0.0.1:8090
    }

    handle {
        rate_limit { zone api }
        reverse_proxy 127.0.0.1:8090
    }
}
```

**Handle rate limit errors in client:**

```javascript
async function makeRequest(fn, retries = 0, maxRetries = 3) {
  try {
    return await fn();
  } catch (error) {
    if (error.status === 429 && retries < maxRetries) {
      // Rate limited - wait and retry with limit
      const retryAfter = error.response?.retryAfter || 60;
      console.log(`Rate limited. Retry ${retries + 1}/${maxRetries} after ${retryAfter}s`);

      // Show user-friendly message
      showMessage('Too many requests. Please wait a moment.');

      await sleep(retryAfter * 1000);
      return makeRequest(fn, retries + 1, maxRetries);
    }
    throw error;
  }
}

// Usage
const result = await makeRequest(() =>
  pb.collection('posts').getList(1, 20)
);
```

**Recommended limits by endpoint type:**

| Endpoint Type | Suggested Limit | Reason |
|--------------|-----------------|--------|
| Auth endpoints | 5-10/min | Prevent brute-force |
| Password reset | 3/hour | Prevent enumeration |
| Record creation | 30/min | Prevent spam |
| General API | 60-100/min | Normal usage |
| Public read | 100-200/min | Higher for reads |
| File uploads | 10/min | Resource-intensive |

**Monitoring rate limit hits:**

```javascript
// Check PocketBase logs for rate limit events
// Or set up alerting in your monitoring system

// Client-side tracking
pb.afterSend = function(response, data) {
  if (response.status === 429) {
    trackEvent('rate_limit_hit', {
      endpoint: response.url,
      timestamp: new Date()
    });
  }
  return data;
};
```

Reference: [PocketBase Going to Production](https://pocketbase.io/docs/going-to-production/)

## 4. Configure Reverse Proxy Correctly

**Impact: LOW-MEDIUM (HTTPS, caching, rate limiting, and security headers)**

Use a reverse proxy (Nginx, Caddy) for HTTPS termination, caching, rate limiting, and security headers.

**Incorrect (exposing PocketBase directly):**

```bash
# Direct exposure - no HTTPS, no rate limiting
./pocketbase serve --http="0.0.0.0:8090"

# Port forwarding without proxy
iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 8090
# Still no HTTPS!
```

**Correct (Caddy - simplest option):**

```caddyfile
# /etc/caddy/Caddyfile
myapp.com {
    # Automatic HTTPS via Let's Encrypt
    reverse_proxy 127.0.0.1:8090 {
        # Required for SSE/Realtime
        flush_interval -1
    }

    # Security headers
    header {
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
        Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
        Referrer-Policy "strict-origin-when-cross-origin"
        -Server
    }

    # Restrict admin UI to internal/VPN networks
    # @admin path /_/*
    # handle @admin {
    #     @blocked not remote_ip 10.0.0.0/8 172.16.0.0/12 192.168.0.0/16
    #     respond @blocked 403
    #     reverse_proxy 127.0.0.1:8090
    # }

    # Rate limiting (requires caddy-ratelimit plugin)
    # Install: xcaddy build --with github.com/mholt/caddy-ratelimit
    # Without this plugin, use PocketBase's built-in rate limiter (--rateLimiter=true)
    # rate_limit {
    #     zone api {
    #         key {remote_host}
    #         events 100
    #         window 1m
    #     }
    # }
}
```

**Correct (Nginx configuration):**

```nginx
# /etc/nginx/sites-available/pocketbase

# Rate limit zones must be defined in http context (e.g., /etc/nginx/nginx.conf)
# limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

upstream pocketbase {
    server 127.0.0.1:8090;
    keepalive 64;
}

server {
    listen 80;
    server_name myapp.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name myapp.com;

    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/myapp.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myapp.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    # Note: X-XSS-Protection is deprecated and can introduce vulnerabilities.
    # Use Content-Security-Policy instead.

    location / {
        proxy_pass http://pocketbase;
        proxy_http_version 1.1;

        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # SSE/Realtime support
        proxy_set_header Connection '';
        proxy_buffering off;
        proxy_cache off;
        chunked_transfer_encoding off;

        # Timeouts
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }

    # Rate limit API endpoints
    location /api/ {
        limit_req zone=api burst=20 nodelay;

        proxy_pass http://pocketbase;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection '';
        proxy_buffering off;
    }

    # Static file caching
    location /api/files/ {
        proxy_pass http://pocketbase;
        proxy_cache_valid 200 1d;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }

    # Gzip compression
    gzip on;
    gzip_types text/plain application/json application/javascript text/css;
    gzip_min_length 1000;
}
```

**Docker Compose with Caddy:**

```yaml
# docker-compose.yml
version: '3.8'

services:
  pocketbase:
    # NOTE: This is a third-party community image, not officially maintained by PocketBase.
    # For production, consider building your own image from the official PocketBase binary.
    # See: https://pocketbase.io/docs/going-to-production/
    image: ghcr.io/muchobien/pocketbase:latest
    restart: unless-stopped
    volumes:
      - ./pb_data:/pb_data
    environment:
      - PB_ENCRYPTION_KEY=${PB_ENCRYPTION_KEY}

  caddy:
    image: caddy:2-alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config
    depends_on:
      - pocketbase

volumes:
  caddy_data:
  caddy_config:
```

**Key configuration points:**

| Feature | Why It Matters |
|---------|---------------|
| HTTPS | Encrypts traffic, required for auth |
| SSE support | `proxy_buffering off` for realtime |
| Rate limiting | Prevents abuse |
| Security headers | XSS/clickjacking protection |
| Keepalive | Connection reuse, better performance |

Reference: [PocketBase Going to Production](https://pocketbase.io/docs/going-to-production/)

## 5. Tune OS and Runtime for PocketBase Scale

**Impact: MEDIUM (Prevents file descriptor exhaustion, OOM kills, and exposes secure config for production deployments)**

Three low-effort OS/runtime knobs have outsized impact on production stability: open-file limits for realtime connections, Go memory limits for constrained hosts, and settings encryption for shared or externally-backed infrastructure. None of these are set automatically.

**Incorrect (default OS limits, no memory governor, plain-text settings):**

```bash
# Start without raising the file descriptor limit
/root/pb/pocketbase serve yourdomain.com
# → "Too many open files" once concurrent realtime connections exceed ~1024

# Start in a container that has a 512 MB RAM cap without GOMEMLIMIT
docker run -m 512m pocketbase serve ...
# → OOM kill during large file upload because Go GC doesn't respect cgroup limits

# Store SMTP password and S3 secret as plain JSON in pb_data/data.db
pocketbase serve  # no --encryptionEnv
# → Anyone who obtains the database backup can read all credentials
```

**Correct:**

```bash
# 1. Raise the open-file limit before starting (Linux/macOS)
#    Check current limit first:
ulimit -a | grep "open files"
#    Temporarily raise to 4096 for the current session:
ulimit -n 4096
/root/pb/pocketbase serve yourdomain.com

#    Or persist it via systemd (recommended for production):
# /lib/systemd/system/pocketbase.service
# [Service]
# LimitNOFILE = 4096
# ...

# 2. Cap Go's soft memory target on memory-constrained hosts
#    (instructs the GC to be more aggressive before the kernel OOM-kills the process)
GOMEMLIMIT=512MiB /root/pb/pocketbase serve yourdomain.com

# 3. Encrypt application settings at rest
#    Generate a random 32-character key once:
export PB_ENCRYPTION_KEY="z76NX9WWiB05UmQGxw367B6zM39T11fF"
#    Start with the env-var name (not the value) as the flag argument:
pocketbase serve --encryptionEnv=PB_ENCRYPTION_KEY
```

**Docker deployment pattern (v0.36.8):**

```dockerfile
FROM alpine:latest
ARG PB_VERSION=0.36.8

RUN apk add --no-cache unzip ca-certificates

ADD https://github.com/pocketbase/pocketbase/releases/download/v${PB_VERSION}/pocketbase_${PB_VERSION}_linux_amd64.zip /tmp/pb.zip
RUN unzip /tmp/pb.zip -d /pb/

# Uncomment to bundle pre-written migrations or hooks:
# COPY ./pb_migrations /pb/pb_migrations
# COPY ./pb_hooks      /pb/pb_hooks

EXPOSE 8080

# Mount a volume at /pb/pb_data to persist data across container restarts
CMD ["/pb/pocketbase", "serve", "--http=0.0.0.0:8080"]
```

```yaml
# docker-compose.yml
services:
  pocketbase:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - pb_data:/pb/pb_data
    environment:
      GOMEMLIMIT: "512MiB"
      PB_ENCRYPTION_KEY: "${PB_ENCRYPTION_KEY}"
    command: ["/pb/pocketbase", "serve", "--http=0.0.0.0:8080", "--encryptionEnv=PB_ENCRYPTION_KEY"]
volumes:
  pb_data:
```

**Quick-reference checklist:**

| Concern | Fix |
|---------|-----|
| `Too many open files` errors | `ulimit -n 4096` (or `LimitNOFILE=4096` in systemd) |
| OOM kill on constrained host | `GOMEMLIMIT=512MiB` env var |
| Credentials visible in DB backup | `--encryptionEnv=YOUR_VAR` with a 32-char random key |
| Persistent data in Docker | Mount volume at `/pb/pb_data` |

Reference: [Going to production](https://pocketbase.io/docs/going-to-production/)

## 6. Optimize SQLite for Production

**Impact: LOW-MEDIUM (Better performance and reliability for SQLite database)**

PocketBase uses SQLite with optimized defaults. Understanding its characteristics helps optimize performance and avoid common pitfalls. PocketBase uses two separate databases: `data.db` (application data) and `auxiliary.db` (logs and ephemeral data), which reduces write contention.

**Incorrect (ignoring SQLite characteristics):**

```javascript
// Heavy concurrent writes - SQLite bottleneck
async function bulkInsert(items) {
  // Parallel writes cause lock contention
  await Promise.all(items.map(item =>
    pb.collection('items').create(item)
  ));
}

// Not using transactions for batch operations
async function updateMany(items) {
  for (const item of items) {
    await pb.collection('items').update(item.id, item);
  }
  // Each write is a separate transaction - slow!
}

// Large text fields without consideration
const schema = [{
  name: 'content',
  type: 'text'  // Could be megabytes - affects all queries
}];
```

**Correct (SQLite-optimized patterns):**

```javascript
// Use batch operations for multiple writes
async function bulkInsert(items) {
  const batch = pb.createBatch();
  items.forEach(item => {
    batch.collection('items').create(item);
  });
  await batch.send();  // Single transaction, much faster
}

// Batch updates
async function updateMany(items) {
  const batch = pb.createBatch();
  items.forEach(item => {
    batch.collection('items').update(item.id, item);
  });
  await batch.send();
}

// For very large batches, chunk them
async function bulkInsertLarge(items, chunkSize = 100) {
  for (let i = 0; i < items.length; i += chunkSize) {
    const chunk = items.slice(i, i + chunkSize);
    const batch = pb.createBatch();
    chunk.forEach(item => batch.collection('items').create(item));
    await batch.send();
  }
}
```

**Schema considerations:**

```javascript
// Separate large content into dedicated collection
const postsSchema = [
  { name: 'title', type: 'text' },
  { name: 'summary', type: 'text', options: { maxLength: 500 } },
  { name: 'author', type: 'relation' }
  // Content in separate collection
];

const postContentsSchema = [
  { name: 'post', type: 'relation', required: true },
  { name: 'content', type: 'editor' }  // Large HTML content
];

// Fetch content only when needed
async function getPostList() {
  return pb.collection('posts').getList(1, 20);  // Fast, no content
}

async function getPostWithContent(id) {
  const post = await pb.collection('posts').getOne(id);
  const content = await pb.collection('post_contents').getFirstListItem(
    pb.filter('post = {:id}', { id })
  );
  return { ...post, content: content.content };
}
```

**PocketBase default PRAGMA settings:**

PocketBase already configures optimal SQLite settings. You do not need to set these manually unless using a custom SQLite driver:

```sql
PRAGMA busy_timeout       = 10000;  -- Wait 10s for locks instead of failing immediately
PRAGMA journal_mode       = WAL;    -- Write-Ahead Logging: concurrent reads during writes
PRAGMA journal_size_limit = 200000000;  -- Limit WAL file to ~200MB
PRAGMA synchronous        = NORMAL; -- Balanced durability/performance (safe with WAL)
PRAGMA foreign_keys       = ON;     -- Enforce relation integrity
PRAGMA temp_store         = MEMORY; -- Temp tables in memory (faster sorts/joins)
PRAGMA cache_size         = -32000; -- 32MB page cache
```

WAL mode is the most impactful setting -- it allows multiple concurrent readers while a single writer is active, which is critical for PocketBase's concurrent API request handling.

**Index optimization:**

```sql
-- Create indexes for commonly filtered/sorted fields
CREATE INDEX idx_posts_author ON posts(author);
CREATE INDEX idx_posts_created ON posts(created DESC);
CREATE INDEX idx_posts_status_created ON posts(status, created DESC);

-- Verify indexes are being used
EXPLAIN QUERY PLAN
SELECT * FROM posts WHERE author = 'xxx' ORDER BY created DESC;
-- Should show: "USING INDEX idx_posts_author"
```

**SQLite limitations and workarounds:**

| Limitation | Workaround |
|------------|------------|
| Single writer | Use batch operations, queue writes |
| No full-text by default | Use view collections with FTS5 |
| File-based | SSD storage, avoid network mounts |
| Memory for large queries | Pagination, limit result sizes |

**Performance monitoring:**

```javascript
// Monitor slow queries via hooks (requires custom PocketBase build)
// Or use SQLite's built-in profiling

// From sqlite3 CLI:
// .timer on
// SELECT * FROM posts WHERE author = 'xxx';
// Run Time: real 0.003 user 0.002 sys 0.001

// Check database size
// ls -lh pb_data/data.db

// Vacuum to reclaim space after deletes
// sqlite3 pb_data/data.db "VACUUM;"
```

**When to consider alternatives:**

Consider migrating from single PocketBase if:
- Write throughput consistently > 1000/sec needed
- Database size > 100GB
- Complex transactions across tables
- Multi-region deployment required

**Custom SQLite driver (advanced):**

PocketBase supports custom SQLite drivers via `DBConnect`. The CGO driver (`mattn/go-sqlite3`) can offer better performance for some workloads and enables extensions like ICU and FTS5. This requires a custom PocketBase build:

```go
// main.go (custom PocketBase build with CGO driver)
package main

import (
    "github.com/pocketbase/dbx"
    "github.com/pocketbase/pocketbase"
    _ "github.com/mattn/go-sqlite3"  // CGO SQLite driver
)

func main() {
    app := pocketbase.NewWithConfig(pocketbase.Config{
        // Called twice: once for data.db, once for auxiliary.db
        DBConnect: func(dbPath string) (*dbx.DB, error) {
            return dbx.Open("sqlite3", dbPath)
        },
    })

    if err := app.Start(); err != nil {
        panic(err)
    }
}
// Build with: CGO_ENABLED=1 go build
```

Note: CGO requires C compiler toolchain and cannot be cross-compiled as easily as pure Go.

**Scaling options:**
1. **Read replicas**: Litestream for SQLite replication
2. **Sharding**: Multiple PocketBase instances by tenant/feature
3. **Caching**: Redis/Memcached for read-heavy loads
4. **Alternative backend**: If requirements exceed SQLite, evaluate PostgreSQL-based frameworks

Reference: [PocketBase Going to Production](https://pocketbase.io/docs/going-to-production/)

