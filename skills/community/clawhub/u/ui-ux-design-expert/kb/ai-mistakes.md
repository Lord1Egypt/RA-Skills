---
type: cross-cutting
name: ai-mistakes
domain: ui-ux-design
skill_name: ui-ux-design-expert
version: 1
updated: 2026-11-17
merged_at: 2026-11-16
---

# AI 生成 UI 的典型错误总集（横切蒸馏）

来源：7 个子领域（visual-perception / layout-composition / color-system / typography / style-design-system / interaction-motion / usability-accessibility）AI 错误自我质询萃取文件的合并去重。

分级标准：**致命**=违反全局法则或无障碍合规（WCAG）/直接破坏可用性；**严重**=显著损害视觉质量或一致性；**一般**=细节瑕疵。
统计：共 38 条 — 致命 12（AIM-1~12）/ 严重 24（AIM-13~33、36~38）/ 一般 2（AIM-34~35）。全文按「致命 → 严重 → 一般」序排列于下，各节标题含严重度。

---

## 致命

### [AIM-1] 焦点样式摘除（致命）
- 错误: `button:focus{outline:none}` / `focus:outline-none` 后不补替代焦点样式，Tab 导航焦点完全不可见，违反 WCAG 2.4.7。典型: outline 摘完就没下文。
- 纠正: 摘除前必须给替代 `:focus-visible{outline:2px solid #1a73e8;outline-offset:2px}`；祖先 `overflow:hidden` 会裁掉焦点环（外扩 outline 需留 padding 余量）。

### [AIM-2] 非语义交互元素与 mouse-only 组件（致命）
- 错误: `<div onClick>` 代替 button（无 role/焦点/Enter/Space 响应，读屏不知道是控件）；自定义下拉/标签页/菜单只实现 mouse 事件，键盘无法操作。「加了 aria-* 修补不了错误的元素选择」。
- 纠正: 原生元素优先（button/a/select/details）；确需自定义组件按 WAI-ARIA APG 补全键盘交互（Enter/Space/方向键/Home/End/ESC）+ `role` + aria 状态（`aria-expanded` 等）。

### [AIM-3] 模态可访问性四件套缺失（致命）
- 错误: 打开后焦点仍在背景、Tab 穿透到遮罩下、ESC 无效、关闭后焦点丢 body；drawer/模态打开不锁 body 滚动（背景跟着滚/滚动链）。
- 纠正: 四件套——打开时 focus 移入 → focus 陷阱 → ESC 关闭 → 关闭时焦点返还触发元素，配 `role="dialog" aria-modal="true"`；锁滚动 `document.body.style.overflow='hidden'`（记录原值恢复）+ 内容区 `overscroll-behavior:contain`；长内容模态 `max-height`+内部滚动。

### [AIM-4] 纯颜色编码状态（致命）
- 错误: 红/绿状态点、仅红边框的表单报错、红绿双色图表——信息只走颜色单通道，色盲用户（男性约 8%）完全不可辨，违反 WCAG 1.4.1。
- 纠正: 颜色+形状/文字双通道：状态点配图标（✓/✗）或文本标签；表单错误=红边框+错误文本+图标；图表用色盲安全色板或 shape/pattern 差异。

### [AIM-5] 触控目标过小（致命）
- 错误: 把视觉尺寸当命中尺寸；24px 甚至 16px icon 按钮手机上点 3 次点不中关闭按钮，违反 WCAG 2.5.8（AA 底线 24px，推荐 44px）。
- 纠正: `.close{width:44px;height:44px;display:grid;place-items:center} .close svg{width:20px}`；视觉必须小时用 padding/伪元素扩展热区。

### [AIM-6] Hover-only 可见性与反馈（致命）
- 错误: 删除按钮 `opacity-0 group-hover:opacity-100`，操作反馈全写在 `:hover`——触屏无 hover，隐藏=不存在、反馈=没有。
- 纠正: `@media (hover:hover)` 内才启用 hover 显隐（并配 `:focus-within`）；`@media (hover:none)` 下触屏常显；触屏用 `:active` 提供按压反馈。

