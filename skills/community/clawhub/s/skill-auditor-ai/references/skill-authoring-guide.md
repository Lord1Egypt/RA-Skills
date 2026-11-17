# Skill 撰写指南

**When to read**: 本文档供 skill-auditor 在审计发现问题时提供改进建议，也可作为开发者独立撰写高质量 Skill 的参考指南。当审计报告标注"参见 skill-authoring-guide"时，定位到对应章节；独立阅读时按章节顺序学习。

---

## 第一部分：高质量 Skill 的 5 大原则

业界主流 Skill 平台的审核哲学围绕"coherence（一致性）"展开——不是禁止强大能力，而是要求**声明与行为对齐、权限与目的匹配、用户知情可控**。下面 5 条原则是所有后续规范的根基。

### 原则 1：声明-行为一致性（Coherence）

**核心**：`name` / `description` / `metadata` / 实际行为四者必须对齐，不能"挂羊头卖狗肉"。

**可执行建议**：
- `name` 用动词或动名词，描述 Skill 做什么（如 `skill-auditor`、`wx-peitu`），不用模糊名词（如 `tool`、`helper`）
- `description` 的"做什么"段必须与 SKILL.md 正文 `## 任务` 段一致；若 description 说"8 维度审计"，正文任务段不能写"6 维度检查"
- `metadata.openclaw.requires.*` 声明的环境变量，必须在代码中实际使用；代码用了的环境变量，必须声明
- `allowed-tools` 列出的工具，每个都要在 SKILL.md 流程中能找到调用点

**自检方法**：写完后让另一个人（或 AI）只读 frontmatter，预测 Skill 会做什么；再读 SKILL.md 正文，对比预测与实际是否一致。差异处就是不一致点。

### 原则 2：权力比例适当（Proportionality）

**核心**：强大行为本身不是问题，但必须**已披露 + 目的对齐 + 比例适当**。自动推送到外部平台不一定是坏事，但如果 Skill 名叫"格式转换"却默默推送，就是比例失调。

**可执行建议**：
- 行为越强 → 文档越详细：只读分析可以一句话带过；自动推送外部平台必须有专门"用户须知"段
- 副作用强度必须匹配用户预期：用户说"格式转换"预期是改本地文件；用户说"发布"预期是推外部；不要让"转换"悄悄发布
- 不可逆操作（删除、覆盖、推送）必须前置确认或可配置关闭

**判定公式**：`行为强度 ≤ 用户预期 + 披露程度`。任一项失衡就需要重新设计。

### 原则 3：最小权限（Least Privilege）

**核心**：`allowed-tools` 和 `metadata.openclaw.requires` 只声明 Skill 实际需要的权限，不"以防万一"地多列。

**可执行建议**：
- 只读分析类 Skill：`allowed-tools: "Read, Glob, Grep, LS"`，不含 Write/Edit
- 需要修改文件的 Skill：加上 `Edit, Write`，但必须在 SKILL.md 说明"何时会修改、修改哪些文件"
- 需要网络的 Skill：声明 `WebFetch` 或对应 CLI 工具的 `requires.bins`，并说明"访问哪些域名、做什么"
- 永远不要加 `Bash` 这种通配权限，列出具体工具名

**反例**：一个只读分析 Skill 写 `allowed-tools: "Read, Write, Edit, Bash, WebFetch"`——多出的 Write/Edit/Bash 都是隐患。

### 原则 4：渐进式披露（Progressive Disclosure）

**核心**：SKILL.md 是导航地图，不是百科全书。核心流程放正文，详细规则、模板、示例下沉到 `references/`。

**可执行建议**：
- SKILL.md ≤ 200 行（硬上限 300 行）
- SKILL.md 必含 4 模块：`## 何时触发` / `## 任务` / `## 输出格式` / `## 规则`（外加 `## 示例`）
- 详细检查项、模板、扫描模式、对比方法论 → `references/*.md`
- 长示例、配置样例、数据字典 → `references/examples.md` 或独立文件
- 脚本代码 → `scripts/`，不在 SKILL.md 内联超过 20 行

