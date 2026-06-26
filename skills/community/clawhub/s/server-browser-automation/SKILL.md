# Server Browser Automation Skill

在无桌面服务器上实现 OpenClaw 浏览器自动化的完整解决方案。

## 📖 描述

**Server Browser Automation** 是一个帮助你在无桌面 Ubuntu 服务器上配置和使用 OpenClaw 浏览器自动化功能的 Skill。

**解决的核心问题**：
- ❌ 无桌面环境无法显示浏览器
- ❌ Chrome 远程调试配置复杂
- ❌ AI 无法操作需要登录的网站
- ❌ Cookie 无法持久化保存

**提供的解决方案**：
- ✅ XFCE + VNC 虚拟桌面
- ✅ Chrome 远程调试配置
- ✅ 个人资料模式（Cookie 持久化）
- ✅ AI 自然语言操作浏览器

## 🎯 适用场景

| 场景 | 说明 |
|------|------|
| **数据采集** | 爬取抖音、微博、Twitter 等需要登录的网站 |
| **自动化测试** | 自动测试网页功能、表单提交 |
| **定时任务** | 定期抓取数据、监控价格变化 |
| **批量操作** | 多账号管理、批量发布内容 |

## 📦 安装

### 前置要求

- Ubuntu Server 20.04+（无桌面版本）
- OpenClaw 2026.3.13+
- Node.js 22+
- Docker（可选，用于 noVNC）
- root 或 sudo 权限

### 一键安装脚本

```bash
# 1. 克隆 Skill
git clone https://github.com/YOUR_USERNAME/server-browser-automation.git
cd server-browser-automation

# 2. 运行安装脚本
./install.sh

# 3. 验证安装
openclaw browser --browser-profile openclaw status
```

### 手动安装

```bash
# 1. 安装 XFCE 桌面
sudo apt-get update
sudo apt-get install -y xfce4 xfce4-goodies

# 2. 安装 VNC 服务器
sudo apt-get install -y tigervnc-standalone-server tigervnc-common

# 3. 设置 VNC 密码
vncpasswd

# 4. 启动 VNC
vncserver :1 -geometry 1920x1080 -depth 24

# 5. 安装 Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update
sudo apt-get install -y google-chrome-stable

# 6. 配置 OpenClaw
# 编辑 ~/.openclaw/openclaw.json，添加 browser 配置（见下方配置章节）

# 7. 启动 Chrome
export DISPLAY=:1
google-chrome \
  --remote-debugging-port=18800 \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --user-data-dir=~/.config/openclaw-browser-openclaw \
  > /tmp/chromium.log 2>&1 &

# 8. 重启 Gateway
openclaw gateway restart
```

## ⚙️ 配置

### OpenClaw 配置

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "openclaw",
    "headless": false,
    "remoteDebuggingPort": 18800,
    "userDataDir": "/home/your_user/.config/openclaw-browser-openclaw",
    "profiles": {
      "openclaw": {
        "cdpPort": 18800,
        "color": "#FF4500",
        "userDataDir": "/home/your_user/.config/openclaw-browser-openclaw"
      }
    }
  }
}
```

### VNC 配置

创建 `~/.vnc/xstartup`：

```bash
#!/bin/bash
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
exec startxfce4
```

```bash
chmod +x ~/.vnc/xstartup
```

## 🚀 使用

### 基本命令

```bash
# 检查浏览器状态
openclaw browser --browser-profile openclaw status

# 查看标签页
openclaw browser --browser-profile openclaw tabs

# 打开网页
openclaw browser --browser-profile openclaw open https://www.example.com

# 截图
openclaw browser --browser-profile openclaw screenshot page.png

# 执行 JavaScript
openclaw browser --browser-profile openclaw eval "document.title"
```

### 自然语言指令

直接用自然语言告诉 AI：

```
帮我打开抖音
用浏览器访问 https://www.douyin.com
看看百度的标题是什么
帮我登录抖音，然后爬取前 20 个视频
截图当前页面
提取这个页面的所有视频链接
```

### 首次登录流程

1. **启动 Chrome**（见安装步骤）
2. **用 VNC 查看器连接**：`服务器 IP:5901`
3. **在 Chrome 中访问目标网站**（如抖音）
4. **完成登录**（扫码 + 验证码）
5. **保持 Chrome 运行**
6. **后续 AI 自动操作**（Cookie 已保存）

### 自动化示例

#### 抖音数据爬取

```bash
# 打开抖音（首次需要人工登录）
openclaw browser --browser-profile openclaw open https://www.douyin.com

# 登录后，后续可以直接爬取
# AI 会自动提取数据并保存
```

#### 价格监控

```bash
# 每天检查价格
openclaw browser --browser-profile openclaw open https://item.jd.com/xxx.html

