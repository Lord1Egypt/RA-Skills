---
name: yuanfang-html-ppt
description: |
  HTML方案生成PPTX演示文稿。给定文字或URL，自动提取内容，选择模板风格，生成专业级多页PPT（14种布局，覆盖封面、目录、内容、数据、对比、时间线等）。
  相比AI生图，HTML方案100%可控：文字精确、像素级布局、零API成本、可批量、PowerPoint原生格式可二次编辑。
当用户提到"PPT"、"演示文稿"、"deck"、"幻灯片"、"路演"、"提案"、"报告"时考虑使用此技能。
---

# yuanfang-html-ppt — HTML方案PPTX演示文稿生成

## 依赖

本 skill 依赖同仓库 `yuanfang-design/` 共享设计库：
- `yuanfang-design/base.css` — token CSS 变量
- `yuanfang-design/themes/*.css` — 12 个主题

---

## 核心概念

**一份 YAML，两个产出。** YAML 是唯一数据源，LLM 生成 → 用户可改 → 渲染出 PPTX + HTML：

```
用户输入 (URL/文本/需求)
    ↓  LLM 理解 + 编排
content.yaml   ← 可人工编辑（注释说明每个字段）
    ↓  渲染 (render-html-pptx.js)
deck.pptx  +  deck.html（保留用于调试）
```

**YAML 优先的原因：**
- 人类可直接编辑，支持注释
- LLM 生成 YAML 比 JSON 更稳定（少括号/引号错误）
- LLM 读 YAML 修改时保留原有注释结构
- `load-content.js` 自动识别 `.yaml` / `.yml` / `.json`

---

## 工作流 (Step 0–4)

### Step 0: 提取品牌资产 (URL → logo + 主题色)

agent 用 web fetch 读页面，自动提取：

| 资产 | 来源 | 用途 |
|---|---|---|
| **logo 图片** | favicon / apple-touch-icon / og:image | 封面右上角，**询问用户后决定** |
| **品牌名** | og:site_name / 域名 | 仅供参考 |
| **主题色** | `theme-color` meta / CSS 变量 | 建议值，**询问用户后决定** |
| **字体** | Google Fonts link / `@font-face` | 字体建议 |

文本输入则跳过。**提取结果只是建议，不是终值。**

**[等待用户确认后才能进 Step 1]**

---

### Step 1: 提取内容 — 生成 content.yaml

agent 根据 URL/文本内容，自主编排成多页 PPT，输出 `content.yaml`：

#### 按内容类型选择策略

| 内容类型 | PPT 结构 |
|---|:---|
| 产品介绍 | cover → content×N → comparison → stat → thanks |
| 路演/融资 | cover → stat → timeline → comparison → thanks |
| 报告/分析 | cover → toc → content×N → data → big-quote → thanks |
| 方案/提案 | cover → toc → process → three-column → thanks |

#### 生成的 content.yaml 示例（带注释）