### [AIM-7] 文本对比度灾难组合（致命）
- 错误: hex 对模型无感知语义，「对比度足够」断言来自模式匹配而非计算。高频组合: `text-white/60` 叠渐变（≈#999 叠彩底）；`text-gray-400` 正文（on #FFF ≈2.5:1 fail）；黄底白字（#FFF on #FACC15 ≈1.5:1 几乎隐形）；深色模式沿用浅灰（slate-600 on dark ≈3.7:1 fail）；随机亮度图上白字无 scrim；`font-weight:300`+14px 叠加雪上加霜。
- 纠正: 正文 ≥4.5:1、大字 ≥3:1、非文本组件边界 ≥3:1。锚点参数: 浅色正文 `#374151`+、辅助 `#6b7280`、边框最低 `#767676`（≈4.5:1，#999 ≈2.8:1 不达）；深色正文 `#e5e7eb`、次级 `#94a3b8`（≈7:1 on #0f172a）；黄底必须深字 `text-slate-900`（≈13.7:1）；图上白字必配 scrim `rgba(15,23,42,0.45)` 以上；渐变背景按最差区域校验（单点取色会漏）。

### [AIM-8] 动效无障碍缺失（致命）
- 错误: `prefers-reduced-motion` 系统性盲区；每元素入场 fade+slide+scale 三连、stagger 8 个子元素总时长 2.4s+，前庭障碍用户眩晕。
- 纠正: 所有含动效代码携带标准降级块 `@media (prefers-reduced-motion: reduce){*,*::before,*::after{animation:none!important;transition-duration:.01ms!important}}`；动画属性仅 transform/opacity；微交互 150~250ms、入场 200~400ms。

### [AIM-9] Placeholder 当 label（致命）
- 错误: 输入框只有 placeholder 无 label——输入后提示消失、低视力用户对比不足、读屏支持不一；「简洁=少元素」错误先验。
- 纠正: `<label for="email">邮箱</label><input id="email" type="email" placeholder="example@site.com" autocomplete="email">`——placeholder 只作格式示例；表单补 `autocomplete`（密码管理器/自动填充依赖）。

### [AIM-10] 完美数据盲视（四态缺失）（致命）
- 错误: 只渲染 happy path——列表只有 `data.map`，无空/加载/错误/超长预案；假数据长度理想（John Doe、恰到好处的两行简介）。「截图里看得见的我做，看不见的我不做」——demo 与生产代码的核心差距；静默通过验收，上线集中爆发。
- 纠正: 四态完备——`isLoading→骨架屏（与加载后布局同构避免跳动）`、`isEmpty→引导空态（插画/说明/主行动按钮）`、`error→错误信息+重试出口`、`success→数据`；检查 `res.ok`，错误分类（4xx/5xx/网络）。

### [AIM-11] 连点重复提交（致命）
- 错误: 交互 handler 无 pending 概念——慢网下连点→重复下单/发帖/支付；乐观更新无失败回滚。
- 纠正: pending 锁+`disabled={pending}`+文案切换（「支付中…」）；乐观更新必配回滚——保存 prev，`catch{setLiked(prev);toast('操作失败')}`，`finally` 复位 pending。

### [AIM-12] 读屏信息缺失（致命）
- 错误: 图片 alt 缺失或写「图片」、装饰图不给 `alt=""`、icon-only 按钮无 aria-label、动态更新（购物车计数、校验错误）无 aria-live——读屏用户零感知。
- 纠正: icon-only 按钮 `aria-label="搜索"`；内容图 alt 描述信息、纯装饰图 `alt=""`；动态更新容器 `aria-live="polite"`。

---

## 严重

### [AIM-13] AI slop 模板脸（严重）
- 错误: 训练分布最大似然输出——任何项目 hero 都紫蓝渐变 `linear-gradient(135deg,#667eea,#764ba2)`；blue-500/indigo 起手（十项目十张同脸）；渐变文字、玻璃拟态满页、发光按钮、`rounded-lg shadow-md` 全家桶。
- 纠正: 品牌未定时先问/用占位品牌 token（`bg-[--action-primary]` 注明「待替换」）或中性克制方案（白底+单主色+灰阶）；渐变 ≤1 处/页且 hue 差 ≤60°；渐变文字 ≤1 处；玻璃拟态仅 1~2 个浮层且背后有内容；高级感优先来自留白/对齐/字阶而非特效数量。

