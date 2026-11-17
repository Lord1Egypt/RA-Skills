---
name: session-continuity-protocol
description: "跨工作区 / 跨会话记忆连续性协议（潘布达首发）。触发场景：新会话开局、用户说「续上上下文 / 你还记得吗 / 你失忆了」、或要做任何连续性敏感任务（公众号发稿、品牌资产、发布阻塞、密钥投递、项目状态）之前。加载后严格跑「开局四步」把已固化事实回灌，避免在已定稿事项上重复问用户、避免失忆。真源 = 文件层（_ACTIVE_PROJECTS.md + 账号 MEMORY.md）优先于 localmem 语义层兜底。 适用场景：当需要跨会话连续性协议（开局四步）能力时使用本技能；触发词：continuity、memory、localmem、cross-session、开局四步。"
version: 1.0.1
agent_created: true
author: 潘布达 (Buda Pan) @SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write, Edit, WebFetch, WebSearch
category: 通用技能
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
read_when:
  - 新会话开始、用户还没说具体任务前（默认主动跑）
  - 用户质疑「你失忆了 / 怎么又忘了 / 昨天不是已经…」
  - 要做公众号发稿、品牌资产、发布阻塞、密钥投递类任务前
  - 跨工作区接续上一个会话的半成品（如推送草稿箱仍卡在哪）
tags: [continuity, memory, localmem, cross-session, 开局四步, 失忆, 跨工作区]
slug: session-continuity-protocol
displayName: 跨会话连续性协议（开局四步）
display_name: 跨会话连续性协议（开局四步）
title: 跨会话连续性协议（开局四步）
description_zh: "跨工作区 / 跨会话记忆连续性协议（潘布达首发）。触发场景：新会话开局、用户说「续上上下文 / 你还记得吗 / 你失忆了」、或要做任何连续性敏感任务（公众号发稿、品牌资产、发布阻塞、密钥投递、项目状态）之前。加载后严格跑「开局四步」把已固化事实回灌，避免在已定稿事项上重复问用户、避免失忆。真源 = 文件层（_ACTIVE_PROJECTS.md + 账号 MEMORY.md）优先于 localmem 语义层兜底。"
description_en: "Cross-workspace and cross-session memory continuity protocol: session-opening and continuity-sensitive task flows so context survives account, workspace and device switches."
classification:
  skillhub: ["knowledge"]
  iso_25010: ["Maintainability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
ai_protocol: true
spec: usk/1.0
interface:
  type: prompt
  entry_point: SKILL.md
  runtime: none
  call_pattern: prompt
input_schema:
  task:
    type: string
    description: 本技能为协议型：新会话开局主动执行「开局四步」，把已固化事实从记忆文件回灌，避免重复询问用户。
    required: true
output_schema:
  result: 按 SKILL.md 规定的结构化产出（协议步骤 / 团队派单 / 选题打分卡）
exit: 无进程退出码；由主 agent 依文档执行
capabilities:
  - memory
  - continuity
  - session
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); internal platform names neutralized; 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
- Session starts and the user has not stated the task yet (run proactively by default).
- The user questions "you forgot / how come you forgot again / wasn't this settled yesterday".
- Before continuity-sensitive work: official-account publishing, brand assets, publishing blocks, key delivery, project status.
- Resuming half-finished work from a previous session across workspaces (e.g. where exactly the push draft box is stuck).
- Trigger words: continuity, memory, localmem, cross-session, opening four steps.

Not for: anything outside the protocol scope (see body / description).

### Usage
Invocation and parameters are detailed in section "I. Opening four steps (run every new session; order mandatory)" below.

### Workflow
Step 1 · read the global master index
Step 2 · read the account-level source MEMORY
Step 3 · localmem semantic recall (fallback)
Step 4 · scan project-level MEMORY from the last 14 days

> Author: Buda Pan (content-publishing ops lead) · finalized 2026-09-04 · background: the user repeatedly pointed out "amnesia" — the root cause was not a missing plan, but that **known facts were not re-loaded via protocol at session start**.