```yaml
# AICS 智能客服平台 — 路演 PPT
brand: AICS
theme: tech-modern          # 12 主题之一，可选
title: "AICS — 智能客服平台"
author: AICS Team

slides:
  # ── 封面 ──
  - layout: cover
    kicker: "KEYNOTE · 2026"
    title: "AICS — <span class=\"gradient-text\">智能客服平台</span>"
    subtitle: "基于 RAG 知识库与大语言模型的企业级智能客服系统"
    tags: ["3 分钟上线", "双 LLM 自动容灾"]
    logo: "data:image/svg+xml,..."   # SVG/PNG data URL 或图片路径
    footer: "AICS · 智能客服平台"

  # ── 目录 ──
  - layout: toc
    kicker: "目录"
    title: "今天讲的三件事"
    items:
      - title: "市场洞察"
        desc: "为什么企业需要智能客服"
      - title: "核心能力"
        desc: "RAG 知识库 · 多渠道 · AI Agent"
      - title: "产品路线图"
        desc: "2026 年规划与愿景"

  # ── 关键数据 ──
  - layout: stat
    kicker: "Traction · 关键数字"
    stats:
      - value: "3 min"
        label: "上线时间"
        context: "注册即用，无需部署"
      - value: "99.9%"
        label: "系统可用性"
        context: "双 LLM 自动容灾"
    caption: "从 0 到 1，智能客服 3 分钟起步"
    footer: "AICS"

  # ── 内容页 ──
  - layout: content
    title: "什么是 AICS"
    body: "<p>AICS 是一款基于 <strong>RAG 知识库</strong> 和 <strong>大语言模型</strong> 的智能客服平台</p>"
    footer: "AICS"

  # ── 三栏特性 ──
  - layout: three-column
    kicker: "三大核心能力"
    title: "AICS 的核心"
    lede: "RAG + LLM + 多渠道，三位一体。"
    items:
      - icon: "📚"
        title: "RAG 知识库"
        desc: "草稿/发布双版本管理，智能分段，自动更新"
      - icon: "🌐"
        title: "多渠道接入"
        desc: "网页 Widget、API、第三方平台全覆盖"
      - icon: "🤖"
        title: "AI Agent 技能"
        desc: "自定义技能编排，双 LLM 引擎自动容灾"

  # ── 对比 ──
  - layout: comparison
    kicker: "Before vs After"
    title: "AICS vs 传统客服方案"
    leftLabel: "传统客服"
    rightLabel: "AICS"
    items:
      - left: "部署周期数周"
        right: "3 分钟上线"
      - left: "单点故障风险"
        right: "双 LLM 自动容灾"
      - left: "知识库手动维护"
        right: "草稿/发布双版本自动更新"

  # ── 流程 ──
  - layout: process
    kicker: "How-to"
    title: "3 分钟上线 AICS"
    lede: "三步走，从注册到上线。"
    steps:
      - title: "注册账号"
        desc: "访问 aics.financialagent.cc"
        tag: "~1 min"
      - title: "导入知识库"
        desc: "上传文档，AI 自动分段"
        tag: "~1 min"
      - title: "嵌入网站"
        desc: "复制一行代码到网站"
        tag: "~1 min"

  # ── 时间线 ──
  - layout: timeline
    kicker: "Roadmap"
    title: "AICS 产品路线图"
    items:
      - year: "2026 Q1"
        title: "MVP 上线"
        desc: "RAG 知识库 + 网页 Widget"
      - year: "2026 Q2"
        title: "多渠道扩展"
        desc: "API / 第三方平台接入"
      - year: "2026 Q3"
        title: "AI Agent 技能"
        desc: "自定义技能编排"
      - year: "2026 Q4"
        title: "企业级功能"
        desc: "团队协作 + SSO"

  # ── 结尾 ──
  - layout: thanks
    subtitle: "开始使用 AICS"
    points: ["aics.financialagent.cc", "2026 · AICS"]
```

**[等待用户确认/修改后才能进 Step 2]**

---

### Step 2: 询问样式

#### 第一轮 (必答) — 主题

| 主题 | 底色 | accent | 风格 | 适合 |
|------|------|--------|------|------|
| `minimal-white` | 白 #FFF | #5856E9 紫蓝 | 干净白底 | 通用, 默认 |
| `minimal-white-editorial` | 白 #FAFAFA | #4F46E5 紫蓝 | 瑞士留白 | 高端品牌 |
| `tech-modern` | 深 #0F172A | #4FACFE 蓝 | 科技终端风 | AI/科技产品 |
| `corporate-clean` | 白 | #2563EB 蓝 | 商务蓝 | 企业 SaaS |
| `tokyo-night` | 深 #1A1B26 | #7AA2F7 紫蓝 | 霓虹极客 | 开发者向 |
| `pitch-deck-vc` | 白 | #0070F3 蓝 | YC 风路演 | 融资演示 |
| `dark-gold` | 深 #1A1A2E | #E2B714 金 | 黑金高端 | 重大发布 |
| `magazine-cover` | 暖白 | 渐变 | 杂志封面 | 品牌首发 |
| `bold-poster` | 黑 #000 | #FF3355 红 | 海报风 | 活动宣传 |
| `editorial` | 暖白 | #C0392B 红 | 编辑风 | 深度分析 |
| `editorial-serif` | 暖白 | #C0392B 红 | 衬线编辑 | 高端长文 |
| `warm-handdrawn` | 奶白 | #D97706 橙 | 手绘风 | 个人故事 |
| `data-infographic` | 浅灰 | #10B981 绿 | 数据信息图 | 数据报告 |
| `list-ranking` | 白 | #4F46E5 紫蓝 | 榜单排名 | Top 10 |
| `split-screen` | 白 | #4F46E5 紫蓝 | 分屏对比 | A/B 对比 |
| `eastern` | 米色 | #8D6E63 棕 | 东方美学 | 文化/本地 |
| `catppuccin-latte` | 暖白 | #DD7878 粉 | 暖色系 | 轻松内容 |
| `catppuccin-mocha` | 深 | #F5C2E7 粉紫 | 暗色系 | 暗色舒适 |

