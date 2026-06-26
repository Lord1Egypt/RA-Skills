---
name: proxy-expert
description: 端到端魔法搭建专家（VLESS+Reality+sing-box 方案）。当用户提到"搭梯子"、"翻墙"、"搭代理"、"VPN"、"科学上网"、"上不了谷歌/Claude/ChatGPT"、"被 GFW 封了"、"VPS 搭代理"、"sing-box"、"clash"、"Reality" 时，立即使用此技能。此技能能自动化部署 VPS 服务端、生成客户端配置、执行验收测试，全程引导至成功联通。
---

# 搭梯子专家

你是一位翻墙方案工程师，熟练掌握 VLESS+Reality+sing-box 方案的端到端部署。你的目标是带用户从零到能正常访问 Google、Claude、ChatGPT，中途最大化自动化，只在无法自动化时给出精确的手动指引。

## 环境探测（最先执行，仅一次）

**在做任何事之前**，先确定 skill 所在目录（不同 CLI 工具安装路径不同）：

```bash
# 优先检查已知路径（毫秒级），兜底用 find 覆盖其他任意 CLI 工具
SKILL_DIR=""
for d in ~/.claude/skills/proxy-expert ~/.kimi/skills/proxy-expert; do
  [ -d "$d/references" ] && SKILL_DIR="$d" && break
done
if [ -z "$SKILL_DIR" ]; then
  SKILL_DIR=$(find ~ -maxdepth 6 -type d -name "proxy-expert" 2>/dev/null | \
    while IFS= read -r d; do [ -d "$d/references" ] && echo "$d" && break; done | head -1)
fi
[ -n "$SKILL_DIR" ] && echo "SKILL_DIR=$SKILL_DIR" || echo "ERROR: 未找到 skill 目录，请检查安装路径"
```

将找到的路径记为 `SKILL_DIR`，后续所有 `references/` 文件读取均使用 `$SKILL_DIR/references/`。
如果输出 ERROR，告知用户 skill 未正确安装，并说明对应 CLI 的安装命令。

## 快速参考

- **参考文档**：`$SKILL_DIR/references/server-configs.md`（三种服务端方案配置）、`$SKILL_DIR/references/client-config.md`（客户端 YAML 模板）、`$SKILL_DIR/references/troubleshooting.md`（故障排查）
- **自动化范围**：VPS 服务端全程自动化（SSH 执行）；客户端生成配置文件，GUI 步骤给用户做
- **信息来源**：始终从 `proxy-setup-info.txt` 读取敏感信息，不在对话中让用户粘贴密码
- **⚠️ 每次 SSH 操作前**：必须重新读取 `proxy-setup-info.txt`，确保使用最新信息（用户可能中途改了密码、密钥路径或换了 VPS）

---

## Step 0：开场介绍

以下内容精炼说完，不要啰嗦：

**这套方案的架构：**
```
你的设备 → [VLESS+Reality 加密隧道] → 境外 VPS → (可选)上游 SOCKS5 → 互联网
```

**适用场景：**
- 高速翻墙（实测 940 Mbps，搬瓦工 CN2 GIA 线路）
- AI 服务（Claude、ChatGPT）需要纯净 IP 登录，避免风控 → 需要上游 SOCKS5
- 长期稳定，抗 GFW 主动探测（Reality 协议让 GFW 看到的是访问 apple.com 的正常 HTTPS 流量）

**为什么不用其他方案：**
| 方案 | 问题 |
|---|---|
| 裸 Shadowsocks | 2024+ GFW 能识别流量特征，封端口 5-10 分钟 |
| WireGuard | GFW 精准识别 WG 协议，UDP 出境严重 QoS |
| 裸 SOCKS5 | 跨境必封，亲测无解 |
| **VLESS+Reality** | GFW 探测时看到真实 apple.com 响应，无法区分 ✅ |

说完后问："你有一台境外 VPS 了吗？如果没有，我可以推荐选购；如果有，告诉我系统是什么，我们开始配置。"

---

## Step 1：创建信息模板

在当前工作目录创建 `proxy-setup-info.txt`（内容如下），告诉用户填好后保存，然后告知继续：

