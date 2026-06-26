---
name: zz-chat
description: 爪爪/钳钳 — 手机直连 OpenClaw 聊天。触发词：钳钳、爪爪、钱钱、龙虾、聊天机器人、创建爪爪、安装钳钳、打开钳钳、zz-chat。
metadata: {"clawdbot":{"emoji":"🦞"}}
---

# 爪爪 🦞 — 手机直连 OpenClaw

## 架构

```
OC 聊天:  手机 ←WebSocket→ 用户的Worker ←→ bridge ←→ OpenClaw CLI
朋友互聊: 手机A ←WebSocket→ WorkerA ──HTTP──→ WorkerB ←WebSocket→ 手机B
注册发现:  Worker ──注册──→ 中心Worker（ai0000.cn）←──查询── Worker
```

每个用户独立部署 Worker，用自己 Cloudflare 额度，互不影响。

## 执行流程（按顺序执行，每一步都做）

用户说"部署爪爪"或类似指令时，按以下步骤自动执行：

### 第一步：部署 Worker（用用户自己的 Cloudflare 账号）

安装 wrangler（如果没装）：

```bash
export PATH="/usr/local/bin:$PATH"
which wrangler 2>/dev/null || npm install -g wrangler 2>&1
```

检查登录状态，未登录则弹出浏览器让用户授权：

```bash
wrangler auth whoami 2>&1
```

如果显示"Not logged in"，执行登录（会自动弹浏览器，用户点同意即可）：

```bash
wrangler login 2>&1
# 等用户在浏览器中点 "Allow" 授权
```

准备用户版 Worker 文件：

```bash
cd ~/.openclaw/workspace/openchat/simple
# 用用户版文件覆盖中心版
cp worker-user.js worker-user-deploy.js
cp wrangler-user.toml wrangler-user-deploy.toml
```

修改 `wrangler-user-deploy.toml` 中的 `name`，改成用户喜欢的名字（如 zz-chat-xxx）：

```bash
sed -i '' "s/name = \"zz-proxy\"/name = \"zz-chat-$(whoami)\"/" wrangler-user-deploy.toml
```

部署：

```bash
cd ~/.openclaw/workspace/openchat/simple
export PATH="/usr/local/bin:$PATH"
wrangler deploy -c wrangler-user-deploy.toml 2>&1
```

记录 Worker URL：

```bash
WORKER_URL=$(wrangler deploy -c wrangler-user-deploy.toml 2>&1 | grep -o 'https://[^ ]*workers.dev' | head -1)
mkdir -p ~/.zz
echo "$WORKER_URL" > ~/.zz/worker_url
echo "Worker URL: $WORKER_URL"
```

### 第二步：注册获取全局 UID

```bash
WORKER_URL=$(cat ~/.zz/worker_url)
ZZ_ID=$(curl -s "$WORKER_URL/register" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "$ZZ_ID" > ~/.zz/id
echo "编号: $ZZ_ID"
```

### 第三步：启动桥接 + 看门狗

先杀掉旧进程：

```bash
pkill -f "bridge.py" 2>/dev/null
pkill -f "watchdog.py" 2>/dev/null
sleep 1
```

复制桥接脚本：

```bash
BRIDGE_DIR=~/.openclaw/workspace/openchat/bridge
mkdir -p "$BRIDGE_DIR"
cp ~/.openclaw/skills/zz-chat/bridge.py "$BRIDGE_DIR/"
cp ~/.openclaw/skills/zz-chat/watchdog.py "$BRIDGE_DIR/"
```

启动看门狗（自动拉起 bridge）：

```bash
WORKER_URL=$(cat ~/.zz/worker_url)
ZZ_ID=$(cat ~/.zz/id)
nohup python3 -u "$BRIDGE_DIR/watchdog.py" >> "$BRIDGE_DIR/watchdog.log" 2>&1 &
sleep 5
# 检查是否启动成功
ps aux | grep -E "(bridge|watchdog)" | grep -v grep
```

或配置 launchd 开机自启（macOS）：

```bash
cat > ~/Library/LaunchAgents/com.zz-chat.bridge.plist << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.zz-chat.bridge</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string><string>-u</string>
        <string>/Users/$(whoami)/.openclaw/workspace/openchat/bridge/watchdog.py</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key><string>/Users/$(whoami)/.local/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
        <key>all_proxy</key><string></string><key>ALL_PROXY</key><string></string>
        <key>http_proxy</key><string></string><key>HTTP_PROXY</key><string></string>
        <key>https_proxy</key><string></string><key>HTTPS_PROXY</key><string></string>
    </dict>
    <key>RunAtLoad</key><true/><key>KeepAlive</key><true/>
    <key>StandardOutPath</key><string>/Users/$(whoami)/.openclaw/workspace/openchat/bridge/watchdog.log</string>
    <key>StandardErrorPath</key><string>/Users/$(whoami)/.openclaw/workspace/openchat/bridge/watchdog.log</string>
    <key>WorkingDirectory</key><string>/Users/$(whoami)/.openclaw/workspace/openchat/bridge</string>
</dict>
</plist>
PLIST
launchctl load ~/Library/LaunchAgents/com.zz-chat.bridge.plist
sleep 5
ps aux | grep -E "(bridge|watchdog)" | grep -v grep
```

