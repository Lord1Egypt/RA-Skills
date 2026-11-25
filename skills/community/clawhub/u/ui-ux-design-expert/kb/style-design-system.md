---
domain: ui-ux-design
skill_name: ui-ux-design-expert
subdomain: style-design-system
title: 风格与设计系统（style-design-system）
version: 4
updated: 2026-11-17
merged_at: 2026-11-16
source_index: corpus/ui-ux-design/style-design-system/elicited/01~08；docs/hig/（R34 实抓 11 主题：typography/color/materials/dark-mode/layout/app-icons/accessibility/buttons/menus/sliders/text-fields；R39 增量 2 主题：designing-for-iphone-duo（2026-09-09 新页）/gestures（macOS touch input，2026-10-28）；R40 收尾 4 主题：design-principles（2026-06-08 重新引入）/offering-help（Tooltips 并入页）/snippets（2026-06-08 新页）/pointing-devices（2026-10-28 更新））
knowledge_ratio: "法则 ~25% / 最佳实践 ~45% / 坑点 ~30%"
---

# 风格与设计系统（style-design-system）

## 定位与心智模型

界面「为什么好看」的根因：**统一的风格语言 + 系统化的设计决策**。风格不是贴在组件上的皮肤，而是把视觉决策收敛到可复用刻度上的纪律体系。核心机制 **Design Tokens**：设计决策命名化、集中化、可复用——组件只引用语义名不知具体值，故「改一处全局生效」（主题/暗色/换品牌在换绑层）。

与 Apple HIG 对齐（R34 全量实抓）：Materials「在前景与背景元素之间创造深度、分层与层级感的视觉效果」，Liquid Glass 只用于控件与导航功能层 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/materials.md)；Color「克制用色可增强沟通、唤起品牌、提供视觉连续性、传达状态与反馈」[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/color.md)——分别与 elevation 深度语言、60-30-10 方向一致。

适用边界：本文件管「风格语言系统」（token 架构、风格谱系、状态体系、深度质感、品牌注入、变体与 token 治理）+ **Apple HIG 平台规格锚点**（材质/系统色/Dark Mode/安全区/控件尺寸/图标，见参数速查）。色彩调色 → color-system；字阶机制与字体加载 → typography；间距布局机制 → layout-composition；微交互时序 → interaction-motion；组件交互模式 → patterns。

## 法则

