# vibe-ledger 设计文档

- 日期：2026-10-09
- 状态：待审（设计已在对话中逐段确认，本文是汇总定稿）
- 形态：Claude Code skill（打包为插件），同时可在 Codex 中使用

## 1. 要解决的问题

用 AI 做出了一个应用，但看不懂它的代码的人，需要回答几个朴素的问题：我的数据存在哪、谁能看到、什么操作会花钱、哪里最容易出事、当初说"以后再说"的事还欠着几件。会一点代码的人也有同样的问题，只是想看到证据和代码位置。

vibe-ledger 读取**生成这个应用的那些对话**和**当前的代码**，把"你要求过的、AI 声称做过的、AI 说以后再做的"整理成一本承诺账本，逐条对上代码证据，用图表加大白话呈现。理解和自查是同一个动作：账对不上的地方，就是要么你理解错了、要么代码有问题的地方。

## 2. 现有项目和定位

2026 年这个领域已经有不少工具（调研于 2026-10-09）：

| 类别 | 代表 | 面向谁 | 做什么 |
|---|---|---|---|
| 仓库 wiki | DeepWiki、Google Code Wiki | 开发者 | 从代码反推结构和含义 |
| 来源记录 | Entire CLI、git-ai、Agent Trace（Cursor 牵头的草案规范）、SpecStory | 开发者、团队 | 把会话或提示词挂到提交或代码行上；多数需要**事先安装**才开始记录 |
| 意图漂移检查 | Nissy、AWS Kiro、ARCTIC（arXiv 2607.29516） | 开发者 | 对比需求或 spec 和生成的代码 |
| vibe 应用安全扫描 | Lovable 内置扫描、VibeEval、UNPWNED、人工审计（约 1500 美元起） | 创作者 | 输出问题清单 |

vibe-ledger 刻意**不做**仓库 wiki、逐行溯源、通用安全扫描器，这些已经有成熟的免费方案。它的差异点：

1. **服务看不懂代码的人**，同时用分层显示照顾会一点代码的人。
2. **事后可用**：直接读本机已有的会话日志，不要求事先装任何东西。
3. **以"承诺"为单位对账，而不是逐行**。非程序员不关心是哪一行；以承诺为单位也不受"很多改动是通过 shell 完成的"影响（作者本机最近一个会话里，Bash 调用 3171 次，Edit 只有 77 次、Write 49 次）。
4. **"报错后的妥协"侦测**：专门找对话里"报错 → AI 为了跑通而绕过保护"的转折点。这类信号只存在于对话日志里。
5. **每条结论都带可校验的证据**，校验不通过就降级成"查不到"，不会编出来画到图上。

## 3. 用户与分层

- **默认层（大白话 + 图）**：给看不懂代码的人。不显示代码，用图和两三句结论说明。
- **开发者层（证据 + 代码）**：整页切换，或者每条结论单独点开，可以看到对话原文（带时间）、文件:行号和代码片段、探针结果，以及关键操作路径图 E。

两层用的是同一份报告、同一份数据。

## 4. 第一版范围

**包含**
- 承诺账本，按五问组织（见 §7）。
- 报错后的妥协侦测。
- 四张图（A 应用地图、B 权限矩阵、C 对话时间线、E 关键操作路径）加对账表 D。
- 确定性探针，覆盖 Next.js、Vite + React、Express、Supabase、Firebase。
- 同时支持 Claude Code 和 Codex 的会话日志。
- 首次运行时的日志抢救。

**不包含（留到第二版或以后）**
- 先猜再揭晓：用户先猜，再和实际情况对照，也就是三方对账里"你以为的"那一栏。
- 现场证明：在本地跑起应用，演示陌生账号读到数据等问题。
- 运行时点击追踪动画、把报告做成视频。
- 功能类需求的对账。账本**只收和五问相关的承诺**，"按钮改成蓝色"这类不收。
- Cursor 等其他工具的日志。

## 5. 形态与仓库结构

仓库根目录就是 skill 本身，同时带 `.claude-plugin/` 插件清单，和 travel-buddy 的做法一致。