### Why this protocol is needed
The baseline finding on GitHub about agent memory (memory-systems skill + LoCoMo benchmark): **file-level memory reads beat dedicated memory tools** — basic file operations already reach 74%, above the 68.5% of dedicated tools like Mem0. So the "local-first minimal stack" already in place is right: no migration, no cloud.

- `localmem-mcp` (v0.1.1 installed): SQLite+FTS5+local fastembed, hybrid cosine+keyword retrieval, zero LLM / zero API.
- Config `LOCALMEM_DB_PATH=<your-workspace-root>/_localmem_memories.db` — one db shared across workspaces / accounts.
- Global master index: `<your-workspace-root>/_ACTIVE_PROJECTS.md`.
- Account-level source: `<memory-root>/MEMORY.md`.

**The only gap**: facts were not re-loaded at session start. Amnesia = the continuity owner failing to run the protocol. This skill turns that protocol into a callable, reusable action.

### I. Opening four steps (every new session; order mandatory)
> Run all four **before** any substantive task. < 1 minute; saves repeated user questions.

**Step 1 · read the global master index**
```
Read <your-workspace-root>/_ACTIVE_PROJECTS.md
```
Get: active project list, RACI, per-project block status, latest handoff points — the overview of "what is on my plate now".

**Step 2 · read account-level source MEMORY**
```
Read <memory-root>/MEMORY.md
```
Get **finalized hard facts that must never be re-asked**. Key sections:
- 🔴 "Official-account articles · template & VI master entry" — take templates, SynomosAI red VI palette and QR-code paths from here first.
- Real account name = **SynomosAI** (CTA reads "Follow 【SynomosAI】"; the old platform purple is forbidden).
- The 4 big blocks in the push draft box.
- Publishing-gate iron rule (if a platform flags content as suspicious → do not appeal).
- Key-delivery iron rule (DPAPI / key_drop; plaintext forbidden).
- Signature / copyright system.

**Step 3 · localmem semantic recall (fallback)**
Use localmem MCP tools: `recall_memory` (15 cross-workspace seeds loaded) or `search_memory`.
- Model cache: `<your-workspace-root>/_localmem_models` (**must be kept / backed up; search works offline; the model download source now returns 401 and cannot be re-pulled**).
- Recall limit=5~8; hard facts already loaded at file level hit even at low semantic scores.
- Verified hit queries: brand color, VI, account name, push blocks, project index, WeChat preview pitfalls, publishing gate, SOP.

**Step 4 · scan project-level MEMORY from the last 14 days**
```
Glob <your-workspace-root>/*/memory/MEMORY.md  → read the most recently modified
```
Get: each workspace's own project iron rules (e.g. "base64 QR inlining", "remove old platform name from CTA", "VI iron rules" in the 2026-09-03 workspace).

### II. Source hierarchy (whose word wins on conflict)
1. **First source = file layer**: `_ACTIVE_PROJECTS.md` + account MEMORY.md + project MEMORY.md. Conflicts resolve to the file layer.
2. **Second layer = localmem semantic layer**: recall fallback only; never write new facts there (facts go to Step 2 file layer).
3. **localmem is only "fallback when I can't recall"**, never a replacement for the file layer.

### III. Seed cheat-sheet (15 core seeds in localmem)

| id | Content | Example hit query |
|---|---|---|
| 4 | SynomosAI brand name + red VI palette + template path | "what brand color for the official account" |
| 6 | The 4 big push-draft-box blocks | "where is the push draft stuck" |
| 9 | Publishing-gate iron rule (no appeal when platform flags suspicious) | "platform flags content suspicious before publish, what to do" |
| 10 | Key-delivery iron rule (DPAPI / key_drop) | "how to deliver keys safely" (limit≈8) |
| 13 | Pointers to 6 in-flight projects | "which projects are active now" |
| 14 | WeChat X5 preview pitfall + LAN channel | "images don't show in WeChat" |
| 15 | Content-publishing ops SOP | "how does the publish flow run" |

> Note: id10 scores low semantically; Step 2 file-layer loading is the double insurance — always run Step 2 first in a new session.

