---
domain: ui-ux-design
skill_name: ui-ux-design-expert
subdomain: interaction-motion
title: 交互与动效——操作反馈与动效如何降低感知成本
version: 3
updated: 2026-11-17
merged_at: 2026-11-16
knowledge_ratio: 法则 ~20% / 最佳实践 ~45% / 坑点 ~35%
source_index: corpus/ui-ux-design/interaction-motion/elicited/01~11（E1~E11 依次对应）；docs/apple-hig-index.md；docs/hig/motion.md（R34 实抓）；official_urls 与 fetch_status 见文末来源索引
---

# 交互与动效（interaction-motion）

## 定位与心智模型

本子领域：**操作反馈与动效如何降低感知成本**。核心心智：① **反馈是契约**——每个操作必须得到回应，无回应被判定「卡死」；② **动效是信息不是装饰**——回答「元素从哪来、到哪去、谁层级更高」，且必须有目的、不为动而动；不能作为传达重要信息的唯一方式，辅以 haptics、audio 等替代反馈通道 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/motion.md)；③ **等待是被设计的对象**——感知性能优先于压缩真实耗时。

适用边界：微交互、动效参数、加载体验、表单交互、页面转场、编排、滚动体验；不含品牌 Motion Identity、3D/WebGL、物理仿真。

## 法则

[GLOBAL] 为全局宪法候选（汇入 kb/laws.md）。E1~E11 全路径见来源索引。

[IM-1] **NEVER**: 动画必须用显式属性列表；NEVER `transition: all`/`transition-property: all`（无关属性连带动画→布局波浪+性能劣化）
[IM-2] **MUST**: 时长按交互层级：微反馈 100~150ms、常规转场 200~300ms、页面级/大位移 ≤450ms；NEVER >500ms 常规交互动效、<100ms 页面转场
[IM-3] **MUST**: 入场 ease-out（快出慢停）、退出 ease-in（慢起快走）；NEVER 反用
[IM-4] **NEVER**: 禁止动画 top/left/width/height/margin 等 layout 属性；必须 transform/opacity（否则每帧全管线，低端机 <30fps）
[IM-5] **[GLOBAL]** **MUST**: 异步操作必须有失败分支 UI：loading/success/error 三态齐全；NEVER 只写 happy path
[IM-6] **MUST**: 乐观更新必须配失败回滚（还原快照，NEVER 硬编码）+ pending 锁；低成功率操作（支付/扣库存）NEVER 乐观更新
[IM-7] **[GLOBAL]** **MUST**: 提交类按钮 pending 期间必须 disabled+进行中反馈；NEVER 提交中可点击
[IM-8] **MUST**: 可交互元素必须具备 hover/active/focus-visible 三态梯度 + cursor:pointer；触屏必须有非 hover 依赖反馈（:active/状态变化）。溯源：[官方文档](https://developer.apple.com/design/human-interface-guidelines.md)（Gestures/Inputs）
[IM-9] **MUST**: 所有动效必须在 `prefers-reduced-motion: reduce` 下降级（移除位移/缩放，保留无运动反馈）；平台侧 Reduce Motion 做法参照：减少自动与重复动画（缩放/zooming/周边运动）、收紧动画弹簧减少弹跳、动画直接跟随手势、避免 z 轴深度变化动画、以 fades 替代 x/y/z 轴位移过渡、避免出入模糊动画 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/motion.md)、[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/accessibility.md)
[IM-10] **MUST**: JS 动效逻辑与 CSS 时长单一来源同步（timeout ≥ CSS duration 或读 CSS 变量）；transitionend 必须 timeout 兜底（display:none/被打断/值未变时不触发）
[IM-11] **MUST**: 前进/返回转场方向对称（push 从右入则 pop 向右出）；形式匹配语义：深入=侧推、同级=交叉淡入 ≤200ms、模态=底部升起/中心缩放。溯源：[官方文档](https://developer.apple.com/design/human-interface-guidelines.md)（Materials）
[IM-12] **MUST**: 转场期间屏蔽点击穿透（旧页 pointer-events:none 或覆盖层）+ 锁导航栈防连点
[IM-13] **MUST**: 骨架屏必须镜像真实内容结构与尺寸（图片 aspect-ratio 占位）；显示延迟 200~300ms 防闪现
[IM-14] **MUST**: 等待 >1s 必须有进度指示；>10s 必须真实进度/预估/取消出口；NEVER 假进度停 ~90% 无真实信号
[IM-15] **[GLOBAL]** **MUST**: 同一数据源并发请求必须去重/取消过期请求（AbortController 或标识比对）
[IM-16] **MUST**: 校验时机以 onBlur 为主；error 态改 onChange 复查；NEVER 输入完成前报格式错误；提交全量校验+聚焦第一个错误字段
[IM-17] **MUST**: 错误提示必须同时具备：文字说明（非仅颜色/红框）+ 行动指引 + 就近位置 + 无障碍语义（aria-invalid + aria-describedby / role="alert"）；措辞 NEVER 指责用户
[IM-18] **NEVER**: 破坏性操作 NEVER 依赖原生 confirm() 作唯一防护；可恢复操作提供撤销（toast undo 窗口 ≥5s），不可恢复用内联二次确认 + destructive 视觉隔离（红色、与安全按钮分离）
[IM-19] **MUST**: 单元素并发动画属性 ≤2（opacity+transform 为上限）；弹窗/覆盖层打开期间锁背景滚动（body overflow + overscroll-behavior: contain）
[IM-20] **MUST**: 表单提交失败必须保留已填数据（仅成功后清理）；长表单自动保存草稿
[IM-21] **MUST**: stagger 交错间隔 30~80ms，序列总时长=间隔×(n-1)+单项时长 ≤600ms（超限收敛间隔/截断/分组）；仅对增量项交错
[IM-22] **MUST**: 入场/交互/转场三层独立时长预算，同一时刻仅一个编排主角；转场期间 NEVER 触发入场序列
[IM-23] **NEVER**: view-transition-name 同屏 NEVER 重名；FLIP 反演仅 transform/opacity，前后测量 MUST 同坐标系（滚动偏移补偿）
[IM-24] **MUST**: 每个滚动视图唯一主滚动容器；嵌套/弹层滚动容器 MUST `overscroll-behavior: contain` 收口防滚动链
[IM-25] **MUST**: 跨页滚动位置 MUST 显式恢复（`history.scrollRestoration:'manual'`+自存；虚拟列表先锚定数据再恢复偏移）；无限滚动 MUST 可达页脚且有终止条件
[IM-26] **MUST**: snap 严格度按内容选型（浏览型 mandatory/流式 proximity 或不用）；视差仅 transform 且 ≤2 层，reduced-motion 降级
[IM-27] **MUST**: 动效必须有目的（不为动而动）；高频 UI 交互一般不加自定义动效（系统标准元素已提供微妙动画）；动效 NEVER 作为传达重要信息的唯一方式，必须辅以 haptics、audio 等替代反馈通道 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/motion.md)
[IM-28] **MUST**: 反馈动效必须真实且符合手势预期（顶部下滑出现的视图不应侧滑消失）；反馈动画简短精确（轻盈不突兀），自定义元素避免每次交互强加多余动效 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/motion.md)
[IM-29] **MUST**: 动画必须允许中断——NEVER 迫使用户等动画播完才能继续操作（尤其重复经历的动画）[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/motion.md)
[IM-30] **MUST**: 空间动效（visionOS）纪律——避免视野边缘动效（周边视觉对运动敏感，分心+引发移动错觉）；大型虚拟对象移动时提高半透明度或降低对比度；对象重定位用 fade out → 移动 → fade in（无意义移动不引人追踪）；NEVER 让用户旋转虚拟世界（改用快速 fade-out 期间瞬时方向变化）；提供静止参照系；持续振荡对象特别敏感频率约 0.2 Hz（必须振荡时低振幅+半透明）[官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/motion.md)
[IM-31] **MUST**: 游戏/实时图形类保持 30~60 fps 帧率（流畅视觉体验标准），按设备图形能力提供默认画质，允许用户自定义视觉效果以优化性能/电量 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/motion.md)

