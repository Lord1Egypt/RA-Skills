---
domain: ui-ux-design
skill_name: ui-ux-design-expert
subdomain: typography
title: 字体排印（Typography）
version: 4
updated: 2026-11-16
source_index: 模型萃取 corpus/ui-ux-design/typography/elicited/01~10；HIG typography 锚点 corpus/ui-ux-design/style-design-system/docs/hig/typography.md（跨域语料，R34 实抓）
knowledge_ratio: 法则 ~15% / 最佳实践 ~45% / 坑点 ~40%
merged_at: 2026-11-16
---
# 字体排印（Typography）

## 定位与心智模型

回答「文字如何呈现才易读且有层次」——用户先读内容，后看装饰。六条主线：①字体选择与栈（逐字符匹配回退链）；②字阶与行高（层次由字号×字重×颜色承担，非字体数量）；③可读性（行长/行高/对比度；readability ≠ legibility）；④加载性能（webfont 渲染关键资源；FOUT/FOIT/CLS）；⑤中文排印工艺（禁则/字距/全半角独立规则，西文经验不可迁移）；⑥流体与可变字体（clamp 连续缩放、单文件多轴）。颜色见 visual-perception，布局见 layout-composition，无障碍见 usability-accessibility。溯源 [模型经验] 01~09 见来源索引。

## 法则

[TY-1] **MUST**: 每个 `@font-face` 必须显式设置 `font-display`（正文 `swap`/`fallback`，非关键 `optional`）。违反→弱网 FOIT 文字隐形数秒，Lighthouse 报 `Ensure text remains visible during webfont load`。溯源: [模型经验] 04（AI 高频遗漏）

[TY-2] **MUST**: `font-family` 栈必须以通用族（sans-serif/serif/monospace）结尾。违反→字体全缺失时静默回落浏览器默认衬线体，无报错。溯源: [模型经验] 01

[TY-3] **MUST**: 中西文混排字体栈必须西文字体在中文字体之前。违反→拉丁字符与数字命中中文字体的西文字形，字形发闷、宽度异常。溯源: [模型经验] 01（中西混排第一坑）

[TY-4] **MUST**: 全局正文 `line-height` 必须用无单位数值（如 `1.5`），禁止 body/容器上 px/em/%。违反→终值被继承给不同字号子元素，行距过紧或重叠。溯源: [模型经验] 02

[TY-5] **MUST**: 字号 ≥24px 的标题必须显式收紧行高（1.05~1.25），不得继承正文行高。违反→多行标题空隙过大、占高失控。溯源: [模型经验] 02（AI 高频遗漏）

[TY-6] **MUST**: 长文正文容器必须有行长上限（西文 ≤75ch、中文 ≤40 字级别），禁止占满宽容器。违反→每行 100+ 字符，扫读丢行。溯源: [模型经验] 02

[TY-7] **MUST**: 会变化的数字（计时器、价格、表格数值列）必须启用 `font-variant-numeric: tabular-nums`。违反→比例宽数字逐位抖动，列宽跳动。溯源: [模型经验] 03（AI 高频遗漏）

[TY-8] **NEVER**: 中文文本禁止正 `letter-spacing`（允许 `0`）。违反→方块字节奏撕裂（「设 计 系 统」感），标点后双空隙。溯源: [模型经验] 05（AI 高频残留）

[TY-9] **NEVER**: 禁止 `word-break: break-all` 作中文容器换行默认；中文换行用 `line-break: strict`+`overflow-wrap: break-word`。违反→英文单词/数字串被拦腰斩断，禁则被破坏。溯源: [模型经验] 05（AI 高频误用）

[TY-10] **NEVER**: 禁止用 `line-height` 撑 UI 控件（按钮/标签）高度；用 `height`/`min-height`+flex 居中。违反→换行或加图标后错位溢出。溯源: [模型经验] 02

[TY-11] **NEVER**: `text-overflow: ellipsis` 禁止单独出现，必须与 `white-space: nowrap`+`overflow: hidden` 同时声明。违反→三件套缺一即不生效。溯源: [模型经验] 06

[TY-12] **MUST**: 单页可见字族数 ≤2（正文族+至多 1 个标题/display 族）；层次由字阶/字重/颜色承担。违反→字体「声音」打架、加载成本升。溯源: [模型经验] 01

[TY-13] **NEVER**: 禁止只写 `font-family` 名称引用未加载字体——必须提供 `@font-face` 来源或可用回退链。违反→生产环境静默缺失。溯源: [模型经验] 01（AI 高频错误）

[TY-14] **MUST**: CJK 字体必须子集化或按 `unicode-range` 分包后上线；禁止整包（数 MB）加载。违反→中文站首屏 >10s。溯源: [模型经验] 04