```
vibe-ledger/
  SKILL.md                 总流程：什么时候触发、5 步各自运行哪条命令、每一步之后打印的下一步命令
  .claude-plugin/          plugin.json、marketplace.json
  scripts/
    sessions.py            找到本项目的会话，生成 digest（已脱敏）
    candidates.py          标出候选窗口，生成 reading_pack
    probes/                确定性探针，每个一个文件，共用一个注册表
    ledger.py              ledger 格式定义、合并分块结果（merge）
    verify.py              证据校验，输出 ledger.verified.json
    render.py              输出 report.html
    redact.py              密钥打码（digest 和 render 共用）
  references/              抽取指南、五问定义、ledger 字段说明、探针说明、候选规则
  tests/                   单元测试 + 测试样本（见 §13）
```

中间文件放在仓库外的工作目录：`~/.vibe-ledger/projects/<项目标识>/runs/<时间戳>/`。项目标识 = 项目目录名 + 项目绝对路径 SHA-1 的前 8 位，例如 `jizhang-3fa91c02`，这样同名目录不会混在一起。报告默认交付到 `~/Desktop`；桌面不存在就放 `~/Downloads`，再不行就放运行目录。路径总会打印出来。

## 6. 流水线与数据流

```
~/.claude/projects/**/*.jsonl ┐
~/.codex/sessions/**/*.jsonl  ┴→ ① sessions.py → digest.jsonl（已脱敏）
                                     ② candidates.py → candidates.json + reading_pack.md
代码仓库 ─────────────────────────→ ④ probes/ → probes.json
             模型读 reading_pack + 候选点 + 代码 + 探针结果 → ② ledger.json
             ③ verify.py（对照 digest、代码、探针）→ ledger.verified.json
             ⑤ render.py → report.html
```

### 6.1 会话归属（sessions.py）

- **Claude Code**：扫描 `~/.claude/projects/` 下所有 `*.jsonl`，包括子 agent 的记录（`isSidechain`）。会话里**只要有一条记录**的 `cwd` 在项目根目录内，或者有一次 Edit、Write、MultiEdit 的 `file_path` 在项目根目录内，这个会话就归属本项目。原因：同一个会话里的 `cwd` 会变，只看会话所在目录会漏掉或误收。
- **Codex**：扫描 `~/.codex/sessions/**/rollout-*.jsonl`。依据 `session_meta.payload.cwd`、`turn_context` 里的 `cwd`，以及 `apply_patch` 补丁里的文件路径判断归属。用户消息和 AI 回复分别来自 `event_msg` 的 `user_message` 和 `agent_message`；命令和输出来自 `function_call` 和 `function_call_output`。
- **对格式变化要宽容**：两种日志格式都是没有公开文档的内部格式，会随版本变化。遇到不认识的记录类型就跳过并计数，写进报告的覆盖范围一节。如果某个归属本项目的文件里一条能识别的消息都没有，要明确警告"日志格式可能已变化"。
- **digest 每条记录的字段**：`id`（Claude Code 用原日志里的 `uuid`；Codex 用 `<rollout 文件名>:<行号>`）、`session`、`agent`、`ts`（来自日志）、`role`、`kind`（text / edit / command / error / tool_output）、`text`、`files`。
  - 用户消息和 AI 的文字回复**逐字保留**（脱敏后）。
  - 改动记录保留文件路径和变更内容摘要。
  - 工具输出只保留报错，截到 2000 字符；其他工具输出丢弃。
- **校验以 digest 为准**：digest 由脚本生成，不经过模型。原始日志被清理后，归档的 digest 仍然可以用来校验引文。

### 6.2 首次运行：日志抢救

1. 报告本项目最早还能找到的会话日期，以及当前 `cleanupPeriodDays` 的值（读 `~/.claude/settings.json`；没有设置就是默认的 30 天）。
2. **先征得用户同意**，再调高 `cleanupPeriodDays`。这一步会修改用户的设置文件。
3. 把本项目的 digest 归档到 `~/.vibe-ledger/projects/<项目标识>/digests/`，放在仓库外。归档的是 digest，不是原始日志；digest 已经打码，避免把对话里的密钥复制到第二个地方。

### 6.3 模型读什么