（IM-21~23 源 E8、IM-24~26 源 E9）

## 核心概念速览

| 概念 | 定义 |
|---|---|
| 微交互 | Trigger→Rules→Feedback→Loops & Modes 四元组（Saffer） |
| 三阈值模型（Nielsen） | 见参数速查表·反馈阈值 |
| Doherty 阈值 | 响应 <400ms 进入「对话」心流（已锚定：Doherty & Thadani 1982，IBM Systems Journal；详见 kb/laws.md 与 kb/visual-perception.md） |
| 感知性能 | 缓存先渲染/prefetch/渐进加载让等待更短 |
| FLIP | 测前后 rect 差值、transform 反演再归零 |
| 共享元素转场（Hero） | 「同一个东西」的位置/尺寸连续过渡 |
| 缓动语义 | ease-out=入场、ease-in=退出、linear 仅匀速语义（进度条） |
| CLS | 累计布局偏移；骨架与内容不符直接劣化 |

## 最佳实践

### 1. 可交互元素全状态微反馈（桌面+触屏降级）

路径：五态梯度 → 微反馈 100~150ms ease-out、pressed scale(.97) → hover 包 `@media (hover:hover)`，触屏主反馈 `:active` → 焦点环。
- 错误: 仅颜色 hover，无梯度，触屏零反馈
- 正确: `.btn{cursor:pointer;transition:background-color 150ms ease-out,transform 150ms ease-out}` + `.btn:active{transform:scale(.97)}` + `.btn:focus-visible{outline:2px solid #007aff;outline-offset:2px}`

边界：混合输入设备 `:active` 不能省；disabled 需解释原因。源于 [IM-8]（HIG Gestures/Inputs）。

### 2. 乐观更新+回滚+提交锁

路径：同步代码内锁 pending → 乐观翻转 → 失败回滚 prev 快照并提示 → loading 态锁按钮尺寸。
- 错误: `const onClick=()=>{setLiked(!liked);api.like()}`——无锁无回滚
- 正确: `if(pending)return;setPending(true);const prev=liked;setLiked(!prev);try{await api.toggle(!prev)}catch{setLiked(prev);toast('操作失败，请重试')}finally{setPending(false)}`
- CSS: `.btn{min-width:120px}`（防 spinner 宽度塌陷）

