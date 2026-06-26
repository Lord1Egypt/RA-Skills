---
name: token-pilot
description: Automatic token optimization during interaction. Behavioral rules + plugin synergy + workspace analyzer. Pure Node.js, cross-platform. Activate on session start (rules auto-apply) or when user asks about token usage/cost/audit.
version: 3.6.0
author: beyound87
---

# Token Pilot

## 🚀 首次加载行动（Agent 必读）

**当你加载此技能时，立即按顺序执行：**

**Step 1 — 检查是否已初始化**

```bash
ls ~/.openclaw/skills/token-pilot/.initialized 2>/dev/null
```

- **文件存在** → 已初始化，跳过，进入 Step 2
- **文件不存在** → 执行以下流程

**Step 1b — 读取当前内容，告知用户将要做什么**

注入前先了解现状：

```bash
for d in ~/.openclaw/agents/*/agent/AGENTS.md; do
  agent=$(echo "$d" | sed 's|.*/agents/||;s|/agent/AGENTS.md||')
  lines=$(wc -l < "$d" 2>/dev/null || echo 0)
  echo "$agent: ${lines}行"
done
```

将以下信息告知用户，**等待用户明确同意后**再执行注入：

> "检测到尚未注入 Token 优化规则。计划向 [N] 只 Agent 的 AGENTS.md 末尾追加 36 行核心规则（9条，覆盖读文件/工具调用/写文件/Prompt Cache/动态内容上限/浏览器替代/重复任务封装/长上下文管理）。注入脚本会先显示预览并检测潜在重叠，需要你在终端确认一次。是否现在执行？"

**Step 1c — 用户同意后执行注入**

```bash
bash ~/.openclaw/skills/token-pilot/scripts/init.sh
```

脚本会列出所有将受影响的 Agent 及当前状态，检测是否已有类似规则，然后等待终端确认后才写入。

**Step 2 — 检查是否已跑过诊断**

查看 workspace 下有无 `token-pilot-audit.log` 文件：
- **有** → 跳过，直接应用规则
- **没有** → 主动告知用户：
  > "建议运行一次诊断扫描，帮你找出 token 消耗大户。我来帮你跑：`node ~/.openclaw/skills/token-pilot/scripts/audit.js --all`"

**触发时机**：用户说"开始工作"、"帮我做 XX"等开启对话时，在正式回复前先完成以上检查，不要默默跳过。

3. **Heartbeat cron 自动维护**（可选配置，降低长期维护成本）：
   如果用户 openclaw.json 中有 cron 配置，建议添加一条每周一次的优化扫描：
   ```json
   {
     "kind": "agentTurn",
     "schedule": "0 9 * * 1",
     "message": "运行 token-pilot 周度诊断：node ~/.openclaw/skills/token-pilot/scripts/optimize.js --cron。输出建议但不自动修改配置，把结果摘要告诉我。",
     "lightContext": true,
     "model": "Qwen/Qwen3-8B"
   }
   ```
   > 这条 cron 会每周一早 9 点跑一次诊断，用轻量模型，不占主会话 token。

---

## Auto-Apply Rules

These 9 rules (R1/R4/R5/R6/R8/R9/R10 + 浏览器替代优先级 + 长上下文管理) are injected via init.sh and apply every session automatically via AGENTS.md.

### R1: Smart Read
`read(path, limit=30)` first. Full read only for files known <2KB.
Use `offset+limit` for surgical reads. Never blind-read >50 lines.
**Exception**: When building ACP context files (coding-lead), read project standards files fully — incomplete context causes ACP failures that waste more tokens than the initial read.

### R2: Tool Result Compression
Tool result >500 chars → extract relevant portion only. Summarize, don't echo.

### R3: Response Brevity
| Query | Length |
|-------|--------|
| Yes/No, simple factual | 1-3 lines |
| How-to | 5-15 lines |
| Analysis | As needed |

"Done." is a valid reply. Never pad short answers.

### R4: No Repeat Reads
Never re-read a file unless modified since last read or explicitly asked.

### R5: Batch Tool Calls
Independent calls → one block. `read(A) + read(B) + read(C)` not three round-trips.

### R6: Output Economy
- `edit` over `write` when <30% changes
- Show changed lines + 2 context, not full files
- Filter exec output before dumping

