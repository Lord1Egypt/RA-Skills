---
name: remote-browser-deploy
author: 王教成 Wang Jiaocheng (波动几何)
description: 一键部署远程可视化浏览器：Linux（云服务器/NAS/本地）noVNC + Chromium + CDP 三合一，Windows 本机 Edge/Chrome CDP 一键接管。技术栈：noVNC（Web VNC）+ Chromium（浏览器）+ CDP（Chrome DevTools Protocol）。解决 Headless 浏览器自动化中登录、验证码、滑块等需要人工介入的场景。
---

# 远程可视化浏览器部署

## 技术栈

| 组件 | 作用 | 端口 |
|------|------|------|
| **noVNC** | Web VNC 客户端，用户通过浏览器访问远程桌面 | 6080/tcp |
| **Chromium** | 开源浏览器，运行在虚拟显示器上 | - |
| **CDP** | Chrome DevTools Protocol，Agent 通过 WebSocket 控制浏览器 | 9223/tcp |
| **Xvfb** | 虚拟显示器，让 Chromium 在无图形界面的服务器上运行 | :99 |
| **x11vnc** | VNC 服务器，将虚拟显示器画面转发给 noVNC | 5900/tcp |
| **websockify** | WebSocket 代理，连接 noVNC 和 x11vnc | - |

**数据流**：
- Linux：Xvfb → 虚拟显示器 :99 → Chromium (CDP 9223) → x11vnc → noVNC/websockify → 用户浏览器
- Windows：Edge/Chrome (CDP 9223) + 本机屏幕 → Agent 控制，无需额外组件

## 适用场景

**典型场景：**
- 登录类后台：抖音创作者中心、小红书创作者平台、微博、公众号后台等
- 风控验证：滑块验证、扫码登录、短信验证、图形验证码、设备验证等
- 内容发布：自动打开发布页、填写标题/正文/标签/封面，并让用户处理最后的人工验证
- 网页调试：需要用户和 AI 同时看到同一个浏览器画面，方便排查页面状态

**不适合场景：**
- 纯 API 调用任务，不需要浏览器画面
- 对安全要求极高、不能暴露任何远程桌面入口的生产环境
- Linux 模式：无法开放 `6080/tcp` 或无法提供 root/sudo 权限的服务器（Windows 模式无此限制）

**最终效果：**
- Linux 模式：用户访问 `http://<服务器IP>:6080/vnc.html`，Agent 控制 `http://127.0.0.1:9223/json`
- Windows 模式：用户在本机屏幕直接看到 Edge/Chrome 浏览器，Agent 控制 `http://127.0.0.1:9223/json`

> 💡 统一使用 **9223** 端口，避免与 AI Agent 自带的 Playwright/Chromium 抢占 **9222** 端口。

## 重要原则

> ⚠️ **最高优先级规则，不可违反：**

1. **必须使用本技能部署的浏览器**：部署完成后，用户让 AI Agent「打开浏览器 / 看网页 / 截图 / 点击 / 登录」等任何浏览器操作，**默认必须使用本技能部署的 CDP 浏览器**（`127.0.0.1:9223`）。**禁止使用 Agent 自带的内置 headless 浏览器或临时拉起其他实例**，否则用户和 Agent 看到的画面不同频。

2. **严禁添加 headless 参数**：**严禁给 Chromium 添加 `--headless` 或 `--headless=new` 启动参数**，否则 noVNC 画面无法正常显示。

3. **系统检测是强制步骤**：Agent 拿到 `ENV_TYPE` 后，**必须严格按以下规则发送对应 IP 地址，不得自行判断或偷懒**：
   - `CLOUD`（云服务器）→ 必须用 `curl -4 -s https://ifconfig.me` 获取公网 IP，**严禁**发内网地址
   - `NAS`（NAS 设备）→ 用 `hostname -I` 取内网 IP，同时提醒用户在 NAS 控制面板开放 6080 端口
   - `LOCAL`（本地 Linux）→ 用 `hostname -I` 取内网 IP，同时提醒用户放行系统防火墙 6080 端口

4. **发送顺序铁律**：必须先把 noVNC 地址、访问密码、浏览器状态、开机自启状态、端口提醒和验证码处理说明发送给用户，**再把截图作为最后一步发送**。截图失败不得阻塞核心信息。

---

## 部署流程

### 第一步：系统检测

