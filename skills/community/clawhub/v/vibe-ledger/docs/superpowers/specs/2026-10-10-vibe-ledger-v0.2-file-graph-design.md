# vibe-ledger v0.2 设计文档：文件流程图 + 点开即讲解

- 日期：2026-10-10
- 状态：待审（设计已在对话中逐段确认，页面布局和节点样式通过浏览器样稿选定）
- 基于：`2026-10-09-vibe-ledger-design.md`（v0.1）。v0.1 的流水线、账本、校验、探针全部保留，本文只写新增和改动的部分。

## 1. 为什么要改

v0.1 在 5 个测试应用上全部通过，但在一个真实的 Chrome 扩展项目上试跑后，用户的结论是“没太看懂”，并明确说出真正想要的形式：

> 一个可视化很好的流程图，显示文件之间的联系调用，同时例如点击文件，可以获取文件的讲解。

v0.1 的图表围绕五个抽象问题（数据存在哪、谁能看到……），没有给出“这个项目由哪些文件组成、它们怎么连起来”的心智模型。v0.2 把**项目自己的文件结构**作为主视图，把讲解、风险、承诺、来历都挂到文件上。

## 2. 已确定的决定

| 问题 | 决定 |
|---|---|
| 主视图 | 分层流程图：从左到右“入口/界面 → 逻辑 → 数据与外部”，箭头表示谁调用谁 |
| 页面布局 | 左图右讲解（并排）；手机上改为上下排 |
| 节点样式 | 彩色卡片加图标：按类型着浅色底，配图标 ▶ 入口、ƒ 逻辑、⛁ 数据、✦ 付费服务、▤ 文件夹 |
| 讲解内容 | 用途和上下游、主要函数、风险与问题、来历（有对话记录时） |
| 讲解覆盖 | 重点文件由 AI 详讲（最多 30 个），其余由脚本生成简版 |
| 旧报告 | 风险、承诺、来历并入文件讲解；五问区、对账表、覆盖范围放进第二个标签页“总览” |
| 排版 | dagre（`@dagrejs/dagre`，MIT，2026-08 仍在维护）负责分层排版，绘制和交互自己做；不用 elkjs（EPL/GPL 许可证） |

## 3. 图里画什么

### 3.1 节点

- **文件节点**：项目里的源码文件，包括 JS/TS 一家（`.js .jsx .ts .tsx .mjs .cjs .vue .svelte`）和 Python（`.py`）。
  - 默认排除测试文件（路径含 `test/ tests/ __tests__/ spec/ fixtures/`，或文件名形如 `*.test.* *.spec.*`）和配置文件（`*.config.*`、`.eslintrc*` 等）；排除的数量写进“这份报告没看到什么”。
  - 依赖和构建目录沿用 v0.1 的 `SKIP_DIRS`，`vendor/` 等目录也在其中。
- **数据与外部节点**：只为“值得一看”的外部依赖建节点，每个都要有代码证据（出现位置的文件、行号、片段）：
  - **付费服务（✦，橙）**：AI 服务的 SDK（openai、@anthropic-ai/sdk、@google/genai、@google/generative-ai、groq-sdk、cohere-ai、replicate、elevenlabs）、stripe、twilio、resend，以及代码里请求的已知付费 API 地址（`api.openai.com`、`api.anthropic.com`、`api.deepseek.com`、`generativelanguage.googleapis.com`、`api.stripe.com` 等）。
  - **数据（⛁，绿）**：@supabase/supabase-js、@supabase/ssr、firebase、firebase-admin、prisma、pg、mysql2、mongoose、redis，代码里出现的 `*.supabase.co` 地址，以及浏览器存储 API（`localStorage`、`sessionStorage`、`indexedDB`、`chrome.storage`）。
  - 普通工具库（react、lodash 等）不画。

### 3.2 连线

用静态分析提取“谁引用谁”：
- **JS/TS**：`import … from '…'`、`import '…'`、`export … from '…'`、`import('…')`、`require('…')`。
- **Python**：`import a.b`、`from a.b import c`、`from . import x`、`from ..pkg import y`。
- **路径解析**：
  - 相对路径；
  - tsconfig/jsconfig 里 `compilerOptions.paths` 加 `baseUrl` 定义的别名；
  - 没有配置时，`@/` 依次尝试 `src/` 和项目根目录，`~/` 指项目根目录；
  - 可省略的扩展名（`.ts .tsx .js .jsx .mjs .cjs .vue .svelte`）；
  - 目录下的 `index.*` 文件；
  - Python 包的 `__init__.py`。
