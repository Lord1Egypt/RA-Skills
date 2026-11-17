# 最佳实践达标清单（12 条核心检查）

> 本文是达标检查的唯一运行面清单。它不替用户做“全面治理”，只检查会直接影响 skill 使用效率的 12 个行为/底座事实。
> A 层由 `scripts/usage_diag.py` 读取事实；B/C 层由 agent 在会话内观察或询问。结果只表达「达标 / 未达标 / 不适用」，不合成成熟度等级。
> 完整说明在 `checklist-details.md`，仅对未达标项按需加载；旧的扩展审计材料属于作者维护资料，不作为运行面要求。

## 用户级别加载

| 用户级别 | 加载范围 | 条数 |
|----------|----------|------|
| `beginner` 初级 | L1 | 3 |
| `intermediate` 进阶 | L1+L2 | 10 |
| `advanced` 高级 | L1+L2+L3 | 12 |

## 判定流程

- A 层：直接采信 `usage_diag` 的 `checklist` 结果。
- B 层：按 domain 聚合 1–3 次 `conversation_search`，证据不足时只入队一条 `ask`。
- C 层：交互态一次询问，答案回写 `state.md`。
- 未达标：只生成最多 3 条优先动作，按 P0/P1/P2 排序，不再补“弱项分值”。

## A 层 · 底座事实

### C-mem-01 · 记忆画像是否完整 〔L1〕
- 领域：记忆
- 达标判据：`SOUL.md` 且 `USER.md` 均存在且 `chars ≥ 200`
- 检查方式：A 层确定性
- 证据来源：`usage_diag.profile`
- 改进动作：`guide` 初始化画像；确认后 `write_memory`
- 严重度：P1

### C-auto-01 · 是否有自动化在真正跑 〔L1〕
- 领域：自动化
- 达标判据：`automations.active ≥ 1`
- 检查方式：A 层确定性
- 证据来源：`usage_diag.automations`
- 改进动作：`enable_automation` 建每日检查；或按模板建立重复任务
- 严重度：P1

### C-conn-01 · 常用连接器是否已启用 〔L1〕
- 领域：连接器
- 达标判据：至少 1 个 session 的实时 `connected` 非空
- 检查方式：A 层确定性
- 证据来源：`usage_diag.connectors`
- 改进动作：`reconnect` 常用连接器；启用前先确认授权范围
- 严重度：P1

### C-skill-01 · skill 是否精简、不囤积 〔L2〕
- 领域：skill
- 达标判据：`skills.count ≤ 30`
- 检查方式：A 层确定性
- 证据来源：`usage_diag.skills`
- 改进动作：用 `skill-check-pro` 找低频项；优先关闭，不直接删除
- 严重度：P1

### C-skill-02 · 是否有 skill 生态维护入口 〔L2〕
- 领域：skill
- 达标判据：已装 `skill-check-pro` / `skill-check` 或 `skill-map`
- 检查方式：A 层确定性
- 证据来源：`usage_diag.skills`
- 改进动作：按 `toolbox.md` 的 SkillHub prompt 安装维护入口
- 严重度：P2

### C-skill-03a · SKILL.md frontmatter 是否可用 〔L2〕
- 领域：skill
- 达标判据：每个已装 `SKILL.md` 含 `name` 与 `description`
- 检查方式：A 层确定性
- 证据来源：`usage_diag.checklist`
- 改进动作：按 skill creator 规范补齐字段
- 严重度：P2

### C-skill-06 · 是否存在同 slug 重复 〔L2〕
- 领域：skill
- 达标判据：无裸 slug 与命名空间 slug 并存
- 检查方式：A 层确定性
- 证据来源：`usage_diag.checklist`
- 改进动作：保留一份并统一命名空间
- 严重度：P2

### C-auto-03 · 自动化是否真的在用 〔L2〕
- 领域：自动化
- 达标判据：ACTIVE 自动化最近运行 ≤90 天；无运行记录则未达标
- 检查方式：A 层确定性
- 证据来源：`usage_diag` runtime state
- 改进动作：保活关键自动化；把重复任务接入现有自动化
- 严重度：P2

### C-conn-02 · 连接器是否真的在用 〔L2〕
- 领域：连接器
- 达标判据：近 30 天日志有 `mcp__` 调用痕迹；无日志则不适用
- 检查方式：A 层确定性
- 证据来源：`usage_diag` 连接器调用痕迹
- 改进动作：把实际数据任务接到连接器；无需求时不强行新增连接器
- 严重度：P2

### C-mem-02 · 记忆日志是否新鲜 〔L2〕
- 领域：记忆
- 达标判据：最近日期日志距今天 ≤7 天；没有日期日志则不适用
- 检查方式：A 层确定性
- 证据来源：`usage_diag.memory_freshness`
- 改进动作：完成实质工作后写一条可复用记忆
- 严重度：P2

## B/C 层 · 真正会用

### C-prompt-01 · 提示词是否包含五要素 〔L3〕
- 领域：提示词
- 达标判据：近期任务有角色、背景、任务、格式、边界
- 检查方式：B 层启发式；证据不足时 C 层自评
- 证据来源：近期对话
- 改进动作：用五要素模板重写下一条真实任务
- 严重度：P2

### C-work-01 · 长任务是否拆解并留检查点 〔L3〕
- 领域：工作流
- 达标判据：长任务有明确子任务、验收点或可恢复检查点
- 检查方式：B 层启发式；证据不足时 C 层自评
- 证据来源：近期任务轨迹
- 改进动作：先输出任务清单，再逐项执行和验收
- 严重度：P2
