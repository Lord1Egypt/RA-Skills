---
domain: ui-ux-design
skill_name: ui-ux-design-expert
subdomain: layout-composition
title: 布局与构图——元素如何摆放、对齐、分配空间
version: 2
updated: 2026-11-16
merged_at: 2026-11-16
source_index: 模型萃取 corpus/ui-ux-design/layout-composition/elicited/01~12；HIG layout 锚点 corpus/ui-ux-design/style-design-system/docs/hig/layout.md（跨域语料，R34 实抓）；详见文末来源索引
knowledge_ratio: 法则 ~15% / 最佳实践 ~45% / 坑点 ~40%
---

# 布局与构图（layout-composition）

## 定位与心智模型

「为什么好看」的根因之一：**元素如何摆放、对齐、分配空间**。布局是关系的编码：**间距=关系**（近=同组，格式塔接近性）；**对齐=扫视路径**（强版式全页一条主轴）；**层级=注意力分配**（视觉重量=尺寸×对比×密度×位置力矩，一屏一个最强音）；**栅格=强制对齐工具**（12 列是工程共识，因子 1/2/3/4/6/12）。
边界：颜色（color-system）、字体与排印（typography）、感知原理深层（visual-perception）、无障碍合规（usability-accessibility）由对应 kb 承担，本文只留衔接点。

## 法则

（条款尾括号数字 = 文末来源索引 elicited/0N 文件，均为 [模型经验]）

`[LC-1]` **MUST**: 间距必须取自固定刻度（4 的倍数，推荐 4/8/12/16/24/32/48/64），禁 13/15/18px 等任意值。违反→垂直节奏断裂、间距失去编码能力。（02）

`[LC-2]` **MUST**: 关系层级必须由间距编码——同组间距 < 相邻组间距，相邻层级约 2 倍递减（组间 32 : 控件间 16 : 组内 4~8）。违反→分组错误、标签被看成上一组尾巴。（02）

`[LC-3]` **MUST**: 区块间距必须大于区块内部 padding（区块间隙 96~128 > 卡片 padding 16~24）。违反→模块边界消失、整页糊成一片。（02）

`[LC-4]` **MUST**: 每屏必须恰好一个最高强度主操作（primary），其余降级 secondary/ghost/text。违反→注意力稀释、转化率下降。（05、06）

`[LC-5]` **NEVER**: 主操作不得与大面积背景/导航同色同饱和——主 CTA 须与局部背景有可辨识 Δ 对比+留白孤立。违反→主 CTA 显著性归零。（05）

`[LC-6]` **MUST**: 同一视觉组内文本共享一条对齐轴线；全页主对齐轴唯一，装饰图形可出血例外。违反→扫视路径横跳。（03）

`[LC-7]` **NEVER**: 超过 3 行的正文段落不得居中对齐。[GLOBAL]（03）

`[LC-8]` **MUST**: 正文必须限行长——英文 45~75 字符（约 65ch）、中文 30~40 字/行，不得无 max-width 拉满全宽。[GLOBAL]（02、04）

`[LC-9]` **MUST**: 断点必须按内容重排行为定义（列数降级/侧栏转抽屉/间距分档），移动端重排非等比缩放；±1px 必测。违反→767/769px 布局异常。（01、06）

`[LC-10]` **MUST**: 12 列内 span 布局必须满足整除关系或显式子栅格；禁 12 列直接 5 等分。违反→尾行留洞、错位。（01）

`[LC-11]` **NEVER**: 替换型内容（img/video/iframe/table/pre）不得无溢出防护放入布局容器——须 `max-width:100%` 或滚动容器包裹。[GLOBAL]（01、06）

`[LC-12]` **MUST**: grid/flex 子项含不可控内容（用户文本/URL/长词）必须显式处理溢出（`min-width:0`+`overflow-wrap`）。[GLOBAL] 违反→长字符串撑爆轨道。（06）

`[LC-13]` **MUST**: 媒体必须提供固有尺寸（width/height）或 aspect-ratio 占位。[GLOBAL] 违反→CLS 布局跳动。（06）

`[LC-14]` **NEVER**: 全屏区块不得用固定 height（px/vh），须 min-height+内容驱动；移动端全屏高用 svh/dvh。违反→小视口裁切 CTA、地址栏遮挡。（01、06）

`[LC-15]` **MUST**: 交互目标可点击区域 ≥44×44pt（iOS，HIG 已锚定）/48×48dp（Android，待验证），行内小图标 padding 扩热区。[GLOBAL]（02）

`[LC-16]` **MUST**: 移动端主操作必须位于拇指可达区（吸底操作栏/底部标签），不得只置顶部。（05）

`[LC-17]` **MUST**: 层级与状态必须多通道编码——字号差 ≥1.2 倍，或字号+字重/颜色双通道；禁仅靠细微字号差或仅颜色区分。[GLOBAL]（05、06）

`[LC-18]` **NEVER**: 不得用空元素或绝对定位拼贴承担布局结构；布局空间须由 gap/margin/padding/grid 区域承担。违反→视口一变即碎。（02、06）

