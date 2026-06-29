# Multi-Illustration Mode

Generate multiple illustrations for a single article. Triggered by keywords: `多图` / `配图` / `全套` / `文章配图` / `封面+配图`.

## Core Principles

1. **Content drives quantity, not templates** — extract "visualizable units" from content, don't force a fixed number
2. **Every illustration independently passes density gate** — 3-dimension 15-point scoring, ≥9 to generate
3. **Style consistency across all illustrations** — shared design-tokens.css, shared palette + style
4. **Two confirmation points before generation** — content plan first, then style plan

## Execution Flow

```
Article Input
  ↓
Step A: Article Parsing (silent)
  ↓
Step B: Illustration Plan + Density Scoring ← Confirmation Point 1 (MANDATORY)
  ↓
Step C: Style Unification ← Confirmation Point 2 (default required, "直接生成" skips)
  ↓
Step D: Batch Generation
  ↓
Step E: Illustration Map
```

## Step A: Article Parsing (Silent)

Read the full article and extract:

| Extract | What to Look For | Illustration Type | Purpose |
|---------|-----------------|-------------------|---------|
| **Core thesis** | The one-sentence argument | cover | attention |
| **Data points** | 3+ related numbers, percentages, trends | data chart (bar/line/donut) | readability |
| **Logic chains** | Causal/sequential/conditional reasoning | logic-chain, flow-chart | readability |
| **Processes** | 3+ sequential steps | flow-chart, swimlane | readability |
| **Comparisons** | A vs B with 3+ attributes each | versus, comparison | readability |
| **Key quotes** | Statements impactful outside context | quote-card | memorability |
| **Core judgment** | Author's definitive stance/verdict | verdict-card | memorability |
| **Myth vs fact** | Misconceptions to correct | myth-fact-card | memorability |
| **Audience signal** | "适合谁/不适合谁" content | audience-fit-card | attention |
| **Brand manifesto** | Value statements, declarations | manifesto-card | memorability |
| **Hierarchies** | Nested/categorical structures | tree-chart, layered-diagram | readability |
| **Timelines** | Chronological milestones | timeline | readability |
| **Supply/demand** | Gap/shortage narratives | bar-chart, waterfall | readability |
| **Cases/testimonials** | Real examples with outcomes | cases-card | memorability |
| **Definitions** | Technical terms needing explanation | definition-card | readability |
| **Action items** | CTA, subscribe, follow guidance | cta-card, subscribe-card | conversion |
| **Brand info** | Author name, publication, QR code | back-cover | conversion |
| **Chapter transitions** | Between-section bridges | bridge-card, section-divider | readability |
| **Series context** | "第N篇，共M篇" | series-card | attention |
| **Alerts/notices** | Important warnings, policy changes | notice-card, callout-card | attention |

### Extraction Rules

- A "visualizable unit" must have **≥2 data points** OR **a clear logical structure** OR **standalone quote impact**
- Isolated single numbers are NOT visualizable (e.g., "48天" alone → not a chart; "48天 + 5000亿 + 万亿" together → timeline)
- Narrative paragraphs without data/structure/quotes are NOT visualizable
- When two units share the same source section and overlap in content, **merge** them

## Step B: Illustration Plan (Confirmation Point 1 - MANDATORY)

**Persona rule**: Never show professional jargon to the user. Translate all type names into emoji + one-sentence descriptions. Density scores are calculated internally but NOT exposed to the user.

### Internal: Density Scoring (Silent)

Each proposed illustration is scored on 3 dimensions (5 points each, 15 total):

| Dimension | 1 | 3 | 5 |
|-----------|---|---|---|
| **Information Increment** | Pure decoration | Reorganizes for clarity | Reveals invisible structures |
| **Data Value** | No data | 2-3 data points | 4+ data points + relationships |
| **Standalone Readability** | Fully context-dependent | Needs title only | Self-explanatory |

**Gate threshold: ≥9/15.** Below 9 = skip or merge. Cover/back-cover exemption: ≥6/15.

### User-Facing Output Format (MANDATORY)

Present the plan in natural language, NOT technical terms:

```
📋 配图方案：共 N 张

我帮你从文章中提取了这些值得做配图的内容亮点：

┌──────────────────────────────────────────────────┐
│ #1 📷 封面                                        │
│ [文章核心论点/标题]                                 │
│                                                    │
│ #2 [emoji] [一句话描述]                            │
│ [具体内容亮点，用户能看懂的语言]                     │
│                                                    │
│ #3 ...                                             │
└──────────────────────────────────────────────────┘

💡 我的建议：
- [主动给出精简/丰富/合并的具体建议]
- [指出哪几张可以合并，哪张信息密度最高]

你想怎么调整？（也可以直接说"确认"）
```