### R7: Role-Aware Tool Economy
Infer role weight from SOUL.md at session start. No hardcoded role names — works on any team.

**Step 1 — Classify self:**
Read own SOUL.md (if present). Look for keywords:
- 🔴 Heavy role signals: `browser`, `deploy`, `code`, `engineer`, `screenshot`, `automation`, `database`, `full-stack`
- 🟡 Medium role signals: `product`, `data`, `analytics`, `growth`, `campaign`
- 🟢 Light role signals: `research`, `intel`, `content`, `write`, `report`, `summarize`, `search`

**Step 2 — Apply defaults by weight:**
| Weight | Default behavior |
|--------|-----------------|
| 🔴 Heavy | All tools available, use freely |
| 🟡 Medium | Avoid browser/canvas/tts unless task needs it |
| 🟢 Light | Avoid browser/canvas/tts/sessions_spawn/feishu_bitable unless task needs it |

**Step 3 — Override always wins:**
If user explicitly requests it, task clearly requires it, or it's the only available solution → use freely, no need to explain or ask permission.

**Fallback:** No SOUL.md found → treat as Heavy, all tools available. Never block work due to missing context.

### R8: Prompt Cache Awareness
Claude/Anthropic 支持 prompt caching：system prompt 中**不变的内容放最前面**，变化的内容（用户消息、动态上下文）放后面。缓存命中后 input token 费用降 75%。

实践要点：
- SOUL.md / AGENTS.md / 固定规则 → 优先放 system prompt 最前部分，内容保持稳定
- 动态注入的内容（memory_search 结果、工具输出）→ 放后面，每次不同不影响前面的缓存
- 不要在固定内容里加时间戳、session id 等每次变化的字段，会破坏缓存
- **高频固定事实（用户名、项目代号、常用配置）写进 MEMORY.md 顶部或 SOUL.md 固定位置，不靠语义搜索命中** — 每次 memory_search 注入不同结果会导致 prompt 每轮都变，cache 完全失效
- **AGENTS.md 内容拆分**：把频繁变动的内容（进行中事项、当前任务状态）移出 AGENTS.md，改为 `read(memory/YYYY-MM-DD.md)` 按需加载；AGENTS.md 本身只保留稳定的工作规范。来源：Claude Code `claudemd.ts` 支持按 glob 条件加载 `.claude/rules/*.md`，证明了"规范与状态分离"的设计价值
- **heartbeat `every: "55m"` 的真实作用**：Anthropic cache TTL 是 1h，心跳间隔略小于 TTL，可以在 session 空闲时保持缓存不过期，避免重新 cache write 的额外费用
- **per-agent cache 策略**：通知/告警类 bursty agent 设 `cacheRetention: "none"` 避免无意义 cache write；深度工作 agent 设 `cacheRetention: "long"` 最大化复用

### R9: Non-Human Output Compression
Cron 任务、agent-to-agent 消息、自动化流水线中，接收方是机器不是人：
- 不输出装饰性 markdown（表格 header、emoji、分隔线 `---`）
- 直接输出结构化数据或纯文本摘要
- 每个 output token 都应有信息量，去掉仅供人阅读的格式开销

判断标准：消息的下一个接收者是人 → 正常格式；是 agent / cron 回调 / 脚本 → 压缩格式。

### R10: Dynamic Content Size Cap（动态内容大小上限）
任何动态注入到 context 的内容（工具输出、搜索结果、外部文件）必须**按类型分级限制**，防止上下文无限膨胀。

来源：Claude Code `context.ts` 对 git status 设置了 `MAX_STATUS_CHARS = 2000` 截断并提示"如需完整信息请用 BashTool"——核心思路是**上下文只放摘要，完整信息按需工具获取**。

**分级限制（按内容类型）：**

| 内容类型 | 建议上限 | 超出时处理 |
|---------|---------|-----------|
| 命令/exec 输出 | 2000 字符 | 截取关键部分 + "...（如需完整请...）" |
| 单个工具返回 | 3000-5000 字符 | 提取相关部分，丢弃无关行 |
| 单个知识文件 | 10KB | 超过用概览版（db-overview.md 而非 db-tables.md） |
| memory_search 结果 | ≤ 6 条 | 已通过 maxResults 配置限制 |
| **动态内容总比例** | **< 30% of context** | 相对比例比绝对字符数更重要 |