### [AIM-14] 万物居中综合征（严重）
- 错误: 标题、多行段落、按钮排、表单、页脚全 `text-align:center`——居中破坏 F 型扫描基线，>2 行居中文本每行起笔随机（左右双毛边），全页居中=无对齐轴=无版式。
- 纠正: 仅标题/短副标题（≤2 行）可居中；正文/列表/表单/页脚左对齐: `.hero h1{text-align:center} .hero p{text-align:left;margin-inline:auto;max-width:65ch} .footer{text-align:left}`。

### [AIM-15] 强调反转（严重）
- 错误: 红色实心「取消/删除」+灰色描边「确认」——用户扫一眼点了最醒目的恰是破坏性操作。根因: 把「危险=红色」颜色语义直接当强调规则；Von Restorff 要求隔离推荐项而非任意有语义色的项。
- 纠正: 主操作=实心主色（右侧），取消=文本/描边（左侧）；真正的删除: 红色描边（弱于主操作）+后果写入文案的二次确认（输入名称等）。

### [AIM-16] 视觉层级决策缺失（严重）
- 错误: ①等权布局——所有区块 `repeat(3,1fr)`、3 个实心 CTA 同尺寸同排；②层级手段贫乏——H1 48/H2 40/H3 32 全 400 字重（相邻层级肉眼难辨）；③假数据仪表盘——4 张等宽 stat 卡+图标+绿色 `+12%`，主 KPI 与次要信息同视觉强度。
- 纠正: 12 列栅格按权重分配（`.main{grid-column:span 8} .side{span 4}`）；每屏 1 个主 CTA；字号阶梯 1.25~1.333 倍+字重/颜色/间距多通道: `h1{48px;700} h2{32px;600} h3{24px;600}`；eyebrow 用 `uppercase+letter-spacing:0.08em+12px+500`；仪表盘 1 个核心指标大卡+次级紧凑列表，趋势 sparkline、增长箭头+颜色双通道。

### [AIM-17] 间距失序（严重）
- 错误: ①单值化——整页只有 `gap:16px`/`space-y-4`，接近性分组失效；②非刻度值——`margin-top:13px; padding:15px 18px; gap:22px` 记忆分布「附近值扰动」；③移动端不缩放——手机上区块间仍 96px 空白。
- 纠正: 4px 网格刻度（13→12、15/18→16、22→24）；层级 2 倍递减（组 32/字段 16/标签 4）；组件内 8/组件间 16~24/区块间 48+；移动端分档缩放 `.section{padding-block:48px}` → `@media(min-width:768px){72px}` → `@media(min-width:1024px){96px}`。

### [AIM-18] 卡片汤（严重）
- 错误: 每组数据一个边框+阴影卡片，卡中卡三层嵌套各带边框——分组焦虑→边框当默认分组手段（格式塔优先级应为间距>背景>边框）。
- 纠正: 外层一个容器，内层用间距/分隔线不再起框: `.panel{border:1px solid #e5e7eb;padding:16px} .panel .stat+.stat{border-top:1px solid #f3f4f6}`；分组优先用间距差和背景色差。

### [AIM-19] 图标体系混乱（严重）
- 错误: 🚀💡✨ emoji 当 UI 图标与线性 SVG 图标库同屏混用；线性+填充+duotone 多风格并存——emoji 是彩色位图跨平台渲染不一，且零资产成本是「最省事」选择。
- 纠正: 统一图标库（如 lucide-react）固定 stroke 宽度 `<Package size={16} strokeWidth={2}/>`，全站单一风格（线性或填充二选一）；emoji 仅出现在聊天/情感语境的内容中。

### [AIM-20] 暗色模式天真移植（严重）
- 错误: 深色=`#000` 底+沿用浅色字阶与阴影，或 `filter:invert(1)` 取反思维——阴影不可见面板糊成一片、正文暗灰难读、层级消失；surface 层级/品牌色/语义色全部没有重映射。
- 纠正: 重建表面色阶（层级=表面色阶）: `--bg-base:#0b0d10 / --bg-surface:#16191f / --bg-raised:#1f232b`；文字 `#f3f4f6`、次级 `#9ca3af`（不碰 slate-600 级）；品牌色提亮一档；深度语言改描边为主；灰阶锚点两套独立。

