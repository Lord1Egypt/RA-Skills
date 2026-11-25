---
domain: ui-ux-design
skill_name: ui-ux-design-expert
subdomain: aria-patterns
title: WAI-ARIA APG 模式契约（30 模式键盘交互与 ARIA 属性全量）
version: 1
updated: 2026-11-17
source_index:
  docs: corpus/ui-ux-design/usability-accessibility/docs/apg/（30 模式语料 + _index.md + 3 份 _fetch_log_r34-apg-{a,b,c}.md）+ docs/aria-apg-dialog-modal.md（Dialog Modal 全文）+ docs/aria-apg-patterns-index.md
knowledge_ratio: 法则 20% / 模式契约 70% / 焦点管理对照 10%
merged_at: 2026-11-17
---

# WAI-ARIA APG 模式契约（aria-patterns）

本文件是自定义控件实现的**执行层契约**：WAI-ARIA APG（Authoring Practices Guide）30 个模式的键盘交互、角色/状态/属性与易错点逐模式展开。与 usability-accessibility kb 的分工：UA kb 的「APG 30 模式速查表」是一行式索引，本文件是逐模式完整契约——**实现任一自定义控件前先读本文件对应模式**，审计发现 4.1.2/4.1.3 违反（wcag22-audit kb）后按本文件契约修复。

全部内容 [官方文档] 逐字锚定（语料 docs/apg/ 30 文件 + dialog-modal 全文，源 https://www.w3.org/WAI/ARIA/apg/patterns/）。模式计数 30（R34 全量清点更正历史「31 模式」口径，见 UA kb 冲突记录 9）。

## 法则

**[AP-1]** MUST: 原生优先——ARIA 第一法则：有原生宿主语言等价物（`button`/`a[href]`/`select`/`input`/`table`）时一律用原生；给元素加 WAI-ARIA role **不会**让浏览器赋予标准行为（导航、激活、上下文菜单），全部行为由作者负责。原生可解决的场景用 ARIA 是负担，原生解决不了才照本契约实现。源: APG Link/Button/Table
**[AP-2]** MUST: 复合控件单 Tab 停靠——tabs/toolbar/menubar/menu/listbox/grid/tree/treegrid/radiogroup/combobox 在页面 Tab 序列中只占**一个**停靠点；Tab 进出组件、方向键在组件内移动焦点（例外：multi-thumb slider 每 thumb 一个停靠点；carousel 控件随结构）。源: APG Grid/Menubar/Listbox/Tabs/Toolbar
**[AP-3]** MUST: 焦点管理二选一——roving tabindex（当前项 `tabindex="0"` 其余 `"-1"`，方向键移动时交换并 focus）或 `aria-activedescendant`（容器 `tabindex="0"` 持 DOM 焦点，ID 属性指向逻辑当前项）；同一组件内不得混用两方案；经 `aria-owns` 引入的项排在 DOM 后代之后进入 AT 阅读顺序，脚本须保证视觉焦点顺序与之一致。源: APG Menubar/Listbox/Tree/Grid
**[AP-4]** MUST: 标签恒定——用 `aria-pressed`（toggle button）/`aria-checked`（switch/checkbox）表达状态时，控件可见标签在状态切换前后**绝不能改变**（静音按钮 pressed 后仍叫「Mute」）；设计确需标签随状态变化则弃用状态属性（改双标签或标签切换）。源: APG Button/Switch
**[AP-5]** MUST: `aria-expanded` 与真实可见性同步——popup/面板可见 true、不可见 false；不控制子内容显示的元素**不设** `aria-expanded`（treeview 末端节点、treegrid 非父行误设会被 AT 错误描述为父节点）。源: APG Accordion/Disclosure/Menu Button/Tree View/Treegrid
**[AP-6]** MUST: 值语义五件套——slider/spinbutton/meter/separator 类控件设 `aria-valuenow`（+有界的 `aria-valuemin`/`aria-valuemax`）；`aria-valuenow` 对用户不友好时**必须**设 `aria-valuetext`（如星期、电池「50% (6 hours) remaining」）；垂直时设 `aria-orientation="vertical"`（各 role 默认 horizontal/vertical 见对应模式）。meter 禁用于进度（用 progressbar）与无意义上限量值。源: APG Meter/Slider/Spinbutton/Window Splitter
**[AP-7]** MUST: 动态集合属性——滚动加载/DOM 不全时逐项设 `aria-posinset`/`aria-setsize`（feed 总数未定用 **-1**）；DOM 多操作变更期间容器 `aria-busy="true"`，**完成时必须复位 false**，否则部分 AT 用户看不到变更。源: APG Feed/Listbox/Tree View
**[AP-8]** MUST: 模态纪律——dialog 四件套（打开焦点移入/Tab 首尾环绕/Esc 关闭/关闭返还触发元素）；仅当「代码阻止所有用户与框外交互」且「视觉遮蔽框外内容」两条件都满足才标 `aria-modal="true"`（ARIA 1.1，取代 aria-hidden 标 inert）；`aria-describedby` 仅简单描述性内容设、结构化内容**省略**（结构化内容先聚焦 `tabindex="-1"` 静态起始元素）；alertdialog 的 `aria-describedby` **必设**指向 alert 消息（与 dialog 的可选不同）。源: APG Dialog (Modal)/Alert Dialog
**[AP-9]** MUST: `aria-selected` 与 `aria-checked` 二选一——listbox/tree 同一组件内不得混用（极罕见双用须各自含义明显+独立控制）；无更合适因素时推荐惯例：单选用 `aria-selected`、多选用 `aria-checked`，全站一致；「全选/取消全选」是重要功能时实现**独立控件**（Select All 按钮），不靠快捷键承载。源: APG Listbox/Tree View
**[AP-10]** MUST: selection follows focus（选择跟随焦点）按场景评估后才启用——单选 listbox/单选树中「焦点即选中」部分场景有用、部分场景**严重损害可访问性**，须按官方指引逐场景判断并在文档记录决策。源: APG Listbox/Tree View
**[AP-11]** MUST: 环绕语义区分——radio group/tabs/menu 内方向键**环绕**（末项→首项）；**数据 grid/treegrid 不环绕**（AT 用户会迷失，行/列边界处不动）；布局 grid 的环绕有用可选。源: APG Grid/Radio/Tabs
**[AP-12]** MUST: 文本编辑类依赖浏览器内置编辑——combobox 输入框/spinbutton 文本框用 `input type=text` 或 `contenteditable`，**勿让 JS 捕获编辑按键**干扰浏览器单行文本编辑；焦点在 combobox/spinbutton 上时方向键归控件语义而非滚动。源: APG Combobox/Spinbutton
**[AP-13]** MUST: 触屏 AT 实测——slider 与 multi-thumb slider 官方警告：触屏 AT 需经合成键事件响应增减值手势，该新约定可能未被部分 AT 完整实现；生产部署前必须在触屏为主设备上用 AT 充分测试。源: APG Slider/Slider (Multi-Thumb)
**[AP-14]** SHOULD: 禁用项可聚焦性——菜单禁用项**仍可聚焦但不可激活**（`aria-disabled="true"`，不摘出 Tab/焦点管理序列）；carousel 当前 slide 选择按钮用 `aria-disabled="true"` 优于 HTML `disabled`（留在 Tab 序列对读屏用户更有益）；功能可发现性关键时 toolbar 禁用控件同样保持可聚焦。源: APG Menubar/Carousel/Toolbar
**[AP-15]** MUST: 无桌面惯例的模式（feed）必须提供**易发现的键盘接口文档**——官方明示因无惯例，文档尤为重要；嵌套 feed 提供专用键（如 Alt+Page Down）时同步文档。源: APG Feed
**[AP-16]** MUST: 进行中模式显式声明——tooltip（issue 127/128，工作组尚无共识）与 window splitter（issue 129/130，ARIA 1.1 修订未完成评审）为进行中工作；采用时向相关方声明「模式未定稿，可能随 APG 更新调整」。源: APG Tooltip/Window Splitter
**[AP-17]** MUST: 方向键与视觉排列解耦——组件垂直排列时 Down/Up 同水平件的 Right/Left（tabs/listbox/toolbar/tree/menubar 垂直变体）；水平 tablist **不监听** Up/Down（保留浏览器滚动）；互换规则在各模式「垂直排列」注记。源: APG Tabs/Listbox/Toolbar/Tree View/Menubar
**[AP-18]** MUST: 初始焦点规则——Tab 进入复合控件：有选中项落选中项（tabs 落活动 tab、radio/多选落第一选中项），无选中落第一项；menubar 曾持焦点可落上次项；对话框初始焦点按内容性质四分支（见模式 9）。源: APG 各复合模式 + Dialog (Modal)