[SD-1] **MUST**: 每个可交互组件必须定义完整状态集（default/hover/focus-visible/active/disabled；表单类加 error；异步动作类加 loading；数据展示类加空态/加载态/错误态），缺一不可交付
[SD-2] **NEVER**: 禁止 `outline: none`（或等价移除焦点框）而不提供替代焦点指示；焦点指示必须用 `:focus-visible`，焦点色与组件背景对比度 ≥3:1（必要时 outline-offset/双层环保证可见）
[SD-3] **MUST**: 所有视觉决策值（颜色/间距/圆角/阴影/时长/缓动/z-index）必须来自预定义 token 刻度，组件代码禁止刻度外一次性字面量；动效时长/缓动取自动效 token（微反馈 100~150ms、常规 200~250ms、大区域 300~500ms），NEVER `transition: all`
[SD-4] **MUST**: token 采用 global→alias→component 三层，组件样式只引用 alias/component 层（NEVER 跳线直引 primitive 如 `var(--blue-500)`）；命名按功能而非外观（`--color-action` 合格，`--color-blue` 不合格）
[SD-5] **MUST**: 间距基于单一基准网格（4px 或 8px 二选一，全站唯一），且间距层级动机化（组件内 < 组件间 < 区块间）
[SD-6] **MUST**: 字阶按固定比例（modular scale，如 1.25/1.333）取样并显式声明档位；行高用无单位值
[SD-7] **MUST**: 圆角限制为 3~4 档 token，同类组件必须同档；形状语言全站一致以构成风格指纹
[SD-8] **MUST**: 阴影定义为离散 elevation 档位 token，档位与组件角色（卡片/悬浮/模态）绑定；全站光源方向唯一；深色模式切换为 surface 明度阶梯 + 描边为主的深度语言
[SD-9] **MUST**: 单一界面风格决策唯一（玻璃拟态+新粗野+拟物混搭即违规），风格必须贯穿布局密度/字体/间距/动效全系统，NEVER 只改 surface 级属性当「贴皮」
[SD-10] **MUST**: 使用 `backdrop-filter` 的元素必须提供高不透明度降级（`@supports not` 回退）且背后必须有可模糊内容；同页大面积玻璃元素 ≤2 类
[SD-11] **MUST**: hover 效果必须包裹在 `@media (hover: hover) and (pointer: fine)` 中；主操作不得依赖 hover 才暴露
[SD-12] **NEVER**: 禁止仅用颜色传达状态/错误信息（error 必须颜色 + 图标/文字 + aria 多通道；增长/下降必须箭头 + 颜色双通道）
[SD-13] **MUST**: 禁用必须同时具备语义（`disabled` 属性或 `aria-disabled` + JS 拦截）与视觉，视觉禁用 NEVER 仅靠 opacity 变灰与次级按钮混淆；异步提交期间必须进入 loading + 禁用态防双击
[SD-14] **MUST**: 状态变化引起的盒尺寸必须中性（透明边框占位、不变字重），NEVER 让 hover/选中导致布局位移
[SD-15] **MUST**: 深色模式 NEVER 纯黑底（`#000`）配纯白字（`#fff`），必须使用 surface 明度阶梯（base→surface→raised ≥3 阶）+ 品牌色提亮（tone shift）+ 调整后的文字灰阶
[SD-16] **MUST**: 品牌色占比遵守 60-30-10（中性底为主、品牌强调 ≤10% 且出场即有意义）；品牌色与功能色（error/success）NEVER 混用同一色；品牌色做文字/按钮底时对比度 ≥4.5:1，不达标生成同色相 UI 专用档
[SD-17] **MUST**: 图标系统唯一（单一图标库、统一 stroke 宽度与 linecap），NEVER emoji 与 SVG 图标混用作 UI 图标；插画风格契约全站一致
[SD-18] **MUST**: 单个组件质感手段（渐变/玻璃/噪点/发光/重阴影）≤2 种；渐变必须同色系或邻近色相、明度差 ≤15%、方向全站统一
[SD-19] **MUST**: 无品牌输入时使用中性克制方案并显式声明「未注入品牌」；NEVER 虚构蓝紫渐变品牌脸（`#667eea→#764ba2`）或默认套用 UI 库主色（Tailwind indigo / Bootstrap `#0d6efd`）冒充品牌色
[SD-20] **MUST**: 组件变体按正交轴组织（size × variant × state 各轴独立取值、自由组合），NEVER 轴耦合（variant 内焊死 size/圆角）；单组件显式变体组合 ≤12，超限走 slot/复合组件
[SD-21] **MUST**: 变体命名用固定序 + 语义名（`btn--primary btn--sm`；primary/secondary/ghost/danger），NEVER 外观名（blue/outline）或两种命名风格并存
[SD-22] **MUST**: token 重命名/废弃必须经 alias 迁移期（旧名映射新名 + 废弃警告 ≥1 个 minor，major 才删除）；NEVER 直接删 token；改 primitive 值前必须列全下游引用影响面（变更走新增档位或换绑 alias）
[SD-23] **MUST**: 多品牌/多主题 = 同一套语义名 + theme 层整组换绑 primitive（`[data-theme]` × `[data-brand]` 正交），NEVER 平行语义名（`-dark` 后缀族）；token 破坏性变更随组件库 major 版本发布并附迁移表
[SD-24] **MUST**: 材质分层纪律——动态材质（Apple: Liquid Glass）只用于控件与导航等功能层，悬浮于内容层之上；内容层禁用（例外：sliders/toggles 等瞬时交互控件激活时）；材质按语义与推荐用法选择而非表面颜色；高透明材质（clear）叠亮内容时必须加 35% 不透明度黑色 dimming 层（内容够暗或系统自带 dimming 除外）[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/materials.md)
[SD-25] **MUST**: 材质厚度与文字层级匹配——厚材质（更不透明）为细文字提供更好对比，薄材质保留背景上下文；vibrancy 文字四级 label/secondary/tertiary/quaternary，最低对比级 quaternary 禁止用于 thin/ultraThin 材质 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/materials.md)
[SD-26] **NEVER**: 禁止硬编码平台系统颜色值（文档值仅供参考且随版本波动），必须用语义化动态系统色；禁止重定义系统语义色语义（如把 separator 色当文本色）；自定义颜色必须提供 light/dark 变体及高对比度变体 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/color.md)
[SD-27] **NEVER**: 禁止提供 app 内独立外观设置（深/浅色跟随系统，独立开关与系统设置冲突会被用户当 bug）；发布前必须测试 light/dark/Auto（可能运行中切换）三外观 × Increase Contrast × Reduce Transparency（单独与组合）下的可读性 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/dark-mode.md)
[SD-28] **MUST**: 前景/背景对比度最低 4.5:1，自定义颜色力求 7:1；平台分档——≤17pt 文本 4.5:1、18pt 或 Bold 文本 3:1 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/dark-mode.md)、[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/accessibility.md)
[SD-29] **MUST**: 深色界面使用双背景组——base（更暗、后退感）与 elevated（更亮、前进感）增强层次感知，模态/popover 前台时 base 自动变 elevated；NEVER 单一背景靠阴影分层 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/dark-mode.md)
[SD-30] **MUST**: 深色环境白色背景的内容图像必须轻微调暗防「发光」；界面图标优先用自动适配的符号（SF Symbols），必要时 light/dark 分别设计并用 asset catalog 合并 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/dark-mode.md)
[SD-31] **MUST**: 布局决策依据 size class（compact/regular，横竖各一）而非设备类型/方向；size class 变化时功能不变、可见功能量可变（宽空间 tab bar 换 sidebar）；Dynamic Type 放大时横向相邻视图改纵向堆叠 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/layout.md)
[SD-32] **MUST**: 内容置于 safe area 内（tvOS 主内容距上下 60pt、左右 80pt）；visionOS 控件中心间距 ≥60pt，≥60pt 按钮周围加 4pt padding 防 hover effect 重叠 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/layout.md)、[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/buttons.md)
[SD-33] **MUST**: 交互控件命中区域 ≥44×44pt（visionOS 60×60pt）；带边框元素周围约 12pt padding、无边框元素可见边缘周围约 24pt padding [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/accessibility.md)
[SD-34] **MUST**: 支持文本放大至少 200%（watchOS 至少 140%）；字号不低于平台最小值（iOS 11pt / macOS 10pt / tvOS 23pt / visionOS 12pt / watchOS 12pt）；细字重自定义字体应大于推荐字号 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/accessibility.md)
[SD-35] **MUST**: 每视图 prominent 按钮 1~2 个；用 style（而非 size）区分首选选项，同尺寸表示选项集合；NEVER 给破坏性按钮赋 Primary（视觉突出易被误点）；自定义按钮必须有 press state [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/buttons.md)
[SD-36] **MUST**: app 图标单一核心概念、最少形状、简单背景，主要内容居中防遮罩裁剪；提供未遮罩原始图层由系统遮罩（预遮罩破坏高光且边缘锯齿）；慎用文本（不支持本地化、小字号难读）；插画优先于照片；让系统处理模糊/高光/阴影等效果 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/app-icons.md)
[SD-37] **MUST**: 菜单项动词标签、title-style 大写、需更多信息完成的操作尾加省略号；重要/常用项列前；逻辑相关项分组加 separator；子菜单 ≤1 级、子项约 >5 个考虑新建菜单；不可用项置灰但菜单保持可打开（子菜单同：子项不可用仍可打开）[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/menus.md)
[SD-38] **MUST**: text field 只用于少量信息（大量文本用 text view）；占位符输入后消失必须另配标签；敏感数据一律 secure field；字段尺寸匹配预期文本量、多字段纵向堆叠同宽分组；校验时机——邮箱失焦校验、用户名/密码提交前校验；数字用 formatter；tvOS/watchOS 最小化文本输入 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/text-fields.md)
[SD-39] **MUST**: slider 方向遵循惯例（水平最小值在 leading、垂直最小值在下）；宽范围值必须配 text field + stepper（显示精确值、直接输入）；音量调节不用普通 slider（iOS 用 volume view）；tvOS 不提供 slider [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/sliders.md)
[SD-40] **MUST**: iPhone Duo（Apple 首款折叠双屏 iPhone，HIG 新页 2026-09-09）布局适配——outer display 为 compact width、inner display 为 regular width；用 size class + layout margins + safe area insets 适配全部 device poses（合书持握/半折/平放/立放），NEVER 为单个 pose 定制布局或写死固定宽度与屏幕特定依赖；功能与元素状态跨屏一致、信息层级保持（大内屏可多展示一级层级，Mail 例：闭合单栏、展开双栏并排）；游戏每种 pose 均可玩——可锁定方向但须填满屏幕，宽高比调整优先于 letterbox/pillarboxing，无法避免时在填充区加 artwork [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/designing-for-iphone-duo.md)
[SD-41] **MUST**: iPhone Duo reserved regions（保留区）——外前摄（常驻，展开为 Dynamic Island 承载 Live Activities）、内前摄（屏下，仅激活时出现、激活时 UI 让位）、folding region（部分折叠时把内屏分为多个可用区、排除中央折叠带）；系统组件（alerts/context menus/sheets）自动避开折叠区，split views 自动调整栏宽与边距；自定义组件用 ReservedRegion API（SwiftUI ReservedRegion / UIKit UIView ReservedRegion）重定位；折叠时 NEVER 极端布局变化——只移动必要元素、优先小调整而非重排；网格布局优先偶数列保证折叠分割干净 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/designing-for-iphone-duo.md)
[SD-42] **MUST**: iPhone Duo arrangement view（双视图容器）——split 型按容器宽高比横向/纵向分割 primary/secondary，overlay 型上下叠放（部分折叠时两视图各占一侧，其余时 primary 叠于 secondary 之上）；HStack/VStack 布局直接映射 split、ZStack 映射 overlay；导航容器（navigation split view/tab view）置于 arrangement view 外而非其内；split view 在内屏展开、外屏折叠为单栏（同常规/紧凑环境间适配）[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/designing-for-iphone-duo.md)
[SD-43] **MUST**: iPhone Duo 垂直控件轴——外屏更宽更矮，系统把 toolbars/tab bars/导航控件（含 Dynamic Island、状态栏）移到侧边保留垂直内容空间，内屏横屏同侧保持连续体验（内屏竖屏保留标准水平栏）；垂直轴顶部为主导航控件（Back/Close）、其次 prominent 动作（Done），其余条目保持原分组；条目溢出自底向上，用 ToolbarItemVisibilityPriority 调整保留顺序（优先保高频动作如 Compose/New Note 与带 badge 状态项）；一般 NEVER 覆盖默认栏位；非纯文本 toolbar item 必须同时提供 title 与 symbol（系统按上下文选用表示，overflow 菜单用 title）；文本按钮最少化（带文本 label 保持水平栏）；空间受限时按体验类型二选一——导航型收 toolbar 进 overflow 保 tab bar（默认压缩行为），任务型压缩 tab bar 保 toolbar（ToolbarVerticalCompressionBehavior / UIVerticalBarCompressionBehavior）；控件靠近其影响的内容（Mail 列表控件留在列表上方而非移到侧边）；用系统 overflow 菜单勿自建、省略号符号保留给 overflow [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/designing-for-iphone-duo.md)
[SD-44] **MUST**: macOS 触摸输入（2026-10-28 新增指南，Mac 触屏或 Sidecar 连接 iPad）——touch 为副输入模式，支持 touch 时布局与元素尺寸保持稳定不变；放大 tap target 而非控件本身（预判触摸起于视觉边界外，标准框架控件自动配置最优 tap target）；小/密集控件考虑 expandable controls（触摸时临时放大变体，松手后短暂保留；标准 steppers/sliders/dials 自动获得）；NEVER 以 touch 作为唯一访问方式——全部功能须经键盘+指针可达，反之指针专属操作（shift-drag、hover 菜单）应提供 touch 等价物；自定义手势须同时支持 touch 与 trackpad（直接+间接输入，必要时用修饰键）[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/gestures.md)
[SD-45] **MUST**: Apple 平台设计八原则（HIG "Design principles" 页，2026-06-08 重新引入）作为设计权衡的官方参照系——Purpose 有意义/Agency 让人自主/Responsibility 以用户利益行事/Familiarity 建立在已知之上/Flexibility 适应多样情境/Simplicity 清晰直接/Craft 关注每个细节/Delight 有人情味；关键细则：引导流程必须可跳过或可退出（Agency）；错误必须可恢复且不耗费用户时间与工作成果（Agency）；请求权限必须给出清晰理由、只收集功能必需的数据（Responsibility）；可访问性从起点作为优先项而非事后补救（Flexibility）；多输入方式（语音/触摸/键盘）与各平台同等用心（Flexibility）；简洁 ≠ 极简主义——聚焦有用的体验让重要的触手可及（Simplicity）；发布不是终点——界面随平台能力与设计模式持续维护（Craft）；愉悦 ≠ 装饰——不为愉悦本身妨碍核心任务（Delight）[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/design-principles.md)
[SD-46] **MUST**: Tip（轻量功能提示，TipKit）纪律——tip 只用于简单功能（描述容易、≤3 步可完成；>3 步的功能对 tip 太复杂）；文案 1~2 句、直接面向动作，禁推广内容或关联其他功能/流程；按类型选择——popover tip 保内容流、inline tip 保周边信息可见（annotation 式指向具体 UI 元素、hint 式无特定 UI）；用参数或事件资格规则控制出现时机（已用过该功能的用户不应再看到），多 tip 并存时设合理展示频率（如每 24 小时一次）；有关联符号时优先 filled 变体；需要更多入口时加按钮直达设置或资源 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/offering-help.md)
[SD-47] **MUST**: Tooltip（macOS「help tag」/visionOS 凝视或悬停出现）纪律——只描述用户所指的控件（不扩展到邻近控件或更大任务）；以动词开头说明控件发起的动作（如 "Restore default settings"）；一般避免重复控件名（占空间且少有价值）；内容 ≤60~75 字符（本地化常改变长度），可用句子片段省略冠词，需要大量文字描述的控件应简化界面而非加长 tooltip；sentence case 大小写；考虑按控件状态提供上下文敏感 tooltip [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/offering-help.md)
[SD-48] **MUST**: Snippet（Siri/App Shortcuts/Spotlight 结果视图，2026-06-08 新页）——两型：confirmation（确认/取消+影响结果的选项，系统提供 Cancel 副按钮+可自定义标签主按钮）与 result（纯信息展示，单个 Done 按钮）；custom view 高度 ≤400pt 保证全部内容可见；内容精简、更多细节 deep-link 进 app 而非塞进视图；主按钮标签必须描述性（点咖啡场景 Order 优于 OK/Proceed，缺省 Continue）；NEVER 依赖对话文本传达 snippet 目的——视觉呈现优先省略口头 dialogue、用 custom view 传达（dialogue 仅供不看屏幕的语音场景）；custom 内容与系统背景在 light/dark 两种外观下均保证对比度与一致边距 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/snippets.md)
[SD-49] **MUST**: 指针交互（iPadOS/macOS/visionOS）——iPadOS 三种 content effect：highlight（指针与控件间出现 Liquid Glass 形状，默认用于 bar buttons/tab bars/segmented controls/edit menus）、lift（缩放+阴影+顶部高光营造浮起，默认用于独立 Liquid Glass 控件/应用图标/控制中心按钮）、hover（自定义 scale/tint/shadow，用于大元素）；标准元素优先系统指针形态（文本区 I-beam 等）；命中区 padding——带边框元素约 12pt、无边框元素可见边缘约 24pt（与 [SD-33] 同数值，指针与触控命中区一致）；bar 内相邻按钮命中区必须连续（间隙导致 highlight 消失闪烁）；自定义指针保持简单、NEVER 纯装饰效果或指针上显示说明文字；shadow 必须搭配 scale（不缩放元素加阴影不产生「靠近」感）；表格行等无法扩展的元素只用 tint 不用 scale；macOS touch 唤出隐藏控件——点击大致位置唤出（只唤出相关控件、用完或数秒后隐藏、保留当前选区）、关键隐藏控件必须进 context menu 兜底、sidebar 点击对应分区头/行唤出（点击隐藏控件区域只显示不激活）、标签页窗口点击任意处唤出当前标签关闭按钮 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/pointing-devices.md)