### [AIM-21] 静态布局假设（严重）
- 错误: ①固定尺寸 `w-[640px]`/`width:1200px`；②高度硬编码——`height:500px` 大屏露一条、移动端 `100vh` 被地址栏裁掉 CTA；③绝对定位+固定 px 坐标拼贴，视口一变即碎；④假响应式——@media 里只改字号/宽度微调，不改结构。
- 纠正: 高度由内容+`min-height` 定义: `.hero{min-height:min(88svh,800px);padding-block:64px}`；absolute 仅用于锚定容器内角标（`.card{position:relative} .badge{position:absolute;top:12px;right:12px}`）；响应式=结构重排: 列数降级/侧栏变抽屉（`.sidebar{position:fixed;transform:translateX(-100%)}`）/间距分档。

### [AIM-22] 动态内容溢出不设防（严重）
- 错误: 用理想长度假数据排版——①固定高度 `h-40`/`height:240px` 真实文案溢出裁切（静默发生）；②flex/grid 子项默认 `min-width:auto`，长用户名/URL 把按钮挤出屏幕；③截断三件套缺件——只写 `text-overflow:ellipsis` 不配 `white-space:nowrap`+`overflow:hidden`。
- 纠正: `.card{min-height:240px}`；`.desc{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}`；`.name{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}`；`.cell{overflow-wrap:anywhere}`（长关键词/URL）；`img,video,pre{max-width:100%}`；`.table-wrap{overflow-x:auto}`。

### [AIM-23] 无媒体占位（CLS）（严重）
- 错误: `<img>` 无 width/height/aspect-ratio，渲染器无法预留空间——图片加载后文字被推下（布局跳动），Lighthouse CLS 扣分（Good <0.1）。
- 纠正: `<img src="hero.jpg" alt="" width="1200" height="630">`；或 `.media{aspect-ratio:16/9}`；骨架屏占位与加载后布局同构，避免二次跳动。

### [AIM-24] z-index 军备竞赛（严重）
- 错误: 9999/99999 叠罗汉——toast 盖住 modal 按钮、scrim 缺失、动效/遮罩/toast 层互相穿透；每加一层随手 +1，没有分层体系。
- 纠正: 分层 token 并全站遵守: sticky 1000 / dropdown 1100 / overlay 1200 / modal 1300 / toast 1400（或 CSS 变量 `--z-*`）；新层必须入表，禁止随手取值。

### [AIM-25] 交互状态集不完备（严重）
- 错误: 组件只有 default 态（偶有 hover），`:focus-visible`/`:active`/`:disabled` 几乎从不生成——键盘不可用、禁用态无视觉；伪类不是「看得见的代码」，不产生错误截图、静默通过验收。
- 纠正: 每个交互组件携带完整状态集: `.btn:hover{background:#1d4ed8} .btn:focus-visible{outline:2px solid #93c5fd;outline-offset:2px} .btn:active{background:#1e40af} .btn:disabled{background:#93c5fd;cursor:not-allowed}`。

### [AIM-26] 动效参数模板化（严重）
- 错误: 一律 `transition:all .3s ease` 占位参数进生产——.3s/ease 是训练语料最高频模板值；`all` 是性能与意外动画之源；ease-in/ease-out 字面义误用（入场误用 ease-in——先僵后跳，用户以为卡了）；时长与感知倒挂（hover 300ms 迟钝、转场 120ms）。
- 纠正: 按交互类型分层——微交互 150~200ms ease-out、入场 200~400ms ease-out（快出慢停）、退场 ~150ms ease-in（快走）、页面转场 300ms `cubic-bezier(0,0,0.2,1)`；显式属性列表代替 all: `.btn{transition:background-color 150ms ease-out,transform 150ms ease-out}`。