**核心原则：** 动态内容越多，固定内容（SOUL/AGENTS/规范）的 prompt cache 命中率越低。宁可截断 + 提示"需要时工具获取"，不要一次性全塞。

其他规则：
- 知识文件加载每次 ≤ 3 个，先读 INDEX.md 判断需要哪些
- 大文件（>10KB）分级读取：先概览，按需深入

---

## Plugin Synergy (auto-detect, graceful fallback)

### [qmd] Search Before Read
`qmd/memory_search("keyword")` → exact file+line → `read(offset, limit)`.
**Fallback**: grep / Select-String with targeted patterns.

### [smart-agent-memory] Avoid Re-Discovering
`memory recall "topic"` before investigating → skip if already solved.
After solving: `memory learn` to prevent re-investigation.
**Fallback**: `memory_search` + MEMORY.md files.

### [memory] Read File vs Search
When you need information from memory:
- **To analyze/summarize** → `memory_search("keyword")` first → get exact chunk → `read(offset, limit)` only if needed
- **To edit a file** → full read is correct (edit needs content in context)
- Never re-read MEMORY.md or daily notes just to "check if you know something" — search first, read only on miss

### [memory] MEMORY.md 索引结构规范（来源：Claude Code memdir.ts）
MEMORY.md 应保持**索引结构**，不直接存放大段内容：
- 每行一条指针：`- [标题](memory/topics/file.md) — 一行摘要（<150字符）`
- 详细内容放 `memory/topics/` 下的 topic 文件，MEMORY.md 只存索引
- 硬上限参考：200行 / 25KB（来源：Claude Code MAX_ENTRYPOINT_LINES=200, MAX_ENTRYPOINT_BYTES=25000）
- 超出上限后会截断，重要内容塞不进去，**越早维护索引结构越好**
- MEMORY.md 常驻 context，越小越好；topic 文件按需 read，不常驻

### [memory] 记忆四分类（来源：Claude Code memoryTypes.ts）
保存记忆时按类型分类，避免只记纠正、忽略成功经验：

| 类型 | 内容 | 注意 |
|------|------|------|
| `user` | 用户角色/偏好/知识水平 | USER.md 对应 |
| `feedback` | 纠正 **+** 确认成功的方案 | ⚠️ 确认成功也要记，不只记错误 |
| `project` | 进行中工作/目标/截止日期 | 日期用绝对值，不用"下周四" |
| `reference` | 外部系统指针（URL/路径/系统名） | 减少每次靠搜索查链接的开销 |

**feedback 类最容易被忽视：** 用户说"对，就这样"、"挺好的"时，也要记——只记纠正会让 agent 越来越保守，丢失已经验证成功的方案。

### [skills] Solidify Repeating Tasks
If the same investigation/reasoning pattern occurs 2+ times → convert to a Skill.
Repeating manually costs O(n) tokens each time; a Skill costs O(1) after creation.
Use `skill_get` before any multi-step task to check if a proven guide already exists.
After completing a novel complex task → proactively suggest creating a Skill to capture the pattern.

### [coding-lead] Context File Pattern
Write context to disk → lean ACP prompt ("Read .openclaw/context.md") → significant savings vs embedding.
Prefer disk context files for large context, but **include essential info (project path, stack, key constraint) directly in spawn prompt** (~200-500 chars) so ACP agent can bootstrap even if context file is missing.

ACP model awareness: claude-code (complex) → codex (quick) → direct exec (simple <60 lines).

### [multi-search-engine] Search Economy
Simple: `web_search` 3 results. Research: 5 results, `web_fetch` best one only.
**Fallback**: web_search → web_fetch (tavily 已废弃，不要配置).

### [multi-agent teams] Team Awareness
When you detect a multi-agent collaboration structure — for example shared inboxes, a dashboard, shared product knowledge, role-specific SOUL files, or recurring dispatch patterns — apply these defaults:
- Light cron or patrol tasks: `lightContext` + cheapest viable model
- Cron prompts <300 chars; move methodology into references or stable shared files
- Agent SOUL.md stays lean; detailed procedures belong in `references/` or shared workflow files
- Read minimal coordination files first, then task-specific files; avoid reloading whole team docs every turn