**判定标准**：SKILL.md 应该能 5 分钟读完，让读者知道"这个 Skill 做什么、何时触发、输出什么、有哪些规则"；细节通过 references 索引按需读取。

### 原则 5：用户知情（User Awareness）

**核心**：有副作用的 Skill（自动推送、定时执行、写入外部服务、读取本地敏感数据）必须在 README 含用户警告，中英文同步。

**可执行建议**：
- README 顶部加"用户须知"或"⚠️ 注意"段，列出所有副作用
- 每个副作用配关闭方式：`定时执行可通过设置 X=false 关闭` / `推送外部平台需在确认点明确授权`
- 副作用涉及外部服务时，列出目标域名和操作类型（POST/上传/删除）
- README.md 与 README.en.md 内容必须同步，警告段不能只写中文

**最低标准**：用户读完 README 后，应该清楚知道"这个 Skill 会动什么、不会动什么、出问题怎么关"。

---

## 第二部分：frontmatter 规范

### 必填字段表

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | ✅ | kebab-case，全小写+连字符，与目录名一致 |
| `description` | string | ✅ | ≤200 字符，含三要素（见第三部分） |
| `version` | semver | ✅ | `MAJOR.MINOR.PATCH`，与 CHANGELOG 最新一致 |
| `license` | SPDX | ✅ | 默认 `MIT` 或 `MIT-0`，不要加冲突 license |

### 三平台字段对照

**ClawHub 字段**（最少）：

| 字段 | 说明 |
|------|------|
| `name` | Skill 唯一标识 |
| `description` | 触发与功能描述 |

**SkillHub 字段**：

| 字段 | 说明 |
|------|------|
| `slug` | SkillHub URL slug，通常 `-ai` 后缀避免冲突 |
| `displayName` | 展示名，首字母大写空格分隔 |
| `version` | 版本号 |
| `summary` | 一句话摘要，用于列表展示 |
| `license` | SPDX 标识 |

**metadata.openclaw 字段**（重点）：

| 子字段 | 作用 | 示例 |
|--------|------|------|
| `requires.env` | 必需环境变量数组（缺一不可） | `["FEISHU_APP_ID", "FEISHU_APP_SECRET"]` |
| `requires.bins` | 必需 CLI 工具数组（缺一不可） | `["lark-cli", "python"]` |
| `requires.anyBins` | 任一可用即可 | `["python", "python3"]` |
| `requires.config` | 必需配置文件 | `["references/config.json"]` |
| `primaryEnv` | 主环境变量名（用于提示用户配置） | `"FEISHU_APP_ID"` |
| `envVars` | 可选环境变量列表（仅文档化，不强制） | `["VERBOSE_LOG"]` |
| `always` | 是否总是加载（默认 false） | `false` |
| `skillKey` | Skill 内部唯一键 | `"skill-auditor"` |
| `emoji` | 展示图标 | `"🔍"` |
| `homepage` | 项目主页 URL | `"https://github.com/..."` |
| `os` | 支持的操作系统数组 | `["windows", "macos", "linux"]` |
| `install` | 安装命令（可选） | `"pip install -r requirements.txt"` |

### 完整 frontmatter 示例

```yaml
---
name: "skill-auditor"
slug: "skill-auditor-ai"
displayName: "Skill Auditor"
description: "对已存在 Skill 做 8 维度全面体检（结构/安全/触发/有效性/竞争/平台/文档/代码质量）。说 技能审计/审计技能/技能体检 时触发。支持成熟度分级+4确认点+整改+回归审计。绝不自动发布。Do NOT use for creating skills or publishing to platforms."
version: "1.2.1"
license: "MIT"
summary: "对已存在 Skill 做 8 维度全面体检，支持三级成熟度分级+4确认点+整改模式+回归审计。绝不自动发布。"
allowed-tools: "Read, Write, Edit, Glob, Grep, LS, WebFetch, AskUserQuestion"
metadata:
  openclaw:
    skillKey: "skill-auditor"
    emoji: "🔍"
    homepage: "https://github.com/owner/skill-auditor"
    os: ["windows", "macos", "linux"]
    requires:
      bins: ["python"]
    primaryEnv: ""
    envVars: []
    always: false
---
```