```bash
# 检测操作系统
uname -s 2>/dev/null | grep -qi linux && echo "LINUX" || true

# 如果是 Linux，再细分环境类型（云服务器 / NAS / 本地 Linux）
if [ "$(uname -s)" = "Linux" ]; then
  # 检测是否云服务器（腾讯云/阿里云/AWS metadata）
  if curl -s --connect-timeout 2 http://metadata.tencentyun.com/latest/meta-data/ 2>/dev/null | grep -q .; then
    echo "ENV_TYPE=CLOUD"
  elif curl -s --connect-timeout 2 http://100.100.100.200/latest/meta-data/ 2>/dev/null | grep -q .; then
    echo "ENV_TYPE=CLOUD"
  elif curl -s --connect-timeout 2 http://169.254.169.254/latest/meta-data/ 2>/dev/null | grep -q .; then
    echo "ENV_TYPE=CLOUD"
  # 检测是否 NAS（群晖 Synology / QNAP 威联通）
  elif [ -f /etc/synoinfo.conf ]; then
    echo "ENV_TYPE=NAS"
  elif [ -f /etc/platform.conf ] || [ -f /etc/version ]; then
    echo "ENV_TYPE=NAS"
  else
    echo "ENV_TYPE=LOCAL"
  fi
fi
```

**分流逻辑**：
- **检测到 Linux（CLOUD / NAS / LOCAL）** → 继续执行「Linux 部署流程」
- **检测到 Windows** → 跳转到「Windows 部署流程」

---

### Linux 部署流程

#### 1. 配置预检

```bash
# 检查系统配置
cat /etc/os-release | head -3
uname -m
nproc
free -h
df -h /

# 权限预检
if [ "$(id -u)" = "0" ]; then
  echo "PERMISSION_OK: 当前是 root 用户"
elif command -v sudo >/dev/null 2>&1 && sudo -n true 2>/dev/null; then
  echo "PERMISSION_OK: 当前用户可免密 sudo"
else
  echo "PERMISSION_DENIED: 当前用户不是 root，且无法免密 sudo。"
fi
```

**权限不足处理**：
```bash
# 首选：引导用户配置免密 sudo
echo "$(whoami) ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/hermes-deploy
# 部署完成后执行 sudo rm /etc/sudoers.d/hermes-deploy 收回权限
```

#### 2. 安装依赖

```bash
# 系统依赖
apt update && apt upgrade -y
apt install -y xvfb x11vnc git python3-pip curl wget ca-certificates

# 安装 Chromium/Chrome（deb 版优先，失败后自动切换）
. /etc/os-release
if [ "$ID" = "debian" ]; then
  apt install -y chromium || apt install -y chromium-browser || true
elif [ "$ID" = "ubuntu" ]; then
  if wget -O /tmp/google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb; then
    apt install -y /tmp/google-chrome-stable_current_amd64.deb || true
  fi
  if command -v google-chrome-stable >/dev/null 2>&1; then
    ln -sf /usr/bin/google-chrome-stable /usr/local/bin/chromium
  else
    apt install -y chromium || apt install -y chromium-browser || true
  fi
else
  apt install -y chromium || apt install -y chromium-browser || true
fi

# 验证浏览器安装
CHROME_BIN=$(command -v chromium || command -v chromium-browser || command -v google-chrome-stable || true)
if [ -z "$CHROME_BIN" ]; then
  echo "ERROR: 未找到 Chromium/Chrome 可执行文件"
  exit 1
fi
echo "浏览器路径：$CHROME_BIN"

# 安装 noVNC 和 websockify
cd /opt
if [ ! -d /opt/noVNC ]; then
  git clone https://github.com/novnc/noVNC.git
fi
pip3 install websockify --break-system-packages

# 如果 noVNC master 版本出现 ES module 报错，固定到稳定版
cd /opt/noVNC
git fetch --tags
git checkout v1.6.0
```

#### 3. 开放端口

根据环境类型（`$ENV_TYPE`）选择对应的防火墙指令：

**CLOUD（云服务器）：**
```bash
ufw allow 6080/tcp || true
ufw reload || true
# 云厂商安全组也要放行 6080/tcp
```

**NAS：**
```bash
# NAS 部署：内网直接访问，无需操作防火墙
# 如需外网访问：在路由器上设置端口转发 6080 TCP → <NAS_IP>
echo "NAS 环境：noVNC 通过内网地址访问。如需外网访问，请在路由器做端口转发 6080。"
```