### [AIM-27] 动效实现缺陷（严重）
- 错误: ①transitionend 无兜底——被打断时事件不触发，快速连点后组件卡在半开状态；②JS timeout 与 CSS 时长两处硬编码不同步（`timeout={300}` vs CSS `.25s`，退出动画被提前卸载）；③组件定义在 render 内部或 `key={index}`——父级重渲即 remount，入场动画全列表重播闪烁；④动画 layout 属性（width/height/top/left）低端机掉帧。
- 纠正: 事件+超时双保险: `const t=setTimeout(onClose,DURATION+50); el.addEventListener('transitionend',()=>{clearTimeout(t);onClose()},{once:true})`；时长单一来源（JS 读 CSS 变量 `--dur`）；组件定义提到模块级、key 用稳定 id；动画只用 transform/opacity，单元素并发动画属性 ≤2。

### [AIM-28] token 口惠而实不至（严重）
- 错误: 宣称「使用了设计 token」，代码里 3 个变量+其余全硬编码——局部生成每组件从「常见值」独立采样、无人持有全局清单: 圆角 4/6/8/12px 漂移、「次要文字」颜色随机（#333/#374151/#64748b/#6b7280）、gray/slate/zinc 多系混用。
- 纠正: 生成任何界面前先输出 CSS 变量块，后续值只允许 `var()` 引用: 圆角 `--radius-sm:6px / --radius-md:10px / --radius-lg:16px`（同类组件必须同档）；文字三级 `--text-primary:#111827 / --text-secondary:#4b5563 / --text-tertiary:#9ca3af`（+白色反转态）；token 不必过度生成——字号 token ≤8、行高分档 ≤4。

### [AIM-29] 颜色语义纪律缺失（严重）
- 错误: ①cry-wolf red——促销红/装饰红泛滥，真 error 出现用户脱敏（偶见绿=错误的语义反转）；②语义色与品牌色冲突不检查（品牌绿 #10B981 撞 success 绿 #059669 肉眼不可辨）；③强调色通胀——单屏每模块一个 accent（5+ hue）；④图表彩虹——饼图 8~10 片 8 色、双 Y 轴柱线混用。
- 纠正: 红色预算留给错误/危险，促销用品牌色；语义色板固定（success #16a34a / warning #d97706 / danger #dc2626 / info #2563eb），装饰色不得占用语义色；冲突时换 hue 拉开（success→teal #0D9488）或加图标兜底；单屏 accent 1~2 个；品牌色遵循 60-30-10；图表分类色 ≤5~6、饼片 ≤5 且降序+「其他」归桶、比较优先条形图。

### [AIM-30] API/参数/资产名幻觉与串扰（严重）
- 错误: ①编造组件库不存在的 props（`variant="tertiary"`）、版本敏感 props 记混；②aria-* 拼错或编造（`aria-role` 不存在、`aria-labelledby` 指向不存在的 id）；③引用不可用字体——`font-family:"Neue Haas Grotesk"` 无任何 @font-face（「名字存在于知识」≠「字体存在于运行环境」）；④断点串扰——AntD 项目写 Tailwind 断点、Bootstrap `992px`（lg）与 Tailwind `lg:`=1024px 同项目混用；⑤Tailwind v3/v4 类名-值映射漂移。
- 纠正: 不确定时 fallback 到原生 HTML+自写 class，注释「取值待查库文档」；引用字体必给加载方案（@import+`display=swap`）或用可近似替代并声明；同一项目只允许一套断点表，生成前确认框架与版本；Tailwind 用语义类（`leading-relaxed`）比任意值（`leading-[1.625]`）更抗记忆漂移。

### [AIM-31] alert()/confirm() 代替正规 UI（严重）
- 错误: 阻塞式原生弹窗打断流、样式不可控与产品调性割裂、移动端体验突兀、无法内嵌帮助信息——「有反馈」的最短路径默认。
- 纠正: 危险操作→自定义确认对话框（后果写入文案）；反馈→toast（可带撤销 action）；表单校验→内联错误信息（字段旁），不用弹窗。

### [AIM-32] 中文排版残留错误（严重）
- 错误: ①`word-break:break-all` 误当中文标配——英文单词/数字串被拦腰斩断（`Flexbo\nox`、`2026111\n6`）且破坏禁则；②中文页面残留西文 `letter-spacing:0.02em~0.05em`（英文模板迁移不完全）；③字体栈顺序写反——`"PingFang SC","Inter"` 西文被中文字体接管；④标点漂移——半角标点混入、直引号、`--` 代破折号、`...` 代省略号。
- 纠正: 中文换行 `line-break:strict; overflow-wrap:break-word`（仅长串兜底）；中文正文 `letter-spacing:normal`；字体栈西文在前 `"Inter","PingFang SC",sans-serif`；中文标点全角化（，。「」），配 lint 约束防长上下文漂移。

