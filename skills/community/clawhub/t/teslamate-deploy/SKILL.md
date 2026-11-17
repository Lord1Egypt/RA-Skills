---
name: teslamate-deploy
description: This skill should be used when the user wants to install or deploy TeslaMate (a self-hosted Tesla vehicle data logger + Grafana dashboard) on a local machine or a remote Linux server. Triggers include requests like "install TeslaMate", "deploy TeslaMate", "装 teslamate", "部署 teslamate", "在云服务器上跑个 teslamate", or "set up a Tesla data logger". The skill handles target selection, pre-flight checks, running the bundled deploy scripts, post-install health checks, and producing a user-facing usage document.
agent_created: true
---

# TeslaMate Deploy

Deploy TeslaMate (Tesla vehicle data logger + Grafana dashboards) onto either the local machine or a remote Linux server, end-to-end. Wraps the bundled shell scripts with pre-flight checks, post-install verification, and a generated usage document.

## When to use this skill

Trigger this skill when the user asks to:

- "Install TeslaMate" / "装个 TeslaMate" / "帮我跑个 teslamate"
- "Deploy TeslaMate to a server" / "把 teslamate 部署到 X.X.X.X"
- "Set up a Tesla data logger"
- "在云服务器上装个 teslamate" / "在我的 VPS 上跑 teslamate"

Do **not** use this skill for:

