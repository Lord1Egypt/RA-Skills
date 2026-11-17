# TeslaMate Deploy — Troubleshooting

Load this file when any step in the SKILL.md workflow fails. Each section gives the symptom, the likely cause, and a concrete fix. The user can run the shell snippets themselves if the AI hasn't already tried them.

## 0. `deploy-setup.sh` / SSH transport problems

### `Connection closed by <ip> port 22` (especially during the `scp` steps)

**Symptom**: setup_server() succeeds, but `scp docker-compose.yml ...` or `scp install-teslamate.sh ...` fails with `Connection closed by <ip> port 22`. The first `ssh` works, then a few seconds later scp dies.

**Cause**: the original `deploy-setup.sh` opens **6+ independent SSH/scp sessions** back-to-back (1 setup + 1 mkdir + 2 scp + 1 install = 6, with each `scp` opening a fresh SSH connection). OpenSSH defaults to `MaxSessions=10` and `MaxStartups=10:30:100`. Combined with any pre-existing connection in the pool, the 11th concurrent unauthenticated connection gets dropped.

**Why the install-teslamate.sh step usually still works**: that one runs over a long-lived SSH connection inside a single shell, so it counts as 1 session.

**Fix** (already applied in current `deploy-setup.sh`): use **OpenSSH ControlMaster multiplexing** so all ssh/scp calls share one master connection:
```bash
SSH_OPTS=(
    -o ControlMaster=auto
    -o ControlPath="${TMPDIR:-/tmp}/teslamate-deploy-ssh-%r@%h:%p"
    -o ControlPersist=600
)
# First call: spawn master with -fN
# Subsequent ssh/scp calls: share the master
```

If you can't upgrade the script, the **manual recovery** is to do everything sequentially in one shell:
```bash
ssh ubuntu@<ip> 'mkdir -p /home/ubuntu/teslamate'
scp docker-compose.yml ubuntu@<ip>:/home/ubuntu/teslamate/
scp install-teslamate.sh ubuntu@<ip>:/home/ubuntu/teslamate/
ssh ubuntu@<ip> 'cd /home/ubuntu/teslamate && sudo ./install-teslamate.sh --install-docker'
```
…with a 2-3 second `sleep` between each call.

**To verify it's a MaxSessions problem** (not auth/network): check the server's `sshd_config`:
```bash
ssh ubuntu@<ip> 'sudo grep -E "^(MaxSessions|MaxStartups)" /etc/ssh/sshd_config'
# Default: MaxSessions 10, MaxStartups 10:30:100
```
If those are non-default and lower, that's the smoking gun.

## 1. `install-teslamate.sh` errors

### `dpkg: error: dpkg frontend is locked by another process`

**Cause**: another `apt` is running (auto-update, snap, unattended-upgrades).

**Fix**:
```bash
# 等现有 apt 跑完
sudo lsof /var/lib/dpkg/lock-frontend
# 或强制解锁 (最后手段, 确认没有 apt 在跑)
sudo killall apt apt-get dpkg 2>/dev/null
sudo rm /var/lib/dpkg/lock-frontend /var/lib/dpkg/lock /var/cache/apt/archives/lock 2>/dev/null
sudo dpkg --configure -a
```

### `E: Unable to fetch ... Could not resolve ...`

**Cause**: no DNS or no internet on the target host.

**Fix**:
```bash
ping -c2 8.8.8.8                    # 基础连通性
ping -c2 archive.ubuntu.com          # DNS + 域名
cat /etc/resolv.conf                # DNS 配置
# 临时换 DNS
echo "nameserver 1.1.1.1" | sudo tee /etc/resolv.conf
```

### `permission denied` on Docker commands

**Cause**: current user not in the `docker` group, script falls back to `sudo docker`.

**Fix**: if `sudo docker` itself fails, passwordless sudo isn't configured. Either:
- Add the user to `docker` group: `sudo usermod -aG docker $USER` (logout/login required)
- Or configure passwordless sudo: `echo "$USER ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/$USER`

### `docker compose version` returns "command not found"

**Cause**: installed `docker-compose` (v1) instead of `docker compose` (v2 plugin). The script checks for both, but some older images only have v1.