## 焦点管理双方案对照（[AP-3] 展开）

| 维度 | roving tabindex | aria-activedescendant |
|---|---|---|
| DOM 焦点 | 移动到当前项（真 focus()） | 恒在容器，不移动 |
| 关键属性 | 当前项 `tabindex="0"` 其余 `"-1"` | 容器 `tabindex="0"` + `aria-activedescendant="当前项ID"` |
| AT 焦点跟随 | 浏览器原生 | 随 ID 属性值移动 |
| 支持模式 | 全部复合模式 | menu/listbox/tree/grid（dialog popup **不支持**——DOM 焦点须真移入） |
| 适用考量 | 项内容复杂/含部件时稳 | 长列表虚拟化友好；ID 引用须实时维护 |
| 共同纪律 | 单 Tab 停靠（[AP-2]）；方向键移动；不混用 | 同左 |

## 模式契约（30 模式）

### 1. Accordion（手风琴/可显隐分区）
- 键盘：焦点在折叠面板标题上 **Enter/Space** 展开面板；只允许单面板展开的实现展开同时折叠另一面板；焦点在已展开面板标题上 Enter/Space 折叠（要求始终至少一面板展开的实现不支持折叠）；Tab/Shift+Tab 走正常页面序列（手风琴内全部可聚焦元素入 Tab 序列）。
- ARIA：标题文本置于 `role="button"` 元素；按钮外裹 `role="heading"`（`aria-level` 按信息架构；有原生 h 元素用原生），heading 内只含 button；按钮 `aria-expanded`（面板可见性，[AP-5]）+`aria-controls` 指向面板；不可折叠时按钮 `aria-disabled="true"`；面板可选 `role="region"`+`aria-labelledby` 指向按钮（嵌套手风琴/含标题面板尤益），**超过约 6 个可同展开面板时免 region**（防 landmark 激增）。
- 易错点：heading 里塞常驻附加元素（只许 button）；region 滥用。

### 2. Alert（警报）
- 键盘：不适用（无键盘交互）。
- ARIA：元素 `role="alert"`。
- 易错点：**动态渲染的 alert 被读屏自动播报，页面加载前已存在的 alert 不播报**；alert 不得影响键盘焦点（与 Alert Dialog 的本质区别——需打断工作流才升级 alertdialog）；避免自动消失（过快可违反 2.2.1/2.2.2 精神）；控制打断频率（频繁打断损害视障与认知障碍用户）。