边界：高失败率/强一致操作 NEVER 乐观更新（[IM-6]），改 pending+结果确认。

### 3. 按场景分层选动效参数（时长×缓动×距离）

路径：定层级 → 按层级与位移距离取时长 → 缓动按方向（入场 ease-out/退出 ease-in）→ 显式属性列表。
- 错误: `.btn/.modal/.page{transition:all .3s ease}`——模板手癖
- 正确: `.btn{transition:background-color 150ms ease-out,transform 150ms ease-out}` / `.modal{transition:opacity 200ms ease-out,transform 200ms ease-out}` / `.page{transition:transform 300ms cubic-bezier(0,0,0.2,1)}`

边界：距离-时长匹配（数值见参数速查表）；500ms 为常规体感上限；高频路径永远快而弱。源于 [IM-1]/[IM-2]/[IM-3]。

### 4. 可中断动画与 JS/CSS 状态同步

路径：可中断场景（drawer/modal）优先 transition/WAAPI → 时长单一来源，timeout ≥ duration+50ms → transitionend 加 timeout 兜底。
- 错误: `el.addEventListener('transitionend',onClose)`——事件丢失状态机卡死半开态
- 正确: `const t=setTimeout(onClose,DURATION+50);el.addEventListener('transitionend',()=>{clearTimeout(t);onClose()},{once:true})`
- 错误: animation 每次从 0 重播（快速开关 drawer 鬼畜）→ 正确: `el.style.transform=open?'translateX(0)':'translateX(100%)'`

边界：多段/循环编排用 animation+WAAPI `fill:'forwards'`；React 重播先查组件身份（模块级、稳定 key）。源于 [IM-10]。官方同向：动画必须允许中断，NEVER 迫使用户等动画播完（尤其重复动画）[IM-29] [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/motion.md)。

### 5. 页面转场与导航方向语义

路径：区分 PUSH/POP 原路对称 → 按语义选形式 → 转场期间锁栈+屏蔽穿透+锁滚动 → 数据请求与转场并行。
- 错误: 整页 fade——丢失空间线索
- 正确: `.page-enter{transform:translateX(100%);opacity:.6}` `.page-enter-active{transform:translateX(0);transition:transform 300ms cubic-bezier(0,0,0.2,1)}` `.page-exit-active{transform:translateX(-30%);pointer-events:none}`
- JS: `navAction==='PUSH'?'slide-from-right':navAction==='POP'?'slide-to-right':'none'`

边界：桌面弱化大位移；瞬态输入（搜索词）勿随转场丢失；返回恢复 scrollTop。源于 [IM-11]/[IM-12]（HIG Materials）。

### 6. 共享元素（Hero/FLIP）动效

路径：起终点 rect 差值 → transform translate+scale 反演 → 非等比缩放 content counter-scale 或容器裁剪 → 滚动容器先记录偏移再测量（同坐标系）→ 图片加载后再启动；旧元素 visibility:hidden 占位。
- 错误: 不考虑滚动的 FLIP——元素飞向屏幕外错误位置
- 正确: 记录 f=rect、s0=scrollTop → 布局变化后 l=rect，dy=(f.top-l.top)+(scroller.scrollTop-s0)，transform=translateY(dy)（符号方向置信中）

边界：多元素只选 1 个 hero 焦点（其余 fade）；起终点内容不同接受过渡中切换。源于 [IM-4]。

### 7. 加载体验：三态分支+骨架屏+竞态取消

路径：三态齐全+重试 → 骨架镜像目标结构（图片 aspect-ratio）、延迟 200~300ms → AbortController 取消过期响应 → 缓存先渲染。
- 错误: 两态渲染——error 时 data undefined，白屏 crash
- 正确: `if(loading)return <CardSkeleton/>;if(error)return <ErrorState message="加载失败" onRetry={refetch}/>;return <Content data={data}/>`
- 竞态: `useEffect(()=>{const c=new AbortController();fetch(q,{signal:c.signal}).catch(e=>{if(e.name!=='AbortError')throw e});return()=>c.abort()},[q])`

边界：分页增量加载保留已渲染列表+底部小 spinner；空态≠加载态。源于 [IM-5]/[IM-13]/[IM-15]。

### 8. 长任务进度反馈（>1s / >10s）

路径：>1s 进度指示就近（按钮内 spinner 优于遮罩）→ 真实进度优先；模拟则 ~90% 后等真实信号+阶段文案 → >10s 转异步任务模型+取消出口。
- 错误: `setInterval(()=>setP(p=>Math.min(p+1,99)),200)`——假进度永不到达
- 正确: `xhr.upload.onprogress=e=>setP(e.loaded/e.total*100)`（e.total 为 0 跨域无 Content-Length 时防除零）

边界：进度宜前快后慢；文案具体化。源于 [IM-14]。

### 9. 表单校验时机与错误呈现

