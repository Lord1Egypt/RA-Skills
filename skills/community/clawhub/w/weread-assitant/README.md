# WeRead Assistant

将微信读书网页端的书架、阅读状态、可见正文内容与 Obsidian/OpenClaw 工作流连接起来的本地工具集。

这个项目当前已经完成一条真实可跑通的链路：

1. 复用你本机 Chrome 中已登录的微信读书会话
2. 抓取书架列表、书籍链接、阅读进度、笔记数量、可见正文块
3. 导出为结构化 JSON
4. 生成适合 Obsidian 的 Markdown 笔记
5. 通过 `obsidian-cli` 直接写入你的 Obsidian vault

## Security Notes

这个 skill 需要访问你本机已登录的微信读书网页，因此公开市场扫描工具有时会把它标成“可疑”。当前代码的默认行为已经收紧为：

- 只抓取当前页面可见 DOM 和滚动后可见正文
- 不读取 cookie、`localStorage`、`sessionStorage`
- 不扫描本机 Obsidian 配置目录
- 只通过 `obsidian-cli` 写入 Obsidian，不再走直接写 vault 的回退逻辑

如果后续市场扫描仍然误报，最可能的原因是它依然会看到：

- 需要连接本地 Chrome Debug 代理
- 需要访问已登录网页内容
- 需要调用本地命令行把笔记发布到 Obsidian

