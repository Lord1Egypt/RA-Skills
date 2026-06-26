---
name: wx-mp-publish
description: 微信公众号文章发布技能。当用户提到发布公众号文章、推送微信公众号、公众号发布、微信公众号发文、将文章发布到公众号、把文章发到公众号、把markdown转成微信公众号格式，或需要将带 YAML frontmatter 的 markdown 文件发布到微信公众号时激活。包含：Markdown → HTML 转换（marked + 内联样式，自动去除 frontmatter）、封面图上传、创建草稿、API 发布或手动发布指引、常见错误处理。
---

# wx-mp-publish — 微信公众号发布技能

## 技术方案

**Node.js + marked**：微信 API 返回的 JSON 含特殊字符，Python `json.loads()` 解析失败率高（报错 `Invalid \uXXXX escape`），Node.js V8 原生 JSON 解析稳定可靠。
**Python 版本已废弃删除**（scripts/wx-mp/ 目录下仅保留 Node.js）。

## 快速流程

```
用户提供 Markdown 文章（含 YAML frontmatter）
    ↓
自动去除 frontmatter（re.sub 去掉 --- 之间的内容）
    ↓
marked.parse() → HTML（gfm 模式）
    ↓
applyInlineStyles() → 内联 style
    ↓
上传封面图（≤64KB）
    ↓
创建草稿 → 手动发布（或 API 发布）
```

## 发布命令

```bash
cd ~/.openclaw/workspace/skills/wx-mp-publish/scripts
node wx-publish.js draft <文章.md> \
  --title "标题（≤64字符）" \
  [--thumb <封面图路径>]

node wx-publish.js publish <文章.md> \
  --title "标题" \
  [--thumb <封面图路径>]
```

### 查询与预览

```bash
node wx-publish.js drafts       # 列出草稿
node wx-publish.js del <id>    # 删除草稿
node wx-publish.js status       # 查看配额
```

## 📝 发布流程（必须按顺序执行）

创建草稿后，还需在公众号后台手动设置以下选项：

| 设置项 | 位置 | 说明 |
|--------|------|------|
| **🤖 AI辅助生成标注** | 文章开头或结尾 | 必须标注「本文包含AI辅助内容」 |
| **✅ 声明原创** | 编辑框下方 | 原创标签按钮 |
| **💰 打开赞赏** | 文章底部 | 赞赏按钮开关 |
| **✍️ 作者** | 文章底部 | 填写"你的名字" |
| **⏰ 定时群发** | 发布设置 | 可选，但订阅号每月只4次，要节省使用 |

**后台路径：** 内容与创作 → 草稿箱 → 找到草稿 → 编辑 → 发布

### ⚠️ API发布限制

- **订阅号（审核中）**：只能创建草稿，`publish` 命令会报 `[48001] api unauthorized`
  - 发布限制：每天1次
- **服务号**：可直接API发布
  - 发布限制：每月4次
- 定时群发API需要服务号权限

## ⚠️ 关键注意事项

### 1. 不用 Python，用 Node.js

Python `json.loads()` 对微信 API 返回的某些 JSON 失败（`Invalid \uXXXX escape`），Node.js 无此问题。

### 2. YAML frontmatter 必须去除

微信文章不需要 frontmatter，若不去除会显示为正文乱码。
`wx-publish.js` 内置自动去除：`content.replace(/^---\n[\s\S]*?\n---\n/, '')`

### 3. 不要用 nl2br 模式

Python markdown 库的 `nl2br` 扩展把换行符变成裸 `<br>`，微信编辑器无法正确渲染。正确做法是 paragraphs 自然闭合。

### 4. API 发布权限限制

**错误**：`[48001] api unauthorized`

订阅号（审核中）只能创建草稿，需手动在公众号后台发布。
后台路径：**内容与创作 → 草稿箱 → 找到草稿 → 发布**

### 5. 标题/摘要长度限制

- 标题 ≤64 字符
- 摘要 ≤120 字符（或留空让微信自动生成）

### 6. 封面图大小限制

≤64KB。建议尺寸 900×383 像素（2.35:1）。

## 📝 文章写作格式规范（2026-04-03）

> ⚠️ 每次写文章前必读

### 事实核查要求（最高优先级）

写文章涉及外部产品/工具时，**必须**：

1. 先查 `~/workspace/docs/product-facts.md` 确认产品事实
2. 不确定的概念用 `web_search` 主动搜索核实
3. **禁止凭记忆瞎写产品功能**

涉及的关键产品：
- Claude Code = Anthropic商业AI编程CLI
- OpenCode = opencode.ai开源竞品，provider-agnostic
- OpenClaw = 个人AI助手平台，不只是编程
- Google Cloud Code = Kubernetes工具，和AI编程无关

### 不确定事实的主动核查规则

**触发条件：** 文章中出现任何不熟悉的概念、产品、技术名词，而 product-facts.md 里没有记载。

**执行流程：**

1. **主动搜索** — 用 `web_search` 搜索该概念，获取权威来源
2. **核实后记录** — 把确认的事实按分类存入 `~/workspace/docs/product-facts.md`
3. **标注来源** — 记录信息源URL和核实日期

**事实分类标准（存入 facts 文档的分类标签）：**

