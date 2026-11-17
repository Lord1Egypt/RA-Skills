# Docker Diagnostics Without Docker CLI

When the remote SSH user is **not in the docker group** and **has no sudo
NOPASSWD** — but you still need to diagnose containers, networks, and services.

## Techniques

### 1. List active containers via cgroup

```bash
ls /sys/fs/cgroup/system.slice/docker-*.scope 2>/dev/null | while read f; do
  id=$(echo "$f" | grep -oP "docker-\K[a-f0-9]{12}")
  echo "Container ID: $id"
done
```

⚠️ Shows ALL active containers (not just running — any process in the
cgroup). Useful as a starting point.

### 2. Identify processes inside a container

```bash
# PIDs in the container
cat /sys/fs/cgroup/system.slice/docker-<FULL_ID>.scope/cgroup.procs

# What each PID executes
for pid in $(cat /sys/fs/cgroup/system.slice/docker-<ID>.scope/cgroup.procs); do
  cmd=$(cat /proc/$pid/cmdline 2>/dev/null | tr "\0" " " | head -c 200)
  echo "PID $pid: $cmd"
done
```

### 3. Determine the container's network_mode

Compare the process network namespace with the host's:

```bash
host_ns=$(readlink /proc/1/ns/net)
container_ns=$(readlink /proc/<PID>/ns/net)
if [ "$host_ns" = "$container_ns" ]; then
  echo "network_mode: host"
else
  echo "network_mode: bridge (or other)"
fi
```

### 4. Find container IPs via bridge ARP

Knowing which bridge is active (via `ip addr show`):

```bash
# List active bridges
ip addr show | grep -E "^[0-9]+: br-|^[0-9]+: docker" | grep UP

# Show ARP neighbors (active IPs)
ip neigh show dev br-<ID>
```

Example output:
```
172.18.0.5 lladdr de:9a:bb:2b:2a:32 REACHABLE
172.18.0.7 lladdr 66:1d:5b:2c:c2:08 STALE
```

**REACHABLE/STALE** IPs = active containers. **FAILED** = IP does not exist.

### 5. Discover which process listens on which port

```bash
ss -tlnp    # TCP listening, with PID
ss -ulnp    # UDP
```

⚠️ Without root, `ss -p` does not show the process (empty column). Use the port
as a clue and cross-reference with `/proc/PID/cmdline`.

### 6. Test TCP connectivity without tools

```bash
timeout 2 bash -c "echo > /dev/tcp/<IP>/<PORT>" 2>/dev/null && echo "OPEN"
```

Useful for quickly scanning ports on a bridge or host — **only on networks you own or have explicit authorization to probe**:

```bash
# ⚠️ Network scanning — verify authorization before running
for ip in 172.18.0.{1..10}; do
  timeout 1 bash -c "echo > /dev/tcp/$ip/3306" 2>/dev/null && echo "$ip:3306 OK"
done
```

### 7. Read container configuration via docker-compose

Not every container was started with compose, but when it was:

```bash
cat /path/docker-compose.yml
```

Pay special attention to:
- `network_mode:` (host vs bridge)
- `networks:` → `driver:` (host = shares host IP)
- `ports:` (mapping)
- `extra_hosts:` (hostname resolution)
- `environment:` / `env_file:` (configuration variables)

### 8. Check internal configuration files

For services like MySQL/MariaDB, even without container access:

```bash
# Process has config args in cmdline
cat /proc/<PID>/cmdline | tr "\0" " "

# Check default config (host filesystem)
cat /etc/mysql/mysql.conf.d/mysqld.cnf  # Host MySQL
# Container may have a DIFFERENT config

# For MariaDB in network_mode host:
# The container default bind-address is 0.0.0.0
# But the docker run command may override with --bind-address=127.0.0.1
```

### 9. Check ports on the host (outside container)

```bash
# Ports listening on IPv4
ss -tlnp -4
```

Quick common ports table:

| Port | Service | Typical container |
|-------|---------|-----------|
| 3306 | MySQL/MariaDB | mysql-db, web-db |
| 80 | HTTP | nginx, apache |
| 443 | HTTPS | nginx (via reverse proxy) |
| 11211 | Memcached | memcached |
| 10051 | Zabbix trapper | zabbix-server |

### 10. Check MariaDB/MySQL datadir

When the container mounts a volume:

```bash
ls /var/lib/<project>/mariadb/    # or mysql/
# List databases:
ls /var/lib/<project>/mariadb/ | grep -v "^#" | grep -v "^aria\|^ib_\|^mysql\|^performance\|^sys"
```

## Real Case: MariaDB container with network_mode host

A real-world example: a `mysql-db` container (mariadb:10.5) was configured with
`network_mode: host` and mysqld was running (active PID), but it was **not
listening on any port 3306** — neither TCP nor Unix socket.

Diagnosis performed:
1. `cat /proc/<PID>/cmdline` → confirmed mysqld with MariaDB args
2. `readlink /proc/<PID>/ns/net == readlink /proc/1/ns/net` → network_mode host
3. `ss -tlnp` → **zero** port 3306 on any IP
4. `cat /etc/mysql/mysql.conf.d/mysqld.cnf` → bind-address = 127.0.0.1 on host
   (but this is the host config, not the container's)
5. `ls /var/lib/<project>/mariadb/` → datadir present with databases
6. Bridge 172.18.0.0/16 active (with containers) vs 172.19.0.0/16 linkdown

**Conclusion:** The MariaDB inside the container did not complete initialization
correctly or the default `bind-address` (0.0.0.0 in official mariadb) was
overridden. Requires `docker logs <container>` (with docker access) for
final diagnosis.

## Pitfalls

| Problem | Cause | Solution |
|----------|-------|---------|
| `ls /proc/PID/fd/` empty | PID runs as different UID (e.g. 999 = mysql) | Try `sudo ls` or use other techniques |
| `nsenter` access denied | No CAP_SYS_ADMIN permission | Do not use nsenter without sudo |
| `ip neigh` shows FAILED | Container with network_mode host (no dedicated IP) | Container shares host IP; look for port on host |
| Bridge linkdown but IP configured | Docker network without containers (created but unused) | Check which bridge has REACHABLE/STALE traffic |
| `docker logs` unavailable | No docker CLI access | Only option: `journalctl` or process logs in datadir |