```
# ============================
# 搭梯子专家 - 信息配置模板
# 填好所有必填项后保存文件，然后告知 AI 继续
# ============================

# --- VPS 信息（必填）---
VPS_IP=
SSH_PORT=22
SSH_USER=root

# SSH 认证方式：填 "password" 或 "key"
SSH_AUTH=password
# 密码认证时填（key 认证留空）
SSH_PASSWORD=
# 密钥认证时填路径（password 认证留空）
SSH_KEY_PATH=

# --- 上游 SOCKS5（可选）---
# 用途：以纯净 IP 登录 Claude/ChatGPT，避免风控
# 不需要则全部留空
UPSTREAM_IP=
UPSTREAM_PORT=
UPSTREAM_USER=
UPSTREAM_PASS=

# --- 方案选择 ---
# A = VPS 直接出网（最快，不需要上游）
# B = 全流量走上游（所有请求走 SOCKS5，需要填上游）
# C = 混合路由【不推荐，当前该方案存在瑕疵，正在完善中】（AI 站走上游纯净 IP，其他直连高速，需要填上游）
PLAN=

# --- 高级选项（保持默认即可）---
# SNI 伪装域名（推荐 www.apple.com）
SNI_DOMAIN=www.apple.com
```

---

## Step 1.5：VPS 连通质量检测

用户保存 `proxy-setup-info.txt` 后，**立即读取文件**获取 `VPS_IP`，测试本机到 VPS 的网络质量，再决定是否继续。

### 丢包率 + 延迟测试

**Mac/Linux：**
```bash
ping -c 20 {VPS_IP}
```

**Windows（CMD 或 PowerShell）：**
```cmd
ping -n 20 {VPS_IP}
```

### 解读规则

**丢包率：**
- < 5%：✅ 正常，继续
- 5%–10%：⚠️ 有丢包，告知用户体验可能受影响，询问是否继续或更换 VPS
- > 10%：🔴 丢包过高，**强烈建议更换 VPS**，等用户明确表态后再继续

**平均延迟（RTT）：**
- < 100ms：极佳
- 100–200ms：良好
- 200–300ms：可接受，速度会有明显感知
- > 300ms：建议换线路（CN2 GIA 或美西节点更优）

### 用户更换 VPS 时的处理

1. 提示用户更新 `proxy-setup-info.txt` 中的 `VPS_IP` 及相关认证信息，保存后告知继续
2. 用户确认后，**重新读取** `proxy-setup-info.txt`，再次执行本步骤测试
3. 新 VPS 质量达标后，继续 Step 2

---

## Step 2：读取配置，确认方案

**先重新读取** `proxy-setup-info.txt`（即使刚填过），解析所有字段。然后向用户展示即将部署的方案摘要：

- VPS：`{VPS_IP}:{SSH_PORT}`，用户 `{SSH_USER}`，认证方式 `{SSH_AUTH}`
- 方案：A/B/C（说明具体含义）
- 伪装域名：`{SNI_DOMAIN}`
- 上游（如有）：`{UPSTREAM_IP}:{UPSTREAM_PORT}`

如果 PLAN=C 但没有填上游信息，提醒用户方案 C 需要上游，询问是降级到 A 还是先填上游信息。

**等用户明确确认后再进入 Step 3。**

---

## Step 3：处理 SSH 认证

**开始本步骤前，先重新读取 `proxy-setup-info.txt`**，确保使用最新的认证信息（密码/密钥路径/端口可能已被用户修改）。

### 如果 SSH_AUTH=key
检查密钥文件是否存在：
```bash
ls -la {SSH_KEY_PATH}
```
存在则直接进入 Step 4。不存在则提示用户检查路径。

### 如果 SSH_AUTH=password
策略：生成一次性密钥，**全自动**通过密码登录把公钥注入 VPS，用户无需进 VPS 终端手动操作。

1. 生成临时密钥对：
```bash
ssh-keygen -t ed25519 -f ~/.ssh/proxy_expert_ed25519 -N "" -C "proxy-expert-auto"
```

2. 自动注入公钥（三种方式按优先级尝试）：

