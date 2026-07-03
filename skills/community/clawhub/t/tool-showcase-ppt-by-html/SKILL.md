---
name: Tool Showcase PPT by HTML
display_name: 项目介绍 PPT 
display_name_en: Tool Showcase PPT by HTML
description: 生成工具/应用介绍的网页 PPT，单文件 HTML，横向翻页。专为产品展示和工具推广设计，采用科技产品展示风视觉基调，含 24 种布局、17 种动态背景、9 套主题色，支持截图占位自动降级。
description_en: Generate tool/app showcase web PPT, single-file HTML with horizontal flip pages. Designed for product showcase and tool promotion, with tech product showcase visual style. 24 layouts, 17 dynamic backgrounds, 9 themes, auto icon-fallback for missing screenshots.
author: 森林（你好森林）· suenty@foxmail.com
version: 1.2.0
category: productivity
icon: ./icon.png
tags:
  - ppt
  - presentation
  - product-showcase
  - tool-intro
  - html
  - single-file
  - 工具介绍
  - 产品展示
  - 演示文稿
disable: false
---

# Tool Showcase Deck

> 一份**单文件 HTML**的横向翻页工具介绍 PPT，专为开发者工具/应用产品设计。

## 这个 Skill 做什么

生成一份展示工具/应用的网页 PPT,采用**科技产品展示风**视觉基调:

- **截图第一公民** — 工具介绍的核心是展示产品界面,不是堆文字
- **简洁现代** — Product Hunt / GitHub README 式的视觉语言
- **双模切换** — Light(白底,公众号嵌入友好) + Dark(深底,独立演示)
- **SVG 装饰背景** — 可选几何点阵/电路线/流动色块,不依赖图片
- **动态背景** — 页面加载后自动运行动画,无需 JS
- **动态 CSS** — 淡入/侧滑/弹入动效 + hover 微交互 + 按钮光泽扫过
- **无 WebGL** — 纯 CSS 渐变 + SVG 背景,加载快、兼容好

美学锚点:像 Apple 产品页贴上了 GitHub README。

## 何时使用

**合适的场景**:
- 公众号工具推荐文章配图/嵌入页
- 开源项目的 GitHub Pages 展示
- 新产品发布/demo day 演示
- 内部分享工具介绍 slides
- 工具测评/对比页面

**不合适的场景**:
- 人文/艺术/行业观察类内容(用 guizang-ppt-skill)
- 大段表格数据(用常规 PPT)
- 培训课件(信息密度不够)

## 工作流

### Step 1 · 自主分析（不提问）

AI 根据用户提供的工具信息**自动完成所有决策**。只在信息严重不足时（如仅给工具名且无上下文）才用 1-2 个问题确认关键信息（如有无截图/性能数据），不问冗余问题。

#### 自动决策链路

| 维度 | AI 判断方式 | 输出 |
|------|-----------|------|
| 主题色 | 解析工具名/描述关键词，按类型映射 | 直接选定 1 套 |
| 页面结构 | 分析可用素材（截图/数据/竞品） | 自动编排布局序列 |
| 背景装饰 | 主题色 + 页面类型 | 自动搭配 class |
| 语言风格 | 推断受众（开发者/普通用户/公众号读者） | 调整措辞 |
| CTA 链接 | 从上下文提取下载/GitHub 地址 | 填入按钮 |

#### 主题色推荐

| 工具类型 | 推荐主题 |
|---------|---------|
| 截图/录屏/标注工具 | 🔵 科技蓝 |
| CLI/终端/开发工具 | 🟣 极客紫 |
| 笔记/文件/效率工具 | 🟢 效率绿 |
| 安全/审计/监控工具 | ⚫ 暗夜黑 |
| 创意/设计/图像工具 | 🔥 日落橙 |
| 协作/云服务/API 工具 | 🌊 海洋青 |
| 生活/轻量应用 | 🌸 玫粉 |
| 企业/旗舰产品 | 🪐 午夜金 |
| 教育/知识管理 | 🌿 森琥珀 |
| 不确定 | 🔵 科技蓝(默认) |

#### 页面自动编排

AI 无需逐页让用户选布局，按以下规则自动生成页面序列。

**页数范围（按工具复杂度自适应）**：