> SD-1~SD-19、SD-22~SD-23 溯源：[模型经验](corpus/ui-ux-design/style-design-system/elicited/01~08)。
> SD-20~SD-21 溯源：[模型经验](corpus/ui-ux-design/style-design-system/elicited/08-component-variants-token-governance.md)。
> SD-24~SD-39 溯源：[官方文档] Apple HIG R34 实抓（corpus/ui-ux-design/style-design-system/docs/hig/，11 主题全量）。
> SD-40~SD-44 溯源：[官方文档] Apple HIG R39 增量实抓（designing-for-iphone-duo.md 新页 2026-09-09、gestures.md macOS touch input 2026-10-28；corpus/ui-ux-design/style-design-system/docs/hig/）。
> SD-45~SD-49 溯源：[官方文档] Apple HIG R40 收尾实抓（design-principles.md 2026-06-08 重新引入、offering-help.md（Tooltips 并入页）、snippets.md 新页 2026-06-08、pointing-devices.md 更新 2026-10-28；corpus/ui-ux-design/style-design-system/docs/hig/）。

> 全局候选 SD-G1~G3（魔法值可溯源、完整性先于美观、同维度取值来源唯一）已提交横切 `kb/laws.md`。

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| Design Tokens（三层） | 设计决策命名化、集中化、可复用；组件只引用语义名，主题在 alias 层换绑 |
| 4px 网格 / Modular scale / Elevation / 9 态 | 间距基准（8-point 亦常见，取其一）/ 字阶固定比率递进 / 离散阴影档位 / 状态完备清单（见参数速查） |
| 60-30-10 / Tone shift / Shape language | 品牌色占比纪律 / 深色品牌色提亮（VI 色 ≠ UI 主色）/ 形状语言是更隐蔽的品牌指纹 |
| Liquid Glass / base·elevated / size class / Dynamic Type | Apple 动态材质（仅控件导航层）[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/materials.md) / 深色双背景组（后退·前进）[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/dark-mode.md) / 布局决策依据（compact·regular）[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/layout.md) / 系统字阶随辅助功能设置联动缩放 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/typography.md) |
| 语义动态色 | 系统色按 light/dark/increase contrast 上下文自动适配；禁止硬编码值与重定义语义 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/color.md) |
| iPhone Duo（折叠双屏）/ reserved regions / 垂直控件轴 | outer=compact、inner=regular 用 size class 适配全部 poses；三保留区（外前摄/内前摄/折叠带）系统自动避让；toolbars/tab bars 移侧边保垂直内容空间 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/designing-for-iphone-duo.md) |
| Apple 设计八原则 | HIG 官方设计权衡参照系：Purpose/Agency/Responsibility/Familiarity/Flexibility/Simplicity/Craft/Delight（引导可跳过、错误可恢复、简洁≠极简、愉悦≠装饰）[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/design-principles.md) |

## 最佳实践

### 场景 1：从零建立三层 token 体系（源于 [SD-3][SD-4][SD-26]）

路径：先输出 primitive 层（色板/灰阶/间距/圆角/阴影/时长刻度）→ 建 alias 语义名 → 组件层只引用 alias；命名按功能；token 数量从实际组件需求反推；生成界面前先写 token 块，值只允许 `var()`。

- 错误: `--color-blue:#3B82F6` + `.btn{background:var(--color-blue)}`——按外观命名+跳线直引 primitive，换品牌/暗色无法换绑
- 正确: `--blue-500:#3B82F6`（primitive）→ `--color-primary:var(--blue-500)`（alias）→ `--color-action:var(--color-primary)`（用途粒度）→ `.btn{background:var(--color-action)}`

Apple 语义动态色是三层结构的官方范例：组件引语义名（labelColor/separatorColor），light/dark/高对比变体由系统在 alias 层自动换绑 [SD-26]。边界：小团队可合并 global+semantic 为 2 层；token 套娃 ≤2 层；`display:flex` 等布局机制不 token 化。

### 场景 2：刻度落地——间距、圆角、字阶（源于 [SD-5][SD-6][SD-7]）

路径：声明基准网格（4px 或 8px 二选一），间距只取刻度值 → 圆角 3~4 档 + full，同类同档 → 字阶声明比率按档取样，行高一律无单位。

- 错误: `button{border-radius:8px} input{border-radius:6px} .card{border-radius:12px}` + `margin-top:13px; gap:22px` + 字阶比值 1.14/1.13/1.22 无规律 + `line-height:24px`
- 正确: `--radius-sm:4px`（输入框）/ `--radius-md:8px` / `--radius-lg:12px`（卡片）/ `--radius-full:9999px`（胶囊）；`--space-1:4px … --space-16:64px`；1.25 字阶（12/16/20/25/31px）；无单位行高（tight 1.25 / normal 1.5 / loose 1.75）

