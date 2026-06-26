---
name: tailscale-vpn
version: 1.0.0
description: Tailscale安全组网工具 - 基于WireGuard的虚拟组网，安全内网穿透，不暴露公网IP，点对点加密连接。适用于远程访问、居家办公、服务器管理。
keywords: [tailscale,vpn,wireguard,组网,安全,远程访问,内网穿透,network]
---

# Tailscale 安全组网

**触发词：** `Tailscale组网` / `Tailscale安装` / `安全远程访问`

**官网：** https://tailscale.com

---

## 什么是 Tailscale？

基于 **WireGuard** 的虚拟组网工具：
- 🌐 把你所有设备组成**虚拟安全网络**
- 🔒 端到端加密，不暴露公网IP
- ⚡ 点对点直连，延迟低
- 🔓 无需配置路由器/端口映射

---

## 核心优势

| 特性 | Tailscale | 传统VPN |
|------|-----------|---------|
| 连接方式 | WireGuard P2P | 中心服务器 |
| 公网暴露 | ❌ 不暴露 | ⚠️ 可能暴露 |
| 延迟 | 低（P2P直连） | 高（中转） |
| 配置 | 极简 | 复杂 |
| 设备数 | 100+免费 | 通常有限 |

---

## 工作原理

```
传统方式（危险）：
你的设备 → 公网IP → 暴露风险 → 被攻击

Tailscale方式（安全）：
你的设备 → Tailscale加密隧道 → 对方设备
                ↓
         不暴露公网IP
```

---

## 安装步骤

### 1️⃣ 注册账号

1. 访问 https://login.tailscale.com
2. 用 GitHub/Google/Microsoft 注册
3. 免费版支持 **100台设备**

### 2️⃣ 安装客户端

**Windows:**
```powershell
# 下载安装
https://tailscale.com/download/windows
# 或用 winget
winget install Tailscale.Tailscale
```

**macOS:**
```bash
# 用 Homebrew
brew install tailscale
# 或 App Store 下载
```

**Linux:**
```bash
# 一键安装
curl -fsSL https://tailscale.com/install.sh | sh

# 启动服务
sudo tailscaled up
```

**iOS/Android:**
App Store / Play Store 搜索 "Tailscale" 下载

### 3️⃣ 连接登录

```bash
# 启动并登录
tailscale up

# 会自动打开浏览器授权
```

### 4️⃣ 查看网络

```bash
# 查看所有设备
tailscale status

# 示例输出：
# 100.x.x.x   macbook
# 100.x.x.x   desktop
# 100.x.x.x   phone
```

---

## 常用命令

```bash
# 连接/断开
tailscale up
tailscale down

# 查看状态
tailscale status

# 分享设备给其他用户
tailscale share

# 访问另一台设备（像本地一样）
ssh 100.x.x.x
ping 100.x.x.x
\\100.x.x.x\c$  # Windows共享

# 退出登录
tailscale logout
```

---

## 高级功能

### 1️⃣ 子网路由（访问整个局域网）

```bash
# 假设局域网是 192.168.1.0/24
sudo tailscale up --advertise-routes=192.168.1.0/24

# 在管理后台批准路由
# https://login.tailscale.com/acls
```

### 2️⃣ Exit Node（用其他设备上网）

```bash
# 把某设备设为出口节点
tailscale up --exit-node=100.x.x.x

# 其他设备通过它上网
```

### 3️⃣ 配合远程桌面

**RustDesk + Tailscale：**
```bash
# 1. 两台设备都加入Tailscale网络
# 2. 获取对方IP（如 100.105.1.200）
# 3. RustDesk连接 100.105.1.200
```

**优势：**
- ✅ 不暴露公网IP
- ✅ 加密P2P连接
- ✅ 无需设置端口转发

---

## ACL 访问控制

在 https://login.tailscale.com/admin/acls 设置谁可以访问谁：

```json
{
  "acls": [
    {"action": "accept", "src": ["group:tech"], "dst": ["*:*"]}
  ]
}
```

---

## 安全优势

| 风险 | Tailscale解决方案 |
|------|-----------------|
| 公网IP暴露 | ✅ 使用100.x.x.x虚拟IP |
| 中间人攻击 | ✅ WireGuard端到端加密 |
| 未授权访问 | ✅ Tailscale认证 + ACL |
| 端口映射 | ✅ 无需端口映射 |

---

## 使用场景

| 场景 | 说明 |
|------|------|
| 🏠 居家办公 | 访问公司内网资源 |
| 🖥️ 远程桌面 | 连接家里/公司电脑 |
| 🖥️ 服务器管理 | SSH/远程管理服务器 |
| 📱 跨设备同步 | 文件共享、剪贴板 |
| 🔒 安全访问 | 不暴露公网的服务 |

---

## 搭配推荐

**最佳组合：**
```
Tailscale（安全组网）+ RustDesk（远程控制）
```

**优势：**
- 公网IP完全隐藏
- 端到端加密
- 无需配置路由器
- 延迟低，体验好

---

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| 无法连接 | 检查 tailscale status |
| 延迟高 | 尝试不同出口节点 |
| 设备不在线 | 确保客户端运行中 |
| ACL限制 | 检查管理后台设置 |

---

## 安装状态

检查是否已安装：
```bash
which tailscale
tailscale version
```

---

*基于 WireGuard | 安全组网专家*