- **连线信息**：每条连线记录引用发生的行号，以及引用了哪些名字（能解析出来时）。
- **兜底**：解析不了的本地引用（以 `.`、`@/`、`~/` 开头，或命中了某个别名）列进 `unresolved`，并在报告里列出，不会悄悄丢掉。
- **文件到外部节点的连线**：引用了上面那些 SDK 的文件，或代码里出现了已知 API 地址、浏览器存储 API 的文件，各连一条线到对应的外部节点。

### 3.3 入口

按以下规则识别入口（命中任意一条即可），每个入口都记下识别理由：

| 技术栈 | 规则 |
|---|---|
| Next.js | `app/**/page.*`、`app/**/route.*`、`pages/**`（`_app`、`_document` 除外） |
| Chrome 扩展 | `manifest.json` 里的 `background.service_worker`、`content_scripts[].js`、`side_panel.default_path` / `action.default_popup` / `options_page` 指向的 HTML 里 `<script src>` 引用的脚本 |
| Vite / 静态页 | 根目录或 `public/` 的 `index.html` 里 `<script src>` 引用的脚本 |
| package.json | `main` 和 `bin` 指向的文件 |
| Express / Node 服务 | 出现 `.listen(` 的文件 |
| Python | 含 `if __name__ == "__main__":` 的文件、`app.py`、`main.py`、`manage.py` |

一个入口都识别不出来时，把“没有被任何文件引用的文件”当作入口。

### 3.4 分层和排版

- **dagre 参数**：`rankdir: LR`。
- **入口放最左**：加一个不可见的起点，连到所有入口。
- **外部节点放最右**：加一个不可见的终点，所有外部节点连到它。
- **其余文件**：层次和顺序交给 dagre，它负责减少交叉、处理循环引用。
- **三条背景色带**：按节点角色计算，入口所在的列为“入口 / 界面”，外部节点所在的列为“数据与外部”，中间为“逻辑”。

### 3.5 大项目

图里的文件节点超过 **80** 个时：
- 默认折叠成文件夹节点（▤，虚线框），节点上写“N 个文件 · 点开展开”。按哪一层文件夹折叠：从项目根往下找，选**能把文件分成至少 3 组的最浅一层**（例如所有文件都在 `src/` 下时，用 `src/ai`、`src/ui` 这一层）；直接位于这一层的单个文件保持为普通节点；
- 文件夹之间的连线合并成一条，线上标注合并了几条引用；
- 点击文件夹节点展开或收起，展开后 dagre 重新排版；
- 提供“全部展开 / 全部折叠”按钮；
- 有问题的文件所在的文件夹也显示红色或黄色角标。

## 4. 文件讲解

### 4.1 自动部分（脚本生成，每个文件都有）

- **对外提供什么**：导出的函数和类，附行号（JS/TS 的 `export` 声明、`module.exports` 的成员；Python 的顶层 `def` / `class`）。
- **它调用谁、谁调用它**：都可以点击跳转。
- 它碰到的数据与外部节点。
- 行数。
- 风险和承诺（见 4.4）。

### 4.2 AI 详讲（重点文件，最多 30 个）

**挑选**：脚本给每个文件打分，取前 30 名；同分时按路径排序。分数构成：

| 条件 | 分数 |
|---|---|
| 是入口 | +3 |
| 有 ❌ 承诺、仍在代码里的妥协，或“确定”级发现 | +3 |
| 有 ⚠/⏳ 承诺或“仅提示”级发现 | +1 |
| 被多少个文件引用 | 每个 +1，最多 +5 |
| 连到数据或外部节点 | +2 |
| 在对话里被改过的次数 | 每 3 次 +1，最多 +3 |