| 工具类型 | 推荐页数 | 判断依据 |
|----------|----------|----------|
| 轻量 CLI / 脚本 | 4-6 页 | 功能少，无截图 |
| 中型 GUI 应用 | 6-9 页 | 有截图，有功能点 |
| 复杂平台 / 多模块 | 9-13 页 | 多截图，有数据/对比 |

最终页数在范围内即为合理，无需追求固定数字。

---

**必选页面（每种工具都必须有）**：

| 布局 | 说明 | 位置 |
|------|------|------|
| T01 Hero 封面 | 工具名 + 定位 + CTA | 第 1 页 |
| T02 功能卡片 | 3-6 个核心功能 | 第 2 页 |
| T09 CTA 收尾 | 下载引导 | 最后一页 |

---

**可选页面（有素材才加，无则跳过）**：

| 条件 | 插入布局 | 插入位置 |
|------|----------|----------|
| 有截图 ≥1 张 | T03 大图展示 | T02 后 |
| 有截图 ≥3 张 | T10 功能详情 | T03 后，每 2-3 张插 1 页 |
| 有使用步骤 | T04 操作流程 | T02 后，T03 前 |
| 有性能/体积数据 | T05 数据大字报 | T02 后 |
| 有 Before/After 场景 | T06 前后对比 | T04/T05 后 |
| 有系统要求/格式说明 | T07 技术规格 | T06 后 |
| 有适用场景 | T08 场景卡片 | T07 后 |
| 有常见问题 | T11 FAQ | T08 后，T09 前 |
| 有竞品对比 | T16 对比矩阵 | T07 后 |
| 有安装步骤 | T15 安装指南 | T07 后 |
| 有版本历史 | T13 版本时间线 | T11 后 |
| 有用户评价 | T14 用户口碑 | T08 后 |

---

**编排逻辑（AI 自主执行）**：

1. 从 3 个必选页面开始
2. 按上表条件依次判断，满足则插入对应可选页面
3. 插入后若超出推荐页数上限，按优先级删减可选页（低优先级：T13、T14、T11）
4. 最终页数落入推荐范围即为合理

---

**主题节奏自动遵循**：Hero 每 3-4 页穿插；Light/Dark 交替，连续 ≤3 页同色；≥9 页时必有 ≥1 hero dark + ≥1 hero light。

#### 背景自动搭配（场景驱动）

AI 根据以下四个维度**自主选择**每页背景，不逐页问用户：

| 决策维度 | 判断方式 |
|---------|---------|
| **页面目标** | 该页的核心目的：视觉冲击 / 信息展示 / 数据强调 / 对比矩阵 / 流程引导 / 人文社交 |
| **情绪基调** | 科技炫酷 → 电路/粒子/条纹/流星；专业稳重 → 几何/六边/圆点/网格；温暖人文 → 色块/波浪/光晕；简洁留白 → 无背景 |
| **明暗模式** | light 页偏纹理/几何/留白，dark 页偏动效/光点/炫酷 |
| **主题联动** | 选定主题色决定偏好方向（见下表） |

---

**背景选池（按目标场景归类，AI 从中自主选取）**：

| 页面目标 | 可用背景池 | 明暗建议 |
|---------|-----------|---------|
| 🔥 视觉冲击 | blobs, bg-glow, bg-meteor, bg-stars, bg-hex, bg-diagonal, bg-stripeflow | dark 为主 |
| 📋 信息展示 | bg-geo, bg-dots, bg-grid, bg-noise, bg-ripple | light + dark 均可 |
| 📊 数据强调 | bg-particles, bg-stripes, bg-grid, bg-circuit, bg-waveline | dark 为主 |
| ⚖️ 对比矩阵 | bg-circuit, bg-grid, bg-stripes | light + dark 均可 |
| 🧭 流程引导 | bg-geo, bg-wave, 留白 | light 为主 |
| 🤝 人文社交 | bg-wave, bg-geo, blobs | light 为主 |

**选择约束**（AI 必须遵守）：

1. **种类收敛**：同一 deck 内背景种类控制在 4-6 种（blobs 不计入种类数）
2. **Hero 冲击**：T01/T30 等 Hero 页优先用 blobs 或 bg-meteor
3. **相邻不重复**：连续两页不用相同背景 class
4. **暗页动效**：dark 页优先有动效的背景（particles/circuit/stripes/dots/meteor/stars）
5. **亮页纹理**：light 页优先几何/纹理（geo/grid/noise/wave）或直接留白
6. **全亮 deck**：公众号嵌入等全 light 场景，主要在 geo/dots/grid/wave/ripple 之间轮换，不超过 4 种
7. **流星特殊**：bg-meteor 需在 `<section>` 内添加 5 个 `<div class="meteor-trail"></div>`，每 deck 最多用 1 次

