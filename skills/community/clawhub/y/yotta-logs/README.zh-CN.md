<p align="center"><b>语言 / Language</b>：中文（本文件）· <a href="./README.md">English</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-logs banner" width="100%" />
</p>

<h1 align="center">yotta-logs · 元史</h1>

<p align="center">YottaMeta 自有的历史会话 / 记忆日志检索技能：<b>零依赖检索 / 分析 JSONL、JSON、SQLite、Markdown 多格式记录</b>，回溯旧对话与父会话上下文，为跨会话追溯提供原始日志依据。适用于查以前说过的结论、定位某段决策、回顾某次讨论。</p>
<p align="center">用户引用先前聊过的内容 / 父会话 / 历史上下文时自动激活——<b>不依赖 jq / rg，纯标准库确定性检索</b>。</p>
<p align="center">纯 Python 3.8+ 标准库实现，零外部依赖；Windows + Linux + macOS 通用；只读本地日志，默认脱敏，不联网上传。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-logs"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-logs" /></a>
  <a href="https://github.com/YottaMeta/yotta-logs"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-logs" /></a>
  <a href="https://github.com/YottaMeta/yotta-logs/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-logs" /></a>
  <a href="https://github.com/YottaMeta/yotta-logs"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## 这是什么

智能体每天产生大量会话与记忆记录（JSONL / 单文件 JSON / SQLite / Markdown…），跨会话追溯时最缺的不是「记得发生过」，而是「原文在哪、谁说的、什么时候说的」。元史把这些记录做成**确定性检索引擎**：全源登记日志与记忆位置 → 按关键词 / 正则 / 日期 / 会话 / 角色 / 来源 / 类型 / 格式检索 → 提取会话原文 → 统计消息、token、成本与工具调用。

它不是某个平台的专属功能，而是一份与智能体无关的工具包：装进任何支持 Agent Skills 的智能体即可按需调用。全程零依赖、只读本地、不联网；输出默认脱敏，避免把日志里的密钥 / token 带到上下文。

## 核心价值

- **零依赖检索**：Python 3.8+ 标准库，不依赖 jq / rg / ripgrep 等外部工具，Windows + Linux + macOS 开箱即用。
- **多格式通用（v0.2.0）**：不再只认 JSONL——按「格式族 × 字段别名归一 + 配置兜底」适配 JSONL / 单文件 JSON / SQLite（opencode、Cursor state.vscdb 等）/ Markdown（记忆 md + 自由笔记）/ 二进制（只读标题），统一 Record 模型，引擎零改动接入怪格式。
- **全源登记**：`locate` / discover 自动发现本机常见日志与记忆源（Codex / Claude Code / Clawdbot / opencode / Gemini / yotta-memory / Codex 笔记…），按默认检索范围过滤。
- **容错解析**：坏行 / 坏字段自动跳过并计数，不中断检索；二进制 / 加密文件只回退标题不崩。
- **默认脱敏**：输出自动打码疑似密钥 / token / 口令（sk-、ghp_、AKIA、JWT、Bearer、URL 口令、key=value 赋值、超长 token），--no-redact 关闭。
- **多维度过滤**：关键词（不区分大小写）/ 正则 / 日期 / 会话 ID / sessions.json 别名 / 角色（user / assistant / tool / system / developer）/ 来源（--source）/ 类型（--kind）/ 格式（--format）。
- **结构化输出**：--json 输出纯净 JSON，含来源、会话 ID、行号、时间戳、角色，适合程序化核对出处。
- **只读安全**：只读本地日志与记忆文件，不修改、不删除、不联网上传，与元忆（语义记忆）互补分工。

## 核心优势

| 优势 | 说明 |
|---|---|
| **零依赖** | Python 3.8+ 标准库，无模型、无数据库、无外部服务；Windows + Linux + macOS 通用 |
| **多格式** | JSONL / JSON / SQLite / Markdown / 二进制五大格式族，字段别名归一 + 配置兜底 |
| **确定性** | 检索逻辑可复现、可解释；命中即原文片段 + 行号，不靠模型猜测 |
| **默认脱敏** | 疑似密钥 / token / 口令自动打码，降低日志原文外泄风险 |
| **默认范围** | 会话源 + 结构化记忆源默认开；自由笔记 / 二进制日志默认关，可显式开 |
| **容错** | 不同智能体的存储形态差异可容忍，坏行跳过不中断，加密文件只回退标题 |
| **定位准确** | 命中结果带来源 / 会话 ID / 行号 / 时间戳 / 角色，可精确回溯出处 |
| **生态分发** | GitHub + npm + ClawHub 三源同步发布；npx / git clone / Download ZIP / install.sh 四种安装方式 |

## 功能体系

| 命令 | 说明 |
|---|---|
| locate | 全源登记：发现本机所有日志 / 记忆源（来源 / 格式 / 类型 / 默认开关） |
| scan | 列出所有会话（跨源）：来源 / 会话 ID / 日期 / 消息数 / 大小 / 别名 |
| search | 跨源检索：关键词 / 正则 + 日期 / 会话 / 角色 / 来源 / 类型 / 格式过滤，输出时间线命中（--json 结构化） |
| session | 提取单个会话原文：时间线 + 角色 + 文本，--role 过滤，--tools 标注工具调用 |
| stats | 会话统计：消息 / 角色分布 / token / 成本 / 时间范围 / 分源（--daily 每日汇总） |
| tools | 工具调用次数排行 |
| version | 打印版本 |

