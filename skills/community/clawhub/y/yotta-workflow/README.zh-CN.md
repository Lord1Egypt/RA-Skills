<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-workflow banner" width="100%" />
</p>

<h1 align="center">yotta-workflow · 元序</h1>

<p align="center">一套面向所有 AI 智能体的通用工作流标准：<b>流程全局定、状态跟项目根目录；开工必读状态，收工必留锚点</b>。让任何 AI 会话都能无痛接续，避免单会话拉长而失忆。</p>
<p align="center">状态目录统一 <code>.workflow</code>——同一项目所有智能体会话读写同一份状态（一个真相源）；开工读状态恢复上下文、进行中主动落盘流水 / 任务 / 决策、收工生成自包含交接锚点。</p>
<p align="center">纯 Markdown 文本，零依赖、不注入、不锁平台；安装一次，Claude Code / Codex / Cursor / OpenCode 等 78+ 智能体通用。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-workflow"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-workflow" /></a>
  <a href="https://github.com/YottaMeta/yotta-workflow"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-workflow" /></a>
  <a href="https://github.com/YottaMeta/yotta-workflow/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-workflow" /></a>
  <a href="https://github.com/YottaMeta/yotta-workflow"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## 这是什么

AI 会话本身是无状态的：每次对话相互独立，聊得越长越容易失忆，换个会话或换个智能体就接不上前文。各平台自带的记忆方案通常只服务单一智能体，不同智能体各记各的，还会产生多个「真相源」。

yotta-workflow 把「跨会话协作」沉淀为一套与智能体无关的协议，回答三个问题：

- **状态放哪里、以什么格式记录**——统一由规则判定，不靠各智能体自由发挥。
- **什么时候读、什么时候写**——开工必读、进行中主动写、收工必留锚点。
- **交接怎么交**——固定模板生成自包含交接锚点，下个会话只凭锚点即可无痛接续。

它不依赖任何特定智能体或平台：状态就是项目目录下的 Markdown 文件，任何智能体、任何工具都能读能写。

## 核心价值

- **一个真相源**：同一项目所有智能体会话读写同一份 `.workflow\` 状态目录，不再各建目录、各记各的。
- **状态跟着项目根目录走**：`.workflow` 只放项目根目录，不放源码目录，也不放工作区根；已有 `.workflow` 就近沿用、不自动迁移。
- **主动防失忆**：进行中每完成一件事就落盘流水 / 任务 / 决策，不靠对话记忆（上下文会被自动压缩）。
- **自包含交接**：收工生成固定格式交接锚点，下个会话只凭锚点 + 状态文件即可恢复全部上下文。
- **与既有机制兼容**：项目已有自己的交接 / 状态机制时沿用原机制，只需满足两个强制点——开工先读状态、收工更新状态并留锚点。

## 核心优势

| 优势 | 说明 |
|---|---|
| **跨智能体统一** | 符合 Agent Skills 开放标准（agentskills.io），安装一次，78+ 智能体共用同一套状态协议 |
| **一个真相源** | 状态目录统一 `.workflow`，同一项目任何智能体读写同一份状态，杜绝多真相源 |
| **路径判定无歧义** | 只认用户明确指定或向上找到已有 `.workflow`；两种证据都没有就先问，不靠 `.git` / cwd 猜 |
| **主动式落盘** | 进行中即时写流水 / 任务 / 决策，上下文压缩也不丢关键状态 |
| **自包含交接锚点** | 固定模板 + 强制校验（内容必须与状态文件一致），下个会话无痛接续 |
| **轻量零依赖** | 纯 Markdown 文件，无 daemon / 无数据库 / 无注入；任何平台可读可写 |
| **渐进采用** | 已有状态机制的项目可沿用原机制，只需满足两个强制点，迁移成本低 |
| **生态分发** | GitHub + npm 双源同步发布；npx / git clone / Download ZIP / install.sh 四种安装方式，覆盖 17+ 类智能体目录 |

## 协议详解

### 路径模型与状态文件位置判定

**先分清三个概念：项目根目录是拥有整个项目状态的目录，也是 `.workflow` 的唯一锚点；源码目录默认是项目根目录下的代码子目录；工作区根只是并列多个项目根目录的父目录。**

| 目录 | 定义 | `.workflow` 放哪 |
|---|---|---|
| **项目根目录** | 拥有整个项目状态的父目录；默认承载 `.workflow` 和源码目录 | `<项目根目录>\.workflow\` |
| **源码目录** | 项目根目录下的代码目录；可以有独立 `.git` | 不放，除非用户明确说明它同时就是项目根目录 |
| **工作区根目录** | 并列多个项目根目录的容器；不拥有某个项目的状态 | 不放；先选具体项目根目录 |

```text
<项目根目录>\
├── .workflow\         # 工作流；直接放在项目根目录
└── <源码目录>\        # 源码目录；位于项目根目录之下
```

**定位顺序（只认两种证据）：**

1. 用户明确指定项目根目录 → 直接用。
2. 从 cwd 向上查找已有的 `.workflow\STATE.md` → 找到最近的，其父目录就是项目根目录；**永不自动迁移**。
3. 两种证据都没有 → 先问“项目根目录是哪一个？”，不得用 `.git`、`package.json`、`src`、`README`、cwd 或目录结构自行猜测。

> 本技能只规定标准形态与状态位置；实际项目中源码目录怎么命名、怎么分层，由用户按项目情况调整。

### 项目状态体系（五类文件）

| 文件 | 内容 |
|---|---|
| `STATE.md` | 当前进度 / 最近决定 / 遗留问题 / 下一步（下个会话恢复的关键） |
| `TASKS.md` | 任务清单（`- [ ]` 待办 / `- [x]` 已完成 / `- [~]` 进行中） |
| `DECISIONS.md` | 决策记录（每条含背景 / 决定 / 理由 / 备选） |
| `ROADMAP.md` | 长期目标 + 下一步计划 |
| `logs\YYYY-MM-DD.md` | 每天一份流水（做了什么 / 产出什么 / 踩了什么坑） |

### 三段式协议

**开工（每次会话开始必做）**：按判定规则定位状态目录 → 存在则完整读取 STATE / TASKS / ROADMAP / DECISIONS 与近期 logs 恢复上下文；不存在则初始化全部文件并向用户确认；一个会话只交付一个里程碑。

**进行中（主动及时写，不靠记忆）**：每完成一件事就追加当天流水；任务状态实时更新 TASKS；方向性决定当场写入 DECISIONS；STATE 的「当前进度」保持最新；关键信息必须已落盘，不能只留在对话里。

**收工（每次会话结束必做）**：更新 STATE / TASKS / ROADMAP → 追加当天流水 → 按模板生成交接锚点，原样输出给用户复制。

### 交接锚点格式

收工时按固定模板输出，锚点必须自包含，内容必须与状态文件一致、不得凭空编写。完整模板见 SKILL.md「五、交接话术模板」，结构要点：

| 段 | 内容 |
|---|---|
| 头部 | 项目名（一句话定位）、项目根目录绝对路径、上次会话结束日期 |
| 进度 | 当前进度、已完成（与 STATE.md 一致） |
| 后续 | 下一步（按优先级）、关键决定、遗留问题 / 注意 |
| 结尾 | 开工请先读取：`.workflow\STATE.md`、TASKS.md、ROADMAP.md |

## 使用示例

**开工**——先读状态，再谈任务：

```text
请先读取 .workflow\STATE.md、TASKS.md、ROADMAP.md，恢复项目上下文。
```

**进行中**——完成一件事，立即落盘：

```text
已完成「xxx」，追加到 logs\2026-08-25.md；勾选 TASKS.md 对应项；更新 STATE.md 当前进度。
```

**收工**——按模板生成交接锚点：

```text
给你的下个会话锚点