**交给 AI 的材料**：`explain_pack.md` 列出要讲的文件和每个文件的自动事实，并说明写法。AI 读这些文件后写 `explain.json`（格式见 6.2），每个文件包括：
- `purpose_plain`：大白话 1–3 句，让不会写代码的人看懂这个文件管什么；
- `purpose_dev`：一句开发者版本；
- `functions`：主要函数，每个包含 `name`、`line` 和一句话 `plain`；
- `history`：只在有对话记录时写，每条附上对话引文的证据编号。

**分块**：要讲的文件超过 8 个时，每组约 8 个交给一个子 agent，各自写 `parts/explain_NN.json`，再由 `vl.py merge` 合并。

### 4.3 核对（`explain.py`）

1. **路径**：必须是图里的文件节点，否则整张卡片作废，退回只显示自动部分，并记入覆盖范围一节。
2. **函数**：`name` 必须在这个文件里定义过。认可的写法：
   - JS/TS：`function NAME`、`async function NAME`、`export (default) (async) function NAME`、`const|let|var NAME = (async) (function | (…) => | x =>)`、`class NAME`、类方法 `(async) NAME(…) {`、对象方法 `NAME(…) {` / `NAME: (async) function` / `NAME: (…) =>`；
   - Python：`def NAME(`、`async def NAME(`、`class NAME`。

   `line` 落在真实定义行前后 3 行以内算通过；偏得更多、但这个名字在文件里只定义了一次时，自动更正行号；其余情况删掉这条函数讲解，并记录原因。
3. **用途**：`purpose_plain` 和 `purpose_dev` 里用反引号括起来的标识符，每个都必须作为完整单词出现在项目源码里，或者就是图里的某个文件名；有一个找不到，这段用途就标成“未核实”。页面上照样显示，但加“未核实”标记和原因。
4. **来历**：引文按 v0.1 的规则校验，要能在对话里逐字找到，时间从日志读取。没通过的那条来历删掉。
5. **格式**：严格检查，缺字段或类型不对就列出全部问题，并以退出码 2 结束，和 `vl.py check` 校验账本时的做法一致。

### 4.4 v0.1 的结果挂到文件上

- **哪些结果算到某个文件上**：
  - 检查脚本的发现：路径就是这个文件；
  - 已校验的承诺：有任何一条代码或探针证据指向这个文件（显示状态标签，并能跳到“总览”页的对应卡片）；
  - 报错后的妥协：`now` 证据指向这个文件；
  - 对话里对这个文件的改动：次数、第一次和最后一次的日期。
- **节点状态**：
  - 红框加角标“N 个问题”：有 ❌ 承诺、仍在代码里的妥协，或“确定”级发现；
  - 黄框加角标“N 个提示”：只有 ⚠/⏳ 承诺或“仅提示”级发现；
  - 连线标红：任一端的文件有问题时。

## 5. 页面和交互

### 5.1 结构

单个 HTML 文件，可以离线打开。dagre 的压缩版放在 `scripts/ledger_report/vendor/dagre.min.js`，附 `LICENSE-dagre`（MIT），渲染时整段内联进页面。支持浅色和深色模式，沿用 v0.1 的 CSS 变量体系。

- **顶部栏**：项目名；“文件流程图 | 总览”两个标签页；搜索框（按文件名过滤，回车后图移过去并选中）；“大白话 ⇄ 开发者”视图切换。
- **左侧流程图**（宽度约 63%）：
  - 拖动画布平移，滚轮缩放，右上角有“+ / − / 适应窗口”按钮；
  - 图例画在画布左下角。
- **右侧讲解面板**（宽度约 37%，位置固定，内容可以独立滚动）。

### 5.2 交互

- **点击文件节点**：
  - 该节点用紫色描边，它的上游和下游节点保持原样；
  - 连到它的线加粗、变紫；
  - 其余节点透明度降到约 0.28，其余连线降到约 0.18；
  - 面板显示这个文件的卡片。
- **取消选中**：点击空白处或按 Esc。
- **面板里的文件名**：可以点击，点了图会平移到那个文件并选中它。
- **没有选中文件时，面板显示**：
  - 一句项目概览（脚本生成：N 个文件、M 个入口、连到 K 个外部服务，其中 P 个按次收费）；
  - “这张图怎么读”三行说明；
  - 问题最多的前 3 个文件，点一下直接跳过去。