**主题联动增强**（选定主题后自动倾向）：

| 主题 | 暗色页偏好 | 亮色页偏好 |
|------|----------|----------|
| 🔵 科技蓝 | circuit, particles, waveline | geo, grid |
| 🟣 极客紫 | meteor, stars, circuit, diagonal | geo, dots |
| ⚫ 暗夜黑 | stripes, noise, particles, stripeflow | geo, noise |
| 🔥 日落橙 | dots, ripple | wave, blobs |
| 🪐 午夜金 | hex, ripple, stars | geo, dots |
| 🟢 效率绿 | dots, ripple | geo, 留白 |
| 🌸 玫瑰粉 | dots, ripple | wave, blobs |
| 🌊 海洋青 | dots, grid, ripple | geo, noise |
| 🌿 森琥珀 | dots, noise | geo, noise |

---

**AI 自主选择流程**（每页执行一次）：

```
1. 确定页面目标 → 圈定选池（上表第1列）
2. 检查明暗模式 → 过滤明暗不适配的背景
3. 参考主题偏好 → 优先选偏好表里的背景
4. 避开上页已用 → 相邻不重复
5. 检查种类计数 → 若已达 6 种上限，从已用种类中选
6. 输出 class → 直接写入 <section class="...">
```

### Step 2 · 拷贝模板

```bash
mkdir -p "项目/XXX/ppt/images"
cp "<SKILL_ROOT>/assets/template.html" "项目/XXX/ppt/{工具名英文或拼音}.html"
```

> **HTML 文件命名规则（重要）**：
> - ❌ 不要叫 `index.html`（与网站首页混淆，且不便区分多份 PPT）
> - ✅ 用工具的中文名/英文名/拼音/缩写，例如 `screenshot-tool.html` / `flowmind.html` / `devops-cli.html`
> - 多份 PPT 共用目录时，命名能直接区分（如 `screenshot-tool.html` 和 `markdown-flow.html` 放一起不混淆）
> - 全部小写、连字符分隔，避免空格和中文（部分服务器/浏览器对中文文件名支持差）

`template.html` 是**完整可运行**的文件,CSS、翻页 JS、Lucide 图标 CDN 全已预设,只有 `<!-- SLIDES_HERE -->` 占位符等待填充。

#### 必改占位符

拷贝后立刻改:

| 位置 | 原始 | 需改为 |
|------|------|--------|
| `<title>` | `[必填] 工具名 · 产品介绍` | 实际工具名 |

`grep "必填" {工具名}.html` 确认全部替换完。

#### 截图替换工作流（给非 HTML 用户）

> 即使不懂 HTML,使用者只需把图片放进 `images/` 文件夹,无需碰代码。

**目录结构**:
```
ppt/
├── {工具名}.html  ← AI 生成好的 PPT
└── images/       ← 把图片按占位提示命名后放这里
    ├── p1.png
    ├── p2-1.jpg
    ├── p2-2.jpg
    └── p4.png
```

**占位框生成规则**:AI 在含图片的布局(T04 操作流程 / T10 功能详情 / T16 对比矩阵 / T17 数据仪表盘 等)中,直接生成**带 onerror 回退的 `<img>` 标签**——一行搞定,无需后处理:

```html
<img src="images/p2-1.jpg" alt="步骤截图" onerror="this.outerHTML='<div class=&quot;img-slot&quot;>IMG · p2-1.jpg</div>'">
```

**两种状态无缝切换**:
- **有图**:`<img>` 正常加载,显示真实截图
- **没图**:`<img>` 404 触发 onerror,JS 原地把 img 节点替换为带文件名提示的占位 div,使用者立刻知道该放什么文件

**使用流程**:
1. AI 生成 PPT 时,使用者提供截图(如拖给 AI),AI 为每张图分配一个**简单文件名**(如 `p2-1.jpg`),写入 `<img src="images/xxx.jpg">`
2. AI 同步把图片文件写到 `images/` 目录(如运行环境能拿到文件)
3. **使用者打开 {工具名}.html**:有图看图,没图看占位提示
4. **二次修改**:使用者按提示文件名,把自己准备的图片放进 `images/`,刷新页面即可

