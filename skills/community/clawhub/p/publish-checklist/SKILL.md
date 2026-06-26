---
name: publish-checklist
description: 对外发布前审查清单。发布 ClawHub skill、提交 GitHub PR/Issue、发帖、发邮件、任何公开内容前必须加载此 skill 并逐项检查。
metadata:
  openclaw:
    emoji: "✅"
    category: "workflow"
    tags: ["publish", "review", "checklist", "security", "privacy"]
---

# 对外发布前审查

发布前必须逐项检查，不能跳过。

## 隐私

- [ ] 无用户名、路径、IP、API key、token、内部配置泄露
- [ ] 无仅属于内部的逻辑或人设（如 ram-review 教训）

## 安全性（面向社区审查）

- [ ] 默认行为无害（不带显式参数不执行危险操作）
- [ ] 危险操作需要显式 opt-in（如 `--kill`、`--force`）
- [ ] 权限要求最小化（不需要 root 除非必须）
- [ ] 有审计日志（操作可追溯）
- [ ] 输入校验到位（恶意参数不会造成破坏）
- [ ] 安全设计在文档中透明可见（审查者能快速理解保护机制）

## 扩展性

- [ ] 跨平台支持状态在文档中写清楚（支持/不支持/计划中）
- [ ] 硬编码值已参数化（路径、阈值等可配置）
- [ ] 扩展点预留（新增支持不需要改核心逻辑）

## 公开内容安全

- 提交 PR/Issue 用双语（中英文）
- 不暴露高权限信息（API Key、scope 数量等）
- 推代码前检查：格式化 + TS 类型
- 不用 Python 字符串拼接生成 TS 代码（转义问题），用 heredoc 或 sed