**LOCAL（本机 Linux）：**
```bash
ufw allow 6080/tcp || true
ufw reload || true
# 如需外网访问：在路由器上设置端口转发 6080 TCP → <本机IP>
```

#### 4. 创建启动脚本与密码

```bash
# 生成 noVNC 访问密码（8 位随机字母+数字）
NOVNC_PASS=$(tr -dc 'A-Za-z0-9' </dev/urandom | head -c 8)
echo -n "$NOVNC_PASS" > /root/.novnc_password
chmod 600 /root/.novnc_password
x11vnc -storepasswd "$NOVNC_PASS" /root/.vncpasswd
chmod 600 /root/.vncpasswd
echo "noVNC 访问密码已生成：$NOVNC_PASS"

# 写入启动脚本
cat > /root/start-remote-browser.sh <<'SCRIPT_END'
#!/bin/bash
set -e

pkill -9 -f x11vnc 2>/dev/null || true
pkill -9 -f Xvfb 2>/dev/null || true
pkill -9 -f websockify 2>/dev/null || true
pkill -9 -f 'chromium.*remote-debugging-port=9223' 2>/dev/null || true
sleep 2

echo "[1/4] 启动虚拟显示器..."
Xvfb :99 -screen 0 1920x1080x24 &
sleep 1
export DISPLAY=:99

echo "[2/4] 启动 Chromium (CDP:9223)..."
CHROME_BIN=$(command -v chromium || command -v chromium-browser || command -v google-chrome-stable || true)
if [ -z "$CHROME_BIN" ]; then
  echo "ERROR: 未找到 Chromium/Chrome 可执行文件"
  exit 1
fi
# ⚠️ 严禁添加 --headless 或 --headless=new，否则 noVNC 画面无法显示。
"$CHROME_BIN" \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --remote-debugging-port=9223 \
  --remote-debugging-address=127.0.0.1 \
  --remote-allow-origins='*' \
  --window-size=1920,1080 \
  --start-maximized \
  --no-first-run \
  --no-default-browser-check \
  --user-data-dir=/root/.chromium-remote \
  --restore-last-session=false \
  https://www.baidu.com/ &
sleep 3

echo "[3/4] 启动 x11vnc..."
x11vnc -display :99 -forever -rfbauth /root/.vncpasswd -quiet -listen 127.0.0.1 &
sleep 1

echo "[4/4] 启动 noVNC (端口:6080)..."
websockify --web /opt/noVNC 6080 127.0.0.1:5900 &
sleep 1

IP=$(hostname -I | awk '{print $1}')
echo ""
echo "========================================"
echo "  ✅ 远程浏览器已就绪"
echo "  用户访问: http://${IP}:6080/vnc.html"
echo "  CDP: http://127.0.0.1:9223/json（仅供本机 Agent）"
echo "========================================"
SCRIPT_END

chmod +x /root/start-remote-browser.sh
```

#### 5. 启动远程浏览器

```bash
bash /root/start-remote-browser.sh
```

启动完成后，验证 CDP 连通性：
```bash
curl -s http://127.0.0.1:9223/json/version
curl -s http://127.0.0.1:9223/json
```

**⚠️ 部署到这一步时，手动脚本启动的 Chromium 还在后台运行。接下来配置 systemd 自启前，必须先杀掉手动进程，避免两个 Chromium 实例抢同一个 `--user-data-dir`，导致标签页不断堆叠。**

```bash
pkill -9 -f "(chromium|chrome).*remote-debugging-port=9223" 2>/dev/null || true
sleep 2
```

#### 6. 配置开机自启（systemd）