### 3. Alert and Message Dialogs（警报与消息对话框）
- 键盘：同 Dialog (Modal) 四件套（模式 9）。
- ARIA：容器 `role="alertdialog"` + `aria-modal="true"`；有可见标签 `aria-labelledby`（否则 `aria-label`）；**`aria-describedby` 必设**指向 alert 消息元素（[AP-8]，与 dialog 可选 describedby 不同）。
- 易错点：把普通通知做成模态打断（通知用 alert/status 即可）；describedby 漏设。

### 4. Breadcrumb（面包屑）
- 键盘：不适用（常规链接导航）。
- ARIA：轨迹置于 `nav` landmark 内；landmark 用 `aria-label`/`aria-labelledby` 标注（重复 nav 区分的典型场景）；指向当前页的链接 `aria-current="page"`（非链接元素可选）。
- 易错点：nav 无 label 与主导航混同。

### 5. Button（按钮）
- 键盘：**Space** 激活；**Enter** 激活；激活后焦点去向按动作类型：开对话框→焦点移入；关对话框→返还触发按钮（除非逻辑指别处）；不关上下文（Apply/Recalculate）→留在按钮上；指示上下文变更（向导下一步）→移到动作起点；快捷键激活→留在原上下文。
- ARIA：`role="button"` + accessible name（内部文本/`aria-labelledby`/`aria-label`）；附加描述 `aria-describedby`；不可用 `aria-disabled="true"`；toggle button 用 `aria-pressed` 且**标签恒定**（[AP-4]：pressed 后仍叫「Mute」；设计要标签变则弃 aria-pressed）；menu button `aria-haspopup="menu"`。
- 易错点：标签加「…」=打开对话框的惯例（「Save as…」）；视觉像链接行为是按钮的元素——**更优方案是改视觉匹配功能**而非只换 role。

### 6. Carousel（轮播）
- 键盘：自动轮播在**任一元素获得键盘焦点时停止**，除非用户激活轮播控件不恢复；Tab/Shift+Tab 正常序列；激活上一张/下一张**不移动焦点**（便于反复激活）；轮播控制按钮是轮播内 Tab 序列**第一元素**；slide 选择器用 tabs 时按 Tabs 模式。
- ARIA：容器 `role="region"` 或 `group` + `aria-roledescription="carousel"` + 可见标签 `aria-labelledby`（否则 `aria-label`；标签不含「carousel」一词）；每 slide `role="group"` + `aria-roledescription="slide"` + accessible name（无名用「3 of 10」序号）；停止/重启按钮标签随动作变化（Stop/Start slide rotation），因标签变化**不设** aria-pressed；Tabbed 变体 slide 容器 `role="tabpanel"`（去 roledescription）+ tablist 选择器；Grouped 变体选择按钮组 `role="group"`+`aria-label`，当前 slide 选择按钮 `aria-disabled="true"`（[AP-14]，优于 HTML disabled）；slide 集合可选 `aria-atomic="false"`+`aria-live`（自动轮播 `off`、非自动 `polite`）。
- 易错点：不可见 slide 未正确隐藏（off-screen 残留致读屏混乱）；鼠标悬停不停止。

