# Memory Orchestrator v2 — Runtime Protocol

## 1. Session start protocol
每次会话开始或任务切换时，按这个顺序：
1. 读 `SESSION-STATE.md`
2. 判断当前热态是否过时：
   - 任务已完成但未清理
   - blocker 已消失但未更新
   - pending actions 与当前目标不一致
3. 如有必要，先修正 hot state
4. 若任务与历史相关，再用 `memory_search`
5. 只在需要时再读具体 `memory/*.md`

## 2. In-task protocol
以下事件发生时，应优先更新 `SESSION-STATE.md`：
- 开始一个明确的多步骤任务
- 当前目标发生变化
- 出现真实 blocker
- 出现新的关键决策
- 需要 handoff / 抗 compaction 时

热态写入要求：
- 只写当前态
- 不写长篇历史
- 写完再继续回复或执行

## 3. Task closeout protocol
任务结束或阶段完成时，按顺序判断：
1. 哪些内容只属于当前态？→ 从 `SESSION-STATE.md` 清掉或重置
2. 哪些值得留存为当日记录？→ 写入 `memory/YYYY-MM-DD.md`
3. 哪些已经稳定？→ 升格到 `preferences/system/projects/MEMORY`
4. 哪些是 recurring issue？→ 提权到 enforcement layer
5. 是否需要给旧 daily 增加“已收敛/已迁移/已失效”说明？

## 4. Promotion guide
- preference → `memory/preferences.md`
- environment fact / endpoint / constraint → `memory/system.md`
- project status / decision → `memory/projects.md`
- cross-cutting stable rule → `memory/MEMORY.md`
- every-session high-value summary → root `MEMORY.md`
- repeated annoyance / behavior fix → `SOUL.md` / `AGENTS.md` / `TOOLS.md`

## 5. Hot state discipline
`SESSION-STATE.md` 允许为空，但不允许长期失真。

至少在这些时点更新：
- 复杂任务开工前
- blocker 出现时
- blocker 消失时
- 决策发生变化时
- 任务收尾时

## 6. Hygiene execution rules
定期巡检时，重点检查：
- `SESSION-STATE.md` 是否陈旧
- root `MEMORY.md` 是否膨胀
- daily 是否存在应升格未升格内容
- structured long-term 是否存在过时事实
- `.learnings/` 是否漂移回主账本角色
- recall/reference 文档是否仍指向旧体系

## 7. Minimal reliability rule
如果一个记忆动作没做完，不要只说“已保存/已同步”。
真正的完成标准是：
- 目标文件已更新
- 路由层级正确
- 若需要提权，也已同步更新 enforcing layer
