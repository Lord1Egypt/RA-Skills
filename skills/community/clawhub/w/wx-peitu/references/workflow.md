# 公众号长文配图生成器 — 核心工作流

> 版本: 6.0 | 输出格式: 纯 HTML → Puppeteer 截图 → PNG 交付
> 触发词: `多图` / `配图` / `全套` / `文章配图` / `封面+配图`

## Core Principles

1. **Content drives quantity, not templates** — 从内容中提取"可视化单元"，不强制固定数量
2. **Every illustration independently passes density gate** — 3维15分评分，≥9/15 才生成
3. **Style consistency across all illustrations** — 共享设计令牌，统一调色板 + 风格
4. **Two confirmation points before generation** — 先确认内容方案，再确认风格方案

## 执行流程

```
文章输入
  ↓
Step A: 文章解析（静默）
  ↓
Step B: 配图方案 + 密度评分 ← 确认点1（必须）
  ↓
Step C: 风格定制 ← 确认点2（默认必须，"直接生成"可跳过）
  ↓
Step D: 批量生成 HTML
  ↓
Step E: 配图使用指南
  ↓
Step F: 截图交付 + 云盘同步
```

---

## Step A: 文章解析（静默）

读取全文，提取可视化单元：

| 提取项 | 寻找什么 | 配图类型 | Purpose |
|--------|---------|---------|---------|
| **核心论点** | 一句话论断 | cover | attention |
| **数据点** | 3+相关数字/百分比/趋势 | data chart | readability |
| **逻辑链** | 因果/顺序/条件推理 | logic-chain | readability |
| **流程** | 3+顺序步骤 | process-pipeline | readability |
| **对比** | A vs B 各3+属性 | versus | readability |
| **金句** | 脱离上下文仍有冲击力的陈述 | quote-card | memorability |
| **核心判断** | 作者明确立场/结论 | verdict-card | memorability |
| **误区vs事实** | 需要纠正的错误认知 | myth-fact-card | memorability |
| **受众信号** | "适合谁/不适合谁"内容 | audience-fit-card | attention |
| **品牌宣言** | 价值声明、宣告 | manifesto-card | memorability |
| **层级结构** | 嵌套/分类结构 | tree-chart | readability |
| **时间线** | 按时间排列的里程碑 | version-timeline | readability |
| **供需关系** | 缺口/短缺叙事 | bar-chart | readability |
| **案例/证言** | 有结果的真实案例 | cases-card | memorability |
| **定义** | 需要解释的技术术语 | definition-card | readability |
| **行动项** | CTA/关注/订阅引导 | subscribe-card | conversion |
| **品牌信息** | 作者名/刊物/二维码 | back-cover | conversion |
| **章节过渡** | 节与节之间的桥接 | bridge-card / section-divider | readability |
| **系列上下文** | "第N篇，共M篇" | series-card | attention |
| **警示/通知** | 重要警告/政策变更 | notice-card / callout-card | attention |

### 提取规则

- 可视化单元须有 **≥2个数据点** 或 **清晰逻辑结构** 或 **独立金句冲击力**
- 孤立单个数字不可视化（如"48天"单独→不做图；"48天+5000亿+万亿"一起→时间线）
- 无数据/结构/金句的叙述段落不可视化
- 两个单元来源段落重叠时，**合并**

---

## Step B: 配图方案（确认点1 — 必须）

**人设规则**：永远不向用户展示专业术语。所有类型名翻译为 emoji + 一句话描述。密度评分内部计算，不暴露给用户。

### 内部：密度评分（静默）

每张拟生成配图按3维度评分（每维5分，满分15）：

| 维度 | 1分 | 3分 | 5分 |
|------|-----|-----|-----|
| **信息增量** | 纯装饰 | 重组更清晰 | 揭示隐形结构 |
| **数据价值** | 无数据 | 2-3个数据点 | 4+数据点+关系 |
| **独立可读性** | 完全依赖上下文 | 只需标题即可 | 自解释 |

**门控阈值：≥9/15。** 低于9跳过或合并。封面/封底豁免：≥6/15。

### 用户友好输出格式（必须）

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

### Emoji映射表（内部类型 → 用户友好描述）

| 内部类型 | Emoji | 用户描述 | 内部类型 | Emoji | 用户描述 |
|---------|-------|---------|---------|-------|---------|
| cover | 📷 | 封面 | back-cover | 📷 | 封底 |
| quote-card | 💬 | 金句图 | verdict-card | ⚖️ | 最终判断卡 |
| myth-fact-card | 🔍 | 认知纠偏卡 | audience-fit-card | 👥 | 读者匹配卡 |
| manifesto-card | 🏴 | 宣言卡 | bridge-card | 🌉 | 转场卡 |
| callout-card | 📢 | 提示框 | definition-card | 📖 | 术语定义卡 |
| cases-card | 🏆 | 案例卡 | notice-card | 🚨 | 重要通知卡 |
| series-card | 📚 | 系列说明卡 | subscribe-card | 🔔 | 关注引导卡 |
| rule-card | ⚡ | 铁律/规则卡片 | checklist-card | 🛡️ | 检查清单 |
| cheatsheet-card | 🎯 | 速查表 | logic-chain | 💡 | 论证链 |
| process-pipeline | 🔧 | 流程管道 | version-timeline | 📈 | 版本演进线 |
| section-divider | ➖ | 章节分隔图 | bar-chart | 📊 | 数据对比图 |