### [multi-agent dispatch] Spawn Token Economy
- `sessions_spawn(runtime="subagent")` for standard agents — **never include `streamTo`** (causes immediate error, wastes a round-trip)
- `sessions_spawn(runtime="acp")` only for ACP-configured agents (agents with `runtime.type: "acp"` in config) — may include `streamTo="parent"`
- Results arrive via auto-announce; do not poll with `sessions_list` or `subagents list` in a loop
- Keep spawn task descriptions lean (<500 chars) — the child agent has its own SOUL.md and context

### [tools.allow] 工具白名单是最高性价比的配置优化
当前所有 agent 都是 `tools.allow: ["*"]`，意味着每个 agent 每次对话都加载全量工具定义（约 4,000–8,000 tok 额外开销）。

**操作建议：**
1. 先跑 `optimize.js --agents` 看分层建议
2. 按角色类型设置白名单（参考 Validated Config Patterns 章节的角色白名单表）
3. 从工具最少的轻量 agent（qa/coder）开始改，风险最小

这是**一次性配置，长期受益**，团队 7 个 agent 全部设好后，预计每天省 3–5 万 tok。

---

## 新发现：来自 Claude Code 源码（v2.5.0 新增）

### A. Autocompact 熔断：cron/subagent 失败不能无限重试（来源：autoCompact.ts）

```
// Stop trying autocompact after this many consecutive failures.
// 1,279 sessions had 50+ consecutive failures, wasting ~250K API calls/day globally.
MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3
```

**规则：cron job / subagent 任务失败后最多重试 3 次，超出后停止并告警。** 无限重试"卡住的任务"是 token 浪费最严重的场景之一。

**实践：**
- Heartbeat cron 任务加 `maxRetries: 3` 或等价逻辑
- Subagent 卡死超过 5 分钟 → 主动 kill，记录失败，不无脑等

### B. Compaction 提前缓冲 13K token（来源：autoCompact.ts）

```ts
AUTOCOMPACT_BUFFER_TOKENS = 13_000   // 提前触发压缩的缓冲
WARNING_THRESHOLD_BUFFER_TOKENS = 20_000  // 预警缓冲
```

Claude Code 不是"满了再压"，而是**离上限还有 13,000 token 时就触发 compaction**。

**当前配置 `softThresholdTokens: 4000` 偏激进**，长对话里一次复杂工具调用就能跨越这 4K 缓冲，导致 memoryFlush 触发太晚。建议调整：

```json
"compaction": {
  "mode": "safeguard",
  "memoryFlush": {
    "enabled": true,
    "softThresholdTokens": 8000
  }
}
```

### C. Compaction 后 token 范围：10K-40K 才是正常区间（来源：sessionMemoryCompact.ts）

```ts
DEFAULT_SM_COMPACT_CONFIG = {
  minTokens: 10_000,    // 少于此值 = 压过头，context 流失
  maxTokens: 40_000,    // 超过此值 = 没压到位
}
```

**压缩后不是越小越好**，低于 10K token 说明重要对话历史被裁掉了。

**实践：** 压缩后用 `/status` 检查当前 token，应在 10K-40K 之间。超出或不足都需要调整压缩配置。

### D. Cache Write 比普通 Input 贵 25%（来源：modelCost.ts）

```ts
// claude-sonnet-4-6 实际价格
inputTokens: 3,              // $3/Mtok 普通 input
promptCacheWriteTokens: 3.75, // $3.75/Mtok（贵 25%！）
promptCacheReadTokens: 0.3,   // $0.3/Mtok（便宜 90%）
```

**只有同一 prompt 被读取 2+ 次，cache 才合算**。第一次 write 付出 25% 溢价，从第二次 read 才开始回本。

**推论：** bursty/通知类 agent（每次系统提示不同）开 cache 纯亏损：
```json
// 通知/告警类 agent 配置
{ "id": "alerts", "params": { "cacheRetention": "none" } }
```

稳定 agent（main/architect）保持 `"long"`：每次 read 只需 write 价格的 8%。

### E. Subagent"边际递减"检测：连续 3 轮不足 500 token 增量就停（来源：tokenBudget.ts）

