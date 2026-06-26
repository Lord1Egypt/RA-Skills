# 学习记录模板

学习记录模板，说明状态定义和技能提取字段。

## 状态定义

| 状态 | 含义 |
|------|------|
| `pending` | 未处理 |
| `in_progress` | 正在处理 |
| `resolved` | 已解决或知识已集成 |
| `wont_fix` | 决定不处理（原因在解决方案中） |
| `promoted` | 提升到 SOUL.md、AGENTS.md 或 TOOLS.md |
| `promoted_to_skill` | 提取为可重用技能 |

## 技能提取字段

当学习被提升为技能时，添加这些字段：

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

示例：
```markdown
## [LRN-20260326-001] best_practice

- Agent: agent1
- Logged: 2026-03-26T10:00:00+08:00
- Priority: high
- Status: promoted_to_skill
- Skill-Path: skills/docker-m1-fixes
- Area: infra

### 摘要
Docker 构建在 Apple Silicon 上因平台不匹配而失败

### 详情
...

### 建议行动
...
```

## 类别

**类别**：correction | insight | knowledge_gap | best_practice

**区域**：frontend | backend | infra | tests | docs | config

## 提升决策树

```
学习是否项目特定？
├── 是 → 保留在 .learnings/
└── 否 → 是否与行为/风格相关？
    ├── 是 → 提升到 SOUL.md
    └── 否 → 是否与工具相关？
        ├── 是 → 提升到 TOOLS.md
        └── 否 → 提升到 AGENTS.md（工作流）
```