**命名规则**:
- `p1` / `p2` / `p3` = 第几页(`p` = page,数字=页码)
- `p2-1` / `p2-2` = 第 2 页有 2 张图
- 后缀 `.jpg` 或 `.png` 皆可

**降级兜底**:
- 没图时,占位框显示文件名提示文字,PPT 仍可正常翻页演示
- 灰底虚线框 + 提示文字,设计上已经预留视觉占位

> 📌 **AI 生成规范（图片布局）**:遇到以下布局,**直接使用上面 onerror 回退的 `<img>` 写法**,不要再生成纯 `<div class="img-slot">` 占位。
>
> | 触发布局 | 类名容器 | 典型场景 |
> |---------|---------|---------|
> | T03 大图展示 | `.screenshot-wrap` | 单张大截图 |
> | T04 操作流程 | `.step-item .step-img` | 步骤配图 |
> | T08 场景卡片 | `.case-card .case-img` | 案例配图 |
> | T10 功能详情 | `.img-frame` | 多张功能截图 |
> | T16 对比矩阵 | `.compare-col .compare-img` | 前后对比 |
> | T20 能力雷达 | `.img-frame` | 能力图示 |
> | T25 设备展示 | `.img-frame` | 设备/界面图 |
>
> 预创建目录:`Step 2` 的 `mkdir -p` 已自动建好 `images/` 子文件夹,使用者只需把图片按 `p{页码}-{序号}.jpg/png` 命名丢进去。

#### 选定主题色（AI 自主选用，用户指定时优先用户）

主题色来源**按优先级**：

1. **用户明确指定**（最高优先级）
   - 用户说"用紫色"/"用蓝调"/"和我品牌色差不多" → **AI 选用同色调协调的色系**（不照搬字面，避免奇怪搭配）
   - 关键不是"严格匹配颜色名"，而是"色调相符 + 整体协调"
   - 用户给出具体 hex（如 `#ff5722`）：以 hex 的色调为主，**AI 自动调整**其他 9 个变量（bg/text/card/muted）保持配色协调，**告知用户最终色值**
   - **不需要严格映射**（不必"紫色 = 极客紫"），AI 根据色调灵活搭配，只要看起来舒服即可

2. **AI 关键词映射**（默认行为，用户没指定时）
   - 解析工具名/描述关键词 → 查下表 → 直接选用 1 套

3. **拿不准** → 🔵 科技蓝兜底

**核心原则**：
- 色调相符 > 字面匹配（用户说紫色，AI 用紫色系即可，不必强行套预设）
- 配色协调 > 严格对应（可以微调饱和度/明度让整体好看）
- 拒绝刺眼荧光色（#00ff00、纯荧光等）

从 `references/themes.md` 找到对应 CSS 变量（或基于色调自由搭配），整体替换 `:root` 开头标有"主题色"注释的 10 行 CSS 变量。

**硬规则**：
- 一份 deck 只用一套主题，不混搭
- 用户没指定时，AI 自主决策；不展示 9 套预设让用户挑
- 用户指定颜色后，**告知用户最终所用色值**

#### 背景装饰（自动应用）

每页背景 class 已由 Step 1「场景驱动」规则决定，无需手动选。以下为全部 17 种背景 class 速查（含流星 + 噪波线特殊用法）：