### Emoji + Description Mapping (Internal → User-Facing)

| Internal Type | Emoji | User-Facing Description |
|---------------|-------|------------------------|
| cover | 📷 | 封面 |
| back-cover | 📷 | 封底 |
| quote-card | 💬 | 金句图 |
| verdict-card | ⚖️ | 最终判断卡 |
| myth-fact-card | 🔍 | 认知纠偏卡 |
| audience-fit-card | 👥 | 读者匹配卡 |
| manifesto-card | 🏴 | 宣言卡 |
| bridge-card | 🌉 | 转场卡 |
| callout-card | 📢 | 提示框 |
| definition-card | 📖 | 术语定义卡 |
| cases-card | 🏆 | 案例卡 |
| notice-card | 🚨 | 重要通知卡 |
| series-card | 📚 | 系列说明卡 |
| subscribe-card | 🔔 | 关注引导卡 |
| rule-card | ⚡ | 铁律/规则卡片 |
| checklist-card | 🛡️ | 检查清单 |
| cheatsheet-card | 🎯 | 速查表 |
| logic-chain | 💡 | 论证链 |
| process-pipeline | 🔧 | 流程管道 |
| version-timeline | 📈 | 版本演进线 |
| bar-chart | 📊 | 数据对比图 |
| donut-chart | 🍩 | 份额占比图 |
| waterfall | 💰 | 投资结构图 |
| section-divider | ➖ | 章节分隔图 |

### Purpose-Based Design Adjustments (Internal)

Each illustration's `purpose` (from Step A) adjusts design parameters silently:

| Purpose | Visual Tendency | Token Overrides |
|---------|----------------|-----------------|
| **attention** | High contrast, large type, brand color prominent, generous whitespace | `--text-hero` +20%, `--color-accent-1` saturation +15%, `--space-12` for padding |
| **readability** | Clear hierarchy, structured layout, comfortable spacing | Default tokens, `--leading-relaxed` for body, `--space-6` gaps |
| **memorability** | Single focus, quote magnified, visual anchor, minimal noise | `--text-hero` +30%, reduce to 1 accent color, `--space-16` around focal point |
| **conversion** | CTA prominent, brand info complete, action guidance | `--color-accent-1` for CTA, `--radius-md` for buttons, brand logo area |

**Rule**: Purpose adjusts tokens within the same shared design-tokens.css. Never create a separate token file per purpose.

### User Override (Natural Language)

User can say:
- "确认" → proceed with plan
- "去掉第N张" → remove
- "加上[描述]" → add (override gate)
- "第N张换成[描述]" → change type
- "合并第M和第N张" → merge
- "大师推荐" → auto-decide, skip this confirmation point

### Master Mode Shortcut

If user said "大师推荐"/"你定"/"直接来" at Mode Detection:
- Skip Step B output entirely
- Auto-select all gate-passed illustrations
- Auto-merge overlapping items
- Proceed directly to Step C (or skip Step C too if Master Mode)

## Step C: Style Customization (Confirmation Point 2)

**Persona rule**: Never ask users to choose from style/palette/font names. Use 3 simple questions instead. Every option must explain what it MEANS, not what it IS.

### Category Detection (Silent, before Q1)

Before asking the 3 questions, silently detect the content category from the article's topic, keywords, and structure. This determines the default visual language recommendation.