`[LC-19]` **MUST**: 嵌套间距必须层级递减（父 gap > 子 padding > 孙 gap），同值 gap 不得叠加。违反→间距节奏翻倍。（01）

`[LC-20]` **MUST**: 页面必须设计四态——空/加载/错误/成功（+溢出态）；空态必须提供下一步动作。[GLOBAL]（04、06）

`[LC-21]` **MUST**: 均分轨道含长不可断内容必须 `minmax(0,1fr)` 或子项 `min-width:0`，防 min-content 撑爆、均分失衡。（08）

`[LC-22]` **MUST**: 数量不可预知的列表流必须 `auto-fill+minmax(最小可读宽,1fr)`，`auto-fit` 仅限少量固定项，防空轨道折叠拉伸。（08）

`[LC-23]` **NEVER**: 同项目禁并存两套栅格体系（12 与 24 列、Bootstrap 类与 Tailwind 类、负 margin 与 gap 混用），防双对齐线间距失控。（08）

`[LC-24]` **MUST**: 框架断点/容器宽/gutter 必须以当前框架版本文档为准，禁跨框架记忆移植，防响应式行为整体偏移。[GLOBAL]（08）

`[LC-25]` **MUST**: 可复用组件内部响应式必须基于容器查询（`@container`），禁依赖视口断点假设容器宽，防窄容器内永不切换。（08）

`[LC-26]` **MUST**: 栅格类型必须匹配内容权重——等权用对称列栅格、杂志矩阵用模块栅格、权重悬殊用非对称分层（8+4），禁默认等分削平主内容。（08）

`[LC-27]` **MUST**: line-height 计算值必须落 4px 子网格，正文行高为基线整数倍（16×1.5=24），防垂直节奏断裂。[GLOBAL]（08）

`[LC-28]` **MUST**: 12 列每行 span 之和必须=12；复杂排布用显式起止线（`grid-column:a/b`），防换行留洞/越界无警告。（08）

`[LC-29]` **MUST**: 跨卡片横向对齐必须优先 subgrid，禁固定高度 hack；不支持环境须显式降级。（08）

`[LC-30]` **MUST**: gutter/margin 必须随断点分档缩放（桌面 24→移动 12~16），防移动端占比过高（24/375≈6.4%）。（08）

`[LC-31]` **MUST**: 设计稿画板宽（1440/1920）禁直接用作 CSS max-width；容器宽=画板−两侧 margin，防内容区偏宽列宽全错。[GLOBAL]（08）

`[LC-32]` **MUST**: 栅格列数必须整除最常见的同时展示内容数（或显式声明留洞），列数选择先于样式，防尾行孤卡。（08）

`[LC-33]` **MUST**: Apple 平台布局决策必须依据 size class（compact/regular，横竖各一）而非设备类型/方向；size class 变化时功能不变、可见功能量可变（如宽空间 tab bar 换 sidebar）；须考虑所有 size class 组合，idiom 不随窗口缩放改变。交叉引用 [SD-31]，平台规格矩阵归 style-design-system kb 表 C。[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/layout)

`[LC-34]` **MUST**: 内容必须置于 safe area 内（避开 Dynamic Island、状态栏、toolbar/tab bar 遮挡）；tvOS 主内容距上下 60pt、左右 80pt；layout guide 用于定位/对齐/间距（含文本可读宽度限制）。交叉引用 [SD-32]，数值归 style-design-system kb 表 C。[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/layout)

`[LC-35]` **NEVER**: watchOS 每行不得超 2~3 个控件（glyph 按钮 ≤3 并排、文本按钮 ≤2，文本按钮通常占满全宽）；macOS 避免控件/关键信息置于窗口底部（用户常把底边移出屏幕）及顶部摄像头区域之后。[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/layout)

`[LC-36]` **MUST**: 平台适配清单必须全覆盖：size class 组合、屏幕尺寸/方向/宽高比、Dynamic Island、可调窗口（iPad 与 Mac/外接屏/Display Zoom）、字号变化（Dynamic Type 大字号横向相邻改纵向堆叠、行高增长）、国际化（RTL、文本长度、日期数字格式）。[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/layout)

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| 8pt 体系 | 间距/尺寸取 8px 基准刻度（4px 半步长），Token 化 |
| 基线网格 | 行高与垂直间距均为 4px 基线整数倍 |
| gutter/gap | 栅格列间距（16~32px），属间距刻度 |
| margin 折叠 | 块级相邻垂直 margin 取大值不相加；flex/grid 内不折叠 |
| 格式塔接近性 | 视觉按间距自动分组——间距即语义 |
| 光学对齐 | 按视觉重量而非包围盒对齐，圆/三角补偿 1~2px |
| 视觉中心 | 平衡点略高于几何中心，居中后光学上移 1~2px |
| 视觉重量 | 尺寸×明度对比×饱和度×密度×位置力矩 |
| Z/F 动线 | Z：图形稀疏页四点连线；F：文字密集页压左缘与前两行 |
| 倒金字塔 | 结论前置：首屏/首段先答 what/for whom/next step |
| mobile-first | 断点统一 min-width 递增，桌面增量覆盖移动基线 |
| `min-width:0` | grid/flex 子项默认 auto，长内容撑爆轨道的解药 |
| measure（行长） | 正文一行长度：英文 ~65ch，中文 30~40 字 |
| CLS | 布局偏移指标；媒体无占位是布局侧首要成因 |
| svh/dvh/lvh | 移动端小/动态/大视口高度单位，替代 100vh |
| subgrid | 子网格继承父轨道，解决嵌套对齐 |
| Container Queries | `@container`+cqw/cqi，组件级响应式 |
| 四态设计 | 空/加载/错误/成功（+溢出态）是布局完整交付物 |

