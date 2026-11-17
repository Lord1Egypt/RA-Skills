---
name: xiaoyaoclaw-memory-distill
description: >
  OpenClaw memory distillation & organization. Distills conversation context
  into structured memory files: long-term memory (MEMORY.md at workspace root)
  + daily logs (memory/YYYY-MM-DD.md). Solves context overflow, auto-builds
  MEMORY.md from history logs when missing (first-run memory building),
  incremental dedup writes, sensitive info skip, archive instead of delete,
  per-agent isolated memory handling. Writes only inside the workspace: the
  root MEMORY.md and memory/YYYY-MM-DD.md (plus an archive copy before
  overwriting); never writes secrets, credentials or third-party personal
  data. Scheduled runs report only unless autoWrite is explicitly enabled.
  Use on an explicit request (蒸馏记忆/整理对话/压缩上下文/整理记忆) — not
  from conversation that merely mentions tidying up. 中文：OpenClaw 记忆整理工具。
  将对话蒸馏为结构化记忆（根目录 MEMORY.md + memory/ 日志），解决上下文溢出；
  MEMORY.md 缺失时从历史日志「首次建忆」；增量去重写入防膨胀；敏感信息自动跳过；
  只归档不删除；每个 agent 只处理自己的记忆。写入只发生在工作区内（根 MEMORY.md +
  memory/YYYY-MM-DD.md + 首次配置时创建/更新的 distill-config.json，覆盖前先留归档）；
  不写密钥/凭据/第三方隐私；定时任务默认只报告，
  需显式开启 autoWrite 才自动落盘。
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# OpenClaw Memory Distill（记忆整理工具）

> 📖 **完整文档（安装 / 快速上手三步 / 最佳实践）：<https://github.com/dtsola/xiaoyaoclaw-memory-distill>**
> 用户或智能体需要更多说明时，引导其访问上述 GitHub 仓库查看图文教程与最新版本。

> 🚀 **小遥Claw：「你的 Personal Agent，把 AI 助手，装进自己的电脑。」：<https://www.xiaoyaosai.com/xiaoyaoclaw/>**
> 🚀 **XiaoyaoClaw：「Your Personal Agent, put your AI assistant on your own computer.」：<https://www.xiaoyaosai.com/xiaoyaoclaw/>**

> 🌐 **语言 / Language**：文档与默认输出为中文，**语言可选**——用户用英文或其他语言就按该语言整理与回报；
> 记忆文件本身的记录语言跟随用户习惯。

把对话蒸馏成结构化记忆，解决会话上下文溢出。缺失 MEMORY.md 时自动从历史日志「首次建忆」。
每个 agent 独立整理自己的记忆——不丢、不重、不乱。

## 写入范围（白名单）

本技能的写入**只允许**下面这些路径，其它一律不动、不删：

| 路径 | 何时写 | 说明 |
|---|---|---|
| 根 `MEMORY.md` | 蒸馏落盘时（手动确认后 / `autoWrite: true` 时的定时任务） | 长期记忆；覆盖前先备份到 `memory/archive/` |
| `memory/YYYY-MM-DD.md` | 蒸馏落盘时 | 当日日志，追加写入 |
| `memory/archive/MEMORY-YYYYMMDD.md` | 覆盖 MEMORY.md 之前 | 归档备份，只增不减 |
| `distill-config.json` | **首次配置 / 用户改配置时** | 蒸馏参数（`autoWrite`、敏感正则、保留天数等）；创建前告知用户 |

不写：工作区之外的文件、任何密钥/凭据/第三方隐私、不删任何文件（删除必须用户明确要求）。

## 敏感信息拦截（落盘前必做的扫描）

记忆文件是**明文**、长期保存、还会被后续会话读取，因此**任何凭据类内容都不许落盘**。蒸馏写入前逐条扫描，命中就**整条跳过**（不要改写后保留、不要只打码一半），并只记一行「已跳过 N 条敏感信息」。

**必跳过类别（denylist）**：