【会话交接锚点】
项目：<项目名>（<一句话定位>）
路径：<项目根目录绝对路径>
上次会话结束于：<日期>
当前进度：…
下一步（按优先级）：…
开工请先读取：.workflow\STATE.md、TASKS.md、ROADMAP.md
```

## 触发方式

在以下场景使用本技能：

- 开始或结束一个工作会话，或恢复一个项目时。
- 项目状态发生变化时（完成任务 / 记录决策 / 更新路线图）。
- 需要给下一个会话留下自包含交接锚点，或读取已有交接锚点时。

针对一次性的只读提问（如「这个函数什么意思」）不必触发本技能。

## 安装

以下四种方式任选，顺序即推荐优先级；技能文件一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-workflow@0.4.5 --agent <智能体名称>      # 装到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-workflow@0.4.5 --dir <智能体的技能目录>  # 指到技能目录本身（如 ~/.codex/skills）
```

- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定的技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），或稍等镜像缓存。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-workflow.git <智能体的技能目录>/yotta-workflow
```

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-workflow` 点 **Code → Download ZIP**，解压后把 `yotta-workflow` 文件夹放进智能体技能目录。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。
## 升级 / 卸载

- **升级**：重新安装最新版覆盖即可——重跑你用的安装命令（如 `npx -y @yottameta/yotta-workflow@0.4.5 --agent <name>` 或 `bash install.sh --agent <name>`）。技能目录内旧文件会被替换；项目里的状态文件（`.workflow\`）不受影响。
- **卸载**：删除目标智能体 skills 目录下的 `yotta-workflow` 文件夹（各智能体目录见上表）。卸载不影响已写入项目的状态文件。

## 常见问题

- **状态目录在哪？** 先认用户明确指定的项目根目录，再从 cwd 向上找已有 `.workflow\`；两者都没有就先问。状态始终放 `<项目根目录>\.workflow\`，不放源码目录或工作区根。
- **多个智能体状态不同步？** 确认它们指向同一项目目录（同一份 `.workflow\`）。本技能设计为共享一份状态；若各自建了 `.workflow`，说明项目目录不一致。
- **源码目录里有 `.git`，状态应该放那里吗？** 不应只凭 `.git` 判断；状态只放项目根目录下的 `.workflow`。源码目录的具体组织由用户决定。
- **项目已有自己的交接机制？** 沿用原机制即可，只需满足两个强制点：开工先读状态、收工更新状态并留锚点。

## 开发与校验

本项目内运行：`python tools/validate-skill.py yotta-workflow`。

## 参考文档

- references/faq.md
- references/path-model.md
- references/walkthroughs.md
- references/exception-playbook.md

## 许可证

MIT © YottaMeta