## 最佳实践

### 场景 1：间距系统（刻度 + 层级编码）

1. 定刻度：全项目仅 4 的倍数，Token 化（Tailwind v3 映射见下参数速查表）。
2. 三级关系：组间 > 控件间 > 控件内约 2 倍递减（32→16→8→4）；区块间隙 > 区块内 padding（[LC-3]）；嵌套父 gap > 子 padding > 孙 gap（[LC-19]）。
3. 分档：section 间距移动 48~64 / 桌面 96~128。
- 错误：全 16px 单值+区块粘连；正确：`.group{margin-bottom:32px}.field{margin-bottom:16px}.label{margin-bottom:4px}section{padding:48px 0;margin-bottom:96px}`。
- 边界：B 端高密度可下探 4px 半步；营销页放大步长；同一关系禁 gap 与 margin 混用。源于 [LC-1][LC-2][LC-3][LC-19]（02）。

### 场景 2：12 列栅格 + 内容驱动断点（mobile-first）

1. 容器 `max-width:1140~1280px`+`margin-inline:auto`；安全边距移动 16~24 / 平板 32~48。
2. `repeat(12,1fr)`，span 只用 1/2/3/4/6/12。
3. 断点从内容推：最小可读宽×列数+gap ≈ 降列断点（KPI 卡 220×4+3×24≈1020 → ~1024 降 3 列），不抄设备名。
4. 方向统一 min-width，断点只增不改；边界 767/769、1023/1025 逐像素测。
- 错误：抄设备断点+min/max 混用；正确：`.kpi{grid-template-columns:1fr;gap:8px}` → 520px 起 `repeat(2,1fr);gap:12px` → 820px 3 列 → 1024px 4 列。
- 边界：5 等分脱离 12 列 span 语义改 `repeat(5,1fr)`（[LC-10]）；组件级响应用 Container Queries。源于 [LC-9][LC-10]（01）。

### 场景 3：自适应卡片网格（minmax + 嵌套间距）

1. 不定列数用 `repeat(auto-fill,minmax(下限,1fr))`，下限=最小可读宽（列表卡 ~280、KPI 卡 ~220px），先测再写。
2. 嵌套递减：外层 gap 24 → 卡内 padding 16 → 卡内元素 gap 8~12；需与母网格对齐用 subgrid。
3. 卡内不可控文本补 `min-width:0`（[LC-12]）。
- 边界：`auto-fit` 折叠空轨道拉伸末项，仅意图占满时用；均分防溢出 `minmax(0,1fr)`（[LC-21]）。源于 [LC-10][LC-12][LC-19][LC-22]（01）。

### 场景 4：阅读容器与行长控制

1. 正文 `max-width:65~75ch`（中文 30~40 字/行）+`margin-inline:auto`；短文案（≤2~3 行副标题）可居中，正文回左对齐（[LC-7]）。
2. 表格/代码/媒体不塞正文容器硬撑——`max-width:100%`+外层 `overflow-x:auto` 滚动容器。
3. 表单单列宽 480~640px 居中。
- 正确：`.article .body{text-align:left;max-width:65ch;margin-inline:auto}` `.article pre{max-width:100%;overflow-x:auto}`。
- 边界：引用/图注可比正文窄一档制造层级；英文 justify 产生"河流"（`hyphens:auto` 缓解），中文 justify 可接受。源于 [LC-7][LC-8][LC-11]（02、03）。

### 场景 5：页面版式骨架速配

- **落地页**：Nav/Hero（H1+副题+主 CTA+信任标记）/社证/特性 3~6/图文交替/定价/FAQ/尾部 CTA。首屏答"是什么、给谁、下一步"；主 CTA 首屏 ≥1 且页尾复现；图文交替偶数块反转；H1 限宽 ~18ch，hero `min-height:88svh`。
- **仪表盘**：侧栏 240~280/顶栏 56~64/KPI 行/图表/表格。KPI 卡=数值+环比 delta+标题+sparkline；span 按优先级非均分（主图 8 次 4）；图表高 280~360；移动端侧栏变抽屉。
- **详情页**：媒体 55~60%+信息 40~45%（`3fr 2fr;gap:48px`）；价格与主 CTA 同组；buy-box `position:sticky;top:88px`；移动端操作栏吸底（场景 7）。
- **表单页**：单列 > 双列；仅语义相关字段（姓/名、城市/邮编）并排且移动塌陷；分组间 32~48、字段间 16~24、标签贴字段 4~8；提交按钮不远离末字段；>8 字段改分步向导。
- **列表页**：筛选侧栏 240~300 sticky（`top:64px`）+工具行+结果+分页；筛选 chips 可单个移除+一键清空；空态给原因+"清除筛选"；无限滚动/分页二选一，前者需计数常显+位置记忆+页脚入弹层。
- **登录页**：居中卡片（表单 360~400px）或分屏；分屏移动端砍品牌图；键盘弹起不遮主按钮。
- 边界：经验锚点非铁律，产品密度模式（营销低/后台高）决定分档；所有版式补四态（[LC-20]）。（04）