**Fix**:
```bash
# 装 v2 plugin (Ubuntu 22.04+)
sudo apt-get install -y docker-compose-v2
# 装 v1 binary (兜底)
sudo apt-get install -y docker-compose
```

## 2. Image pull problems

### `ERROR: pull access denied for ...` or `toomanyrequests`

**Cause**: hit Docker Hub rate limit, OR the configured mirror (`mirror.ccs.tencentyun.com`) is unreachable from the target host.

**Fix**:
```bash
# 看当前 mirror 配置
cat /etc/docker/daemon.json

# 测 mirror 是否通
curl -fsS -o /dev/null -w "tencent mirror: %{http_code}\n" https://mirror.ccs.tencentyun.com/v2/
curl -fsS -o /dev/null -w "docker hub: %{http_code}\n" https://registry-1.docker.io/v2/

# 换 mirror (比如用国内通用 mirror.aliyuncs.com)
sudo tee /etc/docker/daemon.json > /dev/null << 'EOF'
{
  "registry-mirrors": [
    "https://mirror.aliyuncs.com",
    "https://mirror.ccs.tencentyun.com"
  ]
}
EOF
sudo systemctl restart docker

# 重试
cd ~/teslamate   # 远程是 /home/ubuntu/teslamate
sudo docker compose pull
```

### Pull hangs for >5 minutes, no progress

**Fix**:
```bash
# 中断当前 pull, 重启 docker daemon
sudo systemctl restart docker
# 单个 image 试拉, 确认网络
sudo docker pull postgres:17
```

### All mirrors time out only for `postgres:17` (or specific image)

**Symptom**: `docker pull alpine:3.19` works fast (seconds), `docker pull postgres:17` hangs forever on "Pulling fs layer" with no progress. Multiple public mirrors all exhibit the same hang.

**Cause**: this specific image's manifest or blobs aren't cached at the public mirror backend, or the mirror is rate-limiting. Different images go to different backend shards.

**Fix — relay host strategy**: use a host that has working network as a "staging area" to pull the image, save it as a tar, then load it on the target:

```bash
# On relay host (e.g. a Tencent CVM that has mirror.ccs.tencentyun.com working)
ssh ubuntu@RELAY_IP
sudo docker pull postgres:17                  # 32s on a CVM with internal mirror
sudo docker save postgres:17 -o /tmp/pg17.tar
sudo chmod 644 /tmp/pg17.tar                  # let non-sudo scp read it
exit

# On your Mac (the deploy machine)
scp ubuntu@RELAY_IP:/tmp/pg17.tar /tmp/pg17.tar
scp /tmp/pg17.tar root@TARGET_IP:/tmp/pg17.tar

# On target
ssh root@TARGET_IP
docker load -i /tmp/pg17.tar
rm /tmp/pg17.tar
cd /root/teslamate
docker compose up -d
```

Total transfer: ~160MB for postgres:17. Takes ~3 minutes round-trip vs 5+ minutes of hanging with no progress.

### GitHub image download (alternative to relay host)

`prepare-images.sh` supports downloading pre-packaged images from GitHub as a fallback when `docker pull` fails due to mirror issues.

**GitHub repo**: `https://github.com/martinbj2008/docker_images`

**Directory structure**:
```
docker_images/
├── eclipse-mosquitto/
│   └── 2/
│       ├── eclipse-mosquitto-2.tar.gz
│       └── sha256sums.txt
├── postgres/
│   └── 17/
│       ├── postgres-17.tar.gz.aa   (split if >90MB)
│       ├── postgres-17.tar.gz.ab
│       └── sha256sums.txt
├── teslamate_teslamate/
│   └── latest/
│       ├── teslamate_teslamate-latest.tar.gz
│       └── sha256sums.txt
└── teslamate_grafana/
    └── latest/
        ├── teslamate_grafana-latest.tar.gz.aa
        ├── teslamate_grafana-latest.tar.gz.ab
        ├── teslamate_grafana-latest.tar.gz.ac
        └── sha256sums.txt
```