边界：间距层级动机化（组件内 < 组件间 < 区块间，如 8/16/24/48）；密集体可用更密刻度但基准不变。

### 场景 3：elevation 阴影档位与深度语言（源于 [SD-8]）

路径：阴影定义为 3~5 个离散档位，档位与组件角色绑定（卡片 < sticky < 浮层 < 模态）→ 多层低不透明度小阴影替代单层大阴影 → 浅色低对比界面优先 1px 描边 → 深色切换为 surface 阶梯 + 细描边。

- 错误: 随手写阴影 + 层级倒挂（下拉比卡片轻）+ 贴纸感单层重阴影
- 正确: `--shadow-1`（卡片）`--shadow-2`（sticky）`--shadow-3`（下拉/浮层）`--shadow-4`（模态），具体值见参数速查；深色切换为 surface 阶梯 + 细描边（见场景 8）

边界：深度强度与信息密度负相关（数据密集后台用描边体系）；hover 抬升不直接过渡 `box-shadow`（重绘），预渲染两层阴影 `opacity` 切换。

### 场景 4：组件状态矩阵设计（9 态完备，源于 [SD-1][SD-2][SD-11][SD-13][SD-14][SD-35]）

路径：按组件类型勾选状态矩阵（见参数速查「状态清单」）→ 焦点用 `:focus-visible`，focus 色对比 ≥3:1 → hover 包 `@media (hover: hover) and (pointer: fine)` → 禁用走语义（`disabled`/`aria-disabled`+JS 拦截），loading 进 disabled+Spinner → 盒尺寸中性化（透明边框占位）。

- 错误: `.btn{background:#2563eb}` 只有 default（AI 最常见截断）
- 正确: 补全 `:hover` `:focus-visible{outline:2px solid #93c5fd;outline-offset:2px}` `:active`（press state 必备 [SD-35]）`:disabled{background:#93c5fd;cursor:not-allowed}` + hover 包媒体查询 + `<button disabled={submitting}>{submitting?<Spinner/>:'提交'}</button>`（loading+禁用防双击）

边界：一致性对象是「同一语义角色」而非「所有元素」——每屏至多一个 primary 按钮（HIG 同向：prominent 每视图 1~2 个 [SD-35]）；变体体系（层级）与状态体系正交，不要用状态差异表达主次。

### 场景 5：风格选型与全系统贯彻（源于 [SD-9]）

路径：按硬约束筛风格：内容密度（密集后台禁重质感）、业务调性（律所 ≠ 新粗野）、性能预算（低端机禁满页玻璃）→ 选型即选参数区间 → 同步决策布局密度/间距节奏/字阶字重/图形语言/动效曲线（只改 surface 属性是「贴皮」）→ 深色模式重调参数。

| 风格 | 识别要素（CSS 特征） |
|---|---|
| 极简 | 负空间 >40%、≤3 色板、细字重标题 |
| 扁平 | `box-shadow: none`、实色按钮、2D 图标 |
| 拟物 | `linear-gradient` 模拟凸起、皮革/纸质纹理、`inset` 内阴影 |
| 新拟态 | 双阴影一亮一暗、组件与背景同色 |
| 玻璃拟态 | `backdrop-filter: blur()` + 半透明底/描边 |
| 新粗野主义 | 粗黑描边 + 硬阴影 `6px 6px 0 #000` + 撞色 |
| Material 式 | elevation 分层投影体系 |

边界：混合风格只有一种合法形态——以一种为底座、另一种仅作局部点缀（如扁平 + 玻璃导航），点缀全站同类同参。

### 场景 6：玻璃拟态与材质分层安全落地（源于 [SD-10][SD-24][SD-25]）

路径：背景先铺可模糊内容（彩色斑点/渐变/图片）再叠玻璃 → `@supports` 降级为高不透明度实色 → 大面积玻璃每页 ≤2 处。

- 错误: 纯色背景上的「伪玻璃」——模糊后仍是纯色，退化为脏灰块
- 正确: 背景铺 `radial-gradient` 斑点 + `.glass{backdrop-filter:blur(12px);background:rgba(255,255,255,.65);border:1px solid rgba(255,255,255,.3)}` + `@supports not (backdrop-filter:blur(1px)){.glass{background:rgba(255,255,255,.95)}}`

Apple 材质分层作参照系：动态材质只用于控件/导航功能层悬浮于内容层之上，内容层内用标准材质做视觉区分；regular 变体（模糊+亮度调节）适合文本多的组件，clear 变体适合悬浮富媒体之上且必须考虑 35% 黑色 dimming 层兜底；材质之上用 vibrant colors 保证可读性，quaternary 文字禁用于 thin/ultraThin [SD-24][SD-25] [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/materials.md)。Web 玻璃拟态无系统滚动边缘效应，可读性需自行验证。

边界：数据密集/性能敏感（后台、低端机）放弃大面积玻璃；玻璃上不再叠玻璃（双层 blur 互相污染）。

### 场景 7：品牌色注入（60-30-10 + UI 档 + tone shift，源于 [SD-16][SD-19][SD-26]）

路径：60% 中性底 + 30% 结构色 + 10% 品牌强调，品牌色出场即有意义 → VI 色直接当 UI 色不达标时生成同 hue UI 专用档 → 深色模式品牌色提亮换绑（tone shift）→ 无品牌输入用中性克制方案并声明「未注入品牌」。

- 错误: 品牌黄 `#FFC107` 直接做按钮底配白字（对比约 1.6:1）；满屏品牌色
- 正确: `--brand:#FFC107`（VI 色：大面积装饰、图标）+ `--brand-ui:#B45309`（UI 档：按钮/链接，≥4.5:1）+ `.btn-primary{background:var(--brand-ui);color:#fff}`
- 错误: 深色模式品牌色原样照搬（发闷）
- 正确: tone shift——`:root{--brand:#7C3AED}` `[data-theme=dark]{--brand:#A78BFA}` 提亮约 2 档

着色纪律同向佐证：Liquid Glass 无固有颜色、透出后方内容，着色保留给真正需要强调的元素（如主 CTA 背景），避免给多个控件背景同时着色 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/color.md)。

边界：品牌色 ≠ UI 主色（同色相不同明度）；品牌红不与错误红混用；「高级感」来自克制色板、留白、精确对齐、独特字体，而非质感堆料。

### 场景 8：暗色模式系统性换绑（源于 [SD-15][SD-4][SD-27][SD-28][SD-29][SD-30]）

路径：组件只引用 alias 层，暗色 = `[data-theme=dark]` 重绑 alias，禁止组件内 `if(dark)` 双轨 → surface 阶梯 ≥3 阶（base→surface→raised，越高越亮）→ 文字灰阶、tone shift、阴影改描边同步处理。

- 错误: `[data-theme=dark]{--color-bg:#000;--color-text:#fff}` 只反转两三个变量
- 正确: `[data-theme=dark]{--color-bg-base:#0f1115;--color-bg-surface:#1a1d23;--color-bg-surface-raised:#24272e;--color-text-primary:#f3f4f6;--color-text-secondary:#9ca3af;--color-primary:#60a5fa;--shadow-sm:none}`（surface ≥3 阶 + 文字灰阶 + tone shift + 阴影改描边）

HIG 官方锚点：深色不是简单反转——base（更暗、后退）与 elevated（更亮、前进）双背景组增强层次，模态前台时 base 自动变 elevated [SD-29]；对比最低 4.5:1、自定义力求 7:1 [SD-28]；测试矩阵 light/dark/Auto × Increase Contrast × Reduce Transparency（Auto 可能在运行中切换）[SD-27]；白底内容图像轻微调暗防「发光」、图标优先自动适配符号 [SD-30]；注意 Dark Mode 不支持 visionOS/watchOS（visionOS 用自适应 glass 材质替代）[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/dark-mode.md)。

边界：深色不是反转——是独立 surface 体系；玻璃参数（rgba、blur）深色下需重调。

### 场景 9：变体轴设计决策——加变体还是加组件（源于 [SD-20][SD-21]）

| 信号 | 决策 |
|---|---|
| 仅视觉参数不同（颜色/描边/密度） | 加 variant |
| DOM 结构不同（图标槽/二级文本） | slot 或复合组件 |
| 语义/行为角色不同（Button/Link/Tag） | 加新组件 |
| 组合 >12 或出现「变体的变体」 | 停：轴已耦合，拆轴或用 slot |