模型**不读原始日志**，只读 `reading_pack.md`。它由 candidates.py 生成，包含：
- 用户原话的全集；
- 所有候选窗口（§8）；
- 每一轮（定义同 §8.1）最后一段 AI 文字回复。

reading_pack 超过 120,000 字符时，按会话切块，由子 agent 分别抽取出部分 ledger，再用 `ledger.py merge` 合并。合并时按引文去重，冲突的条目两份都保留，并标成冲突。

## 7. 五问

每条承诺必须恰好归到一问下：

| 键 | 问题 | 主图 |
|---|---|---|
| `where_data` | 数据存在哪 | A |
| `what_costs` | 什么操作会花钱 | A（💰 节点） |
| `who_can_see` | 谁能看到 | B |
| `what_breaks` | 哪里最容易出事 | C，并在 A 上标出 |
| `open_debts` | 还欠着的"以后再说" | C |

## 8. 候选点规则（candidates.py）

脚本只负责找候选，判断交给模型，最后由校验器把关。

### 8.1 报错后的妥协
- **报错信号**（满足任一即可）：
  - 工具调用返回失败（`is_error`，或命令退出码不为 0）；
  - 输出匹配报错特征，例如 `permission denied`、`violates row-level security`、`401`、`403`、`CORS`、`Failed to compile`、`TypeError`；
  - 用户贴了报错，或者说"还是不行""报错了""still not working"。
- **候选窗口**：从报错那条记录开始，到"往后第 20 条 digest 记录"和"下一轮结束"两者中**较早**的那个为止（一轮 = 从一条用户真实输入到下一条用户真实输入）。窗口内只要出现任何改动就成为候选，改动包括编辑或写入文件、用 Bash 改文件、执行 SQL 或数据库 CLI。
- **"绕过"特征**，只用来调高候选的优先级，不作为判定依据：
  - 删除的代码里含 `auth`、`policy`、`verify`、`check`、`validate`；
  - 新增 `disable row level security`、`using (true)`；
  - CORS 被设成 `*`；
  - 新增 `@ts-ignore`、`eslint-disable`、`any`、`--no-verify`；
  - 关掉证书校验（`verify=False`、`rejectUnauthorized: false`）；
  - 在前端使用 `service_role`；
  - 注释掉中间件；
  - 出现空的 `catch`；
  - 用假数据替换真实调用。
- **模型的任务**：判断这是否是一次妥协、绕过了哪种保护，并**对照当前代码**确认它是否还在。"还在"这个判断必须附代码证据。

### 8.2 以后再说
- 用多语言说法匹配 AI 和用户的原话：for now、temporarily、placeholder、mock、hardcode、stub、later、in production you should、quick fix、暂时、先这样、之后再、后续再、临时、写死、模拟、先跑起来、先不管。
- 当前代码里的 `TODO`、`FIXME`、`mock`、`placeholder` 注释也算候选。
- 模型判断：是否真的推迟了某件和五问相关的事？后来兑现了吗？兑现的判断要同时查后面的对话和当前代码。

### 8.3 AI 声称做过
- 每一轮（定义同 §8.1）最后一段 AI 文字回复里，含"已经加了""已实现""✅""I've added""now protected"这类说法的句子。

### 8.4 用户要求
- 用户原话的全集，由模型抽取其中和五问相关的要求。

## 9. ledger 格式与校验

### 9.1 格式（ledger.json）

