# 提升机制说明

## 何时提升

当学习广泛适用（不是一次性修复）时，提升到 SOUL.md。

### 提升条件

- 学习适用于多个文件/功能
- 任何贡献者（人类或 AI）都应该知道的知识
- 防止重复错误
- 记录项目特定的约定

## 自动提升规则

### 规则 A：重复 >= 3 次（自动）

**触发条件（每日 00:00 自动执行）：**
- 按 `Pattern-Key` 累计 `Recurrence-Count`
- 累计次数 >= 3 时触发提升

**自动操作：**
1. 提取 `### 摘要` 和 `### 建议行动`
2. 根据 `Area` 字段映射到对应的二级标题
3. 生成规则写入 `SOUL.md`
4. 更新原始记录：
   - `Status: promoted`
   - `Promoted: SOUL.md`
   - `Promoted-By: <agent_id>`

**提升格式：**
```markdown
### 一句话总结
一句话建议行动

---
```

**Area 映射规则：**
- `行为准则`|`行为模式`|`交互规范` → `## Core Truths（核心准则）`
- `工作流`|`工作流改进`|`任务分发` → `## 工作流程`
- `工具`|`配置`|`工具问题` → `## 工具使用`
- `边界`|`安全` → `## Boundaries（边界）`
- `风格`|`气质` → `## Vibe（风格气质）`
- `连续性`|`偏好` → `## Continuity（连续性）`
- 其他 → `## 其他`

**重要说明：**
- ✅ 所有 agent 的记录合并统计
- ✅ 按 `Pattern-Key` 累计 `Recurrence-Count`
- ✅ 共享目录：所有使用共享目录的智能体都提升
- ✅ 独立目录：对应智能体提升到自己的 SOUL.md

### 规则 B：高优先级（自动）

**触发条件：** `Priority: critical`

**自动操作：**
1. 立即提升到 SOUL.md
2. 标记为 `promoted`
3. 添加 `Promoted-By: <agent_id>`

### 规则 C：工作流/工具问题（自动）

**触发条件：** `Priority: high` 且 `Area: infra | config | tools`

**自动操作：**
1. 提升到 SOUL.md
2. 标记为 `promoted`
3. 添加 `Promoted-By: <agent_id>`

## 多 Agent 统计

### 统计逻辑

- 按 `Pattern-Key` 累计所有 agent 的 `Recurrence-Count`
- 累计次数 >= 3 时自动提升到 SOUL.md
- 不区分 agent，只看累计次数

### 示例

```markdown
## [ERR-20260326-001] git_push_without_pull
- Agent: agent1
- Pattern-Key: git.push.without.pull
- Recurrence-Count: 1

## [ERR-20260327-001] git_push_without_pull
- Agent: agent2
- Pattern-Key: git.push.without.pull
- Recurrence-Count: 1

## [ERR-20260328-001] git_push_without_pull
- Agent: agent3
- Pattern-Key: git.push.without.pull
- Recurrence-Count: 1
```

统计结果：`git.push.without.pull` 累计次数：3 → 触发自动提升

## 提升决策树

```
学习是否项目特定？
├── 是 → 保留在 .learnings/
└── 否 → 提升到 SOUL.md
```