### 场景 6：CTA 显著性与强度阶梯

1. 每屏唯一 primary（[LC-4]），其余走强度阶梯：实心 > 描边 > 文本。
2. CTA 三件套：与局部背景 Δ 对比（全场唯一强调色）+尺寸+留白孤立。
3. 文案倒金字塔：H1 限宽 ~18ch 写实（不写"重新定义未来"）；首段答 what/for whom/next。
4. 动线检查：中央模态/cookie 条改底部窄条；hero 85~90svh 露下模块上缘暗示可滚；装饰不引离 CTA（深化见场景 12）。
- 错误：三个同强度按钮；正确：`.btn-primary{background:var(--accent);color:#fff}` `.btn-secondary{border:1px solid var(--line);background:transparent}` `.btn-tertiary{color:var(--accent)}`。
- 边界：定价三档仍强化推荐档（徽标+边框+微放大 1.05~1.1）；层级手段按成本：位置/DOM → 尺寸（相邻 ≥1.25 倍显差）→ 字重 → 颜色 → 留白 → 填充。源于 [LC-4][LC-5][LC-17]（05）。

### 场景 7：移动端适配（结构重排 + 拇指可达）

1. 响应式=结构重排：列数降级、侧栏转抽屉、间距分档、操作栏吸底——非等比缩字号。
2. 间距分档或 `clamp()`：`margin-block:clamp(48px,8vw,128px)`。
3. 全屏区块 `min-height:100svh`（回退 vh），绝不定值 height（[LC-14]）。
4. 主操作吸底+safe-area：`padding-bottom:calc(12px + env(safe-area-inset-bottom))`；桌面侧栏移动端变抽屉而非 `display:none`。
- 错误：`@media(max-width:768px){body{font-size:14px}}` 假响应式；正确：`.layout{grid-template-columns:1fr}` `.sidebar{position:fixed;transform:translateX(-100%)}` `.action-bar{position:fixed;inset:auto 0 0 0}`。
- 边界：内容浏览型 App 导航用底部 tab；平板（md 档）最常被漏测。源于 [LC-9][LC-14][LC-16]（05、06）。

### 场景 8：对齐轴与光学修正

1. 全页一条硬左轴（文本），层级用间距/字号表达而非缩进起梯田。
2. 图标与文字按形状光学校正：三角/圆包围盒等距≠视觉等距，补偿 1~2px；垂直居中元素光学上移 1~2px（大元素 2~4px）。
3. 表单标签三模式：顶对齐（扫描最快、移动友好）> 右对齐（左缘锯齿）> 左对齐（最慢）；B 端长表单用顶对齐。
4. 表格金额/数量列右对齐，文本列左对齐。
- 错误：三个起点+数学等距当光学等距；正确：`.title,.desc{margin-left:32px}` `.badge>svg{transform:translateY(-2px)}`。
- 边界：图片/装饰可出血但文本锚点保持；比例不硬算黄金比——用整数近似（2:3、3:5）或"主区自适应+侧栏固定 260~320px"。源于 [LC-6]（03）。

### 场景 9：防御性布局（溢出 + 占位 + 四态）

1. 全局兜底：`img,video,pre{max-width:100%}`；table 包 `overflow-x:auto`。
2. 含用户内容的 grid/flex 子项：`min-width:0`+`overflow-wrap:anywhere`。
3. 媒体占位：img 写 width/height 或容器 `aspect-ratio`。
4. z-index 分层：sticky 1000/dropdown 1100/overlay 1200/modal 1300/toast 1400，禁 9999。
5. 四态：空态（给下一步）/加载态（骨架屏）/错误态（可重试）/溢出态（截断策略）。
6. 短内容页脚不上浮：`body{min-height:100dvh;display:flex;flex-direction:column}`+main `flex:1`。
- 边界：`overflow-wrap:anywhere` 与 break-word 差异（anywhere 参与 min-content 计算）待验证，防御先 anywhere。源于 [LC-11][LC-12][LC-13][LC-20]（06）。

### 场景 10：垂直节奏（基线网格）