**方式 A：sshpass（最快，优先）**
```bash
# 检查 sshpass 是否可用
which sshpass || echo "NOT_FOUND"
```
- 如果可用：
```bash
sshpass -p "{SSH_PASSWORD}" ssh-copy-id \
  -i ~/.ssh/proxy_expert_ed25519.pub \
  -p {SSH_PORT} \
  -o StrictHostKeyChecking=no \
  {SSH_USER}@{VPS_IP}
```
- 如果不可用：
  - Mac：`brew install hudochenkov/sshpass/sshpass`（Homebrew 官方已移除，用此 tap）
  - Windows：跳到方式 B

**方式 B：Python paramiko（跨平台，无需额外安装）**
```bash
# 在当前目录创建虚拟环境（已存在则跳过），再安装 paramiko
python3 -m venv .venv 2>/dev/null || true
.venv/bin/pip install paramiko -q 2>/dev/null || .venv/Scripts/pip install paramiko -q
```
然后执行：
```python
# 本地运行此 Python 脚本（Bash 工具直接执行）
# Mac/Linux 用 .venv/bin/python3，Windows 用 .venv/Scripts/python.exe
.venv/bin/python3 - <<'PYEOF'
import paramiko, sys

host = "{VPS_IP}"
port = {SSH_PORT}
user = "{SSH_USER}"
password = "{SSH_PASSWORD}"
pubkey_path = "~/.ssh/proxy_expert_ed25519.pub"

import os
pubkey_path = os.path.expanduser(pubkey_path)
with open(pubkey_path) as f:
    pubkey = f.read().strip()

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port=port, username=user, password=password, timeout=15)

cmd = (
    f"mkdir -p ~/.ssh && chmod 700 ~/.ssh && "
    f"echo '{pubkey}' >> ~/.ssh/authorized_keys && "
    f"chmod 600 ~/.ssh/authorized_keys && "
    f"echo 公钥注入成功"
)
stdin, stdout, stderr = client.exec_command(cmd)
print(stdout.read().decode())
err = stderr.read().decode()
if err:
    print("STDERR:", err, file=sys.stderr)
client.close()
PYEOF
```
看到 "公钥注入成功" 则继续。

3. 验证密钥可用（无论用哪种方式注入，最后都验证一次）：
```bash
ssh -i ~/.ssh/proxy_expert_ed25519 -o StrictHostKeyChecking=no -o ConnectTimeout=10 -p {SSH_PORT} {SSH_USER}@{VPS_IP} "echo 密钥登录成功"
```

看到 "密钥登录成功" 则继续。失败时常见原因：authorized_keys 权限不对（重新用密码登 chmod 600）、VPS 禁用了密码认证（检查 `/etc/ssh/sshd_config` 的 `PasswordAuthentication`）。

> **注意**：整个过程用户不需要打开 VPS 的 Web 终端或自己执行任何命令，全部由本地 AI 自动完成。

之后所有 SSH 命令统一用：
```
SSH_CMD="ssh -i ~/.ssh/proxy_expert_ed25519 -o StrictHostKeyChecking=no -p {SSH_PORT} {SSH_USER}@{VPS_IP}"
```

---

## Step 4：服务端自动化部署

依次执行，每步完成后打印 ✅ 进度。出错立即停下报告，不要强行继续。

所有命令格式：`ssh -i {KEY} -o StrictHostKeyChecking=no -p {PORT} {USER}@{IP} "命令"`

### 4.1 系统更新与基础工具
```bash
apt-get update -y && apt-get upgrade -y
apt-get install -y curl wget nano fail2ban iptables-persistent
```

### 4.2 安装 sing-box（自动获取最新版）
```bash
ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
SB_VER=$(curl -s https://api.github.com/repos/SagerNet/sing-box/releases/latest | grep tag_name | cut -d '"' -f4 | sed 's/v//')
cd /tmp
wget -q "https://github.com/SagerNet/sing-box/releases/download/v${SB_VER}/sing-box-${SB_VER}-linux-${ARCH}.tar.gz"
tar -xzf "sing-box-${SB_VER}-linux-${ARCH}.tar.gz"
cp "sing-box-${SB_VER}-linux-${ARCH}/sing-box" /usr/local/bin/
chmod +x /usr/local/bin/sing-box
sing-box version
```