```jsonc
{
  "evidence": {
    "E1": {"kind": "transcript", "session": "…", "msg_id": "…", "quote": "只有我自己能看到账目"},
    "E2": {"kind": "code", "path": "supabase/migrations/001.sql", "line": 14,
           "snippet": "alter table expenses disable row level security"},
    "E3": {"kind": "probe", "probe": "supabase_rls", "finding_id": "…"}
  },
  "promises": [{
    "id": "P3",
    "type": "user_requirement",          // user_requirement | ai_claim | deferred
    "question": "who_can_see",           // §7 五问的键
    "plain": "只有我自己能看到账目",
    "source": ["E1"],                    // 只能引用 transcript 类证据
    "status": "broken",                  // kept | broken | partial | pending | unknown
    "verdict_plain": "前门锁了，后窗一直开着",
    "verdict_dev": "expenses 表的访问规则（RLS）被禁用",
    "evidence": ["E2", "E3"],
    "fix_prompt": "…"                    // 可以直接复制给 AI 的修复指令
  }],
  "compromises": [{
    "id": "C1", "error": "E7", "change": ["E8"], "bypassed": "rls",
    "still_present": true, "now": ["E2"], "breaks": "P3"
  }],
  "map": {
    "nodes": [{"id": "n_db", "lane": "storage",       // browser | server | storage
               "kind": "database", "label": "Supabase", "holds": ["expenses", "users"],
               "paid": false, "evidence": ["E…"]}],
    "edges": [{"from": "n_web", "to": "n_db", "carries": "账目", "risk": null, "evidence": ["E…"]}]
  },
  "access": {
    "subjects": ["anonymous", "signed_in", "owner"],
    "resources": [{"name": "expenses",
                   "cells": {"anonymous": {"read": "deny", "write": "deny", "evidence": ["E…"]}, "…": {}},
                   "required_by": "P3"}]
  },
  "paths": [{"action": "点保存", "steps": [{"label": "saveExpense()", "evidence": "E…",
                                            "warning": null}]}]
}
```

状态的含义：

| 状态 | 含义 | 显示 |
|---|---|---|
| `kept` | 代码确实做到了 | ✅ |
| `broken` | 代码和承诺相反 | ❌ |
| `partial` | 只做到了一部分 | ⚠ |
| `pending` | 只用于 `deferred`：说了以后做，到现在还没做 | ⏳ |
| `unknown` | 查不到，或证据没通过校验 | ❓ |

`deferred` 类承诺如果后来兑现了，状态就是 `kept`。

### 9.2 校验规则（verify.py）

1. **对话证据**：`msg_id` 必须在 digest 里存在，`quote` 必须是该消息文本的逐字子串（忽略空白差异）。**时间戳一律从 digest 读取**，模型写的任何时间都会被覆盖。
2. **代码证据**：
   - 路径解析后必须在仓库根目录内，指到仓库外（比如用 `../`）的一律拒绝；文件必须存在。
   - 片段（忽略空白差异）出现在所写行号的前后 3 行以内，就算通过。
   - 不在附近、但在同一文件里只出现一次时，自动更正行号，并记下"行号已更正"。
   - 其余情况判定不通过。
3. **探针证据**：引用的探针结果必须真实存在于 `probes.json`。
4. **结论要有底气**：状态不是 `unknown` 的承诺，必须至少有一条通过校验的代码证据或探针证据。证据全部不通过时，状态强制改为 `unknown`，并记录原因。`source` 全部不通过的承诺不能出现在账本里，改为列进"被拒条目"。
5. **图上只画通过校验的东西**：
   - 地图节点和连线：没通过校验的不画，放进地图下方的"未核实"清单。
   - 权限矩阵：没通过校验的格子显示为 `?`。
   - 操作路径：没通过校验的步骤显示为虚线框，并标"未核实"。
6. **和探针冲突时两边都显示**：模型结论和探针结果相反时，比如矩阵说陌生人 `deny`、探针说 RLS 没开，就在该格同时显示两种说法并标出冲突，不悄悄只采信一边。原因是探针也有盲区，比如访问规则是在 Supabase 后台手动开的、迁移文件里看不到。
7. **格式严格检查**：缺字段、枚举值不合法、`pending` 用在非 `deferred` 的承诺上、引用的证据编号不存在，都直接报错退出，不会带着错往下渲染。

## 10. 探针（probes/）

每条探针结果都包含 `id`、`probe`、`level`（`certain` 确定 / `hint` 仅提示 / `fact` 事实）、`path`、`line`、`snippet`、`message`。结果用和代码证据相同的方法校验。