1. 行高显式取 4 的倍数（20/24/28/32/48px），不用 unitless 1.05/1.618。
2. 配对示例：h1 40/48、h2 32/40、正文 16/24；中文行高 1.5~1.8。
- 错误：`h1{line-height:1.05}`；正确：`h1{font-size:40px;line-height:48px}` `p{font-size:16px;line-height:24px}`。
- 边界：display 大标题可例外，正文与组件文本守刻度；中文最优行高为经验值待验证。源于 [LC-1][LC-27]（01、02、08）。

### 场景 11：栅格系统选型与实现

类型决策：

| 内容特征 | 类型 | 实现 |
|---|---|---|
| 等权重复单元 | 对称列栅格 | `repeat(N,1fr)`，N 整除内容数（[LC-32]） |
| 文本密集+垂直节奏 | +基线栅格 | 行高落 4px 网格（[LC-27]） |
| 杂志式受控错落 | 模块栅格 | `grid-template-areas` 跨格 |
| 权重悬殊（hero/3:1） | 分层栅格 | `2fr 1fr`/8+4 非对称 span（[LC-26]） |

12 列计算式：`列宽=(容器宽−margin×2−gutter×11)/12`（Bootstrap gutter 走列 padding 不减 margin：`(容器宽−11×gutter)/12`）；例 1440/120/24→78px。span 速查：6+6/8+4/9+3/7+5（近黄金比）/4+4+4/3×4/2×6，行内和必=12（[LC-28]）。
CSS Grid 参数：`repeat(12,minmax(0,1fr));gap:24px`；关键行显式起止线 `grid-column:1/7`，流式才 `span N`；列表流 `auto-fill+minmax(最小可读宽,1fr)`（[LC-22]）；等高 `grid-auto-rows:1fr`；跨卡对齐 subgrid（[LC-29]）。
框架对照（断点见下）：Bootstrap 12 列负 margin+padding / Tailwind v3 任意列走 gap / M3 4-8-12 列跳档（dp 与 px 不同源不可直译）/ AntD 24 列。
- 边界：画板宽≠CSS 容器宽（[LC-31]）；框架数值待验证。源于 [LC-21]~[LC-32]（08）。

### 场景 12：视觉流编排

视觉重量≈尺寸×色彩×位置×形态乘积，左右半区重量矩应大致平衡（大而轻配小而重）：

| 维度 | 增重 |
|---|---|
| 尺寸 | 面积大者重（近线性） |
| 色彩 | 高饱和>低饱和；暖>冷；与背景 Δ 大者重；深色块=锚点 |
| 位置 | 左上>右下（LTR 重力）；负空间孤立加成 |
| 形态 | 实心>描边；照片>插画；人脸/箭头带指向；动效>静态 |

要点：① 每页恰一个入口点（唯一强调色/最大字号/唯一动效/留白孤立至少其一）；② 文字密集页 F 型（前两行+左缘放关键信息）、稀疏图形页 Z 型（右下终点放 CTA）、均质无锚点页 Gutenberg（右下放 CTA）；③ 指向性元素必指向 CTA，装饰避开动线终点；④ 入口到 CTA 跳点 ≤3，长页每 1~1.5 屏复现次级 CTA；⑤ 深色区后露下模块上缘 80~120px 防"页面结束"误判。
- 诊断：模糊测试（模糊后仍可辨认=真实入口点）+灰度测试（去色后重量层次仍分明）。源于 [LC-4][LC-5]（09）。

### 场景 13：现代版式速查

| 版式 | 结构特征 | 适用 | CSS 要点 | 滥用警示 |
|---|---|---|---|---|
| Bento grid | 圆角卡片混排，大卡=高权重 | 特性总览/作品集 | `repeat(4,1fr)+grid-auto-rows:160px`，大卡 span 2×2 | span 随机；卡数>8 |
| 分屏 hero | 图文 50/50（或 60/40） | 品牌/登录/双角色 | `1fr 1fr`；移动塌单列、图限高 ~40svh、文案在上 | 双侧都放重点 |
| 卡片流 | 同构卡片网格/feed | 数量不可预知列表 | `auto-fill+minmax(280px,1fr)`；操作栏沉底 | 信息全同字重 |
| 杂志式 | 模块栅格+跨格+display 字阶 | 长文/品牌故事 | `grid-template-areas`+拉引文 | 后台套杂志版式 |
| 不对称构图 | 主体 60~70%+小要素偏置 | 单品发布/作品集 | `minmax(0,2fr) 1fr`，比例全站复用 | 比例每页都变 |
| 大留白极简 | 窄列 640~720+巨距 120~240 | 高端品牌/单品页 | `max-width:680px`+`clamp(120px,15vw,240px)` | 内容多产品硬套 |
| 密度分级 | 舒适/标准/紧凑（gap 24/16/8~12） | B 端后台/监控 | `--gap/--pad/--row-h` token；紧凑禁触屏 | 一屏混两档 |

- 边界：Bento/极简风为社区归纳无规范出处；密度档数值为经验值。源于 [LC-26][LC-32]（10）。

### 场景 14：响应式图片与媒体交付