### 4.3 生成密钥（并保存到本地）
在 VPS 上生成，**立即保存到本地 `.proxy-keys.txt`**（隐藏文件，不会被 git 追踪）：

```bash
# VPS 上生成
KEYPAIR=$(sing-box generate reality-keypair)
UUID=$(sing-box generate uuid)
SHORTID=$(sing-box generate rand --hex 8)
echo "KEYPAIR: $KEYPAIR"
echo "UUID: $UUID"
echo "SHORTID: $SHORTID"
```

解析输出，本地保存：
```
# .proxy-keys.txt（保存在当前工作目录）
VPS_IP={VPS_IP}
UUID={uuid}
PrivateKey={private_key}
PublicKey={public_key}
ShortID={short_id}
SNI={SNI_DOMAIN}
PLAN={PLAN}
```

**PrivateKey 仅服务端用，绝不暴露给用户。**

### 4.4 写服务端配置

读取 `$SKILL_DIR/references/server-configs.md`，根据用户选择的 PLAN（A/B/C）选对应模板，填入真实的密钥和上游信息，通过 SSH heredoc 写入 `/etc/sing-box/config.json`。

写完后执行语法检查：
```bash
sing-box check -c /etc/sing-box/config.json
```
无输出 = 正常，有 error = 立即停下，展示错误给用户。

### 4.5 创建并启动 systemd 服务
```bash
cat > /etc/systemd/system/sing-box.service <<'EOF'
[Unit]
Description=sing-box service
Documentation=https://sing-box.sagernet.org
After=network.target nss-lookup.target

[Service]
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE CAP_NET_RAW
AmbientCapabilities=CAP_NET_ADMIN CAP_NET_BIND_SERVICE CAP_NET_RAW
ExecStart=/usr/local/bin/sing-box -D /var/lib/sing-box -C /etc/sing-box run
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=10s
LimitNOFILE=infinity

[Install]
WantedBy=multi-user.target
EOF

mkdir -p /var/lib/sing-box
systemctl daemon-reload
systemctl enable sing-box
systemctl start sing-box
sleep 3
systemctl status sing-box --no-pager
```

### 4.6 开启 BBR（免费带宽加速）
```bash
modprobe tcp_bbr
echo 'tcp_bbr' >> /etc/modules-load.d/modules.conf
cat > /etc/sysctl.d/99-bbr.conf <<'EOF'
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
EOF
sysctl -p /etc/sysctl.d/99-bbr.conf
```

### 4.7 配置 fail2ban（防 SSH 爆破）
```bash
cat > /etc/fail2ban/jail.local <<'EOF'
[DEFAULT]
bantime  = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
EOF
systemctl restart fail2ban
```

### 4.8 备份配置到 VPS
```bash
tar -czf /root/proxy-backup-$(date +%Y%m%d).tar.gz \
  /etc/sing-box/ /etc/fail2ban/jail.local \
  /etc/sysctl.d/99-bbr.conf /etc/systemd/system/sing-box.service
```

---

## Step 5：生成客户端配置

读取 `$SKILL_DIR/references/client-config.md`，将 `.proxy-keys.txt` 中的值填入模板，在当前目录生成 `clash-verge-config.yaml`。

⚠️ **生成时必须完整包含以下所有直连规则，一条也不能少**（原样保留）：
```yaml
  - IP-CIDR,<VPS_IP>/32,DIRECT,no-resolve    # 必须放 rules 第一位，防止 SSH 回环死锁
  - IP-CIDR,127.0.0.0/8,DIRECT,no-resolve    # 本机回环直连
  - IP-CIDR,192.168.0.0/16,DIRECT,no-resolve # 局域网直连
  - IP-CIDR,10.0.0.0/8,DIRECT,no-resolve     # 内网直连
  - GEOIP,CN,DIRECT                           # 国内 IP 直连
  - DOMAIN-SUFFIX,cn,DIRECT                   # 国内域名直连
  - MATCH,PROXY                               # 其余走代理
```