```bash
# 1) Xvfb 虚拟显示器
cat > /etc/systemd/system/xvfb.service <<'EOF'
[Unit]
Description=Xvfb virtual display :99
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/Xvfb :99 -screen 0 1920x1080x24 -ac
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# 2) x11vnc（必须使用 -rfbauth 走密码模式）
cat > /etc/systemd/system/x11vnc.service <<'EOF'
[Unit]
Description=x11vnc server on :99 (password protected)
After=xvfb.service
Requires=xvfb.service

[Service]
Type=simple
Environment=DISPLAY=:99
ExecStart=/usr/bin/x11vnc -display :99 -forever -shared -rfbauth /root/.vncpasswd -rfbport 5900 -quiet
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# 3) noVNC websockify
cat > /etc/systemd/system/novnc.service <<'EOF'
[Unit]
Description=noVNC websockify on 6080
After=x11vnc.service
Requires=x11vnc.service

[Service]
Type=simple
ExecStart=/usr/local/bin/websockify --web=/opt/noVNC 6080 localhost:5900
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# 4) Chromium + CDP（自动找可用 Chromium/Chrome 二进制）
CHROME_BIN=$(command -v chromium || command -v chromium-browser || command -v google-chrome-stable)
cat > /etc/systemd/system/chromium-remote.service <<EOF
[Unit]
Description=Chromium with CDP on :9223, display :99
After=xvfb.service
Requires=xvfb.service
StartLimitBurst=3
StartLimitInterval=120

[Service]
Type=simple
Environment=DISPLAY=:99
# 启动前杀掉残留的 chromium/chrome 进程，避免 user-data-dir 冲突导致标签页堆叠
ExecStartPre=/usr/bin/pkill -9 -f "(chromium|chrome).*remote-debugging-port=9223" || true
ExecStartPre=/bin/sleep 2
# ⚠️ 严禁添加 --headless 或 --headless=new，否则 noVNC 画面无法显示。
ExecStart=${CHROME_BIN} --no-sandbox --disable-gpu --disable-dev-shm-usage --disable-session-crashed-bubble --restore-last-session=false --remote-debugging-port=9223 --remote-debugging-address=127.0.0.1 --remote-allow-origins=* --user-data-dir=/root/.chromium-remote --no-first-run --no-default-browser-check --window-size=1920,1080 --start-maximized https://www.baidu.com/
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now xvfb.service x11vnc.service novnc.service chromium-remote.service
```

验证（应全部 `active`）：
```bash
systemctl is-active xvfb x11vnc novnc chromium-remote
ss -tlnp | grep -E ':6080|:5900|:9223'
```

#### 7. 收尾

**第一步：打开百度确认**
```bash
python3 - <<'PY'
import json, time, urllib.request
import websocket

tabs = json.load(urllib.request.urlopen('http://127.0.0.1:9223/json'))
page = next(t for t in tabs if t.get('type') == 'page')
ws = websocket.create_connection(
    page['webSocketDebuggerUrl'],
    header=['Origin: http://127.0.0.1:9223'],
    timeout=20,
)

msg_id = 0
def call(method, params=None):
    global msg_id
    msg_id += 1
    ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get('id') == msg_id:
            return msg

call('Page.enable')
call('Page.navigate', {'url': 'https://www.baidu.com/'})
time.sleep(3)
print("百度页面已打开")
ws.close()
PY
```

**第二步：发送核心完成信息**

获取 noVNC 地址和密码：
```bash
# 根据环境类型选择 IP
if [ "$ENV_TYPE" = "CLOUD" ]; then
  PUBLIC_IP=$(curl -4 -s https://ifconfig.me 2>/dev/null || curl -4 -s https://api.ipify.org 2>/dev/null || true)
  if [ -n "$PUBLIC_IP" ]; then
    NOVNC_URL="http://${PUBLIC_IP}:6080/vnc.html"
  else
    LOCAL_IP=$(hostname -I | awk '{print $1}')
    NOVNC_URL="http://${LOCAL_IP}:6080/vnc.html"
  fi
else
  LOCAL_IP=$(hostname -I | awk '{print $1}')
  NOVNC_URL="http://${LOCAL_IP}:6080/vnc.html"
fi
echo "$NOVNC_URL"
cat /root/.novnc_password
```

**回复模板（根据环境类型选择）**：

**CLOUD（云服务器）：**
```text
远程 Chromium 浏览器已启动：

- noVNC 地址：http://<公网IP>:6080/vnc.html
- noVNC 访问密码：<读取 /root/.novnc_password>
- 浏览器状态：已自动打开百度页面，截图将作为最后一步补充确认发送
- 开机自启：已配置 systemd，重启后自动拉起
- CDP 地址：仅供 Agent 本机控制，不建议公开
- 请确认云服务器安全组已放行 6080/tcp
- 如果遇到登录、验证码、滑块，请在 noVNC 页面手动完成，完成后告诉我继续。
```

