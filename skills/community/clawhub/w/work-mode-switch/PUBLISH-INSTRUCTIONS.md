# ClawHub 发布指南 / ClawHub Publishing Guide

---

## 📦 待发布技能 / Skills to Publish

### 1. work-mode-switch (v1.0.0)

**说明 / Description:** SuperMike 工作模式切换技能 - 12 种工作模式

**文件已准备 / Files Ready:**
- ✅ SKILL.md (中英双语详细说明)
- ✅ package.json (包元数据)
- ✅ README.md (使用说明)

**敏感信息检查 / Sensitive Data Check:**
- ✅ 无 API Key
- ✅ 无密码
- ✅ 无个人身份信息
- ✅ 无内部路径

---

## 🚀 发布步骤 / Publishing Steps

### 方式 1: 手动发布（推荐）/ Manual Publish (Recommended)

**在 PowerShell 中执行 / Run in PowerShell:**

```powershell
# 1. 确认登录状态 / Check login status
clawhub whoami

# 2. 如未登录，先登录 / If not logged in, login first
clawhub login

# 3. 发布技能 / Publish skill
clawhub publish D:\Personal\OpenClaw\skills\work-mode-switch
```

**预期输出 / Expected Output:**
```
✓ Publishing work-mode-switch@1.0.0...
✓ Published successfully!
🔗 https://clawhub.ai/skills/work-mode-switch
```

---

### 方式 2: 批量发布（如有多个技能）/ Batch Publish

```powershell
# 扫描并发布所有新技能 / Scan and publish all new skills
clawhub sync D:\Personal\OpenClaw\skills
```

---

## ✅ 发布前检查清单 / Pre-publish Checklist

| 检查项 / Item | 状态 / Status |
|--------------|--------------|
| SKILL.md 存在 | ✅ |
| package.json 存在 | ✅ |
| README.md 存在 | ✅ |
| 无敏感信息 | ✅ |
| 描述清晰 | ✅ |
| 许可证明确 | ✅ (MIT) |
| 版本正确 | ✅ (1.0.0) |

---

## 📝 发布后验证 / Post-publish Verification

**访问技能页面 / Visit Skill Page:**
```
https://clawhub.ai/skills/work-mode-switch
```

**测试安装 / Test Installation:**
```powershell
clawhub install work-mode-switch
```

---

## 🎯 发布说明 / Release Notes

**版本 / Version:** 1.0.0  
**发布日期 / Release Date:** 2026-03-31  
**作者 / Author:** SuperMike  
**许可证 / License:** MIT

**更新内容 / What's New:**
- 12 种工作模式定义 / 12 work modes defined
- 支持灵活切换协作节奏 / Flexible collaboration mode switching
- 中英双语文档 / Bilingual documentation (CN/EN)
- 深度研究模式（6 阶段流程）/ Deep Research mode (6-stage process)
- 自检模式（系统健康检查）/ Self-Check mode (system health check)
- 自学模式（独立学习提升）/ Self-Learn mode (independent learning)

---

## 📞 问题排查 / Troubleshooting

### 问题 / Issue: "Not logged in"

**解决方案 / Solution:**
```powershell
clawhub login
# 浏览器会打开认证页面 / Browser will open auth page
# 完成登录后重试 / Retry after login
```

### 问题 / Issue: "Skill already exists"

**解决方案 / Solution:**
```powershell
# 更新版本后发布 / Update version and publish
# 修改 package.json 中的 version 字段 / Update version in package.json
clawhub publish D:\Personal\OpenClaw\skills\work-mode-switch
```

---

_创建日期 / Created: 2026-03-31_  
_用途 / Purpose: ClawHub 技能发布指南_