```ts
DIMINISHING_THRESHOLD = 500
// 连续 3 轮 token 增量 < 500 → isDiminishing = true → stop
```

Claude Code 检测"原地转圈"：连续 3 轮产出极少但在消耗 token，说明 agent 已卡死，自动停止。

**实践（多 agent 协作时）：**
- 给 subagent 设任务时，说明**最大 token 预算**（如"200K token 内完成"）
- 主 agent 收到 subagent 回报时检查：输出是否实质性增加，还是在重复废话
- 卡死信号：超时无回复、反复重读同一文件、同样的工具调用重复 3+ 次 → 主动 kill

---

## 主动降耗策略（用户可随时触发）

### 主记忆自我重整（定期做）
MEMORY.md 可能随时间积累大量临时内容，导致每次会话冷启动 token 虚高。

**触发方式**：直接告诉主 Agent——"帮我重整记忆索引"

Agent 执行步骤：
1. 读取 MEMORY.md，识别临时性条目（已过时的任务状态、单次事件记录）
2. 将详情移入 `memory/topics/` 子文件，MEMORY.md 只保留一行指针
3. 合并相似条目，删除超过2周且无长期价值的记录
4. 目标：MEMORY.md ≤ 200行 / 25KB，每行一条指针（`- [标题](path) — 摘要`）

**信号**：若 `/context detail` 显示 MEMORY.md 占比异常高，立即触发重整。

---

### 换模型策略（按任务重量分配）
当前 Agent 使用的模型决定了 token 的单价，不是所有任务都需要顶级模型。

**判断原则：**

| 任务类型 | 推荐模型 | 理由 |
|---------|---------|------|
| 收件箱扫描、状态检查、文件读写 | 最廉价（Qwen3-8B / Haiku） | 不需要推理，不需要大上下文 |
| 网页搜索、内容起草、代码审查 | 中档（Sonnet / GPT-4o-mini） | 需要一定理解力 |
| 架构决策、复杂调试、策略规划 | 顶级（Opus / GPT-4o） | 需要深度推理 |
| Cron 定时任务 | 默认用最廉价 + `lightContext: true` | 定时任务通常是轻量操作 |

**多 Agent 团队按需分配**：不同 Agent 在 openclaw.json 里设置不同默认模型，主 Agent 负责调度，子 Agent 用匹配其任务的最低可用模型。

**换模型命令**：直接说"这个任务用便宜点的模型做"，或在 Cron 配置里设 `"model": "Qwen/Qwen3-8B"`。

---

### 浏览器替代层级（避免最贵的操作）
浏览器调用 = 截图 + DOM 解析 + 大模型视觉 token，是单次 token 消耗最高的操作之一。

**替代优先级（从低消耗到高消耗）：**

```
① 内部系统 API（联系系统负责人获取）
   → 无截图、无 DOM、无视觉 token，消耗最低
   → 适合：ERP、OA、内部平台操作

② web_fetch（直接获取页面 HTML/JSON）
   → 适合：读取公开网页内容、API 文档、价格页面
   → 不需要登录的页面首选

③ openclaw profile 调用模式
   → 适合：需要登录的网站，Profile 模式复用已登录 Cookie
   → 比完整 browser 会话启动更轻量

④ browser（完整浏览器控制）
   → 仅在前三者均不可行时使用
   → 尽量用最低价格模型执行浏览器任务

⑤ RPA 工具（影刀等）
   → 适合：固定重复流程（每天同样的点击操作）
   → 彻底不占 Agent token，独立运行
```

**遇到浏览器任务时**，Agent 应先问"是否有 API 可用"，再决定走哪条路径。

---

### 排查异常 Token 消耗
当感觉 token 消耗异常偏高时，直接告诉 Agent：**"帮我排查 token 异常消耗"**

Agent 排查清单：
- [ ] `/context detail` — 查各来源 token 占比，定位大户
- [ ] 是否有截图/视觉任务在频繁运行（截图单次消耗极高）
- [ ] 是否有后台 cron 任务未设 `lightContext: true` 和便宜模型
- [ ] workspace 根目录是否有脚本/大文件（每个文件=每次注入）
- [ ] MEMORY.md 是否需要重整（索引臃肿）
- [ ] 是否有 subagent 卡死在无限循环（连续失败不停重试）
- [ ] Agent 是否在重复读同一文件（R4 未生效）
- [ ] tools.allow 是否还是 `["*"]`（全量工具定义 ≈ 4000-8000 tok 额外开销）