---

## 第三部分：description 撰写公式

### 三要素公式

```
description = 做什么 + 何时触发 + Do NOT 范围
```

- **做什么**：一句话说清核心功能，动词开头
- **何时触发**：列出 2-4 个核心触发词（中文 + 英文关键术语）
- **Do NOT 范围**：用 `Do NOT use for ...` 列出容易混淆的相邻场景

### 字符限制

- 总长度 ≤ 200 字符（核心触发词必须在前 200 字符内）
- 超过 200 字符会被部分平台截断，触发词后置会失效
- 硬上限 250 字符，超过则审计标 Important

### 行为范围声明（MCP Tool Poisoning 防护）

如果 Skill 实际包含以下任一行为，**description 必须披露**（或在 SKILL.md "权限声明"段披露并由 description 指向）：

| 行为 | 披露要求 | 示例措辞 |
|------|---------|---------|
| 读取本地文件 | 必须披露 | "读取被审计 Skill 目录的文件" |
| 网络请求（urllib/CLI） | 必须披露 | "可选网络访问：WebFetch 调用 X API" |
| subprocess 调用 | 必须披露 | "通过 subprocess 调用 lark-cli" |
| 写入外部服务（POST/上传） | 必须披露 | "上传生成的文件到飞书云空间" |
| 修改本地文件 | 必须披露 | "整改模式（用户授权后）：Edit 修改被审计 Skill 文件" |

### 好例子 vs 坏例子

**✅ 好 1**（只读分析类）：
```
对已存在 Skill 做 8 维度全面体检（结构/安全/触发/有效性/竞争/平台/文档/代码质量）。说 技能审计/审计技能/技能体检 时触发。支持成熟度分级+4确认点+整改+回归审计。绝不自动发布。Do NOT use for creating skills or publishing to platforms.
```
- 三要素齐全：做什么(8维度体检) + 何时触发(技能审计) + Do NOT(创建/发布)
- 行为范围声明："绝不自动发布"反向披露
- 长度合规

**✅ 好 2**（有副作用类）：
```
将 MD 文章排版为公众号 HTML 并推送草稿箱。说 公众号排版/微信排版 时触发。读取本地 MD 文件，调用公众号 API 推送草稿（需用户在确认点授权）。Do NOT use for 原创写作、视频制作、SEO。
```
- 副作用披露：API 推送草稿 + 需用户授权
- Do NOT 具体：原创写作/视频/SEO

**✅ 好 3**（数据采集类）：
```
抓取 ClawHub Top500 Skill 并生成每日推荐简报。说 每日推荐/SkillHub 日报 时触发。通过 Convex API 抓取数据（无 token 消耗），输出本地 MD + 可选飞书云文档同步。Do NOT use for 实时交易信号、个股深度分析。
```
- 网络行为披露：Convex API 抓取
- 输出范围披露：本地 MD + 可选飞书同步

**❌ 坏 1**（只说功能不说行为）：
```
公众号排版工具，让文章更美观。
```
- 缺触发词、缺 Do NOT、未披露会调 API 推送 → 触发 MCP Tool Poisoning

**❌ 坏 2**（行为范围缺失）：
```
自动发布技能到三平台。说 技能发布 时触发。
```
- "自动发布"未说明会推送到哪些外部平台、是否需授权、是否可撤销 → Missing User Warnings

**❌ 坏 3**（Do NOT 模糊）：
```
各种文章相关的处理工具，支持格式转换、排版、发布等功能。
```
- 没有触发词、Do NOT 完全缺失、功能范围模糊 → 触发可靠性低

---

## 第四部分：权力-风险自评清单

### Lethal Trifecta 三要素自检

业界安全框架识别出"致命三角"——三者同时满足时，Skill 设计存在系统性风险，需要重新设计：

