# Gotchas: MISP Deployment

## MariaDB OOM (Showstopper)
- Default InnoDB buffer pool is **2GB**
- On 4GB hosts, MariaDB crashes instantly with `Out of memory (Needed 2587885448 bytes)`
- MariaDB container enters restart loop
- **Fix:** Set `INNODB_BUFFER_POOL_SIZE` in `.env` BEFORE first `docker compose up`
- Scaling: 4GB = 512M, 8GB = 2048M, 16GB = 4096M

## Recovery from OOM
- If MariaDB already crashed with the wrong buffer size:
  1. `docker compose down -v` (wipes failed DB volume)
  2. Fix `INNODB_BUFFER_POOL_SIZE` in `.env`
  3. `docker compose up -d`
- Without `-v`, the corrupted DB volume persists and MariaDB keeps crashing

## First Boot is Slow
- MISP takes 5-10 minutes on first boot
- DB schema creation, initial data load, worker initialization
- Web UI may show errors during this period
- **Fix:** Poll `https://localhost/users/login` until it returns a login page

## Self-Signed HTTPS
- MISP defaults to self-signed certificates
- All `curl` commands need `-k` flag
- For production: mount proper certs or put behind a reverse proxy

## API Key Generation
- MISP has "advanced authkeys" enabled by default
- The `cake` CLI inside the container is the most reliable method:
  ```bash
  docker compose exec -T misp /var/www/MISP/app/Console/cake user change_authkey <email>
  ```
- API alternative: session login then `POST /auth_keys/add`, but cake is simpler

## Web UI Port
- MISP listens on HTTPS port 443 (not 80)
- URL format: `https://<ip>` (no port needed)
- Port 80 redirects to 443

## Template .env
- Official repo has `template.env`, copy to `.env` before editing
- Don't edit `template.env` directly (git pull conflicts)