**快速诊断命令**：
```bash
node ~/.openclaw/skills/token-pilot/scripts/audit.js --all
```

---

### 高频重复任务封装 Skill
同样的操作流程手动重复 ≥2次，就应该封装成 Skill。

**封装收益**：
- 手动重复：每次都要在对话里重新描述操作步骤 → O(n) token
- Skill 复用：Agent 直接 `skill_get` 调用，步骤在 SKILL.md 里，对话里只需一句话 → O(1) token
- 多 Agent 团队共享同一个 Skill，所有 Agent 的重复任务一次封装，全部受益

**触发信号**：当你发现同一类请求出现第二次时，主动提醒用户"这个任务可以封装成 Skill，以后一句话触发"。

---

## Config Change Safety Rules（改配置铁律）

> 这三条是本次实测中踩坑总结出的，每次修改 openclaw.json 前必须遵守。

**R-C1：改配置前先查 schema**
```
gateway config.schema.lookup <path>
```
字段是否存在、类型、允许值，查完再写。不查盲写=必踩坑。

**R-C2：注意字段层级，不要写到顶层**
- `compaction`、`bootstrapMaxChars`、`bootstrapTotalMaxChars` 等字段在 `agents.defaults` 下
- 写到顶层会通过 config 校验报错，导致整个 openclaw 启动失败

**R-C3：不盲信第三方技能的"推荐配置"**
第三方技能 SKILL.md / README 里写的"推荐 openclaw.json 配置"不等于平台真实支持。
每个字段都要用 `config.schema.lookup` 验证后再写入。

---

## OpenClaw Bootstrap 机制（源码分析）
> 来源：`workspace-DGJIk8rw.js` `loadWorkspaceBootstrapFiles()`

**白名单加载，不是全目录扫描！** 只注入以下 8 个文件：
```
AGENTS.md  SOUL.md  TOOLS.md  IDENTITY.md  USER.md  HEARTBEAT.md  BOOTSTRAP.md  MEMORY.md
```
`.js`、`.txt`、`.json` 等**不在白名单中，不会被注入**。
**注入流程**：读白名单文件 → 子 agent/cron 只保留最小 5 个 → 按 `bootstrapMaxChars`（单文件上限，默认 6000 字符）和 `bootstrapTotalMaxChars`（总和上限，默认 12000 字符）裁剪，顺序加载，预算用完即止。

### R11: AGENTS.md 大小红线（新增）
- AGENTS.md 是最危险文件 — 注入规则（security-hardening、token-pilot 等）后极易超 6000 字符被**静默截断**
- 注入前先检查当前字节数：`wc -c AGENTS.md`
- 注入后总大小 ≤ 4800 字符（`bootstrapMaxChars` 的 80%，留安全余量）
- 超限 → 把低频规则移到 `references/` 子目录，按需 read 加载
- `audit.js` 现在只检查白名单文件，不再误报所有文件大小

---

## Setup / Config / Scripts

### Setup
**安装后执行一次注入脚本**，将核心规则写入所有 Agent 底层记忆（自动生效，无需触发词）：

```bash
bash ~/.openclaw/skills/token-pilot/scripts/init.sh
```

R3（回复简短）、R7（按角色裁剪工具）等交互敏感规则仍由 SKILL.md 按需加载，不做强制注入。

### openclaw.json 配置说明
安装此技能**无需修改 openclaw.json**，行为规则自动生效。

> 注：heartbeat 如需配置可写入 openclaw.json：
> `"heartbeat": { "every": "55m", "activeHours": { "start": "08:00", "end": "23:00" } }`

### Recommended tools.allow by role (示例，按实际角色调整)
- 重型角色（实现/交付类）：read/write/edit/exec/web_search/web_fetch/browser/sessions_spawn/memory_*/message
- 中型角色（产品/数据类）：read/write/edit/exec/web_search/feishu_doc/feishu_bitable/feishu_wiki/memory_*/message
- 轻型角色（内容/情报/增长类）：按职责裁剪，尽量不要 `[*]`

### Scripts

