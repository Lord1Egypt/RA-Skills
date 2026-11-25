---
domain: ui-ux-design
skill_name: ui-ux-design-expert
subdomain: visual-perception
title: 视觉感知与认知法则（人类怎么看界面）
version: 2
updated: 2026-11-16
source_index:
  - https://lawsofux.com/ 30 法则逐页（docs/laws/×29 + fittss-law.md + lawsofux-index.md）
  - https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/ 与 /banner-blindness-old-and-new-findings/
  - corpus/ui-ux-design/visual-perception/elicited/01~09
knowledge_ratio: "法则 ~18% / 最佳实践 ~42% / 坑点 ~40%"
merged_at: 2026-11-16
---
# 视觉感知与认知法则

## 定位与心智模型

UI/UX 最底层根因层：**人怎么看界面**，下游供给全部子领域。三条主线：①**分组机器**——感知先于语义，先见「块」再读「字」，分组优先级 间距>背景>边框，线索冲突取最强；②**注意力稀缺**——层次是给视线修路，扫描模式由内容诱发非指令；③**美观放大感知、不修复行为**——美学-可用性效应只污染感知与自述，不污染行为数据。Laws of UX 30 法则已逐页全量锚定 [官方文档](https://lawsofux.com/)（语料 docs/laws/，速查表见参数区）。

## 法则

[VP-1] [GLOBAL] **MUST**: 组间间距 ≥2× 组内；间距取自离散刻度（4/8/16/24/48/64）；组间/组内/同级不得同值。违反→分组不可辨、扫读成本陡增。溯源: [官方文档](https://lawsofux.com/law-of-proximity/)（邻近分组）+ [模型经验] 01（2×/刻度）

[VP-2] [GLOBAL] **MUST**: 每视图至多一个视觉焦点（唯一实心主 CTA 或唯一最重元素）。违反→注意力分散、主任务转化下降。溯源: [官方文档](https://lawsofux.com/von-restorff-effect/)（独特者被记住）+ [模型经验] 02

[VP-3] **MUST**: 不同重要级操作以视觉重量档位区分（实心/描边/文本），不得仅靠色相。违反→误判操作等级。溯源: [官方文档](https://lawsofux.com/law-of-similarity/)（相似=同组）+ [模型经验] 01

[VP-4] **NEVER**: 危险操作不得为同屏最醒目操作，且须与确认操作有位置或样式隔离。违反→被引导点删除/取消（AI 高频：红实心「取消」+灰描边「确认」）。溯源: [官方文档](https://lawsofux.com/von-restorff-effect/)（隔离推荐项；强调保持克制防误认广告、勿仅靠颜色）+ [模型经验] 06

[VP-5] [GLOBAL] **MUST**: 可交互命中区 ≥24×24 CSS px（移动触控 ≥44×44），可用透明 padding 扩展超出视觉尺寸，目标间留足间距。违反→触控/指针连点不中。溯源: [官方文档](https://lawsofux.com/fittss-law/)（takeaways）；24/44/48=WCAG 2.5.8/Apple 44pt/Material 48dp [模型经验] 03，未验证

[VP-6] [GLOBAL] **NEVER**: 不得以 placeholder 充当 label；每字段有持久可见标签。违反→聚焦后提示消失、自动填充后无法核对。溯源: [模型经验] 05（识别优先于回忆，见 [VP-39]）

[VP-7] **MUST**: 正文对比度 ≥4.5:1；文本层级用预定义色阶 token（gray-900/600/500），最浅档（gray-400 以下）仅限禁用/占位。违反→可读性崩塌。溯源: [模型经验] 02（4.5:1 为 WCAG 共识）

[VP-8] [GLOBAL] **MUST**: 承载动态文本的容器不得固定高度；动态文本须有截断策略（line-clamp / ellipsis + min-w-0）。违反→真实数据溢出破版。溯源: [模型经验] 06

[VP-9] **MUST**: 遮罩以不透明度 ≥0.4 的 scrim（或等效模糊）建立图底分离；暗色用表面色阶（#0a0a0a→#171717→#262626）表达层级，不依赖阴影。违反→弹窗浮不起来、暗色糊成一片。溯源: [模型经验] 01（scrim 0.4~0.6）

[VP-10] **MUST**: 标题自解释且关键词前置（前 2 词承载信息），禁纯装饰标题（「欢迎！」「了解更多」）。违反→扫读抓不到信息。溯源: [官方文档](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)（解药 3：标题前 2 词承载大意）+ [模型经验] 02

[VP-11] **NEVER**: 关键操作不得仅 hover 显现；hover 可见性以 `@media (hover: hover)` 限定并提供触屏等价路径。违反→触屏上功能不存在。溯源: [模型经验] 06

[VP-12] [GLOBAL] **MUST**: 列表/导航/下拉中高频或关键项置于首位或末位，不埋长列表中部；关键操作放导航最左与最右。违反→序列位置效应下被忽略。溯源: [官方文档](https://lawsofux.com/serial-position-effect/)（首因+近因；最左最右记忆度最高；最不重要项放中部）

[VP-13] **NEVER**: 多步流程不得以错误状态收尾；校验就地（inline 字段级）反馈，不得仅流程末尾错误墙。违反→峰终定律下整段体验被终点失败定性。溯源: [官方文档](https://lawsofux.com/peak-end-rule/)（Kahneman et al. 1993 冷水实验；负面记忆更鲜明）+ [模型经验] 05（onblur 惯例）

[VP-14] [GLOBAL] **MUST**: 核心导航与操作模式循平台惯例（logo 左上回首页、下划线链接、汉堡=菜单、弹窗右上 ×、移动底部 tab），偏离须有数据或场景理由；重大变更允许用户有限时间内继续使用熟悉版本。违反→Jakob's Law 违背、学习成本转嫁。溯源: [官方文档](https://lawsofux.com/jakobs-law/)（期望迁移；YouTube 2017 改版先预览后切换）

[VP-15] [GLOBAL] **MUST**: 状态不得仅用颜色传达，须同配图标或文本。违反→色觉障碍用户（男性约 8%）不可辨。溯源: [模型经验] 06（WCAG 1.4.1）；[官方文档](https://lawsofux.com/von-restorff-effect/)（强调勿仅靠颜色，同向）

[VP-16] **MUST**: 单屏字体家族 ≤2；可辨字阶 ≤5 级且相邻级差过 [VP-21] 阈值。违反→层次信号淹没。溯源: [模型经验] 02（比例 1.125/1.25/1.333/1.5）

[VP-17] **MUST**: 动画仅作用于 transform/opacity，微交互 150~300ms，须响应 prefers-reduced-motion。违反→掉帧+前庭障碍用户眩晕。溯源: [模型经验] 06

[VP-18] [GLOBAL] **MUST**: 首屏一眼答三问——这是什么（品类）、对我何用（≤2 行）、下一步（唯一主 CTA）。违反→50ms 首评失败、跳出率升。溯源: [官方文档](https://lawsofux.com/aesthetic-usability-effect/)（Kurosu & Kashimura 1995：26 ATM 变体×252 人，美观度与感知易用性相关性强于与实际易用性）+ [模型经验] 04（三问；50ms=Lindgaard 2006 未验证）

[VP-19] **NEVER**: 分组不得边框优先——顺序 间距>背景/分隔线>边框容器；边框与背景是官方共同区域标准手法，边框仅用于语义独立对象，嵌套 ≤2 层。违反→卡片汤。溯源: [官方文档](https://lawsofux.com/law-of-common-region/)（边框/背景创建共同区域）+ [模型经验] 01（优先级为视觉税推论）

[VP-20] **MUST**: 生成的每个数据视图含加载/空/错误三态，除非用户明确只要静态视觉稿。违反→真实环境白屏/裸报错。溯源: [模型经验] 06

[VP-21] [GLOBAL] **MUST**: 层级/类别/状态差异至少过一个强通道阈值（字号比 ≥1.2/字重跨 400→600/色阶跳档/实心 vs 描边），轻微不同=错误。违反→层级不可辨。

[VP-22] **NEVER**: 不得以增加色相制造对比；单视图功能色 ≤5，装饰色不承载层级/焦点。违反→焦点失守、语义崩坏。

[VP-23] [GLOBAL] **MUST**: 先建可枚举 token（色板/字阶/间距/圆角/阴影），样式值全引用 token；同语义变量禁多个「近似值」。违反→实例漂移、系统性崩坏。

[VP-24] **MUST**: 同语义组件复用同一实现；圆角/内边距/图标风格全实例一致；一套图标一种风格，禁混 emoji。违反→跨实例学习失效。

[VP-25] [GLOBAL] **MUST**: 每元素与 ≥1 其他元素共享对齐轴线；同容器对齐方式 ≤2 种且服务同一意图。违反→轴线打架、视线无滑行路径。

[VP-26] **NEVER**: >3 行正文段落不得居中；居中仅限短标题（≤2~3 行）与孤立展示元素。违反→扫读动线锯齿化。

[VP-27] **NEVER**: 不得为「填满空间」对语义无关项用 space-between/等距分布；组间间距不得等于组内（[VP-1] 联动）。违反→均匀分布病。

[VP-28] **MUST**: 网格卡片底部操作区以 `margin-top:auto` 锚定；混排字号 baseline 对齐；数字列 tabular-nums+右轴。违反→按钮漂移、数字轴锯齿。

[VP-29] [GLOBAL] **MUST**: 骨架屏与真实内容一一对应（块数/位置/高度差 ≤8px），中性色，禁装饰性骨架。违反→加载完成跳版。

[VP-30] **MUST**: sticky/fixed 具备不透明或半透明+blur 背景，滚动内容不穿透。违反→图底失守、可读性事故。

[VP-31] [GLOBAL] **MUST**: 文字直接叠图必须加 overlay/压暗，对背景任意区域对比 ≥4.5:1；禁裸字压图。违反→图底不分、不可读。

[VP-32] **MUST**: 列表重排（删除/拖拽/筛选排序）以 FLIP/共同运动动画外显；marquee 框选命中项与选框同帧高亮。违反→空间地图丢失。

[VP-33] **MUST**: 勾选/选中态同帧反映到整行/整卡（背景+勾选框双通道），不得仅变勾选框。违反→扫视列表时选中态不可见。

[VP-34] **MUST**: 同组入场动画 stagger ≤50ms/项、组总时长 ≤600ms；同界面同类过渡时长一致。违反→整体感瓦解为「逐个事件」。

[VP-35] **NEVER**: z-index 必须来自分层 token（dropdown<sticky<overlay<toast 量级），禁魔法值；新增层须携带可见背景/边界差异。违反→层序事故。

[VP-36] **MUST**: 树形/时间线连接线连续且与缩进刻度严格一致（每层等距）；连接线与容器边框不得双重表达同一分组。违反→层级混乱、线索冗余。

[VP-37] **NEVER**: 重要内容不得具备广告三特征——广告位位置（页顶横幅/右侧栏）、广告式视觉处理（动画、与上下文差异突出的大图）、与真实广告/推广相邻；内容与广告不得混排同一视觉区块。违反→横幅盲视过滤（右侧栏注意力可低至面积占比 1/33；跨 3 个十年 1997/2007/2018 证实的强健现象）。溯源: [官方文档](https://www.nngroup.com/articles/banner-blindness-old-and-new-findings/)（三特征/烫手山芋扫视/0.8% vs 25% 面积）

[VP-38] **MUST**: 文字密集页按 F 解药处理——最重要要点放前两段、标题比正文醒目且前 2 词承载信息、加粗关键词、边框/背景视觉分组、列表化、删减冗余。F 型是「文字墙+高效意图+低投入」三条件齐备时的默认最小努力路径，对用户和企业都是坏事（用户漏看右侧且不自知）。违反→F 型扫读吃掉右侧内容。溯源: [官方文档](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)（解药八条；RTL 语言呈镜像 F）

[VP-39] **MUST**: 关键信息跨屏由系统携带（对比表、面包屑、已访问链接视觉区分），识别优先于回忆；工作记忆任一时刻仅容 4~7 组块、每组块 20~30 秒消退。违反→跨屏丢上下文、强迫回忆。溯源: [官方文档](https://lawsofux.com/working-memory/)（4~7 组块×20~30s；记忆负担放系统不放用户）

[VP-40] **MUST**: 多步流程与清单提供清晰进度指示；可用人为初始进度（artificial progress）提升完成动机——越接近目标推进越快。违反→中途弃单。溯源: [官方文档](https://lawsofux.com/goal-gradient-effect/)（Hull 1932/1934；人为初始进度）+ [官方文档](https://lawsofux.com/zeigarnik-effect/)（未完成任务记忆更牢、进度激励完成）

[VP-41] **MUST**: 输入宽容、发送保守（Postel/鲁棒性原则）——接受用户可变输入并转换为标准格式、划定输入边界、给清晰反馈；系统输出/导出严格符合规范。违反→用户被格式拒绝、集成方解析失败。溯源: [官方文档](https://lawsofux.com/postels-law/)

> VP-21~28 溯源 [模型经验] 08；VP-29~36 溯源 [模型经验] 09（corpus 路径见 source_index；1.2/8px/50ms/600ms 为经验值）；VP-37~41 溯源 R34 全量文档（lawsofux/NN/g 语料）。

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| 格式塔原则 | 大脑自动把视觉场组织为「块」（1910 Wertheimer 铁路道口灯光观察起源；分组五类：接近/相似/连续/闭合/连接+共同区域） [官方文档](https://lawsofux.com/law-of-pr%C3%A4gnanz/) |
| 图底关系 | 前景与背景分离（scrim/表面色阶的感知基础） |
| 视觉重量 | 尺寸×对比×位置×留白 |
| 扫描模式 | NN/g 官方清单：F 型/层叠蛋糕（只扫标题）/斑点式（跳读找特定元素）/标记式（眼停一处靠滚动翻页，移动端多）/绕过式（跳过列表项相同开头词）/投入式（高动机全读，勿指望）；内容诱发非指令 [官方文档](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)；Z 型无官方支持 |
| UX 定律速记 | Proximity/Similarity/Common Region=分组三线索；Hick 选项↔时间对数；Fitts 距离↔大小；Miller 7±2（教训=组块化非「≤7」教条）；Von Restorff 同质中独特者被记住；Jakob 期望与熟悉站点一致；Peak-End 峰值+结尾定记忆；Serial 首尾最好；Doherty <400ms 免等待——全表见「Laws of UX 30 法则速查」 |
| 美学-可用性效应 | 美的被感知为更好用——只污染感知不污染行为数据（Kurosu & Kashimura 1995） |
| 认知负荷 | 内在（目标相关信息吸收）应管理、外在（无助于理解的加工）应剔除 [官方文档](https://lawsofux.com/cognitive-load/)；germane 为 [模型经验]（官方页未列，2010s 后有弱化主张） |
| 识别 vs 回忆 | 可见选项只需识别；隐藏选项强迫回忆（[VP-39]） |
| 加工流畅性 | 易加工=「美」；熟悉布局=高流畅性=好感 |
| 渐进披露 | 主选项可见、低频高级项收起 |
| 横幅盲视 | 用户忽略像广告/靠近广告/在广告位的内容——选择性注意实例 [官方文档](https://www.nngroup.com/articles/banner-blindness-old-and-new-findings/) |

## 最佳实践

### 场景：间距系统
路径: 离散刻度三关系各配档位（刻度见参数表）→ 校验组间 ≥2× 组内（[VP-1]）。
- don't: 卡片间/卡片内/区块间全 16px——关系信息清零。
- do: `.card-grid{gap:24px} .card{padding:16px} .card>*+*{margin-top:8px} .section{margin-top:64px}`。
边界: 2× 是惯例非实验值；高密度后台可放宽，「组间>组内」方向不可破。来源: [模型经验] 01。

### 场景：视觉层次
路径: 模块化字阶（[VP-16]）→ 三档文本色阶（[VP-7]）→ 单实心主 CTA，次级描边、三级文本链接（[VP-2]/[VP-3]）。
- don't: 级差 2px 无字重差+gray-400 正文（#9ca3af 白底 ≈2.8:1）。
- do: `body{font-size:16px;line-height:1.5;color:#111827} h1{32px;700} h2{25px;600} h3{20px;600}`；`.text-secondary{#4b5563≥4.5:1} .text-tertiary{#6b7280} .text-disabled{#9ca3af仅禁用}`。
焦点放大器: 主按钮周围留白 ≥ 相邻间距 2 倍。边界: 字重差可辨性与字号成正比——16px 下 400→500 几乎不可辨。来源: [模型经验] 02。

### 场景：CTA 与按钮档位系统
路径: 重要性决策 → 实心/描边/文本三档落位 → 危险操作降权重+二次确认（[VP-3]/[VP-4]）。
- don't: 三个实心 CTA 等权同排（AI 高频：「立即购买」「了解详情」「联系销售」）。
- do: `.btn-primary{background:#2563eb;color:#fff} .btn-secondary{transparent+border #d1d5db} .btn-tertiary{文本链接}`；确认框：确认=实心在右、取消=文本在左；真删除另配输入名称确认。
边界: 破坏性流程可给红色描边危险按钮，但视觉重量仍须弱于主操作。来源: [模型经验] 06。

### 场景：触控/指针目标设计（Fitts's Law）
路径: 视觉与命中尺寸分离 → 命中区 ≥44×44（移动）/≥24×24（桌面）→ 高频操作放易获取区（移动端底部中点最快、贴边目标等效无限深）。
- don't: 24px 图标按钮命中区=视觉区。
- do: `.icon-btn{width:44px;height:44px;display:grid;place-items:center} .icon-btn svg{width:24px;height:24px}`。
数值三标准（未验证）: Apple 44pt / Material 48dp / WCAG 2.2 AA 24×24px（2.5.8）。边界: Fitts≠越大越好，按频率分层；「5→9 翻倍」讹传，log₂ ≈+34%。来源: [官方文档](https://lawsofux.com/fittss-law/) + [模型经验] 03。

### 场景：表单
路径: 外在负荷最密集区——字段最小化 → 能预填的绝不问（自动检测时区/国家/单位；autofill 防任务膨胀）→ label 永久在场（[VP-6]）→ 收窄宽度保邻近 → 按语义分组 → onblur inline 校验+成功态收尾（[VP-13]）→ 进度指示（[VP-40]）。
- don't: placeholder 当 label + 12 字段平铺无分组。
- do: `.form{max-width:560px} label{display:block;font-size:14px;margin-bottom:4px}`；onblur 校验、错误紧贴字段 `<p role="alert">`、正确给 ✓，避免每键入即报错。
边界: 同意类绝不允许默认勾选；默认值只用于「绝大多数人都会选」或可安全反悔项。来源: [模型经验] 05；autofill 要点 [官方文档](https://lawsofux.com/parkinsons-law/)。

### 场景：选项结构（Hick/Miller）
路径: 减少认知负荷=结构化而非删功能 → 默认值覆盖可跳过项 → 组块化输入（格式见参数表）→ 渐进披露只藏「低频+高级」项。
- don't: 注册第一步问 9 个偏好；为凑「7 项」把第 8 项塞「更多」；导出藏三级菜单而首屏摊开 6 个主题切换。
- do: 默认值覆盖 7 个可跳过项只问 2 个必答；导航按语义分组（每组 4~5 项）；导出在主导航、主题收进设置。
边界: Hick 适用菜单扫选，不适用深度语义决策（选保险）；「≤7 项」是组块容量教条化——中等广度（约 4~8 项/层）优于极深结构；响应时间关键时才最小化选项，勿过度简化到抽象（官方同向警告）。来源: [官方文档](https://lawsofux.com/hicks-law/)（Google/Apple TV/Slack 渐进引导例）+ [模型经验] 05。

### 场景：首屏与第一印象
路径: 50ms 只加工三件事——品类识别（原型性）、复杂度、色彩反应 → 首屏答三问（[VP-18]）→ scrim 保图上文本对比 → 控制复杂度（1 主色+1 强调色+中性面，动效 ≤1 处）。
- don't: 白 70% 透明大字叠浅色天空图（对比可能 <2:1）+5 色+玻璃拟态堆「高级感」。
- do: `.hero::before{content:'';position:absolute;inset:0;background:linear-gradient(to bottom,rgba(0,0,0,0.35),rgba(0,0,0,0.65))} .hero h1{color:#fff;font-weight:600}`。
信任微要素: 错别字 0 容忍；真实照片>图库；具体地址/作者；定价透明；具体社交证明（「2,340 家」>「数千家」）；无 Lorem ipsum/假倒计时。边界: 50ms 测吸引力与复杂度，不证明「极简=好」——空荡首屏同样失败。来源: [官方文档](https://lawsofux.com/aesthetic-usability-effect/) + [模型经验] 04。

### 场景：暗色模式
路径: 非纯黑表面（#000 有光晕）→ 表面色阶表达层级（[VP-9]）→ 文本整体提亮（正文 ≥gray-200）→ 弃用阴影。
- don't: 换底色+沿用浅色阴影与灰阶（`#000` 底+`#9ca3af` 正文）。
- do: `.dark body{background:#0a0a0a;color:#e5e7eb} .dark .surface-1{#171717} .dark .surface-2{#262626} .dark .text-muted{#9ca3af}`。
边界: 光晕对散光人群更明显（模型记忆）。来源: [模型经验] 06。

### 场景：扫描模式与信息前载
路径: NN/g 官方扫视模式清单——F 型（三条件：文字墙+高效意图+低投入；默认最小努力路径）、层叠蛋糕（只扫标题/子标题）、斑点式（跳读找特定元素）、标记式（眼停一处靠滚动翻页，移动端多）、绕过式（跳过列表项相同开头词）、投入式（高动机才全读，勿指望）→ 文字密集页按 F 解药八条处理（[VP-38]/[VP-10]）→ 长下拉/底部导航按序列位置排高频项（[VP-12]）→ 重要内容防横幅盲视三特征（[VP-37]）。
- don't: 「在当今快节奏的时代…」开场；国家下拉 200 项按字母、常用国埋中部；把关键功能做成页顶横幅大图/右侧栏动画卡。
- do: 「任务管理工具：3 分钟整理今天待办。」；常用国置顶+字母表在后；底部 tab 核心功能第 1 位；关键内容融入内容流、样式与站点一致。
边界: F 型对用户和企业都是坏事（用户漏看右侧且不自知），解药是消除三条件而非「设计成 F」；RTL 语言呈镜像 F；Z 型不在 NN/g 官方清单，无实证支持；SERP 文字广告例外不盲视。来源: [官方文档](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/) + [官方文档](https://www.nngroup.com/articles/banner-blindness-old-and-new-findings/) + [模型经验] 02。

### 场景：测试与评估
路径: 行为先态度后——直接布置任务（成功/失败/时长/求助次数）→ 再收主观评分 → 追问失败警惕「我觉得挺好的」。
- don't: 演示后问卷「好看吗/好用吗」（美感污染评分，双双失真）。
- do: 任务先行→行为指标→评分殿后；「访谈说好看」与可用性证据严格分离。
边界: 自述被美感污染，行为数据不污染；美观还会掩盖可用性问题使测试更难发现问题（官方同向）。来源: [官方文档](https://lawsofux.com/aesthetic-usability-effect/) + [模型经验] 04。

### 场景：CRAP 四原则自检法
- C 对比: 眯眼后层级消失；修参：字号比 ≥1.2 或字重跨 400→600，多通道叠加（[VP-21]）。
- R 重复: 「近似的蓝」/圆角漂移/图标混风格；修参：样式值全 token 化，长列表每 5~7 项一个节奏单元（[VP-23]/[VP-24]）。
- A 对齐: 容器内 >2 种对齐轴线/按钮随内容漂移；修参：单一强左轴+操作区 `margin-top:auto`（[VP-25]/[VP-28]）。
- P 亲密: 组间==组内间距或 space-between 撑满无关项；修参：组间 ≥2× 组内，先归组再对齐（[VP-27]）。
来源: [模型经验](corpus/ui-ux-design/visual-perception/elicited/08-crap-principles.md)

### 场景：格式塔分组效力应用
效力排序（低置信）: 共同区域>闭合>连通>接近>相似>连续；声明分组用最强线索，歧义清理弱线索（[VP-19]）。
| 需求 | 分组手段 | 法则 |
|---|---|---|
| 并行分组 | 间距（首选）/背景 | [VP-1]/[VP-19] |
| 语义独立对象 | 边框容器（≤3 层） | [VP-19] |
| 显式层级/流程 | 连接线（每层等距，与边框二选一） | [VP-36] |
| 卡内紧凑排版 | 容器分组信用：组内距下探一档 | [VP-1] |
来源: [模型经验](corpus/ui-ux-design/visual-perception/elicited/09-gestalt-full.md)

## 高频坑点

### Top 1：对比度灾难三连
- 症状: hero 副标题渐变上不可读；深色正文暗灰难读。
- 根因: `text-white/60`+`font-weight:300`+14px 三连，AI「氛围感」偏好压过可读性（违反 [VP-7]）。
- don't: `linear-gradient(135deg,#667eea,#764ba2)`+`color:rgba(255,255,255,0.6);font-weight:300`。
- do: scrim `rgba(15,23,42,0.45)`+`#e5e7eb;400`（≥4.5:1）；白系叠图 scrim ≥0.4 或压暗渐变。来源: [模型经验] 06。

### Top 2：强调反转（红实心「取消」+灰描边「确认」）
- 症状: 用户点了最醒目的「取消」，任务被打断。
- 根因: 把「危险=红色」语义当强调规则；Von Restorff 隔离**推荐项**而非任意语义色项（违反 [VP-4]）。
- don't: `.btn-cancel{background:#ef4444;color:#fff} .btn-confirm{transparent+border #d1d5db}`。
- do: 确认=主操作实心（右）、取消=文本（左）；真删除另配输入名称确认。来源: [模型经验] 06 + [官方文档](https://lawsofux.com/von-restorff-effect/)。

### Top 3：统一间距病（全页 gap-4）
- 症状: 界面「一坨或散沙」，说不出哪块是一组。
- 根因: 间距未承载关系——统一间距=关系信息清零，接近性失效（违反 [VP-1]），修复见「间距系统」。来源: [模型经验] 01。

### 坑点速查表

| 症状 | 根因 | 修复 | 详情/法则 |
|---|---|---|---|
| 落地页全居中，多行段落双毛边 | 居中破坏扫读基线 | 标题 ≤2 行可居中；段落/表单/列表左对齐 | [VP-26]；06 |
| 点不中 24~32px 关闭/点赞按钮 | 视觉尺寸当命中尺寸 | 命中区 ≥44×44，padding 扩展 | [VP-5]；03/06 |
| 触屏上删除按钮「不存在」 | hover-only 可见性 | `@media (hover:hover)` 限定+触屏常显 | [VP-11]；06 |
| 真实文案卡片溢出、40 字符用户名挤出按钮 | 定高容动态文本；flex 子项 `min-width:auto` | `min-height`+`line-clamp`+`min-width:0`+`text-overflow:ellipsis`；禁 `h-` 定高 | [VP-8]；06 |
| 每组一个边框卡片、三层嵌套 | 边框当默认分组手段 | 间距>背景>边框；内层用分隔线 | [VP-19]；01/06 |
| 自动填充后不知字段是什么 | placeholder 当 label | 持久 label，placeholder 只做示例 | [VP-6]；05 |
| 提交后收到 8 条错误汇总 | 校验延迟到流程末尾 | onblur inline 校验，错误贴字段 | [VP-13]；03/05 |
| 弹窗「浮不起来」；暗色面板糊成一片 | scrim 过浅（0.1）；暗色沿用浅色阴影（深底不可见） | scrim ≥0.4 可选 blur(2px)；暗色用表面色阶 #0a0a0a→#171717→#262626 | [VP-9]；01/06 |
| 红绿状态点色盲不可辨；促销红泛滥真 error「狼来了」 | 状态仅用颜色；装饰色占用语义色 | 颜色+图标/文本双编码；红色预算留给错误/危险、促销用品牌色 | [VP-15]；06 |
| 移动端功能埋长列表中部使用率低 | 序列位置效应违背 | 高频项置首/末，关键操作最左最右 | [VP-12]；03 |
| 入场动画 8 元素 stagger 3s+ | 动画最大化+`transition-all` | 仅 transform/opacity，150~300ms，尊重 prefers-reduced-motion | [VP-17]；06 |
| 上线遇空列表/网络失败/加载中即白屏；空态只有插画+「暂无数据」 | 完美数据盲视；空态当死胡同 | 补加载/空/错误三态+容器预设截断；空态=一句话+主行动按钮 | [VP-20]；05/06 |
| 饼图 9 色 9 片不可比 | 仪表盘彩虹 | 分类色 ≤5~6；饼片 ≤5 降序+「其他」；比较用条形图 | 06 |
| 图标混作一组、猜不出功能 | 风格混用；图标-only 强迫回忆 | 一套图标一种风格；图标+文本标签 | [VP-24]；01/05 |
| 标题三档 18/16/15px 层级不可辨 | 对比畏缩未过阈值 | 相邻档字号比 ≥1.2 或字重跨 400→600 | [VP-21]；08 |
| 同会话三种「近似的蓝」/圆角 12 与 14 混用 | 逐组件生成、无 token 表 | 样式值全部 token 化，同语义单值 | [VP-23]；08 |
| 滚动穿透 sticky 顶栏；hero 裸字压图 | 顶栏无背景；图上文字无 overlay | 顶栏半透明+blur；叠图 overlay 保 ≥4.5:1 | [VP-30]/[VP-31]；09 |
| 加载完成「跳版」视线锚点丢失 | 骨架与真实结构不对应 | 块数/位置/高度一一对应（差 ≤8px） | [VP-29]；09 |
| 页顶横幅大图放核心功能、用户视而不见 | 横幅盲视三特征命中（位置/广告式处理/邻近广告） | 融入内容流；样式随站点；顶部/右栏关键内容必做可用性测试 | [VP-37] |
| 长文页右侧内容大面积无人看 | F 型三条件未消除（文字墙无格式化） | F 解药八条：前两段要点/醒目标题/前 2 词/加粗/分组/列表/删减 | [VP-38] |
| 多步流程中途大量弃单 | 无进度指示；无初始动能 | 清晰进度指示；可用人为初始进度 | [VP-40] |

## 参数速查表

| 参数 | 数值/公式 | 出处/性质 |
|---|---|---|
| Fitts's Law | MT=a+b·log₂(2D/W)；贴屏幕边缘「无限深」 | [官方文档](https://lawsofux.com/fittss-law/)（1954）；公式 [模型经验] 03 |
| Hick's Law | RT=a+b·log₂(n+1)；5→9 约 +34%（非「翻倍」） | [官方文档](https://lawsofux.com/hicks-law/)（Hick-Hyman 1952）；公式/34% [模型经验] 03 自算 |
| Doherty | <400ms 保心流；100ms 即时；1s+ loading；10s+ 进度+可离开 | [官方文档](https://lawsofux.com/doherty-threshold/)（1982 IBM Systems Journal，Doherty & Thadani 将标准从 2000ms 提高到 400ms；进度条提升容忍；刻意延迟可提升感知价值）；分档 [模型经验] 03 |
| 触控目标 | 移动 ≥44×44（Apple 44pt/Material 48dp）；WCAG 2.2 AA 24×24（2.5.8） | [模型经验] 03（未验证） |
| 间距刻度 | 4/8（组内）→16/24（同级）→48/64/96（区块）；组间 ≥2× 组内 | [模型经验] 01 |
| 字阶比例 | 1.125/1.25/1.333/1.5；级差过阈值（字号比 ≥1.2 或字重 400→600） | [模型经验] 02 |
| 文本对比度 | 正文 ≥4.5:1；大字/UI ≥3:1；gray-600 白底 ≈7.6:1 | [模型经验] 02（WCAG 共识） |
| 行长/行高 | 45~75ch（66 经典）；正文行高 1.4~1.6；justify 禁用 | [模型经验] 02 |
| scrim 不透明度 | 0.4~0.6 | [模型经验] 01 |
| 暗色表面色阶 | 底 #0a0a0a→卡 #171717→浮层 #262626；正文 ≥gray-200；纯黑有光晕 | [模型经验] 01/06 |
| 第一印象 | 约 50ms 形成吸引力判断（Lindgaard 2006） | [模型经验] 04 |
| 工作记忆 | 4~7 组块/时刻；每组块 20~30s 消退 | [官方文档](https://lawsofux.com/working-memory/) |
| 扫描模式 | NN/g 官方清单：F/层叠蛋糕/斑点/标记/绕过/投入；RTL 镜像 F | [官方文档](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)（Pernice 2017） |
| 组块格式 | 手机号 138 0013 8000；OTP 3+3；卡号 4-4-4-4 | [模型经验] 05 |
| 动画时长 | 微交互 150~300ms；入场 200~400ms；仅 transform/opacity | [模型经验] 06 |
| 色觉障碍 | 红绿色盲男性约 8%（常见引用） | [模型经验] 07 |
| 菜单广度 | 中等广度 4~8 项/层优于极深（Snowberry 1981，最优值不确定） | [模型经验] 03 |
| 表单宽度 | max-width ≈560px（保 label-input 邻近） | [模型经验] 05 |

### Laws of UX 30 法则速查（R34 全量锚定）

来源: [官方文档](https://lawsofux.com/)（30 法则逐页抓取，语料 docs/laws/）。用法：设计决策找「为什么」时按法则名查此表，再读对应语料全文。

| 法则 | 一句话陈述 | 起源 | 设计要点 |
|---|---|---|---|
| Aesthetic-Usability | 美的被感知为更好用 | Kurosu & Kashimura 1995（26 ATM 变体×252 人，日立） | 宽容小问题；掩盖可用性问题（测试警惕） |
| Choice Overload | 选项过多压垮决策（选择的悖论） | Toffler 1970《Future Shock》 | 必须比较时并排对比（定价档）；精选+搜索筛选先行 |
| Chunking | 信息拆片再组成有意义整体 | Miller 1956 | 视觉分明的组+清晰层级 |
| Cognitive Bias | 系统性思维错误影响感知与决策 | Tversky & Kahneman 1972 | 设计与研究解读警惕确认偏误 |
| Cognitive Load | 理解使用界面所需心理资源总量 | Sweller 1988 | 剔除外在负荷（无助于理解的加工） |
| Doherty Threshold | <400ms 交互生产率飙升 | Doherty & Thadani 1982（IBM Systems Journal，2000ms→400ms） | 感知性能；进度条提升容忍；刻意延迟可增感知价值 |
| Fitts's Law | 命中时间随距离增加/目标减小而增加 | Fitts 1954 | 大目标+近距离+贴边等效无限深 |
| Flow | 全神贯注沉浸投入的心理状态 | Csíkszentmihályi 1975 | 难度匹配技能；必要反馈；移除摩擦 |
| Goal-Gradient | 越接近目标动力越强 | Hull 1932/1934（老鼠跑道实验） | 清晰进度指示；人为初始进度提升动机 |
| Hick's Law | 决策时间随选项数与复杂度增加（对数） | Hick & Hyman 1952 | 减选项；拆步骤；高亮推荐；渐进引导；勿过度简化 |
| Jakob's Law | 用户偏好你的站点与已知站点一致 | Jakob Nielsen（NN/g） | 利用既有心理模型；重大变更给熟悉版本过渡期 |
| Law of Common Region | 共享明确边界的元素为一组 | 格式塔 | 加边框或背景=标准手法 |
| Law of Proximity | 靠近的对象被感知为一组 | 格式塔 | 间距承载关系（Google 搜索结果簇） |
| Law of Prägnanz | 复杂图像被知觉为最简形式 | Wertheimer 1910（铁路道口灯光） | 简单形状加工与记忆优于复杂 |
| Law of Similarity | 相似元素被知觉为一组/完整画面 | 格式塔 | 颜色/形状/尺寸/方向/运动标组；链接与正文区分 |
| Law of Uniform Connectedness | 视觉相连的元素更相关 | 格式塔 | 线/箭头/边框建立连接（Google 精选摘要边框） |
| Mental Model | 自认为所知的系统压缩模型 | Craik 1943 | 设计对齐用户模型；缩小设计者-用户模型差距 |
| Miller's Law | 工作记忆 7±2 条目 | Miller 1956 | 组块化；勿拿「神奇数字 7」为设计限制辩护 |
| Occam's Razor | 预测相当时选假设最少者 | William of Ockham（约 1287–1347） | 一开始就避免复杂；移除一切可移除后才算完成 |
| Paradox of Active User | 用户从不读手册直接上手 | Rosson & Carroll 1987 | 情境化引导全程可用（带帮助信息的 tooltip） |
| Pareto Principle | 约 80% 效果来自 20% 原因 | Vilfredo Pareto（意大利土地观察） | 精力集中于为最多用户带来最大收益的少数领域 |
| Parkinson's Law | 任务膨胀直到耗尽可用时间 | Parkinson 1955《The Economist》 | 任务限时于预期内；autofill 省时 |
| Peak-End Rule | 评价取决于峰值与结尾时刻 | Kahneman et al. 1993（冷水实验） | 精心设计峰与终；负面记忆更鲜明 |
| Postel's Law | 对接受宽容，对发送保守 | Jon Postel（TCP 鲁棒性原则） | 输入宽容转标准格式+边界+反馈；输出严格合规 |
| Selective Attention | 只注意与目标相关的刺激子集 | Cherry 1953 鸡尾酒会效应起 | 引导注意；防横幅盲视/变化盲视 |
| Serial Position Effect | 序列首尾条目最好记 | Ebbinghaus | 关键操作放最左最右；最不重要项放中部 |
| Tesler's Law | 任何系统存在无法消减的核心复杂性 | Larry Tesler（Xerox PARC） | 设计开发阶段消化复杂性，勿转嫁用户 |
| Von Restorff Effect | 多个相似对象中不同者被记住 | Hedwig von Restorff 1933 | 强调保持克制；防误认广告；勿仅靠颜色/动效 |
| Working Memory | 临时保持并操纵任务信息的认知系统 | Miller/Galanter/Pribram 1960s | 4~7 组块×20~30s；识别优先回忆；系统携带跨屏信息 |
| Zeigarnik Effect | 未完成/被打断的任务记得更牢 | Bluma Zeigarnik 1920s | 清晰示能引导发现；进度激励完成 |

## 版本注意

- **Fitts's Law**: 1954（[官方文档](https://lawsofux.com/fittss-law/)）；公式 [模型经验] 补充。**Miller's Law**: 官方 7±2；Cowan 4±1 现代估计——引用区分，不混用；官方明确警告勿用「7」为不必要的设计限制辩护。
- **Doherty**: 1982 年 Doherty & Thadani（IBM Systems Journal）证实——将计算机响应时间标准从 2000ms 提高到 400ms；「刻意延迟提升感知价值」为官方要点（R34 锚定）。**WCAG 2.2**: 2.5.8（AA 24×24）与 2.5.5（AAA 44×44）关系及豁免见 usability-accessibility kb（已锚定）。
- **平台触控**: Apple 44pt / Material 48dp 版本敏感。**第一印象**: 50ms（Lindgaard 2006）单一锚点仍未验证；「17ms」归属不确定。
- **CLT**: 官方页仅内在/外在两类；germane load 为 [模型经验]（2010s 后有弱化主张，引用保守）。**Tailwind**: v3/v4 类名差异（`shadow-sm`→`shadow-xs` 一系）；生成前确认版本。
- **扫描模式（R34 更新）**: F 型已全量锚定（Pernice 2017 复审版，桌面+移动均成立）；NN/g 官方扫视模式清单不含 Z 型——Z 型降级为「无官方支持」，不得作为设计依据推荐。
- **CSS 特性**: `line-clamp` 前缀、`backdrop-filter`、flex `min-width:auto` 均版本敏感。

## 与其他子领域的集成要点

- **→ layout-composition**: [VP-1] 间距刻度与 2× 规则；格式塔分组线索供网格/信息密度；扫描模式供视觉流编排。
- **→ color-system**: [VP-7] 三档色阶与 4.5:1 阈值；[VP-15] 无障碍配色；装饰色不占语义色。
- **→ typography**: [VP-16] 字阶/字重阈值；行长 45~75ch、行高 1.4~1.6、justify 禁用；tabular-nums；[VP-10] 标题写作。
- **→ interaction-motion**: [VP-13] 峰终/inline 校验；Doherty 分档供加载（1982 IBM 证实）；[VP-17]/[VP-34] 动效原则；[VP-32] FLIP/共同运动；[VP-40] 进度指示。
- **→ style-design-system**: [VP-3] 三档体系映射 variant；[VP-9] 表面色阶供 elevation/token；倒 U 约束堆料。
- **→ usability-accessibility**: [VP-5]/[VP-11]/[VP-15]/[VP-17] 为 WCAG 视觉侧输入；识别优先于回忆（[VP-39]）；峰终供错误预防。
- **→ 供规则方式**: 本文件输出「为什么」与硬阈值；下游做「怎么做」，引用用编号（如命中区下限见 [VP-5]）。

## 来源索引

- 文档锚点（阶段 2 + R34 阶段 A 全量抓取，2026-11-16）：
  - https://lawsofux.com/ 30 法则逐页 → docs/laws/（29 文件：aesthetic-usability/choice-overload/chunking/cognitive-bias/cognitive-load/doherty-threshold/flow/goal-gradient/hicks-law/jakobs-law/law-of-common-region/law-of-proximity/law-of-pragnanz/law-of-similarity/law-of-uniform-connectedness/mental-model/millers-law/occams-razor/paradox-of-the-active-user/pareto-principle/parkinsons-law/peak-end-rule/postels-law/selective-attention/serial-position-effect/teslers-law/von-restorff-effect/working-memory/zeigarnik-effect）+ docs/fittss-law.md + docs/lawsofux-index.md
  - https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/ → docs/nn-f-shaped-pattern.md（Pernice 2017 复审：F 三段构成/六种扫视模式/三条件/解药八条/RTL 镜像）
  - https://www.nngroup.com/articles/banner-blindness-old-and-new-findings/ → docs/nn-banner-blindness.md（Pernice 2018：三特征/烫手山芋/0.8% vs 25%/SERP 例外）
  - 批次日志: docs/_fetch_log_r34-vp.md
- 模型萃取（阶段 1，已融合）: 01-gestalt、02-visual-hierarchy、03-ux-laws、04-aesthetic-usability、05-cognitive-load、06-ai-mistakes、07-laws（VP-1~20）、08-crap-principles（VP-21~28）、09-gestalt-full（VP-29~36）。
- 降级声明: 未降级——lawsofux 30 法则+NN/g 2 篇全量锚定；未覆盖数值（2× 间距/50ms/scrrim 区间等）逐条标 [模型经验]，未编造 URL。
- 标注约定: [官方文档](url) 仅限白名单 URL；[模型经验] 附 corpus 路径；无 [推断] 入正式区块。

## 冲突消解记录

1. **Miller's Law**: 文档 7±2 为准；Cowan 4±1 降「现代估计」注记；教训统一为「组块化非 ≤7 教条」；官方页另警告勿拿「神奇数字 7」为不必要的设计限制辩护（同向强化）。
2. **Hick「5→9 翻倍」**: 讹传弃用；log₂ 下约 +34%，速查表按对数表述并标注自算。
3. **Common Region**: llms.txt 明确收录，由「待验证」升级确认；「间距>背景>边框」优先级仍是模型成本约束，互补使用；R34 全页锚定（边框/背景=官方标准手法）。
4. **Fitts 边界**: 定义与 takeaways 按文档；贴边无限深/拇指区保留为 [模型经验]（方向高置信、形状低置信）。
5. **F 型「NN/g 正文未抓取」**: 已全量锚定（Pernice 2017 复审版）——三段构成、六种其他扫视模式（层叠蛋糕/斑点/标记/绕过/投入）、三条件、RTL 镜像、解药八条全部升格 [官方文档]；「设计成 F」仍是错误外推——F 是无引导时的默认最小努力路径，解药是消除三条件。
6. **Z 型「实证弱」**: NN/g 官方扫视模式清单不含 Z 型 → 降级为「无官方支持」，概念表与扫描模式场景移除 Z 型推荐（v1 曾作低文字页锚点建议，v2 撤销）。
7. **认知负荷「三类型」**: 官方页仅内在/外在两类；germane 维持 [模型经验] 并保留弱化主张注记。
8. **Doherty「IBM 1982 链条未验证」**: 证实——1982 年 Walter J. Doherty 与 Ahrvind J. Thadani 发表于 IBM Systems Journal，将响应标准从 2000ms 提高到 400ms；新增官方要点「刻意增加延迟可提升感知价值与信任」。
9. **美学-可用性起源**: 证实——Kurosu & Kashimura 1995（日立设计中心，26 ATM 界面变体×252 名参与者）：美观度与「感知易用性」的相关性强于与「实际易用性」的相关性；50ms 第一印象（Lindgaard 2006）仍未验证，维持 [模型经验]。
