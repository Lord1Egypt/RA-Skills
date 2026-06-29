## Teardown Protocol：Agent 生命周期释放协议

> **当职业球队里某位球员已经打完自己那场比赛，你必须让他退场。继续让他站在场上只会拖垮全队节奏。**
> — 猪八戒留任测试推论

紧箍咒之前的协议只覆盖 agent 生命周期的前 4 步（Define → Dispatch → Monitor → Accept），缺后 3 步（**Release → Cleanup → Orphan handling**）。

## 生命周期 7 阶段对照

| #     | 阶段                | 标准协议           | 以前                       | 现在          |
| ----- | ------------------- | ------------------ | -------------------------- | ------------- |
| 1     | Define              | Task Prompt 六要素 | ✅ role-guanyin-pro 阶段二 | 不变          |
| 2     | Dispatch            | dispatch_task      | ✅ task                    | 不变          |
| 3     | Monitor             | 轮询 / 验收结果    | ✅ role-guanyin-pro 阶段三 | 不变          |
| 4     | Accept              | P8/P9 验收         | ✅ role-guanyin-pro 阶段四 | 不变          |
| **5** | **Release**         | 显式释放信号       | ❌ 无                      | 本文 §Release |
| **6** | **Cleanup**         | 清理活跃记录       | ❌ 无                      | 本文 §Cleanup |
| **7** | **Orphan handling** | 孤儿检测 + 回收    | ❌ 无                      | 本文 §Orphan  |

---

## §Release / Cleanup / Orphan（生命周期阶段 5-7）

| #   | 阶段    | 核心规则                                                                              |
| --- | ------- | ------------------------------------------------------------------------------------- |
| 5   | Release | P9 验收后必须发 `[TEARDOWN]` 或 `[REASSIGN]`，不可静默挂起；P10 换届级联 teardown     |
| 6   | Cleanup | 每次 teardown 后 `harness-engine.py cleanup <id>`，移除活跃记录 + 写入 teardown.jsonl |
| 7   | Orphan  | TTL=30min 自动巡检；`/pua:reap-orphans` 手动扫描回收；禁递归派发                      |

> 完整规则（R1-R6 的 WHY/HOW、命令格式、JSON 日志 schema）→ [`references/lifecycle-protocol.md`](references/lifecycle-protocol.md)

---

## §Switches — 开关语义映射

紧箍咒的 slash 命令在本协议下的生命周期语义：

| 命令                   | 原语义       | 扩展后语义            | 映射操作                      |
| ---------------------- | ------------ | --------------------- | ----------------------------- |
| `/pua:on`              | 打开默认加载 | 不变                  | config: always_on=true        |
| `/pua:off`             | 关闭默认加载 | **+ 级联 teardown**   | off → teardown-all            |
| `/pua:cancel-pua-loop` | 清理循环状态 | **+ 原子级联清理**    | cleanup state + active-agents |
| `/pua:team-status` 🆕  | —            | 列活跃 agent / TTL    | 读 active-agents.json         |
| `/pua:reap-orphans` 🆕 | —            | 扫 stale agent 并回收 | age > 30min 批量回收          |
| `/pua:teardown-all` 🆕 | —            | 级联释放 P10→P9→P8→P7 | 发 TEARDOWN-CASCADE 到所有层  |

**设计原则**：

- **幂等**：重复执行同一开关不会产生副作用
- **级联**：顶层开关触发底层清理，反向不允许（P7 不能 teardown P8）
- **可观测**：所有 teardown 写 `data/teardown.jsonl`，便于复盘

---

## §自治 — 自动启动场景

紧箍咒是 `default=true` 自动加载的，不能假设用户会主动清理。核心自治依赖：

| 场景                                | 自治行为                                                    | 实际落地                                                                                             |
| ----------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 技能加载时                          | 初始化 / 加载进化基线                                       | ✅ `python scripts/evolution-engine.py init`（首次）或 `load`                                        |
| 技能加载时                          | 扫 stale active agent，提示确认回收                         | ✅ `python scripts/harness-engine.py status`（非 evolution-engine status）                           |
| 每次工具调用后                      | 自检 active-agents 并清点 stale                             | ✅ `python scripts/harness-engine.py status`                                                         |
| `[紧箍咒生效 🔥]` 标记时            | 追踪主动行为并写入分类                                      | ✅ `python scripts/evolution-engine.py track <behavior> <category>`                                  |
| 方法论沉淀时                        | 记录项目级记忆 / 反模式                                     | ✅ `python scripts/evolution-engine.py add-memory <key> <value>` / `add-antipattern <trap> <lesson>` |
| 主要任务完成时                      | 基线比对与进化统计刷新                                      | ✅ `python scripts/evolution-engine.py complete`                                                     |
| 每次 complete 后                    | session 块自动裁剪（保留最近 30 个）                        | ✅ `_prune_sessions(keep=30)` 内嵌                                                                   |
| 每次 report/failure-detector 写入后 | error_history.jsonl 自动裁剪（保留最近 50 条）              | ✅ `prune_history(keep=50)` 内嵌                                                                     |
| 每次 cleanup/feedback 写入后        | teardown.jsonl + feedback.jsonl 自动裁剪（保留最近 200 条） | ✅ `cmd_prune_logs(keep=200)` 内嵌                                                                   |
| 子 agent 完成时                     | 写 teardown.jsonl + 从 active-agents.json 移除              | ✅ `python scripts/harness-engine.py cleanup <agent_id> <reason>`                                    |
| 级联关闭                            | 一次性释放所有活跃 agent                                    | ✅ `python scripts/harness-engine.py teardown-all [reason]`                                          |

---

## 验收

本协议落地的判定标准：

- ✅ `teardown` / `释放` / `回收` 在 role-guanyin-pro 阶段四后出现 ≥ 3 次
- ✅ `harness-engine.py gate` 存在并实现 gate 子命令
- ✅ `/pua:team-status`、`/pua:reap-orphans`、`/pua:teardown-all` 已在 `references/platform-commands.md` 中定义
- ✅ `data/teardown.jsonl` 可写且有 schema

_（内容由AI生成，仅供参考）_
