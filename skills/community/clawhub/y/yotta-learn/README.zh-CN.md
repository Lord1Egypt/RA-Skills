<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-learn banner" width="100%" />
</p>

<h1 align="center">yotta-learn · 元习</h1>

<p align="center">跨智能体的<b>知识库</b>技能：把跨项目可复用的经验、方法、避坑与教程沉淀进<b>分类知识库</b>（草稿 → 审核 → 可检索），供后续会话与其他智能体复用；首次使用由 AI 引导初始化知识库位置（由你确认）并自动接入 MCP。</p>
<p align="center">检测到值得沉淀的时刻（命令失败 / 用户纠正 / 发现更好做法 / 知识过时 / 请求缺失能力 / 外部接口故障），或需要查询知识的时刻（开工前 / 动手解决不显然问题前 / 用户问“以前怎么解决的”），或用户说 知识库 / kb / 查知识 / 记一笔 / 沉淀 / 经验 / 踩坑 / self-improvement / learnings 时自动激活——<b>不靠关键词碰运气：写入看归位决策树，查询有默认时机</b>。</p>
<p align="center">Python 3.8+ 标准库实现，零依赖；Windows + Linux 通用；初始化绝不覆盖已有数据。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-learn"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-learn" /></a>
  <a href="https://github.com/YottaMeta/yotta-learn"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-learn" /></a>
  <a href="https://github.com/YottaMeta/yotta-learn/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-learn" /></a>
  <a href="https://github.com/YottaMeta/yotta-learn"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## 这是什么

AI 智能体最常见的浪费，是同一个错误在不同会话里反复犯。元习把「这次学到的」变成「下次可复用的」：跨项目通用的经验、方法、避坑与教程 → 分类知识库（草稿 → 三问审核 → 可检索）；项目专属经验写项目自身文件；私密信息进元忆私密区。

它不是某个平台的专属功能，而是一份与智能体无关的 CLI 工具包：装进任何支持 Agent Skills 的智能体即可按需调用；首次使用时由 AI 引导完成知识库初始化（位置由你确认）并自动接入 MCP——同机所有智能体共享同一个知识库。

## 核心价值

- **归位决策树**：写哪里不再犹豫——私密 / 敏感 → 元忆私密区；项目专属 → 项目自身文件；跨项目可复用知识 → 知识库（草稿 → 三问审核）；事实 / 红线 → 元忆 FACT；成熟经验 → 技能化。一句话：「事」进元忆，「法」进知识库。
- **知识沉淀**：kb 命令组把知识按分类沉淀——分类注册、草稿 / 核验、分片索引、关键词查询；写入默认草稿、核验后入库、查询默认只出已核验。
- **写查时机**：事件驱动（失败 / 纠正 / 更好做法 / 知识过时 / 缺能力）+ 周期驱动（复盘 / 周级 review）；开工先查、动手前查、写前查重、复盘过草稿。
- **首次激活**：AI 检测状态 → 你确认库位置（默认 `~/.yottalearn/knowledge`）→ AI 执行初始化 + 写「发现锚点」+ 自动接入 MCP + 自检。
- **分类治理**：复用优先（写前先看现有分类）+ 新建规范（slug / 名称 / 描述）+ 一条一主分类 + 周期合并 / 停用。
- **遗留兼容**：旧 `.learnings/` 命令全部保留（读取 / 处置 / 迁移已有条目），新知识不再默认写入。
- **可联动**：遗留条目 `log --remember` 可选同步到元忆；未安装 / 失败自动降级，绝不阻断。

## 核心优势

| 优势 | 说明 |
|---|---|
| **跨智能体共享** | 知识库为机器级共享（`~/.yottalearn`），同机所有智能体读写同一份；项目专属经验仍在项目内、随仓库走 |
| **三问审核** | 验证过？自包含？无敏感？——核验需证据；敏感 / 疑似重复阻断（确认后可 `--force --note` 留审计放行） |
| **分类 + 中文检索** | 分类注册表 + 中文 bigram / 单字兜底关键词查询；draft / verified / deprecated 状态机 |
| **首装即用** | AI 引导激活 + MCP 自动接入 + 机器级「发现锚点」，装完不当摆设 |
| **可靠性内建** | 原子写 + 跨进程写锁 + 回收站 7 天 + 快照 + 独立目录备份 + `kb doctor` 体检 |
| **零依赖** | Python 3.8+ 标准库，无 daemon / 无数据库；Windows + Linux 通用 |
| **生态分发** | GitHub + npm 双源同步发布；npx / git clone / Download ZIP / install.sh 四种安装方式 |

## 功能体系

| 命令 | 作用 |
|---|---|
| kb | 知识库主命令组：init / config / category / add / list / review / query / index / stats / doctor / backup / trash / snapshot |
| view | 图形化管理台（运行时真命令；仅 127.0.0.1:8791） |
| log / list / review / update / resolve / promote / extract / init | 遗留 `.learnings/` 命令组（兼容旧数据：读取 / 处置 / 迁移；新知识不再写入） |
| log --remember | 遗留条目可选同步到元忆（yotta-memory），未安装自动降级 |

## 数据协议