- 错误: `.btn-primary{font-size:14px}` `.btn-primary-lg{font-size:16px}`——size 焊进 variant，danger-lg 缺失、组合状态不全
- 正确: variant 只换 CSS 变量（`.btn--primary{--btn-bg:var(--color-action)}`），size 只改密度（`.btn--sm{font-size:14px;padding:8px 16px}`），组合自动成立

边界：state 与变体正交——状态矩阵（场景 4）须对每个组合完备；Tailwind 用 cva 显式化变体轴（API 待验证）。

### 场景 10：token 治理生命周期一行式（源于 [SD-22][SD-23]）

提案（用途+命名+影响面）→ 评审（按功能命名？可换绑？）→ 发布（minor）→ 迁移期（旧名 alias 指向新名 + 警告 ≥1 个 minor）→ 废弃（major 删除 + 迁移表）。

- 错误: 「主蓝再深一点」直接改 `--blue-500:#2563EB`——30 个下游 alias（hover/图表/链接色）全体漂移
- 正确: 新增 `--blue-600:#2563EB`，仅换绑 `--color-primary:var(--blue-600)`，blue-500 原值保留

边界：primitive 改值 = 广播（影响所有主题）；alias 重绑 = 局部（影响换绑主题）——影响面不同，不可混同。

### 场景 11：对标 Apple HIG 平台规格（多平台设计系统适配，源于 [SD-24]~[SD-39]）

路径：token 三层与 Apple 语义体系逐项对映——语义色 ↔ 动态系统色（light/dark/高对比变体，禁止硬编码值 [SD-26]）→ elevation ↔ 材质档位（Liquid Glass/标准材质四档 [SD-24][SD-25]）→ 字阶档位 ↔ Text Styles（weight+size+leading 组合、随 Dynamic Type 联动缩放而非独立值，全档见参数速查表 D）→ 布局断点 ↔ size class（功能不变、可见功能量可变 [SD-31]）→ 安全区/控件尺寸/间距取 HIG 数值（[SD-32][SD-33][SD-34]，参数速查表 A~C）→ 组件规格按 HIG 组件页对齐（按钮 prominent 1~2/press state 必备 [SD-35]、菜单组织与子菜单深度 [SD-37]、text field 标签与校验时机 [SD-38]、slider 惯例与降级替代 [SD-39]）→ app 图标分层规格 [SD-36]。

- 错误: 「跨平台复用一套 iOS 参数」——macOS 默认字号 13pt/visionOS 控件 60×60pt/tvOS 安全区 60/80pt 各不相同，照搬 iOS 17pt/44×44pt 即错配
- 正确: 语义名统一、primitive 按平台换绑：`--font-body` 在 iOS 绑 17pt 档、macOS 绑 13pt 档、tvOS 绑 29pt 档；`--hit-target` iOS 44pt / visionOS 60pt / macOS 28pt

边界：Web 项目仅在「对标 Apple 审美」时取 HIG 值作风格参数（数值可调、纪律不变）；Apple 平台项目必须遵守平台规格（App Store 审核 + 系统组件自动行为）。

## 高频坑点（速查）

### Top 3 深度展开

**坑点 1：`outline: none` 焦点危机（违反 [SD-2]）**——Tab 导航不知道焦点在哪；axe 报 "Elements must have visible focus indicators"。根因：重置样式或为审美全局移除。
- 错误: `* { outline: none; }` 全局灭灯
- 正确: `button:focus-visible{outline:2px solid var(--color-focus);outline-offset:2px}`（对比 ≥3:1）

**坑点 2：token 同概念多值 + 跳线（违反 [SD-3][SD-4]）**——「次要文字」多值并存（`#333`/`#374151`/`#64748b`）；暗色模式发现组件直引 primitive 无法换绑。根因：值从记忆逐组件采样而非从刻度推导。修复：三级文字 token（见参数速查）+ alias 引用（见场景 1）。

**坑点 3：深色 = 纯黑反色（违反 [SD-15]）**——`#000` 底 `#fff` 字刺眼；层级靠猜；浮层阴影黑上黑不可见。根因：把深色理解为取反而非独立 surface 体系。修复见场景 8。

### 坑点速查表

（与法则/实践重复的坑点不单列，见对应 [SD-N] 与场景 1~11：同概念多值/跳线、间距/圆角漂移、阴影倒挂、贴皮混搭、玻璃无降级、hover 粘滞、仅颜色编码、灰按钮可点、hover 位移、纯黑反色、品牌滥用、质感堆料、虚构品牌脸等。）
| 症状 | 根因 | 修复 |
|---|---|---|
| Neumorphism 文字不可见、pressed/disabled 不可分辨 | 组件与背景同色，对比 <2:1（WCAG 1.4.3 失败）；状态全靠阴影微变 | 文字 ≥7:1 + `border` 兜底；状态补 inset/换色通道 |
| 扁平按钮与文本无法区分（Metro 教训） | 移除拟物线索后未补替代可供性 | 实色主按钮/描边次按钮/仅可点元素给 1 级阴影 |
| 粗野主义页面「乱」、光源混乱 | 硬阴影方向不一致 + 撞色无主次 | 阴影方向常量化进 token；1 主色 + 1-2 强调色 |
| 深色下玻璃变刺眼灰白块 | 浅色玻璃参数照搬 | 深色重调 rgba 基色与 blur |
| Aurora 渐变上正文局部对比不达标 | 渐变明暗不均 | 正文避开渐变区或压深色 scrim |
| 标题伪粗体 / 加载期布局跳动（FOUT/FOIT）/ display 字体做正文 | 用了未加载的字重 / 无 `font-display`、回退度量不匹配 / 品牌字体误当正文字体 | 字重 token + 按需 `@font-face`；`font-display: swap` + 度量匹配回退；display 字体仅标题 |
| z-index 军备竞赛（999/9999） | 随手写且与第三方库冲突 | z-index 分层 token + 预留库空间 |
| token 体系没人用 / 建了 token 仍写字面量 | 先写代码后逆向归纳 token 失败 / token 与实现脱节 | 设计时即建 token 并文档化刻度；值只允许 `var()` |
| 表单一进页面就全红 | `:invalid` 初始即匹配（空值不满足格式） | `:user-invalid` 或 JS 控制 `aria-invalid` 时机 |
| 大面积柔和渐变出现横向色带（banding） | 8bit 色深量化 | SVG feTurbulence 噪点叠加，`opacity: 0.02~0.05` |
| 不规则 PNG 图标得到矩形阴影 | 用了 `box-shadow` 而非 `drop-shadow` | `filter: drop-shadow()` 跟随非矩形轮廓 |
| hover 抬升动画卡顿 | 直接过渡 `box-shadow` 触发重绘 | 伪元素预渲染两层阴影，`opacity` 切换 |
| 报错页吉祥物卖萌、用户更恼火 | IP 形象用于严肃挫败时刻 | IP 限空态/加载/引导等低挫败场景 |
| 单组件 40+ 变体、矩阵有缺口（无 danger-lg） | size 焊进 variant、结构差异塞进变体轴 | 轴正交：variant 换 CSS 变量、size 改密度；结构走 slot（[SD-20]） |
| token 重命名后跨包样式崩 / Figma 同步报 missing | 直接改名，无 alias 迁移期 | 旧名 alias 指向新名 + 警告，major 才删（[SD-22]） |
| 换主题后部分组件不变色 | 平行语义名（`-dark` 族）或直引 primitive | 主题 = 同一语义名集整组换绑；CI 校验覆盖率（[SD-23]） |
| 玻璃层文字时隐时现不可读 | 最低对比文字层级用于薄材质 | quaternary 禁用于 thin/ultraThin；厚材质配细文字（[SD-25]） |
| 模态打开后背景突然变亮、误判为 bug | base→elevated 是系统自动行为（后退/前进层次感知） | 接受并设计双背景组，不 hack 固定色（[SD-29]） |
| app 内深色开关上线后被用户当 bug | 与系统级外观设置冲突 | 跟随系统，不提供独立开关（[SD-27]） |
| 图标遮罩后边缘锯齿、高光失效 | 提前遮罩/预圆角处理 | 提供未遮罩原始图层，系统负责遮罩（[SD-36]） |
| 菜单项时而可见时而消失 | 不可用项直接隐藏致位置跳动 | 置灰保持菜单位置稳定，菜单仍可打开（[SD-37]） |
| 占位符当标签、输入后不知字段是什么 | 占位符输入后即消失 | 另配标签/浮动标签（[SD-38]） |