- Configuring an already-running TeslaMate (use TeslaMate's own web UI; the skill is for *install* only)
- Upgrading TeslaMate (out of scope of the bundled scripts)
- Setting up a non-Debian-family target (the bundled scripts use `apt-get`)
- Provisioning a new VM (the scripts only install Docker + TeslaMate; they do **not** create a VM — the user must already have a Linux host)

## Supported targets

The script supports any Debian-family distro that exposes `apt-get` and `systemctl`, including:

- **Ubuntu** (any LTS — 20.04 / 22.04 / 24.04)
- **Debian** (11 / 12 / 13)
- **Armbian** (Amlogic / Allwinner / Rockchip / Raspberry Pi CM4 boxes — `ID=debian` in os-release)
- **Raspberry Pi OS** (bookworm / bullseye)

For Armbian SBCs (S905l3 / S922 / H616 / RK3588 etc.), use `REMOTE_USER=root` because these boards typically only enable root SSH out of the box.

## Bundled resources

| File | Purpose |
|---|---|
| `scripts/deploy-setup.sh` | Entry script. With no arg → local install. With one IP arg → SSH to that server and install. |
| `scripts/install-teslamate.sh` | Local install logic. Auto-detects / installs Docker, writes `.env`, pulls images (docker pull → GitHub tgz fallback, or `--github-image` to force GitHub), starts stack. |
| `scripts/docker-compose.yml` | Stack definition: `teslamate` (port 4000) + `postgres:17` + `grafana` (port 3000) + `mosquitto` (port 1883). |
| `scripts/README.md` | Author's original Chinese README (reference only; ignore its `postgres:16` mention — `docker-compose.yml` is the source of truth and uses `postgres:17`). |
| `references/troubleshooting.md` | Common failures and their fixes. Load this when an install step fails. |

## Workflow

Follow these steps in order. Use `AskUserQuestion` for the inputs, then run the script via the Bash tool.

### Step 1 — Confirm target

Ask the user **one** question:

> "装在本地还是远程服务器？"
> - 本地（直接在这台机器上跑）
> - 远程服务器（用 SSH 推到另一台 Ubuntu / Debian）

If remote, ask the follow-ups:

> "服务器 IP 是？SSH 端口默认 22，用户名默认 `ubuntu`（Armbian 盒子/root 免密通常用 `root`），对吗？"
> - Yes, use defaults (`ubuntu` / port 22)
> - Different SSH user (e.g. `root` for Armbian) / different port

> "SSH 用密钥还是密码？"
> - **密钥**（默认，ssh key 已配好免密）
> - **密码**（每次连接输密码，需要本地安装 sshpass）

Collect: `target` ∈ {`local`, `remote`}; if remote, also `server_ip`, `ssh_user` (default `ubuntu`), `ssh_port` (default 22), `ssh_auth` ∈ {`key`, `password`}.

If `ssh_auth=password`:
1. Check `sshpass` availability locally: `sshpass -V` — if missing, install with `brew install hudochenkov/sshpass/sshpass`
2. Ask the user for the password via `read -sp` (in the terminal, NOT in chat)
3. Export `SSH_PASS` before running deploy-setup: `SSH_PASS=xxx ./deploy-setup.sh <ip>`

### Step 2 — Pre-flight checks

Before running the install, verify:

1. **OS family** (remote only): `ssh $ssh_user@$server_ip "cat /etc/os-release | grep ^ID="`. Must be `ubuntu` or `debian`. If not, stop and tell the user the script only supports Debian-family distros.
2. **SSH reachability** (remote only):
   - Key mode: `ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 $ssh_user@$server_ip echo ok`. If it fails, ask the user to confirm SSH key is set up.
   - Password mode: `sshpass -p "TEST_OK" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR $ssh_user@$server_ip echo ok 2>/dev/null`. If it fails, ask the user to re-enter the password.
   - **首次连接**（两种模式均适用）：`StrictHostKeyChecking=no` 自动跳过 `yes/no` 确认，`UserKnownHostsFile=/dev/null` 避免写 known_hosts 权限问题，`LogLevel=ERROR` 隐藏警告信息，保证全程无交互。
3. **sshpass check** (password mode only): if `sshpass -V` returns non-zero, install with `brew install hudochenkov/sshpass/sshpass` (macOS) or `sudo apt-get install sshpass` (Linux).
4. **Port availability**:
   - Local: `lsof -i :3000 -i :4000 -i :1883` (or warn if non-zero exit)
   - Remote: `ssh $ssh_user@$server_ip "ss -ltn | grep -E ':(3000|4000|1883) '"`
   - If any port is occupied, stop and ask the user to either free it or accept a different port (out of skill scope — flag it).
4. **Skill scripts present**: confirm `~/.workbuddy/skills/teslamate-deploy/scripts/{deploy-setup.sh,install-teslamate.sh,docker-compose.yml}` exist. If not, the skill install is broken — stop and tell the user to re-install the skill.

### Step 3 — Run the deploy

```bash
SKILL_DIR="$HOME/.workbuddy/skills/teslamate-deploy"
# 临时拷贝到 ~/teslamate-deploy 一起执行 (install 脚本需要 docker-compose.yml 在同目录)
WORK=/tmp/teslamate-deploy-$USER
rm -rf "$WORK" && mkdir -p "$WORK"
cp "$SKILL_DIR/scripts/"{deploy-setup.sh,install-teslamate.sh,docker-compose.yml} "$WORK/"
chmod +x "$WORK/deploy-setup.sh" "$WORK/install-teslamate.sh"
cd "$WORK"
# 默认用户 ubuntu；要以 root 部署（Armbian 盒子）: REMOTE_USER=root ./deploy-setup.sh <ip>
./deploy-setup.sh $server_ip
```

The script accepts an optional `REMOTE_USER` env var to override the default `ubuntu` user (e.g. `REMOTE_USER=root` for Armbian SBCs). The remote work dir is `/home/$REMOTE_USER/teslamate` for normal users and `/root/teslamate` for root.

Why copy to `/tmp`: `install-teslamate.sh` looks for `docker-compose.yml` in the current dir, and writes `.env` / `import/` there. Keeping it out of the skill dir prevents polluting the skill itself.

Stream the script's output to the user (it's verbose and helpful). Expect a 3–10 minute run: Docker install + 4 image pulls + stack up.

If the target network cannot reach Docker Hub or mirrors reliably, prepend `--github-image` to force downloading pre-packaged images from GitHub:
```bash
# In deploy-setup.sh, the remote invocation passes --github-image via the SSH heredoc
# The install_teslamate function accepts it as: install_teslamate "true"
# Manually on the target:
cd /root/teslamate && sudo ./install-teslamate.sh --github-image
```

### Step 4 — Post-install health check

After the script exits 0, verify:

```bash
# For local:
curl -fsS -o /dev/null -w "Grafana: HTTP %{http_code}\n" http://localhost:3000/api/health
curl -fsS -o /dev/null -w "TeslaMate: HTTP %{http_code}\n" http://localhost:4000
docker compose ps --format 'table {{.Name}}\t{{.Status}}\t{{.Ports}}'

# For remote: same but with ssh + curl-over-ssh, e.g.
ssh $ssh_user@$server_ip "curl -fsS -o /dev/null -w 'Grafana: %{http_code}\n' http://localhost:3000/api/health"
ssh $ssh_user@$server_ip "cd /home/$ssh_user/teslamate && sudo docker compose ps"
```

Pass criteria: Grafana returns 200, TeslaMate returns 200 (or 30x redirect), all 4 containers `Up`. If TeslaMate returns 503 / connection refused within 1–2 minutes, that's normal — the database is still initializing. Re-check after 90 seconds.

### Step 5 — Generate usage document

Create a markdown file at the workspace's outputs directory (or `~/.workbuddy/outputs/teslamate-usage-$TIMESTAMP.md` if outside a workspace). Use this template:

```markdown
# TeslaMate 部署完成 🚗

## 访问地址

| 服务 | URL | 端口 | 默认账号 |
|---|---|---|---|
| TeslaMate | http://$HOST:4000 | 4000 | (登录前需要先在 TeslaMate UI 配 Tesla 账号) |
| Grafana | http://$HOST:3000 | 3000 | `admin` / `admin` |
| MQTT (mosquitto) | `$HOST:1883` | 1883 | (无认证，**仅限内网使用**) |

> 远程部署时把 `localhost` 换成服务器 IP；首次访问 Grafana 会被强制改 admin 密码。

## 第一步：配置 Tesla 账号

TeslaMate v4+ 支持**两种**认证方式，**强烈推荐方案 A**：

### 方案 A：Tesla API Key（永久，不过期，推荐）

1. 浏览器打开 https://developer.tesla.com/ → 用 Tesla 账号登录
2. 左侧 "API Access" → 顶部 "Add API Key" → 起个名字，勾选 scopes：
   - `vehicle_device_data`（必须）
   - `vehicle_cmds`（必须）
   - `vehicle_location`（必须）
3. 复制生成的 key（只显示一次！）
4. 编辑部署机上的 `.env`：
   ```bash
   ssh root@$HOST 'cd /root/teslamate && nano .env'
   # 加上：
   TM_API_KEY=<粘贴 key>
   TM_VIN=<你的 17 位车架号>
   ```
5. `cd /root/teslamate && docker compose up -d teslamate`

**优点**：key 不过期、不用手动续，配置一次永久。

### 方案 B：Legacy OAuth（8 小时过期，不推荐）

适合没有 developer.tesla.com 账号的场景：

1. Mac 跑 `tesla_auth`（`./tesla_auth-aarch64-apple-darwin`），从输出里复制 **ACCESS TOKEN**（不是 refresh token）
2. 打开 http://$HOST:4000，把 token 粘进去，再填 VIN

**⚠️ 大坑**：access token 有效期只有 **8 小时**。从复制到粘贴尽量控制在几分钟内，否则 token 会过期，TeslaMate 报 "令牌无效" 错误。架构（arm64/arm32）和系统时间都不是问题，**就是 8h 时间窗**。

### 快速恢复：交互式 auth 设置脚本

如果 token 过期了，重设最快的方式：
```bash
# 在 Mac 上
ssh root@$HOST '/root/teslamate/set-auth.sh'
# 按提示选 1 或 2，粘贴 token/key + VIN
```
脚本会用 `read -p` 静默读入，不会把 token 写进 shell 历史。脚本会自动备份 `.env` 到 `.env.bak.YYYYMMDD-HHMMSS`。

## 常用运维命令

```bash
# 看所有容器状态
sudo docker compose ps

# 看 TeslaMate 实时日志
sudo docker compose logs -f teslamate