- **开发者视图**：面板里额外显示完整路径、行数、函数行号、每个函数定义处前后的代码片段（已打码，最多 8 行）；连线上标注引用了哪些名字。
- **网址参数**：`?select=<文件路径>` 打开时直接选中这个文件，`?theme=dark` 切到深色，`?view=dev` 切到开发者视图。主要给截图检查用。

### 5.3 卡片（大白话视图）

依次显示：
1. 文件名、所在文件夹、类型标签；
2. 用途（AI 详讲，或“暂无详细讲解”加自动摘要）；
3. 它调用 → / 谁调用它 ←（可点击的文件名）；
4. 主要函数（AI 详讲时显示每个函数的一句话；否则只列出导出的名字）；
5. 风险与问题（来自 4.4，附证据，可以展开）；
6. 来历（有对话记录时显示；没有时写明“没有对话记录”）。

### 5.4 手机

宽度小于 760px 时改为上下排列：图在上，高度约为屏幕的 55%，可以拖动、双指缩放；面板在下。

### 5.5 安全

- 页面数据整体以 `<script type="application/json">` 嵌入，写入前所有字符串先打码，`</` 转义成 `<\/`。
- 面板和节点文字一律用 `textContent` 写入，不用 `innerHTML`。
- 写出页面前沿用 v0.1 的 `assert_no_secrets` 检查。

## 6. 数据格式

### 6.1 `graph.json`（`vl.py start` 生成）

```jsonc
{
  "nodes": [{"id": "src/ai/directApiClient.js", "label": "directApiClient.js", "folder": "src/ai",
             "role": "logic",            // entry | logic
             "lines": 260,
             "exports": [{"name": "createDirectApiClient", "line": 52}],
             "score": 7, "explain": true}],
  "externals": [{"id": "ext:anthropic-api", "label": "Anthropic API", "kind": "paid",   // paid | data
                 "evidence": [{"path": "src/ai/directApiClient.js", "line": 7, "snippet": "…"}]}],
  "edges": [{"from": "src/sidepanel/sidepanel.js", "to": "src/ai/directApiClient.js",
             "line": 3, "names": ["createDirectApiClient"]},
            {"from": "src/ai/directApiClient.js", "to": "ext:anthropic-api", "line": 7, "names": []}],
  "entries": [{"path": "src/sidepanel/sidepanel.js", "reason": "manifest side_panel → sidepanel.html"}],
  "folders": [{"id": "src/ai", "files": ["src/ai/directApiClient.js", "…"]}],
  "collapsed": false,
  "unresolved": [{"from": "src/x.ts", "spec": "@/lib/missing", "line": 4}],
  "excluded": {"tests": 12, "config": 3},
  "languages": ["js"]
}
```

### 6.2 `explain.json`（AI 写）

```jsonc
{
  "evidence": {"H1": {"kind": "transcript", "session": "…", "msg_id": "…", "quote": "…"}},
  "files": {
    "src/ai/directApiClient.js": {
      "purpose_plain": "负责把你的简历和职位描述，连同你这次输入的 API key，直接发给你选的 AI 服务商，再把回答取回来。",
      "purpose_dev": "Provider-specific fetch clients (`runAnthropic`, `runOpenAi`, `runDeepSeek`) behind `createDirectApiClient`.",
      "functions": [{"name": "runAnthropic", "line": 133, "plain": "发请求给 Anthropic，带上你的 key"}],
      "history": [{"plain": "…", "evidence": ["H1"]}]
    }
  }
}
```

`vl.py check` 输出 `explain.verified.json`，在原结构上补充以下字段：每个文件的 `ok`、被删函数及原因、`purpose_unverified` 及找不到的标识符、被更正的行号；每条证据补充 `ok` 和 `reason`。

## 7. 命令行的变化

- **`vl.py start`**：在 v0.1 的步骤之后，运行 `graph.py`，写出 `graph.json` 和 `explain_pack.md`；打印出的下一步要求写 `ledger.json` 和 `explain.json`（只有一个讲解分块时直接写，多块时写进 `parts/`）。
- **`vl.py merge`**：合并 `parts/part_*.json`（账本）和 `parts/explain_*.json`（讲解），两种都有就都合并。
- **`vl.py check`**：校验 `ledger.json` 和 `explain.json`。`explain.json` 缺失时给出明确提示并以退出码 2 结束，不会生成没有讲解的报告。
- **`vl.py render`**：生成两个标签页的页面。
- **`vl.py shot`**：截 4 张图：桌面、深色、手机 390px、选中得分最高的文件。截图时还会用无头浏览器导出排版完成后的页面结构，检查节点之间有没有重叠，结果打印出来。