路径：onBlur 主校验 → error 态 onChange 复查（改对即消错）→ 提交全量+聚焦第一个错误 → 错误三要素+无障碍语义。
- 错误: onChange 全量校验——打一半被「邮箱格式错误」轰炸
- 正确: `onBlur={()=>setError(validateEmail(v))}` `onChange={e=>{setV(e.target.value);if(error)setError(validate(e.target.value))}}`
- 错误: 只有红框（色弱/读屏零感知）→ 正确: `aria-invalid="true" aria-describedby="email-error"` + `<span role="alert">请输入有效的邮箱地址</span>`

边界：密码强度条是 onChange 正例；「密码至少 8 位，当前 5 位」优于「输入有误」；登录失败统一「邮箱或密码不正确」；服务端 422 映射回字段级。源于 [IM-16]/[IM-17]。

### 10. 受控格式化输入不丢光标

路径：整体替换 value 重置光标到末尾——记录 selectionStart → 修正偏移 → rAF 后 setSelectionRange 恢复；或只做 display 层格式化（inputMode+视觉分隔）。
- 错误: `onChange={e=>setVal(format(e.target.value))}`——回改第 3 位光标弹末尾
- 正确: `const pos=el.selectionStart;const{text,cursorOffset}=smartFormat(el.value,pos);setVal(text);requestAnimationFrame(()=>el.setSelectionRange(pos+cursorOffset,pos+cursorOffset))`

边界：粘贴先 strip 再校验；数字避免 type="number"（滚轮改值）用 inputMode="decimal"；iOS 输入 font-size ≥16px 防聚焦缩放。

### 11. 防误操作：撤销优先于确认弹窗

路径：可恢复操作直接执行+undo toast（≥5s，Gmail 模式）→ 不可恢复内联二次确认+destructive 隔离 → 批量预览式确认；NEVER confirm()。
- 错误: `if(confirm('确定删除？'))deleteAll()`——肌肉记忆秒关后不可恢复删除已执行
- 正确: `deleteAll();showUndoToast('已删除 3 项',{onUndo:restore,duration:5000})`；内联二次确认（首点变红「确认删除」，再点执行）

边界：undo toast 需 aria-live 播报；危险按钮无 hover 强化防误触；软删除优于硬删除。源于 [IM-18]。

### 12. 动效编排节奏与预算（stagger/FLIP/scroll-driven）

| 项 | 参数/纪律 |
|---|---|
| stagger 间隔 | 30~80ms；仅首屏/增量项，间隔随 n 收敛 |
| 序列封顶 | 间隔×(n-1)+单项时长 ≤600ms |
| 三层预算 | 入场 ≤450ms / 交互 ≤300ms / 转场 ≤450ms；同时刻单一主角 |
| 节奏关系 | 呼应（同参同拍）/跟随（延迟 60~100ms 表因果）/对比（反参表层级） |
| FLIP | First→Last→Invert→Play，仅 transform 反演+滚动偏移补偿 |
| scroll-driven | `animation-timeline: scroll()/view()` 替代 scroll 监听；不支持则静止 |

源于 [IM-21~23]。来源：[模型经验](corpus/ui-ux-design/interaction-motion/elicited/08-motion-choreography.md)。

### 13. 滚动容器与滚动动线决策

路径：定谁滚动（整页优先；组件内滚动需显式高度）→ 嵌套/弹层 `overscroll-behavior: contain` 收口 → `scrollbar-gutter: stable` 防滚动条占位跳动 → snap 选型（浏览型 mandatory/流式 proximity 或不用）→ 无限滚动配「页脚可达+终止条件+位置恢复」→ 动线选型：消费流用无限滚动；查找/可分享/可统计用分页；折中用手动「加载更多」→ 无限加载用 IntersectionObserver 哨兵（NEVER scroll+高度计算——地址栏收放致误触发）。

边界：视差 ≤2 层且仅 transform，幅度 ≤视口 20%，reduced-motion 静态化；虚拟列表先按首项 id 恢复数据窗口再 scrollTo。源于 [IM-24~26]。来源：[模型经验](corpus/ui-ux-design/interaction-motion/elicited/09-scroll-ux.md)。

### 14. Tooltip/Popover 与轻量提示层纪律

路径：先判层级——关键信息永远在界面本体（label/帮助文本），tooltip 仅悬停/聚焦补充，富交互升级 popover → 触发双通道 hover+focus（纯展示文本不加 tabindex 污染 Tab 链）→ 延迟 in ~500ms / out 100~200ms 且指针可移入，连续目标共享 in 延迟 → 内容 ≤2 行纯文本、禁交互元素 → 定位上方首选、贴边翻转、离触发器 ~8px 不遮挡 → 语义 `aria-describedby`（NEVER `title`——读屏不稳+触屏不可达），Esc/失焦关闭 → 触屏降级：tap 直达目标（tooltip 不触发），帮助图标例外。

边界：tooltip 永不承载唯一信息；错误信息走内联（[IM-17] 非 tooltip）；reduced-motion 直出。源于 [模型经验](corpus/ui-ux-design/interaction-motion/elicited/10-tooltip-popover.md)。

### 15. 键盘快捷键体系

