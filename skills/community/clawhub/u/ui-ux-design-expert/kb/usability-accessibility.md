---
domain: ui-ux-design
skill_name: ui-ux-design-expert
subdomain: usability-accessibility
title: 可用性与无障碍（WCAG 2.2 + Nielsen 启发式 + WAI-ARIA APG）
version: 6
source_index:
  elicited: corpus/ui-ux-design/usability-accessibility/elicited/01~10（10 文件）
  docs: corpus/ui-ux-design/usability-accessibility/docs/（wcag-2-overview / wcag-new-in-22 / webaim-wcag-checklist / nielsen-10-heuristics / aria-apg-patterns-index / aria-apg-dialog-modal / wcag22-spec-extracts（86 条 SC 逐字）/ wcag22-quickref-extracts（技法编号全名+失败模式）/ apg/ 30 模式全量+_index+_fetch_log_r34-*）
knowledge_ratio: 法则 18% / 最佳实践 44% / 坑点 38%
merged_at: 2026-11-16
updated_at: 2026-11-17
---

# 可用性与无障碍（usability-accessibility）

## 定位与心智模型

本域回答：**为什么"好看"必须同时"好用"才算成立**——违反 Nielsen 启发式与 WCAG 2.2 的界面再精致也是失效设计。

- **WCAG 2.2**（W3C Rec，2023-10-05）：可量化合规底线，POUR 四原则 × 13 guideline，A/AA/AAA 三级，AA 是交付基线 [官方文档](https://www.w3.org/WAI/standards-guidelines/wcag/)。
- **Nielsen 十大可用性启发式**（1994，249 个可用性问题因子分析提炼，30 年未改）：可走查的设计原则，覆盖合规之外维度 [官方文档](https://www.nngroup.com/articles/ten-usability-heuristics/)。
- **WAI-ARIA APG**（W3C/WAI Authoring Practices Guide）：30 个 widget/结构模式的键盘交互与 ARIA 角色/状态/属性实现规范——自定义控件的权威契约，v3 全量锚定 [官方文档](https://www.w3.org/WAI/ARIA/apg/patterns/)。

适用边界：规范 Web 与类 Web 界面（含 Hybrid）；纯原生移动控件循 HIG/Material，WCAG 阈值可作基准。启发式是**走查工具而非检查表**，不能替代可用性测试 [官方文档](https://www.nngroup.com/articles/)。

## 法则

> 编号 UA-1~UA-28。溯源缩写：WebAIM=[官方文档](https://webaim.org/standards/wcag/checklist)；n22=[官方文档](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)；NN/g=[官方文档](https://www.nngroup.com/articles/ten-usability-heuristics/)；APG=docs/apg/ 30 模式语料（[官方文档](https://www.w3.org/WAI/ARIA/apg/patterns/)）；01~07=elicited 文件（见来源索引）。

**[UA-1]** NEVER: 禁用原生焦点环（`outline: none`）而不提供可见替代（`:focus-visible`，指示器对比 ≥3:1）。违反 2.4.7，对比不足同时违反 1.4.11。源: WebAIM、06
**[UA-2]** MUST: 优先用原生语义元素（`button`/`a`/`select`/`input`）承载交互；必须自定义时补 `role`+`tabindex="0"`+键盘事件（Enter/Space/方向键）。aria 修补不了错误的元素选择。违反 2.1.1。源: WebAIM、06；APG Button/Link 证实（role 不带来行为，行为由作者负责）
**[UA-3]** NEVER: 用颜色作状态/信息唯一载体——每个语义必须有第二通道（形状/文字/符号）；链接仅凭颜色区分时对比 ≥3:1。违反 1.4.1。源: WebAIM、03（色盲 8% 男性为模型经验）
**[UA-4]** MUST: 正文对比度 ≥4.5:1；大文本（≥18pt ≈ 24px，或 ≥14pt ≈ 18.66px 加粗）≥3:1；UI 组件边界/图标/图形 ≥3:1（1.4.11）。灰底陷阱见坑点表第 2 行。违反 1.4.3/1.4.11。源: [官方文档](https://webaim.org/standards/wcag/checklist)、02
**[UA-5]** MUST: 指针目标命中区 ≥24×24 CSS px（2.5.8 AA 底线）；AAA 44×44（2.5.5）；移动端实践 ≥44×44（Apple）/48dp（Material）。AA 与 AAA 不可混称。源: n22、WebAIM
**[UA-6]** MUST: 异步操作期间触发控件进入 pending/disabled 态并给可见反馈；用户可触发操作须有成功/进行中/失败三态，禁只实现 happy path。违反 Nielsen H1。源: NN/g、06
**[UA-7]** MUST: 表单字段有可见 `label`（for/id 关联），placeholder 不得作唯一标签；关键输入加 `autocomplete`。违反 3.3.2。源: WebAIM、06；3.3.2 已由规范全文锚定（docs/wcag22-spec-extracts.md）
**[UA-8]** MUST: 错误信息含三要素——发生了什么、为什么、怎么办（恢复动作/替代路径），平实语言无错误代码；禁只报「出错了，请重试」。违反 Nielsen H9。源: NN/g、04
**[UA-9]** NEVER: 破坏性操作不给出口——中风险给撤销（undo），高风险给后果写明文案的显式确认；误操作须有"紧急出口"。违反 Nielsen H3。源: NN/g、04
**[UA-10]** MUST: 校验错误定位到具体字段（视觉标记+`aria-describedby`+聚焦/滚动到第一个错误）并给修复建议；禁止只有笼统 toast。违反 3.3.1/3.3.3。源: WebAIM、04
**[UA-11]** MUST: 模态焦点四件套——打开焦点移入、焦点陷阱（Tab 首尾环绕）、ESC 可关、关闭返还触发元素，带 `role="dialog"` `aria-modal="true"`（`aria-labelledby` 指向可见标题），tab 序列含可见关闭钮。违反 2.1.2。源: WebAIM、06；APG Dialog (Modal) 证实（锚点见场景 7）
**[UA-12]** MUST: 动态内容更新（数量/错误/状态变化）通过 `aria-live="polite"` 或等效读屏可达方式通知。源: 06；APG Alert 证实（动态渲染的 role="alert" 被读屏自动播报；页面加载前已存在的 alert 不播报）
**[UA-13]** MUST: 非必要位移动画提供 `prefers-reduced-motion: reduce` 降级；>5s 自动移动/滚动须可暂停/停止/隐藏（2.2.2）；交互动画不可禁用违反 2.3.3（AAA）。源: WebAIM、03
**[UA-14]** NEVER: 使用正 `tabindex`（>0）硬编码焦点顺序；焦点顺序必须与 DOM/感知顺序一致（CSS order/flex/grid 视觉重排不改 DOM 顺序）。违反 2.4.3。源: 02
**[UA-15]** MUST: icon-only 按钮提供 accessible name（`aria-label` 或视觉隐藏文本）；name 须含全部可见标签文本。违反 2.5.3/4.1.2。源: 02
**[UA-16]** MUST: 提交失败保留已输入内容，禁清空或跳转丢数据；长文本编辑提供草稿自动保存。源: 04
**[UA-17]** NEVER: 拖拽作为唯一操作——拖拽排序/滑块须提供免拖拽的单指针/键盘等效。违反 2.5.7（essential 除外）。源: n22
**[UA-18]** NEVER: 确认对话框用模糊文案（「确定吗？」+「是/否」）——后果写入正文，按钮用具体动词，危险按钮不设默认焦点（confirm() 默认焦点在 OK，Enter 连击可穿透）。源: 04
**[UA-19]** MUST: 启发式评估问题记录含五字段——位置（截图+复现路径）、行为 vs 预期、违反启发式编号、严重度（0~4，三因子：频率×影响×持久性）、备注。源: 05（细则未经文档验证）
**[UA-20]** MUST: 登录/认证不得仅依赖认知功能测试（记忆密码、解谜验证码）——必须提供替代（密码管理器支持、OAuth、passkey、生物识别、非认知 CAPTCHA 替代）。违反 2.2 新增 3.3.8 Accessible Authentication (Minimum)。源: n22（例外：替代方式/辅助机制/物体识别/个人内容识别）
**[UA-21]** MUST: 复合控件（toolbar/tabs/menubar/listbox/grid/tree/radio group）在页面 Tab 序列中只占**一个**停靠点；内部焦点用 roving tabindex（当前项 `tabindex="0"` 其余 `"-1"`）或 `aria-activedescendant`（容器持焦+ID 指向当前项）二选一；Tab 进出组件、方向键在组件内移动。禁止每个子项都做 Tab 停靠点。源: APG Toolbar/Tabs/Menubar/Grid/Radio/Listbox/Tree
**[UA-22]** NEVER: toggle button 与 switch 的标签随状态切换而改变——用 `aria-pressed`/`aria-checked` 时标签保持恒定（静音按钮 pressed 后仍叫 "Mute"，读屏播报 "Mute, toggle button, pressed"）；设计确需标签变化（Mute↔Unmute）则不用 aria-pressed。源: APG Button/Switch
**[UA-23]** MUST: 每页 landmark 区域 ≤7 个（数量越多价值越低）；全部内容都应包含在合适的 landmark 区域内。源: APG Landmarks
**[UA-24]** MUST: combobox 的 Esc 必须**无损**关闭 popup（可浏览选项不丢已选值——这是 combobox 优于单选 listbox 的关键可用性事实）；「选择跟随焦点」（selection follows focus）用于单选 listbox 前须按场景评估——部分场景严重损害可用性。源: APG Combobox/Listbox
**[UA-25]** MUST: `role="alert"` 不影响键盘焦点、不自动消失、控制出现频率（频繁打断损害视障与认知障碍用户）；alertdialog（模态打断）的 `aria-describedby` **必设**指向 alert 消息——与 dialog 模式的可选 describedby 不同。源: APG Alert/Alert Dialog
**[UA-26]** MUST: 自动轮播必须配停止/重启按钮；轮播内任一元素获得键盘焦点即停止自动轮播，且除非用户显式激活轮播控件不得自动恢复；轮播控制按钮须为轮播内 Tab 序列**第一**元素。源: APG Carousel
**[UA-27]** MUST: listbox 超过 5 个选项强烈建议支持 Home/End；listbox 与 tree 推荐 type-ahead（尤其超过 7 项）；选项名重复前缀（如「国家+城市」）显著劣化键盘与读屏可用性，应拆成两个控件。源: APG Listbox/Tree View
**[UA-28]** MUST: meter 仅用于有意义上限的量值（电量/油量），禁止用于进度（加载/任务完成用 progressbar）；`aria-valuenow` 对用户不友好时（数字代表星期等）必须设 `aria-valuetext` 为可理解字符串。源: APG Meter/Slider/Spinbutton

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| WCAG 2.2 | W3C 无障碍标准，13 guideline × POUR（可感知/可操作/可理解/健壮），A/AA/AAA，2023-10-05 定版 [官方文档](https://www.w3.org/WAI/standards-guidelines/wcag/) |
| Success Criterion (SC) | 可判定的合格条款，带编号与级别（如 2.5.8 AA） |
| Nielsen 十启发式 | 1994 年从 249 个可用性问题因子分析提炼的 10 条设计原则，走查工具而非检查表 [官方文档](https://www.nngroup.com/articles/ten-usability-heuristics/) |
| APG 模式 | WAI-ARIA Authoring Practices Guide 的 30 个 widget/结构模式：键盘交互+role/状态/属性契约，自定义控件实现基准 [官方文档](https://www.w3.org/WAI/ARIA/apg/patterns/) |
| roving tabindex | 复合控件焦点管理法：当前项 tabindex="0"、其余 "-1"，方向键移动时交换（[UA-21]） |
| aria-activedescendant | 复合控件焦点管理法：容器持 DOM 焦点，属性 ID 指向逻辑当前项，AT 焦点随 ID 移动（[UA-21]） |
| 风险分级防御 | 低风险直接执行 / 中风险执行+撤销 / 高风险显式确认 / 极高风险输入名称确认 [模型经验] 04-error-prevention |

## 最佳实践

### 场景 1：实现键盘可达的交互控件

能用原生元素（`button`/`a`/`select`/`input`）承载则必须用；视觉不像原生时改 CSS 不换元素（"文字按钮"仍是 `button`）；必须自定义时补 `role`+`tabindex="0"`+Enter/Space+方向键+ESC，参照 WAI-ARIA Authoring Practices（源于 [UA-2]）。
- don't: `<div onclick="save()">保存</div>`（键盘死、读屏不识别）；do: `<button onclick="save()">保存</button>`

边界：跳转用 `a[href]`（有 href 才进 Tab 序列），触发行为用 `button`；全键盘场景审查 `:focus` vs `:focus-visible` [模型经验] 03-a11y-visual。按钮激活后焦点去向取决于动作类型（开对话框→焦点入框；关对话框→返还触发钮；Apply 类→留钮上；上下文变更→移到动作起点）[官方文档](https://www.w3.org/WAI/ARIA/apg/patterns/button/)。

### 场景 2：设计可见且合规的焦点样式

不全局移除 outline；自定义用 `:focus-visible`，指示器对比 ≥3:1（1.4.11）[官方文档](https://webaim.org/standards/wcag/checklist)；sticky 层加 `scroll-padding` 防聚焦被遮挡（2.4.11）[官方文档](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)；焦点环勿被 `overflow: hidden` 裁切；错误/正确代码见坑点表第 1 行。

边界：`box-shadow` 焦点环同受 3:1 约束；AAA 2.4.13 面积公式与切换对比数值见速查表 [官方文档](https://webaim.org/standards/wcag/checklist)。

### 场景 3：配色与对比度落地

正文 ≥4.5:1、大文本（≥24px 或 ≥18.67px bold）≥3:1、UI 边界/图标/图表图形 ≥3:1——描边按钮校验边框而非只校验文字 [官方文档](https://webaim.org/standards/wcag/checklist)；#767676 为白底最低合格灰（#999 陷阱见坑点表第 2 行）；渐变按最差区域校验；深色模式用独立 token 逐对重算，禁止 `filter: invert(1)`；状态语义双重编码：颜色+符号/形状/文字（源于 [UA-3]/[UA-4]）。
- do: `[data-theme="dark"]{--text:#e8e8e8;--muted:#a0a0a0}` 独立 token，层级用亮度差+边框；`.success::before{content:"✓ "}` `.error::before{content:"✕ "}` 双通道

边界：disabled 承载关键信息时仍应可读并提示禁用原因 [模型经验] 03-a11y-visual。

### 场景 4：无障碍表单

每字段可见 `label for`+`autocomplete`（1.3.5 落地）；placeholder 仅作格式示例；校验时机分层：input 中只在「曾正确后变错」时报（touched 后实时），blur 首次校验，submit 全量+聚焦/滚动到第一个错误；错误信息=三要素+示例值（例「YYYY-MM-DD，如 1990-08-16」）+`aria-describedby`；提交失败保留全部已输入内容，长文本加草稿自动保存（源于 [UA-7]/[UA-8]/[UA-10]/[UA-16]）。
- don't: `<input placeholder="请输入邮箱">`（placeholder 当 label）；一 input 就校验（首字符即报错）
- do: `<label for="email">邮箱</label><input id="email" type="email" autocomplete="email">`；`touched=false; blur→touched=true+validate; input→if(touched)validate`

边界：前后端校验规则必须一致；「重试」须幂等（幂等键），否则重试重放整单 [模型经验] 04-error-prevention。

### 场景 5：错误信息与确认流程设计

错误文案按三要素模板（+可选引用码）；网络错误分类：4xx 给具体建议 / 5xx 道歉+引用码 / 网络层检查连接——禁止 500 也提示「检查网络连接」；风险分级防御见概念表；确认对话框设计见 [UA-18]（[UA-8]/[UA-9]）。
- don't: `if (confirm('确定吗？')) deleteItem(id)`
- do: `deleteItem(id); showToast('已删除',{action:'撤销',onAction:restoreItem})`（中风险 undo 3~10s）；高风险: `删除「季度报告.xlsx」？此操作可在 7 天内从回收站恢复。[取消][删除]`

边界：undo 窗口无标准值（Gmail ~5s+，惯例 3~10s）；法律/财务/数据提交另有 3.3.4 硬要求：可回退/可验证/可确认 [官方文档](https://webaim.org/standards/wcag/checklist)。禁用 alert/confirm/prompt 作产品 UI [模型经验] 06-ai-mistakes；确认型打断的规范载体是 alertdialog（[UA-25]）。

### 场景 6：触控目标与移动端命中区

相邻目标留间距避免重叠误触；视觉小、命中大：`min-width/height`+flex 居中或伪元素扩展命中区（尺寸标准见 [UA-5]）。
- don't: 16px 图标即 16px 命中区
- do: `.icon-btn{min-width:24px;min-height:24px;display:inline-flex;align-items/justify-content:center}`（移动端建议 44px）；`.hit-area::after{content:"";position:absolute;inset:-12px}`

边界：2.5.8 例外——间距补偿（24px 直径圆不与其他目标圆相交）、等效控件、行内目标、UA、essential [官方文档](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)。行内文本链接可豁免，密集列表仍建议加大行高。

### 场景 7：模态框与动态内容的通知

模态焦点四件套+dialog role（[UA-11]）；动态更新（购物车数量、错误）挂 `aria-live="polite"`，紧急才用 assertive（[UA-12]）；帮助入口跨页面相对位置一致（3.2.6 Consistent Help，A）；同流程不强制重复输入已提供信息（3.3.7 Redundant Entry，A）[官方文档](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)。
- don't: `<span className="cart-count">{count}</span>`（读屏零感知）
- do: `<span aria-live="polite" className="cart-count">{count}</span>`

APG 细则 [官方文档](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)：初始焦点默认第一可聚焦元素，不可逆末步（删除/支付）聚焦最不破坏性动作；结构化内容先聚焦 `tabindex="-1"` 静态起始元素并省 `aria-describedby`；`aria-modal` 取代 `aria-hidden` 标记框外 inert。

边界：`aria-live` 区域须在内容变化前就存在于 DOM；频繁变更（如倒计时）勿用 live 区域轰炸读屏 [模型经验] 06-ai-mistakes。非模态通知（role="alert"）不夺焦点，需打断工作流才升级 alertdialog（aria-describedby 必设，[UA-25]）。

### 场景 8：动效的无障碍降级

全局提供 `prefers-reduced-motion: reduce` 分支：位移动画归零，保留状态表达；超 5s 自动移动/滚动（轮播、marquee）提供暂停/停止/隐藏控件（2.2.2）；闪烁 ≤3 次/s（2.3.1）[官方文档](https://webaim.org/standards/wcag/checklist)；JS 用 `matchMedia('(prefers-reduced-motion: reduce)')` 切换 `scrollIntoView` smooth→auto（源于 [UA-13]）。
- don't: 无差别位移动画/视差（前庭用户眩晕）
- do: `@media (prefers-reduced-motion: reduce){*,*::before,*::after{animation-duration/transition-duration:0.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important}}`

APG Carousel 细则 [官方文档](https://www.w3.org/WAI/ARIA/apg/patterns/carousel/)：键盘焦点进入轮播即停止自动轮播且不自动恢复；停止/重启按钮必配且为轮播内 Tab 首元素；鼠标悬停停止（[UA-26]）。

边界：opacity 淡入淡出通常非前庭触发可保留；「降级」≠删除所有反馈；删 transition 可能破坏依赖动画结束事件的逻辑——用 0.01ms 而非移除 [模型经验] 03-a11y-visual。

### 场景 9：执行一次启发式评估

确定范围与代表性任务；选 3~5 名背景异质评估者（至少一名非本项目开发）全程独立。双遍走查：第一遍按核心任务流走（整体感受、大问题），第二遍逐界面 × 逐启发式细查。每个问题按五字段记录（源于 [UA-19]）。严重度三因子快速映射：无法完成+全员→4、无法完成+少数或耗时+多数→3、耗时+少数或轻微+多数→2、轻微+少数→1。按严重度排序输出问题清单（问题与方案分开），修复后复审。补认知走查模拟新用户四问——会尝试正确效果吗 / 会注意到控件吗 / 会认为能达成目标吗 / 反馈后知道对了吗。

边界：启发式评估不能替代可用性测试；评估者不独立、先讨论会趋同；「这个蓝不好看」是审美偏好不是可用性问题；每迭代小走查优于上线前一次性大走查 [模型经验] 05-heuristic-evaluation。

### 场景 10：读屏语义与 ARIA 纪律

ARIA 第一法则：原生元素能解决不用 ARIA——`div[role=button]` 须手工补齐 role/name/焦点/键盘四项，漏一项比纯 div 更糟；可见文本必须包含于 accessible name 且开头一致（2.5.3）；landmark 靠 HTML5 隐式映射，每页 ≤7 个、全部内容入 landmark（[UA-23]），重复 nav 用 aria-label 区分（面包屑 nav 即典型），每页恰一个 main，heading 是浏览模式第一导航轴禁跳级；`aria-live` 区域须先于内容变化存在于 DOM，默认 polite（`role="status"`），紧急才 assertive（`role="alert"`），倒计时禁 live 轰炸；装饰图标 `aria-hidden="true"`；SPA 路由切换后主动聚焦新视图 h1（`tabindex="-1"`+focus()）；tabs/menu 等复杂控件对照 WAI-ARIA APG，menu 键盘模型易做错（Tab 不在菜单项间移动而是关闭全部菜单、Esc 逐级关+焦点返还）——网站导航用普通 nav+button 更稳，menu 留给应用型命令菜单；复合控件单停靠点见场景 12，全模式键盘契约见「APG 模式速查表」（源于 [UA-2]/[UA-12]/[UA-15]）。

边界：读屏双模式（浏览/焦点）解释「鼠标测过」≠「读屏可用」；APG 30 模式已全量锚定 [官方文档](https://www.w3.org/WAI/ARIA/apg/patterns/)（语料 docs/apg/，dialog 全文见场景 7），其余读屏细则 [模型经验] 09-screen-reader-aria。

### 场景 11：i18n 与 RTL

RTL 一律逻辑属性（`margin-inline`/`inset-inline`/`text-align:start`），禁物理 left/right；镜像布局与方向性图标（返回箭头 `scaleX(-1)`），不镜像媒体控件/logo；文本膨胀防御：德语 +35%、法语 +20%、中→英收缩 30~50%——按钮/标签不固定宽度（min-width 自适应），导航预留膨胀，德语+日语双语言或 pseudo-localization 验收；`html lang` 是 3.1.1 (A) 硬要求，外语片段 lang 标注（3.1.2 AA）；日期/数字/货币/复数一律 `Intl.*`（多复数形语言「{n} items」模板不成立），禁字符串拼接；截断按语言定制：英文按词（overflow-wrap:break-word）、CJK 按字、德语长词 hyphens:auto+lang。

边界：表单勿硬拆 first/last name（单名字文化存在）；CJK 字重感知偏轻（同字号常需 500~600 对齐西文 400，呼应 typography 域）[模型经验] 10-i18n-rtl。

### 场景 12：实现复合控件（composite widget）

问题：自定义 tabs/dropdown/工具栏时把每个子项都做成 Tab 停靠点——Tab 序列爆炸，方向键缺位。APG 全部复合 widget 共同契约：组件整体只占页面 Tab 序列**一个**停靠点（例外：multi-thumb slider 每 thumb 一个且顺序恒定；carousel 控件随结构），Tab 进出组件、方向键内部移动（源于 [UA-21]）。
- do（roving tabindex）：当前项 `tabindex="0"`、其余 `tabindex="-1"`，方向键移动时交换值并 focus 新当前项；Tab 从当前项直接跳出组件
- do（aria-activedescendant）：容器 `tabindex="0"` 持 DOM 焦点，方向键更新 `aria-activedescendant` 为当前项 ID（menu/listbox/tree/grid 支持）；DOM 焦点不动，AT 焦点随 ID 移动
- 进入落点：有选中项落选中项（tabs 落活动 tab、radio 落选中项、多选落第一个选中项），无选中落第一项

边界：grid 单元格含 widget 时 Enter/F2 进入格内导航、Esc 恢复网格导航，方向键导航期间不可操作格内 combobox 或移动编辑光标 [官方文档](https://www.w3.org/WAI/ARIA/apg/patterns/grid/)；数据 grid 禁环绕（AT 用户迷失），布局 grid 环绕有用；tooltip 不接收焦点，含可聚焦元素的悬停层升级为非模态 dialog [官方文档](https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/)；文本编辑类（combobox 输入框/spinbutton）勿让 JS 截获编辑按键——依赖浏览器内置编辑（[UA-24]，[官方文档](https://www.w3.org/WAI/ARIA/apg/patterns/spinbutton/)）。触屏 AT 对 slider 类手势操作支持不全，生产前须触屏实测 [官方文档](https://www.w3.org/WAI/ARIA/apg/patterns/slider/)。

## 高频坑点（速查）

### 坑点速查表

（与法则/场景逐字重复的坑点不再单列，见对应 [UA-N] 与场景 1~12。）

| 症状 | 根因 | 修复 | 关联 |
|---|---|---|---|
| Tab 焦点不可见；axe 报 focus-visible 缺失 | reset 模板带 `outline: none`；替代对比 <3:1 | `button:focus{outline:none}` ✗；`:focus-visible{outline:2px solid #1a73e8;outline-offset:2px}`（≥3:1）✓。axe 原文 `focus-order-semantics`；Lighthouse "Focusable elements have a visible focus indicator" | [UA-1] |
| 白底 #999「高级感」文案不可读（审计报 2.85:1） | 心中无 #767676 合格灰锚点 | `.muted{color:#999}` ✗；`.muted{color:#767676}`（≈4.54:1）✓；大文本 `#949494`（24px，≈3.0:1）达标 | [UA-4] |
| 键盘无法操作自定义下拉/标签页；表格读屏无结构 | div/span+onclick 只实现 mouse 事件；缺 caption/th scope | 原生元素或补 role/keydown/方向键；补 `<caption>`+`th scope` | [UA-2] |
| icon 按钮读屏只念「按钮」；语音用户说「点保存」无响应 | 缺 accessible name；名称与可见标签不一致（2.5.3） | aria-label，名称含可见标签文本（前缀更佳） | [UA-15] |
| 500 报「请检查网络」；渲染 `Error: E11000` 原始 message | 错误分类粗粒度；后端原始 error 直接渲染 | 4xx/5xx/网络层分类；映射为用户语言三要素文案 | [UA-8] |
| 放大 200% 或 320px 宽出现横向滚动 | 固定宽度容器/长串不换行/grid 列不响应 | max-width 百分比+`overflow-wrap: break-word`（1.4.10） | [UA-4] |
| tabs/工具栏 Tab 序列爆炸：20 个 tab 按 20 次 Tab | 每个子项都是 Tab 停靠点，缺 roving tabindex/aria-activedescendant | 组件单停靠点+方向键内部移动（场景 12） | [UA-21] |
| 切换按钮选中后标签从「静音」变「取消静音」，读屏播报混乱 | aria-pressed 与标签变化并用，破坏状态语义 | 标签恒定+aria-pressed；标签必须变则弃 aria-pressed | [UA-22] |
| 自动轮播读屏读到下一张而不自知；键盘无法停轮播 | 无停止控件；焦点进入不停转 | 停止/重启钮（Tab 首元素）+焦点进入即停（[UA-26]） | [UA-26] |

## 参数速查表（API 速查）

### WCAG 2.2 关键成功标准速查

| 条款 | 名称 | 级别 | 阈值/要求 |
|---|---|---|---|
| 1.1.1 | Non-text Content | A | 图片需 alt；装饰图 `alt=""` |
| 1.2.1~1.2.5 | 时基媒体 | A/AA | 纯音/视频给文字稿；预录视频配字幕(1.2.2)+音频描述(1.2.3/1.2.5)；直播实时字幕(1.2.4) |
| 1.3.1~1.3.3 | Adaptable 基础 | A | 结构/关系可编程确定（heading/label/table 语义）；DOM 序即阅读序；指令不只靠形状/位置 |
| 1.3.4/1.3.5 | Orientation / Identify Input Purpose | AA | 不锁横竖屏（essential 除外）；常用字段 purpose 可编程确定（autocomplete） |
| 1.4.1 | Use of Color | A | 颜色不得为唯一信息载体；纯色链接与正文 ≥3:1 |
| 1.4.3 | Contrast (Minimum) | AA | 正文 4.5:1；大文本 3:1（≥24px 或 ≥18.66px bold）；豁免装饰/inactive/logo |
| 1.4.4 | Resize Text | AA | 200% 缩放可读可用 |
| 1.4.6 | Contrast (Enhanced) | AAA | 正文 7:1；大文本 4.5:1 |
| 1.4.10 | Reflow | AA | 320px 宽无横向滚动、无内容丢失（表格等本质例外除外） |
| 1.4.11 | Non-text Contrast | AA | 图形/UI 组件/焦点指示器 ≥3:1，各状态维持（边框、图标同适用） |
| 1.4.12 | Text Spacing | AA | 行高 1.5×、段距 2×、词距 .16×、字距 .12× 覆盖后内容不丢失 |
| 2.1.1 | Keyboard | A | 全部功能键盘可达 |
| 2.1.2 | No Keyboard Trap | A | 焦点可移出（ESC 等常规手段） |
| 2.2.1 | Timing Adjustable | A | 限时可关闭/调整/延长（警告+≥20s 延长；实时活动/essential 例外） |
| 2.2.2 | Pause, Stop, Hide | A | >5s 自动移动/闪烁/滚动须可暂停/停止/隐藏（轮播、marquee） |
| 2.3.1 | Three Flashes | A | 每秒闪烁 ≤3 次（光敏性癫痫） |
| 2.3.3 | Animation from Interactions | AAA | 交互触发的非必要动画可禁用（reduced-motion 条款依据） |
| 2.4.3 | Focus Order | AA | 焦点顺序保持意义与可操作性 |
| 2.4.1/2.4.2 | Bypass Blocks / Page Titled | A | 可跳过重复导航（skip link/landmark）；页面有描述性 title |
| 2.4.4/2.4.6 | Link Purpose / Headings and Labels | A/AA | 链接目的可判定；标题与标签描述性地表达主题 |
| 2.4.5 | Multiple Ways | A | ≥2 种定位页面方式（导航/搜索/站点地图），流程次步例外 |
| 2.4.7 | Focus Visible | AA | 键盘焦点有可见指示器 |
| †2.4.11 | Focus Not Obscured (Minimum) | AA | 聚焦元素不被作者内容完全遮挡 |
| †2.4.12 | Focus Not Obscured (Enhanced) | AAA | 聚焦组件完全可见 |
| †2.4.13 | Focus Appearance | AAA | 指示器面积 ≥ 未聚焦组件 2 CSS px 厚周长面积（矩形 `(w×4)+(h×4)`）；状态切换对比 ≥3:1 |
| 2.5.3 | Label in Name | AA | accessible name 包含可见标签文本 |
| 2.5.1/2.5.2/2.5.4 | Pointer 手势/取消/动作触发 | A | 多指与路径手势有单点替代；up 触发或可撤销；设备动作触发有 UI 替代可禁用 |
| 2.5.5 | Target Size | AAA | 44×44 CSS px（勿与 2.5.8 混淆） |
| †2.5.7 | Dragging Movements | AA | 拖拽须有免拖拽单指针替代（essential 除外） |
| †2.5.8 | Target Size (Minimum) | AA | ≥24×24 CSS px；例外：间距补偿/等效控件/行内/UA/essential |
| †3.2.6 | Consistent Help | A | 帮助机制在页面集合中相对位置一致 |
| 3.1.1/3.1.2 | Language of Page/Parts | A/AA | html lang 声明页面语言；外语片段 lang 标注（读屏切换发音引擎） |
| 3.2.1/3.2.2 | On Focus / On Input | A | 聚焦不触发上下文变更；输入不自动改变上下文（除非已提前告知） |
| 3.2.3/3.2.4 | Consistent Navigation/Identification | AA | 重复导航相对顺序一致；相同功能标识一致 |
| 3.3.1 | Error Identification | A | 错误以文本明确标识 |
| 3.3.2 | Labels or Instructions | AA | 字段有标签或指令 |
| 3.3.3 | Error Suggestion | AA | 错误自动纠正/给出修复建议 |
| 3.3.4 | Error Prevention (Legal, Financial, Data) | AA | 法律/财务/数据提交可回退/可验证/可确认 |
| †3.3.7 | Redundant Entry | A | 同流程已输入信息不强制重输（级别 A 见冲突记录） |
| †3.3.8 | Accessible Authentication (Minimum) | AA | 认知功能测试须有替代/辅助机制 |
| †3.3.9 | Accessible Authentication (Enhanced) | AAA | 同上且无物体识别例外 |
| 4.1.2 | Name, Role, Value | A | 自定义控件名称/角色/值可编程确定 |
| ~~4.1.1~~ | ~~Parsing~~ | — | WCAG 2.2 已 obsolete 移除，勿再引用 |

† = 2.2 新增。来源: [官方文档](https://webaim.org/standards/wcag/checklist) + [官方文档](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)；**A/AA 全部条款（含 1.1.1/2.4.3/2.5.3/3.3.2/4.1.2 等）已经 R34 规范全文逐字锚定**（docs/wcag22-spec-extracts.md，86 条 SC 原文，1.4.12 文本间距 1.5×/2×/.16×/.12×、2.2.1 ≥20s 延长、2.5.8 24×24 CSS px + 24px 直径圆间距例外等数值逐一核对通过）；分组行经 docs/wcag22-quickref-extracts.md（技法 G/ARIA/H/C/F/SL/SM/SCR 编号全名、Situation 分组、F 编号失败模式）复核；AAA 条款备查（31 条原文在 spec 语料）。**逐条审计检查点、技法编号与 80 项 F 失败模式速查见 wcag22-audit kb（v1，本表的执行层展开）。**

### APG 30 模式速查（WAI-ARIA Authoring Practices Guide）

来源: [官方文档](https://www.w3.org/WAI/ARIA/apg/patterns/)（R34 全量抓取，语料 docs/apg/ 30 文件+_index）。用法：实现任一自定义控件前先查此表定键盘契约，再读对应模式语料全文；**逐模式完整契约（键盘交互/ARIA 属性/易错点/焦点管理双方案）见 aria-patterns kb（v1，本表的执行层展开）。**

| 模式 | 核心 role | 键盘契约要点 |
|---|---|---|
| Accordion | heading>button | Enter/Space 切换面板；标题按钮 aria-expanded/controls；面板 region+labelledby（>6 个可同展开时免 region） |
| Alert | alert | 无键交互；不夺焦点；动态渲染自动播报（加载前已存在的不播报）[UA-25] |
| Alert/Message Dialog | alertdialog | 模态四件套（[UA-11]）；aria-describedby 必设 |
| Breadcrumb | nav | aria-label 标注 landmark；当前页 aria-current="page" |
| Button | button | Enter/Space；aria-pressed 标签恒定 [UA-22]；「…」后缀=打开对话框惯例 |
| Carousel | region/group + aria-roledescription | 焦点进入即停 [UA-26]；停止/重启钮为 Tab 首元素 |
| Checkbox | checkbox | Space 切换；aria-checked true/false/mixed（三态全选） |
| Combobox | combobox+popup | ↓ 开 popup；Esc 无损关 [UA-24]；Enter 接受建议；aria-autocomplete none/list/both |
| Dialog (Modal) | dialog | 四件套+初始焦点细则（场景 7）；aria-modal 取代 aria-hidden |
| Disclosure | button | Enter/Space 切换；aria-expanded/controls |
| Feed | feed | Page Down/Up 篇章导航；aria-posinset+setsize（总数未定 -1）；更新期 aria-busy（完必复位 false） |
| Grid | grid/row/gridcell | 方向键格间；Home/End 行首末；Ctrl+Home/End 网格首末；单 Tab 停靠；Enter/F2 进格、Esc 恢复 |
| Landmarks | 8 个 role | ≤7 个/页 [UA-23]；全部内容入 landmark |
| Link | link | Enter 执行；首选原生 a[href] |
| Listbox | listbox/option | ↑↓ 移动；Home/End（>5 项强烈建议）；type-ahead [UA-27]；Space 切换多选 |
| Menu/Menubar | menu/menubar/menuitem | 方向键导航；Esc 逐级关+焦点返还；Tab 移出并关闭全部菜单；Home/End（无环绕时） |
| Menu Button | button | Enter/Space/↓ 开菜单并聚焦首项；aria-haspopup="menu"+aria-expanded |
| Meter | meter | 无键交互；禁表进度 [UA-28]；aria-valuetext（如 "50% (6 hours) remaining"） |
| Radio Group | radiogroup/radio | 方向键移动并选中（环绕）；Space 选中聚焦项；Tab 落选中项 |
| Slider | slider | 方向键 ±step；Home/End 极值；触屏 AT 需充分实测 |
| Slider (Multi-Thumb) | slider×n | 每 thumb 独立 Tab 停靠且顺序恒定不随视觉位置变 |
| Spinbutton | spinbutton | ↑↓ 增减；Home/End 极值；可打印字符直接编辑；勿让 JS 截获编辑键 |
| Switch | switch | Space 切换（Enter 可选）；标签恒定 [UA-22]；HTML checkbox 实现用 checked 属性 |
| Table | table/row/cell | 静态非交互；含大量交互控件改 grid 缩短 Tab 序列 |
| Tabs | tablist/tab/tabpanel | ←→ 环绕（垂直 tablist 用 ↑↓）；活动 tab aria-selected；面板预载时建议聚焦自动激活 |
| Toolbar | toolbar | ←→ roving tabindex；Tab 单停靠 [UA-21]；≥3 控件才值得用 toolbar |
| Tooltip | tooltip | Esc 关闭；不接收焦点；触发元素 aria-describedby 引用 |
| Tree View | tree/treeitem | ←→ 开闭/入子级/回父级；↑↓ 移动；Home/End；type-ahead；仅父节点设 aria-expanded |
| Treegrid | treegrid/row/gridcell | grid+tree 组合：←→ 折叠/展开/格间，↑↓ 格间；选择键同 grid |
| Window Splitter | separator | 方向键移动分割器；Enter 折叠主窗格；aria-valuenow/min/max |

slug 修正记录：menu→`menubar`、window splitter→`windowsplitter`（见 docs/apg/_index.md）。

### Nielsen 十启发式速查（1994，2024-01-30 审校）

| # | 启发式 | 走查核心问句 |
|---|---|---|
| H1 | Visibility of System Status | 异步操作有反馈？位置明确？ |
| H2 | Match Between System and the Real World | 术语是用户的语言？循现实惯例？ |
| H3 | User Control and Freedom | 进得去出得来？支持 Undo/Redo？ |
| H4 | Consistency and Standards | 同类操作同图标同文案？合平台惯例？ |
| H5 | Error Prevention | 高风险有前置约束？slips 与 mistakes 都防？ |
| H6 | Recognition Rather than Recall | 选项可见？跨页信息不必记？ |
| H7 | Flexibility and Efficiency of Use | 有快捷键/默认值/加速器？ |
| H8 | Aesthetic and Minimalist Design | 每个信息单元都在稀释相关信息——去冗余 |
| H9 | Help Users Recognize, Diagnose, and Recover from Errors | 报错平实、精确、给建议 |
| H10 | Help and Documentation | 文档可搜索、聚焦任务、步骤简短 |

来源: [官方文档](https://www.nngroup.com/articles/ten-usability-heuristics/)（Molich & Nielsen 1990；1994 基于 249 个可用性问题因子分析）。

### 严重度评级 0~4（启发式评估）

| 级别 | 定义 |
|---|---|
| 0 | 非可用性问题 |
| 1 | 表面问题（cosmetic），不影响任务 |
| 2 | 次要问题（minor），受挫但能完成 |
| 3 | 主要问题（major），显著增加难度 |
| 4 | 灾难（catastrophe），阻碍任务完成，交付前必须修 |

三因子：频率/影响/持久性（+可选商业重要性）；映射见场景 9。来源: [模型经验] 05——0~4 与三因子为 Nielsen severity ratings 高置信记忆，**数值细节未经文档验证**。

## 版本注意

- **当前版本: WCAG 2.2**，2023-10-05 发布为 W3C Recommendation，2024-12-12 更新；脉络 2.0（2008-12-11）→ 2.1（2018-06-05，+1 guideline +17 SC）→ 2.2（+9 SC）[官方文档](https://www.w3.org/WAI/standards-guidelines/wcag/)。
- **4.1.1 Parsing 在 WCAG 2.2 中已 obsolete（移除）**，不得再作审计/规范引用依据 [官方文档](https://www.w3.org/WAI/standards-guidelines/wcag/)、[官方文档](https://webaim.org/standards/wcag/checklist)。向后兼容：符合 2.2 即符合 2.1/2.0；后版本只增不改已有条款（4.1.1 除外）。
- WCAG 2.2 已成为 ISO 标准 **ISO/IEC 40500:2025**；**ISO/IEC 40500:2026**（对应 2024-12-12 版 WCAG 2.2）预计 2026 年底发布（R39 复核）；**2026 版 EN 301 549**（欧洲 EAA 依据）采用 WCAG 2.2——欧洲市场直接按 2.2 执行 [官方文档](https://www.w3.org/WAI/standards-guidelines/wcag/)。
- 2.2 新增 9 条 SC 快记：2.4.11/12/13（焦点三连）、2.5.7/8（拖拽与目标）、3.2.6、3.3.7/8/9（帮助与认证）[官方文档](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)。Quick Reference: https://www.w3.org/WAI/WCAG22/quickref/
- **WCAG 2.2 规范全文锚定（R34 阶段 B）**：`https://www.w3.org/TR/WCAG22/`（W3C Recommendation 12 December 2024）第 1~4 章全部 86 条 SC 原文逐字落盘（docs/wcag22-spec-extracts.md，A 31 / AA 24 / AAA 31，含 obsolete 4.1.1 标注）；quickref 技法层落盘（docs/wcag22-quickref-extracts.md，87 条目含 2.0/2.1 兼容保留的 4.1.1 旧文，Sufficient Techniques 86 节/Advisory 36 节/Failures 53 节、"(Added in 2.2)" 9 处与 wcag-new-in-22.md 一一对应）。速查表 A/AA 全行升格为规范原文锚定（见冲突记录 10）。
- Nielsen 十启发式自 1994 定版不变，最新审校 2024-01-30 [官方文档](https://www.nngroup.com/articles/ten-usability-heuristics/)。
- **APG v3（R34 阶段 B）**：30 模式全量锚定（语料 docs/apg/），新增 [UA-21]~[UA-28]、场景 12、APG 模式速查表；模式计数更正 31→30（见冲突记录 9）。
- 留意 WCAG 3.0（评分制，非 A/AA/AAA）或带来的体系变化——当前合规仍以 2.2 为准 [模型经验] 02（置信中）。

## 与其他子领域的集成要点

- **color-system**: 对比度是色彩 token 的硬约束——text token 按底色逐对校验 4.5:1/3:1；状态色携带符号/文字第二通道（[UA-3]/[UA-4]）；深色模式用独立 token；验收标准即 1.4.3/1.4.6/1.4.11 阈值表。
- **interaction-motion**: [UA-13] 是动效的发布门槛——动画必须附 `prefers-reduced-motion: reduce` 降级与 >5s 内容暂停控件（2.2.2）；JS 动画经 matchMedia 分流。动效域定义"动什么"，本域定义"何时必须能停"。tooltip 升级路径与 APG Tooltip 契约一致：tooltip 不接收焦点、Esc 关闭、aria-describedby 引用；轮播动效服从 [UA-26] 停止纪律。
- **layout-composition**: 触控目标 24×24/44×44 是间距计算输入——相邻命中区不重叠；Reflow 要求 320px 单列无横向滚动（1.4.10）；sticky/fixed 布局搭配 `scroll-padding`（2.4.11）。
- **typography**: 1.4.3 大文本阈值（24px / 18.67px bold）决定哪些字号档位享 3:1 宽松对比；1.4.12 行高/段距覆盖不破版——token 不得写死绝对值；200% 缩放（1.4.4）依赖 rem/em。

## 来源索引

官方文档（阶段 2 真实抓取，白名单 URL）：
- https://www.w3.org/WAI/standards-guidelines/wcag/ → docs/wcag-2-overview.md（版本、POUR、级别、4.1.1 obsolete、ISO 40500:2025、EN 301 549:2026）
- https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/ → docs/wcag-new-in-22.md（2.2 新增 9 条 SC 全文，含 2.4.13/2.5.8 数值与例外）
- https://webaim.org/standards/wcag/checklist → docs/webaim-wcag-checklist.md（对比度/目标尺寸/焦点/动效/文本间距阈值；2.5.5=44×44 AAA）
- https://www.nngroup.com/articles/ten-usability-heuristics/ → docs/nielsen-10-heuristics.md（十启发式逐字措辞与出处）
- https://www.nngroup.com/articles/ （文章索引；heuristic-evaluation 文章入口确认存在）
- https://www.w3.org/TR/WCAG22/ → docs/wcag22-spec-extracts.md（R34 全文提取：86 条 SC 规范原文逐字，A/AA/AAA 全级别；速查表 A/AA 行锚定源）
- https://www.w3.org/WAI/WCAG22/quickref/ → docs/wcag22-quickref-extracts.md（R34 全文提取：技法编号全名/Situation 分组/F 失败模式/SC 原文对照；87 条目含 2.0/2.1 兼容的 4.1.1 旧文）
- 抓取批次日志: docs/_fetch_log_r34-wcag.md（两源无截断、零遗漏记录）
- https://www.w3.org/WAI/ARIA/apg/patterns/ → docs/aria-apg-patterns-index.md（30 个 ARIA 模式官方清单，R33 锚定、R34 计数更正）
- https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ → docs/aria-apg-dialog-modal.md（模态键盘交互与 ARIA 属性全文，R33 锚定）
- https://www.w3.org/WAI/ARIA/apg/patterns/<slug>/ × 29 → docs/apg/（R34 阶段 A 全量抓取：30 模式语料+apg/_index.md+3 份批次日志 _fetch_log_r34-apg-{a,b,c}.md；dialog-modal 语料在 docs/ 根）

模型经验（elicited，前缀 corpus/ui-ux-design/usability-accessibility/elicited/）：01-nielsen-heuristics（响应阈值归属存疑）、02-wcag（A/AA 措辞已由 R34 spec 语料升格锚定）、03-a11y-visual、04-error-prevention、05-heuristic-evaluation（0~4 细则未验证）、06-ai-mistakes、07-laws、08-wcag22-aa-full（已由 R34 spec 语料取代锚定地位）、09-screen-reader-aria（APG 30 模式已全量锚定）、10-i18n-rtl（膨胀系数待校准）。

降级状态：未降级（WCAG/WebAIM/NN/g/APG-30 模式 五源锚点齐备，见 docs/_fetch_log.md 与 _fetch_log_r34-apg-*.md）。

## 冲突消解记录

1. 3.3.7 级别：记忆 **AA** → 文档 **A** [官方文档](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/) → 以文档为准，入速查表与场景 7。
2. 2.4.13 数值「低置信待验证」→ 证实：面积 ≥ 2 CSS px 厚周长面积（矩形 (w×4)+(h×4)）、切换对比 ≥3:1 [官方文档](https://webaim.org/standards/wcag/checklist) → 入速查表与场景 2。
3. 2.5.8 间距豁免「判定公式不确定」→ 24px 直径圆不与其他目标圆相交，另有等效控件/行内/UA/essential [官方文档](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/) → 例外清单入场景 6。
4. 2.2 发布日 2023-10-05「置信中」→ 文档证实（2024-12-12 更新），升格硬事实。
5. 广度轮遗漏 3.2.6 (A)、2.4.12 (AAA)、3.3.9 (AAA) → 2.2 新增共 9 条：2.4.11/12/13、2.5.7/8、3.2.6、3.3.7/8/9 [官方文档](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/) → 补全入速查表与场景 7。
6. placeholder 当 label「是否违反 3.3.2 待验证」→ 文档锚点未覆盖逐字措辞 → 维持实践禁令（[UA-7]），不宣称条款级违反。
7. 单评估者 ~35% 发现率、严重度 0~4（置信中）→ NN/g 入口存在但内容未抓取 → 维持 [模型经验]，显式声明「未经文档验证」。
8. 模态四件套/role="dialog"/aria-modal/焦点返还（置信中）→ APG Dialog (Modal) Pattern 全文证实（含 Tab 首尾环绕、可见关闭钮必入 tab 序、aria-modal 取代 aria-hidden）→ [UA-11] 升格 [官方文档]，细则入场景 7 锚点。
9. APG 模式计数：R33 索引自注 **31 项** → R34 全量抓取逐项清点为 **30 项**（30 语料+slug 修正记录见 docs/apg/_index.md）→ 以 30 为准，v2 的「31 模式」表述已全部更正；aria-apg-patterns-index.md 批注同步更正。
10. 速查表「逐字措辞未验证」降级（v3）→ R34 规范全文提取（TR 86 条 SC + quickref 技法层）→ A/AA 全部条款升格 [官方文档] 逐字锚定；elicited/02（wcag）与 08（wcag22-aa-full）的「逐字措辞未验证」标注就此作废，以 spec 语料为准；placeholder 当 label（[UA-7]）维持实践禁令但 3.3.2 条款级锚定已补齐。