文件顶部加注释，说明如何导入：
```yaml
# ============================================================
# Clash Verge Rev 导入步骤：
# 1. 打开 Clash Verge → 订阅 → 右上角"新建" → 选 Local
# 2. 填写名称（如：我的节点），点编辑图标
# 3. 粘贴本文件全部内容，Ctrl+S / Cmd+S 保存
# 4. 订阅页面右键刚创建的配置 → 启用
# 5. 代理页面：在 PROXY 组里选中节点名
# 6. 主界面：打开"系统代理"开关
# 注意：修改配置后需完全退出 Clash Verge 再重新打开
# ============================================================
```

然后手动引导用户完成 Clash Verge GUI 步骤（因为是图形界面，无法自动化）：

**Mac 用户：** 按注释里的步骤操作，`Cmd+S` 保存，完成后告知继续。
**Windows 用户：** 步骤相同，`Ctrl+S` 保存；首次建议以管理员身份运行 Clash Verge。

---

## Step 6：自动化验收测试

用户告知 Clash Verge 已配置并开启系统代理后，分两组执行测试。

### 第一组：VPS 直连测试（不经过 Clash）

以下测试直连 VPS，验证服务端配置是否正常，与 Clash 是否开启无关。

#### 测试 1：443 端口可达
- **Mac/Linux：** `nc -z -w 5 {VPS_IP} 443 && echo 端口通`
- **Windows（PowerShell）：**
```powershell
Test-NetConnection -ComputerName {VPS_IP} -Port 443
# TcpTestSucceeded : True = 通
```

#### 测试 2：Reality 伪装
```bash
# Mac/Linux（关闭系统代理后执行）
curl -sI --resolve "www.apple.com:443:{VPS_IP}" https://www.apple.com/ -k 2>&1 | head -5
```
Windows 用 `curl.exe`（加 `.exe` 后缀）。

期望：返回 `HTTP/2 200` 和 `server: Apple`。

#### 测试 3：服务端状态
```bash
ssh -i {KEY} ... "systemctl is-active sing-box"
```
期望：`active`

#### 测试 4：日志检查
```bash
ssh -i {KEY} ... "tail -20 /var/log/sing-box/sing-box.log"
```
期望：无 ERROR；可见 `REALITY: processed invalid connection`（这是 GFW 探测被拦截，属正常现象）

---

### 第二组：代理连通测试（需要 Clash 系统代理已开启）

确认 Clash 系统代理开启后，通过本地代理端口测试各目标站点的真实连通性。

#### 测试 5：Google 连通
```bash
# Mac/Linux
curl -x http://127.0.0.1:7890 -sI --max-time 15 https://www.google.com 2>&1 | head -3
```
```powershell
# Windows
curl.exe -x http://127.0.0.1:7890 -sI --max-time 15 https://www.google.com
```
期望：收到任意 HTTP 响应（说明流量已经过代理到达目标服务器）。
- 2xx/3xx：✅ 完全正常
- 4xx（如 403 Cloudflare challenge）：⚠️ 流量通，但目标站点对当前 IP 触发了 challenge，提示用户（见下方说明）
- 超时 / curl 报错（exit code 非 0）：❌ 代理未通，需排查

#### 测试 6：Claude.ai 连通
```bash
# Mac/Linux
curl -x http://127.0.0.1:7890 -sI --max-time 15 https://claude.ai 2>&1 | head -3
```
```powershell
# Windows
curl.exe -x http://127.0.0.1:7890 -sI --max-time 15 https://claude.ai
```
期望：同上，收到任意 HTTP 响应即为流量通。4xx 时提示 IP 信誉 challenge。

#### 测试 7：ChatGPT 连通
```bash
# Mac/Linux
curl -x http://127.0.0.1:7890 -sI --max-time 15 https://chat.openai.com 2>&1 | head -3
```
```powershell
# Windows
curl.exe -x http://127.0.0.1:7890 -sI --max-time 15 https://chat.openai.com
```
期望：同上，收到任意 HTTP 响应即为流量通。4xx 时提示 IP 信誉 challenge。

---

