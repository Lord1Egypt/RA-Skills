# Install SeekDB — Docker

**Supported platforms:** Linux x86_64, Linux aarch64, macOS (with Docker Desktop). Not Windows.

---

## Step 1 — Check Docker

```bash
docker --version
docker info 2>&1 | head -5
```
If Docker is not running, tell the user to start Docker Desktop (macOS/Windows) or `systemctl start docker` (Linux), then wait.

## Step 2 — Pull and run the container

```bash
docker run -d \
  --name seekdb \
  -p 2881:2881 \
  -p 2886:2886 \
  -v "$(pwd)/seekdb-data:/var/lib/oceanbase" \
  oceanbase/seekdb:latest
```
If a container named `seekdb` already exists, check its state first:
```bash
docker ps -a --filter name=seekdb
```
If it exists and is stopped, offer to restart it: `docker start seekdb`. If it exists and is running, skip to Step 3.

## Step 3 — Wait for SeekDB to be ready

SeekDB takes a few seconds to initialize. Check readiness by polling:
```bash
for i in $(seq 1 12); do
  docker exec seekdb mysql -h 127.0.0.1 -P 2881 -u root -e "SELECT 1" 2>/dev/null && echo "Ready!" && break
  echo "Waiting... ($i/12)"
  sleep 5
done
```
If it is not ready after 60 seconds, check the logs:
```bash
docker logs seekdb --tail 50
```
Diagnose the error and fix it.

## Step 4 — Verify connectivity from host

```bash
mysql -h 127.0.0.1 -P 2881 -u root -e "SELECT 'SeekDB is running!' AS status;"
```

## Step 5 — Done

Confirm success and show:
- MySQL port: `127.0.0.1:2881`
- HTTP port: `127.0.0.1:2886`
- Data directory: `./seekdb-data`
- Stop: `docker stop seekdb` / Start: `docker start seekdb` / Logs: `docker logs seekdb`

---

## References

- Docker image: <https://github.com/oceanbase/docker-images/blob/main/seekdb/README.md>
