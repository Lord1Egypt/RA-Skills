# Plan Mutation Protocol — 计划突变协议

WBS 计划确认后仍可变更，但**必须留痕**。本协议定义了 5 种突变操作及其审计要求。

---

## 铁律

1. 所有突变必须在 WBS 台账的 **Mutation Log** 中记录
2. 突变涉及依赖关系变化时，必须验证无循环依赖
3. 计划审查（adversarial review）通过后的突变，需要**重新触发审查**
4. 突变不删除原行——使用 `skipped` 状态 + 原因

---

## 5 种突变操作

### 1. Split — 拆分

**触发条件**：任务太大，一个 subagent 无法在合理时间内完成（> 30 分钟或 > 5 个文件）。

**操作**：
```
原任务 ID: 3 → 标记 skipped + 原因"拆分为 3.1 / 3.2"
新任务: 3.1, 3.2 — 继承原任务依赖，3.2 depends on 3.1
```

**Mutation Log 记录**：
| Time | Type | Affected | Reason | New IDs |
|------|------|---------|--------|---------|
| ... | split | 3 | 任务太大，涉及 8 个文件需拆分 | 3.1, 3.2 |

**后续**：3.1 和 3.2 的 Context Brief 必须各自完整。原来依赖 Task 3 的任务改为依赖 3.2。

---

### 2. Insert — 插入

**触发条件**：执行中发现遗漏了必要的前置工作（如"需要先加环境变量"）。

**操作**：
```
在 Task N 和 Task N+1 之间插入 Task N.5
```

**Mutation Log 记录**：
| Time | Type | Affected | Reason | New IDs |
|------|------|---------|--------|---------|
| ... | insert | 2→3 | 发现缺少数据库迁移脚本，需插入 | 2.5 |

**规则**：
- 插入位置前后任务的 Dependencies 更新
- 被依赖的新任务 ID 必须出现在后续任务的 Dependencies 中

---

### 3. Skip — 跳过

**触发条件**：任务已不需要（需求变更、已被其他任务覆盖、前提条件不满足）。

**操作**：
```
Task N → 标记 skipped + 原因
```

**Mutation Log 记录**：
| Time | Type | Affected | Reason | New IDs |
|------|------|---------|--------|---------|
| ... | skip | 4 | 需求变更，不再需要搜索功能 | - |

**规则**：
- 被跳过任务的依赖者（dependents）的 Dependencies 列移除被跳过的 ID
- 如果依赖者缺少必要前置，需要插入新任务或重新评估

---

### 4. Reorder — 重排

**触发条件**：发现依赖关系有误，或并行机会被遗漏。

**操作**：
```
更新任务 ID 顺序 + Dependencies 列
```

**Mutation Log 记录**：
| Time | Type | Affected | Reason | New IDs |
|------|------|---------|--------|---------|
| ... | reorder | 5,6 | Task 5 和 6 无文件冲突，可并行 | - |

**规则**：
- 重排后必须运行依赖验证（`checkpoint.sh phase-2` 会验证）
- 并行化时，在 Dependencies 列去掉不必要的依赖

---

### 5. Abandon — 废弃

**触发条件**：方向完全错误（如"不应该用 Redis，应该用 PostgreSQL"），不只是跳过。

**操作**：
```
Task N → 标记 skipped + 原因"废弃：[具体原因]"
```

**Mutation Log 记录**：
| Time | Type | Affected | Reason | New IDs |
|------|------|---------|--------|---------|
| ... | abandon | 6 | 废弃：Redis 方案改为 PostgreSQL，需新建 Task | 7(新建) |

**规则**：
- 必须注明废弃原因和替代方案
- 废弃的任务在 Delivery Summary 中列出为"已废弃"
- 如果引入替代任务，走 Insert 流程

#### Abandon 回滚指引

如果废弃了原方案、切换到新方案后失败，按以下步骤回退：

```
1. 停止当前执行
2. 检查 Mutation Log → 找到 abandon 记录 → 获取原任务 ID
3. 原任务从 skipped 改回 todo（恢复）
4. 新方案任务标记 skipped + 原因"回退：新方案失败，恢复原方案"
5. Mutation Log 记录回退操作
6. 更新所有受影响任务的 Dependencies
7. 重新运行 checkpoint.sh phase-2 验证依赖
8. 继续执行原方案
```

**铁律：abandon 不是永久删除。原任务永远保留在台账中（skipped 状态），随时可恢复。**

---

## 依赖验证（每次突变后）

```bash
./scripts/checkpoint.sh phase-2  # 重新生成 Phase 2 报告
```

人工检查：
1. 所有 Dependencies 列引用的 ID 在 WBS 中存在
2. 无循环依赖（A→B→A）
3. 无悬空依赖（引用了 skipped/abandoned 的任务）
4. 所有 `doing`/`todo` 状态的任务的依赖都已 `done`

---

## 突变后的 Context Brief 更新

任何拆分/插入产生的新任务，必须写完整的 Context Brief。突变改变了依赖关系后，下游任务的 Context Brief 中"前置产物"部分需要更新。

---

## 与对抗性审查的关系

```
原始计划 → 对抗性审查 → 通过 → 开始执行
                                ↓
                          执行中突变 → 重新触发对抗性审查
```

执行中的小突变（skip/reorder 不涉及新增任务）可以走轻量审查（agent 自检依赖链）。大突变（split/insert/abandon 引入新任务）必须重新触发完整审查。