### Purpose-Based Design Adjustments（内部）

| Purpose | 视觉倾向 | Token覆盖 |
|---------|---------|-----------|
| **attention** | 高对比、大字号、品牌色突出、留白充裕 | `--text-hero` +20%, `--color-accent-1` 饱和度+15%, `--space-12` |
| **readability** | 清晰层级、结构化布局、舒适间距 | 默认token, `--leading-relaxed`, `--space-6` |
| **memorability** | 单一焦点、金句放大、视觉锚点、极简 | `--text-hero` +30%, 减至1个强调色, `--space-16` |
| **conversion** | CTA突出、品牌信息完整、行动引导 | `--color-accent-1` 用于CTA, `--radius-md` 按钮 |

**规则**：Purpose 在同一 design-tokens.css 内调整 token，不为每个 purpose 创建独立 token 文件。

### 用户覆盖选项

- "确认" → 按方案执行
- "去掉第N张" → 移除
- "加上[描述]" → 添加（覆盖门控）
- "第N张换成[描述]" → 更换类型
- "合并第M和第N张" → 合并
- "大师推荐" → 自动决策，跳过此确认点

### Master Mode 快捷方式

用户说了"大师推荐"/"你定"/"直接来"：
- 跳过 Step B 输出
- 自动选择所有通过门控的配图
- 自动合并重叠项
- 直接进入 Step C（或同时跳过 Step C）

---

## Step C: 风格定制（确认点2）

**人设规则**：不让用户选风格/调色板/字体名。用3个简单问题代替。每个选项解释"意味着什么"，而非"是什么"。

### 品类路由表（静默，Q1之前）

| 品类 | 检测信号 | 默认模式 | 默认主题 | 推荐 Recipe 序列 | 文图方案 | 图源优先 | 常见坑 |
|------|---------|---------|---------|-----------------|---------|---------|--------|
| 深度观察/商业洞察 | "IPO"/"估值"/"财报"/"行业" | Swiss | IKB Blue | S01→S06→S04→S10 | text-beside-image | Unsplash>Wallhaven | 不要用暖色照片做背景 |
| 科技/产品 | "AI"/"发布"/"功能"/"测评" | Swiss | IKB Blue / Safety Orange | S01→S03→S09→S05→S10 | text-beside-image | Pexels>Unsplash | 不要用emoji代替图标 |
| 人文/文化 | "历史"/"文学"/"艺术"/"电影" | Editorial | 牛皮纸/森林墨 | E01→E11→E04→E02→E07 | text-beside-image | Unsplash>Pexels | 不要用Swiss做人文 |
| 职场/干货 | "方法"/"步骤"/"清单"/"工具" | Swiss | Lemon Green | S01→S09→S03→S05→S10 | text-only | Pexels | 不要用照片做背景 |
| 旅行/生活 | "旅行"/"城市"/"美食"/"探店" | Editorial | 暖色/earth | E01→E02→E11→E04→E07 | text-on-image | 用户照片>Pexels | 不要用Swiss做旅行 |
| 读书/笔记 | "书评"/"阅读"/"笔记"/"摘录" | Editorial | 墨水经典 | E01→E04→E11→E03→E07 | text-beside-image | Unsplash | 不要用亮色accent |
| 人物/访谈 | "专访"/"对话"/"人物"/"故事" | Editorial | 沙丘/森林墨 | E01→E10→E04→E11→E07 | text-on-image | Unsplash>用户照片 | 不要裁切人脸 |
| 数据/研究 | "研究"/"报告"/"调查"/"统计" | Swiss | IKB Blue | S01→S02→S04→S06→S10 | text-only | N/A | 不要用Editorial做纯数据 |
| 观点/评论 | "我认为"/"其实"/"真相"/"误区" | Editorial | 墨水经典 | E01→E09→E05→E04→E07 | text-beside-image | Unsplash | 不要用Swiss做观点文 |
| 教程/指南 | "教程"/"指南"/"如何"/"入门" | Swiss | Lemon Green | S01→S09→S03→S05→S10 | text-beside-image | Pexels | 步骤不要超过5步 |
| 情感/故事 | "回忆"/"成长"/"告别"/"相遇" | Editorial | 沙丘/莫兰迪 | E01→E02→E04→E09→E07 | text-on-image | 用户照片>Unsplash | 不要用Swiss做情感 |

**规则**：品类检测是静默建议。用户Q1回答与检测矛盾时，用户显式回答优先。

### 3个问题（用户友好）