路径：发现性先行——就地 `<kbd>` 徽标 + `?`/`Ctrl+/` 全局面板（可搜索），NEVER 教程强制 → 选键避开浏览器/系统保留（Ctrl/⌘+W/T/N/P/S 等，交付前实测）→ 全局 keydown 双守卫：先判 `e.target`（文本输入内默认不触发），再判 `e.isComposing || e.keyCode===229`（IME 选字期不触发——中文产品高频事故点）→ 无修饰单字母仅限非文本上下文（列表 j/k、命令面板）→ Esc 由最内层组件消费不冒泡 → 显示 ⌘/Ctrl 跟随平台 → 每个快捷键有可见等价入口（NEVER 唯一路径）。

边界：`aria-keyshortcuts` 读屏支持弱仅作补充；保留键清单随浏览器版本演进。源于 [模型经验](corpus/ui-ux-design/interaction-motion/elicited/11-keyboard-shortcuts.md)。

### 16. 动效克制与空间动效（HIG Motion 官方总则，源于 [IM-27]~[IM-31]）

路径：先问目的（无目的不动）→ 高频交互复用系统标准动画不自造 → 动效不承载唯一信息（替代通道 haptics/audio）→ 反馈动效符合手势方向预期且简短精确 → 全部动画可中断 → 空间/沉浸场景执行 visionOS 纪律（边缘动效禁用、fade 重定位、静止参照系、0.2 Hz 振荡线）→ 游戏类锁 30~60 fps 并给画质分级。

- 错误: 列表每项 hover 都播放自定义弹跳动画（高频交互强加动效）；visionOS 场景中对象直接平移跨视野、侧边栏持续呼吸发光（~0.5 Hz 振荡）
- 正确: hover 仅颜色/位移 150ms 微反馈；对象重定位 fade out → 移动 → fade in；必须振荡时低振幅+半透明且避开 ~0.2 Hz 敏感频率 [IM-30] [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/motion.md)

边界：Web 页面仅取「目的性/可中断/替代通道」三条普适纪律；空间数值（0.2 Hz、边缘动效）仅在 XR/visionOS 类项目适用。

## 高频坑点（速查）

Top 3 与实践同源：`transition: all`+一刀切时长（[IM-1]/[IM-2]）；只写 happy path 无失败分支/锁/回滚（[IM-5]/[IM-6]/[IM-7]）；ease-in/ease-out 反用（[IM-3]）。

### 坑点速查表

| 症状 | 根因 | 修复 | 详情 |
|---|---|---|---|
| hover 反馈 >300ms 像设备故障 | 微反馈超感知阈值 | 降至 100~150ms ease-out | IM-2 |
| 大位移 200ms 闪跳、小位移 400ms 烦躁 | 时长与距离不匹配 | <100px→150ms；100~500px→250ms；>500px→300~450ms | IM-2 |
| 汉堡菜单/手风琴展开 30fps | 动画 width/height 触发 layout | 改 transform；确需高度用 FLIP 或 grid 0fr→1fr | IM-4 |
| will-change 后内存暴涨 | will-change:all/长期挂载 | 仅动画期间临时加，结束移除 | E2 |
| cubic-bezier 被静默忽略 | x 超出 [0,1] | x 限制 [0,1]，优先标准曲线 | E2 |
| `transition: transform, opacity 200ms` 后者无时长 | 逗号错切属性组 | 每组独立写全 | E2 |
| animation 结束跳回初始帧 | 缺 fill-mode | 加 forwards；可逆场景用 transition | E6 |
| keyframes 初始值跨浏览器不一致 | 只写 to 未写 from | 显式 from/to | E2 |
| 无限循环装饰动画耗电晕眩 | 未在 reduced-motion 降级 | 降级为淡入或停用 | IM-9 |
| 触屏真机点按零反馈 | hover-only 反馈 | @media (hover:hover) 包裹；主反馈 :active | IM-8 |
| 键盘 Tab 无视觉指示 | 只写 hover/active | :focus-visible 焦点环 | IM-8 |
| 连续操作 toast 洪水 | 无叠加控制 | 同类合并+队列上限；停留 1.5~6s | E1 |
| 反馈出现在页面角落被忽略 | 反馈与操作点错位 | 反馈就近：按钮内/操作原位 | E1 |
| 同一操作不同入口行为不一致 | 微交互缺 Rules 层 | 统一四元组 | E1 |
| 异步失败后动画状态残留 | 循环动画未随生命周期清理 | 请求生命周期绑定动画清理 | E1 |
| 二次访问仍白屏等待 | 有缓存不先渲染 | stale-while-revalidate（SWR 默认） | E4 |
| 首屏 LCP 元素带入场动画致 LCP 骤降 | hero 图/大文案做入场动画 | 首屏关键元素不做入场动画 | E2 |
| 首屏一片红 | mount 即跑校验缺 touched | touched/dirty 后才显示错误 | E5 |
| 改对了红框不清除 | 校验只在 blur 触发一次 | error 态 onChange 复查；消错 150ms 过渡 | IM-16 |
| 提交一次炸出 10 条错误 | 全量错误无导航 | 聚焦/滚动第一个错误+内联错误 | IM-16 |
| 卡号编辑光标跳末尾 | 受控整体替换 value | selectionStart 记录+偏移修正（实践 10） | E5 |
| textarea 回车误触提交 | button 缺 type 默认 submit | 非提交按钮写 type="button" | E5 |
| 错误文字顶开下方布局 | 无预留空间 | 预留 error slot 高度或 grid 布局 | E5 |
| iOS 输入聚焦页面放大 | 输入框字体 <16px | font-size ≥16px（业界常识，待锚定） | E5 |
| 服务端 422 只 toast 一句 | catch 丢字段映射 | errors.email[0] 映射回字段级 | E5 |
| 提交失败表单数据全清空 | 无论成败都 reset() | 仅成功后清理+草稿自动保存 | IM-20 |
| 列表入场动画全列表重播 | 内联组件/index key 致 remount | 模块级组件+稳定 key | E6 |
| drawer 打开背景仍可滚 | 缺滚动锁 | body overflow:hidden+overscroll-behavior:contain | IM-19 |
| 转场期间连点误触新旧页 | 未屏蔽点击穿透 | pointer-events:none/覆盖层+锁导航栈 | IM-12 |
| modal 有入场无退场 | 只写 enter 不写 exit | 退场 150ms ease-in 后再移除 | E2 |
| keyframes 与 transition 同属性打架 | transform 上双层动画 | 拆分属性或统一一层负责 | E6 |
| z-index 递增竞赛互相穿透 | 无分层 token | --z-toast/--z-modal 分层变量 | E6 |
| toast 停留 >6s 打扰/<1.5s 不可读 | 时长阈值越界 | 常规 3~4s，可交互 ≥5s | E1 |
| stagger 20 项拖 1.5s+ 与用户滚动打架 | 间隔×(n-1) 无封顶 | 总量 ≤600ms：间隔收敛/仅增量项 | IM-21 |
| 弹层滚到底带走背景页 | 嵌套滚动链未收口 | overscroll-behavior: contain | IM-24 |
| 返回列表回顶位置丢失 | 位置未存或仅存 scrollTop | scrollRestoration manual+自存；虚拟列表锚数据 | IM-25 |
| 长文档滚半屏被硬吸 | mandatory 误用于流式内容 | mandatory 仅浏览型；流式 proximity | IM-26 |