[TY-15] **MUST**: `<html>` 必须声明正确的 `lang`（`hyphens: auto` 硬前提）。违反→hyphens 失效；损害读屏与翻译。溯源: [模型经验] 03

[TY-16] **MUST**: 正文对比度满足 WCAG AA（正文 ≥4.5:1、大字 ≥3:1）；`#999` 级灰色禁止用于正文。违反→无障碍审计失败。溯源: [模型经验] 03

[TY-17] **MUST**: 字阶必须由固定基准+固定比率（1.125~1.333）推导；相邻级差可感知（≥约 8% 或 ≥2px）。违反→字号无规律或相邻层级无差。溯源: [模型经验] 02

[TY-18] **NEVER**: `text-wrap: balance` 禁止用于长正文；仅用于 ≤6 行短文本（标题、按钮、卡片标题）。违反→长文本计算代价高且效果反直觉。溯源: [模型经验] 05

[TY-19] **NEVER**: 屏幕正文禁止同时用 `text-indent` 与段落间距（二选一；屏幕惯例用段间距）。违反→段落边界信号冗余。溯源: [模型经验] 05

[TY-20] **MUST**: 用到的 `font-weight` 必须有对应加载的字重文件（或可变字体轴），禁止依赖浏览器合成加粗/斜体。违反→合成字重粘连发虚、伪斜体不可读。溯源: [模型经验] 01

[TY-21] **MUST**: 视口缩放字号必须 `clamp()` 三段齐全（min/max 用 rem，preferred=`calc(rem+vw)`）。违反→小屏跌破可读、超大屏炸版、用户字号设置失效（WCAG 1.4.4）。溯源: [模型经验] 08

[TY-22] **NEVER**: `html{font-size:62.5%}` 禁止入持久代码库（1rem=10px，rem 字面值失真）。违反→按 1rem=16px 假设的第三方组件错乱、浏览器最小字号强制放大破版。溯源: [模型经验] 08

[TY-23] **MUST**: 流体字号仅限标题/display 层且两端点等于字阶 token；正文与 UI 控件用断点阶梯。违反→正文无感漂移、控件溢出、断点处字号跳变。溯源: [模型经验] 08

[TY-24] **MUST**: 可变字体 `@font-face` 必须声明轴区间（`font-weight:400 700`）；标准轴用高层属性驱动，`font-variation-settings` 仅限自定义轴。违反→按单字重匹配、层级退化合成加粗、级联断裂。溯源: [模型经验] 09

[TY-25] **MUST**: swap/fallback 的 webfont 必须为回退字体配 `size-adjust`+`ascent/descent/line-gap-override`，数值按「字体对」用工具计算。违反→swap 瞬间 CLS 飙升。溯源: [模型经验] 09

[TY-26] **MUST**: 按 `unicode-range` 分包时每个 `@font-face` 必须带对应描述符。违反→分包形同虚设，浏览器全量下载。溯源: [模型经验] 09

[TY-27] **MUST**: Apple 平台字号不得低于平台最小值（iOS/iPadOS 11pt、macOS 10pt、tvOS 23pt、visionOS 12pt、watchOS 12pt）；正文默认 iOS/visionOS 17pt、macOS 13pt、tvOS 29pt、watchOS 16pt；细字重自定义字体应大于推荐字号以保证可读性。溯源: [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/typography)

[TY-28] **NEVER**: 一般避免细字重（Ultralight/Thin/Light），系统字体优先 Regular/Medium/Semibold/Bold；层级用字重、字号、颜色传达，尽量少的字族数量。溯源: [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/typography)

[TY-29] **MUST**: 三行以上文本避免 tight leading；宽列/长文用 loose leading。分界=[TY-5]：大字号短标题（≤3 行）可收 1.05~1.25，三行以上正文禁收紧。溯源: [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/typography)

[TY-30] **MUST**: Apple 平台文字规格必须用 Text Styles（body/headline/title 等=字重+字号+行距组合）而非散值字号，随 Dynamic Type 与辅助功能缩放联动（iOS Large 档 body 17/22pt → AX5 53/62pt）；macOS 不支持 Dynamic Type，用 controlContentFont/labelFont/menuFont 等动态系统字体变体；大字号下布局联动（横向相邻改纵向堆叠、减少列数、最小化截断、放大界面图标）。溯源: [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/typography)

[TY-31] **MUST**: 使用 SF 系统字族（SF Pro/SF Compact/New York）时字距由系统按字号自动施加（SF Pro 12pt=0、17pt=−26/1000em、80pt+ 归 0），禁手动重设字距覆盖光学排印；自定义字体须自行复现 tracking 曲线，否则 12~23pt 段字形发松。溯源: [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/typography)

### 全局法则候选（[GLOBAL]，供 laws.md 合并）