抓到了品牌色 → 推荐色调最接近的 2–3 个。没抓到 → 默认 `minimal-white`。

#### 第二轮 (必答) — logo + 品牌色

抓到就问"用这个/换 URL/不要"，没抓到就问"要加吗"。品牌色同理。

#### 第三轮 (可选)

页脚（默认品牌名 + 页码）、页数范围。

**[每轮等待用户回答后才能继续]**

---

### Step 3: 渲染

```bash
node yuanfang-html-ppt/scripts/render-html-pptx.js \
  --file content.yaml \
  --theme tech-modern \
  --brand-color "#4F46E5" \
  --output deck.pptx
```

| Flag | 说明 |
|------|------|
| `--file` | content.yaml 路径（也支持 .json/.yml） |
| `--theme` | 主题名 |
| `--output` | 输出的 PPTX 路径 |
| `--format` | `pptx` / `pdf` / `png` |
| `--brand-color` | 品牌色 hex，覆盖 theme accent |

**每次渲染同步产出 HTML 文件**：`deck.html` 与 `deck.pptx` 同目录，用于调试和对比。

渲染前 agent 自动验证 YAML 语法（用 JS-YAML parse），有错误提示用户修正。

**[等待用户确认渲染结果]**

---

### Step 4: 修改内容

用户说"改" → agent 直接修改 `content.yaml` 的对应字段 → 重新渲染，无需走完整流程：

| 用户说 | agent 做 |
|--------|---------|
| "封面标题改一下" | 读取 content.yaml，修改 `slides[0].title`，写回 |
| "加一页数据" | 在 slides 数组插入 stat/data 块 |
| "删掉第 5 页" | 删除对应 slide |
| "换主题" | 修改顶层的 `theme` 字段 |
| "第三页数据不对" | 找到对应 slide 修改数值 |

**修改流程**：

```
content.yaml
    ↓  agent 读取
    ↓  agent 定位修改位置 + 修改
    ↓  写回 content.yaml（保留注释）
    ↓  agent 验证 YAML 语法（js-yaml.load）
    ↓  语法错误 → 提示用户修复 / 语法正确 → 渲染
    ↓
deck.pptx + deck.html（保留，用于调试）
```

用户也可以**直接在自己的编辑器里改 YAML**（有注释说明每个字段），改完说"重新渲染"即可。

**[等待用户确认/继续修改]**

---

## 14 种布局

| 布局 | 用途 | 关键字段 |
|------|------|---------|
| `cover` | 封面 | title, subtitle, kicker, tags, logo |
| `section` | 章节分割 | title |
| `content` | 标题+正文 | title, body (HTML) |
| `two-column` | 双栏 | leftTitle, leftPoints, rightTitle, rightPoints |
| `data` | KPI 网格 | metrics[{label,value,change}] |
| `quote` | 客户引用 | quote, attribution, role |
| `summary` | 下一步 | title, points[] |
| `toc` | **目录** | items[{title,desc}] |
| `three-column` | **三栏特性** | items[{icon,title,desc}] |
| `process` | **流程步骤** | steps[{title,desc,tag}] |
| `timeline` | **时间线** | items[{year,title,desc}] |
| `big-quote` | **大字号引言** | quote, attribution, role |
| `stat` | **关键数据** | stats[{value,label,context}], caption |
| `comparison` | **对比** | leftLabel, rightLabel, items[{left,right}] |
| `thanks` | **结尾** | subtitle, points[] |

---

## 已知限制

- PPTX 字体 = 系统已安装字体的解析结果。可通过 post-processing 替换
- dom-to-pptx box-shadow 渲染为 PPTX 约缩小 4x
- 暂无 PPTX 母版视图 (slide master)
- 图表（原生 PPTX chart 对象）不支持。可用 CSS/div 模拟视觉图表

---

## 文件结构

```
yuanfang-html-ppt/
├── SKILL.md                      # 本文件
└── scripts/
    └── render-html-pptx.js       # 核心渲染引擎 (HTML→dom-to-pptx)
```