### IV. Durability reminders (already-trodden pits)
- ⚠️ `<your-workspace-root>/_localmem_models` embedding cache **must be kept and backed up** — verification showed HuggingFace re-pull returns **401** (cas-server unreachable). Already-written vectors remain searchable; but **adding new seeds in the future depends on this local cache** — delete it and new memories cannot be written (old ones still searchable).
- ⚠️ localmem is secondary recall; the file layer is always the protagonist. Do not skip writing `_ACTIVE_PROJECTS.md` / MEMORY.md just because localmem exists.

### V. When to add seeds (write path)
When a new finalized hard fact appears (user decided it; it will not change):
1. First write the file layer: account MEMORY.md top "official-account template" section / project MEMORY.md.
2. Then write one semantic seed via localmem `store_memory` (tags incl. SynomosAI / publish / continuity).
3. Verify `recall_memory` hits it before considering it done.

### VI. DoD (definition of done)
- [ ] Steps 1~4 all run, none skipped.
- [ ] Before continuity-sensitive tasks, already hold finalized items (account name / VI / QR / blocks / keys).
- [ ] Did not re-ask the user for already-settled items.
- [ ] If new finalized facts were found, persisted to file layer + localmem.

## 中文

### 何时用

- 新会话开始、用户还没说具体任务前（默认主动跑）
- 用户质疑「你失忆了 / 怎么又忘了 / 昨天不是已经…」
- 要做公众号发稿、品牌资产、发布阻塞、密钥投递类任务前
- 跨工作区接续上一个会话的半成品（如推送草稿箱仍卡在哪）
- 触发词：continuity、memory、localmem、cross-session、开局四步、失忆。

不用于：不适用（详见正文/描述）。

### 用法

调用方式与参数详见正文「## 一、开局四步（每次新会话必跑，顺序不可省）」节。

### 流程

Step 1 · 读全局总索引
Step 2 · 读账号级真源 MEMORY
Step 3 · localmem 语义召回（兜底）
Step 4 · 扫近 14 天项目级 MEMORY

> 作者：潘布达（内容发布运营团主理人）｜定稿：2026-09-04｜背景：用户多次指出「失忆」——根因不是方案缺失，而是**开局没按协议回灌已知事实**。

### 〇、为什么需要这个协议

GitHub 上 agent 记忆的基准结论（memory-systems 技能 + LoCoMo 基准）：**文件级记忆读取比专用记忆工具更可靠**——基础文件操作就能拿 74%，高于 Mem0 专用工具 68.5%。所以本机已搭的「本地优先最小栈」是对的，不用换方案、不用上云：

- ✅ `localmem-mcp`（已装 v0.1.1）：SQLite+FTS5+本地 fastembed，余弦+关键词混合检索，零 LLM/零 API
- ✅ 配置 `LOCALMEM_DB_PATH=<你的工作区根>/_localmem_memories.db`，**跨工作区/跨账号共享同一 db**
- ✅ 全局总索引 `<你的工作区根>/_ACTIVE_PROJECTS.md`
- ✅ 账号级真源 `<memory-root>/MEMORY.md`

**唯一缺口**：开局没按协议回灌。失忆 = 潘布达（连续性 Owner）没执行协议。本技能就是把这个协议变成可调用、可复用的动作。

### 一、开局四步（每次新会话必跑，顺序不可省）

> 动手做任何实质性任务**之前**先跑完这四步。耗时 < 1 分钟，省下反复问用户的成本。

#### Step 1 · 读全局总索引
```
Read <你的工作区根>/_ACTIVE_PROJECTS.md   # Windows 例：~/.skills/<skill-dir><你的工作区文件夹>/_ACTIVE_PROJECTS.md
```
拿到：当前活跃项目清单、RACI、各项目阻塞状态、最近交接点。这是「现在手头有哪些事」的总览。

