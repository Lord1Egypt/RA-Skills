---
name: self-improving-agent
description: "记录错误、纠正、能力缺口与最佳实践，形成可复用的持续改进闭环。适用于：命令失败、用户纠正、外部 API/工具异常、发现更优做法、提出新能力需求，以及任务前复盘历史经验。"
---

# Self-Improving Agent（自我改进）

把“踩坑”变成“资产”。
每次失败、纠正或新发现，都写入结构化记录，后续可检索、可复盘、可沉淀到长期规则。

---

## 1. 什么时候必须记录

出现以下任一情况时，立即记录：

1. **命令/操作失败**（非 0 退出、超时、异常输出）
2. **用户纠正你**（“不对”“应该是…”）
3. **用户提出你当前不具备的能力**
4. **外部服务失败**（API 报错、限流、鉴权失败）
5. **你意识到知识已过时或理解错误**
6. **你发现了可复用的更优流程**

---

## 2. 记录到哪里

在工作区使用 `.learnings/`：

- `.learnings/LEARNINGS.md`：纠正、认知缺口、最佳实践
- `.learnings/ERRORS.md`：失败与异常
- `.learnings/FEATURE_REQUESTS.md`：能力请求

若目录不存在，先创建：

```bash
mkdir -p .learnings
```

---

## 3. 快速分流规则

- **失败/报错** → `ERRORS.md`
- **被纠正/学到新规则** → `LEARNINGS.md`
- **想要但暂不支持的能力** → `FEATURE_REQUESTS.md`

---

## 4. ID 规范

格式：`TYPE-YYYYMMDD-XXX`

- TYPE: `LRN` / `ERR` / `FEAT`
- 日期：当天日期
- XXX：三位序号（如 `001`）

示例：
- `LRN-20260308-001`
- `ERR-20260308-002`
- `FEAT-20260308-001`

---

## 5. 模板（请严格使用）

### 5.1 Learning 模板（LEARNINGS.md）

```markdown
## [LRN-YYYYMMDD-XXX] correction | knowledge_gap | best_practice

**Logged**: ISO-8601 时间
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
一句话总结

### Details
发生了什么、哪里错了、正确做法是什么

### Suggested Action
下一次应执行的具体动作

### Metadata
- Source: conversation | error | user_feedback | simplify-and-harden
- Related Files: path/to/file
- Tags: tag1, tag2
- See Also: LRN-...（可选）
- Pattern-Key: ...（可选）
- Recurrence-Count: 1（可选）
- First-Seen: YYYY-MM-DD（可选）
- Last-Seen: YYYY-MM-DD（可选）

---
```

### 5.2 Error 模板（ERRORS.md）

```markdown
## [ERR-YYYYMMDD-XXX] command_or_integration

**Logged**: ISO-8601 时间
**Priority**: medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
一句话说明失败点

### Error
```
完整报错文本
```

### Context
- 执行了什么命令/操作
- 使用了哪些参数
- 关键环境信息

### Suggested Fix
可执行的修复建议

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file
- See Also: ERR-...（可选）

---
```

### 5.3 Feature Request 模板（FEATURE_REQUESTS.md）

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 时间
**Priority**: low | medium | high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
用户希望实现什么

### User Context
用户为什么需要它

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
实现方向（脚本、工具、流程）

### Metadata
- Frequency: first_time | recurring
- Related Features: ...（可选）

---
```

---

## 6. 状态流转

允许状态：

- `pending`：待处理
- `in_progress`：处理中
- `resolved`：已解决
- `promoted`：已提升到长期规则文件
- `wont_fix`：不处理（需写原因）

当问题已解决时，补充：

```markdown
### Resolution
- **Resolved**: ISO-8601 时间
- **Commit/PR**: commit hash 或 PR 链接
- **Notes**: 做了什么
```

---

## 7. 何时“晋升”到长期记忆文件

满足以下任一条件，建议晋升：

- 同类问题重复出现
- 对多人/多任务都适用
- 不写下来就会反复踩坑

晋升目标：

- 工作流规则 → `AGENTS.md`
- 行为/表达规则 → `SOUL.md`
- 工具使用细节 → `TOOLS.md`
- 长期偏好/事实 → `MEMORY.md`

晋升后把原条目状态改为 `promoted`，并注明目标文件。

---

## 8. 复盘频率

建议在以下时机快速复盘 `.learnings/`：

- 开始新任务前
- 完成复杂任务后
- 每周至少一次

可用命令：

```bash
# 统计 pending
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# 查看高优先级
grep -B5 "Priority\*\*: high" .learnings/*.md | grep "^## \["
```

---

## 9. 执行原则（简版）

1. **立即记录**：别等会儿，信息会丢。
2. **写可执行建议**：不是“再看看”，而是“下次先做 X”。
3. **优先去重与关联**：能关联就加 `See Also`。
4. **重复三次就系统化**：提升到 `AGENTS.md/SOUL.md/TOOLS.md`。
5. **短而准**：结论可复用，描述可追溯。

---

## 10. OpenClaw 场景建议

- 在主会话中把高价值学习同步到 `MEMORY.md`。
- 在需要跨会话协作时，使用 `sessions_send` 分享关键学习。
- 对高频重复问题，优先将规则写入工作区文档，减少未来上下文成本。

> 目标不是“记日志”，而是持续降低错误率、提高可复用性。