**Manual download and load (without prepare-images.sh)**:
```bash
# Single-file image (<90MB)
curl -sL https://raw.githubusercontent.com/martinbj2008/docker_images/main/postgres/17/postgres-17.tar.gz \
  | gunzip | docker load

# Split image (>90MB): download all parts, cat, gunzip, load
for suf in aa ab ac; do
  curl -sL "https://raw.githubusercontent.com/martinbj2008/docker_images/main/teslamate_grafana/latest/teslamate_grafana-latest.tar.gz.$suf" \
    -o "/tmp/part.$suf"
done
cat /tmp/part.* | gunzip | docker load
rm /tmp/part.*
```

**To upload new versions** (run on a machine with Docker + SSH key to GitHub):
```bash
cd /path/to/skill/scripts
./prepare-images.sh upload
```
This saves all 4 images, splits files >90MB, generates SHA256 checksums, and pushes to GitHub.

### `dial tcp [2a03:2880:...:443]: i/o timeout` (IPv6 path is blackholed)

**Symptom**: even with `registry-mirrors` configured, `docker pull` fails with:
```
dial tcp [2a03:2880:f107:83:face:b00c:0:25de]:443: i/o timeout
```

**Cause**: `getent ahosts registry-1.docker.io` returns both A and AAAA records; the system resolver picks the AAAA first; but the IPv6 path to that range is blackholed (common on home ISPs, China Telecom residential, etc.).

**Fix — force IPv4 in the system resolver**:
```bash
# Check what gai.conf currently has
grep -v "^#" /etc/gai.conf | grep -v "^$" || echo "gai.conf empty"
# Add the IPv4 precedence rule
echo "precedence ::ffff:0:0/96 100" | sudo tee -a /etc/gai.conf
# Re-test
getent ahosts registry-1.docker.io   # should now show only A records
```

Combined with the `daemon.json` setting `"ipv6": false, "ip6tables": false`, Docker daemon will now resolve and connect over IPv4.

### `dial tcp: lookup mirror.ccs.tencentyun.com: no such host`

**Cause**: `mirror.ccs.tencentyun.com` is a **Tencent Cloud internal mirror**, only resolvable from inside a Tencent Cloud VPC. If the target is on a home LAN or a non-Tencent cloud, the DNS lookup will fail and Docker will use it as a registry, fail all pulls.

**Fix**: the skill now auto-detects which mirror is resolvable (see `install_docker()` in `install-teslamate.sh`). For manual override:

```bash
# 1. Check what's resolvable from this host
getent hosts mirror.ccs.tencentyun.com && echo "tencent internal: OK" || echo "tencent internal: NO"
getent hosts docker.1ms.run && echo "1ms.run: OK" || echo "1ms.run: NO"
getent hosts docker.m.daocloud.io && echo "daocloud: OK" || echo "daocloud: NO"

# 2. Pick one that's OK and write to daemon.json
sudo tee /etc/docker/daemon.json > /dev/null << 'EOF'
{
  "ipv6": false,
  "ip6tables": false,
  "registry-mirrors": ["https://docker.1ms.run"]
}
EOF
sudo systemctl restart docker
```

## 3. Port conflicts

### `bind: address already in use` on 3000 / 4000 / 1883

**Find what's holding the port**:
```bash
sudo ss -ltnp | grep -E ':(3000|4000|1883) '
# 或
sudo lsof -i :3000 -i :4000 -i :1883
```

**Fix**: either stop the conflicting service, or change the host port in `docker-compose.yml` (e.g. `3001:3000`) and re-run `sudo docker compose up -d`. Note: changing the TeslaMate / Grafana port is fine, but Mosquitto on a non-default port means the TeslaMate container can't reach it via `mosquitto:1883` unless you also update the TeslaMate env. Easier to free the port.

## 4. Remote (SSH) problems

### `ssh: connect to host X.X.X.X port 22: Connection refused`

**Cause**: wrong IP, firewall blocking, or SSH on non-standard port.

**Fix**:
```bash
# 验证机器本身可达
ping -c2 X.X.X.X
# 测常见替代端口
nc -zv X.X.X.X 22 2>&1
nc -zv X.X.X.X 2222 2>&1
# 云服务商安全组需要在控制台放行 22 (出站默认通, 入站要放)
```