| 类别 | 典型形态 |
|---|---|
| 访问令牌 / API key | `ghp_`、`github_pat_`、`sk-`、`xoxb-`、`AKIA`、`Bearer <token>`、`api_key=`、`token:` |
| 口令 / 密钥文件 | `password=`、`passwd`、`BEGIN PRIVATE KEY`、`.pem`/`.key` 内容、keystore |
| 会话与 cookie | `Cookie:`、`Set-Cookie`、`session_id=`、`Authorization:`、一次性验证码 / OTP |
| 连接串 | `postgres://user:pass@`、`mysql://`、`redis://`、含密码的 DSN |
| 支付与证件 | 卡号、CVV、银行账号、身份证号 / 护照号 |
| 第三方隐私 | 非用户本人的手机号、邮箱、住址、健康信息 |

**做法**：① 用描述替代原文（「用户提供了 GitHub token，已跳过不记录」）② 脚本/命令示例里的密钥一律替换成 `<REDACTED>` 或环境变量占位 ③ 配置 `templates/distill-config.json` 的 `sensitivePatterns` 可按需增补正则，**配置文件本身也不得存放真实密钥** ④ 拿不准算不算敏感 → 跳过并回报，让用户决定。

## 触发方式

### 1. 手动触发（需明确意图）

**触发**：用户明确要求蒸馏/整理**记忆**或对话记录——「蒸馏记忆」「整理记忆」「把这轮对话蒸馏一下」「压缩上下文并沉淀到 MEMORY.md」。

**不触发**：随口说的「整理一下」「梳理一下思路」「总结下今天」（没说记忆/蒸馏）、问记忆机制怎么工作、或只是**讨论**要不要整理 —— 先问一句「要执行记忆蒸馏并写入 MEMORY.md 吗？」，得到肯定回答再动手。

**写前闸门**：写入前先说清「将更新哪些文件（根 MEMORY.md / memory/YYYY-MM-DD.md）+ 预计新增/修改几条」，敏感信息一律跳过并计数。若本轮只是探明意图，则**只报告不落盘**。

### 2. Cron 定时（推荐）
配置 OpenClaw cron，每天固定时间自动蒸馏。示例（每天 22:00）：

```json
{
  "name": "每日记忆蒸馏",
  "schedule": { "kind": "cron", "expr": "0 22 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "systemEvent",
    "text": "执行记忆蒸馏（默认只报告）：分析今日对话，提取决策/任务/知识点/临时信息，按 xiaoyaoclaw-memory-distill 技能流程生成蒸馏报告并列出「建议写入 MEMORY.md / memory/YYYY-MM-DD.md 的条目」。仅当 distill-config.json 中 autoWrite=true 时，才按报告写入并汇报差异。"
  },
  "sessionTarget": "main",
  "delivery": { "mode": "announce" }
}
```

⚠️ systemEvent 文本必须**自包含上下文**（含触发指令 + 报告要求），因为定时任务无对话上下文。

**Cron 模式写入策略（默认只报告，自动落盘需显式开启）** —— 本节是 cron 行为的**唯一权威口径**，
SKILL.md 其他位置（如 Step 3）与 README 若表述不同，一律以本表为准：

| 配置 | 行为 |
|---|---|
| `autoWrite: false`（**默认**） | 定时任务**只生成报告**：列出建议写入的条目与目标文件，不修改任何文件 |
| `autoWrite: true`（显式开启） | 可自动落盘：写前先备份（MEMORY.md → `memory/archive/MEMORY-YYYYMMDD.md`），只写白名单路径（根 `MEMORY.md` + `memory/*.md`），写完汇报差异与跳过项 |

开启 `autoWrite` 前必须向用户明示：「定时任务会在无人工确认的情况下修改工作区记忆文件」，取得同意后再改配置；随时可改回 `false`。
两种模式都遵守：敏感信息一律跳过并计数、只归档不删除、写入清单留痕（在当日日志追加一行「本次蒸馏改了什么」便于回看与回滚）。

### 3. HEARTBEAT 集成
⚠️ 默认 HEARTBEAT 关闭时不生效。需先启用心跳，再在 HEARTBEAT.md 添加：