| 探针 | 查什么 | 级别 |
|---|---|---|
| `secrets_exposed` | 前端可见的环境变量里有密钥（`NEXT_PUBLIC_`、`VITE_`、`EXPO_PUBLIC_`、`REACT_APP_` 开头）；前端代码里硬编码了 `sk-`、`sk-ant-`、`sk_live_`、`service_role` JWT、`AKIA…`；`.env` 被 git 跟踪（`git ls-files`） | certain |
| `supabase_rls` | 迁移文件里每张表有没有 `enable row level security`；有没有 `disable` 或 `using (true)`；前端有没有引用 `service_role`。迁移文件里看不到的表记为"未知"，不记为"安全" | certain |
| `firebase_rules` | `firestore.rules` 或 `storage.rules` 里写成永远允许（`allow read, write: if true`），或者是带到期时间的测试模式规则 | certain |
| `cors_wildcard` | `origin: '*'`、`Access-Control-Allow-Origin: *`；如果同时允许携带凭证，要单独标出 | certain |
| `paid_api_unauthed` | 调用了付费服务 SDK（OpenAI、Anthropic、Replicate、Stripe、Twilio、Resend）的服务端接口，在同一个文件或调用链上看不到登录检查 | hint |
| `routes` | Next.js（`app/`、`pages/api/`）和 Express 的路由清单 | fact |

遇到不认识的技术栈，探针就跳过，报告的覆盖范围一节写明"未覆盖：<技术栈>"。

## 11. 报告（render.py）

单个 HTML 文件，可以离线打开。图由 Python 直接生成内联 SVG，不用 Mermaid，也不加载任何 CDN。交互只用原生 JS，支持展开、筛选、复制、切换视图。主题用 CSS 变量，支持浅色和深色。

### 11.1 页面结构
1. **页头**：项目名、视图开关（大白话 ⇄ 开发者），以及一条计数栏（✅/❌/⚠/⏳/❓ 各有几条）。**计数由脚本从 ledger.verified.json 算出**，不由模型填写。
2. **五问区**：每一问 = 一张图 + 两三句结论 + 相关的承诺卡片。
   - 数据存在哪、什么会花钱 → 图 A
   - 谁能看到 → 图 B
   - 哪里最容易出事、还欠着的事 → 图 C
3. **对账表 D**：列出全部承诺，可以按状态筛选。每行展开后显示对话原文和时间、文件:行号和代码片段、探针结果，以及可以一键复制的修复指令。开发者层还会显示相关的图 E。
4. **"这份报告没看到什么"**：读了几个会话、时间跨度多长、跳过了多少不认识的记录、多少改动找不到对话来源、哪些探针运行了或跳过了、多少条证据没通过校验、有哪些被拒条目。

### 11.2 四张图
- **A 应用地图**：固定三条泳道，从左到右是"浏览器 | 你的服务器 | 存储与第三方服务"，不用自动布局。会花钱的节点标 💰；连线上写明传的是什么数据，有风险的连线标红。图例直接画在图上。开发者层会在节点上显示文件:行号。最多画 12 个节点，超出的放进"其他"清单，排序时优先放有问题的、有证据的节点。
- **B 权限矩阵**：行是各类数据，列是陌生人 / 登录用户 / 本人；每格显示读和写两种权限。和用户要求冲突的格子加红框；和探针冲突的格子标双说法。有问题的行排在前面，没问题的行默认折叠。点格子可以看证据。
- **C 对话时间线**：分四条泳道，"你说的 / 报错 / AI 改的 / 以后再说"。每个事件用弧线连到最右边的"今天"一列，显示它现在的状态。只画和承诺、妥协有关的事件，没有事件的空白时间段会被压缩。
- **E 关键操作路径**：只在开发者层显示。画成横向的步骤链，比如"点按钮 → 前端函数 → 接口 → 数据库调用"。每一步标文件:行号，有问题的那一步标 ⚠。

### 11.3 没有数据时
- 没有对话记录：在时间线的位置写"没找到对话记录，无法生成时间线"，账本只保留代码这一侧能确认的内容。
- 没检测到数据库：权限矩阵显示"未检测到数据库"。
- 不画空图。空图会让人误以为"查过了，没问题"。

### 11.4 语言
报告语言用 `--lang zh|en` 指定。不指定时，按 digest 里用户消息的主要文字自动判断（中日韩字符为主就用中文）。界面文字放在一个小字典里，结论文字由模型按同一语言写。

## 12. 隐私与安全