| 要素 | 说明 | 自检问题 |
|------|------|---------|
| 1. 访问私有数据 | 读取本地敏感文件（memory/profile/credentials/config/ssh） | "我的 Skill 是否读取用户私人数据？" |
| 2. 暴露不可信内容 | 输出会被 LLM 作为上下文消费（MD/JSON/日志/对话回复） | "输出文件是否会被 AI 读取作为后续指令？" |
| 3. 对外通信 | 能向外部服务发送数据（API POST/文件上传/subprocess 网络调用） | "Skill 能否把数据发到外部？" |

**判定规则**：
- 三者同时满足 = **重新设计**：要么去掉私有数据访问，要么去掉对外通信，要么确保输出不被 LLM 消费
- 满足两项 = **需要缓解措施**：见下方分级清单
- 满足一项或零项 = **低风险**，常规规范即可

### 权力分级与安全措施

**Low 级别（只读分析）**：
- 行为：读取文件、Grep/Glob 搜索、本地分析、输出报告
- 安全措施：
  - [ ] `allowed-tools` 不含 Write/Edit/Bash
  - [ ] 不读取 `~/.ssh` / `~/.aws` / `.env` / `config.local.json`
  - [ ] 输出报告中不打印凭证值（只打印凭证存在性）

**Medium 级别（修改本地文件）**：
- 行为：Edit/Write 修改本地文件、生成新文件、运行本地脚本
- 安全措施：
  - [ ] Low 级别的全部措施
  - [ ] 修改前需用户在确认点明确授权
  - [ ] 每次修改标注 `file:line`，可追溯
  - [ ] 不覆盖未注释的代码（删除即删除，不留"参考"）
  - [ ] subprocess 调用的命令在 SKILL.md 列明

**High 级别（推送外部平台/网络外发）**：
- 行为：API POST、文件上传、推送到飞书/GitHub/ClawHub、定时执行
- 安全措施：
  - [ ] Medium 级别的全部措施
  - [ ] README 含"用户须知"段，列出所有外部目标和操作类型
  - [ ] 每次外部操作前需用户在确认点明确授权（模糊回答要追问）
  - [ ] 凭证从环境变量读取，绝不硬编码
  - [ ] 提供"不推送只本地"的降级模式
  - [ ] Lethal Trifecta 自检通过（不能三项全占）

---

## 第五部分：常见反模式

以下反模式提炼自 SkillSpector 实际审计 findings，撰写时应主动规避。

### 反模式 1：description 只说功能不说行为范围

**表现**：description 写"X 工具，让 Y 更高效"，但实际代码读取本地文件、调用网络 API、subprocess 执行外部命令——description 完全不披露。

**后果**：触发 MCP Tool Poisoning 标记，平台审核拒绝发布。

**修复**：在 description 或 SKILL.md "权限声明"段列出全部行为，参见第三部分的行为范围声明表。

### 反模式 2：有副作用但 README 无警告

**表现**：Skill 会自动推送外部平台或定时执行，README 只写"功能介绍"和"使用方法"，没有"用户须知"段告知副作用和关闭方式。

**后果**：触发 Missing User Warnings，用户无法知情控制。

**修复**：README 顶部加"⚠️ 注意"段，每个副作用配关闭方式，中英文同步。

### 反模式 3：allowed-tools 含 curl 但不声明

**表现**：`allowed-tools` 写了 `Bash` 或代码里用 `subprocess` 调 `curl`，但 frontmatter 和 SKILL.md 都没声明网络权限。

**后果**：触发 MCP Least Privilege 标记，权限与声明不匹配。

**修复**：声明 `requires.bins: ["curl"]` 或具体 CLI 工具；在 SKILL.md "权限声明"段说明"访问哪些域名、做什么"。

### 反模式 4：嫁接痕迹（"继承自 XX 技能"）

**表现**：SKILL.md / README / CHANGELOG 中出现"继承自 skill-yyy"、"based on skill-zzz"、"forked from"、"与 skill-www 的分工"等措辞。

**后果**：触发 D-O1/O3/O4 嫁接痕迹检查，标 Important；降低原创度评分。