# 改默认密码 / 加密密钥
cd ~/teslamate    # 远程是 /home/$ssh_user/teslamate
sudo nano .env     # 改完重启: sudo docker compose up -d
```

## 注意事项

- 默认密码 `teslamate123` 和 Grafana `admin/admin` **请尽快改掉**
- 端口 3000 / 4000 / 1883 直接暴露在公网不安全；建议至少开防火墙只放行你信任的 IP，或者套个 Nginx + Let's Encrypt
- 数据库默认没做备份 —— 参考 https://docs.teslamate.org/docs/guides/backup
```

Tell the user the file path and offer to open it. Also tell them the access URLs directly in chat.

## Critical rules

- **Never run `deploy-setup.sh` against `localhost` or `127.0.0.1` as a "remote" target** — that would loop back and double-install. If the user wants local, run without args.
- **Never edit the bundled scripts in place.** The skill owns them; per-session copies go in `/tmp/teslamate-deploy-$USER/`.
- **Never `git push` to the original GitHub repo from inside the skill.** The skill is for deploying, not for modifying the source.
- **If the script fails mid-way, do not retry blindly.** Read the error, check `references/troubleshooting.md`, and surface the relevant fix to the user.
- **The bundled default `TM_ENCRYPTION_KEY` and `TM_DB_PASS` are intentionally weak** (they're demo values from the original author). The generated usage document must warn the user to change them.
- **When a step appears "stuck" (no output for >60s on a network operation), don't assume success or failure — poll the process state first** with `pgrep -af <cmd>` on the remote. Long-running operations like `apt-get` over slow mirrors and `docker pull` of large images can legitimately take minutes.

## Recovery playbook for stuck installs

If `setup_server` or `install_teslamate` hangs at one of these points:

| Hang point | Likely cause | First move |
|---|---|---|
| `apt-get install docker.io ...` | `containerd.io` Conflicts (host has Docker preinstalled) | `pkill -9 apt-get dpkg` → check if compose is already working |
| `docker compose pull` "Pulling fs layer" for >5min | Mirror backend slow or no cache for this image | Try a different mirror; if all fail, use `--github-image` to download pre-packaged images from GitHub, or fall back to **relay host** strategy (below) |
| `dial tcp [2a03:...:443]: i/o timeout` | IPv6 blackholed | Add `precedence ::ffff:0:0/96 100` to `/etc/gai.conf` |
| `dial tcp: lookup mirror.ccs.tencentyun.com: no such host` | Internal mirror on non-Tencent host | Skill auto-detects now; manual: `getent hosts` to find a reachable mirror |

**GitHub image download (simpler alternative)** — skip relay host entirely:

```bash
# On the target server, direct download from GitHub:
cd /root/teslamate && sudo ./install-teslamate.sh --github-image
```

`install-teslamate.sh --github-image` downloads `sha256sums.txt` from GitHub, fetches each file with SHA256 verification, then loads into Docker. Files >90MB are pre-split into `.aa, .ab, ...` parts and auto-merged.

**Relay host fallback** (when GitHub is also unreachable):

1. Ask the user for a "good network" host they can SSH to (e.g. a Tencent CVM, or any cloud VM with `mirror.ccs.tencentyun.com` configured)
2. From that relay: `docker pull <image> && docker save <image> -o /tmp/<image>.tar && chmod 644 /tmp/<image>.tar`
3. From your local Mac: `scp RELAY:/tmp/<image>.tar /tmp/<image>.tar && scp /tmp/<image>.tar TARGET:/tmp/<image>.tar`
4. On target: `docker load -i /tmp/<image>.tar && cd ~/teslamate && docker compose up -d`

160MB postgres:17 round-trip ≈ 3 minutes vs indefinite hang.

## What this skill does NOT do

- Provision a VM (Vagrant / cloud-init / UTM)
- Backup / restore existing TeslaMate data
- Upgrade an existing install
- Configure HTTPS / reverse proxy
- Multi-node / HA setups
- Non-Debian-family OSes

If the user asks for any of these, tell them the skill's scope ends at "install + verify + document" and point them to the appropriate next step (e.g. "use `vagrant up` to provision first, then come back to this skill").