| Class | 效果 | 周期 | 最佳明暗 | 适合场景 |
|-------|------|------|---------|---------|
| `bg-geo` | 几何点阵漂移 | 40s | light | 纹理填充、信息展示 |
| `bg-dots` | 圆点脉冲呼吸 | 4s | dark | 科技感、暗色页通用 |
| `bg-circuit` | 电路线流动 | 6s | dark | 开发者/安全工具 |
| `bg-particles` | 浮动粒子漂移 | 15s | dark | 数据仪表盘、科技感 |
| `bg-wave` | 底部正弦波纹 | 8s | light | 创意/设计类工具 |
| `bg-hex` | 六边形网格旋转 | 30s | dark | 企业/专业类工具 |
| `bg-stripes` | 斜条纹流动 | 20s | dark | 安全/审计类 |
| `bg-glow` | 脉冲径向光斑 | 6s | dark | Hero 页增强(可叠加) |
| `bg-noise` | 噪点纹理微动 | 0.5s | dark/light | 质感、沉稳风格 |
| `bg-stars` | 星空粒子明暗呼吸 | 3s | dark | Hero/视频/章节过渡 |
| `bg-meteor` | 流星划过（需 div） | 2.5s | dark | 炫酷 Hero、极客主题 |
| `bg-grid` | 网格线匀速平移 | 12s | dark/light | 数据页、对比页 |
| `bg-ripple` | 同心圆波纹扩散 | 3.6s | dark/light | 优雅专业感、圆润主题 |
| `bg-diagonal` | 双层对角线滑动 | 4/5s | dark | 炫酷视觉冲击、Hero 增强 |
| `bg-waveline` | SimplexNoise 波纹线 | 实时 | dark | 技术主题、数据流动感 |
| `bg-stripeflow` | 理发店条纹水平滚动 | 3s | dark | 炫酷主题、视觉冲击 |

**流星特殊用法** — bg-meteor 需在 `<section>` 内手动添加 5 个流星轨迹 div：
```html
<section class="slide dark bg-meteor">
  <div class="meteor-trail"></div>
  <div class="meteor-trail"></div>
  <div class="meteor-trail"></div>
  <div class="meteor-trail"></div>
  <div class="meteor-trail"></div>
  <!-- 页面其他内容 -->
</section>
```

**噪波线特殊用法** — bg-waveline 使用 Canvas 渲染，**无需手动添加任何 HTML**。翻页到该页时自动启动画布，离开时自动停止。每 deck 最多用 1 次（Canvas 开销较大）。

**对角线特殊用法** — bg-diagonal 使用 `::before` + `::after` 双伪元素叠加，无需手动添加子元素。

**流动色块** — 在 `hero light` / `hero dark` 页的 `<section>` 内添加:
```html
<div class="blob a"></div>
<div class="blob b"></div>
```
给 hero 页增加柔和的流动氛围色块。增强版 (opacity .25, blur 60px, scale 动画)。

**背景搭配** — 由 Step 1「背景自动搭配」规则决定，此处为完整 class 参考。无背景类的页面自动获得微动渐变呼吸效果（gradient-shift，12s 周期）。

### Step 3 · 填充内容

#### 预检:类名必须在模板 `<style>` 里有定义

先 `Read assets/template.html` 的 `<style>` 块,确认要用的类都存在。

常见类名(24 种布局所有组件): `feat-card` / `feat-card.accent` / `step-item` / `compare-col` / `compare-divider` / `spec-table` / `uc-card` / `cta-btn` / `stat-card` / `screenshot-wrap` / `faq-item` / `pricing-card` / `timeline` / `tl-item` / `tst-card` / `install-step` / `matrix-table` / `progress-bar` / `progress-fill` / `tag-bar` / `tag-item` / `icon-row` / `icon-cell` / `quote-block` / `alert-box` / `avatar-stack` / `img-frame` / `img-slot` / `badge` / `divider` / `blob`

#### 布局参考（已自动选定）

页面序列由 Step 1「页面自动编排」规则决定。以下为 24 种布局速查，具体骨架代码见 `references/layouts.md`：