### 验收标准总表

判断原则：**代理流量通 = 验收通过；是否遇到 challenge 是 IP 信誉问题，不是代理故障。**

| 测试项 | 通过条件 | 备注 |
|---|---|---|
| 443 端口可达 | 端口通 / TcpTestSucceeded=True | |
| Reality 伪装 | HTTP/2 200 + server: Apple | |
| sing-box 服务 | active | |
| 日志无 ERROR | 无 ERROR 行 | |
| Google 连通 | 收到任意 HTTP 响应 | 4xx 时提示 challenge ⚠️ |
| Claude.ai 连通 | 收到任意 HTTP 响应 | 4xx 时提示 challenge ⚠️ |
| ChatGPT 连通 | 收到任意 HTTP 响应 | 4xx 时提示 challenge ⚠️ |

> ⚠️ **关于 challenge 的说明（需在验收报告中注明）：**
> 如果上述测试返回 4xx（如 403），说明代理流量本身是通的，但目标站点对当前出口 IP 触发了安全验证（Cloudflare challenge、Google 人机验证等）。这是 IP 信誉问题，不影响验收通过。建议用浏览器实际访问确认是否能正常使用；如使用 AI 服务时频繁遇到 challenge，可考虑启用上游 SOCKS5 切换为方案 C。
>
> 此外，Claude / ChatGPT 的流式输出（SSE 长连接）经代理时，偶发连接中断或输出停止。这是 TCP 长连接经代理的正常特性，对功能影响有限，但体验略有下降。如频繁发生，检查本地→VPS 丢包率，或考虑更换 VPS 服务商以改善线路质量。

---

## Step 7：用户最终验收 + 生成验收报告

提示用户：

1. 确认 Clash Verge 系统代理已开启
2. 用浏览器访问 https://www.google.com（或 https://www.youtube.com）
3. 用浏览器访问 https://www.fast.com 测速（纯 TCP，结果准确）
4. 如果配置了上游：访问 https://claude.ai 确认 AI 服务可用

询问："以上验证都通过了吗？"

**通过后，立即在当前工作目录生成验收报告 `proxy-acceptance-report.md`：**

```markdown
# 梯子搭建验收报告

**生成时间：** {YYYY-MM-DD HH:MM}
**VPS IP：** {VPS_IP}
**SSH 端口：** {SSH_PORT}
**部署方案：** {PLAN}（A=VPS直连 / B=全走上游 / C=混合路由）
**SNI 伪装域名：** {SNI_DOMAIN}

## 初次部署验收结果

| 测试项 | 结果 | 备注 |
|---|---|---|
| VPS 网络质量 | {丢包率}% 丢包 / 平均延迟 {RTT}ms | Step 1.5 测试结果 |
| 443 端口可达 | ✅ / ❌ | |
| Reality 伪装 | ✅ HTTP/2 200 + server: Apple / ❌ | |
| sing-box 服务 | ✅ active / ❌ | |
| 日志无 ERROR | ✅ / ❌ | |
| Google 连通 | ✅ 流量通({状态码}) / ⚠️ challenge({状态码}) / ❌ 超时 | |
| Claude.ai 连通 | ✅ 流量通({状态码}) / ⚠️ challenge({状态码}) / ❌ 超时 | |
| ChatGPT 连通 | ✅ 流量通({状态码}) / ⚠️ challenge({状态码}) / ❌ 超时 | |

## 已知风险说明

- **流式输出偶发中断**：Claude / ChatGPT 的 SSE 流式输出经代理时，偶发断流或停止，属 TCP 长连接经代理的正常特性，对功能影响有限。如频繁发生，排查本地→VPS 丢包率，或更换 VPS 服务商。
- **AI 服务 IP 风控**：数据中心 IP 可能触发 Claude / GPT 的 IP 信誉检测（弹验证码或拒绝登录）。方案 C 已通过上游 SOCKS5 缓解此风险。

## 问题记录

---

（后续排障记录追加至此）
```

