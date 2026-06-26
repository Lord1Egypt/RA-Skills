---
name: xhs-mcp-installer
description: 一键安装并启动小红书 MCP 服务（xiaohongshu-mcp）。当用户说"帮我安装小红书MCP"、"安装 xhs-mcp"、"配置小红书 MCP"、"帮我搞个小红书"、或提供 GitHub 链接 https://github.com/xpzouying/xiaohongshu-mcp 时触发。自动检测系统、下载二进制、配置开机自启、启动服务。
metadata: {"openclaw": {"emoji": "📕", "requires": {"bins": ["curl"]}}}
---

# 📕 小红书 MCP 一键安装器

自动完成以下工作：
1. 检测系统（macOS / Linux）并选择对应二进制
2. 下载 xhs-mcp 到 `~/xiaohongshu-mcp/`
3. 配置为后台服务（macOS: launchd，Linux: systemd）
4. 启动服务并验证健康状态

---

## 一、安装前检查

```bash
# 检查是否已安装
lsof -i :18060 2>/dev/null | grep LISTEN && echo "✅ 已在运行" || echo "❌ 未运行"

# 检查二进制是否存在
[ -f ~/xiaohongshu-mcp/xhs-mcp ] && echo "✅ 已下载" || echo "❌ 未下载"
```

---

## 二、自动安装流程

### 2.1 检测系统

```bash
OS="$(uname -s)"
ARCH="$(uname -m)"
echo "系统: $OS, 架构: $ARCH"
```

| 系统 | 架构 | 二进制名 |
|------|------|----------|
| Darwin (macOS) | x86_64 | xhs-mcp-darwin-amd64 |
| Darwin (macOS) | arm64 | xhs-mcp-darwin-arm64 |
| Linux | x86_64 | xhs-mcp-linux-amd64 |
| Linux | aarch64 | xhs-mcp-linux-arm64 |

### 2.2 下载二进制

```bash
mkdir -p ~/xiaohongshu-mcp
cd ~/xiaohongshu-mcp

# 自动识别架构
case "$(uname -s)-$(uname -m)" in
  Darwin-x86_64)  BINARY="xhs-mcp-darwin-amd64" ;;
  Darwin-arm64)    BINARY="xhs-mcp-darwin-arm64" ;;
  Linux-x86_64)   BINARY="xhs-mcp-linux-amd64" ;;
  Linux-aarch64)  BINARY="xhs-mcp-linux-arm64" ;;
  *) echo "❌ 不支持的平台: $(uname -s) $(uname -m)"; exit 1 ;;
esac

echo "下载 $BINARY ..."
curl -L "https://github.com/xpzouying/xiaohongshu-mcp/releases/latest/download/${BINARY}" \
  -o ./xhs-mcp --progress-bar
chmod +x ./xhs-mcp
```

### 2.3 启动服务（手动测试）

```bash
cd ~/xiaohongshu-mcp

# 杀掉旧进程
lsof -ti :18060 | xargs kill -9 2>/dev/null
sleep 1

# 启动
nohup ./xhs-mcp server --port 18060 > ~/xiaohongshu-mcp/mcp.log 2>&1 &
sleep 3

# 验证
if lsof -i :18060 | grep LISTEN > /dev/null; then
  echo "✅ 服务启动成功，端口 18060 监听中"
else
  echo "❌ 启动失败，查看日志：tail ~/xiaohongshu-mcp/mcp.log"
  tail -20 ~/xiaohongshu-mcp/mcp.log
fi
```

### 2.4 配置开机自启

#### macOS — launchd plist

```bash
XHS_PLIST="$HOME/Library/LaunchAgents/com.openclaw.xhs-mcp.plist"
mkdir -p "$HOME/Library/LaunchAgents"

cat > "$XHS_PLIST" << 'EOFPLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.xhs-mcp</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/$(whoami)/xiaohongshu-mcp/xhs-mcp</string>
        <string>server</string>
        <string>--port</string>
        <string>18060</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/$(whoami)/xiaohongshu-mcp</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/$(whoami)/xiaohongshu-mcp/mcp.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/$(whoami)/xiaohongshu-mcp/mcp.log</string>
    <key>EnvironmentVariables</key>
    <dict/>
</dict>
</plist>
EOFPLIST

# 加载服务
launchctl unload "$XHS_PLIST" 2>/dev/null
launchctl load "$XHS_PLIST"
echo "✅ launchd 服务已加载"
```

#### Linux — systemd

```bash
sudo tee /etc/systemd/system/xhs-mcp.service > /dev/null << 'EOFSYSTEMD'
[Unit]
Description=Xiaohongshu MCP Service
After=network.target

[Service]
WorkingDirectory=/root/xiaohongshu-mcp
ExecStart=/root/xiaohongshu-mcp/xhs-mcp server --port 18060
Restart=always
RestartSec=5
StandardOutput=append:/root/xiaohongshu-mcp/mcp.log
StandardError=append:/root/xiaohongshu-mcp/mcp.log

[Install]
WantedBy=multi-user.target
EOFSYSTEMD

sudo systemctl daemon-reload
sudo systemctl enable xhs-mcp
sudo systemctl start xhs-mcp
echo "✅ systemd 服务已启动"
```

### 2.5 创建看门狗脚本（自动恢复崩溃）

