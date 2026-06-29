# 生命周期协议：§Release · §Cleanup · §Orphan

> 由 SKILL.md 引用。定义 agent 生命周期的阶段 5-7（释放、清理、孤儿回收）的完整协议。

## 生命周期 7 阶段对照

| # | 阶段 | 操作 | 协议来源 | 补全 |
|---|------|------|---------|------|
| 1 | Setup | dispatch_task 参数 | ✅ Marvis 内置 | 不变 |
| 2 | Dispatch | dispatch_task | ✅ task | 不变 |
| 3 | Monitor | 轮询 / 验收结果 | ✅ role-guanyin-pro 阶段三 | 不变 |
| 4 | Accept | P8/P9 验收 | ✅ role-guanyin-pro 阶段四 | 不变 |
| **5** | **Release** | 显式释放信号 | ❌ 无 | 本文 §Release |
| **6** | **Cleanup** | 清理活跃记录 | ❌ 无 | 本文 §Cleanup |
| **7** | **Orphan handling** | 孤儿检测 + 回收 | ❌ 无 | 本文 §Orphan |

---

## §Release — 6 条释放规则

### R1. P9 验收通过必须发 `[TEARDOWN]` 信号

**WHY**：验收通过 ≠ agent 释放。P9 默认会继续分配下一个任务给同一个 P8，但如果没有下一个任务，老 P8 就这样挂在那里。`[TEARDOWN]` 是明确的"释放/退场"指令。

**HOW**：P9 在验收旁白后，追加一行：

```
[TEARDOWN] p8-backend | reason: all_tasks_completed | release_resources: true
```

若还有下一轮任务：

```
[REASSIGN] p8-backend | next_task: <task_id> | keep_agent: true
```

二选一必须显式，不允许默认静默。

### R2. P10 换届强制 teardown 整个 P9 团队

**WHY**：P9 切换（/pua:p9 → 不同项目）时，旧 P9 管理的 P8 全部成了孤儿——没有老板会来验收它们的交付。

**HOW**：P10 下发换届指令时必须级联：

```
[TEARDOWN-CASCADE] p9-current | descendants: [p8-backend, p8-frontend, p7-*] | reason: p9_rotation
```

### R3. agent 完成后必须从活跃记录移除

**WHY**：dispatch_task 返回后，子 agent 的完成状态需要显式登记，否则无法回答"当前还有多少 agent 在场上"。

**HOW**：P8/P9 收到子 agent 的验收结果后，从 `data/active-agents.json` 中移除对应 agent 记录：

```bash
python scripts/harness-engine.py cleanup <agent_id> <reason>
```

harness-engine.py 同时将释放事件写入 `data/teardown.jsonl`。

### R4. background agent 默认 TTL = 30min

**WHY**：dispatch_task 派发的 agent 如果不主动回收，会一直占据上下文预算。

**HOW**：派发时记录 `agent_id` 和 `dispatch_time` 到 `data/active-agents.json`（文件首次写入时自动创建，格式 `{"agents": []}`）。超过 30min 未完成 → 标记为 orphan，`/pua:reap-orphans` 或自动巡检时回收。

### R5. subagent 禁止递归派发（禁嵌套孤儿）

**WHY**：subagent 自己再 dispatch_task 后，上级 agent 完全看不见这些深层的 agent。一旦 subagent 退出，深层 agent 就彻底失联。

**HOW**：P8 被 P9 dispatch_task 后，**只能**用 dispatch_task 派发 P7，**不能**再让 P7 继续 dispatch_task。P9 级别才允许跨层管理。违规的递归派发被发现后由 P9 强制回收。

### R6. Teardown 日志必须可写

**WHY**：所有 teardown 事件写入 `data/teardown.jsonl`，便于复盘"谁在什么时候因为什么原因被释放"。

**HOW**：harness-engine.py cleanup 子命令自动追加 JSON 行。手动释放时追加格式：

```json
{"agent":"<id>","reason":"<reason>","ts":"<ISO8601>"}
```

---

## §Cleanup — 主动清理 checklist

每次 `[TEARDOWN]` 触发后执行：

```bash
# 通过 harness-engine.py 统一清理
python scripts/harness-engine.py cleanup <agent_id> <reason>
```

该命令自动完成：
1. 从 `data/active-agents.json` 移除 agent 记录
2. 清理 state 文件：`data/agent-<id>.state`
3. 记录到 `data/teardown.jsonl`

---

## §Orphan — 孤儿检测与回收

**什么是孤儿**：
- state 文件 mtime > 30 分钟且无对应验收结果
- active-agents.json 中存在但主会话已无对应 dispatch_task 引用

**两层防御**：

1. **自动巡检**：每次工具调用后 P8 自检 `python scripts/harness-engine.py status`，stale 的自动提示
2. **用户显式**（手动）：`/pua:reap-orphans` 一键扫描 + 回收