[GLOBAL][TY-G1] **MUST**: 引用外部资源前必须确认运行环境可用性，不可仅凭「知识中存在该资源名」引用（字体、API、npm 包同理）。违反→生产静默缺失/回退且无报错。溯源: [模型经验] 07（TY-13 升维）

[GLOBAL][TY-G2] **MUST**: 「知识上明确、生成时易省略」的必需配置项必须以 checklist/lint 强制（font-display、回退栈、截断三件套）。违反→demo 不可见的缺陷在审计/弱网/真实数据下爆发。溯源: [模型经验] 06

[GLOBAL][TY-G3] **MUST**: 静态演示数据会掩盖的动态缺陷（数值变化、空态、极端长度）必须在实现时主动预判。违反→接入真实数据后抖动/溢出/换行错乱。溯源: [模型经验] 07

[GLOBAL][TY-G4] **NEVER**: 默认审美/模板惯性不得覆盖目标场景规范——为特定语言/文化/平台生成时必须先做场景适配审查。违反→模板残留（中文加字距、屏幕用印刷缩进等）。溯源: [模型经验] 07

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| font-family 栈 | 逐字符匹配回退链；末尾必须是通用族 |
| type scale | 基准字号 × 固定比率推导的字号序列 |
| 行高单位机制 | 无单位按比例继承；%/em/px 父级先算终值再继承 |
| FOUT / FOIT | 回退先显示后替换（闪动）/ 加载期文字隐形 |
| 禁则（kinsoku） | 行首禁标点、行尾禁开括号的 CJK 换行规则 |
| CLS（布局偏移） | swap 时回退与目标字体度量差异引起的跳动 |

## 最佳实践

### 场景 1：构建跨平台中文字体栈

路径: 先定西文字体（拉丁与数字由它渲染）→ 按平台列中文（macOS/iOS `PingFang SC`→Windows `Microsoft YaHei`→Android `Noto Sans SC`）→ 通用族收尾 → 实测回退。
- don't: `font-family:"PingFang SC","Helvetica Neue"`（中文在前+无通用族）。
- do: `font-family:"Helvetica Neue",-apple-system,"PingFang SC","Microsoft YaHei","Noto Sans SC",sans-serif`。
边界: UI 产品优先 `system-ui` 栈（零下载）: `system-ui,-apple-system,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif`；Linux 映射不可假设；品牌中文需 webfont+子集化（场景 6）。搭配: 强对比或同族不同字重，二选一。源于 [TY-2][TY-3]；溯源: [模型经验] 01

### 场景 2：搭建字阶（type scale）体系

路径: 定基准 `--fs-base:16px`（移动长文可 17~18px）→ 定比率（内容型 1.125~1.2、营销页 1.25~1.333）→ 推导 token（字号 token ≤8、行高 ≤4 档）→ 校验相邻级差 ≥2px 或 ≥8%，不可感知则删级。
- don't: 内容产品用黄金比（第五级 unusable）；`15/16/17px` 三级级差不可感。
- do: `--fs-base:16px; --ratio:1.2`（16/19/23/28/34/41）；级差可感: 14/16/18/20/24/30px。
边界: 海报/大标题可用大比率（1.414~1.618，层级仅 2~3 级）；rem 字阶被用户根字号覆盖属预期。源于 [TY-17]；溯源: [模型经验] 02

### 场景 3：行高分层设置（正文/标题/UI 控件）

路径: body 只写无单位行高（阈值见参数速查表）→ 标题（≥24px）显式覆盖 1.05~1.25（字号越大系数越小）→ UI 控件单行文字行高 1，高度交 `min-height`+flex。
- don't: `body{font-size:16px;line-height:150%} h2{font-size:32px}`——h2 继承 24px 行高（%先算终值）→重叠。
- do: `body{font-size:16px;line-height:1.5} h1{font-size:48px;line-height:1.1} h2{font-size:32px;line-height:1.2} .zh-body{line-height:1.7}`。
边界: 「统一全局行高」是错觉，必须分层；中文行高高于西文（方块字无缓冲，1.3 以下窒息）；框架 reset 可能默认 1.1~1.15，逐段检查多行文本。源于 [TY-4][TY-5]；溯源: [模型经验] 02

### 场景 4：行长控制（measure）

路径: 正文容器 `max-width` 用 `ch`（阈值见参数速查表）→ 中文不适用 `ch`（0 字符宽≠汉字宽），用 `em` → 响应式断点同时调字号、行高、行长。
- don't: `.prose{max-width:1200px}` 每行 100+ 字符。
- do: `.prose{max-width:70ch;margin-inline:auto;padding-inline:1rem} .zh-prose{max-width:35em;margin-inline:auto}`。
边界: 表格/仪表盘等非连续阅读场景不受限；移动端西文靠容器宽度自然达成。源于 [TY-6]；溯源: [模型经验] 02

