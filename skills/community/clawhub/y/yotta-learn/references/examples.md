# 遗留 `.learnings` 字段与示例

> 新知识不再写 `.learnings/`（见 SKILL.md「使用模型」）；本文仅用于读取、处置与迁移旧条目。知识库条目的写入与核验见 `kb.md`。

## 字段

| 字段 | 说明 | 示例 |
|---|---|---|
| Logged | 记录时间（ISO 8601 带时区） | 2026-08-26T10:00:00+08:00 |
| Priority | low / medium / high / critical | high |
| Status | pending / in_progress / resolved / wont_fix / promoted / promoted_to_skill | pending |
| Area | 所属领域（自由填写，便于过滤） | git |
| Pattern-Key | 复发模式标识（相同问题用同一 key 聚合） | push-gate |

## 示例条目

```markdown
## [LRN-20260826-001] correction

**Logged**: 2026-08-26T10:00:00+08:00
**Priority**: high
**Status**: pending
**Area**: git
**Pattern-Key**: push-gate

### Summary
推送前必须先跑测试并核对输出

### Details
第一次直接推被拒；先本地验证再推成功。以后默认先验证。
```

## 不记录什么

- 私钥、令牌、环境变量值、完整凭据（除非用户明确要求）；
- 完整的源码或配置文件；
- 与工作无关的个人信息。