- 知识库：默认 `~/.yottalearn/knowledge`（配置 `~/.yottalearn/config.json`；可用 `kb config set --dir <路径>` 指定任意位置，`--move` 迁移旧库）；条目为 Markdown + 受控 frontmatter，ID `KB-YYYYMMDD-XXX`，状态 draft / verified / deprecated；核验需证据，查询默认只出 verified（`--include-draft` 含草稿）。
- AI 接口：MCP stdio（`scripts/yotta_learn_mcp.py`；15 工具，写工具与 CLI 同源 fail-closed）；图形化管理台 `yotta-learn view`（运行时真命令；仅 127.0.0.1，八视图含「高级 / CLI」；技能目录直跑等价 `python3 scripts/yotta_learn.py view`）。
- 遗留 `.learnings/`（兼容旧数据）：项目根 `.learnings/`（可用 `--dir` 指定）；文件 LEARNINGS.md（LRN-）/ ERRORS.md（ERR-）/ FEATURE_REQUESTS.md（FEAT-）；字段 Logged / Priority / Status / Area / Pattern-Key；初始化幂等、绝不覆盖。
- 迁移：`kb add --from-learning <LRN-ID>` 把旧 `.learnings` 条目转成 KB 草稿（保留可移植来源引用，仍走审核门）。

## 使用示例

> 命令入口说明：示例用技能目录直跑写法 `python3 scripts/yotta_learn.py`；已装 CLI 时把该前缀替换为 `yotta-learn`（如 `yotta-learn kb query 中文检索`），两者完全等价。

```bash
# 激活与状态：首次使用先看状态（未初始化会给出引导）
python3 scripts/yotta_learn.py kb config get

# 初始化知识库（默认 ~/.yottalearn/knowledge；指定位置先 kb config set --dir <路径>）
python3 scripts/yotta_learn.py kb init

# 写前查重 → 分类 → 写入草稿 → 核验 → 查询
python3 scripts/yotta_learn.py kb query 中文检索
python3 scripts/yotta_learn.py kb category list
python3 scripts/yotta_learn.py kb category create agent-skills \
  --name "智能体与技能开发" --description "技能开发与编排相关知识与方法"
python3 scripts/yotta_learn.py kb add --category agent-skills \
  --title "SQLite FTS5 中文检索的坑" \
  --message "默认分词对中文不友好，需要 bigram 或外部分词器。" \
  --tags "sqlite,检索" --source "experiment"
python3 scripts/yotta_learn.py kb review KB-20261005-001 --pass --evidence "本地实测通过"
python3 scripts/yotta_learn.py kb query 中文检索

# 图形化管理台（仅本机）
python3 scripts/yotta_learn.py view
```

**exit code 语义**：0 = 成功；1 = 未找到/无事可做；4 = 用法或校验错误；5 = 门禁阻断（敏感 / 重复）；6 = 完整性（拒绝覆盖 / 数据损坏 / 写锁超时）。

## 安装

以下四种方式任选，顺序即推荐优先级；技能文件一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-learn install --agent <智能体名称>      # 装到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-learn install --dir <智能体的技能目录>  # 指到技能目录本身（如 ~/.codex/skills）
# 旧用法兼容（等价）：npx -y @yottameta/yotta-learn --agent <智能体名称>
```

- `install --agent <name>` 装到该智能体默认用户级目录；`install --list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定的技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），或稍等镜像缓存。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-learn.git <智能体的技能目录>/yotta-learn
```

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-learn` 点 **Code → Download ZIP**，解压后把 `yotta-learn` 文件夹放进智能体技能目录。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。

## 升级 / 卸载

- **升级**：重新安装最新版覆盖即可——重跑你用的安装命令（如 `npx -y @yottameta/yotta-learn install --agent <name>` 或 `bash install.sh --agent <name>`）。技能目录内旧文件会被替换；不影响项目中其他文件。
- **卸载**：删除目标智能体 skills 目录下的 `yotta-learn` 文件夹即可。卸载后本技能不再生效。

## 常见问题

- **新知识写到哪里？** 按归位决策树：私密 → 元忆私密区；项目专属 → 项目自身文件；跨项目可复用 → 知识库（草稿 → 三问审核）；事实 / 红线 → 元忆 FACT；成熟经验 → 技能化。
- **会不会覆盖我已有的数据？** 不会。`kb init` 与旧版 `init` 均为幂等、绝不覆盖已有数据；旧格式条目保持可读。
- **装完没人用怎么办？** 首次加载时 AI 会主动引导激活（检查状态 → 你确认库位置 → 初始化 + 写发现锚点 + MCP 接入 + 自检），之后每次会话按「写 / 查时机」默认动作使用。
- **会记录敏感信息吗？** 不会。私密 / 敏感信息不进入共享知识面（走元忆私密区）；知识库写入有敏感扫描，核验门会阻断。
- **旧的 `.learnings/` 数据怎么办？** 命令全部保留（读取 / 处置 / 迁移）；跨项目条目用 `kb add --from-learning <LRN-ID>` 转成知识库草稿，项目专属条目写进项目自身文件。

## 相关技能

同属 YottaMeta 技能矩阵：[yotta-memory](https://github.com/YottaMeta/yotta-memory)（元忆，跨会话长期记忆）与元习互补——元忆管「事」（事实 / 结论 / 边界 / 私密区），元习管「法」（跨项目可复用的方法 / 流程 / 避坑）；[anti-shallow](https://github.com/YottaMeta/anti-shallow)（防敷衍）与 [workflow-standard](https://github.com/YottaMeta/workflow-standard)（工作流标准）从执行纪律端配合，避免「会沉淀却不严谨」。

## 开发与校验

本项目内运行：`python tools/validate-skill.py yotta-learn`。

## 许可证

MIT © YottaMeta —— 详见 [LICENSE](./LICENSE)。品牌声明见 [NOTICE](./NOTICE)。来源说明：协议与设计参考开源社区 self-improving-agent 类技能思路，实现为 YottaMeta 自有。