### AI 生成界面风格的系统性根源（防御元认知）

AI（含新手）生成风格化代码的错误集中于五类根源（内省假说）：
- **R1 回退众数**：无品牌输入时输出训练数据均值脸（蓝紫渐变 / Tailwind indigo）（[SD-19] 防御）。
- **R2 局部生成、全局失忆**：逐组件独立取值导致圆角/间距/阴影漂移（[SD-3]/[SD-7] 防御；对策：先写 token 块）。
- **R3 审美与可访问性脱节**：focus/触屏/对比度让位于「看起来好」（[SD-2]/[SD-11]/[SD-12] 防御）。
- **R4 像素值凭模式记忆**：16px/14px/12px 高频共现值不构成体系（[SD-5]/[SD-6] 防御）。
- **R5 装饰补偿心理**：「要高级感」回应以渐变/玻璃/发光堆料而非留白/对齐/字阶（[SD-18] 防御）。

最隐蔽的是状态缺失：无错误截图、静默通过验收、上线才暴露——比「难看」更危险。

## 参数速查表

### 设计令牌分层结构

| 层 | 职责 | 示例 | 硬规则 |
|---|---|---|---|
| Primitive/Global | 原始值，只说「是什么」 | `--blue-500: #3B82F6`、`--space-4: 16px` | 组件 NEVER 直引此层 |
| Alias/Semantic | 语义名，说「做什么用」 | `--color-action: var(--blue-500)` | 主题/暗色在此层换绑 |
| Component | 组件级，说「哪个组件用」 | `--button-primary-bg: var(--color-action)` | 引用链 ≤2 层 |

### 状态清单（9 态）

| 状态 | 适用组件 | 实现要点 |
|---|---|---|
| default | 全部 | 基线样式 |
| hover | 指针设备 | 包 `@media (hover: hover) and (pointer: fine)` |
| focus-visible | 键盘聚焦 | outline ≥2px、对比 ≥3:1、offset 防同色淹没 |
| active | 按下瞬态 | 视觉强度应 ≥ hover（防倒挂）；自定义按钮必备 press state（[SD-35]） |
| disabled | 全部 | `disabled` 属性/`aria-disabled` + JS 拦截，NEVER 仅 opacity |
| error | 表单类 | 颜色 + 图标 + 文字 + `aria-invalid` 多通道 |
| loading | 异步动作类 | disabled + Spinner，与纯灰禁用区分 |
| selected/checked | 选择类 | 持久态，强度区别于 active 瞬态 |
| readonly | 输入类 | 视觉弱于可编辑但可读屏 |

数据展示类另加：空态/骨架屏/错误态（重试入口）（[SD-1]）。

### 圆角刻度速查

| token | 值（可调） | 用途 |
|---|---|---|
| `--radius-sm` | 4px | 输入框/小按钮 |
| `--radius-md` | 8px | 卡片内元素 |
| `--radius-lg` | 12px | 卡片 |
| `--radius-full` | 9999px | 胶囊/头像 |

规则：3~4 档封顶，同类同档；具体值是风格参数，离散与同档是纪律（[SD-7]）。

### 阴影 elevation 档位速查

| token | 值 | 组件角色 |
|---|---|---|
| `--shadow-1` | `0 1px 2px rgba(0,0,0,.05), 0 1px 3px rgba(0,0,0,.1)` | 卡片 |
| `--shadow-2` | `0 4px 6px rgba(0,0,0,.05), 0 2px 4px rgba(0,0,0,.06)` | sticky 导航 |
| `--shadow-3` | `0 10px 15px rgba(0,0,0,.1), 0 4px 6px rgba(0,0,0,.05)` | 下拉/浮层 |
| `--shadow-4` | `0 25px 50px -12px rgba(0,0,0,.25)` | 模态 |

易错点：`box-shadow` 参数序 `offset-x offset-y blur spread color`；多阴影逗号分隔、**第一个在最上层**；`drop-shadow()` 跟随非矩形轮廓；`backdrop-filter` ≠ `filter`。

### 间距 / 动效 token 速查

| 类别 | 刻度 |
|---|---|
| 间距（4px 网格） | `--space-1:4px` ~ `--space-16:64px`（4/8/12/16/24/32/48/64） |
| 时长 | `--duration-fast: 150ms`（微反馈 100~150）/ `--duration-base: 200ms`（常规 200~250）/ `--duration-slow: 400ms`（大区域 300~500） |
| 缓动（≤3 条） | `--ease-out: cubic-bezier(0.16,1,0.3,1)` / `--ease-in-out: cubic-bezier(0.65,0,0.35,1)` |
| 行高（无单位） | tight 1.25 / normal 1.5 / loose 1.75 |
| 文字三级 | primary `#111827` / secondary `#4b5563` / tertiary `#9ca3af`（tertiary 需对比度检查） |

### Apple HIG 平台规格速查（R34 实抓 [官方文档]）

**表 A：各平台默认/最小字号（pt）与控件尺寸（pt）** [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/typography.md)、[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/accessibility.md)

| 平台 | 默认字号 | 最小字号 | 控件默认 | 控件最小 |
|---|---|---|---|---|
| iOS/iPadOS | 17 | 11 | 44×44 | 28×28 |
| macOS | 13 | 10 | 28×28 | 20×20 |
| tvOS | 29 | 23 | 66×66 | 56×56 |
| visionOS | 17 | 12 | 60×60 | 28×28 |
| watchOS | 16 | 12 | 44×44 | 28×28 |

命中区域：交互控件 ≥44×44pt（visionOS 60×60pt）[SD-33]；带边框元素周围约 12pt padding、无边框约 24pt padding。

**表 B：对比度、缩放与 Dark Mode 矩阵** [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/dark-mode.md)、[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/accessibility.md)

| 项 | 数值/规则 |
|---|---|
| 对比度底线 | 前景/背景 ≥4.5:1；自定义颜色力求 7:1 |
| 平台分档 | ≤17pt 全字重 4.5:1；18pt 全字重 3:1；Bold 全字号 3:1 |
| 文本缩放 | 至少 200%（watchOS 至少 140%）；Dynamic Type 档位 xSmall→xxxLarge + AX1~AX5 |
| Dark Mode 支持平台 | iOS/iPadOS/macOS/tvOS；**不支持 visionOS/watchOS**（visionOS 用自适应 glass 材质） |
| 测试矩阵 | light/dark/Auto × Increase Contrast × Reduce Transparency（单独与组合；Auto 可能运行中切换）[SD-27] |
| 深色背景组 | base（更暗、后退）/ elevated（更亮、前进）；模态前台 base 自动变 elevated [SD-29] |

**表 C：布局与安全区** [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/layout.md)

| 平台 | 关键数值 |
|---|---|
| tvOS | 安全区：主内容距上下 60pt、左右 80pt；网格水平间距 40pt、最小垂直间距 100pt；两列 860pt → 九列 160pt 递减 |
| visionOS | 按钮中心间距 ≥60pt；按钮五档 Mini 28 / Small 32 / Regular 44 / Large 52 / Extra large 64（圆形全档、文本胶囊 32 起、图文胶囊仅 44/52、圆角矩形 32~52）；≥60pt 按钮周围加 4pt padding |
| watchOS | 每行 ≤2~3 个控件（glyph 按钮 ≤3 并排、文本按钮 ≤2）；文本按钮通常占满全宽 |
| macOS | 避免控件/关键信息放窗口底部（用户常把底边移出屏幕）；避免内容置于顶部摄像头区域之后 |

**表 D：Dynamic Type 与 Text Styles（iOS/iPadOS，Large 默认档，size/leading pt）** [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/typography.md)

| Style | 字重 | Size/Leading | Emphasized |
|---|---|---|---|
| Large Title | Regular | 34/41 | Bold |
| Title 1 | Regular | 28/34 | Bold |
| Title 2 | Regular | 22/28 | Bold |
| Title 3 | Regular | 20/25 | Semibold |
| Headline | Semibold | 17/22 | Semibold |
| Body | Regular | 17/22 | Semibold |
| Callout | Regular | 16/21 | Semibold |
| Subhead | Regular | 15/20 | Semibold |
| Footnote | Regular | 13/18 | Semibold |
| Caption 1 | Regular | 12/16 | Semibold |
| Caption 2 | Regular | 11/13 | Semibold |