```bash
cat > ~/xiaohongshu-mcp/watchdog.sh << 'EOFWATCHDOG'
#!/bin/bash
# xhs-mcp 看门狗：服务崩溃后自动重启
PORT=18060
LOG=~/xiaohongshu-mcp/watchdog.log

check() {
    curl -s --max-time 3 http://localhost:$PORT/health > /dev/null 2>&1
}

restart() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') 重启服务..." >> "$LOG"
    lsof -ti :$PORT | xargs kill -9 2>/dev/null
    sleep 2
    cd ~/xiaohongshu-mcp
    nohup ./xhs-mcp server --port $PORT >> ~/xiaohongshu-mcp/mcp.log 2>&1 &
    sleep 3
    if check; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') 重启成功" >> "$LOG"
    fi
}

if ! check; then
    restart
fi
EOFWATCHDOG
chmod +x ~/xiaohongshu-mcp/watchdog.sh

# macOS: 添加定期检查到 crontab
(crontab -l 2>/dev/null | grep -v watchdog; echo "*/5 * * * * ~/xiaohongshu-mcp/watchdog.sh") | crontab -
echo "✅ 看门狗已配置（每5分钟检查一次）"
```

---

## 三、验证安装

### 3.1 服务健康检查

```bash
# 检查进程
ps aux | grep -i xhs-mcp | grep -v grep

# 检查端口
lsof -i :18060 | grep LISTEN

# 检查登录状态（调用 MCP）
MCP_URL="http://localhost:18060/mcp"
SESSION_ID=$(curl -s -D /tmp/xhs_check -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}},"id":1}' > /dev/null \
  && grep -i 'Mcp-Session-Id' /tmp/xhs_check | tr -d '\r' | awk '{print $2}')
curl -s -X POST "$MCP_URL" -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' > /dev/null
curl -s -X POST "$MCP_URL" -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"check_login_status","arguments":{}},"id":2}'
```

### 3.2 判断结果

| 输出 | 含义 | 操作 |
|------|------|------|
| `✅ 已在运行` + `✅ 已下载` | 已安装，跳过 | 静默完成 |
| 服务启动成功 + 登录状态正常 | 全新安装完成 | 告知用户 |
| 服务启动成功 + `❌ 未登录` | 需扫码登录 | 进入登录流程 |
| ❌ 启动失败 | 下载或权限问题 | 查看日志排查 |

---

## 四、扫码登录（如需要）

### 方式一：直接获取二维码（推荐）

```bash
MCP_URL="http://localhost:18060/mcp"
SESSION_ID=$(curl -s -D /tmp/xhs_qr_h -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}},"id":1}' > /dev/null \
  && grep -i 'Mcp-Session-Id' /tmp/xhs_qr_h | tr -d '\r' | awk '{print $2}')
curl -s -X POST "$MCP_URL" -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' > /dev/null
curl -s -X POST "$MCP_URL" -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_login_qrcode","arguments":{}},"id":2}' | \
  python3 -c "
import sys,json
d=json.load(sys.stdin)
text=d.get('result',{}).get('content',[{}])[0].get('text','')
# 提取base64图片
import re
m=re.search(r'data:image/png;base64,([A-Za-z0-9+/=]+)', text)
if m:
    open('/tmp/xhs_qr.png','wb').write(__import__('base64').b64decode(m.group(1)))
    print('二维码已保存到 /tmp/xhs_qr.png')
else:
    print(text)
"
```

### 方式二：Cookie 导入（无需扫码）

用户提供浏览器 Cookie 字符串后，转换为 JSON 保存：

```bash
python3 -c "
import json, sys
cookie_str = sys.argv[1].strip()
cookies = []
for pair in cookie_str.split(';'):
    pair = pair.strip()
    if '=' not in pair: continue
    name, value = pair.split('=', 1)
    cookies.append({
        'name': name.strip(),
        'value': value.strip(),
        'domain': '.xiaohongshu.com',
        'path': '/',
        'expires': -1,
        'httpOnly': name.strip() in ('web_session', 'id_token', 'acw_tc'),
        'secure': name.strip() in ('web_session', 'id_token'),
        'session': False,
        'priority': 'Medium',
        'sameParty': False,
        'sourceScheme': 'Secure',
        'sourcePort': 443
    })
with open('$HOME/xiaohongshu-mcp/cookies.json', 'w') as f:
    json.dump(cookies, f, ensure_ascii=False)
print(f'已保存 {len(cookies)} 个 Cookie')
" '用户粘贴的cookie字符串'
```

---

## 五、故障排查

```bash
# 服务状态
ps aux | grep xhs-mcp | grep -v grep
lsof -i :18060

# 查看日志
tail -30 ~/xiaohongshu-mcp/mcp.log

# 重启服务（macOS）
launchctl unload ~/Library/LaunchAgents/com.openclaw.xhs-mcp.plist
launchctl load ~/Library/LaunchAgents/com.openclaw.xhs-mcp.plist

# 重启服务（Linux）
sudo systemctl restart xhs-mcp

# 卸载服务
launchctl unload ~/Library/LaunchAgents/com.openclaw.xhs-mcp.plist 2>/dev/null
sudo systemctl disable xhs-mcp 2>/dev/null
```

---

## 六、安装完成告知模板

安装成功后，告知用户：

> ✅ **小红书 MCP 安装完成！**
>
> 🐹 服务已就绪，后台运行中
> 📍 端口：18060
> 🔄 开机自启：已配置
> 🐕 看门狗：每5分钟自动检查
>
> 📌 下一步：用小红书APP扫码登录（告诉我就行，我会发二维码给你）