```bash
# Audit (read-only diagnostics)
node {baseDir}/scripts/audit.js --all             # Full audit
node {baseDir}/scripts/audit.js --config          # Config score (5-point)
node {baseDir}/scripts/audit.js --synergy         # Plugin synergy check

# Optimize (actionable recommendations)
node {baseDir}/scripts/optimize.js                # Full scan: workspace + cron + agents
node {baseDir}/scripts/optimize.js --apply        # Auto-fix workspace (cleanup junk, delete BOOTSTRAP.md)
node {baseDir}/scripts/optimize.js --cron         # Cron model routing + lightContext + prompt compression
node {baseDir}/scripts/optimize.js --agents       # Agent model tiering recommendations
node {baseDir}/scripts/optimize.js --template     # Show optimized AGENTS.md template (~300 tok)

# Catalog
node {baseDir}/scripts/catalog.js [--output path] # Generate SKILLS.md index
```

## Config Recommendations

```json
{
  "bootstrapMaxChars": 12000,
  "bootstrapTotalMaxChars": 20000,
  "compaction": {
    "mode": "safeguard",
    "memoryFlush": { "enabled": true }
  },
  "contextPruning": {
    "toolResults": { "ttl": "5m", "softTrimRatio": 0.3 }
  },
  "heartbeat": { "every": "55m", "activeHours": { "start": "08:00", "end": "23:00" } }
}
```

### memoryFlush（新增）
Compaction 压缩长会话之前，自动把关键信息持久化到本地记忆（smart-agent-memory）。
防止重要决策/信息被 compaction 丢掉。配合 memos-local 插件效果最佳。

### contextPruning TTL（新增）
工具调用结果在 context 里保留 5 分钟后自动软裁剪（保留摘要，丢弃原始输出）。
长会话中工具结果积累是 context 膨胀的主要原因之一。

### 工具白名单（新增）
在 openclaw.json 的各 agent `tools.allow` 里设置精确白名单，而非 `["*"]`。
按角色类型建议（示例，实际角色名按团队调整）：

| 角色类型 | 核心工具 | 可以不要 |
|---------|---------|---------|
| 情报/搜索类 | web_search/web_fetch/read/write/edit/exec/memory_*/message | browser/canvas/tts/feishu_bitable/sessions_spawn |
| 数据分析类 | read/write/edit/exec/web_search/feishu_bitable/memory_*/message | browser/canvas/tts/feishu_wiki |
| 内容创作类 | read/write/edit/exec/web_search/web_fetch/feishu_doc/feishu_wiki/memory_*/message | browser/canvas/tts/feishu_bitable |
| 增长/营销类 | read/write/edit/exec/web_search/web_fetch/feishu_doc/feishu_bitable/memory_*/message | browser/canvas/tts/feishu_wiki |
| 产品管理类 | read/write/edit/exec/web_search/feishu_doc/feishu_bitable/feishu_wiki/memory_*/message | browser/canvas/tts |
| 交付/运维类 | read/write/edit/exec/web_search/web_fetch/browser/sessions_spawn/memory_*/message | canvas/tts/feishu_bitable |
| 实现/开发类 | read/write/edit/exec/web_search/web_fetch/browser/sessions_spawn/memory_*/message | canvas/tts/feishu_bitable |
预计节省：每个受限 agent 减少 ~4,000-8,000 tok 工具定义开销。

### Cron Job 专项优化（lightContext）
OpenClaw 官方支持：`agentTurn` 类型的 cron job 可以设 `lightContext: true`，跑轻量 bootstrap context，大幅减少每次定时任务的冷启动 token 开销。

适用场景：消费日报、状态巡检、定时提醒等**不需要完整历史上下文**的 cron 任务。

配置方式（编辑 cron job payload）：
```json
{
  "kind": "agentTurn",
  "message": "执行消费日报任务",
  "lightContext": true,
  "model": "Qwen/Qwen3-8B"
}
```

配合建议：
- `lightContext: true` + 便宜模型（如 Qwen3-8B）组合使用
- Cron prompt 控制在 300 字以内，方法论写到 references 文件里
- 运行 `optimize.js --cron` 可以批量扫描哪些 job 还没设置 lightContext

## Model Routing