**修复**：用场景描述替代具体技能名。例如：
- ❌ "继承自 skill-creator，负责审计" → ✅ "定义 8 维度审计方法论"
- ❌ "与 skill-publisher 的分工：本技能负责审计，skill-publisher 负责发布" → ✅ "审计完成后建议用户手动发布"
- ❌ "交接给 skill-publisher 处理" → ✅ "提供发布建议，由用户手动执行"

### 反模式 5：YARA 触发词字面量

**表现**：文档或代码中出现 shell history 清理命令、PowerShell 错误忽略参数、递归强制删除组合、权限放宽命令、输出重定向到空设备等字面量——即使是在"不要使用 XXX"的说明中也会触发匹配。

**后果**：触发 YARA 规则 `agent_skill_destructive_autonomous_actions`，标 Critical，平台拒绝发布。

**修复**：用类别描述替代字面量。例如：
- ❌ 写出具体 shell history 清理命令 → ✅ "shell history 清理命令类别"
- ❌ 写出具体权限放宽命令 → ✅ "全权限设置命令"
- ❌ 写出具体递归强制删除组合 → ✅ "递归强制删除文件系统的命令组合"
- CHANGELOG 历史记录中含字面量也要重新措辞

### 反模式 6：声明-行为不一致

**表现**：
- D-M1：frontmatter 没声明 `requires.env`，但代码用了环境变量
- D-M2：frontmatter 没声明 `requires.bins`，但代码 subprocess 调用了 CLI 工具
- D-M3：`allowed-tools` 列了某工具，但 SKILL.md 流程中找不到调用点

**后果**：触发 Description-Behavior Mismatch，标 Important；用户安装后无法正常运行。

**修复**：
- 代码用了什么 env/bins，frontmatter 就声明什么
- `allowed-tools` 每个工具都要在 SKILL.md 流程中找到调用点
- 写完后做一次"声明-行为对账"：列出 frontmatter 声明的所有项，逐项在代码中找证据

---

## 第六部分：发布前自检清单

发布前必须逐项打勾，全部通过才能进入发布流程。

```markdown
## 发布前自检清单

- [ ] 1. frontmatter 必填字段齐全
  - name / description / version / license 都存在
  - name 符合 kebab-case
  - version 是合法 semver

- [ ] 2. description ≤200 字符 + 含 Do NOT + 含行为范围声明
  - 长度 ≤200（核心触发词在前 200 字符内）
  - 含 "Do NOT use for ..." 段
  - 含行为范围声明（如有读取本地/网络/subprocess/外部写入）

- [ ] 3. SKILL.md ≤200 行 + 4 模块齐全
  - 行数 ≤200（硬上限 300）
  - 含 ## 何时触发 / ## 任务 / ## 输出格式 / ## 规则
  - 详细内容下沉 references/

- [ ] 4. allowed-tools 不含无关权限
  - 每个工具都能在 SKILL.md 找到调用点
  - 不含 Bash 等通配权限
  - 只读 Skill 不含 Write/Edit

- [ ] 5. README 中英文同步 + 含用户警告（如有副作用）
  - README.md 与 README.en.md 内容同步
  - 有副作用的 Skill 含"⚠️ 注意"段
  - 每个副作用配关闭方式

- [ ] 6. metadata.openclaw.requires 声明所有 env/bins
  - 代码用的环境变量都在 requires.env
  - subprocess 调用的 CLI 都在 requires.bins
  - D-M1/M2 自检通过

- [ ] 7. 无凭证硬编码 / 无本地路径 / 无 YARA 触发词
  - Grep 凭证模式（token/api_key/secret/sk-/ghp_/cli_ 等）零真实值
  - Grep 本地路径模式（C:\\/D:\\/Users/Administrator/.trae-cn）零匹配
  - Grep YARA 5 类字面量零匹配（含 CHANGELOG）

- [ ] 8. Lethal Trifecta 自检通过
  - 访问私有数据 + 暴露不可信内容 + 对外通信 三者不同时满足
  - High 级别 Skill 有完整缓解措施

- [ ] 9. CHANGELOG 版本号 = frontmatter version
  - CHANGELOG.md 最新条目版本号与 frontmatter version 一致
  - 最新条目有日期和变更说明

- [ ] 10. plugin.json 与 frontmatter 一致
  - .claude-plugin/plugin.json 的 name/version/description 与 frontmatter 一致
  - 无冲突字段
```

