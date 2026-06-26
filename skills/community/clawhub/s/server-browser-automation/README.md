# Server Browser Automation Skill

在无桌面服务器上实现 OpenClaw 浏览器自动化的完整解决方案。

## 快速开始

```bash
# 1. 安装 XFCE + VNC
sudo apt-get update
sudo apt-get install -y xfce4 xfce4-goodies tigervnc-standalone-server tigervnc-common

# 2. 设置 VNC
vncpasswd
vncserver :1 -geometry 1920x1080 -depth 24

# 3. 安装 Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update
sudo apt-get install -y google-chrome-stable

# 4. 配置 OpenClaw（编辑 ~/.openclaw/openclaw.json）
# 添加 browser 配置（见 SKILL.md）

# 5. 启动 Chrome
export DISPLAY=:1
google-chrome --remote-debugging-port=18800 --no-sandbox --user-data-dir=~/.config/openclaw-browser-openclaw &

# 6. 重启 Gateway
openclaw gateway restart

# 7. 测试
openclaw browser --browser-profile openclaw status
```

## 使用

```bash
# 打开网页
openclaw browser --browser-profile openclaw open https://www.douyin.com

# 查看标签页
openclaw browser --browser-profile openclaw tabs

# 截图
openclaw browser --browser-profile openclaw screenshot page.png
```

## 文档

详细文档请查看 [SKILL.md](./SKILL.md)

## 许可证

MIT License