### [AIM-33] 排版机制遗漏（知道但漏写）（严重）
- 错误: 「知识存在但生成时省略」——比「不知道」更危险，无法靠教知识修复，只能靠 checklist/lint。高频遗漏: ①@font-face 忘 `font-display`（Lighthouse 报 `Ensure text remains visible during webfont load`）；②标题不收紧 line-height（h1 3.5rem 继承 body 1.6→两行标题巨大空隙）；③计时器/价格/表格忘 `tabular-nums`（动态数字宽度抖动，静态 demo 掩盖、接真实数据才暴露）；④正文无行长控制（每行 100+ 字符）。
- 纠正: 生成后自查清单——`font-display:swap`；标题 `line-height:1.1~1.2` 显式覆盖继承；数字组件 `font-variant-numeric:tabular-nums`；正文 `max-width:65~70ch; margin-inline:auto; padding-inline:1rem`。

### [AIM-36] 数据可视化配色失当（严重）
- 错误: 分类图表按类别数直接生成色相（9 类 9 色彩虹，相邻不可辨）；趋势/热力/时序图用色相渐变（彩虹）表达数值大小——色相无固有顺序，读序混乱；配色不过色盲模拟。典型: 饼图 9 片全彩。
- 纠正: categorical ≤8 类+「其他」聚合；sequential/热力用明度单调色带（明度是唯一可靠数值通道，禁彩虹）；交付前过 deuteranopia 模拟+灰度验证。

### [AIM-37] 滚动与动效编排失当（严重）
- 错误: 弹窗/抽屉内滚动不收口，与页面滚动串轴；路由返回后列表回顶部（位置丢）；入场动画逐个 stagger 无封顶（8 元素拖 3s+，整体感瓦解为「逐个事件」）。
- 纠正: 弹层滚动容器 `overscroll-behavior:contain`；列表返回恢复滚动位置；stagger ≤50ms/项、组总时长 ≤600ms，编排只做骨架级。

### [AIM-38] 排版工程化参数误用（严重）
- 错误: `html{font-size:62.5%}` rem hack（破坏第三方嵌入与无障碍字号缩放）；`clamp()` 流体缩放用于正文（窄屏缩至不可读）；@font-face 不声明可变字体轴区间与回退 size-adjust 度量匹配（首行跳动）。
- 纠正: 禁 62.5% hack（px→rem 换算交工具）；流体 clamp 仅限 ≥24px 大标题，正文用离散档位；可变字体显式限定轴区间，回退配 size-adjust/ascent-override 对齐度量。

---

## 一般

### [AIM-34] 字距与断行细节（一般）
- 错误: 全大写文本不加 tracking（视觉松散）；正文误加 `letter-spacing:0.1em`；`font-size:2vw` 视口单位排文字（小屏字号坍缩）；`<br>` 做间距/换行控制；用 letter-spacing 修截断问题（机制错配）；孤行寡尾不管。
- 纠正: 全大写配 `letter-spacing:0.08em+`；正文 letter-spacing 保持 normal（仅大标题收紧 `-0.02em`）；字号用 rem/clamp() 不用 vw；间距用 margin/padding 不用 `<br>`；标题 `text-wrap:balance`、正文 `text-wrap:pretty` 缓解孤寡行。

### [AIM-35] 语义标签与结构细节（一般）
- 错误: `<b>/<i>` 与 `<strong>/<em>` 语义混用；表格无 `<caption>`/`th scope`；heading 跳级（h2 后直接 h4）；autoFocus 滥用（读屏/键盘用户被强行拽走——登录页聚焦用户名是可接受惯例，常规页面到处 autofocus 是错误）；tabindex 正值乱序。
- 纠正: 强调用 `<strong>/<em>`，纯样式加粗用 CSS `font-weight`；表格配 `<caption>`+`<th scope="col|row">`；heading 逐级不跳；autoFocus 仅限登录/搜索等单一任务页；DOM 顺序即 tab 顺序，避免 tabindex 正值。

