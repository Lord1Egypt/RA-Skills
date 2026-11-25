---
domain: ui-ux-design
skill_name: ui-ux-design-expert
subdomain: color-system
title: 配色与色彩系统（color-system）
version: 3
updated: 2026-11-16
source_index: corpus/ui-ux-design/color-system/elicited/01~09；docs/（webaim-contrast-thresholds、_fetch_log）；HIG color 锚点 corpus/ui-ux-design/style-design-system/docs/hig/color.md（跨域语料，R34 实抓）
knowledge_ratio: "法则 ~15% / 最佳实践 ~45% / 坑点 ~40%"
merged_at: 2026-11-16
---

# 配色与色彩系统（color-system）

## 定位与心智模型

「网站为什么好看」的色彩侧根因：好看不是运气色，而是**组织（token 分层）+ 和谐（显式策略约束）+ 可用（对比度验证）**三件事同时成立。

- **组织**：色值经 primitive → semantic 分层间接引用，禁裸 hex 进组件。
- **和谐**：整页取色受单一和谐策略与面积配比（60-30-10）约束，禁逐组件随机取色。
- **可用**：一切取色过 WCAG 阈值（4.5:1/3:1/7:1）与"仅颜色"检验，在真实渲染背景上计算。

边界：对比度条款的完整 a11y 执行见 usability-accessibility；token 跨类型（色/字/距）架构见 style-design-system。

## 法则

（条款尾括号数字 = frontmatter source_index 的 elicited/0N 文件；未标注者为 [模型经验]）

[CS-1] **NEVER**: 组件样式中禁硬编码具体色值（hex/rgb()/命名色）；色值只允许出现在 token 定义处，组件一律引用语义 token。违反→换肤/深色模式/品牌迭代全站样式发散失效。（01）