```
🎨 风格定制（3个问题帮你定调）

问题1：你的文章调性是？
  A. 严肃深度（像经济学人、财新）  → Editorial：衬线体+暖色底+单品牌色
  B. 专业理性（像36氪、极客公园）  → Swiss：无衬线+灰白底+高反差功能色
  C. 温暖人文（像人物、GQ报道）    → Editorial：衬线+无衬线混搭+暖棕底
  D. 活泼有趣（像差评、半佛仙人）  → Swiss：大胆撞色+强调色+粗体

问题2：读者第一眼应该感受到什么？
  A. "这文章有分量"  → 加重衬线体+深色标题+大字封面
  B. "这数据很硬"    → 加粗数字+图表突出+数据标签
  C. "这观点很犀利"  → 金句放大+高对比+红色强调
  D. "这方法很实用"  → 结构清晰+步骤感强+编号突出

问题3：配色偏好？
  A. 跟着文章来源走（微信绿/经济学人红/知乎蓝...）→ 自动检测品牌DNA
  B. 我有指定色系：______
  C. 你来定，高级就行  → 默认克制风（单品牌色+暖灰层级）

---
💡 快捷方式：
- "大师推荐" → 跳过3个问题，我根据文章自动判断
- "和上次一样" → 读取上次风格配置
```

### 答案→风格映射表（内部）

| Q1 | Q2 | Q3 | 模式 | 内部风格 | 内部调色板 | 字体预设 |
|----|----|----|------|---------|-----------|---------|
| A(严肃深度) | any | any | Editorial | kami-editorial | ink-blue / brand-DNA | kami-serif |
| B(专业理性) | any | any | Swiss | swiss-intl | IKB Blue | 现代简约 |
| C(温暖人文) | any | any | Editorial | morandi-journal | warm-earth | editorial-mix |
| D(活泼有趣) | any | any | Swiss | swiss-bold | Lemon Yellow / Safety Orange | 现代简约 |

### 视觉节奏规划

每张配图分配一个 theme class 控制视觉重量：

| Theme Class | 视觉效果 | 使用时机 |
|------------|---------|---------|
| **hero** | 最大视觉冲击、大字号、强对比 | 封面、封底、关键判断 |
| **dark** | 深色背景、浅色文字、呼吸空间 | 论证链、认知纠偏、宣言 |
| **light** | 浅色背景、深色文字、内容密集 | 指标、数据图、清单 |
| **accent** | 强调色高亮、吸引注意 | 金句图、提示框、CTA |

**硬规则**：
- 不超过3张连续配图使用同一 theme class
- 6张以上配图集须有 ≥1 hero + ≥1 dark + ≥1 light
- 每3-4张内容配图，插入1张 hero 或 dark 配图做视觉呼吸
- 封面和封底始终为 hero
- 整体节奏：**hero → content → content → breathing → content → hero**

### 风格一致性规则

1. 所有配图共享同一 design-tokens.css — 同一调色板、同一字体系统
2. 布局按配图类型变化 — 但颜色/字体/间距一致
3. 品牌 DNA 应用于所有配图 — 如选了经济学人红，全部使用
4. 允许单张配图风格覆盖 — 如"第3张用纸墨风"→ 该张独立 token 覆盖

### 跳过条件

- 用户说"直接生成"/"大师推荐" → 跳过 Step C，自动匹配风格
- 用户说"快速搞定" → 同时跳过 Step B 和 Step C（密度门控仍静默执行）

---

## Step D: 批量生成 HTML

**关键变化**：输出纯 HTML，不是 React JSX。每个 HTML 文件独立完整，内联 CSS，截图友好。

### 输出目录结构（扁平）

```
[article-name]-illustrations/
├── 01-cover.html
├── 02-metrics.html
├── 03-logic-chain.html
├── 04-pipeline.html
├── 05-timeline.html
├── 06-myth-fact.html
├── 07-quote.html
├── 08-back-cover.html
└── screenshot.js              ← 一键截图脚本
```

### HTML 生成规则

1. **内联CSS** — 每个 HTML 文件包含完整样式，不依赖外部 CSS 文件
2. **`<img>`标签背景** — 照片背景用 `<img>` + 绝对定位 + `object-fit:cover`，不用 CSS background-image
3. **固定宽高** — `html,body{width:Wpx;height:Hpx;overflow:hidden;margin:0;padding:0}`
4. **overflow:hidden** — 任何溢出内容裁切，确保截图尺寸精确
5. **Google Fonts @import** — 放在 `<style>` 顶部
6. **命名规范** — `{NN}-{type}.html`，NN 为零填充序号

### Hero Page Background Rule（封面/封底背景图规则）

封面和封底是 hero 页面 — 任务是让读者停止滑动。纯色背景做不到。**必须**使用相关照片作为背景。

**强制要求**：
- 封面：使用 Pexels/Unsplash/Wallhaven 照片作为全出血背景
- 封底：使用照片或封面照片的暗化版本作为背景
- 文字放在照片"安静区"（低细节、低对比度区域）
- 应用图文冲突保护规则