### AI 生成自检清单（按频率排序）

1. 占位参数进生产（`transition: all .3s ease`）→ [IM-1]/[IM-2]
2. ease-in 字面义当「淡入」用于入场 → [IM-3]
3. demo 思维缺错误分支 → [IM-5~7]
4. JS/CSS 时长不同步 → [IM-10]
5. 炫技动画堆砌 → [IM-19]
6. prefers-reduced-motion 盲区 → [IM-9]
7. hover-only 反馈给触屏 → [IM-8]
8. transitionend 无兜底卡死 → [IM-10]
9. 内联组件/index key 致 remount 重播 → 模块级稳定身份
10. 动画 layout 属性 → [IM-4]
11. 魔法数与 CSS 变量脱钩 → getComputedStyle/WAAPI 统一
12. z-index 递增竞赛 → 分层 token

## 参数速查表（API 速查）

### 反馈阈值（Nielsen 三阈值+补充）

| 阈值 | 行为要求 |
|---|---|
| <100ms | 即时响应 |
| 100ms~1s | 需要反馈（局部 spinner） |
| >1s | 需要进度指示 |
| ~10s | 放弃线：必须真实进度/预估/可离开承诺/取消出口 |
| 400ms（Doherty） | 人机「对话」心流（[模型经验]，未锚定） |
| INP 200ms | Core Web Vitals 交互响应阈值（2024 替代 FID，置信中） |

### 动效时长分层

| 交互层级 | 时长 | 缓动 |
|---|---|---|
| 微反馈（hover/press/color） | 100~150ms | ease-out |
| toggle/开关过渡 | ≤200ms（>200ms 显迟钝） | ease-out |
| 常规 UI 转场（modal/dropdown/tab） | 200~300ms | 入场 ease-out / 退出 ease-in |
| 页面级/大位移转场 | 300~450ms（体感上限 500ms） | 标准曲线 |
| 骨架 shimmer | 1.2~1.5s 循环 | ease-in-out |
| toast 停留 | 1.5~6s（<1.5s 不可读，>6s 打扰） | — |
| 撤销窗口 | ≥5s（Gmail 惯例） | — |

### 缓动曲线常量（Material）

| 名称 | cubic-bezier | 用途 |
|---|---|---|
| standard | cubic-bezier(0.4, 0, 0.2, 1) | 常规状态变化 |
| decelerate（入场） | cubic-bezier(0, 0, 0.2, 1) | 元素入屏 |
| accelerate（退出） | cubic-bezier(0.4, 0, 1, 1) | 元素出屏 |
| emphasized | cubic-bezier(0.2, 0, 0, 1) | 大位移/容器转场（置信中） |

### CSS transition / animation 速查

