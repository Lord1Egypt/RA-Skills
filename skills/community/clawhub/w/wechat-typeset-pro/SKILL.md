# wechat-typeset-pro

微信公众号专业排版技能。把 Markdown 文章转为微信公众号兼容的精美内联样式 HTML，30 套主题 + 可视化画廊选择 + AI 内容增强 + 一键复制到公众号。可选推送到草稿箱。

## Skill Description

微信公众号专业排版引擎：Markdown → 精美微信兼容 HTML。当用户说"排版""微信排版""公众号排版""format""美化文章"时使用。支持 30 套精美主题、可视化画廊预览、AI 内容结构增强、深色模式、代码高亮。

## When to Use

- 用户需要将 Markdown 文章排版为微信公众号格式
- 用户说"排版""微信排版""美化""格式化为公众号格式""公众号排版"
- `wechat-content-studio` 技能的排版流程调用本技能
- 需要预览多种主题风格并选择最佳方案

## 脚本目录

`{baseDir}` = 本 SKILL.md 所在目录。

| 脚本 | 用途 |
|------|------|
| `scripts/format.py` | 排版引擎：Markdown → 微信兼容 HTML |
| `scripts/publish.py` | 推送：HTML → 公众号草稿箱 |

## 配置

配置文件：`{baseDir}/config.json`

微信凭证优先从环境变量读取（`~/.openclaw/.env`），无需在 config.json 中配置敏感信息。

### 环境变量（自动从 ~/.openclaw/.env 加载）

| 变量 | 用途 |
|------|------|
| `WECHAT_APP_ID` | 微信公众号 AppID |
| `WECHAT_APP_SECRET` | 微信公众号 AppSecret |

## Instructions

### 完整工作流

#### 第 1 步：确认文章

1. 如果用户给了文件路径，直接读取
2. 如果没给路径，问用户要文章路径
3. 读取文章内容，确认标题和字数

#### 第 1.5 步：结构化预处理（仅在需要时）

读取文章后，检测 Markdown 结构完整度。

**判断规则**：
- 有 `##` 标题且格式标记分布合理 → 跳过，直接进入第 2 步
- 缺少 `##` 标题或几乎没有格式标记 → 执行结构化

**结构化规则（只加标记，不改内容）**：
1. 识别逻辑段落插入 `##` 标题（从内容提炼，不编造）
2. 确保段落之间有空行分隔
3. 识别并列内容加列表标记
4. 识别关键词加 `**加粗**`
5. 清理格式（多余空行、缩进、标点）
6. **不改措辞**：不调语序、不增删内容

保存为 `~/WorkBuddy/wechat-typeset-pro/xxx-structured.md`（与 `config.json` 的 `output_dir`，即 `path.join(HOME, 'WorkBuddy', 'wechat-typeset-pro')` 一致），告知用户。

#### 第 2 步：AI 内容分析 + 自动套格式

分析内容结构，在 Markdown 层面自动套用排版容器：

1. **对话/访谈** → `:::dialogue[标题]`
2. **连续多图（3+）** → `:::gallery[标题]`
3. **核心观点/金句** → `> [!important] 标题`（一篇 1-3 处）
4. **小技巧** → `> [!tip] 标题`
5. **注意事项** → `> [!warning] 标题`
6. **分隔符** → 章节转换处确保有 `---`
7. **图说** → 图片后斜体：`*图片说明*`

保存增强后 Markdown 为 `~/WorkBuddy/wechat-typeset-pro/xxx-enhanced.md`。

#### 第 2.5 步：推荐主题

根据内容分析推荐 3 个最适合的主题：

| 内容类型 | 推荐主题 |
|----------|----------|
| 深度长文/分析 | newspaper, magazine, ink |
| 科技产品/AI工具 | bytedance, github, sspai |
| 访谈/对话体 | terracotta, coffee-house, mint-fresh |
| 教程/操作指南 | github, sspai, bytedance |
| 文艺/随笔/观点 | terracotta, sunset-amber, lavender-dream |
| 活力/动态/速报 | sports, bauhaus, chinese |

#### 第 3 步：打开主题画廊（默认）

```bash
python3 {baseDir}/scripts/format.py \
  --input "文章路径.md" \
  --gallery \
  --recommend newspaper magazine ink
```

用**真实文章**渲染 20 个主题，浏览器中选择。

#### 第 3 步（备选）：直接指定主题

```bash
python3 {baseDir}/scripts/format.py \
  --input "文章路径.md" \
  --theme terracotta
```

#### 第 4 步：确认结果

- Gallery 模式：浏览器中切换主题，选中后点按钮复制，粘贴到公众号后台
- 直接模式：浏览器中检查预览，点「复制到微信」