### `Permission denied (publickey)` on SSH

**Cause**: the deploy machine doesn't have a private key matching what's in `ubuntu@$server_ip:~/.ssh/authorized_keys`.

**Fix**: the user needs to add the deploy machine's public key to the server. Ask them to run (on the deploy machine):
```bash
cat ~/.ssh/id_ed25519.pub    # 或 id_rsa.pub
```
…then paste that into the server's `~/.ssh/authorized_keys`. If no key exists yet:
```bash
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519
ssh-copy-id ubuntu@X.X.X.X   # 首次需要输密码
```

### `Host key verification failed`

The script uses `ssh -o StrictHostKeyChecking=no` so this is unlikely, but if it happens it means SSH is rejecting the cipher/algorithm. Fix the server's `sshd_config` to allow modern algorithms, or pre-populate `known_hosts`:
```bash
ssh-keyscan -H X.X.X.X >> ~/.ssh/known_hosts
```

## 5. Post-install: container unhealthy

### TeslaMate returns 503 for the first 1–2 minutes

**Not actually a problem.** Postgres is doing its initial bootstrap. Re-check after 90 seconds:
```bash
sudo docker compose ps
sudo docker compose logs postgres | tail -30
```

### `docker compose ps` shows `Restarting` or `Exit 1`

**Fix**:
```bash
sudo docker compose logs <service-name>     # e.g. teslamate / postgres / grafana
# 常见: .env 文件没生成, 或 TM_ENCRYPTION_KEY 长度不够
cat ~/teslamate/.env    # 远程是 /home/ubuntu/teslamate/.env
# 重新生成 .env
cd ~/teslamate
sudo docker compose down
./install-teslamate.sh
```

### Restart prompts re-login, logs show `No ENCRYPTION_KEY was found` / `Could not decrypt API tokens!`

**Symptom**: after `docker restart teslamate-teslamate-1` (or any host reboot), the Web UI immediately shows the sign-in page again. `docker logs teslamate-teslamate-1` shows:
```
[warning] No ENCRYPTION_KEY was found to encrypt and securely store your API tokens.
[warning] Create an environment variable named "ENCRYPTION_KEY" with the value set to the key above...
[warning] Could not decrypt API tokens!
```

**Cause**: TeslaMate encrypts the stored API refresh token with a key. On first start, if no `ENCRYPTION_KEY` env is set, it generates a random 32-byte base64 key for that session and stores the encrypted token in the `settings` table. On every restart, with no env set, a **new** random key is generated → the old encrypted token can't be decrypted → user must re-login.

**Fix — set a fixed `ENCRYPTION_KEY` env var in `docker-compose.yml` and re-login once**:

```bash
# 1. Generate a fixed key (keep this safe; changing it later invalidates stored tokens)
openssl rand -base64 32
# → e.g. EvJgrT/546llnPOnGhG4fT8FDoWDD9ttni3x0GA+FIo=

# 2. Add to teslamate service environment in docker-compose.yml
#    services.teslamate.environment:
#      - MQTT_HOST=mosquitto
#      - ENCRYPTION_KEY=EvJgrT/546llnPOnGhG4fT8FDoWDD9ttni3x0GA+FIo=
sed -i '/MQTT_HOST=mosquitto/a\      - ENCRYPTION_KEY=EvJgrT/546llnPOnGhG4fT8FDoWDD9ttni3x0GA+FIo=' \
  /root/teslamate/docker-compose.yml

# 3. Recreate the container (this WILL log out the user; they need to sign in once)
cd /root/teslamate && docker compose up -d teslamate

# 4. Open http://<host>:4000/sign_in, paste the REFRESH token, submit
#    → this writes a new token encrypted with your fixed key
#    → future restarts will decrypt it automatically
```

**Important**: the value must be 32 random bytes encoded as base64 (44 chars including `=`). Don't use a guessable string. Don't change it after the first successful login unless you're willing to do one more manual re-login.