**照片搜索关键词**：

| 内容类型 | 搜索关键词 | 来源 |
|---------|-----------|------|
| 科技/产品 | `{topic} technology`, `rocket launch`, `satellite` | Unsplash > Pexels |
| 商业/金融 | `{topic} business`, `stock market`, `city skyline night` | Unsplash |
| 人文/文化 | `{topic} culture`, `library`, `bookshelf` | Unsplash |
| 旅行/生活 | `{topic} travel`, `landscape`, `city` | Pexels > Unsplash |
| 数据/研究 | `abstract dark`, `data visualization`, `blue technology` | Wallhaven > Unsplash |

**文字叠加处理**：
- 浅色照片 → 深色文字 + 微弱 text-shadow
- 深色照片 → 浅色文字(#e8ecf4)，无需阴影
- 混合 → 仅在文字区域添加半透明渐变遮罩（非全画布）
- **绝不**使用全画布深色遮罩破坏照片

**Swiss 例外**：Swiss hero 页面可以使用照片背景。"无装饰"规则仅适用于内容页。只有文字在白底上的封面不是 Swiss 封面 — 是错失机会。

### 封面标题放置模式选择

封面/封底使用照片背景时，根据照片主体位置选择标题放置模式：

| 模式 | 主体位置 | 标题位置 | 适用场景 |
|------|---------|---------|---------|
| **A · 顶压底沉** | 主体在中间，上下留空 | 顶部 kicker + 底部标题 | 默认模式，大多数照片 |
| **B · 侧栏立柱** | 主体占一侧，对侧干净 | 对侧列：kicker→标题→副标题 | 有明确垂直分割的照片 |
| **C · 角落徽章** | 主体充满画面，一角空 | 空角小标题块（≤35%宽×≤25%高） | 只有一个角落可用 |
| **D · 下沉条带** | 宽景，底部大量留白 | 底部条带 78-92% y | 风景/氛围照片 |

**照片门控（选择模式前必须通过）：**
1. 安静区测试：照片必须有 ≥30% 画布面积的低细节区域放标题
2. 光线测试：照片必须是氛围光（阴天/黎明/黄昏/雾气）。拒绝正午高饱和照片
3. 两项都失败 → 改用 E01/S01 分栏布局，不用全出血照片

### WeChat Public Account Size Specs

| 配图类型 | 宽度 | 高度 | 比例 | 用途 |
|---------|------|------|------|------|
| 封面 (cover) | 900px | 383px | 2.35:1 | 文章封面 |
| 正文配图 (body) | 640px | auto | flexible | 文章内嵌 |
| 金句图 (quote) | 640px | 640px | 1:1 | 文章内嵌/朋友圈 |
| 章节分隔 (divider) | 640px | 200px | ~3:1 | 章节间 |
| 封底 (back-cover) | 900px | 383px | 2.35:1 | 文章结尾 |

### HTML模板骨架（截图友好）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@400;700&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }
html, body {
  width: 640px;           /* 按配图类型调整 */
  height: 800px;          /* 按配图类型调整，auto高度用固定值 */
  overflow: hidden;
  font-family: 'Noto Sans SC', sans-serif;
}

/* ——— 设计令牌（内联） ——— */
:root {
  --color-bg: #f8f6f1;
  --color-text: #1a1a2e;
  --color-accent: #c0392b;
  --color-muted: #6b7280;
  --font-display: 'Noto Serif SC', serif;
  --font-body: 'Noto Sans SC', sans-serif;
}

/* ——— 照片背景层（封面/封底必须） ——— */
.bg-photo {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
}

/* ——— 渐变遮罩（仅文字区域） ——— */
.overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.1), rgba(0,0,0,0.5));
  z-index: 1;
}