### 场景 5：Web 字体加载策略

路径: `@font-face` 完整声明（family+src woff2 优先+weight+style+`font-display`）→ 正文 `swap`、非品牌必需且 CLS 敏感 `optional`、关键 UI `fallback` → 首屏字体 preload（`as="font"`+`crossorigin`，同源也必须写）→ 回退度量对齐（`size-adjust` 系）压 CLS → 只加载用到字重，WOFF2 必备。
- don't: `@font-face{font-family:"Body";src:url(body.woff2)}` 无 font-display（弱网 FOIT 数秒）；`rel="preload" as="style"`（as 写错+缺 crossorigin→双请求）。
- do: `@font-face{font-family:"Body";src:url(body.woff2) format("woff2");font-weight:400 700;font-display:swap}`；`@font-face{font-family:"Inter-fallback";src:local("Arial");size-adjust:107%;ascent-override:90%;descent-override:22%;line-gap-override:0%}`（百分比用 fontaine/capsize 计算）。
边界: `optional` 超时后本会话不换；文字是 LCP 时字体策略直接影响 LCP；preload 只给首屏 1~2 个；系统字体够用不引 webfont。源于 [TY-1][TY-25]；溯源: [模型经验] 04、09

### 场景 6：中文字体子集化与分包

路径（三选一或组合）: ①静态子集——按内容裁剪（fonttools `pyftsubset`/fontmin/cn-font-split），适合固定文案，动态内容缺字回退宋体；②动态分包——`unicode-range` 按 Unicode 区块切小包，浏览器只下命中包（Google Fonts 中文即此）；③首屏关键子集内联+其余异步。
- do: `@font-face{font-family:"NotoSansSC";src:url(sc-001.woff2) format("woff2");unicode-range:U+4E00-4FFF}`（多个 @font-face 各管一个区块）。
边界: 汉字字形 2 万+（GB18030 更广），不子集化=为用不到的字形买单；分包须配长缓存（文件名哈希）。源于 [TY-14][TY-26]；溯源: [模型经验] 04、09

### 场景 7：数字排版（动态数值、表格、长数字）

路径: 会变的数字加 `tabular-nums`（表格、倒计时、价格）→ 数字列右对齐 → 长数字分组（`20261116-0001`、`1,234,567.89`；组块 4~7）→ 验证码/序列号用等宽字体（0/O、1/l 可区分）。
- don't: 比例宽数字，每次刷新列宽抖动。
- do: `.price{font-family:"Inter";font-variant-numeric:tabular-nums}`（低层等价 `font-feature-settings:"tnum"`）。
边界: 字体必须内建 tnum 特性（Inter 有；中文字体大多没有，需验证）；静态展示数字不强制。源于 [TY-7]；溯源: [模型经验] 03

### 场景 8：中文排印工艺（字距、禁则、孤寡行、全半角）

路径: 中文正文 `letter-spacing:0`（全大写英文短标签才加 0.05em~0.1em；大号西文标题微收 -0.01em~-0.03em）→ 换行 `line-break:strict`+`overflow-wrap:break-word` → 中西文空隙渲染层自动化（pangu）→ 屏幕正文段间距无 `text-indent` 二选一 → 孤寡行: 短文本 `text-wrap:balance`、长正文 `text-wrap:pretty` → 文案层: 破折号「——」、省略号「……」、全角标点、弯引号。
- don't: `.zh-body{letter-spacing:0.02em}`（西文模板残留）；`.zh-container{word-break:break-all}`（破坏禁则）。
- do: `.zh-body{letter-spacing:0} .zh-container{line-break:strict;overflow-wrap:break-word}`；段落信号二选一: `p{margin-bottom:1em}` 或 `p.book{text-indent:2em;margin:0}`。
边界: `text-autospace` 草案，用渲染层工具；`hanging-punctuation` 记忆仅 Safari 部分支持；EPUB 等 print 场景 `orphans`/`widows` 有效且必要。源于 [TY-8][TY-9][TY-18][TY-19]；溯源: [模型经验] 05

### 场景 9：强调与对比度层级

路径: 字重两级——正文 400/强调 600~700 → 段内 bold ≤10%，次级强调用颜色 `#595959` 或 500 字重，警示用背景色 → 灰阶分层（比值见参数速查表）: `#333`→`#595959`→`#8c8c8c` → 中文强调用加粗或着重号（`text-emphasis:dot`，支持度待验证）不用斜体 → 非链接文本不用下划线。
- don't: `p{color:#999}`（on #fff ≈2.85:1，AA 不达标）；`em{font-style:italic}`（中文伪斜体）。
- do: `p{color:#333} .secondary{color:#595959} em{font-style:normal;font-weight:600}`。
边界: 低对比只可用于「可忽略的辅助信息」（placeholder `#aaa` 12px 属不达标）；「全强调=无强调」。源于 [TY-16][TY-20]；溯源: [模型经验] 03