更完整的权限边界、数据流和误报说明见 [SECURITY.md](/Users/mcxu/workspace/projects/weread_assitant/SECURITY.md#L1)。

## 项目目标

这个仓库不是通用爬虫，而是一个偏个人知识管理的桥接层：

- 面向微信读书网页端的真实登录态采集
- 优先产出可供 AI 和笔记系统消费的中间数据
- 让 OpenClaw、飞书 bot、Obsidian 能基于本地文件继续工作

推荐工作方式不是每次都实时访问微信读书，而是：

1. 先同步一次数据到本地
2. 再让 OpenClaw/飞书/Obsidian 消费本地文件
3. 需要更新时重新同步

## 当前能力

### 1. 书架同步

从 `https://weread.qq.com/web/shelf` 拉取：

- 书名
- `bookId`
- 微信读书阅读链接
- 封面链接
- 当前页面可见的书架快照

输出文件：

- `output/weread/shelf.json`
- `output/obsidian/weread-shelf.md`

### 2. 单书抓取

针对某一本书的 `web/reader/<bookId>` 页面抓取：

- 书名
- 作者
- 阅读进度
- 笔记数量
- 阅读时长
- 当前章节线索
- 当前页面可见的正文块
- 划线/想法候选

输出文件：

- `output/weread/books/<slug>.json`
- `output/obsidian/books/<slug>.md`

### 3. Obsidian 发布

将导出的 Markdown 通过 `obsidian-cli` 直接发布到 Obsidian vault。

当前模板已经支持两类阅读场景：

- 卡片笔记：金句卡片、问题卡片、永久笔记草稿
- 阅读面板：阅读进度、当前章节、本轮待办
- 读后感回写：把你在聊天里补充的读后感沉淀回对应书籍笔记

## 目录结构

```text
.
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── package.json
├── references/
│   └── data-contract.md
├── scripts/
│   ├── add-book-reflection.mjs
│   ├── book-utils.mjs
│   ├── cdp-client.mjs
│   ├── export-obsidian.mjs
│   ├── fetch-book.mjs
│   ├── fetch-shelf.mjs
│   ├── publish-obsidian.mjs
│   └── sync-book-by-title.mjs
└── output/
    ├── obsidian/
    └── weread/
```

## 作为 OpenClaw Skill 安装

这个仓库现在本身就是一个 skill repo。

也就是说，OpenClaw 安装时应该直接安装仓库根，而不是再指向子路径。

仓库根已经包含 skill 需要的核心内容：

- `SKILL.md`
- `scripts/`
- `references/`
- `agents/openai.yaml`

安装后，skill 应直接调用：

- `node scripts/fetch-shelf.mjs`
- `node scripts/fetch-book.mjs`
- `node scripts/export-obsidian.mjs`
- `node scripts/publish-obsidian.mjs`
- `node scripts/sync-book-by-title.mjs`
- `node scripts/add-book-reflection.mjs`

而不是依赖仓库根目录的 `npm run`。根目录的 `package.json` 只是开发时的快捷方式，不是安装后运行的必要条件。

### 从 GitHub 直接安装

如果你已经把这个仓库推到 GitHub，推荐直接使用仓库根 URL 安装：

```bash
python3 /Users/mcxu/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --url https://github.com/MingChaoXu/weread_assitant/tree/main
```

之所以推荐 URL 方式，是因为这个仓库的 skill 就在根目录，而不是某个子路径。

安装完成后，重启 OpenClaw/Codex 以加载新 skill。

### 安装后的触发方式

推荐直接按 skill 名称调用：

```text
使用 $weread-obsidian 同步我的微信读书书架
```

或者：

```text
使用 $weread-obsidian 抓取这本微信读书并生成 Obsidian 卡片笔记
```

也可以直接用更短的自然语言触发：

```text
使用 $weread-obsidian 同步《金字塔原理》笔记
使用 $weread-obsidian 给《金字塔原理》加一段读后感，并润色后同步到 Obsidian
```

## 运行前提

### 必需条件

1. 本机安装 Node.js 22+
2. Chrome 已打开，并已登录微信读书
3. 在 `chrome://inspect/#remote-debugging` 中启用 remote debugging
4. 本机可运行 `web-access` skill 对应的 CDP proxy

### 如果要写入 Obsidian

还需要：

1. 已安装 `obsidian-cli`
2. 已设置默认 vault，或在命令里显式传 `--vault`

当前环境里已验证过：

- `obsidian-cli` 可用
- 默认 vault 为 `claw_notes`

如果 `obsidian-cli` 没有正确配置，发布步骤会显式失败，而不是自动探测或改写你的本地 Obsidian 配置。

## 快速开始

### 1. 拉取书架

```bash
npm run weread:fetch-shelf
```

成功后会得到：

- `output/weread/shelf.json`

### 2. 抓一本文字内容

从书架输出中挑一本书的 reader URL，例如：

```bash
npm run weread:fetch-book -- --book-url "https://weread.qq.com/web/reader/a583244072027d22a58423a"
```

成功后会得到：

- `output/weread/books/从零开始学缠论-缠中说禅核心技术分类精解.json`

### 3. 导出为 Obsidian Markdown

```bash
npm run weread:export-obsidian -- \
  --shelf output/weread/shelf.json \
  --book "output/weread/books/从零开始学缠论-缠中说禅核心技术分类精解.json"
```

成功后会得到：

- `output/obsidian/weread-shelf.md`
- `output/obsidian/books/从零开始学缠论-缠中说禅核心技术分类精解.md`

### 4. 写入 Obsidian vault

```bash
npm run weread:publish-obsidian -- --dir output/obsidian --vault claw_notes
```

当前会发布成以下 note 路径：

- `WeRead/weread-shelf`
- `WeRead/books/<书名>`

### 5. 按书名一键同步整本笔记

如果你只知道书名，不想先自己翻 `shelf.json` 找链接，可以直接：

```bash
npm run weread:sync-book-by-title -- --title "金字塔原理" --vault claw_notes
```

这个命令会自动：

1. 刷新书架快照
2. 按书名匹配书架中的目标书
3. 抓取单书页面
4. 导出 Markdown
5. 发布到 Obsidian

### 6. 给现有书籍笔记追加读后感

如果你已经同步过某本书，可以把读后感直接写回这本书的 Obsidian 笔记：

```bash
npm run weread:add-reflection -- \
  --title "金字塔原理" \
  --reflection "这本书最有价值的地方，是把表达拆成了结论先行、以上统下、归类分组三个动作。它提醒我，写任何复杂内容前都应该先搭清楚结构。接下来我想把这个方法用到周报和投资笔记里。" \
  --vault claw_notes
```

这个命令会：

1. 把读后感保存到 `output/weread/reflections/<slug>.json`
2. 重新生成这本书的 Markdown
3. 重新发布对应 Obsidian 笔记

这样后续你再次同步这本书时，读后感不会被覆盖掉。

## 常见工作流

### 工作流 1：同步书架，决定下一本读什么

适合你刚打开微信读书，想让 OpenClaw 先帮你做阅读决策的时候。

```bash
npm run weread:fetch-shelf
npm run weread:export-obsidian -- --shelf output/weread/shelf.json
npm run weread:publish-obsidian -- --dir output/obsidian --vault claw_notes
```

然后在 Obsidian 或 OpenClaw 中读取：

- `WeRead/weread-shelf`

推荐提问：

```text
请基于我的微信读书书架，推荐下一本最值得深读的书，并说明理由、预期收获和建议的阅读顺序。
```

### 工作流 2：同步单本书，生成卡片笔记底稿

适合你已经在读某本书，想把当前进度和正文片段转成可写的卡片笔记。

```bash
npm run weread:fetch-book -- --book-url "https://weread.qq.com/web/reader/<bookId>"
npm run weread:export-obsidian -- --book "output/weread/books/<slug>.json"
npm run weread:publish-obsidian -- --dir output/obsidian --vault claw_notes
```

然后在 Obsidian 或 OpenClaw 中读取：

- `WeRead/books/<书名>`

推荐提问：

```text
请把这份读书笔记整理成卡片笔记，保留进度面板，挑出 3 条最值得保留的金句，回答 2 个问题卡片，并完成 2 条永久笔记。
```

### 工作流 2.5：通过聊天按书名同步

这适合你在 OpenClaw 里直接说一句话，不想手动找书籍 URL。

推荐触发语句：

```text
使用 $weread-obsidian 同步《金字塔原理》笔记
```

skill 内部应优先执行：

```bash
node scripts/sync-book-by-title.mjs --title "金字塔原理" --vault claw_notes
```

### 工作流 2.6：通过聊天补读后感并回写

这适合你已经有粗糙想法，希望 OpenClaw 先整理文案，再把结果写回对应书籍笔记。

推荐触发语句：

```text
使用 $weread-obsidian 给《金字塔原理》加一段读后感，并润色后同步到 Obsidian：这本书让我意识到，表达问题很多时候不是不会写，而是没有先搭结构。
```

推荐执行策略：

1. 先把用户原话润色成 1 到 3 段自然、克制、可回顾的读后感
2. 再执行：

```bash
node scripts/add-book-reflection.mjs --title "金字塔原理" --reflection "<润色后的文案>" --vault claw_notes
```

## License

This project is licensed under `MIT-0` (`MIT No Attribution`). See [LICENSE](/Users/mcxu/workspace/projects/weread_assitant/LICENSE).

### 工作流 3：完整链路，从微信读书同步到 Obsidian

```bash
npm run weread:fetch-shelf
npm run weread:fetch-book -- --book-url "https://weread.qq.com/web/reader/<bookId>"
npm run weread:export-obsidian -- \
  --shelf output/weread/shelf.json \
  --book "output/weread/books/<slug>.json"
npm run weread:publish-obsidian -- --dir output/obsidian --vault claw_notes
```

这个流程会同时更新：

- 书架总览 note
- 单书卡片笔记 note

## 可用命令

### `npm run weread:fetch-shelf`

抓取微信读书书架页面并保存为 JSON。

### `npm run weread:fetch-book -- --book-url "<url>"`

抓取单本书页面。

常用可选参数：

- `--output <path>`：自定义输出路径
- `--output-dir <dir>`：自定义输出目录
- `--scrolls <n>`：滚动次数，决定正文采样深度
- `--keep-open`：调试时保留浏览器标签页

### `npm run weread:export-obsidian`

将 JSON 转为 Markdown。

常用参数：

- `--shelf <path>`
- `--book <path>`
- `--output-dir <dir>`

### `npm run weread:publish-obsidian`

通过 `obsidian-cli` 写入 Obsidian。

常用参数：

- `--dir <dir>`：批量发布目录
- `--file <file>`：只发布单个 Markdown
- `--vault <name>`：指定 vault
- `--prefix <prefix>`：控制 note 路径前缀，默认 `WeRead`

## 生成的数据格式

更细的数据契约见：

- `references/data-contract.md`

核心产物如下。

### `output/weread/shelf.json`

包含：

- `capturedAt`
- `page`
- `books`
- `rawCandidates`

其中 `books` 是后续抓单书最常用的输入。

### `output/weread/books/<slug>.json`

包含：

- `capturedAt`
- `sourceUrl`
- `page`
- `metadata`
- `toc`
- `notes`
- `content`

其中：

- `metadata` 提供书名、作者、简介、封面
- `notes` 提供划线/评论/状态候选
- `content.blocks` 提供当前页面采集到的正文块

## 当前 Obsidian 模板设计

单书导出的 Markdown 模板分为几个区块：

### 1. 读书进度面板

展示：

- 作者
- 进度
- 当前章节
- 笔记数
- 阅读时长
- 最近同步时间

### 2. 本轮待办

用于让你在一次阅读会话中快速进入状态，比如：

- 复述当前章节
- 选一条金句展开
- 完成一条永久笔记
- 回答一个问题卡片

### 3. 金句卡片

从抓取内容里挑出更适合沉淀的句子，并留出三个空槽：

- 我的理解
- 能连接到哪条旧笔记
- 可以指导什么行动

### 4. 问题卡片

将阅读内容转成值得继续追问的问题，方便你与 OpenClaw 或自己继续展开。

### 5. 永久笔记草稿

为每次阅读自动准备几条可继续加工的永久笔记框架。

### 6. 待清洗原料

保留抓取到的原始划线/想法候选，方便后续二次清洗。

## OpenClaw 使用建议

推荐把这个仓库视为“同步层”，把 Obsidian 视为“知识基座”，把 OpenClaw 视为“整理与对话层”。

### 推荐职责划分

- WeRead Assistant：负责抓取与导出
- Obsidian：负责沉淀与回看
- OpenClaw：负责提炼、提问、改写、连接旧笔记

### 推荐对话顺序

1. 先同步 WeRead 数据到本地
2. 再发布到 Obsidian
3. 最后让 OpenClaw 基于 Obsidian note 继续整理

这样做的好处是：

- 避免每次对话都重新连接微信读书
- 保留可复用的 Markdown 中间层
- 便于后续迭代模板和提示词

### 建议保留的 Prompt 模板

#### 模板 1：章节总结

```text
请基于这份微信读书笔记，先更新读书进度面板，再总结当前章节的核心观点、论证方式和最值得记住的结论。
```

#### 模板 2：卡片提炼

```text
请从这份笔记中挑出最值得保留的 3 条金句，分别补上“我的理解”“可连接的旧笔记”“可指导的行动”。
```

#### 模板 3：永久笔记加工

```text
请把这份笔记中的永久笔记草稿改写成更像人写的标题，并补全论点、例子和可链接的旧笔记方向。
```

#### 模板 4：追问式阅读

```text
请基于问题卡片继续追问，挑 2 个最关键的问题展开，指出我下一次阅读时应该重点验证什么。
```

## 已完成的真实测试

这个仓库已经用你的真实环境完成过一轮端到端测试：

- 成功连接 Chrome debug 端口
- 成功抓取微信读书书架
- 成功识别 50 本书
- 成功抓取至少 1 本书的阅读状态与正文内容
- 成功导出 Markdown
- 成功写入 `claw_notes` vault

测试样例文件：

- `output/weread/shelf.json`
- `output/weread/books/从零开始学缠论-缠中说禅核心技术分类精解.json`
- `output/obsidian/weread-shelf.md`
- `output/obsidian/books/从零开始学缠论-缠中说禅核心技术分类精解.md`

## 已知限制

### 1. 当前抓取的是“可见内容优先”

这不是一个完整电子书导出器，而是页面可见内容采样器。

这意味着：

- 能拿到当前阅读区域内容
- 能拿到部分进度和笔记状态
- 不保证能一次性拿完整本书全文

### 2. DOM 结构变化会影响提取效果

微信读书如果调整前端结构，以下内容可能需要重新适配：

- 目录项识别
- 划线/想法区分
- 当前章节推断

### 3. 划线候选仍有少量噪声

当前模板已经把这些内容降级为“待清洗原料”，但还可以继续优化。

### 4. GitHub 发布尚未完成

当前目录已经初始化为本地 git 仓库，但还没有配置远程仓库地址，因此推送前还需要补上目标 GitHub repo。

## 推荐下一步

最值得继续做的有四项：

1. 优化金句与永久笔记标题生成，让它更像人工写作
2. 把“真实划线”和“正文摘录”进一步分开
3. 增加批量抓取多本书的编排流程
4. 将 OpenClaw/飞书对话 prompt 固化为更稳定的模板

## 开发说明

这个项目目前是一个轻量脚本仓库，没有引入额外 npm 依赖，依赖的都是系统侧能力：

- Node.js
- Chrome debugging
- `obsidian-cli`
- 本地 `web-access` skill 对应脚本

如需调试某个脚本，优先直接运行 `node` 命令或 npm scripts。

## 许可与隐私提醒

这个项目会访问你的真实微信读书登录态，并将抓取结果写到本地文件中。

请注意：

- 不要随意提交包含隐私阅读数据的 `output/` 目录
- 不要在不了解后果的情况下批量抓取大量内容
- 自动化访问网页存在被站点识别的风险