1. **尺寸自适应**：`srcset`（w 描述符）+ `sizes` 必配对（缺 sizes 按 100vw，移动端下大图）；裁切焦点变化才用 `<picture><source media>`，纯分辨率用 srcset。
2. **格式链**：`<source type="image/avif">`→`webp`→`<img src="jpg">` 逐级回退；PNG 仅透明/锐利图形。
3. **占位防 CLS**：`width/height` 属性预留空间（推 aspect-ratio）+ CSS `aspect-ratio` 兜底。
4. **加载策略**：首屏 LCP 图禁 lazy，`fetchpriority="high"`；首屏外 `loading="lazy"`。
5. **alt 分级**：装饰图 `alt=""`（非省略，省略则念文件名）；内容图写实描述（无「图片」前缀）；功能图 alt=动作名。
- don't：首屏 hero `loading="lazy"`（LCP 灾难）；base64 内联大图；LCP 位用 `<video>`（海报图才是 LCP，优先 `<img>`）。
- 边界：深色模式照片 `filter:brightness(.85)` 或换暗调 asset；CSS 背景图走 `image-set()`。源于 [模型经验](corpus/ui-ux-design/layout-composition/elicited/11-responsive-media.md)

### 场景 15：图表选型与可视化信息设计

1. **意图→图型**：比较→条形（类目名长用水平）；趋势→折线（≤5 条，超出分面小图）；构成→堆叠条形 ≤4 层（饼仅 ≤5 片且强调整体时）；分布→直方/箱线；关系→散点（>1000 点降透明度）。类目轴禁折线（无序类目连线误导连续性）。
2. **坐标轴纪律**：条形/柱 y 轴必须从 0（面积编码，截断=夸大差异；折线靠位置编码可非零但标注起始值）；刻度取整（0/25/50/100）；双 Y 轴柱线混用禁（AIM-36）。
3. **交互**：悬停 tooltip 精确值+单位（触屏长按等价、最近点捕获）；图例点击开关系列（禁 hover-only，[VP-11]）；下钻面包屑可回（P-11）；入场 ≤500ms 且 reduced-motion 直出。
4. **无障碍**：每图配数据表 fallback（`<details>` 折叠或「查看数据」）；alt/figcaption 写结论（「Q3 华东超华北 12%」）非图形描述；配色纪律见 color-system kb 场景 6（categorical ≤8/sequential 明度单调/双通道）。
- don't：3D 饼/3D 柱（透视遮挡+面积误读）；饼 >5 片；「其他」片 > 最大实类。
- 边界：各上限值为教科书惯例聚合，无单一出处。源于 [模型经验](corpus/ui-ux-design/layout-composition/elicited/12-chart-selection.md)

## 高频坑点（速查）

### 深度展开 Top 3

**坑点 A：12 列排 5 等分尾行留洞（[LC-10]）**：12 因子仅 1/2/3/4/6/12。修复：`repeat(5,1fr)` 或改 6/4 等分；查行内 span 和=12（[LC-28]）。

**坑点 B：长内容撑爆 grid/flex 轨道（[LC-12]）**：子项默认 `min-width:auto`，不可断行内容以内容宽撑轨道。修复：`min-width:0`+`overflow-wrap:anywhere`；`img,video,pre{max-width:100%}`；table 包滚动容器。

**坑点 C：断点方向混用覆盖错乱（[LC-9]）**：min/max 双向混写+源顺序不统一。修复：统一 min-width，断点只增不改。

### 速查表