## 快速使用

Windows 用 python，Linux/macOS 用 python3。

```bash
# 全源登记：发现本机所有日志 / 记忆源
python3 scripts/yotta_logs.py locate

# 跨源检索关键词（默认范围 = 会话 + 结构化记忆；自由笔记默认关）
python3 scripts/yotta_logs.py search "部署方案"

# 指定目录 / 文件（目录自动嗅探格式族）
python3 scripts/yotta_logs.py scan --dir ~/.clawdbot/agents/<agentId>/sessions

# 正则 + 日期 + 会话过滤
python3 scripts/yotta_logs.py search "CI 失败" --regex --date 2026-08-26 --dir /path/to/sessions

# 按来源 / 类型 / 格式过滤（来源名见 locate）
python3 scripts/yotta_logs.py search "记住" --kind memory
python3 scripts/yotta_logs.py search "XSS" --source opencode-db
python3 scripts/yotta_logs.py search "部署" --format sqlite

# 自由笔记显式开（默认关）
python3 scripts/yotta_logs.py search "推送闸门" --kind note

# 提取单个会话原文
python3 scripts/yotta_logs.py session abc123 --dir /path/to/sessions

# 统计（消息 / token / 成本 / 每日汇总）
python3 scripts/yotta_logs.py stats --dir /path/to/sessions --daily

# 工具调用排行
python3 scripts/yotta_logs.py tools --dir /path/to/sessions

# JSON 结构化输出（适合程序化核对）
python3 scripts/yotta_logs.py search "部署方案" --dir /path/to/sessions --json
```

退出码语义（与元安 / 元审 / 元盾 / 元真家族一致）：0 = 成功；1 = 无匹配 / 空结果集；4 = 用法错误 / 致命异常。

未指定 --dir 时，依次尝试环境变量 YOTTA_LOGS_DIR → discover 全源登记（locate 逻辑）并按默认检索范围过滤；找不到则退出码 4 并提示。

## 安装

以下四种方式任选，顺序即推荐优先级；技能文件一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-logs@0.3.5 --agent <智能体名称>      # 装到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-logs@0.3.5 --dir <智能体的技能目录>  # 指到技能目录本身（如 ~/.codex/skills）
```

- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定的技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），或稍等镜像缓存。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-logs.git <智能体的技能目录>/yotta-logs
```

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-logs` 点 **Code → Download ZIP**，解压后把 `yotta-logs` 文件夹放进智能体技能目录。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。
## 使用示例（AI 智能体）

1. 将本仓库的 SKILL.md 接入任意 AI 智能体的技能/规则系统（见上方安装）。
2. 用户问「上次说的部署方案是什么」时，先定位并检索：
   ```bash
   python3 scripts/yotta_logs.py locate
   python3 scripts/yotta_logs.py search "部署方案"
   ```
   得到命中时间线（来源 / 会话 / 时间 / 角色 / 原文片段）。
3. 需要完整上下文时提取对应会话：
   ```bash
   python3 scripts/yotta_logs.py session <会话ID> --dir <日志目录>
   ```
4. 需要精确出处时用 --json 拿来源 / 会话 ID / 行号 / 时间戳，回答时给出依据。
5. 需要回顾某次会话成本或工具使用分布时用 stats / tools。

## 开发与校验

- 测试：python scripts/test_yotta_logs.py（139 项，含 75 项 v0.1.0 回归 + 64 项 v0.2.0 通用化用例）
- 基础校验：python tools/validate-skill.py yotta-logs（在仓库根目录运行）
- 格式普查：references/agent-formats.md；统一格式：references/format.md；CLI 协议：references/cli.md；安全边界：references/security.md

## 更新日志

- v0.3.1（2026-09-13）：移除本机专属硬编码路径；discovery 与配置统一走环境变量和平台默认位置，并补回归覆盖。
- v0.3.0（2026-09-08）：评测驱动完善——新增常见问题，安装器错误处理与退出码加固，并补齐安装器测试。

- v0.2.2（2026-08-29）：安装方式统一为四方式（对齐发布规范 §3.3.1）——方式一 npx -y @yottameta/yotta-logs@0.3.5 --agent / --dir（推荐，走 npm 源）；方式二 git clone；方式三 GitHub Download ZIP；方式四 bash install.sh --agent/--dir/--list。移除旧式 GitHub 克隆安装器与全局安装（-g）推荐；中英 README 安装节同步。无功能变更。

- v0.2.0（2026-08-27）：多格式通用化——JSONL / 单文件 JSON / SQLite（opencode 等）/ Markdown（记忆 + 自由笔记）/ 二进制五大格式族，统一 Record + 字段别名归一 + 配置兜底，discover 全源登记，新增 --source / --kind / --format 过滤与默认检索范围（会话 + 结构化记忆开、自由笔记 / 二进制日志关）。详见 CHANGELOG.md。
- v0.1.0（2026-08-27）：首版——零依赖 JSONL 会话日志检索引擎（locate / scan / search / session / stats / tools / version + 默认脱敏 + sessions.json 别名 + 只读）。

## 参考文档

- references/faq.md

## 许可证

MIT © YottaMeta —— 详见 [LICENSE](./LICENSE)。