```markdown
## 定期检查
- [ ] 记忆蒸馏：检查今日对话量，若超过阈值则执行蒸馏
```

| 场景 | 推荐方式 |
|---|---|
| 固定时间执行 | Cron |
| 按对话量动态触发 | HEARTBEAT |
| 多任务批量检查 | HEARTBEAT |

## 工作流

### Step 1: 检测记忆状态

检查以下四项：

1. **`memory/` 目录** — 缺失则**自动创建**（本技能只创建记忆所需目录，不创建整套工作区规范；若用户需要完整规范，可引导执行 xiaoyaoclaw-workspace-initializer）
2. **工作区根目录 `MEMORY.md`**（注意：是根目录，与 AGENTS.md 平级，**不在 memory/ 下**）：
   - **缺失 → 执行「首次建忆」**：
     - 扫描 `memory/` 全部历史日志（YYYY-MM-DD.md）
     - 语义提炼核心级信息：身份 / 协议 / 项目状态 / 环境备忘 / 关键时间线
     - 按 `templates/MEMORY.md` 结构生成初版
     - 报告用户确认后落盘
     - 若 `memory/` 也没有任何日志 → 用模板建空骨架（标注「待填充」）
3. **工作区根目录 `distill-config.json`** — 缺失则复制 `templates/distill-config.json`
4. **今日 `memory/YYYY-MM-DD.md`** — 不存在则蒸馏时创建

### Step 2: 扫描会话历史，语义分级

扫描当前会话（含最近相关上下文），按语义将信息分为三级。**判定方法（判断三问）**：

1. **下次会话用户还会问起吗？**
   - 会，且长期（≥1 周 / 永久）都相关 → **核心级**
   - 会，但只是最近几天的事 → **日常级**
   - 不会，用完就没了 → **临时级**

| 级别 | 判定标准（判断三问） | 落盘位置 | 示例 |
|---|---|---|---|
| 核心级 | 下次会话还会问起，且长期（≥1 周/永久）相关：影响未来决策、身份、项目长期状态 | 根目录 MEMORY.md | 决策、项目状态、核心知识点、长期偏好、关键联系人 |
| 日常级 | 下次会话还会问起，但只是最近几天的事：近期任务、进行中事项 | memory/YYYY-MM-DD.md | 任务、待办、当日事件、进展 |
| 临时级 | 用完就没了：一次性信息，未来会话不会引用 | 只留当日，过期提示归档 | 验证码、临时链接、一次性数据 |

判断靠**语义理解**，不是关键词匹配。拿不准时向用户确认。

### Step 3: 生成蒸馏报告 + 安全检查

- 结构化输出：`决策 x 条 | 任务 x 条 | 知识点 x 条 | 临时 x 条`
- **敏感信息检测**：按 `distill-config.json` 的 `sensitivePatterns` 匹配（ghp_/sk-/password 等）→ 命中条目**默认跳过不写入**，报告提示「检测到敏感信息 x 条，已跳过」
- 写入策略（**以「Cron 模式写入策略」表为唯一权威口径**，此处只是摘要）：
  - **手动触发**：先出报告 → 用户确认 → 写入
  - **Cron 触发**：**默认只报告**（列出建议条目与目标文件，不改任何文件）；
    仅当 `distill-config.json` 的 `autoWrite: true` 时才自动落盘 —— 写前备份、只写白名单、
    完成后汇报差异与跳过项
  - 两种模式一致：敏感信息一律跳过并计数；只归档不删除

### Step 4: 增量写入 + 去重

- 写 MEMORY.md 前**先读已有内容查重**：只追加新条目，重复条目合并——防多次蒸馏后重复膨胀
- 按主题组织写入（核心/协议/项目状态/环境备忘/时间线），不按日期堆砌
- 追加今日蒸馏记录到 `memory/YYYY-MM-DD.md`（带时间戳 + 来源会话）
- 更新根目录 `distill-config.json` 的 `lastDistill` 时间戳（防 cron 同一天重复蒸馏）