| 症状 | 根因 | 修复 |
|---|---|---|
| 相邻垂直 margin 取大值不相加 | 块级 margin 折叠 | 单向 margin 或容器 gap |
| gap 行列与意图相反 | `gap:24px 16px`=row column | 显式 row-gap/column-gap |
| gap 与 margin 同关系双倍间距 | 两者混用 | 同一关系只用一种 |
| 卡片群与母栅格错位、间距翻倍 | 嵌套同值 gap 叠加 | 层级递减；subgrid |
| 767→768px 布局巨变 | 断点抄设备不按内容 | 按最小可读宽推降列断点 |
| AntD 项目出现 Tailwind 断点 | 跨框架断点串扰 | 每项目锁定一套断点表 |
| 移动端地址栏收展时裁内容 | 100vh 按最大视口算 | `min-height:100svh` 回退 |
| hero 小屏不满屏/大屏露一条 | `height:500px` 硬编码 | `min-height`+内容驱动 |
| 行高落刻度仍"看着不齐" | 行高非 4px 基线倍数 | 行高取 20/24/28/32/48px（场景 10） |
| 标签被看成上一组尾巴 | 全 16px 单值无层级 | 组间>控件间>控件内 2 倍递减 |
| 图标与文字 8px gap 视觉仍贴 | 包围盒等距≠光学等距 | 按形状 1~2px 补偿 |
| 垂直居中 logo"下沉" | 几何中心≠视觉中心 | translateY(-1~-4px) |
| 英文 justify 出现"河流" | 双端对齐无断词 | 左对齐或+`hyphens:auto` |
| text-align 居中 block 子元素无效 | 只影响行内内容 | 块级用 margin auto/place-items |
| `vertical-align:middle` 仍偏 1~2px | 只作用 inline/table 基线 | flex/grid 居中+光学校正 |
| 主按钮在花哨背景里找不到 | 与背景同色同饱和 | 全场唯一强调色+留白孤立 |
| 用户在 3 个蓝按钮间犹豫 | 每屏多个 primary | 一屏一 primary（[LC-4]） |
| 装饰光晕/渐变球引离 CTA | 指向元素放 Z 型终点 | 装饰避开动线终点 |
| 每屏 stagger 淡入卡住首屏 | 动画 0.3~0.5s × N | 首屏动画 ≤0.5s |
| 单手够不到主操作 | 关键操作在顶部 | 吸底操作栏+safe-area |
| KPI 卡无行动价值 | 只有数字无 delta | 数值+delta+标题+sparkline |
| 详情页滚两屏找不到购买按钮 | buy-box 不吸顶 | `position:sticky;top:顶栏高(56~64)+24` |
| sticky 被顶栏盖住一半 | top 没算顶栏高度 | top=顶栏高（56~64）+24 |
| 表单双列手机上仍两列 | 双列无塌陷 | 640px 下塌单列 |
| 无限滚动页脚永不可达 | 页脚无处安放 | 页脚移入弹层/抽屉 |
| 短内容页页脚悬半空 | 无 flex 沉底 | body 100dvh+main flex:1 |
| 每区块都有强调元素，第一眼不知看哪 | 多入口并列 | 每页唯一入口（场景 12） |
| Bento 区块看似乱排 | span 随机、卡数>8 | 大卡=高权重、卡数≤8（场景 13） |

## 参数速查表（API 速查）

### 间距刻度（8pt 体系）

| 刻度 px | 4 | 8 | 12 | 16 | 24 | 32 | 48 | 64 | 96 | 128 |
|---|---|---|---|---|---|---|---|---|---|---|
| Tailwind v3 | 1 | 2 | 3 | 4 | 6 | 8 | 12 | 16 | 24 | 32 |

禁止值：13/15/18/25 等刻度外值（6/10/14 亦非 4 的倍数）。

### 断点表（跨框架，防串扰——每项目锁定一套）

| 档位 | Tailwind v3 | Bootstrap 5 | AntD 5 |
|---|---|---|---|
| sm | 640 | 576 | 576 |
| md | 768 | 768 | 768 |
| lg | 1024 | 992 | 992 |
| xl | 1280 | 1200 | 1200 |
| xxl | 1536 | 1400 | 1600 |

（均为模型记忆值，待验证。）

### 栅格与容器参数

| 参数 | 推荐值 |
|---|---|
| 列数 | 12（span 只用 1/2/3/4/6/12） |
| 容器 max-width | 1140 / 1280px，`margin-inline:auto` |
| gutter（列间距） | 16~32px，随断点分档（[LC-30]） |
| auto-fill 下限 | 列表卡 ~280px / KPI 卡 ~220px（=最小可读宽） |
| 防溢出轨道 | `minmax(0,1fr)`（不用裸 `1fr`） |
| 页面安全边距 | 移动 16~24 / 平板 32~48 / 桌面由容器控制 |

### 布局尺寸锚点（经验值）

| 元素 | 推荐值 |
|---|---|
| 顶栏高 | 56~64px（sticky top 链条以此起算） |
| 侧边栏 | 展开 240~280 / 折叠 64~72px |
| 表格行高 | 舒适 48~56 / 紧凑 32~40px |
| 表单单列宽 | 480~640px 居中 |
| 正文 measure | 65~75ch（中文 30~40 字/行） |
| 图表容器高 | 280~360px 固定 |
| 区块间隙 | 桌面 96~128 / 移动 48~64px |
| 卡片 padding | 16~24px（营销 24~32 / 后台 12~16） |
| 触控目标 | ≥44×44pt（iOS）/ 48×48dp（Android） |
| z-index 阶梯 | sticky 1000 / dropdown 1100 / overlay 1200 / modal 1300 / toast 1400 |

### Apple 平台布局锚点（HIG，R34）

| 平台 | 关键约束 |
|---|---|
| tvOS | 安全区上下 60pt/左右 80pt；网格水平间距 40pt、最小垂直间距 100pt；列宽 2~9 列 860→160pt 递减 |
| visionOS | 按钮中心间距 ≥60pt（≥60pt 按钮周围加 4pt padding 防 hover 重叠） |
| watchOS | 每行 ≤2~3 个控件；文本按钮占满全宽 |
| macOS | 控件/关键信息避免窗口底部；内容避开顶部摄像头区域 |

来源: [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/layout)；完整平台规格矩阵见 style-design-system kb 表 C（中央锚点）。

### CSS 属性易错点（其余见上坑点速查）

`place-items:center` 几何居中需 1~2px 光学修正（场景 8）；`@container` 组件级响应式（`container-type:inline-size`+cqw/cqi）；`env(safe-area-inset-bottom)` 吸底栏配 viewport-fit=cover（待验证）。