**NAS：**
```text
远程 Chromium 浏览器已启动：

- noVNC 地址：http://<内网IP>:6080/vnc.html
- noVNC 访问密码：<读取 /root/.novnc_password>
- 浏览器状态：已自动打开百度页面，截图将作为最后一步补充确认发送
- 开机自启：已配置 systemd，重启后自动拉起
- CDP 地址：仅供 Agent 本机控制，不建议公开
- 🌐 这是 NAS 局域网地址，请在 NAS 控制面板放行 6080/tcp；通过路由器访问需设置端口转发
- 如果遇到登录、验证码、滑块，请在 noVNC 页面手动完成，完成后告诉我继续。
```

**LOCAL（本机 Linux）：**
```text
远程 Chromium 浏览器已启动：

- noVNC 地址：http://<内网IP>:6080/vnc.html
- noVNC 访问密码：<读取 /root/.novnc_password>
- 浏览器状态：已自动打开百度页面，截图将作为最后一步补充确认发送
- 开机自启：已配置 systemd，重启后自动拉起
- CDP 地址：仅供 Agent 本机控制，不建议公开
- 🌐 这是本机局域网地址，请确保防火墙已放行 6080/tcp
- 如果遇到登录、验证码、滑块，请在 noVNC 页面手动完成，完成后告诉我继续。
```

**🔴 环境误判禁令（最高优先级）：**
- ❌ 对 `NAS`/`LOCAL` 用户**严禁**提「云安全组」「云服务器」「腾讯云」「阿里云」
- ❌ `NAS`/`LOCAL` 环境**严禁**发送公网 IP 的 noVNC 链接（公网 IP 不属于用户，打不开）
- ❌ `CLOUD` 环境**严禁**发送内网 IP 地址给用户
- ❌ **严禁**跳过环境检测步骤直接按云服务器假设来回复

**第三步：截图并发送**

> ⚠️ **铁律：截图必须在核心完成信息发送之后执行和发送。**

**Linux 模式截图：**
```bash
DISPLAY=:99 import -window root /tmp/remote-browser.png
```

**截图发送方式（根据当前平台选择）：**

- **QQ/QQbot 通道**：
  ```bash
  mkdir -p ~/.openclaw/media/qqbot
  cp /tmp/remote-browser.png ~/.openclaw/media/qqbot/remote-browser.png
  ```
  回复中输出：`<qqmedia>/root/.openclaw/media/qqbot/remote-browser.png</qqmedia>`

- **其他通道（Telegram / Discord / 邮件 / 终端 / Web UI 等）**：
  ```text
  MEDIA:/tmp/remote-browser.png
  ```

---

### Windows 部署流程

> Windows 模式下无需安装任何依赖，直接利用系统自带的 Edge 或 Chrome 浏览器。

#### 1. 启动浏览器

**Agent 必须优先自动尝试启动浏览器**，失败后才让用户手动执行。

```powershell
# 优先尝试 Edge
start msedge --remote-debugging-port=9223 --remote-allow-origins=*
```

如果 Edge 不可用，尝试 Chrome：
```powershell
start chrome --remote-debugging-port=9223 --remote-allow-origins=*
```

如果两个命令都执行失败，才告诉用户手动执行：
```text
请以管理员身份打开 PowerShell 或 CMD，执行以下命令：

Edge：
start msedge --remote-debugging-port=9223 --remote-allow-origins=*

或 Chrome：
start chrome --remote-debugging-port=9223 --remote-allow-origins=*
```

#### 2. 验证 CDP 连通性

```bash
curl -s http://127.0.0.1:9223/json/version
```

#### 3. 截图当前页面

**Windows 模式不需要额外导航到百度页面**，直接截取浏览器当前画面即可。

```bash
# 获取当前页面
curl -s http://127.0.0.1:9223/json

# 通过 CDP 截取页面截图，保存为 PNG
python3 - <<'PY'
import json, base64, urllib.request
tabs = json.load(urllib.request.urlopen('http://127.0.0.1:9223/json'))
page = next(t for t in tabs if t.get('type') == 'page')
import websocket
ws = websocket.create_connection(page['webSocketDebuggerUrl'], header=['Origin: http://127.0.0.1:9223'], timeout=20)
msg_id = 0
def call(method, params=None):
    global msg_id
    msg_id += 1
    ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get('id') == msg_id:
            return msg
call('Page.enable')
res = call('Page.captureScreenshot', {'format': 'png'})
with open('/tmp/browser_screenshot.png', 'wb') as f:
    f.write(base64.b64decode(res['result']['data']))
print('截图已保存: /tmp/browser_screenshot.png')
ws.close()
PY
```