- 缩放档：xSmall（Body 14）→ Large（默认，Body 17）→ xxxLarge（Body 23）→ AX1（Body 28）→ AX5（Body 53/62）；Text Styles = 字重+字号+行距组合，随 Dynamic Type 联动缩放。
- 其他平台默认档：macOS Body 13/16（Headline Bold 13）；tvOS Body 29/36（Title 1 76）；watchOS Body 15~17（随表径 38→49mm）。
- Tracking 关键值（1/1000em）：SF Pro 12pt 为 0、17pt 为 -26、80pt+ 为 0；SF Pro Rounded 17pt 为 +22；New York 15pt 为 0、大字号转负（200pt -17）；macOS/tvOS 与 SF Pro 表一致；全表见 corpus hig/typography.md。
- 字重纪律：一般避免细字重（Ultralight/Thin/Light），系统字体优先 Regular/Medium/Semibold/Bold；三行以上文本避免 tight leading，宽列/长文用 loose leading；强调字重（emphasized）2025-12-16 加入规格。

**表 E：系统色与语义动态色** [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/color.md)

- 13 系统色（Red/Orange/Yellow/Green/Mint/Teal/Cyan/Blue/Indigo/Purple/Pink/Brown）+ Gray 1~6，每色 4 变体（default light/dark + increased contrast light/dark）；visionOS 用 dark 列。完整 RGB 表见 corpus hig/color.md（禁止硬编码进产品 [SD-26]）。
- 前景动态色：label/secondaryLabel/tertiaryLabel/quaternaryLabel/placeholderText/separator/link；背景两组：system（primary/secondary/tertiary）与 grouped（primary/secondary/tertiary）。
- 色彩管理：通用 sRGB；广色域 Display P3（16 bits per pixel per channel）；P3 渐变在 sRGB 屏可能被裁剪，必要时 asset catalog 提供双色彩空间版本。
- 包容性：同一颜色禁止表示不同含义；跨文化颜色含义（如股票涨跌红绿相反地区）；不能仅靠颜色传达信息（与 [SD-12] 同向）。

**表 F：材质档位** [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/materials.md)

| 项 | 档位/规则 |
|---|---|
| Liquid Glass 变体 | regular（模糊+亮度调节，文本多组件：alerts/sidebars/popovers）/ clear（高透明，悬浮富媒体之上，+35% 黑 dimming 兜底） |
| 使用边界 | 仅控件与导航功能层；内容层禁用（例外：sliders/toggles 激活时）；节制使用，自定义控件谨慎 [SD-24] |
| iOS 标准材质四档 | ultra-thin / thin / regular（默认）/ thick；厚材质配细文字、薄材质保上下文 [SD-25] |
| vibrancy 文字四级 | label / secondaryLabel / tertiaryLabel / quaternaryLabel（quaternary 禁用于 thin/ultraThin） |
| visionOS | 窗口默认不可修改 glass 材质（自适应环境亮度）；自定义组件 thin=强调交互 / regular=视觉分隔 / thick=深色区分 |
| watchOS | 全屏模态用系统材质提供上下文，不要移除/替换模态 sheet 默认材质背景 |

**表 G：app 图标规格** [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/app-icons.md)

| 平台 | 图层尺寸（px） | 遮罩后形状 | 外观变体 |
|---|---|---|---|
| iOS/iPadOS/macOS | 1024×1024 | 圆角方形 | default/dark/clear light/clear dark/tinted light/tinted dark |
| tvOS | 800×480（2~5 层视差） | 圆角矩形 | N/A |
| visionOS | 1024×1024（背景+1~2 上层 3D） | 圆形 | N/A |
| watchOS | 1088×1088 | 圆形 | 同 iOS 族 |

- 前景层边缘清晰（忌柔和羽化）；背景层全出血不透明；主要内容居中；提供未遮罩原始图层（[SD-36]）；支持 sRGB / Gray Gamma 2.2 / Display P3。

**表 H：菜单/文本字段/滑杆组件速查** [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/menus.md)、[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/text-fields.md)、[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/sliders.md)

| 组件 | 关键规格 |
|---|---|
| 菜单 | 动词标签 + 省略号纪律；重要项列前；子菜单 ≤1 级、>5 项建新菜单（[SD-37]）；iOS 布局三档：Small（顶行 4 图标）/ Medium（顶行 3 图标+短标签）/ Large（默认全列表）；切换项用可变标签（Show↔Hide）+ checkmark |
| text field | 占位符 ≠ 标签；secure field 敏感数据；字段宽度匹配预期输入量；多字段纵向堆叠、同宽分组；失焦校验邮箱、提交前校验密码（[SD-38]）；数字用 formatter；按内容匹配键盘类型 |
| slider | 水平最小值在 leading；宽范围配 text field + stepper；tvOS 不支持（[SD-39]）；macOS 水平=固定起止点、圆形=循环/无限值；tooltip 显示当前值；watchOS 离散步进或连续条 |

## 版本注意

**有文档佐证（R34 阶段 A 实抓，2026-11-16）**：
- Apple HIG 深层主题页 `.md` 版现已全部可稳定抓取（URL 规律 `https://developer.apple.com/design/Human-Interface-Guidelines/<topic>.md`，topic 为 kebab-case）；R33「深层页 404」记载过时，旧式 HTML URL 仍 404。
- 已抓 12 主题页（11 入本域 + motion 入 interaction-motion 域，见来源索引）；Tooltips 404（新版并入 "Offering help" 页）——offering-help.md 已于 R40 补抓（2026-11-17，见下）。
- 强调字重（emphasized weight）于 2025-12-16 加入 HIG 字体规格。
- m3.material.io 仍为 JS 渲染站点无法抓取——**本文件不引用任何 m3 URL**；M3 具体参数不收录。

**有文档佐证（R39 增量实抓，2026-11-17）**：
- **iPhone Duo**：Apple 首款折叠双屏 iPhone；HIG 新页 "Designing for iPhone Duo"（2026-09-09）——device poses、双屏动态布局、reserved regions、arrangement views、垂直控件轴（[SD-40]~[SD-43]）；相关 Tech Talks "Design for iPhone Duo"。
- **macOS touch input**：Gestures 页 2026-10-28 更新——touch 为 Mac（触屏/Sidecar iPad）副输入模式（[SD-44]）。
- 2026-09 系版本事件（iOS/iPadOS 27、macOS 27 UI Kit、SF Symbols 8、Icon Composer 2、iPhone 18/Duo 产品 bezels）本轮仅登记不锚定参数；M3 Expressive 仍因 m3.material.io JS 渲染无法官方锚定。

**有文档佐证（R40 收尾实抓，2026-11-17）**：
- **Offering help**（Tooltips 并入页补抓）：Tips/TipKit 与 macOS·visionOS tooltip（help tag）纪律（[SD-46][SD-47]）。
- **Snippets**（HIG 新页 2026-06-08）：Siri/App Shortcuts confirmation/result 两型视图、custom view ≤400pt、描述性主按钮标签（[SD-48]）。
- **Design principles**（2026-06-08 重新引入）：Apple 设计八原则官方锚点（[SD-45]）。
- **Pointing devices**（2026-10-28 更新）：iPadOS highlight/lift/hover 三效应、命中区 12/24pt（与 [SD-33] 交叉印证）、macOS touch 隐藏控件唤出、visionOS 指针（[SD-49]）。
- m3.material.io 复试仍为 JS 渲染站点（"This website requires JavaScript."）——M3 Expressive 维持降级记录，不入硬事实。

**未经文档验证的版本敏感点（[模型经验]，落地前查证）**：
- W3C Design Tokens Format Module：`$value`/`$type` 语法记忆模糊，采用前必须查证草案/CR 原文。
- 浏览器兼容基线待验证：`backdrop-filter`（记忆 Firefox 约 103 启用）、Safari `-webkit-` 前缀、`:focus-visible`（记忆 Safari 15.4）、`:user-invalid`、`color-mix()`、相对颜色语法、`size-adjust`/`ascent-override`、`@property`；策略统一 `@supports` 降级。
- Tailwind v3/v4 类名-值映射有变动（`rounded-lg`/`shadow-md` 因版本而异），引用工具类须标注版本；Bootstrap 5 主色 `#0d6efd`、MUI elevation 0~24 档为记忆值。
- 时效声明：`backdrop-filter` 性能、社区风格词（Neubrutalism/Claymorphism/Y2K）、Liquid Glass 演变快，趋势敏感。

## 与其他子领域的集成要点