## 8. 新增和改动的文件

| 文件 | 职责 |
|---|---|
| `scripts/graph.py` | import 提取、路径解析、入口识别、外部节点、文件夹分组、打分、`explain_pack.md` |
| `scripts/explain.py` | `explain.json` 的格式检查和核对 |
| `scripts/ledger_report/graph_page.py` | 组装流程图标签页：嵌入数据、面板模板 |
| `scripts/ledger_report/assets/graph.js` | dagre 排版、绘制、平移缩放、选中、面板、搜索、折叠 |
| `scripts/ledger_report/assets/graph.css` | 流程图和面板的样式（彩色卡片加图标） |
| `scripts/ledger_report/vendor/dagre.min.js` + `LICENSE-dagre` | 打包进来的 dagre |
| `scripts/render.py` | 改为标签页外壳：“文件流程图”加“总览”（总览就是 v0.1 的页面主体） |
| `scripts/vl.py`、`scripts/shot.py` | 第 7 节的命令行变化 |
| `SKILL.md`、`references/explain-guide.md` | 讲解的写法和规则 |

## 9. 测试与验收

### 9.1 单元测试
- **`graph.py`**：
  - import 写法：ES、CommonJS、动态 import、`export … from`、Python 的两种写法；
  - 路径解析：tsconfig 别名、`@/` 回退、index 文件、省略扩展名；解析不了的引用要进 `unresolved`；
  - 入口识别：3.3 表里的 6 种规则各有用例，另加“识别不出入口”的回退；
  - 外部节点：SDK、API 地址、浏览器存储各有用例，普通库不建节点；
  - 测试和配置文件被排除并计数；循环引用不出错；超过 80 个文件时折叠；打分和排序结果确定。
- **`explain.py`**：
  - 4.3 列出的每种函数定义写法都能识别；
  - 编造的函数被删，行号偏了能更正；
  - 反引号里有不存在的标识符时，用途被标为“未核实”；
  - 来历引文按规则校验；路径不在图里时整张卡片作废；格式错误时列出全部问题。
- **页面**：
  - 嵌入的数据和 `graph.json`、`explain.verified.json` 一致；
  - 页面里不出现任何密钥原文；
  - 数据里含 `</script>` 时页面不会被截断；
  - 两个标签页都在，“总览”页包含 v0.1 的各个部分。

### 9.2 浏览器检查
用无头浏览器加载页面，等 dagre 排完版后导出页面结构，读取每个节点的位置（`data-x`、`data-y`、`data-w`、`data-h`），断言：
- 节点两两不重叠；
- 外部节点都在入口节点的右边；
- 带 `?select=` 打开时，被选中的节点和它的邻居没有变淡，面板里出现这个文件的用途。

### 9.3 端到端
- 沿用 v0.1 的 5 个测试应用，标准答案里补充图的期望：关键节点、关键连线、入口、外部节点。
- 新增一个脚本生成的中型样本（约 100 个文件），用来测文件夹折叠。
- 派全新的 agent，按 SKILL.md 走完包括讲解在内的全流程，用打分脚本对比标准答案。
- 打开截图逐张看：桌面、深色、手机、选中状态。

### 9.4 验收标准
- 5 个测试应用的图，和标准答案里的节点、连线、入口、外部节点一致；
- 浏览器检查全部通过：节点不重叠，选中状态正确；
- 页面里的密钥原文为 0；
- 在那个真实项目上重跑后，用户确认“看懂了，主要靠图”。

## 10. 不在本版范围内

- 函数级别的调用图（v0.2 只画文件级别）；
- 运行时追踪（实际点按钮看走了哪些代码）；
- JS/TS 和 Python 以外的语言；
- monorepo 里 workspace 包之间的引用（tsconfig 别名能覆盖的除外）；
- 在页面上编辑讲解或写回仓库。
