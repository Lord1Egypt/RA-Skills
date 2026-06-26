# 用量监控 Skill v2.0 - 用户自定义配置指南

## 🎯 核心改进

### v1.0 vs v2.0 对比

| 功能 | v1.0 | v2.0 |
|------|------|------|
| 面板 URL | 硬编码（固定） | ✅ **用户自定义** |
| 告警阈值 | 硬编码 80% | ✅ **用户自定义 (1-100)** |
| 服务名称 | 硬编码 | ✅ **用户自定义** |
| 检查频率 | 固定 | ✅ **用户自定义** |
| 配置方式 | TOOLS.md | ✅ **独立 config.json** |

## 📝 用户需要填写什么？

用户只需填写 **2 个必填参数**：

### 1️⃣ panelUrl（必填）

**从哪里获取：**
1. 打开你的用量/配额面板页面（如：OpenClaw Token 数量面板、云服务用量页等）
2. **复制浏览器地址栏的完整 URL**

**示例：**
```json
{
  "panelUrl": "https://platform.example.com/token/quota"
}
```

**注意：** 每个用户的 URL 可能不同（包含用户特定的参数），所以必须由用户自己提供。

### 2️⃣ alertThreshold（必填）

**设置你的告警阈值百分比（1-100 的整数）**

**示例：**
```json
{
  "alertThreshold": 50   // 50% 时告警（保守）
}
```

```json
{
  "alertThreshold": 80   // 80% 时告警（推荐）
}
```

```json
{
  "alertThreshold": 95   // 95% 时告警（宽松）
}
```

## 📋 完整配置示例

### 最小配置（仅必填项）

```json
{
  "panelUrl": "你的用量面板页面 URL",
  "alertThreshold": 80
}
```

### 推荐配置（包含可选参数）

```json
{
  "panelUrl": "https://platform.example.com/token/quota",
  "alertThreshold": 80,
  "serviceName": "OpenClaw Token",
  "checkIntervalHours": 4,
  "remainingDays": 30
}
```

## 🔧 安装步骤

### 步骤 1：复制 Skill

```bash
# Windows PowerShell
Copy-Item -Recurse "D:\openclaw_self_skill\usage-monitor" "$env:USERPROFILE\.openclaw\workspace\skills\"
```

### 步骤 2：创建配置

```bash
cd skills/usage-monitor
copy config.example.json config.json
```

### 步骤 3：编辑配置

用文本编辑器打开 `config.json`，填写：

```json
{
  "panelUrl": "从这里粘贴你的 URL",
  "alertThreshold": 80
}
```

### 步骤 4：测试运行

```bash
node check.js
```

看到 `✅ 配置加载成功！` 即表示配置正确。

## ❓ 常见问题

### Q: 为什么 URL 不能固定？

**A:** 用量面板的 URL 可能包含用户特定的参数（如工作区 ID、地域等），每个用户的 URL 都不同。硬编码会导致其他用户无法使用。

### Q: 阈值为什么让用户自己设置？

**A:** 不同用户有不同的使用习惯：
- 保守型用户希望 50% 就告警
- 标准用户希望 80% 告警
- 宽松用户希望 90% 以上再告警

让用户自己选择更灵活。

### Q: 配置错了怎么办？

**A:** 直接编辑 `config.json`，保存后下次运行自动生效。脚本会自动验证配置格式。

### Q: 可以多人共用这个 Skill 吗？

**A:** 可以！Skill 本身（check.js 等）是通用的，每个人只需创建自己的 `config.json` 填写个人配置即可。

## 🔒 隐私保护

- ✅ `config.json` 包含个人 URL，**不要分享给他人**
- ✅ `usage-log.md` 包含用量数据，**不要上传到公开仓库**
- ✅ Skill 代码（check.js 等）可以安全分享
- ✅ `.gitignore` 已配置，自动忽略敏感文件

## 📁 文件说明

| 文件 | 是否包含个人信息 | 是否可以分享 |
|------|-----------------|-------------|
| `check.js` | ❌ 否 | ✅ 可以 |
| `SKILL.md` | ❌ 否 | ✅ 可以 |
| `README.md` | ❌ 否 | ✅ 可以 |
| `config.example.json` | ❌ 否（模板） | ✅ 可以 |
| `config.json` | ✅ 是（用户创建） | ❌ 不要分享 |
| `usage-log.md` | ✅ 是（运行时创建） | ❌ 不要分享 |

## 🎯 适用场景

本 Skill 可用于监控任何有用量/配额面板的服务：

- ✅ OpenClaw Token 数量监控
- ✅ 云服务用量监控（阿里云、AWS、腾讯云等）
- ✅ API 调用配额监控
- ✅ 资源包用量监控
- ✅ 订阅套餐用量监控
- ✅ 任何有用量百分比显示的面板

---

**版本：** 2.0.0  
**更新日期：** 2026-03-15