| Category | Detection Signals | Default Mode | Default Palette | Key Visual Trait |
|----------|------------------|-------------|----------------|-----------------|
| **深度观察/商业洞察** | "IPO"/"估值"/"财报"/"行业"/"竞争" | Swiss | IKB Blue | 数据大字报、KPI塔、对比矩阵 |
| **科技/产品** | "AI"/"发布"/"功能"/"测评"/"对比" | Swiss | IKB Blue or Safety Orange | 设备框截图、功能矩阵、版本对比 |
| **人文/文化** | "历史"/"文学"/"艺术"/"电影"/"音乐" | Editorial | 牛皮纸 or 森林墨 | 衬线大标题、引文居中、大留白 |
| **职场/干货** | "方法"/"步骤"/"清单"/"工具"/"效率" | Swiss | Lemon Green | 编号列表、步骤流程、速查表 |
| **旅行/生活方式** | "旅行"/"城市"/"美食"/"探店"/"推荐" | Editorial | 暖色/earth | 大图压全屏、衬线标题、地图组件 |
| **读书/笔记** | "书评"/"阅读"/"笔记"/"摘录"/"金句" | Editorial | 墨水经典 | 衬线字体、引文居中、留白拉满 |
| **人物/访谈** | "专访"/"对话"/"人物"/"故事"/"经历" | Editorial | 沙丘 or 森林墨 | 人物特写、问答版式、引言突出 |
| **数据/研究** | "研究"/"报告"/"调查"/"数据"/"统计" | Swiss | IKB Blue | 图表密集、数据标签、灰阶层级 |
| **观点/评论** | "我认为"/"其实"/"真相"/"误区"/"反思" | Editorial | 墨水经典 | 金句放大、判断卡、认知纠偏 |
| **教程/指南** | "教程"/"指南"/"如何"/"入门"/"从零开始" | Swiss | Lemon Green | 步骤流程、截图美化、编号清单 |

**Rule**: Category detection is a SILENT suggestion. If the user's Q1 answer contradicts the detected category, user's explicit answer wins.

**User-facing output** (only in non-Master mode):
"我检测到这篇文章属于 [品类]，推荐 [模式] 风格。你也可以在下面3个问题中调整。"

### The 3 Questions (User-Facing)

```
🎨 风格定制（3个问题帮你定调）

问题1：你的文章调性是？
  A. 严肃深度（像经济学人、财新）  → Editorial Magazine：衬线体 + 暖色底 + 单品牌色
  B. 专业理性（像36氪、极客公园）  → Swiss International：无衬线 + 灰白底 + 高反差功能色
  C. 温暖人文（像人物、GQ报道）    → Editorial Magazine：衬线+无衬线混搭 + 暖棕底
  D. 活泼有趣（像差评、半佛仙人）  → Swiss International：大胆撞色 + 强调色 + 粗体

问题2：读者第一眼应该感受到什么？
  A. "这文章有分量"  → 加重衬线体 + 深色标题 + 大字封面
  B. "这数据很硬"    → 加粗数字 + 图表突出 + 数据标签
  C. "这观点很犀利"  → 金句放大 + 高对比 + 红色强调
  D. "这方法很实用"  → 结构清晰 + 步骤感强 + 编号突出

问题3：配色偏好？
  A. 跟着文章来源走（微信绿/经济学人红/知乎蓝...）→ 自动检测品牌DNA
  B. 我有指定色系：______
  C. 你来定，高级就行  → 默认克制风（单品牌色 + 暖灰层级）

---
💡 快捷方式：
- "大师推荐" → 跳过3个问题，我根据文章自动判断
- "和上次一样" → 读取上次风格配置
```

### Answer → Style Mapping (Internal)

| Q1 Answer | Q2 Answer | Q3 Answer | Mode | Internal Style | Internal Palette | Font Preset |
|-----------|-----------|-----------|------|---------------|-----------------|-------------|
| A (严肃深度) | any | any | Editorial | kami-editorial | ink-blue / brand-DNA | kami-serif |
| B (专业理性) | any | any | Swiss | swiss-intl | IKB Blue (default) | 现代简约 |
| C (温暖人文) | any | any | Editorial | morandi-journal | warm-earth | editorial-mix |
| D (活泼有趣) | any | any | Swiss | swiss-bold | Lemon Yellow / Safety Orange | 现代简约 |

### Visual Rhythm Planning (主题节奏规划)

**Before generating, plan the visual rhythm across all illustrations.** Inspired by guizang's theme rhythm system.

Each illustration gets a theme class that controls its visual weight:

| Theme Class | Visual Effect | When to Use |
|------------|--------------|-------------|
| **hero** | Maximum visual impact, large type, strong contrast | Cover, back-cover, key verdict |
| **dark** | Dark background, light text, breathing room | Logic chains, myth-fact, manifesto |
| **light** | Light background, dark text, content-dense | Metrics, data charts, checklists |
| **accent** | Accent color highlight, attention-grabbing | Quote cards, callouts, CTA |

**Hard rules**:
- No more than 3 consecutive illustrations with the same theme class
- Sets of 6+ illustrations must have ≥1 hero + ≥1 dark + ≥1 light
- Every 3-4 content illustrations, insert 1 hero or dark illustration for visual breathing
- Cover and back-cover are always hero
- The overall rhythm should feel like: **hero → content → content → breathing → content → hero**