| 分类标签 | 包含内容 | 示例 |
|----------|----------|------|
| `[产品类]` | 产品名称、厂商、定位、界面形态 | Claude Code是Anthropic的产品 |
| `[技术类]` | 技术名词、协议、架构术语 | MCP、Agent架构、Context管理 |
| `[事件类]` | 重大发布、泄露事件、行业动态 | Claude Code源码泄露事件 |
| `[数据类]` | 用户量、stars数、版本号、价格 | GitHub 68k+ stars |
| `[对比类]` | 多个产品的横向对比结论 | OpenCode vs Claude Code的差异 |

**记录格式（追加到 product-facts.md 末尾）：**

```markdown
## [YYYY-MM-DD] 新增事实

### [产品类] 产品名称
- **事实内容**：...
- **来源**：URL
- **核实日期**：YYYY-MM-DD
```

**自动分类规则：**
- 出现"是什么" → `[产品类]` 或 `[技术类]`
- 出现"发布/泄露/更新/收购" → `[事件类]`
- 出现"对比/差异/哪个更好" → `[对比类]`
- 出现"多少/数量/价格/版本" → `[数据类]`

**示例场景：**
> 文章里要提"Aider"，但 facts 文档里没有 → 立刻 web_search → 确认为开源AI编程CLI工具 → 追加到 `[工具类]` 或新建 `[产品类]` → 继续写文章



### 结构要求

**禁止**在文章正文中出现：
- ❌ "第一节/第二节/第三段"这类内部策划标记
- ❌ "上文说过的"、"承接上篇"、"钩子"等内部术语
- ❌ 阿拉伯数字编号的章节标题（1. 2. 3. / 第一节 第二节）
- ❌ "这篇来讲讲"、"下面我将从三个方面"等说明性文字
- ❌ "一句话总结"、"一句话告诉你"、"一句话说明"（浓AI味，直接写内容即可）

**应该**用：
- ✅ 自然分段，每段讲一个事情
- ✅ 关键转折或新话题用 `——` 或空行分隔
- ✅ 小标题可用问句或短句，控制在10字以内，不带"第一章"、"第三节"等前缀
- ✅ 用语面向普通读者，不是内部备忘录

### 开头格式（必选）

```
> 字数：约XXXX字 | 阅读时间：X分钟
> **"金句内容"**

---
正文（自然分段，不要编号）
```

### 篇末提示格式

如果需要加"中国平替"等提示，直接在正文末尾加一段话即可，不要标注"篇末提示"。

### 实战举例要求

提到自己的项目时：
- ✅ "我做的APP"、"我开发的项目"
- ❌ 具体APP名称、产品名
- ❌ 业务类型、用户群体等业务细节
- ✅ 只讨论技术实现层面（架构、选型、技术栈等）

### ⚠️ 隐私保护（必须遵守）

**1. 项目名称保护**
- 禁止在文章中出现任何具体APP名称
- 只能说"我开发的项目"或"我做的APP"
- 只能讨论技术层面，业务细节一律禁止

**2. Google Cloud Code ≠ Claude Code**
- Google Cloud Code = Google的Kubernetes开发工具（VS Code/IntelliJ插件），和AI编程无关
- Claude Code = Anthropic的AI编程CLI工具
- 两者完全不同，禁止混淆

**3. "Cloud Code" vs "Claude Code" 拼写**
- 文章里只有 Claude Code，没有 Cloud Code
- Cloud Code 是谷歌云工具的名字，文章里不出现
- 输入时养成习惯，先确认再敲

**4. OpenClaw vs OpenCode 对比关系**
- Claude Code ↔ OpenCode = 编程能力直接竞品
- OpenClaw = 个人AI助手平台，不是编程工具的直接竞品
- OpenClaw只在篇末平替提示里提一句，不作为主要对比对象
- 两者名称相近易混，写前必查 product-facts.md

**5. 文章编号规则**
- 技术篇：Cloud Code专题（4篇）= 第1-4篇
- 单篇技术文章从第5篇开始编号
- 发布前查 series-counter.md 确认编号

**6. 封面图规格**
- 尺寸：900×383像素（2.35:1）
- 大小：≤64KB
- 生成后用 ImageMagick 压缩： `convert 原图.png -resize 900x383! -quality 75 输出.jpg`

### 7. 运营数据追踪

文章运营数据记录在 `~/workspace/memory/articles/article-tracker.json`。

**可获取的数据（每日自动更新）：**
- 草稿列表 + 篇序
- 已发布文章列表 + 发布时间
- 总用户数

**需手动更新的数据（用户从后台查看后告知）：**
- 单篇阅读量
- 单篇在看数/点赞数
- 留言数

**更新流程：**
1. 用户查看公众号后台「数据」→「内容」→「群发数据」
2. 告诉你的名字："更新第X篇的阅读量/在看数"
3. 我会更新 article-tracker.json 中对应文章的数据

**查运营数据（不用调用API）：**
直接查看 `memory/articles/article-tracker.json`，包含：
- 最后更新时间（statsUpdated）
- 所有文章篇序、标题、状态
- 每篇的阅读量/点赞等（手动更新）

---

## 依赖

```
cd scripts/
npm install marked
```

## 目录结构

```
wx-mp-publish/
├── SKILL.md              # 本文件
├── references/
│   └── best-practices.md # 详细文档
└── scripts/
    ├── wx-publish.js     # Node.js 发布脚本（核心）
    ├── wx-api.js         # 备用 API 工具
    ├── package.json      # npm 依赖
    └── node_modules/     # npm 包
```