### 第四步：生成链接 + 发送二维码

用 canvas 截图二维码发送给用户：

```
ZZ_ID=$(cat ~/.zz/id)
WORKER_URL=$(cat ~/.zz/worker_url)
PAGE_URL=https://badxtdss.github.io/zz-chat/?bridge=${ZZ_ID}&api=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$WORKER_URL', safe=''))")
```

保存 HTML 到 `/tmp/zz-qr.html`：

```html
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>爪爪</title>
<style>
body{font-family:-apple-system,sans-serif;background:#0a0a0a;color:#e0e0e0;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;margin:0}
h1{font-size:24px;margin-bottom:8px}
.id{font-size:48px;font-weight:bold;color:#4fc3f7;margin:12px 0}
.qr{background:#fff;padding:12px;border-radius:12px;margin:16px 0}
.hint{color:#8892b0;font-size:14px;text-align:center;max-width:300px;line-height:1.6}
</style></head>
<body>
<h1>🦞 爪爪</h1>
<div class="id">编号 {ZZ_ID}</div>
<div class="qr" id="qrBox"></div>
<div class="hint">手机扫码打开爪爪<br>消息通过你的 OpenClaw 处理</div>
<script>
const url = '{PAGE_URL}';
const img = new Image();
img.src = 'https://quickchart.io/qr?text=' + encodeURIComponent(url) + '&size=200';
img.style.borderRadius = '8px';
document.getElementById('qrBox').appendChild(img);
</script>
</body>
</html>
```

用 canvas 工具截图（`action="present"` → `action="snapshot"`），然后发图 + 文字消息：

```
✅ 爪爪已部署完成！

🦞 你的编号: {ZZ_ID}
🔗 链接: {PAGE_URL}

📱 添加到桌面（必做）:
1. 打开后点浏览器菜单 → 「访问电脑版」
2. 再点菜单 → 「添加到桌面」
   微信/QQ: 右上角 ··· → 「添加到桌面」
   Safari: 分享按钮 → 「添加到主屏幕」
3. 以后从桌面图标打开，体验最佳
```

## 消息路由

| 聊天类型 | 路径 | Worker |
|---|---|---|
| OC（OpenClaw） | 手机→Worker→bridge→CLI | 用户自己的 Worker |
| 朋友互聊（在线） | 手机A→WorkerA→WorkerB→手机B | 两个用户的 Worker |
| 朋友互聊（离线文字） | WorkerB 存 DO 持久存储，上线补发 | 接收方的 Worker |
| 注册 | Worker→中心Worker（ai0000.cn） | 中心 Worker |

## 文件说明

| 文件 | 用途 |
|------|------|
| `worker.js` | 中心 Worker（ai0000.cn 用） |
| `worker-user.js` | 用户独立 Worker |
| `wrangler.toml` | 中心 Worker 配置 |
| `wrangler-user.toml` | 用户 Worker 配置模板 |
| `bridge.py` | 桥接脚本，支持 `--worker` 和 `--uid` |
| `watchdog.py` | 看门狗，监控 bridge |
| `index.html` | 手机端首页 |
| `chat.html` | 手机端 OC 聊天页（WebSocket） |
| `bridge.js` | Node.js 版桥接（Windows 兼容） |
| `start-bridge.bat` | Windows 启动脚本 |

## 桥接参数

```bash
bridge.py --worker <URL>    # 指定 Worker 地址
bridge.py --uid <ID>        # 直接指定编号
```

## 看门狗（watchdog.py）

```
launchd → watchdog.py → bridge.py
（系统级）  （进程级）    （实际桥接）
```

- 每 10 秒检查 bridge 进程是否存活
- 每 30 秒 bridge 写心跳日志
- 90 秒无活动 → 重启 bridge
- 零服务器压力（本地检测）

## 注意事项

- 只有扫码（带 `?bridge=` + `?api=` 参数）才能进入网页
- 桥接需要电脑保持运行（不休眠）
- 每用户独立 Worker，免费额度：100 WebSocket 并发 + 10 万请求/天
- 消息通过 `openclaw agent` CLI 处理
- 注册后 1 小时未发消息自动清理，发过消息后 24 小时不活跃自动清理
- watchdog 日志：`~/.openclaw/workspace/openchat/bridge/watchdog.log`
- bridge 日志：`~/.openclaw/workspace/openchat/bridge/bridge.log`

## 开发者

🦞 爪爪 by 秋风悠扬

- B站：[秋风悠扬的个人空间](https://b23.tv/rEEYnVF)
- 抖音：363594031