### 场景 10：流体字阶（clamp 公式速查）

路径: 先有静态 token（场景 2）→ 定两端视口（常用 320/1280px）→ vw 系数=100×(F2−F1)/(V2−V1)、rem 截距=(F1−V1×系数/100)/16 → 仅套用于标题/display token（命名带 fluid 后缀）→ 行高无单位联动 → DevTools 校验两端命中 token。
- 速查（root 16px，320→1280，系数=(大−小)/9.6）: 16→20px ⇒ `clamp(1rem,.9167rem+.4167vw,1.25rem)`；32→48px ⇒ `clamp(2rem,1.3333rem+2.0833vw,3rem)`。
- don't: `font-size:5vw`（无界裸奔）；`clamp(16px,2vw,24px)`（px 边界切断用户字号）；全站滥用（正文流体是负收益）。
边界: 正文/UI 控件走断点阶梯；vw 与 rem 相加必须 calc() 包裹；横竖屏双体验标题才评估 vmin。源于 [TY-21][TY-23]；溯源: [模型经验] 08

### 场景 11：可变字体落地参数

路径: 确认 3+ 字重或多轴需求 → 取轴区间子集（Google Fonts `wght@400..700`；自托管 fonttools instancer 裁轴）→ `@font-face{font-family:"InterV";src:url(inter.woff2) format("woff2");font-weight:100 900;font-display:swap}` → preload ≤1~2 个（crossorigin 必写；href 与 src 一致）+ 回退度量对齐（场景 5）→ 高层属性驱动: `font-weight:620` 连续值直出；自定义轴才 `font-variation-settings:"GRAD" -50`。
- don't: 2 字重引全轴文件；用 font-variation-settings 写 wght（绕过级联）；`format("woff2-variations")` 旧语法（新 Chrome 已移除）。
边界: 旧内核静默回退 Regular，需评估静态字重回退包；CJK 可变字体巨大（10MB 级），先分包（场景 6）再谈轴；微交互动画需 `@property` 注册才可插值（待验证）。源于 [TY-24]；溯源: [模型经验] 09

### 场景 12：打印样式（@media print）

路径: 白名单只显内容区（隐导航/侧栏/广告/交互控件）→ ink 安全: `body{background:#fff;color:#000}`，logo/条码才 `print-color-adjust:exact` → 外链显化 `a::after{content:" ("attr(href)")"}` → 分页防护: 卡片/表格行 `break-inside:avoid`、`orphans:3;widows:3`、thead `table-header-group` 跨页重复表头 → `beforeprint` 展开折叠/放开滚动容器（打印只渲染非滚动流）→ 正文 11~12pt+`@page{margin:2cm}`。
- don't: 屏幕样式直印——导航广告全上纸、深底白字白纸上消失、fixed/sticky 行为不一致（打印前转 static）。
边界: web 字体打印回退系统栈；`@page` 页码 counters 浏览器支持有限（待验证）；复杂套打走服务端 PDF。源于 [TY-G4]；溯源: [模型经验] 10

### 场景 13：Apple 平台原生字阶选档（Text Styles）

路径: 选 Text Style（large title/title 1~3/headline/body/callout/subhead/footnote/caption 1~2）而非散值字号 → 按平台取默认档（iOS Large 档 body 17/22、headline 17/22 Semibold；macOS body 13/16；tvOS body 29/36；watchOS 随表径 38→49mm body 15~17）→ 层级用更高档 Style 或 emphasized weight（2025-12-16 加入规格：medium/semibold/bold/heavy）表达，不另起散值字号 → 大字号/AX 档联动布局改纵向堆叠（[TY-30]）。
- do: iOS 正文用 `preferredFont(forTextStyle: .body)` 随 Dynamic Type 联动；强调用 emphasized 变体。
- don't: 硬编码 17pt 散值（不随用户缩放，[TY-27][TY-30]）；把 caption 档拉来当正文（跌破平台可读基线）。
- 边界: 完整 Dynamic Type 字阶/tracking 表见 style-design-system kb 参数速查表 D（中央平台锚点）；Web 侧对应物是 rem 字阶+用户缩放（[TY-21][TY-22]），两域互不混用。源于 [TY-27][TY-28][TY-30][TY-31]；溯源: [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/typography)

## 高频坑点（速查）

### 深度展开 Top 3

1. **line-height 单位继承陷阱**（[TY-4]）: `%` 父级先算终值（16×150%=24px）再继承给 32px h2 → 过紧/重叠；无单位按比例继承。修复: body 无单位 `1.5`，标题 1.2。场景 3。
2. **@font-face 忘 font-display → FOIT**（[TY-1]）: 弱网正文空白数秒；缺省默认偏 FOIT（block ~3s），「知识存在但生成时省略」（[TY-G2]）。修复: `font-display:swap`。场景 5。
3. **中文字体栈顺序写反**（[TY-3]）: 拉丁字符命中中文字体西文字形 → 发闷、宽度异常。修复: 西文在前。场景 1。