- **color-system**：primitive 色板、色板生成（OKLCH/tonal palette）、对比度与档位推导由其承担；本文件消费 primitive 建 alias 并持有 [SD-16]；tone shift 具体调法在其 kb；Apple 系统色 13 色 + Gray 1~6 全表在其域引用本域 corpus（hig/color.md）。
- **typography**：modular scale 比率选择、`font-display`/回退链/`size-adjust`、可变字体由其展开；本文件约束「字阶 token 化 + 无单位行高」（[SD-6]）并提供 HIG Dynamic Type 平台规格锚点（表 D）。
- **layout-composition**：网格档位应用、间距动机化布局、断点 token 归其展开；本文件定义 token 分层架构（[SD-4]）与基准唯一纪律（[SD-5]）；size class/safe area 数值（表 C）供其引用。
- **interaction-motion**：状态集（9 态）与完备性是本文件的「状态定义」；动效实现（transition 白名单、进场编排、缓动）由其展开；动效 token 分档共用；HIG motion 语料（interaction-motion/docs/hig/motion.md）归其域。
- **usability-accessibility**：对比度 WCAG 对应（4.5:1/3:1 分档 [SD-28]）、文本缩放 200% [SD-34]、命中区域 [SD-33] 在本文件为平台规格锚点，Web 侧 WCAG/ARIA 纪律由其 kb 展开。
- **patterns**：菜单/表单/滑杆的交互行为模式（键盘导航、ARIA）由其 kb 展开；本文件持有 HIG 组件规格值（表 H）。

## 来源索引

官方文档（R34 阶段 A 实抓，白名单 Apple HIG，2026-11-16）：
- https://developer.apple.com/design/Human-Interface-Guidelines/typography.md （各平台字号/Dynamic Type 全档/Text Styles/tracking 表）
- https://developer.apple.com/design/Human-Interface-Guidelines/color.md （13 系统色 + Gray 1~6 RGB 表/语义动态色/P3 色彩管理）
- https://developer.apple.com/design/Human-Interface-Guidelines/materials.md （Liquid Glass/标准材质四档/vibrancy）
- https://developer.apple.com/design/Human-Interface-Guidelines/dark-mode.md （4.5:1/7:1/base-elevated/测试矩阵）
- https://developer.apple.com/design/Human-Interface-Guidelines/layout.md （size class/safe area/tvOS 60-80pt/visionOS 60pt）
- https://developer.apple.com/design/Human-Interface-Guidelines/app-icons.md （分层图标/尺寸表/六种外观）
- https://developer.apple.com/design/Human-Interface-Guidelines/accessibility.md （对比度分档/控件尺寸表/文本缩放 200%/140%）
- https://developer.apple.com/design/Human-Interface-Guidelines/buttons.md （44×44 命中区/prominent 1~2/visionOS 五档）
- https://developer.apple.com/design/Human-Interface-Guidelines/menus.md （标签/组织/子菜单 ≤1 级/布局三档）
- https://developer.apple.com/design/Human-Interface-Guidelines/sliders.md （方向惯例/stepper 配套/tvOS 不支持）
- https://developer.apple.com/design/Human-Interface-Guidelines/text-fields.md （占位符/secure field/校验时机）
- https://developer.apple.com/design/Human-Interface-Guidelines/designing-for-iphone-duo.md （iPhone Duo：poses/reserved regions/arrangement views/垂直控件轴；R39 增量，2026-09-09 新页）
- https://developer.apple.com/design/Human-Interface-Guidelines/gestures.md （macOS touch input 副输入模式/expandable controls/trackpad-touch 手势对照；R39 增量，2026-10-28 更新）
- https://developer.apple.com/design/Human-Interface-Guidelines/design-principles.md （Apple 设计八原则：Purpose/Agency/Responsibility/Familiarity/Flexibility/Simplicity/Craft/Delight；R40 收尾，2026-06-08 重新引入）
- https://developer.apple.com/design/Human-Interface-Guidelines/offering-help.md （Tips/TipKit 资格规则与频率/tooltip 60~75 字符纪律；R40 收尾，Tooltips 并入页）
- https://developer.apple.com/design/Human-Interface-Guidelines/snippets.md （Siri/App Shortcuts snippet 两型/400pt 上限/描述性按钮标签；R40 收尾，2026-06-08 新页）
- https://developer.apple.com/design/Human-Interface-Guidelines/pointing-devices.md （iPadOS highlight/lift/hover 三效应/命中区 12-24pt/macOS touch 隐藏控件；R40 收尾，2026-10-28 更新）
- https://developer.apple.com/design/human-interface-guidelines.md （HIG 根 `.md` 索引）
- https://developer.apple.com/design/human-interface-guidelines/ （HIG 入口页）

模型经验（阶段 1 萃取，未经逐条文档验证）：E1~E8 对应 elicited/01~08。

抓取记录：corpus/ui-ux-design/style-design-system/docs/_fetch_log.md（R33：HIG 深层页 404 旧记载）、_fetch_log_r34-hig.md（R34：12 主题页实抓成功记录、URL 规律、Tooltips 404）、_fetch_log_r39-refresh.md（R39：iPhone Duo 新页 + gestures macOS touch 增量、HIG whats-new 版本检测）、_fetch_log_r40-cleanup.md（R40：offering-help/snippets/design-principles/pointing-devices 收尾、m3 复试仍失败）。

验证声明：本文件 [SD-24]~[SD-49] 及参数速查表 A~H 均经 Apple HIG 主题页（R34/R39/R40 实抓）逐字锚定；[SD-1]~[SD-23] 源自模型萃取；具体版本号/第三方库默认值已显式标注「未经文档验证」。

## 冲突消解记录

1. **M3 elevation 档位与阴影值**：模型原认知（M3 5 级 elevation + surface tint）→ m3.material.io 无法抓取，无对照 → 不收录 M3 参数，禁用一切 m3 URL；elevation 用「离散档位 + 组件角色绑定」表述。
2. **HIG 深层定义引用（R33，已被 #4 更正）**：深层页 404/JS 页，仅根 `.md` 索引稳定可抓 → [官方文档] 标注曾仅限根索引 URL。
3. **`backdrop-filter` 浏览器版本号**：无兼容文档被抓取，版本主张无佐证 → 不写具体版本号，兼容策略统一为 `@supports` 降级 + 「版本注意」声明待验证。
4. **HIG 深层页可抓性（R34 更正 #2）**：R33 记载「深层页 404、仅根索引可作 [官方文档]」→ R34 实测 `<topic>.md` 模式（`Human-Interface-Guidelines/<topic>.md`，kebab-case）12 主题页全部可抓，含完整 Specifications 数值表（_fetch_log_r34-hig.md）→ 引用纪律更新：HIG 主题页 URL 可作 [官方文档] 来源；本文件所有 HIG 事实升格为主题页锚定；旧式 HTML URL 仍 404。
5. **玻璃拟态 vs Liquid Glass 分层**：模型原认知（玻璃拟态=任意半透明模糊层叠内容之上）→ HIG 明确 Liquid Glass 为控件/导航功能层专用、内容层禁用（例外：瞬时交互控件激活时）→ 场景 6 补充分层纪律 [SD-24]；Web 玻璃拟态无系统滚动边缘效应，可读性需自验，两语境不混同。
6. **Dark Mode 平台支持矩阵**：模型记忆中深色模式为现代平台通用能力 → HIG 明确不支持 visionOS/watchOS（visionOS 用自适应 glass 材质替代，无独立 Dark Mode）→ 表 B 记录支持矩阵，跨平台设计系统不假设全平台深色。
7. **R39 增量合并（无证伪，纯新增）**：iPhone Duo（HIG 新页 2026-09-09）与 macOS touch input（Gestures 2026-10-28）为纯新增锚定（[SD-40]~[SD-44]），与既有条目无冲突；[SD-31] size class 纪律被新形态强化（outer=compact/inner=regular 是其在折叠双屏上的实例），保留原文未改。
8. **R40 收尾增量（无证伪，纯新增）**：offering-help（Tooltips 并入页补抓）、snippets（2026-06-08 新页）、design-principles（2026-06-08 重新引入）、pointing-devices（2026-10-28 更新）为纯新增锚定（[SD-45]~[SD-49]）；R34「Tooltips 404」记载更新为「已补抓 offering-help.md」；m3.material.io 复试仍 JS 失败，#1 M3 降级决定维持；pointing-devices 命中区 padding 12/24pt 与 [SD-33]（accessibility.md）数值一致，交叉印证保留原文。
