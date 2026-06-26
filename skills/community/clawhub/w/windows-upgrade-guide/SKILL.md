---
name: windows-upgrade-guide
description: |
  Windows 环境下 OpenClaw 安装与升级排障指南。解决闪退、配置丢失、版本兼容、WSL vs Windows 原生等问题。

  **当以下情况时使用此 Skill**：
  (1) Windows 用户升级 OpenClaw 后闪退
  (2) 需要 WSL vs Windows 原生安装对比
  (3) v2.0 微信集成无损升级
  (4) 配置丢失或版本兼容问题
  (5) 用户提到"windows 升级"、"闪退"、"WSL"
---

# 🪟 Windows OpenClaw 升级排障指南

## 版本信息

- **版本**: v1.0.0
- **作者**: 郑宇航
- **适用场景**: Windows 用户安装/升级/排障

---

## 🚨 常见问题快速索引

| 问题 | 解决方案 | 难度 |
|------|----------|------|
| 升级后闪退 | [方案 1](#方案 1-升级后闪退) | ⭐ |
| 配置丢失 | [方案 2](#方案 2-配置丢失) | ⭐⭐ |
| v2.0 微信无法使用 | [方案 3](#方案 3-v20-微信集成升级) | ⭐⭐⭐ |
| WSL vs Windows 选择 | [对比表](#wsl-vs-windows-原生) | ⭐ |

---

## 💡 核心解决方案

### 方案 1: 升级后闪退

**症状**: OpenClaw 2026.4.8 Windows 版本升级后闪退

**原因分析**:
- Node.js 版本不兼容
- ESM 模块加载失败
- 配置文件格式变更

**解决步骤**:

```bash
# 1. 检查 Node.js 版本
node -v
# 需要 >= 18.0.0

# 2. 清理缓存
npm cache clean --force

# 3. 重新安装
npm uninstall -g openclaw
npm install -g openclaw@latest

# 4. 重置配置
rm -rf ~/.openclaw
openclaw init
```

**使用工具**: `exec`, `node_version_check`

**期望输出**:
```
✅ Node.js v20.10.0
✅ OpenClaw 已重装
✅ 配置已重置
```

---

### 方案 2: 配置丢失

**症状**: 升级后 openclaw.json 配置丢失

**解决步骤**:

```bash
# 1. 备份旧配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak

# 2. 查看配置差异
diff ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json

# 3. 手动合并配置
# 或使用配置迁移工具
openclaw config migrate
```

**使用工具**: `file_backup`, `config_diff`

---

### 方案 3: v2.0 微信集成升级

**症状**: 2.0 版本对接不了微信

**无损升级路径**:

```bash
# 1. 检查当前版本
openclaw -v

# 2. 备份微信配置
cp ~/.openclaw/config/wechat.json ~/.openclaw/config/wechat.json.bak

# 3. 升级到最新版
npm install -g openclaw@latest

# 4. 安装官方飞书插件
npx -y @larksuite/openclaw-lark install

# 5. 恢复微信配置
cp ~/.openclaw/config/wechat.json.bak ~/.openclaw/config/wechat.json

# 6. 验证微信集成
openclaw config get channels.wechat
```

**使用工具**: `feishu-official-plugin-switch`, `config_backup`

---

## 📊 WSL vs Windows 原生

| 特性 | WSL2 | Windows 原生 | 推荐度 |
|------|------|--------------|--------|
| **稳定性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | WSL2 ✅ |
| **性能** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 平手 |
| **兼容性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | WSL2 ✅ |
| **安装难度** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Windows ✅ |
| **文件访问** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Windows ✅ |
| **升级体验** | ⭐⭐⭐⭐⭐ | ⭐⭐ | WSL2 ✅ |

**推荐**:
- **开发/生产**: WSL2 (Ubuntu 22.04)
- **快速体验**: Windows 原生

---

## 🛠️ 安装方式对比

### WSL2 安装（推荐）

```bash
# 1. 安装 WSL2
wsl --install -d Ubuntu

# 2. 进入 WSL
wsl

# 3. 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 4. 安装 OpenClaw
npm install -g openclaw

# 5. 初始化
openclaw init
```

**优势**:
- ✅ 与 Linux 服务器环境一致
- ✅ 升级稳定，不易闪退
- ✅ 完整的文件系统权限

### Windows 原生安装

```powershell
# 1. 安装 Node.js (从官网下载)
# https://nodejs.org/

# 2. 以管理员身份运行 PowerShell
npm install -g openclaw

# 3. 初始化
openclaw init
```

**注意**:
- ⚠️ 需要管理员权限
- ⚠️ 路径可能包含空格导致问题
- ⚠️ 升级时可能闪退

---

## 🔧 排障工具

### 1. 健康检查

```bash
openclaw doctor
```

**检查项目**:
- Node.js 版本
- 配置文件完整性
- 插件加载状态
- 网络连接

### 2. 日志查看

```bash
# 查看最近日志
openclaw logs --tail 100

# 查看错误日志
openclaw logs --level error
```

### 3. 安全模式

```bash
# 无插件启动
openclaw --safe-mode

# 仅加载核心插件
openclaw --minimal
```

---

## 📝 版本兼容性

| OpenClaw 版本 | Node.js | Windows | WSL2 | 备注 |
|---------------|---------|---------|------|------|
| 2026.4.8 | >= 18.0.0 | ⚠️ 有闪退 | ✅ 稳定 | 推荐使用 WSL2 |
| 2026.4.5 | >= 18.0.0 | ✅ 稳定 | ✅ 稳定 | 最后稳定版 |
| 2026.3.x | >= 16.0.0 | ✅ 稳定 | ✅ 稳定 | 旧版 |

---

## 🆘 紧急恢复

### 完全重置

```bash
# 1. 卸载 OpenClaw
npm uninstall -g openclaw

# 2. 清理配置
rm -rf ~/.openclaw

# 3. 清理缓存
npm cache clean --force

# 4. 重新安装
npm install -g openclaw@2026.4.5

# 5. 初始化
openclaw init
```

### 回退到稳定版

```bash
npm install -g openclaw@2026.4.5
```

---

## 📚 相关资源

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [WSL2 安装指南](https://docs.microsoft.com/windows/wsl/install)
- [Node.js 下载](https://nodejs.org/)
- [问题反馈](https://github.com/openclaw/openclaw/issues)

---

## 📊 版本历史

### v1.0.0 (2026-04-09)
- ✅ Windows 升级排障完整指南
- ✅ WSL vs Windows 对比
- ✅ v2.0 微信升级路径
- ✅ 紧急恢复方案

---

**最后更新**: 2026-04-09  
**作者**: 郑宇航