## 版本注意

以下为模型记忆，**未经文档验证**（HIG layout 锚点条目 [LC-33]~[LC-36] 除外，R34 已验证）：

- **浏览器特性**（待验证，作增强非依赖）：svh/dvh/lvh（iOS 15.4+，配 @supports 回退）；subgrid；flex gap；@container+cqw/cqi——支持矩阵以 caniuse 核对。
- **Tailwind v3→v4**：v3 断点与 0.25rem=4px 基较稳；v4 沿用与否、`space-x` 是否仍 margin 实现待验证。
- **其他**：`text-wrap:balance`/`overflow-wrap:anywhere`/祖先 transform 陷阱/fixed 定位/iOS 聚焦缩放——待验证；表单字号 ≥16px。
- **WCAG 2.2**（2.5.8 24px）已由 UA kb spec 语料锚定；HIG 44pt 已锚定（[LC-15]）；Material 48dp 仍待验证。

## 与其他子领域的集成要点

- **visual-perception**：[LC-2][LC-3] 感知根据是格式塔接近性/共同区域。
- **typography**：[LC-8] 行长——栏宽本 kb 定，行内可读性彼处定；场景 10/[LC-27] 是交界面。
- **usability-accessibility**：[LC-15][LC-17][LC-20] 合规口径以该 kb 为准；WCAG 1.4.10 Reflow（320px 单列不横滚）是 [LC-9][LC-12] 验收标准。
- **style-design-system**：Apple 平台规格（size class/安全区/控件尺寸）集中该 kb 表 A~C，本文件 [LC-33]~[LC-36] 与之同源，数值以该表为中央锚点。

## 来源索引

**文档锚点（R34 新增，白名单 Apple HIG）**：

- https://developer.apple.com/design/Human-Interface-Guidelines/layout — 布局决策依据（size class）、safe area/layout guide、tvOS 安全区与网格数值、visionOS/watchOS/macOS 布局约束、适配性清单 → corpus/ui-ux-design/style-design-system/docs/hig/layout.md（物理存于 style-design-system 域，跨域引用注明见 corpus/ui-ux-design/style-design-system/docs/_fetch_log_r34-hig.md）→ [LC-33]~[LC-36]、参数速查表。

**Material 仍降级**：种子 m3.material.io 为 JS 渲染无法抓取（[抓取记录](corpus/ui-ux-design/layout-composition/docs/_fetch_log.md)），Material 侧知识仍为 [模型经验]，无 [官方文档] 与 URL。

模型萃取来源（均为 [模型经验]，corpus 前缀 `corpus/ui-ux-design/layout-composition/elicited/`，条款尾括号数字对应文件）：01-grid-system（栅格/断点/vh/基线）、02-spacing-whitespace（8pt 刻度/留白/margin 折叠）、03-alignment-proportion（对齐轴/视觉中心/比例）、04-page-layouts（六类版式骨架）、05-visual-flow（视觉流/CTA/拇指区）、06-ai-mistakes（AI 布局 18 型）、07-laws（LC-1~20 基础）、08-grid-systems-deep（栅格类型/12 列数学/框架对照，LC-21~32）、09-visual-flow-deep（视觉重量/动线）、10-modern-layouts（Bento/密度分级）、11-responsive-media（srcset/sizes、格式链、加载策略、alt 分级）、12-chart-selection（意图→图型/y 轴纪律/图表交互/a11y fallback）。

数值置信度分层：Tailwind v3 刻度/断点、CSS 机制类（margin 折叠、min-width:auto、vh 行为）=较高；Bootstrap/AntD 断点、触控目标 44/48、光学补偿=中（待验证）；黄金比、Z/F 型动线效力=低（参考而非法则）；Bento/极简风、密度档数值=社区经验。

## 冲突消解记录

| # | 模型原认知 | 文档事实（HIG layout，R34） | 采用结论 |
|---|---|---|---|
| 1 | [LC-9] 断点按内容重排为 Web 侧经验 | 布局决策依据 size class 而非设备类型/方向；size class 变化功能不变、可见功能量可变 | 同构原则；平台侧新增 [LC-33] 携官方锚点 |
| 2 | [LC-15] 44×44pt 标注「下限待验证」 | HIG（经 style-design-system kb [SD-33] 锚定）：命中 ≥44×44pt（visionOS 60×60） | 撤销「待验证」；Android 48dp 仍待验证 |
| 3 | [LC-14] 全屏区块 min-height+svh 为 Web 侧防御 | safe area：内容避开 Dynamic Island/状态栏/toolbar/tab bar；tvOS 60/80pt | 平台侧新增 [LC-34]；Web 侧原判不变 |

其余 Web 侧待验证优先级维持：框架断点/容器宽/gutter 数值（v3/v4、Bootstrap 5、AntD 5、M3）> svh/subgrid/@container 支持矩阵 > Material 48dp > `space-x`/`text-wrap:balance` > 表单标签眼动/拇指研究、Gutenberg/F 型动线证据（只影响溯源强度）。