# AI 提取价格并保存
```

#### 自动化测试

```bash
# 测试登录功能
openclaw browser --browser-profile openclaw open https://example.com/login

# AI 自动填写表单并提交
```

## 🔧 故障排查

### Chrome 未启动

```bash
# 检查进程
ps aux | grep chrome

# 查看日志
cat /tmp/chromium.log

# 重新启动
export DISPLAY=:1
google-chrome --remote-debugging-port=18800 --no-sandbox --user-data-dir=~/.config/openclaw-browser-openclaw &
```

### OpenClaw 无法连接

```bash
# 检查 CDP 端口
curl http://127.0.0.1:18800/json/list

# 检查配置
cat ~/.openclaw/openclaw.json | jq '.browser'

# 重启 Gateway
openclaw gateway restart
```

### VNC 无法连接

```bash
# 检查 VNC 进程
ps aux | grep vnc

# 重启 VNC
vncserver -kill :1
vncserver :1 -geometry 1920x1080 -depth 24
```

### Cookie 失效

```bash
# 删除旧 Cookie
rm -rf ~/.config/openclaw-browser-openclaw

# 重新启动 Chrome，重新登录
export DISPLAY=:1
google-chrome --remote-debugging-port=18800 --no-sandbox --user-data-dir=~/.config/openclaw-browser-openclaw &
```

## 📊 架构说明

```
┌─────────────────────────────────────────────────────────┐
│                    用户（本地电脑）                       │
│                  VNC 查看器 / noVNC                       │
└────────────────────┬────────────────────────────────────┘
                     │ VNC (端口 5901)
                     ▼
┌─────────────────────────────────────────────────────────┐
│              服务器（Ubuntu 无桌面）                       │
│  ┌─────────────────────────────────────────────────┐    │
│  │              XFCE 虚拟桌面 (:1)                   │    │
│  │  ┌─────────────────────────────────────────┐    │    │
│  │  │          Google Chrome                   │    │    │
│  │  │  远程调试端口：18800                      │    │    │
│  │  │  User Data: Cookie 持久化                 │    │    │
│  │  └─────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────┘    │
│                     │ CDP                                 │
│                     ▼                                     │
│  ┌─────────────────────────────────────────────────┐    │
│  │           OpenClaw Gateway                       │    │
│  │           端口：18789                            │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                     │ WebSocket
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    AI 助手                               │
│              （飞书 / Telegram / Discord）                │
└─────────────────────────────────────────────────────────┘
```

## 🎓 进阶技巧

### 1. 保存登录状态

```bash
# Cookie 自动保存在 userDataDir
# 无需手动保存，下次启动 Chrome 自动加载
```

### 2. 多账号管理

```bash
# 为不同账号创建不同的 userDataDir
google-chrome --remote-debugging-port=18801 --user-data-dir=~/.config/chrome-account1 &
google-chrome --remote-debugging-port=18802 --user-data-dir=~/.config/chrome-account2 &
```

### 3. 定时任务

```bash
# 添加 cron 任务
crontab -e

# 每天 9 点执行
0 9 * * * openclaw browser --browser-profile openclaw open https://www.douyin.com
```

### 4. 数据导出

```bash
# AI 自动提取数据并保存为 JSON/CSV
# 示例：提取抖音视频数据
openclaw browser --browser-profile openclaw eval "
  Array.from(document.querySelectorAll('.video-card')).map(card => ({
    title: card.querySelector('.video-title')?.innerText,
    author: card.querySelector('.author-name')?.innerText,
    plays: card.querySelector('.play-count')?.innerText
  }))
"
```

## ⚠️ 注意事项

### 安全

- **不要在生产服务器上启用远程调试**（仅限开发/测试环境）
- **VNC 密码要设置复杂**
- **防火墙只允许信任的 IP 访问 VNC 端口**

### 性能

- **Chrome 会占用较多内存**（建议服务器至少 2GB 内存）
- **定期清理 userDataDir**（避免 Cookie 缓存过大）
- **使用 `--disable-gpu` 减少 GPU 依赖**

### 反爬

- **控制请求频率**（避免被封 IP）
- **使用代理 IP**（如需大规模爬取）
- **遵守网站 robots.txt**

## 📚 相关资源

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [VNC 官方文档](https://www.realvnc.com/en/connect/docs/)
- [XFCE 官方文档](https://docs.xfce.org/)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👥 作者

- 开发者
- OpenClaw 社区

## 🙏 致谢

感谢 OpenClaw 团队提供的优秀框架！

---

**Happy Automating!** 🚀