### 坑点速查表

| 症状 | 根因 | 修复 |
|---|---|---|
| 多行正文行间贴合 | 框架 reset 默认 `line-height:1.1` | 正文显式 1.5~1.6（中文 1.5~1.8） |
| 标题两行空隙巨大 | 大字号继承正文行高系数 | 标题显式 1.05~1.25 [TY-5] |
| 每行 120+ 字符丢行 | 正文占满宽容器 | `max-width:70ch`（中文 ~35em）[TY-6] |
| `font-weight:600` 笔画粘连发虚 | 无该字重文件，合成加粗 | 加载字重文件或可变字体 [TY-20] |
| 页面「说不出哪里怪」 | 两款相似字体搭配 | 强对比或同族不同字重，二选一 |
| 按钮换行/加图标错位 | `line-height` 撑按钮高度 | `min-height`+flex 居中 [TY-10] |
| 长文本不截断溢出 | `ellipsis` 单独出现 | 补 `nowrap`+`hidden`+`ellipsis` [TY-11] |
| 窄栏 justify 词间巨隙 | 窄列无伸缩空间 | 窄列不 justify；宽栏 `hyphens:auto`+`lang` [TY-15] |
| preload 字体双请求 | 缺 `crossorigin`（同源也必须） | 补 `crossorigin`+`as="font"` |
| swap 瞬间 CLS 飙升 | 回退与 webfont 度量差异 | `size-adjust` 系对齐回退 [TY-25] |
| 中文字体全量首屏 >10s | 未子集化/未分包 | 子集化+`unicode-range` 分包 [TY-14] |
| 只需 400/700 却比静态重 | 可变字体多轴全量加载 | 3+ 字重才用可变；或子集轴范围 |
| 中文段落「采用Flexbox布局」贴死 | 中西文间无 1/4 em 空隙 | pangu 类工具；`text-autospace` 待支持 |
| 中文行首出现逗号句号 | 禁则缺失/`break-all` 破坏 | `line-break:strict`，弃 `break-all` [TY-9] |
| 段末孤字悬栏底 | `orphans`/`widows` 仅 print/multicol | 短文本 `balance`；长文 `pretty` |
| 满页 bold 重点消失 | 强调单一过载 | bold ≤10%，次级颜色/500 字重 |
| 字号 15/16/17 三级无差 | 级差低于感知阈值（~8%/2px） | 拉大级差，删冗余级 [TY-17] |
| `optional` 字体「永远不显示」 | 语义误解: 超时后本会话不再 swap | 属预期；品牌标题改 `swap`/`fallback` |
| 屏幕段落缩进+段距双信号 | 印刷惯例混入屏幕 | 二选一，屏幕用段距 [TY-19] |
| 用户调大浏览器字号无效/组件错乱 | `html{font-size:62.5%}` rem 语义失真 | root 100%，构建期 px→rem [TY-22] |
| 小屏跌破可读/4K 标题炸版 | clamp 缺段或 `5vw` 无界 | 三段 `clamp(1rem,.9167rem+.4167vw,1.25rem)` [TY-21] |
| 分包后仍全量下载 | 分包声明漏 `unicode-range` | 每个声明补对应区块 [TY-26] |
| 旧内核可变字体只见 Regular | variations 不支持，回退默认实例 | 静态字重回退包；声明轴区间 [TY-24] |

## 参数速查表（API 速查）

### Apple 平台字号下限（HIG）

| 平台 | 默认正文 | 最小字号 |
|---|---|---|
| iOS/iPadOS | 17pt | 11pt |
| macOS | 13pt | 10pt |
| tvOS | 29pt | 23pt |
| visionOS | 17pt | 12pt |
| watchOS | 16pt | 12pt |

来源: [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/typography)；完整 Dynamic Type/Tracking 表见 style-design-system kb 表 D。

### 字阶比率表

| 比率 | 名称 | 适用场景 |
|---|---|---|
| 1.125 | major second | 内容密集（后台、文档） |
| 1.2 | minor third | 通用 Web（产品 UI 默认） |
| 1.25 | major third | 内容型站点 |
| 1.333 | perfect fourth | 营销页 / Landing |
| 1.414 / 1.5 / 1.618 | — | 海报、大标题；产品界面慎用（第五级起 unusable） |

### 行高与行长阈值