---

## 元根因分析

35 条错误归纳出 6 个系统性根因（各子领域自我质询轮的元分析合并；含 R19 深化轮增补后共 38 条）：

### 根因 1：无视觉反馈回路——结构性「没有眼睛」
AI 基于 token 序列生成 CSS，从不「看到」渲染结果：溢出、错位、对比不足、层级糊成一片全部不可观测；写「对比度足够」时从未计算过——断言是从训练分布抄「常见的」而非「正确的」（AIM-7/20/22 根源）。修复方向：靠可机械判定的规则清单硬补（对比度锚点表、刻度表、四态清单）。

### 根因 2：训练分布污染与收敛解偏好——「常见」≠「正确」
Dribbble 截图美学、模板教程、低质快速原型 demo 在训练语料中密度极高：紫蓝渐变、居中 hero、blue-500、完美假数据。AI 输出的是那个分布的均值，而那个分布本身是「截图美学」（为截图服务，不为使用服务）（AIM-13/14/16/26 根源）。

### 根因 3：局部采样、全局失忆——逐组件从记忆分布独立取值
生成时无人持有全局清单：圆角、灰色、间距、阴影每次从「常见值」独立采样；多框架相似 API（断点表、token 值、间距刻度）在参数空间相邻导致回忆串扰；多轮迭代每轮微调值，不一致持续累积（AIM-17/24/28/30 根源）。修复方向：先输出 token 块、后续值只允许 `var()` 引用的强制流程。

### 根因 4：Happy path 偏好与完成度错觉——负面场景系统性欠生成
「HTML 结构完整=完成」的错觉；错误处理、空态、降级、pending 锁、失败回滚在训练数据密度低、演示截图不可见，被系统性欠生成——最危险的是静默通过验收，接入真实数据/上线审计（Lighthouse/axe/WCAG）时集中爆发（AIM-10/11/25/27 根源）。

### 根因 5：桌面具身心智与理想数据假设——非默认感知通道全是盲区
默认视口 1280/1440 桌面、默认数据理想长度、默认交互鼠标+hover：没有拇指、没有 3.5 寸屏肌肉记忆、没有读屏/键盘/色盲/前庭障碍的具身经验——hover-only、32px 小按钮、无焦点管理、无 reduced-motion 对 AI「看起来完全没问题」（AIM-1/5/6/8/21 根源）。「桌面浏览器 1080p 下没问题=没问题」是看似合理实则错误的自检信条。

### 根因 6：知道但漏写+对记忆过度自信——幻觉的温床
font-display、tabular-nums、line-height 收紧都是明确知道却高频遗漏的项——无法靠「教知识」修复，只能靠 checklist/lint；同时 AI 会一本正经地写死拍脑袋数值、编造精确统计、幻觉组件 props 与字体名（AIM-30/33 根源）。修复方向：不确定参数显式声明「待查文档」，语义 token 类名优先于硬编码数值。

---

## 来源索引

- 7 个子领域自我质询萃取文件（本文档全部条目的合并来源）: corpus/ui-ux-design/<7 子领域>/elicited/06-ai-mistakes.md
- R19 深化轮增补（AIM-36~38）: [模型经验] corpus/ui-ux-design/<sub>/elicited/ 下 CS 08-dataviz-color、IM 08-motion-choreography 与 09-scroll-ux、TY 08-fluid-typography 与 09-variable-fonts-perf
- 性质说明: 本文件为模型自我质询的内省知识（[模型经验]），非官方文档事实；参数值待文档验证，以官方标准（WCAG 2.x、Core Web Vitals）现行版本为准。
- 元根因 1/2/5（训练数据分布类归因）是内省假说；「AI slop 默认审美」属时效性知识，引用前建议实测复核。

## 对账记录

| 轮次 | 结果 | 日期 |
|---|---|---|
| R19（深化轮，回溯补记） | 新增 AIM-36~38——原轮漏对账登记，本回溯补记 | 2026-11-17 |
| R6（项目评审第六轮） | 补账：确认 AIM-01~AIM-38 基线与 SKILL.md 索引一致；本轮评审无新增 | 2026-11-17 |