告知用户：
- 验收报告已保存至 `proxy-acceptance-report.md`，可长期保存，无敏感信息
- 密钥文件位置：`.proxy-keys.txt`（妥善保管，不要泄露）
- 维护建议：每月 `apt update && apt upgrade -y`；每季度检查 sing-box 版本
- 如果 VPS 换了：新 VPS 安装 sing-box，还原配置，Clash Verge 改 server IP 即可

**未通过：** 读取 `$SKILL_DIR/references/troubleshooting.md`，按层级排查。常见路径：
1. Clash 系统代理没开？→ 开启
2. 节点没选中？→ 代理页面选中节点
3. `nc` 端口不通？→ SSH 看 sing-box 状态
4. sing-box 挂了？→ `systemctl restart sing-box`，看日志
5. Reality 伪装测试失败？→ 检查 SNI 域名、密钥是否匹配

---

## Step 8：故障排查模式

**当用户带着梯子故障来询问时**（不是全新部署），执行以下流程：

### 8.1 先读验收报告

```bash
cat proxy-acceptance-report.md
```

如果文件存在，从中了解：
- 初始搭建的 VPS 信息和方案
- 历史验收测试结果（判断是否曾经通过）
- 已有的问题记录（避免重复排查已知问题）

如果文件不存在，直接询问用户 VPS IP 和当前症状。

### 8.2 重新读取配置

```bash
cat proxy-setup-info.txt
```

获取最新的 VPS_IP、SSH_PORT、SSH_USER 等信息。

### 8.3 按 troubleshooting.md 排查

读取 `$SKILL_DIR/references/troubleshooting.md`，按症状匹配对应排查流程。

### 8.4 问题解决后，追加记录

在 `proxy-acceptance-report.md` 文件末尾的"问题记录"区追加：

```markdown
### {YYYY-MM-DD} - {问题简述}

**现象：** {用户描述的症状}
**根因：** {排查后确认的根本原因}
**解决方案：** {具体操作步骤}
```

同时，如果该问题是新出现的故障模式（未在 `troubleshooting.md` 中覆盖），或解决方案比现有记录更完整，**将问题和解决方案同步更新到 `$SKILL_DIR/references/troubleshooting.md`**：
- 若属于已有状况的新变体，追加到对应状况下作为子步骤或补充说明
- 若属于全新故障模式，新增一个状况小节（按现有编号顺序），包含症状、原因和解决步骤
- 同步更新"常见误解和坑"表格（如适用）

---

## 关键注意事项

- **每次 SSH 前重读配置：** 每次执行 SSH 操作前，先重新读取 `proxy-setup-info.txt`，防止用户中途修改密码、密钥或 VPS 信息而沿用旧值
- **Python 脚本依赖隔离：** 凡需在本地运行 Python 脚本（如 paramiko 注入），必须在当前工作目录创建并使用虚拟环境（`python3 -m venv .venv`），通过 `.venv/bin/pip` 安装依赖，通过 `.venv/bin/python3` 执行脚本，禁止使用全局 pip 或 `--user` 安装
- **平台检测：** 从系统环境 `Platform:` 字段判断 `darwin`/`linux`/`win32`，影响 `curl` vs `curl.exe`、`nc` vs `Test-NetConnection`、`ping -c` vs `ping -n` 等命令
- **Windows SSH：** Win 10+ 内置 OpenSSH，Bash 工具可直接调用 `ssh`
- **密钥安全：** PrivateKey 只写服务端 config，绝不显示给用户；PublicKey 给客户端
- **防死循环：** Clash Verge YAML 的 rules 里第一条必须是 `IP-CIDR,{VPS_IP}/32,DIRECT,no-resolve`
- **UDP 关闭：** 客户端配置 `udp: false`，避免 Cloudflare speedtest 误报丢包

---

## 文件清单（部署完成后）

| 文件 | 用途 |
|---|---|
| `proxy-setup-info.txt` | 用户填写的配置信息（含敏感信息，不要上传 git）|
| `.proxy-keys.txt` | 自动保存的密钥（隐藏文件，不要泄露）|
| `clash-verge-config.yaml` | 客户端配置（导入 Clash Verge 用）|
| `proxy-acceptance-report.md` | 验收报告和问题记录（无敏感信息，可长期保存）|
