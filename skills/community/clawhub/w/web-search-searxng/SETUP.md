# SearXNG Self-Hosting Guide

Complete setup instructions for self-hosting SearXNG.

## Quick Start (Docker)

### 1. Basic Setup

```bash
# Create directory for config
mkdir -p ~/searxng/config
cd ~/searxng

# Download default config
curl -o config/settings.yml https://raw.githubusercontent.com/searxng/searxng/master/searx/settings.yml

# Run SearXNG
docker run -d \
  --name searxng \
  -p 8080:8080 \
  -v $(pwd)/config:/etc/searxng:rw \
  --restart unless-stopped \
  searxng/searxng:latest

# Check it's running
curl http://localhost:8080/healthz
```

### 2. Update Smart Router Config

Edit `smart-router/config/router.yaml`:

```yaml
search:
  enabled: true
  base_url: "http://localhost:8080"  # Your self-hosted instance
  limit: 5
  category: "general"
```

### 3. Test

```bash
python scripts/route.py "What's the weather in Tokyo?"
```

## Production Setup

### With Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    ports:
      - "127.0.0.1:8080:8080"  # Only local access
    volumes:
      - ./config:/etc/searxng:rw
    environment:
      - SEARXNG_BASE_URL=https://your-domain.com/  # If using reverse proxy
    restart: unless-stopped
    
  # Optional: Redis for caching
  redis:
    image: redis:alpine
    container_name: searxng-redis
    volumes:
      - redis-data:/data
    restart: unless-stopped

volumes:
  redis-data:
```

Start:
```bash
docker-compose up -d
```

### With Caddy Reverse Proxy

For HTTPS and external access:

```bash
# Install Caddy
sudo apt install caddy

# Create Caddyfile
cat > Caddyfile << 'EOF'
searx.yourdomain.com {
    reverse_proxy localhost:8080
}
EOF

# Run Caddy
caddy run
```

Update config:
```yaml
search:
  base_url: "https://searx.yourdomain.com"
```

## Configuration

### Custom Settings

Edit `~/searxng/config/settings.yml`:

```yaml
# General settings
general:
  debug: false
  instance_name: "My SearXNG"
  
# Search settings
search:
  safe_search: 0  # 0=off, 1=moderate, 2=strict
  autocomplete: "duckduckgo"
  
# Enable/disable engines
engines:
  - name: google
    engine: google
    shortcut: go
    
  - name: duckduckgo
    engine: duckduckgo
    shortcut: ddg
    
  - name: bing
    engine: bing
    shortcut: bi
    
  - name: wikipedia
    engine: wikipedia
    shortcut: wp
    
  - name: github
    engine: github
    shortcut: gh
    
  - name: stackoverflow
    engine: stackoverflow
    shortcut: so
    
  # News engines
  - name: bbc
    engine: bbc
    shortcut: bbc
    
  - name: reuters
    engine: reuters
    shortcut: reu

# UI settings
ui:
  static_use_hash: true
  themes:
    - simple
    - oscar
  default_theme: simple
```

Restart after changes:
```bash
docker restart searxng
```

## Systemd Service (Non-Docker)

### Install from Source

```bash
# Install dependencies
sudo apt update
sudo apt install -y python3-venv python3-dev libxml2-dev libxslt1-dev

# Create user
sudo useradd -r -s /bin/false searxng

# Create directory
sudo mkdir -p /opt/searxng
sudo chown searxng:searxng /opt/searxng

# Switch to user
sudo -u searxng bash
cd /opt/searxng

# Create venv
python3 -m venv venv
source venv/bin/activate

# Install SearXNG
pip install -U pip
pip install searxng

# Copy config
mkdir -p /opt/searxng/config
cp venv/lib/python*/site-packages/searx/settings.yml config/

# Edit config
nano config/settings.yml
```

### Create Systemd Service

Create `/etc/systemd/system/searxng.service`:

```ini
[Unit]
Description=SearXNG Meta Search Engine
After=network.target

[Service]
Type=simple
User=searxng
Group=searxng
WorkingDirectory=/opt/searxng
Environment="PATH=/opt/searxng/venv/bin"
Environment="SEARXNG_SETTINGS_PATH=/opt/searxng/config/settings.yml"
ExecStart=/opt/searxng/venv/bin/python -m searx.webapp
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable searxng
sudo systemctl start searxng
sudo systemctl status searxng
```

## Troubleshooting

### "403 Forbidden"

Public instances often block bots. Solutions:
1. Self-host (see above)
2. Add delay between requests:
   ```yaml
   search:
     rate_limit: 2.0  # Seconds between requests
   ```

### "Connection refused"

Check SearXNG is running:
```bash
docker ps | grep searxng
curl http://localhost:8080/healthz
```

### "No results"

Check enabled engines in `settings.yml`:
```yaml
engines:
  - name: google
    engine: google
    disabled: false  # Make sure not disabled
```

### High memory usage

Limit results in config:
```yaml
search:
  max_results: 20
```

## Security

### Rate Limiting

Add to `settings.yml`:
```yaml
server:
  method: "POST"  # Use POST instead of GET
  http_protocol_version: "1.1"
```

### Firewall Rules

```bash
# Only allow local access
sudo ufw allow from 127.0.0.1 to any port 8080

# Or use reverse proxy
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### Filtron (Advanced Rate Limiting)

```bash
# Run filtron alongside SearXNG
docker run -d \
  --name filtron \
  -p 4040:4040 \
  -p 4041:4041 \
  searxng/filtron:latest

# Update router config
search:
  base_url: "http://localhost:4040"  # Through filtron
```

## Verification

Test your instance:
```bash
# Health check
curl http://localhost:8080/healthz

# Test search
curl "http://localhost:8080/search?q=test&format=json"

# From smart router
python scripts/search.py "test query" --base-url http://localhost:8080
```

## Resources

- [SearXNG Docs](https://docs.searxng.org/)
- [GitHub](https://github.com/searxng/searxng)
- [Public Instances](https://searx.space/)
