# Skill Publish

审计、清理并发布 Agent Skill 到 ClawHub 和 GitHub。适用于 OpenClaw 生态中任何基于 SKILL.md 的 skill。

与 `skill-design-guide`（设计阶段）配合。

**版本**: v1.0.1（2026-06-06）

## 模式

| 模式 | 触发词 | 说明 |
|------|--------|------|
| **审计** | "检查发布" / "audit skill" | 只扫描报告问题，不改动文件 |
| **发布** | "发布 skill" / "publish skill" | 全流程：审计 → 清理 → 推送 → 验证 |

## 检查项

1. **个人数据** — 持仓数量、成本价、账户金额、个人姓名
2. **Frontmatter** — 描述长度、语言、名称中的版本号
3. **内容** — 内部开发备注、参考章节、版本历史
4. **语言** — SKILL.md 英文主体、README 中英双语
5. **文件** — 个股脚本、元文档、过期文件

## 快速开始

```
# 审计一个 skill 目录
"检查发布 ~/.workbuddy/skills/my-skill"

# 发布到 ClawHub + GitHub
"发布 skill ~/.workbuddy/skills/my-skill@1.2.0"
```

## License

MIT