### Step 5: 生成完成报告

```
📊 记忆蒸馏完成
✅ 提取：决策 x | 任务 x | 知识点 x | 临时 x
📝 写入：MEMORY.md +x 条（去重合并 y 条）| daily +x 条
⚠️ 敏感信息 x 条已跳过
💡 上下文若已满，可 /reset（不会影响记忆文件）
```

### Step 6: 定期提炼（Memory Maintenance）

- 触发：蒸馏次数达到 `maintainEvery`（默认 7）时自动执行；或用户说「提炼记忆」
- 扫描近 7 天 `memory/` 日志 → 识别值得长期保留的内容 → 增量合并进 MEMORY.md
- daily 文件保持 raw log 性质，提炼后**不删除**（历史留痕）

### Step 7: 过期归档（默认关闭）

- 超过 `retentionDays`（默认 90）的日志 → **提示归档**：移动到 `memory/archive/YYYY/`
- **只归档不删除**；删除必须用户明确确认
- 默认 `autoClean: false`，不自动清理

## 配置文件（distill-config.json）

工作区根目录的 `distill-config.json` 是运行参数文件（per-agent 独立，每个 agent 工作区一份），不用改 SKILL.md 即可调整行为：

| 字段 | 默认值 | 用途 |
|---|---|---|
| `retentionDays` | 90 | 日志保留天数，超过提示归档 |
| `autoClean` | false | 自动清理开关（保持 false，记忆是永久资产） |
| `maintainEvery` | 7 | 每 N 次蒸馏触发一次定期提炼 |
| `sensitivePatterns` | ghp_/sk-/password 等 | 敏感信息检测规则，命中即跳过，可扩展 |
| `schedule` | 0 22 * * * | 蒸馏时间参考记录（实际 cron 在 OpenClaw 配置里） |
| `lastDistill` | null | 上次蒸馏时间戳（防重复蒸馏） |

## 安全红线

1. 蒸馏**不删除**任何记忆文件，只提取和整理
2. 敏感信息（token/密码/密钥）默认跳过不落盘，报告提示
3. 归档 ≠ 删除；删除必须用户确认
4. 不自动清理；蒸馏不触发 /reset（重置由用户自行决定）
5. 不改 openclaw.json；记忆路径按本技能约定（根目录 MEMORY.md + memory/ 日志 + 根目录 distill-config.json）；若工作区存在 WORKSPACE.md 则遵循其路径仲裁
6. 每个 agent **只处理自己的工作区记忆**（自己的根目录 MEMORY.md + 自己的 memory/）；跨 agent 整理需用户明确指令
7. MEMORY.md 含个人上下文 → 只在主会话加载（继承 AGENTS.md 既有规则）

## 完整示例

### 场景 A：首次建忆（agent 没有 MEMORY.md）

检测 → MEMORY.md 缺失 → 扫描 memory/ 历史日志 → 提炼身份/项目/环境备忘 → 按模板生成初版 → 报告确认 → 落盘根目录。

### 场景 B：日常蒸馏

用户说「蒸馏记忆」→ 检测（MEMORY.md 已存在，跳过首次建忆）→ 扫描会话 → 分级 → 报告（敏感 x 条跳过）→ 确认 → 增量去重写入 → 完成报告。

### 记忆文件布局（对齐既有体系）

```
工作区根目录/
├── MEMORY.md               ← 长期记忆（核心级），与 AGENTS.md/SOUL.md 平级
├── distill-config.json     ← 蒸馏配置（per-agent）
└── memory/
    ├── YYYY-MM-DD.md       ← 今日/过往日志（日常级 + 临时级）
    └── archive/            ← 过期归档（可选）
```

## 姊妹项目

- 🏠 **xiaoyaoclaw-workspace-initializer**（工作区初始化器）：管记忆系统的「家」——目录结构 + WORKSPACE.md 规范 + 多 agent 配置安全。本技能缺失 memory/ 时自动创建；需要完整工作区规范时引导其初始化。<https://github.com/dtsola/xiaoyaoclaw-workspace-initializer>