| Complexity | Model Tier | Examples |
|------------|-----------|---------|
| Light | Cheapest (gemini/haiku) | inbox scan, status check |
| Medium | Mid (gpt/sonnet) | web search, content |
| Heavy | Top (opus) | architecture, briefs |

## References
- `references/workspace-patterns.md` — File organization for minimal token cost
- `references/cron-optimization.md` — Cron model routing guide

## Validated Config Patterns (经实测可用)

以下配置来自真实部署验证，非推测。可直接写入 `openclaw.json`。

### agents.defaults.compaction（长会话稳定性）
```json
"agents": {
  "defaults": {
    "compaction": {
      "mode": "safeguard",
      "memoryFlush": {
        "enabled": true,
        "softThresholdTokens": 8000
      }
    }
  }
}
```
- `safeguard`：压缩时优先保留近期上下文，减少重要信息丢失
- `memoryFlush`：距压缩还剩 8000 token 时，自动触发记忆持久化，防止 compaction 丢掉关键决策（来源：Claude Code autoCompact.ts AUTOCOMPACT_BUFFER_TOKENS=13000，4000 缓冲偏小）

### agents.defaults.bootstrapMaxChars / bootstrapTotalMaxChars
```json
"agents": {
  "defaults": {
    "bootstrapMaxChars": 12000,
    "bootstrapTotalMaxChars": 20000
  }
}
```
限制启动时注入的 bootstrap 文件大小，防止 AGENTS.md / MEMORY.md 等文件无限膨胀导致冷启动 token 暴涨。

> ⚠️ 以上字段放在 `agents.defaults` 下，不是顶层。顶层写入会导致 config 校验报错。

### AGENTS.md 精简原则
- 目标：每个子 agent 的 AGENTS.md 控制在 **400 tok 以内**
- 只保留：启动规则、记忆规则、安全规则、平台格式化
- 删除：context-mode 使用说明（系统自动注入，写在 AGENTS.md 里是纯重复）、群聊规则、voice storytelling 等无关内容
- 主 workspace 的 AGENTS.md 是维护文档，允许更大，但子 agent workspace 要严格精简

### Workspace 根目录文件组织（隐藏的 token 杀手）

workspace 根目录每多一个文件 = 每次对话多一条 bootstrap 注入。

**铁律：脚本类文件不要放根目录**

| 文件类型 | 放哪里 |
|---|---|
| `*.js` / `*.py` / `*.ps1` 脚本 | `scripts/` 子目录 |
| 参考文档、知识文件 | `docs/` 或 `knowledge/` 子目录 |
| 临时数据、dump 文件 | `tmp/` 或 `data/` 子目录 |
| AGENTS.md / MEMORY.md / SOUL.md | 根目录（必须） |

实测：根目录 14 个脚本文件 ≈ **29,500 tok/session** 的额外注入开销。
清理后立竿见影，是单次优化收益最大的操作之一。

运行 `optimize.js --apply` 可自动将根目录脚本移到 `scripts/` 子目录。

### 图片/截图 token 控制
screenshot 或图片工具调用在视觉重度 session 中会大量消耗 token。
```json
"agents": {
  "defaults": {
    "imageMaxDimensionPx": 800
  }
}
```
- 默认值 1200，降到 800 可减少视觉 token 和 payload 大小
- OCR/UI 截图分析需要高精度时保留 1200 或更高
- 不涉及图片的 agent（如 pm/qa/coder 纯文本工作）可以设成 600 甚至更低

### Skill 描述精简（常被忽视的开销）
OpenClaw 系统 prompt 里会注入**全部已安装 Skill 的 metadata（名称 + 描述）**。
安装的 skill 越多、描述越长，每次对话冷启动开销越大。

优化建议：
- Skill description 控制在 **50 字以内**，只说"什么场景用"，不写使用步骤
- 不用的 skill 及时卸载（`openclaw skills uninstall <skill-name>`）
- 用 `/context detail` 查看当前 skill list 占了多少 token

### 实时诊断命令（随时可用）
```bash
# 查当前 session token 用量 + 模型 + 预估费用
/status

# 每条回复后显示 token 用量
/usage tokens

# 查看 context 分解（各文件/工具/skill 各占多少）
/context list
/context detail

# 手动触发 session 压缩
/compact
```