| 维度 | 阈值 |
|---|---|
| 行高·西文正文 | 1.4~1.6 |
| 行高·中文正文 | 1.5~1.8（方块字无缓冲） |
| 行高·标题（≥24px） | 1.05~1.25（字号越大越小） |
| 行高·UI 控件单行 | 1（配合 min-height） |
| 行长·西文 | 45~75 字符（理想 ~66）→ `max-width:70ch` |
| 行长·中文 | 25~40 字（理想 ~35）→ `35em`（`ch` 不适用: 0 字符宽≠汉字宽） |
| 行长·移动端西文 | 30~50 字符（靠容器宽度自然达成） |

### font-display 值语义

- `auto`＝浏览器默认（≈block）；`block`＝FOIT: 隐形 ≤3s，到货即换（基本不用）
- `swap`＝极短隐形+无限交换（FOUT）→ 正文；`fallback`＝~100ms 隐形+~3s 交换窗口，错过不换 → 关键 UI
- `optional`＝~100ms 隐形，超时本会话用回退（缓存供下次）；防抖动 → 非品牌必需、CLS 敏感
- 超时数值（3s/~100ms）为模型记忆值，未验证

### 字重与对比度层级

| 用途 | 值 |
|---|---|
| 字重 | 400 正文 / 500 次强调、按钮 / 600~700 标题；层级间隔 ≥100；300 vs 400 几乎无差、慎用于小字号 |
| 对比度 | 正文 ≥4.5:1；大字（≥24px 或 ≥18.66px bold）≥3:1 |
| 灰阶分层 | `#333` 正文（~12.6:1）→ `#595959` 次要（~7:1）→ `#8c8c8c` 提示（仅大字/非必要信息） |

### font/text CSS 属性速查

| 属性 | 作用 | 易错点 |
|---|---|---|
| `line-height` | 行盒高度 | body 用无单位；%/em/px 算后继承 [TY-4] |
| `letter-spacing` | 字距 | 中文禁正值 [TY-8]；body 上扩散到标点数字 |
| `word-spacing` | 词距 | 中文无效（无词间空格） |
| `font-variant-numeric` | 数字形制 | 高层属性优先；字体须内建特性 |
| `font-feature-settings` | OpenType 底层（"tnum"） | 低层等价；级联覆盖待验证 |
| `font-variation-settings` | 可变字体底层轴 | 仅限自定义轴；不参与高层级联 [TY-24] |
| `clamp()` | 流体字号载体 | 三段齐全；px 边界切断用户字号 [TY-21] |
| `text-wrap:balance`/`pretty` | 平衡断行/优化孤行 | balance 仅 ≤6 行 [TY-18]；pretty 待验证 |
| `hyphens:auto` | 西文断字 | 依赖 `<html lang>` [TY-15] |
| `orphans`/`widows` | 孤寡行 | **仅 print/multicol 生效** |
| `text-overflow:ellipsis` | 单行截断 | 三件套缺一不可 [TY-11] |
| `word-break` | 断字模式 | `break-all` 禁作中文默认 [TY-9] |
| `overflow-wrap:break-word` | 长串兜底 | 中文正确兜底（替代 break-all） |
| `line-break:strict` | CJK 禁则 | 中文容器推荐 |
| `text-autospace`/`hanging-punctuation`/`text-emphasis` | 空隙/标点悬挂/着重号 | 草案/部分支持/待验证，查 caniuse |
| `size-adjust`/`ascent-override` 等 | 回退度量对齐 | 须工具计算（fontaine/capsize）[TY-25] |

## 版本注意

以下为模型记忆，未经文档验证（[TY-27]~[TY-31] 已由 R34 HIG 语料锚定者除外）。

- **Apple HIG typography（R34 已锚定）**: 平台字号下限/细字重规避/leading 纪律/Text Styles/SF tracking 见 [TY-27]~[TY-31] 与场景 13；强调字重 2025-12-16 加入规格；SF 为可变字体格式，支持动态光学尺寸与字重插值。来源: [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/typography)
- **可变字体**: 3+ 字重才划算；Google Fonts 轴子集 `wght@400..700`；`format("woff2-variations")` 已废，现写 `format("woff2")`（`tech(variations)` 待验证）。
- **clamp()/流体**: 2020 起全主流基线；容器查询单位（cqw/cqi）待验证。
- **中文 webfont 生态**: 动态分包主流（Google Fonts 中文、cn-font-split 按 `unicode-range` 切包）；粒度无定论。
- **新 CSS 演进**: `text-wrap:balance/pretty`、`lh`——用前必查 caniuse（完整清单见参数速查表）。
- **浏览器默认行为**: 无 `font-display` 默认策略、`hyphens:auto` 范围、Chrome「最小字号」与 rem 交互可能已变化。
- **Tailwind token**: v3/v4 数值可能不同（`leading-relaxed`≈1.625 不确定）；语义类比更抗漂移。
- **平台字体栈漂移**: Windows/macOS/移动 OS 默认字体随版本演进；Lighthouse 规则同步变化。