/* ——— 内容层 ——— */
.content {
  position: relative;
  z-index: 2;
  padding: 48px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>
</head>
<body>
<!-- 照片背景（封面/封底使用，其他类型可删除此img） -->
<img class="bg-photo" src="https://images.unsplash.com/photo-xxx" alt="" />
<div class="overlay"></div>

<!-- 内容 -->
<div class="content">
  <h1 style="font-family:var(--font-display);font-size:32px;color:var(--color-text)">
    标题
  </h1>
  <p style="font-size:18px;color:var(--color-muted);margin-top:16px">
    正文内容
  </p>
</div>
</body>
</html>
```

---

## Step E: 配图使用指南

**人设规则**：不展示技术文件树。告诉用户每张图放在文章哪里，如何快速修改。

### 用户友好输出格式

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
```

### Master Mode 附加询问

```
对结果满意吗？不满意可以告诉我：
- "第N张改一下" → 进入微调模式
- "重新来" → 回到 Step B 重新规划
```

---

### 微调模式（Tweak Mode）

当用户对已生成的配图不满意时，进入微调模式：

**触发词**: "第N张颜色太深" / "第N张加个[元素]" / "第N张换个版式" / "封面字号再大点"

**流程**:
1. 定位目标：确认用户要修改哪张配图（编号或描述）
2. 理解意图：将用户的模糊反馈翻译为具体设计参数调整
3. 只重新生成目标HTML文件（不重新生成全部）
4. 只重新截图目标PNG
5. 替换桌面文件夹中的对应PNG
6. 同步替换飞书云盘中的对应文件

**禁止**: 不修改用户未提及的配图。微调不是全面重做。

---

## Step F: 截图 & 交付

### Puppeteer-core + 系统Chrome

**依赖**：puppeteer-core（不下载 Chromium）

### Chrome路径检测（Windows，按顺序）

1. 注册表：`HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe`
2. Playwright：`$env:LOCALAPPDATA\ms-playwright\chromium-*\chrome-win64\chrome.exe`
3. 默认：`C:\Program Files\Google\Chrome\Application\chrome.exe`

### 截图参数表

| 配图类型 | Viewport | deviceScaleFactor | 输出 |
|---------|----------|-------------------|------|
| 封面 (cover) | 900×383 | 2 | PNG |
| 正文配图 (body) | 640×auto | 2 | PNG |
| 金句图 (quote, 1:1) | 640×640 | 2 | PNG |
| 章节分隔 (divider) | 640×200 | 2 | PNG |
| 封底 (back-cover) | 900×383 | 2 | PNG |

### 完整截图脚本 screenshot.js

```javascript
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

// ===== Chrome 路径检测（Windows） =====
function detectChromePath() {
  const { execSync } = require('child_process');
  // 1. 注册表
  try {
    const reg = execSync(
      'reg query "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\chrome.exe" /ve',
      { encoding: 'utf-8' }
    );
    const m = reg.match(/REG_SZ\s+(.+)/);
    if (m && fs.existsSync(m[1].trim())) return m[1].trim();
  } catch (_) {}
  // 2. Playwright
  const playwrightDir = path.join(
    process.env.LOCALAPPDATA || '', 'ms-playwright'
  );
  if (fs.existsSync(playwrightDir)) {
    const dirs = fs.readdirSync(playwrightDir)
      .filter(d => d.startsWith('chromium-'))
      .sort()
      .reverse();
    for (const d of dirs) {
      const p = path.join(playwrightDir, d, 'chrome-win64', 'chrome.exe');
      if (fs.existsSync(p)) return p;
    }
  }
  // 3. 默认路径
  const defaultPath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  if (fs.existsSync(defaultPath)) return defaultPath;
  throw new Error('未找到 Chrome，请安装 Google Chrome 或设置 CHROME_PATH 环境变量');
}

// ===== 配图类型 → 截图参数映射 =====
const TYPE_CONFIG = {
  cover:        { width: 900, height: 383, fullPage: false },
  'back-cover': { width: 900, height: 383, fullPage: false },
  quote:        { width: 640, height: 640, fullPage: false },
  divider:      { width: 640, height: 200, fullPage: false },
  // 正文配图：高度自动检测
  default:      { width: 640, height: 800, fullPage: true  },
};

function getTypeFromFilename(name) {
  const known = ['cover','back-cover','quote','divider'];
  for (const t of known) {
    if (name.includes(t)) return t;
  }
  return 'default';
}

// ===== 主流程 =====
(async () => {
  const chromePath = detectChromePath();
  console.log('✅ Chrome 路径:', chromePath);

  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: chromePath,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });

  // 输出目录：桌面文件夹（从目录名提取文章名）
  const scriptDir = __dirname;
  const desktop = path.join(require('os').homedir(), 'Desktop');
  // 从目录名提取文章名（如 mythos-illustrations → mythos）
  const articleName = path.basename(scriptDir).replace(/-illustrations$/, '');
  const outputDir = path.join(desktop, articleName + '公众号配图');
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  // 遍历所有 HTML 文件
  const htmlFiles = fs.readdirSync(scriptDir)
    .filter(f => f.endsWith('.html'))
    .sort();

  console.log(`📄 找到 ${htmlFiles.length} 个 HTML 文件`);

  for (const file of htmlFiles) {
    const filePath = path.join(scriptDir, file);
    const type = getTypeFromFilename(file);
    const config = TYPE_CONFIG[type] || TYPE_CONFIG.default;
    const pngName = file.replace('.html', '.png');
    const pngPath = path.join(outputDir, pngName);

    console.log(`  🖼️  ${file} → ${pngName} (${type}, ${config.width}×${config.height})`);

    const page = await browser.newPage();
    await page.setViewport({
      width: config.width,
      height: config.height,
      deviceScaleFactor: 2
    });

    await page.goto('file:///' + filePath.replace(/\\/g, '/'), {
      waitUntil: 'networkidle0',
      timeout: 30000
    });

    // 等待字体加载
    await page.evaluate(() => document.fonts.ready);

    // 等待外部图片加载（5秒缓冲）
    await new Promise(r => setTimeout(r, 5000));

    // 自动检测高度（正文配图）
    const screenshotOpts = {
      path: pngPath,
      type: 'png'
    };
    if (config.fullPage) {
      screenshotOpts.fullPage = true;
    } else {
      screenshotOpts.clip = { x: 0, y: 0, width: config.width, height: config.height };
    }

    await page.screenshot(screenshotOpts);
    await page.close();
  }

  await browser.close();
  console.log(`\n✅ 截图完成！输出目录: ${outputDir}`);

  // 截图完成后打开文件夹
  const { execSync } = require('child_process');
  try { execSync('explorer.exe "' + outputDir + '"'); } catch(e) {}
})();
```

### 背景图兼容性规则

CSS `background-image: url(...)` 在 Puppeteer headless 模式下可能不加载。

**正确模式**：
```html
<div style="position:relative;width:900px;height:383px;overflow:hidden">
  <img src="https://..." style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover" />
  <div style="position:absolute;inset:0;background:linear-gradient(...)"></div>
  <div style="position:relative;z-index:2">Content</div>
</div>
```

**错误模式**（可能不加载）：
```html
<div style="background-image:url('https://...')">Content</div>
```

### 等待策略

- `waitUntil: 'networkidle0'` — 等待所有网络请求完成
- `document.fonts.ready` — 等待 Web 字体加载
- **5秒缓冲** — 等待外部图片（Unsplash/Pexels）完全渲染
- 自动高度页面（640×auto）：使用 `fullPage: true`

### 输出目录结构

```
[article-name]-illustrations/
├── output/                          ← PNG 截图输出
│   ├── 01-cover.png
│   ├── 02-metrics.png
│   ├── 03-logic-chain.png
│   └── ...
├── 01-cover.html                    ← 源 HTML 文件
├── 02-metrics.html
├── ...
└── screenshot.js                    ← 截图脚本
```

### 输出目录

```
~/Desktop/[文章名]公众号配图/       ← PNG 直接存桌面文件夹
├── 01-cover.png
├── 02-metrics.png
├── 03-logic-chain.png
└── ...

[article-name]-illustrations/       ← HTML 源文件（工作目录）
├── 01-cover.html
├── 02-metrics.html
├── ...
└── screenshot.js
```

### 交付流程（3步自动执行）

**Step F.1: 截图**

screenshot.js 输出目录设为桌面文件夹：
```javascript
const desktop = path.join(require('os').homedir(), 'Desktop');
const outputDir = path.join(desktop, '[文章名]公众号配图');
```

截图完成后用 `explorer.exe` 打开文件夹。

**Step F.2: 本地验证**

- 验证每个 PNG 非空白（文件大小 > 10KB）
- 封面/封底有可见照片背景（非空白白底）
- 中文字符正确渲染

**Step F.3: 飞书云盘同步**

用 `lark-cli` 将 PNG 同步到飞书云盘，手机端可直接下载：

```bash
# 1. 创建云盘文件夹
lark-cli drive +create-folder --name "[文章名]公众号配图"

# 2. 切换到桌面文件夹目录
cd "$env:USERPROFILE\Desktop\[文章名]公众号配图"

# 3. 逐张上传
lark-cli drive +upload --file "./01-cover.png" --folder-token <folder_token>
lark-cli drive +upload --file "./02-metrics.png" --folder-token <folder_token>
# ... 逐张上传

# 4. 返回云盘链接给用户
```

**注意**：
- `lark-cli drive +upload` 要求 `--file` 使用相对路径（必须在目标目录下执行）
- 如果 `lark-cli` 不可用或缺少 scope，跳过云盘同步，仅保存本地

### 质量检查清单

- [ ] 所有 PNG 文件存在且大小 > 10KB
- [ ] 封面/封底有可见照片背景（非空白白底）
- [ ] 文字在50%缩放下可读（模拟手机预览）
- [ ] 无破损图片（Unsplash/Pexels 正确加载）
- [ ] 中文字符正确渲染（字体已加载）
- [ ] 飞书云盘文件夹已创建且图片已上传（如可用）

---

## WeChat Density Check（公众号密度铁律）

### 640px 正文配图

- [ ] 活跃构图 ≥70% 画布高度（非大面积空白）
- [ ] 每张至少3个内容元素（标题+正文+数据/图片/金句）
- [ ] 无纯空白竖条 >30% 画布高度（无设计理由时）
- [ ] 文字在50%缩放下可读（模拟手机浏览）

### 900×383 封面

- [ ] 封面1秒内传达主题（照片+标题+副标题）
- [ ] 文字不与照片主体/人脸重叠
- [ ] 标题在360px宽时可读（缩略图测试）

### 640×640 金句图

- [ ] 金句是唯一焦点
- [ ] 署名清晰在金句下方
- [ ] 中文文字不超过50字（否则拆分）

### 内容密度硬规则（Canvas Coverage Rule）

640px 画布上：
- 内容必须覆盖 **≥70% 画布高度**
- 纯空白竖条 >20% 画布高度（>128px）需声明理由
- 禁止用 `flex:1` 把内容推到垂直居中 — 公众号配图是单张滑动的，不是对页杂志
- 每个 recipe 有 Minimum density 行，内容不够 → 换 recipe 或缩短画布

900×383 封面：
- 照片+标题+副标题必须覆盖 ≥60% 画布
- 标题在 360px 宽缩略图中必须可读

640×640 金句图：
- 金句+署名+至少1个锚点（kicker/meta/hairline rule）必须存在
- 纯金句无锚点 = 空洞，不是克制

---

## Anti-Patterns（Multi-Illustration 专用）

| 反模式 | 检测方式 | 修复 |
|-------|---------|------|
| **强制数量** | "生成10张配图"无视内容 | 移除固定数量，由内容分析决定 |
| **填充配图** | 密度评分 <9 | 跳过或合并；仅用户显式覆盖时生成 |
| **风格漂移** | 不同配图使用不同调色板/字体 | 强制共享 design-tokens |
| **信息重复** | 两张配图展示相同数据 | 合并为一张，或按角度拆分 |
| **依赖上下文的金句** | 金句脱离文章无意义 | 跳过；只用独立有冲击力的金句 |
| **过度配图** | 配图数超过段落数 | 最大比例：1张配图/2个实质段落 |
| **配图不足** | 文章5+数据点但无数据图 | Step B 标记为"遗漏机会" |
| **类型滥用** | 同一类型出现 >1 次 | 强制唯一性约束（见下表） |
| **版式单调** | 连续3+张同版式类型 | 强制版式多样性（见下表） |

### Layout Diversity Rule（版式多样性规则）

每张配图使用 recipe ID 标注版式。**禁止连续3张使用同一 recipe。**

Editorial recipes: E01-E14
Swiss recipes: S01-S10

**Step D 生成时必须检查**：遍历所有配图的 recipe ID，如果连续3张相同，自动将第3张改为同模式下的不同 recipe。

**跨模式规则**：一套配图内不应混用 Editorial 和 Swiss recipes（封面/封底除外）。

### Uniqueness Constraint（类型数量上限）

| 类型 | 上限 | 理由 |
|------|------|------|
| cover | 1 | 一篇文章一个开头 |
| back-cover | 1 | 一篇文章一个结尾 |
| verdict-card | 1 | 一篇文章一个核心判断 |
| manifesto-card | 1 | 一篇文章一个宣言 |
| quote-card | 2 | 开头+结尾，不再多 |
| bridge-card | N-1 | N = 章节数 |
| section-divider | N-1 | 同 bridge |
| callout-card | 3 | 太多提示=噪音 |
| 其他所有类型 | 2 | 需要更多时考虑合并 |

**例外**：用户显式覆盖"我就是要2张封面" — 尊重用户意图。

---

## Illustration Type Templates（20种配图类型模板）

### Cover（封面）
<!-- Layout: hero-center | Content: thesis + author + source + date | Size: 900×383 | Density: low | Purpose: attention | Required: { thesis, author, source, date, accentText } | Gate: ≥6/15 | When: 每篇文章必须有 -->

### Back Cover（封底）
<!-- Layout: center-stack | Content: publicationName + author + QR placeholder + CTA | Size: 900×383 | Density: low | Purpose: conversion | Required: { publicationName, author, qrPlaceholder, cta } | Gate: ≥6/15 | When: 文章结尾品牌展示 -->

### Quote Card（金句图）
<!-- Layout: single-focus | Content: one powerful quote + attribution + contextHint | Size: 640×640 | Density: medium | Purpose: memorability | Required: { quote, attribution, contextHint } | Gate: 金句必须脱离全文仍有冲击力 | When: 脱离上下文仍有力量的陈述 -->

### Rule Card（铁律/规则卡片）
<!-- Layout: grid-cards (compact) | Content: numbered rules + consequence per rule | Size: 640px wide | Density: high | Purpose: readability | Required: { title, rules: [{ number, rule, consequence? }] } | Gate: ≥2条规则，内容可操作 | When: "三条铁律"/"5条原则"/"7条红线" -->

### Checklist Card（检查清单）
<!-- Layout: vertical-list with status markers | Content: numbered items + description + severity marker (✅/⚠️/RED FLAG) | Size: 640px wide | Density: high | Purpose: readability | Required: { title, items: [{ number, description, severity? }] } | Gate: ≥3项，描述不重叠 | When: "安全红线"/"检查清单"/"避坑指南" -->

### Cheatsheet Card（速查表）
<!-- Layout: dense-grid (2-3 columns) | Content: entries + name + one-line example | Size: 640px wide | Density: very high | Purpose: readability | Required: { title, entries: [{ id, name, example }] } | Gate: ≥4条 name+example 对 | When: "速查表"/"cheatsheet"/"B1-B6规则" -->

### Section Divider（章节分隔图）
<!-- Layout: hero-center | Content: sectionNumber + sectionTitle + subtle decoration | Size: 640×200 | Density: minimal | Purpose: readability | Required: { sectionNumber, sectionTitle } | Gate: 仅4+明确分节文章 | When: 章节间视觉分隔 -->

### Logic Chain（论证链）
<!-- Layout: flow-chart (horizontal) | Content: causal chain 3-6 nodes, each = one claim | Size: 640px wide | Density: high | Purpose: readability | Required: { nodes: [{ claim, evidence? }], connections: [{ from, to, label? }] } | Gate: ≥3节点，有明确因果关系 | When: "A导致B导致C"型推理 -->

### Process Pipeline（流程管道）
<!-- Layout: flow-chart (vertical/horizontal with I/O) | Content: sequential phases, each with input→process→output | Size: 640px wide | Density: high | Purpose: readability | Required: { phases: [{ name, input, output, steps? }] } | Gate: ≥2阶段，有明确输入输出边界 | When: "Phase 0→Phase 1→Phase 2"型管道 -->

### Version Timeline（版本演进线）
<!-- Layout: timeline | Content: version/iteration history, each node = what changed | Size: 640px wide | Density: medium | Purpose: readability | Required: { versions: [{ label, changes: string[], keyMetric? }] } | Gate: ≥3版本，有实质差异 | When: "v1→v2→v3"或"2023→2024→2025" -->

### Verdict Card（最终判断卡）
<!-- Layout: single-focus | Content: core judgment + reasoning + applicability note | Size: 640px wide | Density: medium | Purpose: memorability | Required: { eyebrow, title, body, note? } | Gate: 必须有明确可争议的判断 | When: "最终判断"/"核心结论"/"我的判断" -->

### Audience Fit Card（读者匹配卡）
<!-- Layout: split-comparison (fit vs not-fit) | Content: who should read + who should NOT | Size: 640px wide | Density: medium | Purpose: attention | Required: { title, fit: string[], notFit: string[] } | Gate: ≥1 fit AND ≥1 not-fit | When: "适合谁"/"不适合谁"/"写给谁看" -->

### Myth-Fact Card（认知纠偏卡）
<!-- Layout: binary-comparison (myth vs fact pairs) | Content: misconception + correction pairs | Size: 640px wide | Density: high | Purpose: memorability | Required: { title, pairs: [{ myth, fact }] } | Gate: ≥2 myth-fact 对 | When: "误区"/"真相"/"你可能以为…其实" -->

### Manifesto Card（宣言卡）
<!-- Layout: hero-center with emphasis | Content: brand declaration / value statement | Size: 640px wide | Density: low | Purpose: memorability | Required: { eyebrow, title } | Gate: 标题必须是完整断言，非话题标签 | When: "我们相信"/"我的立场"/"宣言" -->

### Bridge Card（转场卡）
<!-- Layout: hero-center (lightweight) | Content: "from → to" transition | Size: 640×200 | Density: minimal | Purpose: readability | Required: { from, to } | Gate: 仅4+章节文章 | When: 章节过渡，"看完了X，接下来看Y" -->

### Callout Card（提示框）
<!-- Layout: inline-block with type-based styling | Content: tip/warning/info/success/danger message | Size: 640px wide | Density: low | Purpose: attention | Required: { type: 'info'|'tip'|'warning'|'success'|'danger', text } | Gate: 文字必须可操作 | When: "注意"/"小技巧"/"警告"/"重要" | Visual: info=蓝, tip=绿, warning=琥珀, success=绿, danger=红 -->

### Definition Card（术语定义卡）
<!-- Layout: inline-block with term highlight | Content: term + definition + optional label | Size: 640px wide (compact) | Density: medium | Purpose: readability | Required: { term, definition, label? } | Gate: 术语对目标受众不显而易见 | When: "OKR"/"RAG"/"微服务"型术语 -->

### Cases Card（案例卡）
<!-- Layout: grid-cards (2-4 columns) | Content: case name + industry + outcome | Size: 640px wide | Density: high | Purpose: memorability | Required: { title, cases: [{ name, industry, outcome }] } | Gate: ≥2案例，有可量化结果 | When: "使用案例"/"客户背书"/"实战效果" -->

### Notice Card（重要通知卡）
<!-- Layout: single-focus with alert styling | Content: urgent title + body explanation | Size: 640px wide | Density: low | Purpose: attention | Required: { title, body } | Gate: 必须真正时间敏感或政策关键 | When: "重要提醒"/"政策变更"/"限时活动" -->

### Series Card（系列说明卡）
<!-- Layout: hero-center (lightweight) | Content: series name + episode position + topic | Size: 640px wide | Density: low | Purpose: attention | Required: { name, episode, topic } | Gate: 仅系列文章 | When: "第N篇，共M篇"/"XX系列" -->

### Subscribe Card（关注引导卡）
<!-- Layout: center-stack with CTA | Content: publicationName + valueProposition + QR placeholder | Size: 640px wide | Density: low | Purpose: conversion | Required: { title, body, qrPlaceholder? } | Gate: 仅文章结尾，配合封底 | When: "关注"/"订阅"/"扫码" -->