- 全部在本机运行，不向外发送任何代码或对话。
- `redact.py` 对以下内容打码，只保留末 4 位：`sk-`、`sk-ant-`、`sk_live_`、`pk_live_`、`AKIA…`、`ghp_`、`xoxb-`、`xoxp-`、JWT（`eyJ…` 长串）、私钥块，以及赋值给名称含 `KEY`、`SECRET`、`TOKEN`、`PASSWORD` 的变量的高熵字符串（长度不少于 20，且香农熵不低于每字符 3.5 比特）。生成 digest 和渲染报告时**都要**过一遍。
- 中间文件和归档放在仓库外，避免被误提交。
- 修改用户的 `~/.claude/settings.json` 之前必须先征得同意。

## 13. 测试与验收

### 13.1 测试样本（自建，不使用用户的真实项目和会话）
| 样本 | 技术栈 | 埋的问题 |
|---|---|---|
| ① | Next.js + Supabase | 权限报错后 AI 关掉 RLS；OpenAI key 放在 `NEXT_PUBLIC_` 变量里；AI 声称"已加登录保护"但有一个接口没加 |
| ② | Vite + React + Firebase | 测试模式规则一直没改；AI 说过"上线前记得改规则" |
| ③ | Express | CORS 设成 `*`；付费 API 接口没有登录检查；"先写死管理员密码"一直没改 |
| ④ | Next.js | **干净应用**，没埋任何问题，用来检查会不会乱报警 |
| ⑤ | Flask | 第一版不覆盖的技术栈，用来检查是否明确报"未覆盖" |

配套的对话日志：
- 参照真实日志的结构手工生成，内容全部虚构。同时覆盖 Claude Code 和 Codex 两种格式，中文、英文都有。
- 包含以下特殊情况：上下文被压缩过的会话、子 agent 会话、会话中途 `cwd` 变化、用 Bash heredoc 改文件、一个完全没有日志的项目、一个超长会话（超过 120,000 字符，会走分块）。
- 每个样本附一份标准答案，写明应该出现的承诺和状态、妥协、探针命中。

### 13.2 单元测试
- **解析器**：两种格式都能解析；遇到坏行和不认识的类型能跳过并计数；`cwd` 变化时归属判断正确。
- **候选点**：样本里埋的每一个事件都要进候选。
- **探针**：每个探针都有"该报"和"不该报"的用例。
- **校验器**：编造的引文被拒；行号偏了能被更正；不存在的文件被拒；指到仓库外的路径被拒；模型写的时间被覆盖；不合法的状态值被拒；`pending` 用错地方被拒。
- **渲染器**：图上节点数等于通过校验的节点数；没核实的内容不出现在图上；空数据时显示明确提示；生成的 HTML 里**找不到任何一个预埋密钥的原文**。

### 13.3 对抗测试
手写一份证据全是编造的 ledger 喂给流水线。所有条目必须降级成 `unknown` 或被拒，编造内容出现在图上和计数里的数量必须为 0。

### 13.4 端到端测试
- 用 Claude Code 把 5 个样本完整跑一遍，和标准答案对比。
- 用 Codex 跑一遍，**只运行脚本打印出来的下一步命令**，检查流程有没有死胡同。

### 13.5 亲眼看产物
用无头浏览器截图，桌面宽度和手机宽度（390px，用 iframe 方式确保真实宽度）、浅色和深色各一张。四张图都要人眼确认看得懂，而不只是检查程序有没有报错。

### 13.6 真实项目试跑
在用户自己的一个真实 vibe 项目上跑一次，**必须先征得用户同意**。

### 13.7 验收标准
- 样本 ①②③ 中预埋的 ❌ 问题全部找出；
- 样本 ④ 的 ❌ 为 0；
- 样本 ⑤ 明确报出"未覆盖"；
- 未核实的内容上图为 0；
- 密钥原文泄漏为 0；
- 用户读一份真实报告后认可"读完懂了，并且是靠图读懂的"。

## 14. 建议的实现顺序

1. `sessions.py` + `redact.py`（含两种日志格式的测试样本）
2. `candidates.py`
3. `probes/`
4. `ledger.py`（格式定义、合并）+ `verify.py`
5. `render.py`（先做对账表 D，再做 B、A、C、E）
6. `SKILL.md` 和 `references/`
7. 端到端测试、跨 agent 测试、亲眼看截图
8. 插件清单和安装验证