### 7. Checkbox（复选框）
- 键盘：**Space** 改变状态。
- ARIA：`role="checkbox"` + label 三选一（内文本/`aria-labelledby`/`aria-label`）；`aria-checked`：true/false/**mixed**（三态全选：mixed 反射并控制组内双态复选框——全选 true、部分 mixed、全不选 false）；组有可见标签置 `role="group"`+`aria-labelledby`；附加描述 `aria-describedby`。
- 易错点：三态全选用两态实现（缺 mixed）；HTML `input[type=checkbox]` 上叠 aria-checked（用原生 checked 属性）。

### 8. Combobox（组合框）
- 键盘（焦点在 combobox，popup 指示按钮与 popup 后代**排除在 Tab 序列外**）：**↓** 打开 popup 移焦入内（自动选中建议时落其后一条）；**↑**（可选）移到 popup 末元素；**Esc** 关闭 popup（可再按清空）；**Enter** 接受选中建议（editable）；可打印字符输入（editable）；editable 支持平台标准单行编辑键（[AP-12]：依赖浏览器内置编辑）；Alt+↓/↑（可选）只开关 popup 不动焦点。listbox popup 内（DOM 焦点留 combobox，`aria-activedescendant` 移 AT 焦点）：Enter 接受并关；Esc 关闭返还；↑↓ 移动且**选择跟随焦点**（单选，[AP-10]）；Home/End（可选）首末项；**Esc 无损关闭**——可浏览选项不丢已选值（combobox 优于单选 listbox 的关键事实）。grid/tree popup 按各自模式；**dialog popup 必须真移 DOM 焦点**（dialog 不支持 aria-activedescendant）。
- ARIA：输入元素 `role="combobox"`；`aria-controls` 指向 popup（ARIA 1.0 的 `aria-owns` 改用 `aria-controls`）；popup 隐式 `aria-haspopup="listbox"`（grid/tree/dialog 需显式）；`aria-expanded` 随 popup 可见性（[AP-5]）；`aria-autocomplete`：none（建议与输入无关）/list（manual selection）/both（automatic+inline completion）；label 用 HTML `label`/`aria-labelledby`/`aria-label`。
- 易错点：把 popup 按钮留在 Tab 序列（应排除）；截获编辑键破坏输入；listbox popup 里 Esc 当作「清除已选」（应无损）。

### 9. Dialog (Modal)（模态对话框）
- 键盘：打开**焦点移入**框内；**Tab/Shift+Tab 框内环绕**（含首尾环绕，非停边缘）；**Esc 关闭**；关闭**焦点返还触发元素**（触发元素已不存在→聚焦工作流逻辑元素，如加行后聚焦首行首格）；初始焦点四分支：默认第一个可聚焦元素；结构化内容（列表/表格/多段）先聚焦 `tabindex="-1"` 静态起始元素**且省略 aria-describedby**；内容长可能滚出开头→聚焦顶部静态元素；不可逆末步（删除/金融交易）→**聚焦最不破坏性动作**；纯信息/继续型→聚焦最常用元素（OK/Continue）。强烈建议 Tab 序列含**可见关闭控件**；强烈不建议 `tabindex`>0。
- ARIA：容器 `role="dialog"` + `aria-modal="true"`（[AP-8]：代码阻框外交互+视觉遮蔽两条件齐备才标 modal）；`aria-labelledby` 指可见标题（否则 `aria-label`）；`aria-describedby` 仅简单描述性内容设；遗留 `aria-hidden` 方案时框元素不得是 aria-hidden=true 的后代。
- 易错点：标 modal 不做 modal 行为（部分 AT 用户严重后果）；焦点陷阱漏 Shift+Tab 首环绕。

### 10. Disclosure（显隐控件）
- 键盘：**Enter/Space** 切换内容可见性。
- ARIA：控件 `role="button"`；`aria-expanded` 随内容可见性（[AP-5]）；可选 `aria-controls` 指向受控内容。
- 易错点：与 accordion 混同——disclosure 无 heading 包裹、无多面板联动；FAQ/折叠导航用此模式而非自造 div 交互。

### 11. Feed（动态加载流）
- 键盘（无桌面惯例，推荐接口）：**Page Down** 焦点到下一篇 article；**Page Up** 上一篇；**Control+End** 焦点到 feed 后第一个可聚焦元素；**Control+Home** feed 前第一个；嵌套 feed（文内评论流）提供专用键（如 Alt+Page Down）；article 内部件占用上述按键时部件优先。**因无惯例必须提供易发现的键盘接口文档**（[AP-15]）。
- ARIA：容器 `role="feed"`+label；每篇 `role="article"`+`aria-labelledby`（区分性标签）；**强烈推荐** `aria-describedby` 指向篇内主要内容；`aria-posinset` 表位置，`aria-setsize` 表已加载数或总数（未定 **-1**，[AP-7]）；增删期间容器 `aria-busy="true"`，**完成必须复位 false**。
- 易错点：aria-busy 忘记复位（部分 AT 用户看不到后续变更）；feed 当 widget 做（feed 是 structure，读屏以阅读模式交互——页面负责按焦点 article 滚动与加载，AT 保证阅读光标持 DOM 焦点）。

### 12. Grid（网格：数据网格/布局网格）
- 键盘（单 Tab 停靠，[AP-2]）：**数据网格**：←→↑↓ 格间移动（**边界不动，不环绕**，[AP-11]）；PageUp/Down 移指定行数；Home/End 当前行首末格；Ctrl+Home/End 全网格首末格；选择键：Ctrl+Space 选列、Shift+Space 选行、Ctrl+A 全选、Shift+方向键扩展选择。**布局网格**：方向键同上但行尾/列底**可选环绕**到下一行/列；Home/End 单列或每行少于三格时可选改全网格首末格。**格内导航**（两类共用）：格内单个不需方向键的部件（link/button/checkbox 等）→网格键直接聚焦该部件；格内文本/图形→聚焦单元格本身；**Enter/F2** 关闭网格导航进格内（编辑框/多部件），再按 F2 或 Esc 恢复；编辑中 Esc 可撤销；格内多部件时 ↑↓/←→ 在部件间移动（可环绕）；网格导航关闭期间方向键不再操作格内部件。
- ARIA：容器 `role="grid"`、行 `role="row"`（grid 或 rowgroup 后代）、格 `columnheader`/`rowheader`/`gridcell`；label 用 `aria-labelledby`/`aria-label`；描述 `aria-describedby`；排序 `aria-sort`；选中格/行 `aria-selected="true"`；部分格禁编辑 `aria-readonly="true"`（**不提供编辑的网格任何元素不含 aria-readonly**）；行列不全时 `aria-colcount`/`aria-rowcount`+`aria-colindex`/`aria-rowindex`（[AP-7]）；HTML table 加 grid role 时用 HTML rowspan/colspan（**不得**用 aria-rowspan/aria-colspan）。
- 易错点：数据网格每格不可聚焦（读屏应用模式只播报可聚焦元素，不可聚焦内容被忽略——行表头格不提供功能时可例外）；数据网格做环绕（AT 用户迷失）；动态加载下 Ctrl+End 只到 DOM 末行而非数据末行。

### 13. Landmarks（地标区域）
- 键盘：不适用（价值在结构语义与 AT 区块跳转）。
- ARIA：8 个 landmark role（main/navigation/search/banner/contentinfo/complementary/form/region）；HTML 元素隐含（`main`→main、`nav`→navigation）；重复 landmark 用 `aria-label` 区分。
- 易错点：一页 landmark **≤7 个**（越多价值越低）；**全部内容都应在合适 landmark 内**。

### 14. Link（链接）
- 键盘：**Enter** 执行链接并把焦点移到目标；Shift+F10（可选）开上下文菜单。
- ARIA：元素 `role="link"`。
- 易错点：**官方强烈建议用原生 `a[href]`**（[AP-1]）；加 link role 不带来导航行为——行为由作者负责；无 href 的 a 不入 Tab 序列。

### 15. Listbox（列表框）
- 键盘：初始焦点（[AP-18]）：单选无选中落第一项（可选自动选中）/有选中落选中项；多选无选中落第一项不改状态/有选中落第一选中项。**↑↓** 移动焦点（单选可选选择跟随焦点，[AP-10]）；**Home/End**（可选，**超 5 个选项强烈建议**）首末项；**Type-ahead**（推荐，**超 7 项尤其**）单字符/连打字符串跳匹配项。多选两模型任选：**推荐模型**（导航无需修饰键）：Space 切换焦点项状态；Shift+↑↓（可选）移动并切换；Shift+Space（可选）连续区间；Ctrl+Shift+Home/End（可选）到首末；Ctrl+A（可选）全选/取消全选。**替代模型**（不按修饰键移动即取消其余选中）：Shift+↑↓ 移动并切换；Ctrl+↑↓ 移动不改状态；Ctrl+Space 切换焦点项。
- ARIA：容器 `role="listbox"`；选项 `role="option"`（可含 `group` 分组，组须有 label）；独立 listbox 必有可见标签 `aria-labelledby` 或 `aria-label`；多选 `aria-multiselectable="true"`；每选项 `aria-selected` **或** `aria-checked` 二选一（推荐惯例：单选 selected/多选 checked，[AP-9]），选中 true、可选未选 false；**选中状态与焦点相互独立**（selection-follows-focus 除外）；滚动加载设 `aria-setsize`/`aria-posinset`；水平排列 `aria-orientation="horizontal"`（默认 vertical；水平时 ↓ 同 →、↑ 同 ←，[AP-17]）。
- 易错点：listbox 不承载交互元素列表（链接/按钮列表用 grid 模式）；选项名重复前缀（「国家+城市」）显著劣化键盘与读屏可用性——拆两个 listbox；选项名过长降低可理解性（整名一次播报）；全选重要时做独立 Select All 控件（[AP-9]）。

### 16. Menu and Menubar（菜单与菜单栏）
- 键盘（**Tab/Shift+Tab 不在菜单项间移动**）：Tab 移入 menubar 落第一项（曾持焦点可落上次项）；**焦点在菜单项上时 Tab 移出并关闭全部菜单与子菜单**；菜单打开时焦点置于第一项；**Enter**：有子菜单→打开子菜单聚焦其第一项；无→激活并关菜单；**Space**（可选）按项类型分支（checkbox 切换不关菜单/radio 选中不关菜单/开子菜单/激活）；**↓↑** 菜单内移动（可选环绕，[AP-11]；menubar 项上 ↓ 开其子菜单）；**→**：menubar 内移下一项；菜单内有子菜单项上→开子菜单；无子菜单项上→关闭本子菜单及父菜单、焦点移 menubar 下一项、（推荐）打开其子菜单不移入焦点；**←**：menubar 内移上一项；子菜单中→关闭子菜单返还父项；**Home/End**（不支持环绕时）首末项；**可打印字符**（可选）跳匹配项；**Esc** 关闭含焦点的菜单并**焦点返还**打开它的元素（menu button 或父菜单项）。
- ARIA：`role="menu"`/`role="menubar"`；项 `menuitem`/`menuitemcheckbox`/`menuitemradio`（menu/menubar 的子元素）；子菜单是紧随父 menuitem 的**兄弟元素**（同 menu 容器内）；父项 `aria-haspopup="menu"`+`aria-expanded`（[AP-5]）；焦点管理 [AP-3] 二选一（容器 `tabindex="-1"/"0"`+`aria-activedescendant`，或每项 `tabindex="-1"` 且 **menubar 首项 `tabindex="0"`**）；checkbox/radio 选中 `aria-checked="true"`；禁用项 `aria-disabled="true"`（**仍可聚焦不可激活**，[AP-14]）；分组 `role="separator"`（不可聚焦不可交互，`aria-orientation` 与方向一致）；label/`aria-orientation`（menubar 默认 horizontal、menu 默认 vertical；menubar 垂直时 ↓↔→、↑↔←，[AP-17]）。
- 易错点：网站导航误用 menu（menu 键盘模型复杂易做错——导航用普通 nav+button 更稳，menu 留给应用型命令菜单）；菜单项开对话框标签加「…」惯例；Tab 未关闭全部菜单。

### 17. Menu Button（菜单按钮）
- 键盘：**Enter/Space**（可选 ↓ 开菜单聚焦首项/↑ 聚焦末项）打开菜单并聚焦第一菜单项；打开后按 Menu and Menubar 模式。
- ARIA：按钮 `role="button"`+`aria-haspopup="menu"`；菜单显示时按钮 `aria-expanded="true"`（[AP-5]）；菜单容器 `role="menu"`；可选 `aria-controls` 指向菜单。
- 易错点：按钮 aria-expanded 与菜单可见性脱同步。

### 18. Meter（计量器）
- 键盘：不适用（纯展示 widget）。
- ARIA：`role="meter"`；`aria-valuenow`（介于 min/max 的十进制数）；`aria-valuemin`<`aria-valuemax`；AT 常把 valuenow 呈现为百分比——仅百分比对用户不友好时**必须**设 `aria-valuetext`（如 `"50% (6 hours) remaining"`，[AP-6]）；label 用 `aria-labelledby`/`aria-label`。
- 易错点：**禁用于进度**（加载/任务完成用 progressbar）；**禁用于无有意义上限的量值**（如当前世界人口）。

### 19. Radio Group（单选组）
- 键盘（非嵌于 toolbar）：**Tab/Shift+Tab** 移入移出（有选中落选中项、无选中落第一项，[AP-18]）；**Space** 选中聚焦项；**→/↓** 移到下一项并**取消之前项、选中新聚焦项**（选择跟随焦点；末项**环绕**回首项，[AP-11]）；**←/↑** 反向同样环绕。**嵌于 toolbar 的 radio group**（方向键归 toolbar 导航）：Space 选中聚焦项（不改其他）；Enter（可选）同 Space；→/← 在组内移动不改选中（组末/组首时移到 toolbar 下/上一元素，toolbar 末/首环绕到 toolbar 另一端）；↓/↑（可选）组内移动。
- ARIA：组容器 `role="radiogroup"`；每项 `role="radio"`；选中项 `aria-checked="true"`；每项 label（内容/`aria-labelledby`/`aria-label`）；组 label（`aria-labelledby`/`aria-label`）；附加信息 `aria-describedby`。
- 易错点：部分浏览器原生 radio 全未选时 Shift+Tab 进入落末项（与本契约「落第一项」不同——自定义实现按契约）；toolbar 内 radio 误用标准组的方向键语义。

### 20. Slider（滑块）
- 键盘（焦点置于 thumb 本身）：**→/↑** 值 +1 step；**←/↓** 值 −1 step；**Home** 最小值；**End** 最大值；PageUp/PageDown（可选）大步长增减；特定场景可反转方向（如 ↑ 减值更直观）。
- ARIA：thumb 元素 `role="slider"`；`aria-valuenow`/`aria-valuemin`/`aria-valuemax` 十进制数；valuenow 不友好时**必须** `aria-valuetext`（如 "Monday"，[AP-6]）；label（`aria-labelledby`/`aria-label`）；垂直时 `aria-orientation="vertical"`（默认 horizontal）。
- 易错点：**触屏 AT 实测强制**（[AP-13]：合成键事件手势约定可能未被部分 AT 实现）。

### 21. Slider (Multi-Thumb)（多拇指滑块）
- 键盘：**每 thumb 各自一个 Tab 停靠点**（[AP-2] 的例外）且各自有完整 Slider 键盘交互；**Tab 顺序恒定**——不随 thumb 值与视觉位置变化（低 thumb 越过高 thumb 后 Tab 序不变）。
- ARIA：每 thumb `role="slider"`+各自的 valuenow/min/max；相互依赖的 thumb（价格区间）在值变化时**动态更新依赖方的 aria-valuemin/aria-valuemax**；valuetext/label/orientation 同 Slider。
- 易错点：Tab 序随视觉位置重排（违反恒定原则）；依赖范围不更新；触屏实测强制（[AP-13]）。

### 22. Spinbutton（数值调节器）
- 键盘（焦点保持文本框）：**↑** 增值；**↓** 减值；**Home**（有最小值时）最小值；**End**（有最大值时）最大值；PageUp/PageDown（可选）大步长；文本框可编辑时支持平台标准单行编辑键+**可打印字符**（实现可只允许合法字符——时分 spinner 只许 0-59、冒号、AM/PM，其余输入不改变值）。
- ARIA：可聚焦元素 `role="spinbutton"`；`aria-valuenow`；有界时 `aria-valuemin`/`aria-valuemax`；valuenow 不友好必须 `aria-valuetext`（[AP-6]）；label（`aria-labelledby`/`aria-label`）；值超范围 `aria-invalid="true"`。
- 易错点：JS 截获编辑键破坏浏览器文本编辑（[AP-12]：用 `input type=text`/`contenteditable` 依赖内置编辑）。

### 23. Switch（开关）
- 键盘：**Space** 切换状态；**Enter**（可选）切换。
- ARIA：`role="switch"`；label 三选一（内文本/`aria-labelledby`/`aria-label`）；on `aria-checked="true"`/off `false`；HTML `input[type=checkbox]` 实现用 HTML `checked` 属性**而非** aria-checked；组场景置 `role="group"`+`aria-labelledby`（或 fieldset+legend）；附加描述 `aria-describedby`。
- 易错点：**标签在状态切换时绝不能改变**（[AP-4]）；与 checkbox/toggle button 选型按语义（"Lights switch on" 优于 "Lights checkbox checked"；预检清单用 checkbox）。

### 24. Table（静态表格）
- 键盘：不适用（静态结构非交互部件；交互表格用 Grid 模式）。
- ARIA：容器 `role="table"`；行 `role="row"`（table 或 rowgroup 后代）；格 `columnheader`/`rowheader`/`cell`；label（`aria-labelledby`/`aria-label`）；描述 `aria-describedby`；排序列头 `aria-sort`；行列不全时 `aria-colcount`/`aria-rowcount`+`aria-colindex`/`aria-rowindex`（[AP-7]）；跨行跨列按 Practice 设 `aria-rowspan`/`aria-colspan`。
- 易错点：**有原生 HTML table 一律用原生**（role=table 是 WAI-ARIA 1.1 新特性须逐浏览器+AT 组合测试，[AP-1]）；表中每个部件是页面 Tab 序列独立停靠点——部件多时换 grid 缩短 Tab 序列。

### 25. Tabs（标签页）
- 键盘：Tab 移入 tablist 落**活动 tab**（[AP-18]）；Tab 从 tab 移到 tablist 外下一元素（即 tabpanel，除非 tabpanel 首个实质内容元素可聚焦）；**水平 tablist**：←/→ 在 tab 间移动（**环绕**，[AP-11]），可选聚焦时自动激活；**垂直 tablist**：↑/↓ 同水平 ←/→（水平 tablist **不监听 ↑↓**，保留浏览器滚动，[AP-17]）；**Space/Enter** 激活（未自动激活时）；Home/End（可选）首末 tab；Shift+F10 开 tab 关联菜单；Delete（可选）删除当前 tab（焦点移下一 tab，末 tab 移前一 tab，全删走工作流逻辑元素）。
- ARIA：容器 `role="tablist"`；`role="tab"`（tablist 内）；面板 `role="tabpanel"`；tablist label（`aria-labelledby`/`aria-label`）；每 tab `aria-controls` 指向 tabpanel；**活动 tab `aria-selected="true"` 其余 false**；每 tabpanel `aria-labelledby` 指向对应 tab；tab 有关联菜单 `aria-haspopup="menu"`；垂直 `aria-orientation="vertical"`（默认 horizontal）。
- 易错点：tabpanel 无可聚焦元素或首个内容元素不可聚焦时 tabpanel 应设 `tabindex="0"` 入 Tab 序列；面板显示无显著延迟（内容预加载）才推荐**聚焦自动激活**——否则自动激活拖慢 tab 间导航。

### 26. Toolbar（工具栏）
- 键盘：Tab/Shift+Tab 移入移出（首次移入落第一未禁用控件；曾持焦点可落上次控件，[AP-18]）；**水平（默认）**：←/→ 在控件间移动（可选环绕，[AP-11]）；Home/End（可选）首末控件；**垂直**：↓ 同 →、↑ 同 ←（[AP-17]）；多行工具栏 ←/→ 逐行环绕导航，留垂直方向键供控件操作。
- ARIA：容器 `role="toolbar"`；label（`aria-labelledby`/`aria-label`）；垂直 `aria-orientation="vertical"`（默认水平）。
- 易错点：**≥3 个控件才用 toolbar** 作分组元素；避免纳入操作需占用与工具栏导航相同方向键对的控件（不可避免时只放一个且置于**最后**——水平工具栏末位的 textbox）；需快速访问时提供文档化快捷键移焦到工具栏（如编辑器 Alt+F10）。

### 27. Tooltip（工具提示）——进行中模式（[AP-16]）
- 键盘：**Esc** 关闭；焦点保持触发元素上（tooltip **不接收焦点**）。
- ARIA：容器 `role="tooltip"`；触发元素 `aria-describedby` 引用 tooltip。
- 易错点：含可聚焦元素的悬停层**升级为非模态 dialog**（不是 tooltip）；焦点触发的 tooltip 在 onBlur 关闭，指针悬停触发的在指针离开触发元素或 tooltip 时关闭；模式本身进行中（issue 127/128，无工作组共识、暂无官方示例）。

### 28. Tree View（树视图）
- 键盘（垂直树；水平树 ↓↔→、↑↔←，[AP-17]）：初始焦点（[AP-18]）：无选中落第一节点/有选中落选中节点（多选落第一选中节点）；**→**：关闭节点上→打开（焦点不动）；打开节点上→焦点移第一子节点；末端节点上→无操作；**←**：打开节点上→关闭；末端+关闭的子节点上→焦点移父节点；末端+关闭的根节点上→无操作；**↓/↑** 移到下一/上一可聚焦节点（不展开折叠）；**Home/End** 树中第一/最后可聚焦节点（不展开）；**Enter** 激活节点（父节点默认动作可为开/关；非跟随选择的单选树默认动作是选中聚焦节点）；**Type-ahead**（推荐，超 7 个根节点尤其）；**\***（可选）展开同级全部兄弟；多选两模型：**推荐模型**（无修饰键导航）：Space 切换聚焦节点；Shift+↓↑（可选）移动并切换；Shift+Space（可选）连续区间；Ctrl+Shift+Home/End（可选）到首末；Ctrl+A（可选）全选/取消。**替代模型**（不按修饰键移动即取消其余选中）：Shift+↓↑ 移动并切换；Ctrl+↓↑ 移动不改状态；Ctrl+Space 切换聚焦节点。
- ARIA：容器 `role="tree"`；节点 `role="treeitem"`；父节点含/拥有 `role="group"`（子节点在其中）；**父节点** `aria-expanded`（关闭 false/打开 true）——**末端节点不设 aria-expanded**（[AP-5]：误设被 AT 错述为父节点）；多选 `aria-multiselectable="true"`；选中 `aria-selected` **或** `aria-checked` 二选一（推荐单选 selected/多选 checked，[AP-9]）；不可选节点两者均不设；label 必备；动态加载设 `aria-level`/`aria-setsize`/`aria-posinset`（[AP-7]）；水平 `aria-orientation="horizontal"`（默认 vertical）。
- 易错点：全部节点都设 aria-expanded（只有父节点设）；选中态与焦点混同（selection-follows-focus 之外相互独立，[AP-10]）；全选重要做独立控件（[AP-9]）。

### 29. Treegrid（树格：分层数据网格）
- 键盘（行与单元格均可聚焦）：**Enter**（cell-only focus 且焦点在带 aria-expanded 的首格上）开/关子行；否则执行格默认动作；**Tab** 行内有可聚焦元素时移到行内下一个，行末移出 treegrid；**→**：折叠行上→展开；展开/无子行的行上→焦点移行内第一格；行最右格上→不动；其他格→右移一格；**←**：展开行上→折叠；折叠/无子行行上→不动；行内第一格且支持行焦点→焦点移到该行；第一格不支持行焦点→不动；其他格→左移一格；**↓/↑** 行间/格间移动（边界不动，不环绕，[AP-11]）；PageUp/Down、Home/End、Ctrl+Home/End 同 Grid 语义（行或格两套）；选择键：Ctrl+Space（行上全选/格上选列）、Shift+Space（选行）、Ctrl+A、Shift+方向键扩展（[AP-9] 语义同 grid）。
- ARIA：容器 `role="treegrid"`；行 `role="row"`（treegrid 或 rowgroup 后代）、格 `columnheader`/`rowheader`/`gridcell`；**父行**在行元素或行内某格设 `aria-expanded`——**不控制子行显示的行不设**（[AP-5]）；多选 `aria-multiselectable="true"`；选中行/格 `aria-selected`（单选其余不出现该属性）；label/描述/`aria-sort`/部分格禁编辑 `aria-readonly`（无编辑功能则任何元素不含）/`aria-colcount`/`aria-rowcount`/`aria-colindex`/`aria-rowindex`/HTML table 场景用 HTML rowspan/colspan——同 Grid 规则（[AP-7]）。
- 易错点：非父行误设 aria-expanded；读屏应用模式只播报可聚焦元素——行与格须含可聚焦元素或自身可聚焦（不提供功能的列头格例外）；方向键导航期间不可操作格内部件或移动编辑光标（Enter/F2 进出，同 Grid）。

### 30. Window Splitter（窗口分割器）——进行中模式（[AP-16]）
- 键盘：**←/→**（垂直分割器）左/右移动；**↑/↓**（水平分割器）上/下移动；**Enter** 折叠主窗格（已折叠时恢复前一位置）；Home/End（可选）主窗格最小/最大位置；F6（可选）窗格间循环切换。**固定尺寸分割器不实现方向键**。
- ARIA：可聚焦分割器 `role="separator"`；`aria-valuenow`（当前位置）/`aria-valuemin`（主窗格最小，通常 0）/`aria-valuemax`（主窗格最大，通常 100）；label 与**主窗格**名匹配（`aria-labelledby`/`aria-label`）；`aria-controls` 指向主窗格。
- 易错点：值语义按主窗格（读书应用目录为主窗格：目录全开=100、折叠=0）；模式按 ARIA 1.1 修订但未完成评审（issue 129/130，暂无官方示例）。

## 与其他子领域的集成要点

- **usability-accessibility**: 本文件是 UA kb「APG 模式速查表」的展开层；法则总纲（原生优先/单停靠/roving tabindex）见 [UA-2]/[UA-21]，本文件 [AP-1]/[AP-2]/[AP-3] 与之一致并逐模式细化；alert/alertdialog/carousel/combobox/meter 等 UA 法则（[UA-12]/[UA-25]/[UA-26]/[UA-24]/[UA-28]）在本文件对应模式有完整契约。
- **wcag22-audit**: 4.1.2（F59/F15）、4.1.3（F103）、2.1.1（F42/F54）、2.4.3（F44/F85）审计命中的修复实现一律回本文件对应模式契约。
- **interaction-motion**: tooltip 出现/消失时序与 IM 域 tooltip 纪律衔接（本契约只管键盘/ARIA，延迟参数归 IM）；carousel 停止纪律（[UA-26]）动效侧由 IM 落实。
- **layout-composition**: grid/treegrid 的行高与命中区（2.5.8 ≥24px）约束；feed 无限滚动与滚动收口/位置恢复实践互补。
- **ai-mistakes**: 自定义控件类 AI 错误（div 造控件漏 role/键盘）修复基准即本契约。

## 来源索引

- APG 30 模式语料全量: corpus/ui-ux-design/usability-accessibility/docs/apg/（accordion/alert/alertdialog/breadcrumb/button/carousel/checkbox/combobox/disclosure/feed/grid/landmarks/link/listbox/menu-button/menubar/meter/radio/slider/slider-multithumb/spinbutton/switch/table/tabs/toolbar/tooltip/treegrid/treeview/window-splitter.md；源 https://www.w3.org/WAI/ARIA/apg/patterns/ 及各模式子路径，R34 阶段 A/B/C 三批抓取）
- Dialog (Modal) 模式全文: corpus/ui-ux-design/usability-accessibility/docs/aria-apg-dialog-modal.md（源 https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/，R33 锚定）
- 模式索引与 30 计数: corpus/ui-ux-design/usability-accessibility/docs/apg/_index.md + corpus/ui-ux-design/usability-accessibility/docs/aria-apg-patterns-index.md（slug 修正记录：menubar/windowsplitter）
- 抓取批次日志: corpus/ui-ux-design/usability-accessibility/docs/_fetch_log_r34-apg-a.md、corpus/ui-ux-design/usability-accessibility/docs/_fetch_log_r34-apg-b.md、corpus/ui-ux-design/usability-accessibility/docs/_fetch_log_r34-apg-c.md
- 进行中模式状态（tooltip issue 127/128、window-splitter issue 129/130）: docs/apg/tooltip.md、docs/apg/window-splitter.md 原文批注

## 冲突消解记录

1. 模式计数：索引页自注 31 项 → 逐文件清点 30 语料 → 以 30 为准（与 UA kb 冲突记录 9 同源，本文件不再重复更正说明）。
2. tooltip「Esc 关闭」与 UA kb 速查表一致；「不接收焦点、触发元素 aria-describedby 引用」两源一致；tooltip 升级为非模态 dialog 的边界（含可聚焦元素）以 APG 原文为准。
3. listbox 多选「推荐模型 vs 替代模型」两模型并存非冲突——契约保留两模型由实现方选一并全站一致。
4. menubar 首项 `tabindex="0"`（焦点管理方案二）与 roving tabindex 通则不矛盾——是 [AP-3] 方案一在 menubar 的具体落点（每项 tabindex=-1，menubar 第一项 0）。
5. dialog popup 不支持 aria-activedescendant（combobox 模式明示）与 [AP-3] 支持 pattern 清单以 combobox 原文为准：dialog popup 必须 DOM 焦点真移入。

