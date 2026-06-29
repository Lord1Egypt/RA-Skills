# repo-explainer

**语言** &nbsp;·&nbsp; [English](README.md) &nbsp;·&nbsp; **简体中文**

> 把任意公开 GitHub 仓库**或本地代码目录**变成一份既好看、又有证据支撑的解读报告 —— 非开发同学能读懂,工程师也信得过。一次运行同时产出 HTML 页面**和**Markdown 文档。

`repo-explainer` 是一条 6 阶段的命令行流水线,输入**公开 GitHub 仓库链接或本地目录路径**,输出两份同步的报告,回答:

- 这个项目到底是干什么的(用大白话讲)?
- 面向谁、解决什么痛点?
- 技术栈、架构、核心数据模型是什么样的?
- 主流程是怎么走的?
- 有哪些诚实的局限与取舍?

每一个结论都引自真实源码,带 `path:line` 引用。报告里出现的每一个文件路径、目录路径和 `path:line` 证据,都是一个可点击的链接,直跳到锁定在 commit SHA 的 GitHub 源码。**本地目录模式**:如果该目录是一个 github.com 远端的 git 检出,链接会自动锚定到工作区的 commit SHA;如果是非 git 目录,证据降级为等宽文本,报告依然完整可读。

---

## 目录

- [核心特性](#核心特性)
- [效果展示](#效果展示)
- [快速开始](#快速开始)
- [主题](#主题)
- [配置](#配置)
- [产物示例](#产物示例)
- [设计理念](#设计理念)
- [仓库结构](#仓库结构)
- [路线图](#路线图)
- [已知局限](#已知局限)
- [非目标](#非目标)
- [贡献](#贡献)
- [许可证](#许可证)

---

## 核心特性

- **双产物 —— HTML + Markdown 并行输出。** 每次运行同时生成一份带主题的单文件 HTML,和一份可粘到任何平台的 Markdown。Markdown 使用原生 ` ```mermaid ` 围栏块,在 GitHub、GitLab、飞书、Notion、Obsidian、Typora、VS Code 预览上都能正确渲染。
- **每个代码路径都是可点击链接。** `path/to/file.ts` 跳转到文件;`dir/` 跳转到目录树;`path/to/file.ts:91` 跳转到第 91 行。URL 都锚定到 commit SHA,链接不会失效。
- **以源码为准,而非营销文案。** 实际扫描仓库源文件(不止 README)。第 4 阶段的 LLM 拿到的是真实路径、真实 LOC 行数、真实 SDK 导入行号 —— 永远不是项目自我宣传的文案。
- **非开发者也能读懂。** Mermaid 节点标签强制使用业务语言(`登录请求`)而非类名(`AuthController`)。内置术语表把每个专有名词翻译成大白话。
- **3 套内置主题。** Midnight(暗色)、Light(打印友好)、Terminal(等宽绿字)。一键切换,通过 `localStorage` 记住选择。
- **架构图自动着色。** 子图按关键词启发式分组并着色,每张图下方自动渲染对应图例。
- **分阶段的时序图。** Mermaid sequence 带 `autonumber` 和 `Note over` 阶段标记。严格的安全规则避开会让飞书 / Notion Mermaid 渲染器崩溃的字符。
- **核心模型表。** 在深入模块细节之前,先提取项目里反复出现的领域类型(struct / class / protobuf),让读者先理解"是什么"再看"怎么做"。
- **诚实的局限。** 每份报告都包含 4–8 条限制卡片,带严重度(高 / 中 / 低)和分类标签。prompt 里明确禁止"需要更多测试"这类套话。
- **单文件 HTML。** 内联 CSS,Mermaid 走 CDN,打印友好(`@media print`),无需任何构建服务。内置一段 JS 点击处理器,保证在严格沙箱 iframe(Mira / 飞书 / Notion 预览面板)里点击代码链接也能正确开新 tab,且绝不会顶替当前页面。
- **主题覆盖机制。** 想改 5 个变量就够的话,丢一个 JSON 文件进来,会被深度合并到基础主题之上。

---

## 效果展示

同一份 `summary.json` 用三套 HTML 主题**和**便携 Markdown 分别渲染了一遍 —— 下面是 [`NousResearch/hermes-agent`](https://github.com/NousResearch/hermes-agent) 的实拍效果。

> 截图为完整页(从 Hero 一直到术语表与页脚),点击可查看大图。

### HTML —— Midnight(默认)

深紫 ⇄ 青色渐变,适合屏幕阅读。

![Midnight 主题预览](https://p-mira-img-sign-sgnontt.byteintl.net/tos-mya-i-xobrcjvdq7/83771931c97a4206b7a0e09e8ae19847.png~tplv-xobrcjvdq7-image-jpeg.jpeg?lk3s=3523e930&x-orig-authkey=miraorigin&x-orig-expires=1781532000&x-orig-sign=F3QPAqxkTz7GCfyGwb5QK8zQapc%3D)

### HTML —— Light

白底蓝调,打印友好,适合嵌入业务报告或导出 PDF。

![Light 主题预览](https://p-mira-img-sign-sgnontt.byteintl.net/tos-mya-i-xobrcjvdq7/c9c398f8c7ac4223854a92efcd26b516.png~tplv-xobrcjvdq7-image-jpeg.jpeg?lk3s=3523e930&x-orig-authkey=miraorigin&x-orig-expires=1781532000&x-orig-sign=845VzIlqktSCuSQ1LQau4WibNlI%3D)

### HTML —— Terminal

黑底霓虹绿等宽,黑客美学,与暗色 IDE 主题相得益彰。

![Terminal 主题预览](https://p-mira-img-sign-sgnontt.byteintl.net/tos-mya-i-xobrcjvdq7/f473b19c3caa436487d1ae3662788358.png~tplv-xobrcjvdq7-image-jpeg.jpeg?lk3s=3523e930&x-orig-authkey=miraorigin&x-orig-expires=1781532000&x-orig-sign=tzFdGGvCrCJkK4YPiPWe%2F2hgNk8%3D)

### Markdown —— 在 GitHub 上的渲染效果

同一份内容,由 `render_markdown.py` 生成,以 GitHub 风格 + 实时 Mermaid 图表渲染。粘到飞书 / Notion / Obsidian 效果一致。

![Markdown 渲染预览](https://p-mira-img-sign-sgnontt.byteintl.net/tos-mya-i-xobrcjvdq7/6bddd00cd39d4597924ce04d9d2f6d18.png~tplv-xobrcjvdq7-image-jpeg.jpeg?lk3s=3523e930&x-orig-authkey=miraorigin&x-orig-expires=1781532000&x-orig-sign=BRJIUtLNlsf20pFZgqzbgh52PPc%3D)

四份产物里的每一个代码路径与 `path:line` 证据都是可点击链接,且都锚定到 commit SHA,读者一键就能去 GitHub 上对证任意结论。

---

## 快速开始

`repo-explainer` 以便携的 **Agent Skill 包**(`repo-explainer.zip`)形式发布 —— 它的目录结构(根目录放 `SKILL.md`,同级放 `scripts/` 与 `templates/`)兼容 Mira、Claude Code、Codex 以及任何遵循 Anthropic 风格 Skill 约定的 agent 宿主。选你常用的那个,或者退回到本地 CLI 跑。

### 选项 A —— 装成 Agent Skill(推荐)

下载最新 skill 包:**`repo-explainer.zip`**(与本仓库同步发布)。然后装到你常用的 agent 里:

#### A1. Mira

- **UI**:任意聊天 → `/find-skills` → **从文件安装** → 选择 `repo-explainer.zip`。
- **编程式**(在另一个 agent 运行里调用):
  ```text
  skill_write(action="enable", skill_type="custom",
              file_uri="<zip 的 URL 或 tos uri>",
              confirmed=false)
  # 看一下预览,再带 confirmed=true 调一次
  ```

#### A2. Claude Code

Claude Code 会自动发现 `~/.claude/skills/` 下的任何 skill 文件夹。解压到那里,下次会话就生效:

```bash
mkdir -p ~/.claude/skills
unzip -d ~/.claude/skills/ repo-explainer.zip
# 验证一下目录结构
ls ~/.claude/skills/repo-explainer/          # → SKILL.md  scripts/  templates/
```

然后开一个 Claude Code 会话触发:

> /skills                                   # 列表里能看到 "repo-explainer"
> explain this repo https://github.com/tiangolo/fastapi

如果要装到某个项目而不是用户全局,把文件夹放到 `<project>/.claude/skills/repo-explainer/`,结构一样,只是仅在那个仓库里可见。

#### A3. Codex CLI

Codex 遵循同样的磁盘约定,解压到 Codex 的 skills 目录:

```bash
mkdir -p ~/.codex/skills
unzip -d ~/.codex/skills/ repo-explainer.zip
# (或者 repo 内:<project>/.codex/skills/repo-explainer/)
```

然后在任意 Codex 聊天里:

> @repo-explainer https://github.com/NousResearch/hermes-agent

#### A4. 试一下

在上述任意一个宿主装好后,直接在聊天里贴 **GitHub 链接或本地目录路径**触发:

> 解读这个项目 https://github.com/tiangolo/fastapi
>
> explain this repo https://github.com/NousResearch/hermes-agent
>
> 分析下这个目录 ~/code/my-side-project
>
> explain this folder /Users/me/work/checkout-service

Skill 会自动跑完 6 个阶段,返回两个产物:一份精致的 HTML 报告 + 一份可粘任意位置的 Markdown 报告。无需本地 Python 环境 —— agent 沙箱内置 `python3`、`git`、`jq` 与一个上下文里的 LLM。

### 选项 B —— 本地 CLI 跑流水线

适合批处理任务、CI 集成,或者你手边没有 agent 宿主的场景。

> 前置:**Python 3.9+**(只用 stdlib)、**git**、**jq**,以及一个可以从命令行 prompt 的 LLM。

```bash
# 1. 拿到包
unzip repo-explainer.zip            # 或: git clone <本仓库>
cd repo-explainer/

# 2. 对任意公开 GitHub URL 跑 6 阶段流水线 …
TARGET="https://github.com/tiangolo/fastapi"

#    …… 或者直接对本地目录跑(参数是已存在的路径会自动识别,
#    歧义时加 --local 强制)。如果目录是 github.com 远端的 git 检出,
#    owner / repo / branch / commit SHA 会从 .git/config 自动恢复,
#    `path:line` 证据照样是可点击的 GitHub 永久链接。
# TARGET="/home/me/code/my-side-project"
# TARGET="~/work/checkout-service"

# 阶段 1–3 是确定性 Python,无 LLM,只用 stdlib
python3 scripts/fetch_repo.py      "$TARGET"                                > meta.json
python3 scripts/scan_structure.py  "$(jq -r .local_path meta.json)"         > scan.json
python3 scripts/analyze_modules.py "$(jq -r .local_path meta.json)" scan.json > analysis.json

# 阶段 4 —— 综合(整条流水线里唯一需要 LLM 的步骤)
#   把 analysis.json + scan.json 喂给你的 LLM,用
#   templates/summary.schema.json 作为严格的输出契约。
#   结果存为 summary.json。

# 阶段 5a —— 带主题的 HTML(单文件,自包含)
python3 scripts/render_html.py summary.json \
        --meta_json   meta.json \
        --file_count  "$(jq '.structure.total_files' scan.json)" \
        --theme       midnight \
        > report.html

# 阶段 5b —— 便携 Markdown(原生 Mermaid,粘哪都能渲染)
python3 scripts/render_markdown.py summary.json \
        --meta_json   meta.json \
        --file_count  "$(jq '.structure.total_files' scan.json)" \
        > report.md
```

`report.html` 用任意浏览器打开;`report.md` 直接粘到 GitHub、GitLab、飞书、Notion 或 Obsidian 即可。

> **提示** —— 只有阶段 4 需要 LLM。其余 5 个阶段都是确定性 Python,可离线运行。整条流水线**没有任何 `pip` 依赖**,仅依赖 Python 标准库。

---

## 主题

`templates/themes.json` 内置 3 套主题,每套都包含:

- 30+ 个 CSS 变量(背景、前景、强调色、Hero 渐变、图表底色 / 边框 / 阴影 等)
- 一整套 Mermaid `themeVariables`(primaryColor、clusterBkg、actorBkg、loopTextColor、edgeLabelBackground 等)
- 架构节点的 5 色调色板:`user / core / module / kernel / store`

| 主题 | 适用场景 | 风格 |
|---|---|---|
| `midnight` | 默认;屏幕阅读 | 深紫 ⇄ 青色渐变 |
| `light` | 打印 / 商务文档 | 白底蓝调 |
| `terminal` | 黑客美学 | 黑底霓虹绿等宽 |

渲染时切换:

```bash
python3 scripts/render_html.py summary.json --meta_json meta.json --theme light > report.html
```

也可以点击报告右上角的主题切换按钮 —— Mermaid 实时重渲染,选择通过 `localStorage` 记住。

---

## 配置

### 自定义主题覆盖

只想换个品牌色、不想把 30 个变量全抄一遍?把差异丢进一个 JSON 文件:

```json
{
  "css_vars": {
    "--bg": "#fdf6e3",
    "--fg": "#073642",
    "--accent": "#268bd2",
    "--hero-grad": "linear-gradient(135deg, #268bd2 0%, #2aa198 100%)"
  },
  "fonts": {
    "primary": "'Source Sans Pro', sans-serif"
  },
  "mermaid": {
    "themeVariables": { "primaryColor": "#eee8d5", "lineColor": "#586e75" }
  },
  "diagram_class_palette": {
    "user":   { "fill": "#eee8d5", "stroke": "#268bd2", "color": "#073642" },
    "core":   { "fill": "#fdf6e3", "stroke": "#6c71c4", "color": "#073642" },
    "module": { "fill": "#eee8d5", "stroke": "#2aa198", "color": "#073642" },
    "kernel": { "fill": "#fdf6e3", "stroke": "#dc322f", "color": "#073642" },
    "store":  { "fill": "#eee8d5", "stroke": "#859900", "color": "#073642" }
  }
}
```

然后叠加在所选基础主题之上(以 Midnight 为例):

```bash
python3 scripts/render_html.py summary.json \
        --meta_json meta.json \
        --theme midnight \
        --theme-override my-brand.json \
        > report.html
```

覆盖会被深度合并到基础主题上,所以你永远不需要复制整份文件。

### CLI 参考

**HTML 渲染器**(`render_html.py`)

```text
python3 scripts/render_html.py <summary.json> [OPTIONS]

  --meta_json <path>          (必填)Stage 1 产出的 meta.json
  --file_count <int>          总文件数,显示在 Hero 区
  --theme <name>              midnight(默认) | light | terminal
  --theme-override <path>     深度合并的覆盖 JSON 文件
```

**Markdown 渲染器**(`render_markdown.py`)

```text
python3 scripts/render_markdown.py <summary.json> [OPTIONS]

  --meta_json <path>          (必填)Stage 1 产出的 meta.json
  --file_count <int>          总文件数,显示在 Hero badge 里
```

Markdown 渲染器纯 Python 标准库 —— 无外部依赖、无主题(颜色交给宿主)。产物对任何支持 GitHub-flavored Markdown + ` ```mermaid ` 围栏块的平台都开箱即用。

---

## 产物示例

一次运行从同一份 `summary.json` 产出两份同步产物:

| 格式 | 适用场景 | 渲染效果最好的平台 |
|---|---|---|
| **`report.html`** | 分享精致的链接、打印、嵌入 dashboard、归档 | 任意现代浏览器(可离线,单文件) |
| **`report.md`** | 粘到 wiki / 群聊 / issue tracker、在 PR 里 code-review、与源码同源版本控制 | GitHub、GitLab、飞书、Notion、Obsidian、Typora、VS Code 预览 |

两份产物章节顺序相同、`path:line` 证据链接相同、Mermaid 源相同。

### 报告内有什么

Hero(项目名 + 一句话简介 + 仓库元数据)→ TL;DR 卡片 → 技术栈表 → 架构图 → **核心模型**表 → **每个关键模块详解**(职责 / 原理 / 子流程 / 证据)→ 主流程时序图 → 对外接口 → 关键依赖 → 项目特色 → **限制概览 + 详情** → 术语对照。

### 链接约定

| 引用形态 | 解析为 | 示例 URL |
|---|---|---|
| `src/cli.ts` | `/blob/<sha>/src/cli.ts` | 跳到文件 |
| `src/ingest/` | `/tree/<sha>/src/ingest` | 跳到目录列表 |
| `src/cli.ts:91` | `/blob/<sha>/src/cli.ts#L91` | 跳到第 91 行 |

Markdown 里链接的可见文本就是路径本身(不在文本里嵌反引号 —— 某些宿主的粘贴行为会因此崩坏)。HTML 里每个代码引用都带一个小小的 `↗` 图标,鼠标悬停时显示下划线,一眼能看出是链接。

---

## 设计理念

### 1. 以源码为准,而非营销

阶段 2 与阶段 3 读真实源文件;阶段 4 的 LLM 拿到的是真实路径、真实 LOC、真实 SDK 导入行号 —— 永远不是仓库自我宣传的 README。每条结论都附一条 `path:line` 可点击链接,锚定到 commit SHA 的源码。

### 2. 非开发者读得懂,工程师信得过

Mermaid 节点标签强制业务语言(`告警事件`,而不是 `AlertEventDto`)。术语表翻译每个专有名词。工程师仍可以通过每个模块卡上的"原理 + 证据"清单深挖。

### 3. 视觉即信任

三层视觉打磨,让读者愿意去打开第二份报告:

- Mermaid `themeVariables` 每套主题覆盖 30+ 细粒度颜色
- 子图节点自动归到 5 类、各自上色,并配一份图例
- 图表容器自带径向渐变背景、3px 顶部品牌色条、SVG 阴影滤镜、圆角节点和虚线 cluster 边框

### 4. 每个引用都可点,每次点击都有效

代码路径与 `path:line` 证据都锚定到 commit SHA,链接不会腐烂。HTML 用一段 JS 点击处理器调用 `window.open(href, '_blank')`(带 `top.location` 和同帧降级),保证每个链接都干净地打开新 tab —— 即使是在 Mira / 飞书 / Notion 预览 iframe 这种 `target="_blank"` 会被静默吃掉的严格沙箱里,也不会顶替当前页。Markdown 里链接文本不带反引号,所以飞书 / Notion 的粘贴处理器能正确显示可见标签,而不会泄漏出原始 URL。

### 5. 诚实的局限是必选项

阶段 4 的 schema 要求每份报告 4–8 条 `limitations`。允许的来源:源码里 grep 出来的 TODO/FIXME/XXX 注释、README 中的已知问题,或显然的架构缺口。prompt 里明确禁止"需要更多测试"这类套话。

---

## 仓库结构

```
repo-explainer/
├── README.md                     # 英文版(默认)
├── README.zh-CN.md               # 本文件
├── SKILL.md                      # Agent-skill manifest + workflow 契约
├── scripts/
│   ├── fetch_repo.py             # 阶段 1 —— 浅克隆(或就地分析本地目录) + GitHub REST 元数据
│   ├── scan_structure.py         # 阶段 2 —— 目录树 / LOC / manifest
│   ├── analyze_modules.py        # 阶段 3 —— 模块排序 / SDK / 路由
│   ├── render_html.py            # 阶段 5a —— 主题化单文件 HTML
│   └── render_markdown.py        # 阶段 5b —— 任意平台可粘 Markdown
└── templates/
    ├── summary.schema.json       # 阶段 4 LLM 输出契约(JSON Schema draft-07)
    └── themes.json               # 3 套内置主题 + 5 类图表调色板
```

---

## 路线图

- **Monorepo 深扫描** —— 当根目录只有一个 `src/` 时,深入一层而不是把 `top_modules` 折叠成一项
- **GitLab / Bitbucket 适配** —— 当前仅支持 GitHub
- **`--subpath` 自动建议** —— 仓库超过 500 MB 时,建议前 3 大的子目录
- **SDK 字典扩充** —— `analyze_modules.py:SDK_HINTS` 现在是硬编码,缺失项(eBPF、MCP、Qwen 等)会静默丢失
- **PDF / PNG 导出** —— 内嵌一个 headless 渲染器
- **i18n** —— 当前 prompt 与 schema 字段偏中文输出,计划增加英 / 日 / 韩等变体

---

## 已知局限

| # | 局限 | 应对 |
|---|---|---|
| 1 | SDK 识别基于字典,小众 SDK 会漏 | 扩 `analyze_modules.py:SDK_HINTS`,或让阶段 4 的 LLM 兜底 |
| 2 | 顶层只有 `src/` 的 monorepo 会被折叠成一项 | 手动 `--subpath packages/<name>` |
| 3 | 超过 500 MB 的仓库直接拒绝 | 用 `--subpath` 聚焦克隆 |
| 4 | 仅公开 GitHub —— 不支持 GitLab / Bitbucket / 私有仓库 | fork `fetch_repo.py` 加适配器 |
| 5 | 无 call-graph 追踪、无安全审计 | 不在范围,请用专用工具 |

---

## 非目标

本项目**不**试图成为:

- 安全扫描器或漏洞审计工具
- 代码审查或重构建议引擎
- 项目运行手册或安装指南
- 多仓库对比 / 基准测试工具
- 深度调用图追踪器

它只做一件事:解读一个仓库。

---

## 贡献

欢迎 PR。最简单的贡献是新增一套主题 —— 按现有 schema 在 `templates/themes.json` 里加一个 JSON 对象即可。流水线相关变更:

1. Fork 后建一个 feature 分支
2. 至少跑一个真实仓库做端到端验证(`tiangolo/fastapi` 是不错的烟测对象)
3. PR 里附一张生成报告的截图
4. 如果引入新能力,在路线图里加一行简介

更大的想法(新阶段、新图表类型、新导出器),先开 issue 一起讨论设计。

---

## 致谢

- [Mermaid.js](https://mermaid.js.org/) —— 流程图与时序图
- [Inter](https://rsms.me/inter/)、[JetBrains Mono](https://www.jetbrains.com/lp/mono/)、[Fira Code](https://github.com/tonsky/FiraCode) —— 字体
- [GitHub REST API v3](https://docs.github.com/en/rest) —— 仓库元数据
- 灵感来自 `deepwiki`、`gitingest`、`gitsummary`;本项目专注于**让非工程师也能读懂**这一点。

---

## 许可证

MIT —— 详见 [LICENSE](LICENSE)。
