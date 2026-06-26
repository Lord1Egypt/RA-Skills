# wsl-chrome-cdp - WSL2 访问 Windows Chrome 浏览器

**版本：** 1.0.0  
**作者：** 杏子  
**创建日期：** 2026-03-11  
**适用系统：** Windows + WSL2 + OpenClaw

---

## 📋 技能描述

解决 WSL2 环境中无法访问 Windows Chrome 浏览器的问题，实现 OpenClaw browser 工具对 Windows Chrome 的远程控制。

**核心功能：**
- ✅ 自动检测 Chrome 是否运行
- ✅ 自动启动 Chrome 调试模式
- ✅ 自动验证 CDP 连接
- ✅ 完全无需手动操作

---

## 🚀 使用方法

### **全自动模式（推荐）**

**安装技能后，无需任何配置！**

**在 OpenClaw 对话中直接说：**

```
打开百度
```

```
访问 GitHub
```

```
帮我截图
```

**杏子会自动：**
1. ✅ 检测 Chrome 是否运行
2. ✅ 如果没运行，自动启动 Chrome 调试模式
3. ✅ 验证 CDP 连接
4. ✅ 执行你的请求

**完全无需手动操作！**

---

### **手动运行（可选）**

```bash
# 一键启用浏览器
./skills/wsl-chrome-cdp/enable-browser.sh
```

---

## 📁 文件结构

```
wsl-chrome-cdp/
├── SKILL.md                          # 技能说明（本文件）
├── README.md                         # 快速入门
├── enable-browser.sh                 # 全自动启用脚本
├── scripts/
│   └── start-chrome-debug.bat        # Windows 备用启动脚本
└── docs/
    └── troubleshooting.md            # 故障排查指南
```

---

## 🔍 故障排查

### **问题 1：Chrome 启动失败**

**症状：** 脚本显示 "Chrome CDP 启动失败"

**解决：**
```bash
# 1. 检查 Chrome 是否安装
ls -la "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"

# 2. 手动启动 Chrome 调试模式
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command \
  'Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" \
   -ArgumentList "--remote-debugging-port=9222","--user-data-dir=C:\Users\$env:USERNAME\AppData\Local\Google\Chrome\Debug","--no-first-run"'
```

---

### **问题 2：CDP 连接超时**

**症状：** `curl http://127.0.0.1:9222/json/version` 超时

**解决：**
```bash
# 1. 取消代理
unset http_proxy https_proxy

# 2. 尝试 Windows IP
WINDOWS_IP=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
curl http://$WINDOWS_IP:9222/json/version
```

---

### **问题 3：端口被占用**

**症状：** 端口 9222 已被其他进程占用

**解决：**
```powershell
# Windows 上检查端口
netstat -ano | findstr 9222

# 结束占用进程
taskkill /F /PID <进程 ID>
```

---

### **更多问题**

**查看完整故障排查指南：** `docs/troubleshooting.md`

---

## 📚 参考资料

- [OpenClaw Browser 文档](https://docs.openclaw.ai/tools/browser)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)

---

## 💕 关于作者

**杏子（Apricot）** - OpenClaw 社区贡献者

**创建背景：**
> 2026-03-11，为解决 WSL2 中 OpenClaw 无法访问 Windows Chrome 的问题，
> 杏子整理了完整的自动化配置流程。
> 希望这个技能能帮助更多人！

**技能理念：**
> "配置应该是全自动的，排查应该是清晰的。"
> "今天踩的坑，明天就不用再踩了。"

---

*技能版本：1.0.0 | 最后更新：2026-03-11*
