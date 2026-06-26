#!/bin/bash
# Server Browser Automation Skill - 安装脚本

set -e

echo "🚀 开始安装 Server Browser Automation Skill..."

# 检查是否 root 或 sudo
if [ "$EUID" -ne 0 ]; then
  echo "❌ 请使用 sudo 运行此脚本"
  exit 1
fi

# 1. 安装 XFCE 桌面
echo "📦 安装 XFCE 桌面..."
apt-get update
apt-get install -y xfce4 xfce4-goodies

# 2. 安装 VNC 服务器
echo "📦 安装 VNC 服务器..."
apt-get install -y tigervnc-standalone-server tigervnc-common

# 3. 安装 Chrome
echo "📦 安装 Google Chrome..."
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
apt-get update
apt-get install -y google-chrome-stable

# 4. 配置 VNC
echo "⚙️  配置 VNC..."
VNC_USER=$(whoami)
VNC_HOME=$(eval echo ~$VNC_USER)

mkdir -p $VNC_HOME/.vnc
cat > $VNC_HOME/.vnc/xstartup << 'EOF'
#!/bin/bash
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
exec startxfce4
EOF

chmod +x $VNC_HOME/.vnc/xstartup
chown -R $VNC_USER:$VNC_USER $VNC_HOME/.vnc

# 5. 提示用户设置 VNC 密码
echo ""
echo "🔐 请设置 VNC 密码："
su - $VNC_USER -c "vncpasswd"

# 6. 启动 VNC
echo "🚀 启动 VNC 服务器..."
su - $VNC_USER -c "vncserver :1 -geometry 1920x1080 -depth 24"

# 7. 配置 OpenClaw
echo "⚙️  配置 OpenClaw..."
OPENCLAW_CONFIG="$VNC_HOME/.openclaw/openclaw.json"

if [ -f "$OPENCLAW_CONFIG" ]; then
  echo "📝 备份 OpenClaw 配置..."
  cp "$OPENCLAW_CONFIG" "$OPENCLAW_CONFIG.bak.$(date +%Y%m%d)"
  
  echo "📝 更新 browser 配置..."
  # 使用 Python 更新 JSON（更安全）
  python3 << PYTHON_EOF
import json

with open('$OPENCLAW_CONFIG', 'r') as f:
    config = json.load(f)

config['browser'] = {
    "enabled": True,
    "defaultProfile": "openclaw",
    "headless": False,
    "remoteDebuggingPort": 18800,
    "userDataDir": f"/home/$VNC_USER/.config/openclaw-browser-openclaw",
    "profiles": {
        "openclaw": {
            "cdpPort": 18800,
            "color": "#FF4500",
            "userDataDir": f"/home/$VNC_USER/.config/openclaw-browser-openclaw"
        }
    }
}

with open('$OPENCLAW_CONFIG', 'w') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print("✅ OpenClaw 配置已更新")
PYTHON_EOF
else
  echo "⚠️  未找到 OpenClaw 配置文件，请手动配置"
fi

# 8. 创建 Chrome 启动脚本
echo "📝 创建 Chrome 启动脚本..."
cat > $VNC_HOME/start-chrome.sh << 'EOF'
#!/bin/bash
export DISPLAY=:1
google-chrome \
  --remote-debugging-port=18800 \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --user-data-dir=/home/$(whoami)/.config/openclaw-browser-openclaw \
  > /tmp/chromium.log 2>&1 &
echo "✅ Chrome 已启动（端口 18800）"
echo "📄 日志：/tmp/chromium.log"
EOF

chmod +x $VNC_HOME/start-chrome.sh
chown $VNC_USER:$VNC_USER $VNC_HOME/start-chrome.sh

# 9. 完成
echo ""
echo "✅ 安装完成！"
echo ""
echo "📋 下一步："
echo "1. 用 VNC 查看器连接：服务器 IP:5901"
echo "2. 运行启动脚本：~/start-chrome.sh"
echo "3. 重启 OpenClaw Gateway: openclaw gateway restart"
echo "4. 测试：openclaw browser --browser-profile openclaw status"
echo ""
echo "📖 详细文档：SKILL.md"
echo ""