#### 4. 发送完成信息

```text
✅ 浏览器已完全由 AI Agent 控制。

- 浏览器：Edge/Chrome（CDP 端口 9223）
- 你可以在屏幕上看到所有操作，随时手动接管
- 请勿关闭这个浏览器窗口
- 如果遇到登录、验证码、滑块，你直接操作即可，完成后告诉我继续
```

Windows 模式也必须先发送上面的接管完成信息，再把截图作为最后一步发送。截图失败不得影响接管完成信息。

---

## 验证清单

### Linux 模式验证

```bash
ss -tlnp | grep -E '6080|5900|9223'
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:6080/vnc.html
curl -s http://127.0.0.1:9223/json/version
```

应满足：
- `6080` 正在监听
- `5900` 正在监听本机 VNC
- `9223` 正在监听 CDP
- `vnc.html` 返回 `200`
- 用户能在浏览器看到远程 Chromium 画面

### Windows 模式验证

```bash
curl -s http://127.0.0.1:9223/json/version
curl -s http://127.0.0.1:9223/json
```

应满足：
- `9223` 正在监听 CDP
- `json/version` 返回浏览器信息
- `json` 返回至少一个 page 类型的标签
- 用户本机屏幕上能看到 Edge/Chrome 浏览器窗口

---

## 常见问题

### Linux 模式

**1. noVNC 打开空白或连不上**
```bash
ps -ef | grep -E 'Xvfb|chromium|x11vnc|websockify' | grep -v grep
ss -tlnp | grep -E '6080|5900|9223'
bash /root/start-remote-browser.sh
```

**2. 外网打不开 6080**
- 云服务器安全组是否放行 `6080/tcp`
- 系统防火墙是否放行 `6080/tcp`
- `websockify` 是否监听 `0.0.0.0:6080`

**3. CDP WebSocket 403**
Chromium 启动参数需要包含 `--remote-allow-origins='*'`，Python websocket 连接时带 Origin：
```python
websocket.create_connection(ws_url, header=['Origin: http://127.0.0.1:9223'])
```

**4. 浏览器画面卡住**
```bash
pkill -9 -f chromium || true
pkill -9 -f Xvfb || true
pkill -9 -f x11vnc || true
pkill -9 -f websockify || true
bash /root/start-remote-browser.sh
```

**5. noVNC 报前端 JS 错误**
固定稳定版本：
```bash
cd /opt/noVNC
git fetch --tags
git checkout v1.6.0
bash /root/start-remote-browser.sh
```

### Windows 模式

**6. Edge/Chrome 无法以 CDP 模式启动**
浏览器可能已经在运行中。需要先关闭所有 Edge/Chrome 窗口：
```powershell
taskkill /F /IM msedge.exe
taskkill /F /IM chrome.exe
start msedge --remote-debugging-port=9223 --remote-allow-origins=*
```

**7. CDP 端口 9223 被占用**
```powershell
netstat -ano | findstr :9223
taskkill /F /PID <PID>
```

**8. CDP WebSocket 403 / 连接拒绝**
确认启动参数包含 `--remote-allow-origins=*`。如果仍然 403，连接时带 Origin header：
```python
websocket.create_connection(ws_url, header=['Origin: http://127.0.0.1:9223'])
```

---

## CDP 控制代码（参考）

使用 Python 控制已启动的 Chromium：

```bash
python3 - <<'PY'
import json, time, urllib.request
import websocket

url = 'https://example.com'
tabs = json.load(urllib.request.urlopen('http://127.0.0.1:9223/json'))
page = next(t for t in tabs if t.get('type') == 'page')
ws = websocket.create_connection(
    page['webSocketDebuggerUrl'],
    header=['Origin: http://127.0.0.1:9223'],
    timeout=20,
)

msg_id = 0
def call(method, params=None):
    global msg_id
    msg_id += 1
    ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get('id') == msg_id:
            return msg

call('Page.enable')
call('Runtime.enable')
call('Page.navigate', {'url': url})
time.sleep(3)
res = call('Runtime.evaluate', {
    'expression': '({title: document.title, url: location.href})',
    'returnByValue': True,
})
print(json.dumps(res['result']['result']['value'], ensure_ascii=False, indent=2))
ws.close()
PY
```

如果缺少 websocket 包：
```bash
pip3 install websocket-client --break-system-packages
```