#### Step 2 · 读账号级真源 MEMORY
```
Read <memory-root>/MEMORY.md
```
拿到：**已固化、永不再问用户** 的终态硬事实。关键段：
- 🔴「公众号文章 · 取模版与 VI 总入口」——优先来这取模版 + SynomosAI 红 VI 色系 + 三码路径
- 公众号真实号名 = **SynomosAI**（CTA 写「关注【SynomosAI】」，禁旧平台紫色）
- 推送草稿箱 4 大阻塞
- 发布闸门铁律（平台判可疑 → 不申诉）
- 密钥投递铁律（DPAPI / key_drop，禁明文）
- 署名/版权体系

#### Step 3 · localmem 语义召回（兜底）
用 localmem MCP 工具：`recall_memory`（已灌 15 条跨工作区种子）或 `search_memory`。
- 模型缓存：`<你的工作区根>/_localmem_models`（**必须保留/备份，断网也可搜；模型下载源已 401 不可再拉**）
- 召回取 limit=5~8，文件层已加载的硬事实即使语义分低也能命中
- 典型问题验证过可命中：品牌色、VI、号名、推送阻塞、项目索引、微信预览坑、发布闸门、SOP

#### Step 4 · 扫近 14 天项目级 MEMORY
```
Glob <你的工作区根>/*/memory/MEMORY.md  → 读最近修改的
```
拿到：各工作区自己沉淀的项目铁律（如本次 2026-09-03 工作区的「三码 base64 内联」「CTA 去旧平台名」「VI 铁律」）。

### 二、真源层级（避免冲突时听谁的）

1. **第一真源 = 文件层**：`_ACTIVE_PROJECTS.md` + 账号 MEMORY.md + 项目 MEMORY.md。冲突以文件层为准。
2. **第二层 = localmem 语义层**：仅作兜底召回，不写新事实（写事实走 Step 2 文件层）。
3. **localmem 只负责"我想不起来时兜底"**，不替代文件层。

### 三、已灌种子速查（localmem 库 15 条核心）

| id | 内容 | 命中查询示例 |
|---|---|---|
| 4 | SynomosAI 品牌名 + 红 VI 色系 + 模版路径 | 「公众号品牌色用什么」 |
| 6 | 推送草稿箱 4 大阻塞 | 「推草稿箱卡在哪」 |
| 9 | 发布闸门铁律（平台判可疑不申诉） | 「发布前平台判可疑怎么办」 |
| 10 | 密钥投递铁律（DPAPI/key_drop） | 「密钥怎么投安全」(需 limit≈8) |
| 13 | 进行中 6 项目指针 | 「现在哪些项目在做」 |
| 14 | 微信 X5 预览坑 + LAN 通道 | 「微信里图不显示」 |
| 15 | 内容发布运营团 SOP | 「发布流程怎么走」 |

> 注：id10 语义分偏低，靠 Step 2 文件层加载双保险；新会话仍先跑 Step 2。

### 四、Durability 提醒（已踩过的坑）

- ⚠️ `<你的工作区根>/_localmem_models` 嵌入模型缓存**必须保留并备份**——验证时从 HuggingFace 重拉返回 **401**（cas-server 不可达）。已写入向量永久可搜；但**未来想再加新种子必须靠这个本地缓存**，删了就写不进新记忆（旧记忆照常能搜）。
- ⚠️ localmem 是二级召回，主角永远是文件层。别因为有了 localmem 就偷懒不写 `_ACTIVE_PROJECTS.md` / MEMORY.md。

### 五、何时补充种子（write 路径）

发现新终态硬事实（用户拍板、不再变）时：
1. 先写文件层：账号 MEMORY.md 顶部「公众号取模版」段 / 项目 MEMORY.md
2. 再用 localmem `store_memory` 写一条语义种子（tags 含 SynomosAI / publish / continuity 等）
3. 验证 `recall_memory` 能命中后再算完成

### 六、DoD（完成标准）

- [ ] Step 1~4 全跑完，未跳过
- [ ] 连续性敏感任务执行前已掌握「号名/VI/QR/阻塞/密钥」等已固化项
- [ ] 未向用户重复询问已定稿事项
- [ ] 若发现新终态事实，已落文件层 + localmem

### 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