**Verification** that the env is being picked up:
```bash
ssh root@<host> 'docker exec teslamate-teslamate-1 env | grep ENCRYPTION_KEY'
# Should print ENCRYPTION_KEY=EvJgrT...
```

**Why this trips up most users**: the warning message in the logs is easy to miss because teslamate keeps running and the web UI just redirects to `/sign_in` silently. The user thinks "oh, just a transient blip" and re-logs in, only to hit the same wall on the next restart.

### Grafana says "login attempt failed" after the user changed `admin/admin`

**Fix**: reset Grafana admin password via the official env var:
```bash
cd ~/teslamate
sudo docker compose stop grafana
# 在 docker-compose.yml 给 grafana 加一条 env:
#   - GF_SECURITY_ADMIN_PASSWORD=newpassword
sudo docker compose up -d grafana
# 登录后立刻在 UI 里把这个 env 删掉
```

## 6. Linking the Tesla account

### "Invalid refresh token"

**Cause**: most common cause is using a *legacy* token (the old auth flow that Tesla deprecated in 2023). User must re-generate.

**Fix**: walk the user through https://docs.teslamate.org/docs/guides/initial_setup — they need to log into `auth.tesla.com` (NOT `owner-api.teslamotors.com`) in a *normal browser session*, grab a fresh refresh token, and paste it into TeslaMate. The token is ~700 chars and starts with `eyJ…`.

### TeslaMate web UI: "Error: 令牌 无效" (token invalid) — within minutes of pasting

**Symptom**: user runs `tesla_auth` (the `tesla_auth-aarch64-apple-darwin` binary from adrianj/tesla_auth), gets a valid-looking access token, copies it to TeslaMate, and the UI immediately says "令牌 无效" (token invalid). The error message in the UI looks like:
> 令牌 eyJ... 刷新令牌 eyJ...
> 通过 Tesla API 获得令牌需要有编程经验或者借助第三方服务。更多信息可以查看 [这里]。

**TeslaMate v4 sign-in page has TWO input boxes** (not one as previously documented): "令牌" (Token) and "刷新令牌" (Refresh Token). User must fill BOTH with the access + refresh tokens respectively. Internally, TeslaMate only uses the refresh token (it does the `auth.tesla.cn POST /oauth2/v3/token` call to exchange for an access token — this is what you see in the logs as `POST auth.tesla.cn -> 200`).

**Most common actual causes of "令牌 无效"** (in order of likelihood):

1. **Network timeout to `auth.tesla.cn`**: TeslaMate's internal HTTP client (Finch) has a ~5s timeout. `auth.tesla.cn` from China residential ISPs / cloud servers can occasionally respond in 6-8s. The log will show:
   ```
   [error] POST https://auth.tesla.cn/oauth2/v3/token -> error: %Finch.TransportError{reason: :timeout, ...} (~6800ms)
   ```
   The token is fine; just retry.

2. **User pasted the access token, not the refresh token**: `tesla_auth` outputs two tokens. The **refresh token** is what TeslaMate needs (it then exchanges for access token). The refresh token is the second `eyJ...` block, ~3 months valid. Decoding JWT payloads to tell them apart:
   - Access: has `exp` field (8h after `iat`), `aud` is an array, has `azp: ownerapi`
   - Refresh: no `exp`, `aud` is the string `https://auth.tesla.cn/oauth2/v3/token`, has a nested `data: {...}` object

3. **Stale UI state from a previous failed attempt**: the error message persists on the sign-in page even after the underlying issue is fixed. User must **reload the page** (Cmd+Shift+R for hard reload) before retrying.

**🚨 NEVER paste Tesla tokens in chat** — they are valid credentials. Use `/root/teslamate/set-auth-v2.sh` on the target host (it prompts over SSH, no token in chat/logs). If a token is accidentally exposed, revoke it immediately at https://auth.tesla.cn or change the Tesla account password (invalidates all active refresh tokens).

**Bypass the UI entirely** (most reliable when network is flaky): the setup script writes `TM_AUTH_TOKEN` directly to `/root/teslamate/.env` and restarts the container — no HTTP round-trip to Tesla during the auth write, so GFW flakiness doesn't matter.

