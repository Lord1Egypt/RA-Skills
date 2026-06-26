# Readarr Setup — Claptrap (Synology)

Readarr runs best as a Docker container on Claptrap (192.168.42.79).

## Docker Compose
```yaml
version: "3"
services:
  readarr:
    image: lscr.io/linuxserver/readarr:develop
    container_name: readarr
    environment:
      - PUID=1026
      - PGID=101
      - TZ=Europe/Lisbon
    volumes:
      - /volume1/docker/readarr:/config
      - /volume1/Books:/books
      - /volume1/Downloads:/downloads
    ports:
      - 8787:8787
    restart: unless-stopped
```

Note: Synology Docker requires `sudo docker` (no docker group). Passwordless sudo for `/usr/local/bin/docker` is configured.

## First-Time Config (via web UI at http://192.168.42.79:8787)
1. Set root folder → `/books` (maps to Claptrap `/volume1/Books`)
2. Add quality profile (Standard or prefer EPUB)
3. Add metadata profile
4. Connect Prowlarr (Settings → Indexers → Add → Torznab; use Prowlarr API key)
5. Add download client (qBittorrent or similar)
6. Get API key: Settings → General → Security → API Key

## Calibre Integration
Option A: Point Readarr root folder at `/Volumes/Bull/calibre-library` (if mounted on same machine)
Option B: Drop downloads to a watch folder; Lucien polls and runs `calibredb add`

## Credentials
```bash
echo "<api-key>" > ~/clawd/credentials/readarr_api_key
chmod 600 ~/clawd/credentials/readarr_api_key
```

## Prowlarr → Readarr sync
In Prowlarr: Settings → Apps → Add → Readarr
- URL: `http://192.168.42.79:8787`
- API Key: Readarr key
- Sync Level: Full Sync