## 与其他子领域的集成要点

- **layout-composition**: 行长阈值（70ch/35em）决定正文栏宽与 grid content 列（[TY-6] 下游）；截断三件套（[TY-11]）配合 flex/grid 溢出处理（`min-width:0`）。
- **visual-perception**: 行长上限根因是认知负荷（回扫定位行首）；级差阈值（≥8%）与对比度感知阈值源于知觉规律。
- **usability-accessibility**: WCAG 1.4.12 Text Spacing: 行高 ≥1.5×、字距 ≥0.12×、词距 ≥0.16×、段后 ≥2× 字号（模型记忆）；[TY-16]↔1.4.3、[TY-21][TY-22]↔1.4.4（用户字号缩放）、[TY-15] 服务读屏。
- **style-design-system**: Apple 平台完整字阶/tracking/规格集中在该 kb 参数速查表 A/D（中央平台锚点），本文件只留选档规则与字号下限（[TY-27][TY-30]）。
- **ai-mistakes 横切**: 本子领域 AI 典型错误汇入 `kb/ai-mistakes.md`；[GLOBAL] 候选 TY-G1~G4 汇入 `kb/laws.md`。

## 来源索引

**文档锚点（R34 新增，白名单 Apple HIG）**：

- https://developer.apple.com/design/Human-Interface-Guidelines/typography — 平台默认/最小字号、细字重规避、leading 纪律、Text Styles 定义、SF 字族与 tracking 全表、Dynamic Type 全档（含 macOS/tvOS/watchOS 字阶）→ corpus/ui-ux-design/style-design-system/docs/hig/typography.md（物理存于 style-design-system 域，跨域引用注明见 corpus/ui-ux-design/style-design-system/docs/_fetch_log_r34-hig.md）→ [TY-27]~[TY-31]、场景 13。

**Practical Typography 仍降级**：种子 https://practicaltypography.com 两次 Transport error（见 corpus/ui-ux-design/typography/docs/_fetch_log.md），Web 排印工艺部分仍为 [模型经验]。
- 模型萃取来源（corpus 路径见 frontmatter source_index）: 01-font-pairing（字体栈搭配）、02-type-scale（字阶/行高/行长）、03-readability（可读性/对比度/数字）、04-webfont-performance（加载/font-display/子集化）、05-typographic-craft（字距/禁则/孤寡行/全半角）、06-ai-mistakes、07-laws、08-fluid-typography（流体/62.5%）、09-variable-fonts-perf（可变字体/度量对齐）、10-print-styles（打印样式）。
- 不确定度声明: 经验阈值类数值（感知阈值 ~8%、font-display 毫秒数、WCAG 1.4.12 倍数、clamp 版本）为设计共识/模型记忆；文档轮优先验证「版本注意」。

## 冲突消解记录

| # | 模型原认知 | 文档事实（HIG typography，R34） | 采用结论 |
|---|---|---|---|
| 1 | 正文行高 1.4~1.6 为经验阈值（[TY-4]） | 「三行以上文本避免 tight leading；宽列/长文用 loose leading」 | 一致；新增 [TY-29] 携官方锚点 |
| 2 | [TY-5] 标题收紧行高 1.05~1.25 与「避免 tight」存在表面张力 | HIG 限定「三行以上文本」 | 不冲突：分界=行数——大字号短标题（≤3 行）可收紧，三行以上正文禁收紧；写入 [TY-29] |
| 3 | 字距经验：大号西文标题微收 −0.01~−0.03em（近似恒定比例） | SF 字族 tracking 随字号变化（12pt=0、17pt=−26/1000em、80pt+ 归 0），非恒定 | Apple 平台禁手动覆盖（[TY-31]）；Web/自定义字体保留经验值 |
| 4 | 平台字号无锚点（Web 视角缺省 16px） | HIG 平台默认/最小字号五平台分档 | 新增 [TY-27]；Web 侧 16px 基准不变（分域适用） |

Web 侧维持原判（HIG 不覆盖）：
- 机制类（line-height 继承、逐字符匹配、orphans/widows 条件、preload crossorigin）与深化轮机制类（clamp 三段、轴区间、unicode-range 描述符、62.5% rem 失真、variation-settings 级联断裂）: 收录为法则/实践。
- 数值类（font-display 超时、Tailwind token、感知阈值 ~8%、WCAG 1.4.12 倍数、流体换算、@property）: 收录并标注未验证/示意。
- 支持矩阵类（hanging-punctuation、text-autospace、text-wrap:pretty、hyphens:auto）: 按模型记忆收录，附「用前查 caniuse」。
- 冲突待登记: Chrome 默认 font-display 行为、`overflow-wrap:break-word` 与废弃 `word-break:break-word` 标准——按保守表述。