| 语法/属性 | 易错点 |
|---|---|
| `transition: <property> <duration> <easing> <delay>` | 简写首个时间值是 duration；逗号错位组后者无时长 |
| `transition: all` | 禁用（[IM-1]） |
| `animation: <name> <duration> <easing> <delay> <iteration> <direction> <fill-mode>` | duration 在 delay 前；结束保持需 forwards |
| `cubic-bezier(x1, y1, x2, y2)` | x ∈ [0,1]（y 可越界）；越界被静默忽略 |
| `will-change` | 动画期间临时使用，勿长期挂载/全列表添加 |
| 动画友好属性 | transform/opacity（仅 composite）；NEVER layout 属性（[IM-4]） |
| `@starting-style` | 入场 transition 起点（2023+，基线待验证） |
| `transition-behavior: allow-discrete` | display 等离散属性过渡（待验证） |
| `@media (hover: hover)` | 触屏降级必备包裹（[IM-8]） |
| `@media (prefers-reduced-motion: reduce)` | 动效强制降级（[IM-9]） |
| `:focus-visible` | 焦点环优于 :focus（避免鼠标点击出环） |

### 转场决策表（语义→形式→时长）

| 语义 | 形式 | 时长 |
|---|---|---|
| 深入下级（push） | 侧推+旧页视差后退 30% | 300~400ms |
| 返回（pop） | 原路反向 | 同 push |
| 同级切换（tab/segment） | 交叉淡入/小位移 | ≤200ms（推荐 150ms） |
| 模态/临时任务 | 底部升起（移动）/中心 scale+fade（桌面） | 250ms |
| 确认打断 | 中心 scale+fade；遮罩 fade 150ms、内容稍慢 | 200ms |
| 覆盖层（sheet/drawer） | 从边缘滑入 ease-out（iOS sheet 用 spring） | 300ms |

### 表单校验时机决策表

| 时机 | 适用 | 反例 |
|---|---|---|
| 输入中（onChange） | 评价类（密码强度/用户名可用性） | 邮箱格式校验 |
| 失焦（onBlur） | 主校验时机 | — |
| error 态 onChange | 已报错字段复查，改对即消错 | 初次输入就校验 |
| 提交时（onSubmit） | 全量+聚焦第一个错误字段 | — |
| 提交后字段级 | 服务端错误映射回字段 | — |

### HIG Motion 数值速查（R34 实抓 [官方文档](https://developer.apple.com/design/Human-Interface-Guidelines/motion.md)）

| 项 | 数值/规则 |
|---|---|
| 目的性 | 有目的地添加动效，不为动而动；动效可选，不作唯一信息通道（haptics/audio 替代）[IM-27] |
| 反馈动效 | 真实、符合手势预期；简短精确；高频交互一般不加自定义动效 [IM-28] |
| 可中断 | 不迫使用户等动画播完（尤其重复动画）[IM-29] |
| 游戏/实时图形 | 30~60 fps 流畅标准；按设备提供默认画质+可自定义 [IM-31] |
| visionOS 振荡线 | 持续振荡敏感频率约 0.2 Hz；必须振荡时低振幅+半透明 [IM-30] |
| visionOS 重定位 | fade out → 移动 → fade in；避免视野边缘动效；避免旋转虚拟世界；静止参照系 [IM-30] |
| Reduce Motion | 减少自动/重复动画；弹簧收紧减弹跳；动画直接跟随手势；避免 z 轴深度变化；fades 替代位移；避免出入模糊 [IM-9] |
| watchOS | 布局与外观动画自动内置 easing，不可关闭或自定义（WKInterfaceImage 图像序列除外） |
| SF Symbols | 5+ 支持符号动画（animated symbols） |

## 版本注意

- **文档锚定升级（R34）**：HIG 深层主题页现已可抓取——motion.md（本域）与 accessibility.md（Reduce Motion 细则，SD 域语料跨域引用）均已实抓锚定（见来源索引）；R33「HIG 深层页未抓取」记载过时。除已锚定条目外，本节其余多为 [模型经验]，用前查 MDN/caniuse。
- **View Transitions API**：SPA 用 `document.startViewTransition(callback)`；伪元素 `::view-transition-group/old/new`（以 MDN 为准）；MPA 支持矩阵待验证。
- **prefers-reduced-motion**：各平台均有系统级开关；降级为 [IM-9] 强制项（HIG Reduce Motion 做法已锚定）。
- **:focus-visible**：2022 起 baseline（待验证）；iOS Safari `:active` 需绑 touchstart 旧问题待验证。
- **CSS 新特性**：`@starting-style`、`transition-behavior: allow-discrete`、`animation-timeline: scroll()/view()`、`animation-range` 均 2023+ 基线待验证；`<dialog>` 转场依赖 display 过渡。
- **React**：18+ unmounted setState 改 no-op（待验证）；useTransition/useDeferredValue 提供 delayed spinner 心智；React 19 View Transitions 名待验证。
- **transition 事件族**：transitionrun/start/cancel 存在；transitionend 中途取消不触发。
- **Core Web Vitals**：INP 2024 替代 FID（200ms，置信中）；CLS 受骨架屏影响。

## 与其他子领域的集成要点