### 推送到草稿箱（可选）

用户说"推送""发公众号"时执行：

```bash
python3 {baseDir}/scripts/publish.py \
  --dir "排版输出目录" \
  --cover "封面图路径（可选）"
```

从 Markdown 直接推送：

```bash
python3 {baseDir}/scripts/publish.py \
  --input "文章.md" \
  --theme terracotta
```

### 参数说明

**format.py**：
- `--input` / `-i`：Markdown 文件路径（必须）
- `--gallery`：打开主题画廊（推荐）
- `--theme` / `-t`：直接指定主题名
- `--output` / `-o`：输出目录（默认 `~/WorkBuddy/wechat-typeset-pro`，即 `path.join(HOME, 'WorkBuddy', 'wechat-typeset-pro')`）
- `--recommend`：推荐主题 ID 列表
- `--no-open`：不自动打开浏览器
- `--format`：输出格式 wechat/html/plain

**publish.py**：
- `--dir`：排版输出目录
- `--input`：Markdown 文件路径（自动排版再推送）
- `--cover` / `-c`：封面图路径
- `--title` / `-t`：文章标题
- `--theme`：排版主题（仅 --input 模式有效）
- `--author` / `-a`：作者名
- `--dry-run`：只做排版，不推送

## 可用主题（30 个）

### 独立风格（9 个）

| 主题 | ID | 风格 |
|------|-----|------|
| 赤陶 | `terracotta` | 暖橙色，满底圆角标题 |
| 字节蓝 | `bytedance` | 蓝青渐变，科技现代 |
| 中国风 | `chinese` | 朱砂红，古典雅致 |
| 报纸 | `newspaper` | 纽约时报风，严肃深度 |
| GitHub | `github` | 开发者风，浅色代码块 |
| 少数派 | `sspai` | 中文科技媒体红 |
| 包豪斯 | `bauhaus` | 红蓝黄三原色，先锋几何 |
| 墨韵 | `ink` | 纯黑水墨，极简留白 |
| 暗夜 | `midnight` | 深色底+霓虹色 |

### 精选风格（7 个）

| 主题 | ID | 风格 |
|------|-----|------|
| 运动 | `sports` | 渐变色带，活力动感 |
| 薄荷 | `mint-fresh` | 薄荷绿，清爽 |
| 日落 | `sunset-amber` | 琥珀暖调 |
| 薰衣草 | `lavender-dream` | 紫色梦幻 |
| 咖啡 | `coffee-house` | 棕色暖调 |
| 微信原生 | `wechat-native` | 微信绿 |
| 杂志 | `magazine` | 超大留白，品质长文 |

### 模板系列（14 个）

4 种布局（Minimal / Focus / Elegant / Bold）× 多种配色（Gold / Blue / Red / Green / Navy / Gray）

## 内置排版增强

- **CJK 间距修复**：中英文/中数字之间自动加空格
- **加粗标点修复**：`**文字，**` → `**文字**，`
- **纯内联样式**：所有 CSS 写在 `style="..."` 上
- **列表模拟**：`<ul>/<ol>` → `<section>` + flexbox
- **外链转脚注**：自动变为正文标注 + 文末脚注
- **语法高亮**：代码块自动着色 + Mac 风格工具栏
- **深色模式**：自动生成微信深色模式 data-darkmode-* 属性
- **多类型 callout**：tip/note/important/warning/caution 各有独立配色
- **图说识别**：图片后斜体自动变居中灰色图说
- **对话气泡**：`:::dialogue` 左右交替聊天气泡
- **图片画廊**：`:::gallery` 横向滚动多图容器
- **时间线**：`:::timeline` 时间线展示
- **步骤流程**：`:::steps` 编号步骤
- **对比卡片**：`:::compare[A vs B]` 两列对比
- **人物引言**：`:::quote[人名]` 引言卡片
- **表格斑马纹**：自动奇偶行背景色

## 容器语法

```markdown
:::dialogue[采访实录]
Alice: 你好
Bob: 你好，很高兴认识你
:::

:::gallery[产品截图]
![](img1.jpg)
![](img2.jpg)
![](img3.jpg)
:::

:::timeline[发展历程]
2020: 项目启动
2022: 用户破百万
2024: 全球化
:::

:::steps[操作步骤]
打开设置页面
点击高级选项
开启开发者模式
:::

:::compare[方案 A vs 方案 B]
速度快 | 稳定性高
成本低 | 安全性强
:::

:::quote[乔布斯]
Stay hungry, stay foolish.
:::

> [!tip] 小技巧
> 选择适合文章风格的主题效果更佳

> [!important] 核心观点
> 这是文章的关键洞察
```