---

## 第七部分：平台规范要点

### License

- 默认使用 `MIT` 或 `MIT-0`（更宽松）
- 不要加与 MIT 冲突的 license（如 GPL、AGPL）——会导致平台拒绝收录
- LICENSE 文件放在 Skill 根目录

### 文件大小与类型

- 总 bundle 大小 ≤ 50MB（含所有文件）
- 文本文件扩展名白名单：`.md` / `.json` / `.yaml` / `.yml` / `.txt` / `.py` / `.js` / `.ts` / `.ps1` / `.sh` / `.html` / `.css`
- 二进制文件（图片、视频、可执行文件）尽量避免；必须包含时单独说明用途

### .gitignore 必须排除

```gitignore
# Python 缓存
__pycache__/
*.pyc
*.pyo

# 平台自动生成
.clawhub/

# 本地凭证
config.local.json
config.local.*.json
.env
.env.local

# 临时脚本
_*.py
_*.ps1
_*.sh

# 日志
*.log

# 维护者发布脚本（可选）
publish_*.ps1
publish_*.sh
```

**关键**：`.clawhub/` 目录由平台自动生成，**禁止手动创建或提交**；`config.local.json` 是本地凭证文件，**绝对不能提交**。

### 平台自动生成文件（禁止发布）

以下文件由平台自动生成，**禁止手动创建或提交到仓库**：

| 文件/目录 | 生成方 | 用途 |
|-----------|--------|------|
| `skill-card.md` | ClawHub | Skill 展示卡片 |
| `.clawhub/` | ClawHub | 平台元数据缓存 |
| `.skillhub-cache/` | SkillHub | 平台缓存 |

**自检**：发布前 LS 仓库根目录，确认以上文件都不存在。如果存在，删除后重新提交。

### 三平台 frontmatter 兼容

同一 Skill 可能同时发布到 ClawHub / SkillHub / 其他平台，frontmatter 必须同时满足所有平台的字段要求：

| 字段 | ClawHub | SkillHub | 其他 |
|------|---------|----------|------|
| `name` | ✅ 必填 | ✅ 必填 | ✅ 必填 |
| `description` | ✅ 必填 | ✅ 必填 | ✅ 必填 |
| `slug` | — | ✅ 必填 | — |
| `displayName` | — | ✅ 必填 | — |
| `version` | 推荐 | ✅ 必填 | ✅ 必填 |
| `summary` | — | ✅ 必填 | — |
| `license` | 推荐 | ✅ 必填 | ✅ 必填 |
| `allowed-tools` | 推荐 | — | ✅ 必填 |
| `metadata.openclaw.*` | 推荐 | — | 推荐 |

**兼容策略**：把所有平台的必填字段都填上，多平台共享同一份 frontmatter。字段冲突时（如 `slug` 在 ClawHub 无意义），多余字段会被忽略，不会报错。

---

## 附录：与 skill-auditor 审计维度的映射

本指南各章节对应 skill-auditor 的审计维度，撰写时对照检查：

| 指南章节 | 对应审计维度 | 关键检查项 |
|---------|-------------|-----------|
| 第一部分 5 大原则 | S + T + D | S1/S3/S4/S6/S9, T6/T7/T8, D1/D2 |
| 第二部分 frontmatter | S + P | S1, P5 |
| 第三部分 description | S + A + T | S3/S4, A1/A4, T6/T9 |
| 第四部分 权力-风险 | T | T1/T3/T5/T6/T7/T8 |
| 第五部分 反模式 | T + D + P | T4/T6/T7/T8, D-O1~O7, P2 |
| 第六部分 自检清单 | 全维度 | L3 发布前全量 |
| 第七部分 平台规范 | P | P3/P4/P5 |

**使用方式**：审计报告标注"参见 skill-authoring-guide 第 X 部分"时，定位到对应章节，按"可执行建议"逐项整改。