[CS-2] **MUST**: 文本对比度满足 WCAG AA——正文 ≥4.5:1；大字（≥18pt≈24px 常规 / ≥14pt≈18.66px 加粗）与非文本（图标/UI 边界/焦点指示器，含各交互状态）≥3:1。违反→a11y 审计与 EN 301 549 合规被打回。[官方文档](https://webaim.org/standards/wcag/checklist)（SC 1.4.3/1.4.11）

[CS-3] **NEVER**: 仅用颜色作传达信息的唯一手段；状态/数据/链接须叠加图标、形状、文字或位置差异。仅颜色区分链接时，对周围文本 ≥3:1 且 hover/焦点加下划线。违反→色盲用户无法区分关键信息（红绿色盲男性约 8%，待查）。[官方文档](https://webaim.org/standards/wcag/checklist)（SC 1.4.1）（04）

[CS-4] **MUST**: token 分层为 primitive（原始色阶）→ semantic（语义角色）→ component（可选）；组件只允许消费 semantic 层。（01）

[CS-5] **MUST**: 每个可交互色角色必须预生成 hover/active/focus/disabled 状态变体 token；禁用态用实色 tint 而非 opacity。（01）；状态对比度 [官方文档](https://webaim.org/standards/wcag/checklist)（SC 1.4.11）

[CS-6] **NEVER**: 禁 HSL 亮度等比缩放或 Sass `lighten()/darken()` 生成 tint/shade；须用 sRGB 混色、感知空间（OKLCH/HCT）或手工调校（暗化允许 hue 微移）。违反→黄变土橄榄、蓝过电霓虹、越界静默 clamp。（01、02）

[CS-7] **MUST**: 界面面积配比服从 60-30-10（60% 中性/背景、30% 次级、10% 强调）；高饱和品牌色不得作为大面积背景。（02）

[CS-8] **NEVER**: 高饱和互补/三角 hue 对（如 #EF4444 于 #22C55E）不得大面积相邻——同时对比最大化产生色彩振动（chromatic vibration），视疲劳。（02）

[CS-9] **MUST**: 语义反馈色遵循惯例：success=绿、error=红、warning=琥珀、info=蓝；品牌色与语义色同 hue 冲突时偏移明度/饱和或换 hue 拉开。（04）

[CS-10] **MUST**: 红-绿不得作为唯一区分轴；状态/数据配色必须通过 deuteranopia（绿色盲）模拟验证；红绿并置时以蓝-橙为安全替代对比轴。原则 [官方文档](https://webaim.org/standards/wcag/checklist)（SC 1.4.1）（04）

[CS-11] **MUST**: 深色模式必须为语义 token 的整体重映射；禁用 `invert()/hue-rotate()` 全局反转或逐色明度翻转冒充深色模式。（05）

[CS-12] **NEVER**: 大面积纯黑 #000 背景承载高亮 #FFF 正文（21:1 光晕 halation）；深色基底默认 #121212 一级，纯黑仅作用户可选 OLED 省电档。（05）

[CS-13] **MUST**: 深色模式下表面层级越高越亮（叠白/换更高 tone）；禁用"更深的黑"表达浮起。（05）

[CS-14] **MUST**: 深色模式下品牌色与语义色降饱和+提明度 1–2 档（如 #2563EB→#60A5FA、#DC2626→#F87171）；不得沿用浅色值。（05）

[CS-15] **NEVER**: 半透明文本色（rgba 白/黑）用于图片、渐变或彩色背景，除非叠加 scrim；次级文本优先实色 tint。（01、03）

[CS-16] **MUST**: 灰阶整体统一色温（全冷或全暖、统一 hue 偏移），禁纯灰与偏色灰混用；灰阶须染色进配色和谐体系。（01、02）

[CS-17] **MUST**: 对比度验证必须在真实渲染背景（灰底、彩底、深色底）上计算，禁只对纯白验证。违反→灰底灰字 2.3:1 类"淡雅但不可读"。（03）；阈值 [官方文档](https://webaim.org/standards/wcag/checklist)

[CS-18] **MUST**: 同一界面的全部取色受单一显式和谐策略（单色/类比/互补/分裂互补/三角 择一）约束；禁逐组件随机取色。违反→"彩虹界面"。（02）

[CS-19] **MUST**: 图表配色为浅深两主题分别定义，并分别验证对比度与色盲可辨性。（05）

[CS-20] **NEVER**: 黄/琥珀高亮度底配白字（#FACC15+白 ≈1.5:1）；高亮度底必须配深色文字。阈值 [官方文档](https://webaim.org/standards/wcag/checklist)（SC 1.4.3）（06）

[CS-21] **MUST**: categorical 色板 ≤8 类、色相均布、亮度一致；超类改分组/分面/direct label。（08）

[CS-22] **NEVER**: 数值映射禁彩虹系（jet/rainbow，明度非单调）；sequential=单 hue 明度单调，diverging 中点对准数据 0/中位语义。（08）

[CS-23] **MUST**: 图表配色过色盲模拟（deuteranopia 等）后发布；categorical 首选 Okabe-Ito/viridis + 形状双通道。（08）

[CS-24] **MUST**: 色阶按 OKLCH/HCT L 等步长生成、C 随 L 联动；禁 sRGB/HSL 数值等分冒充感知等距（sRGB 绿敏感蓝迟钝）。（09）

[CS-25] **NEVER**: 层级配色未过灰度验证（去饱和后层级仍成立）不得交付；P3 宽色域色必须配 sRGB 回退（@media color-gamut 增强层）。（09）

[CS-26] **NEVER**: Apple 平台禁硬编码系统颜色值（文档 RGB 值仅供参考且随版本波动）、禁重定义动态系统颜色的语义（如把 separator 色当文本色）；系统色一律经语义动态色 API（SwiftUI Color/UIKit UIColor）引用。溯源: [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/color)

[CS-27] **MUST**: 自定义颜色必须提供 light/dark 变体及高对比度（Increase Contrast）选项，同一颜色在 light/dark/increase contrast 上下文均可用；同一颜色禁止表示不同含义。溯源: [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/color)

[CS-28] **MUST**: 宽色域资产用 Display P3（16 bits per pixel per channel，PNG 导出）；P3 渐变在 sRGB 屏可能被裁剪，必要时提供双色彩空间版本（Apple 侧 asset catalog，Web 侧 `@media (color-gamut:p3)` 增强层）。溯源: [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/color)

[CS-29] **NEVER**: tvOS 焦点态禁仅用颜色表达——焦点指示以缩放+动画为主，颜色为辅；watchOS 避免长时间驻留视图使用全屏背景色。溯源: [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/color)

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| primitive token | 原始色阶（`--blue-600:#2563EB`），只定义不消费 |
| semantic token | 语义角色（`--action-primary-bg`），主题切换的重映射单元 |
| tint / shade | 与白/黑混合的浅/深变体；感知空间生成，HSL 亮度缩放为禁用方式 |
| 60-30-10 | 面积配比：60% 中性背景 / 30% 次级 / 10% 强调（源自室内设计） |
| 和谐策略 | 单色/类比(±30°)/互补/分裂互补/三角等 hue 关系方案，整页取一 |
| 相对亮度 L | 对比度计算中间量：L = 0.2126R + 0.7152G + 0.0722B（线性化分量） |
| 同时对比 / 色彩振动 | 高饱和互补色相邻时对比最大化，边缘产生彩边闪烁 |
| halation（光晕） | 纯黑底白字（21:1）高光溢出感知，字缘"发光"发虚 |
| gamut clamp | OKLCH 高 L 高 C 越 out sRGB gamut 被静默映射（保 L 降 C），hue 可能漂移 |
| OKLCH / HCT | 感知均匀色彩空间（HCT 为 Material 3 色阶核心）；L 均分才近似感知等距 |
| scrim | 图上文字下的暗色蒙层（如 `rgba(0,0,0,.5)`），保证任意背景下可读 |
| surface elevation | 深色模式下表面层级：层级越高越亮（叠白/更高 tone） |
| color-scheme | CSS 属性，声明后滚动条/表单等原生 UI 跟随明暗主题 |
| 语义反馈色 | success/error/warning/info 的行业惯例色映射，不可被品牌色覆盖 |

## 最佳实践

### 场景 1：从零构建色彩 token 体系

1. 先列语义角色矩阵再填色（顺序不可反）：role（bg-page/bg-surface/text-*/border/action-*/feedback-*）× state（default/hover/active/disabled）× theme（light/dark）。
2. 选定 primitive 色阶填入角色（来源见场景 2、3）；每交互角色生成状态四件套 token（[CS-5]）；组件只消费 semantic token（[CS-1][CS-4]）。
- do：primitive `--blue-600:#2563EB; --blue-700:#1D4ED8` → semantic `--action-primary-bg:var(--blue-600)` + `-hover/-active(#1E40AF)/-disabled(#DBEAFE 实色 tint 非 opacity)` → `.btn{background:var(--action-primary-bg)}`。
- don't：`.btn{background:#2563EB}` 裸 hex；`:hover{filter:brightness(.9)}` 运行时临时算；`:disabled{opacity:.4}` 叠彩底显脏且对比失控。
- 边界：原型期可暂用单层变量，但 semantic 间接层不可省（[CS-4]）；只有三个变量的"token 体系"在深色模式与换品牌两时刻必暴露残缺。（01）

### 场景 2：生成 tint/shade 色阶

1. 生成方式三选一（[CS-6]）：a) `color-mix(in srgb, <base> <n>%, white/black)`；b) OKLCH 按 L 均分、L 变化同步调 C（L>0.8 显著降 C 防 clamp）；c) 手工调校，暗化时允许 hue 微移（成熟色阶实际做法：暗化黄向橙移）。
2. 逐档目检 hue 是否漂移、相邻档是否可辨；两端补全（50 与 950 档），渐变/hover 深化/深色模式都需要。
- do：`--amber-tint:color-mix(in srgb,#F59E0B 80%,white)`；`--amber-shade:oklch(0.62 0.13 60)`（L 降 C 同步降）。don't：`hsl(45,100%,34%)` HSL 直暗→土橄榄绿。
- 边界：OKLCH 越界**静默 clamp 无报错**，高危，产出后逐档目检 hue；`color-mix()` 混色空间（in srgb / in oklch 差异大）要显式选择；Sass `lighten()/darken()` 与 HSL 缩放同属禁用。（01）

### 场景 3：选定和谐策略与面积配比

1. 显式选择一种 hue 关系策略：单色（最稳，靠明度层级撑）／类比（±30°）／互补（一主一辅、一浓一淡）／分裂互补／三角（[CS-18]）。
2. 按 60-30-10 分配面积：60% 中性/背景（白、近白、极浅 tint），30% 次级（浅 tint/辅色），10% 高饱和 accent（CTA/关键数据）（[CS-7]）。
3. accent hue 全页唯一；语义色按需出现，不计入装饰 accent；灰阶染同 hue（暖色板配暖灰），白色/近白纳入色板管理（[CS-16]）。
4. 情绪板驱动时：最大面积气质色**中性化进背景**，小面积高对比色做 accent，再派生全阶与灰阶。
- do：`bg-slate-50`（60 中性底）+ 白卡 `border-gray-200`（30）+ `bg-blue-600` 按钮（10 唯一 accent）；don't：`bg-blue-600` 品牌色大面积打底。
- 边界：单色策略须明度层级足够，否则"高级感"变"没设计"；跨 hue 取色黄系压 S 提 L（oklch L≈0.85）、蓝系保 S 降 L（≈0.55）校准等亮，或故意做非等亮明度层次；hue 旋转生成色板须随 hue 补偿 S/L。（02）

### 场景 4：保证文本对比度达标（锚点值法）

1. 按锚点表选色（见「参数速查表」）：白底正文至少 #4B5563 档；白底最浅 AA 灰为 #767676（≈4.5:1）。
2. 在真实渲染背景上复核（灰底卡片、彩色底、深色底）（[CS-17]）。
3. 半透明文本先复合再计算：有效色 = α×前景 + (1−α)×背景，逐通道复合；`rgba(0,0,0,.54)` on #FFF ≈ 4.6:1，on gray-100 需重算。
4. 链接双重要求：对背景 ≥4.5:1 + 对周围文本 ≥3:1，加下划线。
- do：`.card{background:#F3F4F6}` 标题 #1F2937（≈14:1）、次级 #4B5563（≈7.7:1）、`input::placeholder{color:#767676}`（4.54:1，placeholder 不豁免）。
- don't：#9CA3AF on #F3F4F6（≈2.3:1 "淡雅但不可读"）；placeholder #999（≈2.85:1）；链接与正文差 <1.5:1 不可辨。
- 边界：禁用元素、纯装饰豁免；大字 3:1；18–24px 非加粗**无**宽限仍需 4.5:1；渐变/图片上文字取**最差区域**验证。阈值 [官方文档](https://webaim.org/standards/wcag/checklist)（SC 1.4.3/1.4.1）；锚点色值（03）

### 场景 5：深色模式完整适配

1. 为每个 semantic token 建第二主题列值（整体重映射，[CS-11]）；基底取 #121212 级深灰或带色相深底（#0F172A），非 #000（[CS-12]）。
2. surface 层级越高越亮：叠白递增或换更高 tone（[CS-13]）；阴影失效时以边界线（`rgba(255,255,255,.08)`）+ 微亮底替代。
3. 品牌色/语义色提亮降饱和 1–2 档：#2563EB→#60A5FA、#DC2626→#F87171、#059669→#34D399（[CS-14]）。
4. 文本锚点：primary #F1F5F9（≈16:1）/ secondary #94A3B8（≈7:1）/ tertiary #64748B（临界，慎用于正文）。
5. 工程侧：`:root{color-scheme:light dark}` + 主题恢复脚本内联在 `<head>` 先于首帧执行（防 FOUC 白屏闪烁）。
- do：`html.dark{--bg-page:#0F172A;--bg-surface:#1E293B;--text-primary:#F1F5F9;--text-secondary:#94A3B8;--action-primary-bg:#60A5FA}`。
- don't：`filter:invert(1) hue-rotate(180deg)` 假深色（负片+品牌变浊）；深色次级 #6B7280（on #0F172A ≈3.7:1 fail）；卡片 `background:#000`（更深的黑 = 层级消失）。
- 边界：#000 有 OLED 省电优势，可作用户可选档（X/Twitter 范式）；图表是第二套配色系统，独立处理（场景 6）。（05）

### 场景 6：数据与状态配色（图表 / 语义色 / locale）

1. 图表系列色浅深两主题分别定义并验证（[CS-19]）：深色版提亮降饱和，轴线/网格用深色灰档。
2. 按数据类型选板（[CS-21][CS-22]）：类别→categorical（≤8 类，Okabe-Ito/viridis 等亮）；数值→sequential（单 hue 明度单调，离散档 ≤7）；双向→diverging（双 hue+中性中点，三段 domain 对准 0/中位，禁 min-max 中点漂移）。
3. 红-绿不作唯一区分轴（[CS-10]）：叠加 ▲▼/纹理/位置，过 deuteranopia 模拟；行情红绿 locale token 化反转（东亚 red=up，[CS-23]）；同 dashboard 系列色全局唯一（同色同义）。
4. 语义色不被品牌色覆盖（[CS-9]）：撞 hue 偏移明度/饱和或换 hue（品牌绿撞 success 改 teal #0D9488）。
- do：`:root[lang="zh-CN"]{--market-up:#DC2626;--market-down:#16A34A}`+`<span class="up">▲</span>`；热力图 viridis；偏差图 `.domain([-100,0,100])` 对准 0。
- don't：全球硬编码红绿（东亚读反）；`jet`（虚假边界+色盲不安全）；连续数据套 categorical；`.error{color:#3B82F6}` 品牌蓝被读作 info。
- 边界：色彩-情绪映射是统计偏好不是物理定律，验收以对比度/可辨性为准；"红按钮转化高"的真实机制是与页面基色的互补对比+违反预期，非色相魔力。（04、05、08）

### 场景 7：OKLCH 色阶生成参数

1. 三轴：L 感知明度(0–1，层级/对比锚轴)、C 彩度（气氛/降噪）、H 色相（和谐轴）；调层级动 L、调气氛动 C，互不牵连。
2. 色阶 L 等步长（如 11 档 L 0.97→0.25 等距）；C 随 L 联动：L>0.8 显著降 C（防静默 clamp）、L<0.4 降 C（防浑浊）、中段 C 峰值 hue 依赖（[CS-24]）。
3. 工程：先 hex 回退后 `oklch(0.55 0.18 255)` 覆盖；禁 `lch()`（CIELab）与 `oklch()` 混用；P3 走 `@media (color-gamut:p3)` 增强层（[CS-25]）；HCT=M3 专用，数值不与 OKLCH 互换。
4. 验证：逐档目检 hue 漂移/塌陷档 + 灰度验证层级；OKLCH L 差仅初筛对比度，终值按 WCAG 公式复核。
- do：`--brand-600:oklch(0.55 0.18 255)`（L 定层级、H 换主题）。don't：C 恒定全线（两端必翻车）；无回退直用 oklch()。
- 来源 [模型经验](corpus/ui-ux-design/color-system/elicited/09-perceptual-color-spaces.md)

### 场景 8：跨文化配色与行业惯例（出海）

1. **行业惯例先行**：金融保险=蓝、医疗=绿青+白、环保=绿棕米、奢侈=黑白金、快餐=红黄、儿童=高饱和原色、游戏=深底霓虹——惯例保证品类联想正确。
2. **惯例 vs 差异化**：整体守品类惯例（信任盘）+ 单点反差 accent 做记忆点；全套反惯例信任崩，全从众无记忆。
3. **跨文化重映射（出海必查）**：白=东亚哀悼（节庆/婚庆/长辈向禁大面积纯白，红金暖调）；红=东亚喜庆/涨；行情 locale 反转（[CS-23]）；「绿帽」中文语境营销禁忌；紫=部分文化哀悼（泰/墨，置信低）；蓝=全球最少被讨厌（最安全默认）。
4. **CTA 反迷信**：转化由与页面基色的互补对比+违反预期+唯一性+面积克制决定，非色相魔力。
- 边界：色彩-情绪映射是统计偏好非物理定律（蓝最稳、黄橙争议大），随语境/文化漂移；调查数字待验证，勿编造百分比。来源 [模型经验](corpus/ui-ux-design/color-system/elicited/04-color-psychology.md)

## 高频坑点（速查）

| # | 症状 | 根因 | 修复 | 关联 |
|---|---|---|---|---|
| 1 | 正文/placeholder 用 #999 或 gray-400（on #FFF ≈2.85:1 / 2.5:1） | 对比度拍脑袋，未查锚点表 | #767676（4.5:1 临界）或更深；placeholder 不豁免 | CS-2/CS-17 |
| 2 | `bg-blue-500 text-white` 按钮（≈3.7:1） | blue-500 亮度较高离白太近 | `bg-blue-600`（≈5.2:1）或深字浅底 | CS-2 |
| 3 | `bg-yellow-400 text-white`（≈1.5:1） | 黄感知亮度极高 | 配 `text-slate-900`（≈13.7:1） | CS-20 |
| 4 | 灰底灰字：gray-400 on gray-100（≈2.3:1） | 只对纯白验证 | 真实背景复核 + 深字（#1F2937 ≈14:1） | CS-17 |
| 5 | 深色沿用浅色灰：#6B7280 on #0F172A（≈3.7:1） | 未建深色锚点表 | dark 次级 #94A3B8（≈7:1） | CS-14 |
| 6 | `filter:invert()` 假深色：负片、阴影消失、品牌变浊 | 逐色反转非感知等距变换 | 语义 token 整体重映射 | CS-11 |
| 7 | 纯黑底白字长文刺眼（21:1 光晕） | halation 超舒适区 | #121212 基底 + ~87% 白（≈14:1） | CS-12 |
| 8 | 深色卡片用比页面更深的黑，层级消失 | 层级方向搞反 | 层级越高越亮（叠白/更高 tone/描边） | CS-13 |
| 9 | 黄 hover 变土橄榄、蓝 pressed 电霓虹 | HSL L 等比缩放生成 | color-mix / OKLCH(L+C 联动) / 手工调校 | CS-6 |
| 10 | hover 靠 `brightness(.9)`、disabled 靠 `opacity:.4` | 无状态变体 token | 四件套 token + 实色 disabled tint | CS-5 |
| 11 | 半透明白字压图片/渐变随背景失明 | 有效色 = 与背景复合，token 层无法约束背景 | 实色 tint + scrim | CS-15 |
| 12 | 红底绿字边缘"闪烁"（#EF4444 on #22C55E） | 高饱和互补同时对比最大化 | 一主一辅、一浓一淡（#F0FDF4 底 + 深绿字 + 红点睛） | CS-8 |
| 13 | 红→蓝渐变中点脏紫灰 | RGB 插值 + hue 差 ≥120° 必经浊区 | hue 差 ≤60° 类比渐变或同 hue 明度渐变 | CS-18 |
| 14 | 单屏 4+ accent hue（每卡片一色） | 强调色通胀，注意力预算超支 | 单 accent hue + 中性分层 | CS-7/CS-18 |
| 15 | 链接与正文同色系仅深半档，用户找不到链接 | 链接双对比（对正文 ≥3:1）未做 | 拉开色相差 + 下划线（SC 1.4.1） | CS-2/CS-3 |
| 16 | 品牌色 60% 大面积打底，页面"吵/廉价" | 60-30-10 误读为"60% 品牌色" | 60% 中性背景，品牌色收进 10% | CS-7 |
| 17 | 切深色后滚动条/原生 select/自动填充仍白底 | 缺 `color-scheme` 声明 | `color-scheme:light dark` + head 内联主题脚本防 FOUC | CS-11 |
| 18 | `oklch(0.95 0.2 260)` 渲染发灰偏紫，无报错 | 高 L 高 C 越 sRGB gamut 被静默 clamp | 高 L 区显著降 C，逐档目检 hue | CS-6 |
| 19 | 热力图用 jet：虚假边界、色盲全糊 | 明度非单调+红绿双通道 | viridis/magma | CS-22 |
| 20 | 连续数值套 categorical 离散色 | 类别色暗示虚假分类 | sequential 单 hue 明度渐变 | CS-21/CS-22 |
| 21 | 单图 12 系列颜色循环复用 | 超 8 类上限硬塞 | 分组/分面/direct label | CS-21 |
| 22 | OKLCH L 等分 C 恒定：高 L 发灰低 L 浑浊 | C 未随 L 联动，clamp 静默 | L>0.8 与 L<0.4 均降 C | CS-24 |

### 深潜 1：低对比灰字（AI/开发者最高频真实错误）

- 根因：hex 对生成者无感知语义，取值来自训练分布"统计常见"；"淡雅"审美与可读性反向；placeholder 被误认为豁免项（实际不是）；审计工具报 "Very low contrast" 而无运行时报错——静默失败更危险。
- 代码对照：错误 `.body{color:#9CA3AF}`、`input::placeholder{color:#999}`；正确 `.body{color:#1F2937}`（≈14.7:1）、`input::placeholder{color:#767676}`（≈4.54:1 白底最浅 AA 灰）。
- 关联：[CS-2][CS-17]；详见场景 4 锚点值法。阈值依据 [官方文档](https://webaim.org/standards/wcag/checklist)；锚点色值 [模型经验](corpus/ui-ux-design/color-system/elicited/03-contrast-readability.md)。

### 深潜 2：深浅模式同值灰

- 根因：`dark:text-slate-600` 翻车（#6B7280 on #0F172A ≈3.7:1）；深浅灰阶锚点方向相反（浅色越深越"次级"，深色越浅越"次级"），只建一套锚点必一侧翻车。
- 代码对照：错误 `html.dark .secondary{color:#6B7280}`（fail）；正确 `html.dark .secondary{color:#94A3B8}`（≈7:1）、`html.dark .primary{color:#F1F5F9}`（≈16:1）。
- 关联：[CS-14]；详见场景 5。来源 [模型经验](corpus/ui-ux-design/color-system/elicited/05-dark-mode.md)。

### 深潜 3：中高亮度底配白字（蓝/黄两型）

- 根因：按档位习惯（"500=主色档"）而非按对比度选档；blue-500 相对亮度 L≈0.235 离白太近；黄感知亮度极高、在文本分布里无信号。
- 代码对照：错误 `.btn{background:#3B82F6;color:#FFF}`（3.7:1）、`.badge{background:#FACC15;color:#FFF}`（1.5:1）；正确 `.btn{background:#2563EB;color:#FFF}`（≈5.2:1 blue-600）、`.badge{background:#FACC15;color:#0F172A}`（≈13.7:1 黄底必须深字）。
- 关联：[CS-2][CS-20]；500 vs 600 哪档配白字过 AA 是常见记忆混淆点，以锚点表为准。阈值 [官方文档](https://webaim.org/standards/wcag/checklist)；具体色值 [模型经验](corpus/ui-ux-design/color-system/elicited/06-ai-mistakes.md)。

## 参数速查表（API 速查）

### WCAG 对比度阈值表

| 场景 | 阈值 | WCAG 级别 | 条款 |
|---|---|---|---|
| 正文文本 | ≥4.5:1 | AA | SC 1.4.3 Contrast (Minimum) |
| 大文本（≥18pt≈24px 常规 / ≥14pt≈18.66px 加粗） | ≥3:1 | AA | SC 1.4.3 |
| 正文文本（增强） | ≥7:1 | AAA | SC 1.4.6 Contrast (Enhanced) |
| 大文本（增强） | ≥4.5:1 | AAA | SC 1.4.6 |
| 非文本：图标/图形对象、UI 边界/焦点指示器，含各状态 | ≥3:1 | AA | SC 1.4.11 Non-text Contrast |
| 仅凭颜色区分的链接 vs 周围文本 | ≥3:1（另需下划线等额外区分） | A | SC 1.4.1 Use of Color |
| 焦点指示器 vs 背景 | ≥3:1 | AAA | SC 2.4.13 Focus Appearance |

来源: [官方文档](https://webaim.org/standards/wcag/checklist)。豁免：禁用元素、纯装饰。

### 对比度计算公式（WCAG 相对亮度法）

1. sRGB 分量归一：c = v/255
2. 线性化：c ≤ 0.04045 → c/12.92，否则 ((c+0.055)/1.055)^2.4（旧文 0.03928 已由 WCAG errata 更正为 0.04045，8bit 值结果相同）
3. 相对亮度：L = 0.2126R + 0.7152G + 0.0722B（R/G/B 为线性化分量）
4. 对比度 = (L浅 + 0.05) / (L深 + 0.05)，值域 1:1–21:1

来源: [模型经验](corpus/ui-ux-design/color-system/elicited/03-contrast-readability.md)。

### 锚点色值表（手算，建议用工具复核）

| 组合 | 对比度 | 判定 |
|---|---|---|
| #767676 on #FFF | ≈4.5:1 | 白底最浅 AA 灰（临界） |
| #595959 on #FFF | ≈7.0:1 | 过 AAA |
| #808080 on #FFF | ≈3.9:1 | fail 正文，仅够大字 |
| #999999 on #FFF | ≈2.85:1 | fail（placeholder 惯犯） |
| #6B7280 on #FFF（gray-500） | ≈4.8:1 | 过 AA |
| #9CA3AF on #FFF（gray-400） | ≈2.5:1 | fail |
| #9CA3AF on #F3F4F6 | ≈2.3:1 | 双灰 fail |
| #FFF on #3B82F6（blue-500） | ≈3.7:1 | fail 正文 |
| #FFF on #2563EB（blue-600） | ≈5.2:1 | 过 AA |
| #FFF on #FACC15（yellow-400） | ≈1.5:1 | fail（近乎隐形） |
| #0F172A on #FACC15 | ≈13.7:1 | 黄底深字正确解 |
| #FFF on #121212 | ≈18.7:1 | 超舒适区（配 #000 达 21:1 光晕） |
| #F1F5F9 on #0F172A | ≈16:1 | dark primary 文本 |
| #94A3B8 on #0F172A | ≈7.0:1 | dark secondary 文本 |
| #6B7280 on #0F172A | ≈3.7:1 | fail（浅色灰搬深底惯犯） |

来源: [模型经验](corpus/ui-ux-design/color-system/elicited/03-contrast-readability.md)。验证工具：WebAIM Color Contrast Checker / Link Contrast Checker（[官方文档](https://webaim.org)）、Chrome DevTools 取色器、Stark、axe。

### Apple 系统色（HIG——引用而非复制）

13 系统色（Red/Orange/Yellow/Green/Mint/Teal/Cyan/Blue/Indigo/Purple/Pink/Brown）与 Gray 1~6 均有 default light/dark + increased contrast light/dark 四列值，且随系统版本波动——**只经语义动态色 API 引用，禁复制数值**（[CS-26]）；visionOS 系统色取 dark 列。完整四列值见 style-design-system kb 表 E 与 corpus hig/color.md。来源: [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/color)。

### 色阶生成公式

| 方法 | 写法 | 注意 |
|---|---|---|
| sRGB 混色 | `color-mix(in srgb, #F59E0B 80%, white)` | `in srgb` 与 `in oklch` 结果差异大，显式选空间 |
| 感知空间 | OKLCH 按 L 均分，L 变化时同步调 C；L>0.8 时 C 显著下调 | 高 L 高 C 越 gamut 静默 clamp，逐档目检 |
| 手工调校 | 允许暗化时 hue 微移（黄暗化向橙移） | 成熟色阶的实际做法 |
| （禁用） | `hsl()` L 等比缩放、Sass `lighten()/darken()` | 黄变土橄榄、蓝过电、梯度断裂 |

来源: [模型经验](corpus/ui-ux-design/color-system/elicited/01-color-tokens.md)。

## 版本注意

- **Apple HIG color（R34 已锚定）**: 系统色引用纪律（[CS-26]）、light/dark/高对比三上下文（[CS-27]）、P3 双色彩空间（[CS-28]）、tvOS 焦点（[CS-29]）；Liquid Glass 默认无固有色（透出后方内容），着色保留给真正需强调的元素（如主 CTA 背景），避免多控件背景同时着色。来源: [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/color)。
- **WCAG 2.2 为现行标准**（2023-10-05 发布）；EN 301 549:2026 采用之，验收以 2.2 条款为准。来源: [官方文档](https://webaim.org/standards/wcag/checklist)；标准原文 [官方文档](https://www.w3.org/TR/WCAG22/)。
- **APCA（WCAG 3 草案）**：Lc 值替代单一比值的新对比度体系，仍为草案、未进现行合规要求，不得以 APCA 替代 SC 1.4.3 验收；Lc 分档数值待验证。来源: [模型经验](corpus/ui-ux-design/color-system/elicited/03-contrast-readability.md)。
- **CSS Color 4**（`oklch()`/`color-mix()`/`color-scheme`）浏览器支持版本记忆模糊，使用前以 MDN/caniuse 实时核对；gamut mapping 的 hue 一致性依赖实现进度。来源: [模型经验](corpus/ui-ux-design/color-system/elicited/01-color-tokens.md)。
- **Tailwind 色阶**：50–950 十一档为事实标准，勿引用不存在的 20/1000 档；档位 hex 为模型记忆（置信中高），交付前机械复核。来源: [模型经验](corpus/ui-ux-design/color-system/elicited/01-color-tokens.md)。

## 与其他子领域的集成要点

- **usability-accessibility**：[CS-2][CS-3] 阈值与"仅颜色"原则同源 WCAG 清单；配色侧取值与验证在本文件，完整 a11y 执行（辅助技术、focus 顺序、audit 工具链）在彼处。
- **style-design-system**：primitive→semantic→component 是 token 架构的色彩维度实例；命名/跨类型分层/交付流程归彼处；Apple 系统色四列值/材质/Liquid Glass 着色纪律集中在该 kb 表 E 与 materials 条目，本文件只留引用纪律（[CS-26]~[CS-29]）。
- **visual-perception**：[CS-7] 的 10% 面积约束与 accent 唯一性对应 Von Restorff 孤立效应；同时对比/振动（[CS-8]）机理详见该 kb。
- 反向依赖：深色模式工程实现（主题切换/FOUC/`prefers-color-scheme`）本文件仅最小集，完整方案随平台技术栈走。

## 来源索引

**官方文档（阶段 2 真实抓取，白名单 URL）**：
- https://webaim.org/standards/wcag/checklist — WCAG 对比度与色彩阈值（1.4.x/2.4.13、大字定义、WCAG 2.2 现行版本、EN 301 549:2026）→ docs/webaim-contrast-thresholds.md
- https://webaim.org/ — 根页入口（Checklist、Contrast Checker 工具）
- https://www.w3.org/WAI/standards-guidelines/wcag/ — W3C WAI WCAG 标准入口
- https://www.w3.org/TR/WCAG22/ — WCAG 2.2 规范原文
- https://developer.apple.com/design/Human-Interface-Guidelines/color — Apple HIG Color（系统色/灰色四列值、动态色纪律、P3 色彩管理、平台特性）→ corpus/ui-ux-design/style-design-system/docs/hig/color.md（跨域语料，物理存于 style-design-system 域，归属注明见 _fetch_log_r34-hig.md）

**模型经验（corpus 路径，见 frontmatter source_index）**：01-color-tokens、02-color-harmony、03-contrast-readability、04-color-psychology、05-dark-mode、06-ai-mistakes、07-laws、08-dataviz-color、09-perceptual-color-spaces。

**降级声明**：种子 https://m3.material.io 为 JS 渲染站点、抓取失败（docs/_fetch_log.md）——Material 3/HCT/surface-container 精确值、Radix Colors 算法、Tailwind 档位 hex 均为模型经验，未经文档验证；引用前需机械复核。

## 冲突消解记录

| # | 模型原认知 | 文档事实 | 采用结论 |
|---|---|---|---|
| 1 | 07-laws CS-2 大字加粗阈值写"≥18.7px"，另有 18.5px 舍入说法 | WebAIM：≥14pt ≈ **18.66px** 加粗 | 以文档为准统一 18.66px；18–24px 非加粗无宽限 |
| 2 | 03 对 Focus Appearance 条款号记忆模糊（误写 1.4.13） | WebAIM：**SC 2.4.13** Focus Appearance（AAA），焦点指示器与背景 ≥3:1 | 条款号更正为 2.4.13，写入 [CS-2] 与速查表 |
| 3 | 07-laws CS-2 仅列非文本元素阈值，未提组件状态 | WebAIM（1.4.11）：组件各状态（focus/hover/active）均须 ≥3:1 | 补入 [CS-2]/[CS-5] 与速查表 |
| 4 | [CS-25] P3 配 sRGB 回退仅写 Web 侧 `@media (color-gamut:p3)` | HIG：P3 渐变在 sRGB 屏可能被裁剪，必要时 asset catalog 提供 sRGB/P3 双色彩空间版本 | 同一原则平台各自表述；升 [CS-28] 官方锚点 |
| 5 | [CS-11] 深色模式=light/dark 两态整体重映射 | HIG：自定义颜色须提供 light/dark 变体**及高对比度选项**，同一颜色 light/dark/increase contrast 上下文均可用 | HIG 多一档维度；升 [CS-27]（Web 侧 `prefers-contrast` 对应） |
| 6 | [CS-1] 禁硬编码色值为通用 token 纪律 | HIG：不硬编码系统颜色值、不重定义动态系统颜色语义，文档 RGB 值随版本波动 | 平台侧具体化；升 [CS-26] |

其余原子均为模型经验，文档未覆盖，无冲突。