| # | 布局 | 用途 | 推荐主题 |
|---|------|------|---------|
| T01 | Hero 封面 | 工具名 + 定位 + CTA | `hero dark` |
| T02 | 功能卡片 | 3-6 个核心功能 | `light` + `bg-geo` |
| T03 | 大图截图 | 完整界面截图 | `dark` + `bg-dots` |
| T04 | 操作流程 | 3-5 步步骤 | `light` |
| T05 | 数据大字报 | 性能/体积/速度 | `hero light` + blobs |
| T06 | 使用前后对比 | Before/After | `dark` + `bg-circuit` |
| T07 | 技术规格表 | 系统要求/格式 | `light` |
| T08 | 场景卡片 | 适用场景/人群 | `dark` |
| T09 | 下载引导 CTA | 下载链接/GitHub | `hero light` + blobs |
| T10 | 功能详情 | 单功能 + 截图 | `light`/`dark` 交替 |
| T11 | FAQ 问答 | 常见问题解答 | `light` |
| T12 | 价格方案 | 版本/套餐对比 | `dark` |
| T13 | 版本时间线 | 发展历程/更新日志 | `light` |
| T14 | 用户口碑 | 推荐语/评价 | `hero light` |
| T15 | 安装指南 | 安装步骤 + 代码块 | `dark` |
| T16 | 功能对比矩阵 | 与同类工具横向对比 | `light` |
| T17 | 数据仪表盘 | 指标 + 进度条 | `dark` + `bg-particles` |
| T18 | 功能筛选 | 标签栏 + 卡片 | `light` |
| T19 | 大引用页 | 核心推荐语 | `hero light` + blobs |
| T20 | 能力雷达 | 多维度进度条 | `dark` + `bg-stripes` |
| T21 | 架构总览 | 模块 + 数据流 | `light` + `bg-geo` |
| T22 | 生态集成 | 第三方服务图标 | `dark` + `bg-hex` |
| T23 | 动图展示 | 操作演示 GIF | `light` |
| T24 | 多入口 CTA | 下载/GitHub/文档/社区 | `hero dark` + `bg-glow` |
| T25 | 代码展示 | 核心代码片段 | `dark` |
| T26 | 数据卡片墙 | 多指标数据一览 | `light`/`dark` |
| T27 | 用户案例 | 真实使用场景 | `light` |
| T28 | 左右分屏 | 两种模式/方案对比 | `dark` |
| T29 | 更新动态流 | 版本更新时间线 | `light` |
| T30 | 章节过渡 | 大章节分隔页 | `hero dark/light` |
| T31 | 团队成员 | 贡献者/团队介绍 | `light` |
| T32 | 视频嵌入 | 操作演示视频 | `dark`/`light` |
| T33 | 二维码引导 | 微信社群/公众号 | `hero light` + blobs |

#### 主题节奏（见 Step 1）

#### 动效

三种入场动效可选:

| 属性 | 效果 | 用法 |
|------|------|------|
| `data-anim="d1"~"d6"` | 淡入+上移 | 通用,适合正文元素 |
| `data-anim-x="d1"~"d3"` | 左侧滑入 | 适合列表项、对比栏 |
| `data-anim-pop="d1"~"d3"` | 缩放弹入 | 适合数据大字、CTA按钮 |

chrome-min 和 footer-min 不加动效标记,始终可见。

**动态交互**(自动生效):
- 功能卡片 hover 浮起+发光边框
- CTA 按钮光泽扫过动画
- 截图框 hover 微放大
- 数据卡 accent 脉冲光环

### Step 4 · 对照检查清单

打开 `references/checklist.md`,逐项对照 P0/P1/P2 级别的问题。

### Step 5 · 本地预览

直接在浏览器打开 `{工具名}.html`:

```bash
# Windows
start "项目/XXX/ppt/{工具名}.html"
```

不需要本地服务器。图片走相对路径 `images/xxx.png`。

## 资源文件导览

```
tool-showcase-ppt/
├── SKILL.md              ← 你正在读
├── assets/
│   └── template.html     ← 种子模板(完整可运行,含 10 种动态背景 + 30+ 组件样式)
└── references/
    ├── themes.md         ← 9 套主题色预设
    ├── layouts.md        ← 24 种布局骨架(可直接粘贴) + 背景选择指南
    └── checklist.md      ← 质量检查清单
```

**加载顺序**:
1. 读完 SKILL.md(这个文件)
2. Step 1 先确定主题色,读 `themes.md`
3. **动手前 Read template.html 的 `<style>` 块** — 类名唯一来源
4. 读 `layouts.md` 挑布局
5. 生成后读 `checklist.md` 自检

---

## 关于作者

**森林**（你好森林）

- 公众号：**你好森林**（开发者效率工具推荐）
- 邮箱：suenty@foxmail.com

## 核心设计原则

> 违反其中任何一条,工具展示感都会垮。

1. **截图优先于文字** — 能截图说明的,不写文字
2. **每页一个核心信息** — 不堆砌,不塞入多主题
3. **简洁优于炫技** — 不要阴影、浮动卡片、复杂装饰
4. **无衬线只此一家** — Inter + Noto Sans SC,任何衬线都是错的
5. **数据要有来源** — 性能数据标注测试环境,不编造
6. **CTA 在首尾** — 封面和收尾有下载按钮,正文不打断阅读
