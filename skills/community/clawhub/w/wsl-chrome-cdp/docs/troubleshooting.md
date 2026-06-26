# 故障排查指南

**最后更新：** 2026-03-11

---

## 🔍 快速诊断

```bash
# 运行诊断脚本
./skills/wsl-chrome-cdp/enable-browser.sh
```

**根据输出信息排查：**

| 输出 | 原因 | 解决 |
|------|------|------|
| Chrome 未找到 | Chrome 未安装 | 安装 Google Chrome |
| CDP 启动失败 | 防火墙阻止 | 允许端口 9222 |
| 端口被占用 | 其他程序使用 9222 | 结束占用进程 |

---

## ❌ 问题 1：Chrome 未找到

**症状：**

```
[✗] Chrome CDP 启动失败
请检查：
  1. Chrome 是否安装
```

**解决：**

```bash
# 检查 Chrome 是否安装
ls -la "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"

# 如果不存在，安装 Chrome
# 下载地址：https://www.google.com/chrome
```

---

## ❌ 问题 2：CDP 连接超时

**症状：**

```bash
curl http://127.0.0.1:9222/json/version
# 超时或 Connection refused
```

**解决：**

```bash
# 1. 取消代理
unset http_proxy https_proxy
export no_proxy="127.0.0.1,localhost,*"

# 2. 尝试 Windows IP
WINDOWS_IP=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
curl http://$WINDOWS_IP:9222/json/version

# 3. 如果成功，修改 OpenClaw 配置
# ~/.openclaw/openclaw.json
{
  "browser": {
    "profiles": {
      "remote": {
        "cdpUrl": "http://$WINDOWS_IP:9222"
      }
    }
  }
}
```

---

## ❌ 问题 3：端口被占用

**症状：**

```powershell
# Windows 上检查
netstat -ano | findstr 9222
```

**解决：**

```powershell
# 1. 查看占用进程
Get-Process -Id <PID>

# 2. 结束进程
taskkill /F /PID <PID>

# 3. 或使用其他端口
# 修改 enable-browser.sh 中的 CDP_PORT=9223
```

---

## ❌ 问题 4：PowerShell 无法执行

**症状：**

```bash
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe
# command not found
```

**解决：**

```bash
# 检查 WSL 是否配置正确
ls -la /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe

# 如果不存在，检查 WSL 安装
wsl --list --verbose
```

---

## ❌ 问题 5：防火墙阻止

**症状：**

```bash
# WSL 可以 ping 通 Windows，但 CDP 端口不通
curl http://$WINDOWS_IP:9222/json/version
# Connection refused
```

**解决：**

**在 Windows PowerShell（管理员）中执行：**

```powershell
# 添加入站规则
New-NetFirewallRule -DisplayName "Chrome CDP" -Direction Inbound -LocalPort 9222 -Protocol TCP -Action Allow
```

---

## 📋 完整测试流程

```bash
# 1. 检查 Chrome 安装
ls -la "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"

# 2. 检查 PowerShell
ls -la /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe

# 3. 运行启用脚本
./skills/wsl-chrome-cdp/enable-browser.sh

# 4. 测试 CDP
curl http://127.0.0.1:9222/json/version

# 5. 测试 OpenClaw
openclaw browser status
```

---

## 💕 需要帮助？

**如果以上方法都无法解决：**

1. 查看技能目录：`~/.openclaw/workspace/skills/wsl-chrome-cdp/`
2. 检查日志输出
3. 在 ClawHub 提交 Issue

---

*故障排查指南版本：1.0.0 | 最后更新：2026-03-11*