- **usability-accessibility**：[IM-9] 衔接 WCAG 2.2.2；[IM-17] 衔接 3.3.1/3.3.3；aria-live 与 undo toast 播报在该域定案。
- **style-design-system**：五态 token 化；时长/缓动/z-index CSS 变量单一来源支撑 [IM-10]。
- **visual-perception**：阈值心理学依据（100ms/Doherty 400ms/感知速度）在感知域展开。
- **横切**：[IM-5]/[IM-7]/[IM-15] 为 [GLOBAL] 候选；自检清单汇入 ai-mistakes.md；跨域坑点汇入 gotchas.md。

## 来源索引

**官方文档（白名单）**：
- https://developer.apple.com/design/Human-Interface-Guidelines/motion.md — HIG Motion 主题页（R34 实抓）：动效总则/目的性/可中断/30-60fps/visionOS 0.2Hz 与 fade 重定位/Reduce Motion（[IM-9]/[IM-27~31] 锚定源）
- https://developer.apple.com/design/Human-Interface-Guidelines/accessibility.md — HIG Accessibility 主题页（R34 实抓，SD 域语料跨域引用）：Reduce Motion 具体做法（[IM-9] 锚定源）
- https://developer.apple.com/design/human-interface-guidelines.md — HIG 根 .md 索引：Materials（深度/分层/层次感）；Gestures/Inputs（输入方式是反馈设计前提）；Patterns；Components（组件交互状态定制）
- https://developer.apple.com/design/human-interface-guidelines/ — HIG 根页（JS 渲染，锚点同上）

**模型经验（corpus 路径，缩写 E1~E11 对应 elicited/01~11）**：
- E1 微交互四元组、状态反馈、乐观更新回滚
- E2 时长/缓动/距离模型、动画性能、reduced-motion
- E3 转场层级、导航方向语义、共享元素/FLIP
- E4 三阈值、骨架屏、感知性能、竞态
- E5 校验时机、错误文案、防误操作与撤销
- E6 AI 生成典型错误（防御清单核心）
- E7 法则化萃取（IM-1~IM-20 基础）
- E8 动效编排：stagger 封顶、FLIP、View Transitions 纪律、三层预算、节奏关系、scroll-driven
- E9 滚动体验：滚动容器纪律/滚动链、snap、视差克制、无限滚动陷阱、位置恢复、动线选型
- E10 tooltip/popover：层级判据、双通道触发、延迟、aria-describedby、触屏降级
- E11 键盘快捷键：发现性/保留键/IME isComposing 守卫/平台适配

**文档锚点**：corpus/ui-ux-design/interaction-motion/docs/apple-hig-index.md、_fetch_log.md

**未经文档验证声明**：HIG 深层页未抓取（降级）；除根索引要点外，全部参数类知识均为模型经验；「待验证」项用前查 MDN/caniuse/NN-g。

**标注约定**：[官方文档] 仅用于白名单 URL 根索引要点；[模型经验] 指向 corpus 路径；推断性内容不得进入法则/最佳实践/坑点/参数速查/版本区块（本文件无 [推断] 条目）。

## 冲突消解记录

1. **参数类知识无文档对照（R33）**：仅根索引可锚定 → 保留模型值+[模型经验] 标注，用前查 MDN/caniuse；一致性锚定：① 输入方式分支反馈 ↔ HIG Gestures/Inputs → [IM-8]；② 转场层级/方向对称 ↔ HIG Materials → [IM-11]；③ 组件状态梯度 ↔ HIG Components → 五态梯度（实践 1）。
2. **HIG Motion 深层页可抓性（R34 更正）**：R33 记载「HIG 深层页未抓取」→ R34 实抓 motion.md 成功（`Human-Interface-Guidelines/motion.md` 模式，见 _fetch_log_r34-hig.md）→ [IM-27]~[IM-31] 及「HIG Motion 数值速查」升格为 [官方文档] 锚定；其余参数类知识维持 [模型经验]。
3. **Reduce Motion 细则归属**：模型原认知将 Reduce Motion 仅当 CSS media query 降级开关 → HIG 给出平台级具体做法（弹簧收紧/跟随手势/fades 替代位移/避免 z 轴深度变化/避免出入模糊）→ [IM-9] 扩充双锚定（motion.md + accessibility.md）；accessibility.md 语料物理存于 style-design-system 域（跨域引用，见 _fetch_log_r34-hig.md）。
4. **动效可选 vs 反馈必需**：HIG「高频 UI 交互一般不加动效」与 [IM-8]「可交互元素必须具备反馈」的表面张力 → 消解：反馈必须有（颜色/状态变化即反馈），自定义动效克制（系统标准动画承担微反馈）；[IM-27] 与 [IM-8] 并行不悖。
5. **微交互时长区间与 [LAW-15] 的粒度分层（R10 语义层评审登记）**：[LAW-15]「微交互 150~300ms」为常规区间包络（全局宪法口径），[IM-2]「微反馈 100~150ms」为最快档特例（hover/press/color 级反馈可低于常规下限），ai-mistakes「微交互 150~200ms」为常规工作点推荐——三者非事实冲突而是分层粒度：微反馈 < 常规微交互 < 转场。裁决规则：最快档微反馈取 [IM-2]；常规微交互与时长预算取 [LAW-15]；两档同守 NEVER >500ms 上限与 prefers-reduced-motion 降级。
