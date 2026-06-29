---
name: verifyguard
description: "AI 产出预检工具。发布博客/提交任务前自动检查：内容完整性、链接可用性、敏感信息泄露、格式合规。受 Claude Code Verify 设计模式启发，完全原创实现，使用 Python + requests。"
metadata:
  openclaw:
    emoji: "✅"
    requires:
      bins: [python3]
---

# OpenClaw Verify ✅

> 设计灵感来自 Claude Code 的独立验证视角（VerificationAgent），
> 但实现完全原创——不涉及任何泄露代码。

## 使用方式

```bash
# 检查 Markdown 文件
python3 {{SKILL_DIR}}/scripts/verify.py check path/to/article.md

# 检查 URL 链接
python3 {{SKILL_DIR}}/scripts/verify.py links path/to/article.md

# 检查敏感信息
python3 {{SKILL_DIR}}/scripts/verify.py secrets path/to/article.md

# 全量检查
python3 {{SKILL_DIR}}/scripts/verify.py all path/to/article.md
```

## 检查维度

| 维度 | 检查内容 | 严重级别 |
|------|---------|---------|
| 🔒 安全 | 密钥、Token、密码、内网IP | CRITICAL |
| 🔗 链接 | URL 可达性、格式正确 | WARNING |
| 📋 完整 | 未完成标记(TODO/FIXME)、截断内容 | ERROR |
| 📐 格式 | Markdown 语法、编码问题 | WARNING |