**Example rhythm for 8 illustrations**:
```
01-cover:     hero (dark)
02-metrics:   light
03-logic:     dark
04-pipeline:  light
05-timeline:  light
06-myth-fact: dark
07-quote:     accent
08-back:      hero (light)
```

**Self-check**: After planning, verify rhythm is not monotonous. If all content pages are "light", the set feels flat — add dark/accent pages.

Q2 fine-tunes: A→heavier headings, B→larger numbers, C→bigger quotes, D→stronger structure
Q3 overrides palette: A→brand-DNA auto-detect, B→user custom, C→default restrained

### Style Consistency Rules

1. **All illustrations share the same design-tokens.css** — one palette, one font system
2. **Layout varies per illustration type** — but colors/fonts/spacing are identical
3. **Brand DNA applies to all** — if economist-red is selected, ALL illustrations use it
4. **Individual illustration style override is allowed** — e.g., "第3张用纸墨风" → that one gets its own tokens override

### Skip Conditions

- User says "直接生成" / "大师推荐" → skip Step C, auto-match style from content analysis
- User says "快速搞定" → skip both Step B and Step C (density gate still applies silently)

## Step D: Batch Generation

### Output Directory Structure

```
[article-name]-illustrations/
├── shared/
│   └── design-tokens.css          ← Shared across all illustrations
├── 01-cover/
│   ├── data.js
│   ├── components/
│   │   └── CoverHero.jsx
│   └── App.jsx
├── 02-timeline/
│   ├── data.js
│   ├── components/
│   │   └── MilestoneTimeline.jsx
│   └── App.jsx
├── ...
├── 08-back-cover/
│   ├── data.js
│   ├── components/
│   │   └── BackCover.jsx
│   └── App.jsx
└── index.html                      ← Preview all illustrations in one page
```

### Generation Rules

1. **Shared design-tokens.css** — generated once, referenced by all
2. **Each illustration has its own data.js** — isolated, independently editable
3. **Component granularity** — same 80-line limit as single mode
4. **Naming convention** — `{NN}-{type}/` where NN is zero-padded sequence number
5. **index.html** — a single preview page showing all illustrations in order, for quick review
6. **Hero pages (cover/back-cover) MUST use photo backgrounds** — see rule below

### Hero Page Background Rule (封面/封底背景图规则)

Cover and back-cover are **hero** pages — their job is to stop the reader from scrolling past. A solid-color background cannot do this. They MUST have a relevant photo as background.

**Mandatory**:
- Cover: Use a photo from Pexels/Unsplash/Wallhaven (see `references/image-sources.md`) as full-bleed background
- Back-cover: Use a photo or a darkened version of the cover photo as background
- Text must be placed in the photo's "quiet zone" (low-detail, low-contrast area)
- Apply Image-Text Conflict Protection rules from `references/aesthetics-guide.md`

**Photo search keywords by content type**:
| Content Type | Search Keywords | Source |
|-------------|----------------|--------|
| 科技/产品 | `{topic} technology`, `rocket launch`, `satellite` | Unsplash > Pexels |
| 商业/金融 | `{topic} business`, `stock market`, `city skyline night` | Unsplash |
| 人文/文化 | `{topic} culture`, `library`, `bookshelf` | Unsplash |
| 旅行/生活 | `{topic} travel`, `landscape`, `city` | Pexels > Unsplash |
| 数据/研究 | `abstract dark`, `data visualization`, `blue technology` | Wallhaven > Unsplash |

