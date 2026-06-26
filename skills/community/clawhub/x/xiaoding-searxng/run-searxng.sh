#!/bin/sh


docker stop searxng || true
docker rm searxng || true
mkdir ./config || true

cat > config/settings.yml << EOF
# Minimal SearXNG configuration with JSON API and Bing enabled
# See https://docs.searxng.org/admin/settings/settings.html

use_default_settings: true

search:
  # Enable JSON format for API access
  formats:
    - html
    - json

server:
  # CHANGE THIS in production!
  secret_key: "temporary-key-please-change-me"
  bind_address: "0.0.0.0"
  port: 8080
  limiter: false  # Disable rate limiting for local use
  public_instance: false

# Enable Bing search engine (critical for Chinese queries)
engines:
  - name: bing
    engine: bing
    shortcut: bi
    disabled: false
    # Add user-agent to reduce timeout issues
    headers:
      User-Agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

# Optional: Enable other engines for redundancy
#  - name: duckduckgo
#    engine: duckduckgo
#    disabled: false
#  - name: brave
#    engine: brave
#    disabled: false
EOF


docker run --restart always --network host --name searxng -d -e GRANIAN_HOST=127.0.0.1 -v "./config/:/etc/searxng:Z" searxng/searxng:latest