**Architecture is NOT the issue** — `tesla_auth` is a local OAuth client; whether you run it on `aarch64-apple-darwin` (M1/M2 Mac), `arm32`, or `x86_64`, the JWT output is the same string. Tesla's auth server validates by `exp` timestamp, not by client architecture.

**System clock skew is also NOT the issue** on this stack — both Mac and the target host use NTP, typically within 1 second. (Verify with `date '+%s'` on both sides.)

**Three fixes (in order of preference):**

1. **Best: switch to Tesla API Key (permanent, no expiry)**:
   - Go to https://developer.tesla.com/ → log in with Tesla account → "API Access" tab → "Add API Key"
   - Required scopes: `vehicle_device_data`, `vehicle_cmds`, `vehicle_location`
   - In TeslaMate's `.env`, set `TM_API_KEY=<your-key>` (instead of `TM_AUTH_TOKEN`)
   - Restart `docker compose up -d teslamate`

2. **Quick (legacy): use the REFRESH token from tesla_auth, not the access token**:
   - Re-run `tesla_auth` if you don't have the refresh token anymore
   - Paste the **REFRESH TOKEN** (the second block) into TeslaMate's web UI
   - The refresh token lasts ~3 months, so this is a one-time setup

3. **Setup script for safe token entry** — write to target's `/root/teslamate/set-auth.sh` (already done on this user's box):
   ```bash
   #!/bin/bash
   set -e
   ENV_FILE=/root/teslamate/.env
   cp "$ENV_FILE" "${ENV_FILE}.bak.$(date +%Y%m%d-%H%M%S)"
   sed -i -E '/^TM_AUTH_TOKEN=/d; /^TM_API_KEY=/d; /^TM_VIN=/d' "$ENV_FILE"
   echo "Choose: 1=legacy OAuth (REFRESH token, ~3 months), 2=API key (permanent)"
   read -p "[1/2] (default 1): " method
   method=${method:-1}
   if [ "$method" = "2" ]; then
       read -p "Paste Tesla API key: " k
       echo "TM_API_KEY=$k" >> "$ENV_FILE"
   else
       echo "IMPORTANT: paste the REFRESH TOKEN (second block from tesla_auth),"
       echo "NOT the access token (which expires in 8h)."
       read -p "Paste Tesla REFRESH token: " t
       echo "TM_AUTH_TOKEN=$t" >> "$ENV_FILE"
   fi
   read -p "Vehicle VIN (17 chars): " v
   echo "TM_VIN=$v" >> "$ENV_FILE"
   cd /root/teslamate && docker compose up -d teslamate
   sleep 10 && docker compose logs --tail=20 teslamate
   ```
   User runs `ssh root@<ip> '/root/teslamate/set-auth.sh'` and pastes values when prompted. Token never appears in shell history or logs.

### TeslaMate can fetch the car once, then "401 unauthorized" on the next refresh

**Cause**: Tesla's access tokens now expire in ~8h. The refresh token should auto-refresh; if it doesn't, the user's refresh token itself has been invalidated (Tesla rotates them occasionally).

**Fix**: re-grab a fresh refresh token from `auth.tesla.com` and re-paste it into TeslaMate's UI.

## 7. "It worked yesterday, now TeslaMate is down"

Walk through this in order:

```bash
sudo docker compose ps                   # 哪个挂了?
sudo docker compose logs --tail=200      # 最近的错误
df -h /                                  # 磁盘满了? Postgres 撑爆常见
free -h                                  # OOM?
sudo systemctl status docker             # docker daemon 还活着吗
# 重启整个 stack
cd ~/teslamate
sudo docker compose down
sudo docker compose up -d
```

If disk is full, the most common culprit is `mosquitto-data` or `postgres-data` volumes growing without bound. Check sizes with `sudo docker system df -v`.

## 8. Want to uninstall

```bash
# 停 stack + 删容器 + 删 volumes (数据会丢!)
cd ~/teslamate
sudo docker compose down -v
sudo docker image prune -a
# 远程的话: rm -rf /home/ubuntu/teslamate
```

Always confirm with the user before `-v` (deletes volumes = deletes database = loses all driving history).