**Text overlay treatment**:
- Light photo → dark text with subtle text-shadow
- Dark photo → light text (#e8ecf4) with no shadow needed
- Mixed → add a semi-transparent gradient overlay ONLY around text area (not full canvas)
- **Never** apply a full-canvas dark overlay that destroys the photo

**Swiss mode exception**: Swiss hero pages CAN use photo backgrounds. The "no decoration" rule applies to CONTENT pages only. A cover with just text on white is NOT a Swiss cover — it's a missed opportunity.

### WeChat Public Account Size Specs

| Illustration Type | Width | Height | Ratio | Usage |
|------------------|-------|--------|-------|-------|
| 封面 (cover) | 900px | 383px | 2.35:1 | 文章封面 |
| 正文配图 (body) | 640px | auto | flexible | 文章内嵌 |
| 金句图 (quote) | 640px | 640px | 1:1 | 文章内嵌/朋友圈 |
| 章节分隔 (divider) | 640px | 200px | ~3:1 | 章节间 |
| 封底 (back-cover) | 900px | 383px | 2.35:1 | 文章结尾 |

### WeChat Density Check (公众号密度铁律)

Before delivery, verify each illustration passes these checks:

**For 640px-wide content illustrations**:
- [ ] Active composition ≥70% of canvas height (not mostly empty)
- [ ] At least 3 content elements per illustration (title + body + data/image/quote)
- [ ] No pure blank vertical band >30% of canvas height without design reason
- [ ] Text legible at 50% zoom (simulates mobile viewing)

**For 900×383px covers**:
- [ ] Cover communicates topic in 1 second (photo + title + kicker)
- [ ] Text not overlapping photo subject/faces
- [ ] Title readable at 360px wide (thumbnail test)

**For 640×640px quote cards**:
- [ ] Quote is the single focal point
- [ ] Attribution clearly below quote
- [ ] No more than 50 characters of Chinese text (otherwise split)

## Step F: Screenshot & Deliver (截图交付)

After generating HTML files, convert them to PNG/JPEG for direct upload to WeChat Official Account.

### Screenshot Method: Puppeteer-core + System Chrome

**Dependencies**: puppeteer-core (does NOT download Chromium)

**Chrome Path Detection** (Windows, in order):
1. Registry: `HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe`
2. Playwright: `$env:LOCALAPPDATA\ms-playwright\chromium-*\chrome-win64\chrome.exe`
3. Default: `C:\Program Files\Google\Chrome\Application\chrome.exe`

**Screenshot Parameters by Illustration Type**:

| Type | Viewport | deviceScaleFactor | Output |
|------|----------|-------------------|--------|
| 封面 (cover) | 900×383 | 2 | PNG |
| 正文配图 (body) | 640×auto | 2 | PNG |
| 金句图 (quote, 1:1) | 640×640 | 2 | PNG |
| 章节分隔 (divider) | 640×200 | 2 | PNG |
| 封底 (back-cover) | 900×383 | 2 | PNG |

**Screenshot Script Template**:
```javascript
const puppeteer = require('puppeteer-core');

// Detect Chrome path
const chromePath = detectChromePath(); // Use detection logic above

const browser = await puppeteer.launch({
  headless: 'new',
  executablePath: chromePath,
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
});

const page = await browser.newPage();
await page.setViewport({ width: 900, height: 383, deviceScaleFactor: 2 });
await page.goto('file:///path/to/01-cover.html', { waitUntil: 'networkidle0', timeout: 30000 });
await page.evaluate(() => document.fonts.ready);
await new Promise(r => setTimeout(r, 5000)); // Wait for external images to load
await page.screenshot({ path: 'output/01-cover.png', type: 'png', fullPage: false });
```

**CRITICAL: Background Image Compatibility**:
- CSS `background-image: url(...)` may NOT load in Puppeteer headless mode
- **Always use `<img>` tag** for photo backgrounds, positioned absolutely with `object-fit: cover`
- Correct pattern:
  ```html
  <div style="position:relative;width:900px;height:383px;overflow:hidden">
    <img src="https://..." style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover" />
    <div style="position:absolute;inset:0;background:linear-gradient(...)"></div>
    <div style="position:relative;z-index:2">Content</div>
  </div>
  ```
- Wrong pattern (may not load):
  ```html
  <div style="background-image:url('https://...')">Content</div>
  ```

**Wait Strategy**:
- `waitUntil: 'networkidle0'` — wait for all network requests to finish
- `document.fonts.ready` — wait for web fonts to load
- **5 second buffer** — wait for external images (Unsplash/Pexels) to fully render
- For auto-height pages (640×auto): use `fullPage: true` in screenshot options

### Output Directory Structure

```
[article-name]-illustrations/
├── output/                          ← PNG screenshots go here
│   ├── 01-cover.png
│   ├── 02-metrics.png
│   ├── 03-logic-chain.png
│   ├── ...
│   └── 08-back-cover.png
├── 01-cover.html                    ← Source HTML files
├── 02-metrics.html
├── ...
└── 08-back-cover.html
```

### Delivery Package

After all screenshots are taken:
1. Verify each PNG is not blank (check file size > 10KB)
2. Create a zip: `Compress-Archive -Path output\*.png -DestinationPath "[article-name]公众号配图.zip" -Force`
3. Save to user's desktop: `Move-Item "[article-name]公众号配图.zip" "$env:USERPROFILE\Desktop\"`
4. Report to user: "8张配图已截图为PNG，打包在桌面：[article-name]公众号配图.zip"

### Quality Check Before Delivery

- [ ] All PNG files exist and size > 10KB
- [ ] Cover/back-cover have visible photo backgrounds (not blank white)
- [ ] Text is legible at 50% zoom (mobile preview)
- [ ] No broken images (Unsplash/Pexels loaded correctly)
- [ ] Chinese characters rendered correctly (fonts loaded)

## Step E: Usage Guide

**Persona rule**: Don't show technical file trees. Show users WHERE to put each illustration in their article, and HOW to quickly modify anything they don't like.

### User-Facing Output Format

```
🗺️ 配图使用指南

你的文章配图已经准备好了！以下是每张图在文章中的建议位置：

§1 [章节名] ──── 📷 #1 封面（设为公众号封面图）
§2 [章节名] ──── [emoji] #2 [描述]（插在[具体位置建议]）
§3 [章节名] ──── [emoji] #3 [描述]（插在[具体位置建议]）
...
§N 结尾 ──────── 📷 #N 封底（文章末尾，引导关注）

📝 快速修改（告诉我就行）：
- "第N张颜色太深" → 我帮你调
- "第N张加个[元素]" → 我帮你加
- "全部换个风格" → 我重新生成
- "导出图片" → 我帮你截图保存

🔧 技术编辑（如需精细调整）：
- 修改数据 → 改对应目录的 data.js
- 修改配色 → 改 shared/design-tokens.css（全局生效）
- 修改单张风格 → 在该目录新建 local-tokens.css 覆盖
- 调整顺序 → 重命名目录编号
```

### Master Mode Addition

In Master Mode, after showing the usage guide, also ask:

```
对结果满意吗？不满意可以告诉我：
- "第N张改一下" → 进入微调模式
- "重新来" → 回到 Step B 重新规划
```

## Illustration Type Templates

### Cover (封面)

```jsx
// Layout: hero-center
// Content: thesis statement + author + source + date
// Size: 900×383
// Density: low (visual impact > information density)
// Required data: { thesis, author, source, date, accentText }
```

### Back Cover (封底)

```jsx
// Layout: center-stack
// Content: publication name + author + QR placeholder + CTA
// Size: 900×383
// Density: low (brand identity > information)
// Required data: { publicationName, author, qrPlaceholder, cta }
```

### Quote Card (金句图)

```jsx
// Layout: single-focus
// Content: one powerful quote + attribution + context hint
// Size: 640×640
// Density: medium (one idea, maximum impact)
// Required data: { quote, attribution, contextHint }
// Gate rule: quote must be impactful WITHOUT full article context
```

### Rule Card (铁律/规则卡片)

```jsx
// Layout: grid-cards (compact)
// Content: numbered rules + violation consequence / impact per rule
// Size: 640px wide
// Density: high (distills rules into scannable format)
// Required data: { title, rules: [{ number, rule, consequence? }] }
// Gate rule: must have ≥2 rules with clear, actionable content
// When to use: "三条铁律"/"5条原则"/"7条红线" type content
```

### Checklist Card (清单/检查项卡片)

```jsx
// Layout: vertical-list with status markers
// Content: numbered items + description + severity/status marker (e.g., RED FLAG, ✅, ⚠️)
// Size: 640px wide
// Density: high (actionable checklist)
// Required data: { title, items: [{ number, description, severity? }] }
// Gate rule: must have ≥3 items with distinct, non-overlapping descriptions
// When to use: "安全红线"/"检查清单"/"避坑指南" type content
```

### Cheatsheet Card (速查表卡片)

```jsx
// Layout: dense-grid (2-3 columns)
// Content: numbered entries + name + one-line example, ultra-compact
// Size: 640px wide
// Density: very high (maximum information per pixel)
// Required data: { title, entries: [{ id, name, example }] }
// Gate rule: must have ≥4 entries with name + example pairs
// When to use: "B1-B6访谈规则"/"速查表"/"cheatsheet" type content
```

### How to Choose Knowledge Card Sub-Type

| Content Pattern | Sub-Type | Key Signal |
|----------------|----------|-----------|
| "N条铁律/原则/规则" + 每条有违反后果 | rule-card | "违反后果"/"否则" per rule |
| "N条红线/检查项" + 需要逐项打勾 | checklist-card | "检查"/"红线"/"RED FLAG" markers |
| "N个方法/规则" + 每条有简短示例 | cheatsheet-card | "示例"/"e.g." per entry, compact layout |
| 单独一句引述/金句 | quote-card | Single quote, standalone impact |

### Section Divider (章节分隔图)

```jsx
// Layout: hero-center
// Content: section number + section title + subtle decoration
// Size: 640×200
// Density: minimal (rhythm > information)
// Required data: { sectionNumber, sectionTitle }
// Gate rule: only for articles with 4+ clearly delineated sections
```

### Logic Chain (论证链)

```jsx
// Layout: flow-chart (horizontal)
// Content: causal chain with 3-6 nodes, each node = one claim
// Size: 640px wide
// Density: high (reveals structure invisible in prose)
// Required data: { nodes: [{ claim, evidence? }], connections: [{ from, to, label? }] }
// Gate rule: chain must have ≥3 nodes with clear CAUSAL relationship (A causes B)
// When to use: "A导致B导致C" type reasoning
```

### Process Pipeline (流程管道)

```jsx
// Layout: flow-chart (vertical or horizontal with input/output)
// Content: sequential phases/stages, each with input → process → output
// Size: 640px wide
// Density: high (reveals pipeline structure)
// Required data: { phases: [{ name, input, output, steps? }] }
// Gate rule: must have ≥2 phases with clear input/output boundaries
// When to use: "Phase 0 → Phase 1 → Phase 2" type pipeline, each phase has defined input/output
```

### Version Timeline (版本演进)

```jsx
// Layout: timeline
// Content: version/iteration history, each node = what changed
// Size: 640px wide
// Density: medium (shows evolution trajectory)
// Required data: { versions: [{ label, changes: string[], keyMetric? }] }
// Gate rule: must have ≥3 versions with meaningful differences
// When to use: "v1→v2→v3" type iteration history
```

### How to Distinguish

| Content Pattern | Type | Key Signal |
|----------------|------|-----------|
| "A导致B导致C" | logic-chain | Causal verbs: 导致/引起/使得 |
| "阶段0 → 阶段1 → 阶段2" | process-pipeline | Phase/stage structure with input/output |
| "v1→v2→v3" or "2023→2024→2025" | version-timeline | Version numbers or dates as nodes |
| "步骤1 → 步骤2 → 步骤3" | flow-chart (from chart-system.md) | Sequential steps without causal claim |

### Verdict Card (最终判断卡)

```jsx
// Layout: single-focus
// Content: core judgment + supporting reasoning + applicability note
// Size: 640px wide
// Density: medium (one judgment, maximum clarity)
// Purpose: memorability
// Required data: { eyebrow, title, body, note? }
// Gate rule: must have a clear, debatable judgment (not a fact)
// When to use: "最终判断"/"核心结论"/"我的判断" type content
```

### Audience Fit Card (读者匹配卡)

```jsx
// Layout: split-comparison (fit vs not-fit)
// Content: who should read + who should NOT read
// Size: 640px wide
// Density: medium (helps reader decide quickly)
// Purpose: attention
// Required data: { title, fit: string[], notFit: string[] }
// Gate rule: must have ≥1 fit AND ≥1 not-fit item
// When to use: "适合谁"/"不适合谁"/"写给谁看" type content
```

### Myth-Fact Card (认知纠偏卡)

```jsx
// Layout: binary-comparison (myth vs fact pairs)
// Content: misconception + correction pairs
// Size: 640px wide
// Density: high (corrects wrong beliefs efficiently)
// Purpose: memorability
// Required data: { title, pairs: [{ myth, fact }] }
// Gate rule: must have ≥2 myth-fact pairs
// When to use: "误区"/"真相"/"你可能以为...其实" type content
```

### Manifesto Card (宣言卡)

```jsx
// Layout: hero-center with emphasis
// Content: brand declaration / value statement
// Size: 640px wide
// Density: low (emotional impact > information)
// Purpose: memorability
// Required data: { eyebrow, title }
// Gate rule: title must be a complete assertion, not a topic label
// When to use: "我们相信"/"我的立场"/"宣言" type content
```

### Bridge Card (转场卡)

```jsx
// Layout: hero-center (lightweight)
// Content: "from → to" transition between sections
// Size: 640×200
// Density: minimal (navigation > information)
// Purpose: readability
// Required data: { from, to }
// Gate rule: only for articles with 4+ sections
// When to use: chapter transitions, "看完了X，接下来看Y"
```

### Callout Card (提示框)

```jsx
// Layout: inline-block with type-based styling
// Content: tip / warning / info / success / danger message
// Size: 640px wide
// Density: low (single message, high visibility)
// Purpose: attention
// Required data: { type: 'info'|'tip'|'warning'|'success'|'danger', text }
// Gate rule: text must be actionable (not just decorative)
// When to use: "注意"/"小技巧"/"警告"/"重要" type content
// Visual: info=blue, tip=green, warning=amber, success=green, danger=red
```

### Definition Card (术语定义卡)

```jsx
// Layout: inline-block with term highlight
// Content: term + definition + optional label
// Size: 640px wide (compact)
// Density: medium (explains jargon efficiently)
// Purpose: readability
// Required data: { term, definition, label? }
// Gate rule: term must be non-obvious to target audience
// When to use: "OKR"/"RAG"/"微服务" type jargon that needs explanation
```

### Cases Card (案例卡)

```jsx
// Layout: grid-cards (2-4 columns)
// Content: case name + industry + outcome per case
// Size: 640px wide
// Density: high (evidence compression)
// Purpose: memorability
// Required data: { title, cases: [{ name, industry, outcome }] }
// Gate rule: must have ≥2 cases with quantifiable outcomes
// When to use: "使用案例"/"客户背书"/"实战效果" type content
```

### Notice Card (重要通知卡)

```jsx
// Layout: single-focus with alert styling
// Content: urgent title + body explanation
// Size: 640px wide
// Density: low (urgency > information)
// Purpose: attention
// Required data: { title, body }
// Gate rule: must be genuinely time-sensitive or policy-critical
// When to use: "重要提醒"/"政策变更"/"限时活动" type content
```

### Series Card (系列说明卡)

```jsx
// Layout: hero-center (lightweight)
// Content: series name + episode position + topic
// Size: 640px wide
// Density: low (context > information)
// Purpose: attention
// Required data: { name, episode, topic }
// Gate rule: only for articles that are part of a series
// When to use: "第N篇，共M篇"/"XX系列" type content
```

### Subscribe Card (关注引导卡)

```jsx
// Layout: center-stack with CTA
// Content: publication name + value proposition + QR placeholder
// Size: 640px wide
// Density: low (conversion > information)
// Purpose: conversion
// Required data: { title, body, qrPlaceholder? }
// Gate rule: only at article end, paired with back-cover
// When to use: article ending, "关注"/"订阅"/"扫码" type content
```

## Anti-Patterns Specific to Multi-Illustration Mode

| Anti-Pattern | Detection | Fix |
|-------------|-----------|-----|
| **Forced quantity** | "Generate 10 illustrations" regardless of content | Remove fixed number; let content analysis determine count |
| **Filler illustrations** | Illustration with density score <9 | Skip or merge; only generate if user explicitly overrides |
| **Style drift** | Different palettes/fonts across illustrations | Enforce shared design-tokens.css |
| **Duplicate information** | Two illustrations showing the same data | Merge into one, or split by angle (e.g., same data as bar chart + donut chart = duplicate) |
| **Context-dependent quote** | Quote that makes no sense without the article | Skip; only use quotes that are independently impactful |
| **Over-illustration** | More illustrations than paragraphs | Maximum ratio: 1 illustration per 2 substantial paragraphs |
| **Under-illustration** | Article with 5+ data points but no data chart | Flag in Step B as "missed opportunity" |
| **Type overuse** | Same illustration type appears >1 time (e.g., 2 covers, 3 quote-cards) | Enforce uniqueness constraint per type (see below) |

### Uniqueness Constraint

Each illustration type has a maximum count per article. Exceeding it means the content should be merged or the type should be changed:

| Type | Max Count | Rationale |
|------|-----------|-----------|
| cover | 1 | One article, one opening |
| back-cover | 1 | One article, one closing |
| verdict-card | 1 | One core judgment per article |
| manifesto-card | 1 | One declaration per article |
| quote-card | 2 | Opening + closing, no more |
| bridge-card | N-1 | Where N = number of sections |
| section-divider | N-1 | Same as bridge |
| callout-card | 3 | Too many callouts = noise |
| All other types | 2 | If more needed, consider merging |

**Exception**: User can explicitly override with "我就是要2张封面" — respect user intent.
