---
type: cross-cutting
name: gotchas
domain: ui-ux-design
skill_name: ui-ux-design-expert
version: 1
updated: 2026-11-17
merged_at: 2026-11-16
subdomains: [visual-perception, layout-composition, color-system, typography, style-design-system, interaction-motion, usability-accessibility]
counts: 65
---

# ui-ux-design 全领域坑点速查（gotchas）

跨 7 个子领域蒸馏的高频坑点清单，按「严重度 × 出现频率」筛选。每条一行：症状 → 根因 → 规避 → 法则引用。

## visual-perception 坑点

[G-1] placeholder 充当 label — 症状： 输入后提示消失、自动填充后无法核对字段、读屏关联缺失 | 根因： 以占位符替代持久标签，可见性随输入归零 | 规避： 每字段配 `<label for>`；placeholder 仅作格式示例 | 参考： VP-6；UA-7
[G-2] 危险操作为同屏最醒目 — 症状： 红实心"取消/删除"成为唯一强调按钮，用户被引导误点 | 根因： 强调色被无条件消费，Von Restorff 效应反向利用 | 规避： 危险操作降视觉档（描边/文本）并与确认键拉开距离，唯一实心留给主操作 | 参考： VP-4；VP-3
[G-3] 统一间距病 — 症状： 全页所有间距同为 16px，分组不可辨、扫读成本陡增 | 根因： 间距未编码亲疏关系 | 规避： 组间 ≥2× 组内，间距取 4/8 系刻度（4/8/16/32/64） | 参考： VP-1；LC-2
[G-4] 等权按钮无唯一焦点 — 症状： 一屏多个实心按钮，用户不知下一步点哪 | 根因： 视觉重量档位未区分操作等级 | 规避： 每视图唯一实心主 CTA，其余降描边/文本档 | 参考： VP-2；VP-3；LC-4
[G-5] hover-only 功能 — 症状： 触屏上操作按钮只在悬停时浮现，功能不可达＝不存在 | 根因： 关键操作依赖鼠标 hover | 规避： 关键操作常驻可见；hover 用 `@media (hover:hover)` 包裹并提供触屏等价路径 | 参考： VP-11；SD-11
[G-6] 固定高度容动态文本 — 症状： 真实长文案溢出裁切或撑破卡片 | 根因： 容器高度按 demo 短文本定值 | 规避： min-height + 截断策略（line-clamp/ellipsis + min-w-0） | 参考： VP-8
[G-7] 卡片汤 — 症状： 每个区块都套边框容器、三层嵌套，视觉噪音淹没内容 | 根因： 分组手段边框优先，接近性能力退化 | 规避： 分组顺序 间距 > 背景/分隔线 > 边框；嵌套容器 ≤2 层 | 参考： VP-19
[G-60] 对齐轴线打架 — 症状： 同容器左/中/右混用，卡片按钮随内容长度漂移 | 根因： 元素各自选对齐，无共享轴线 | 规避： 每元素至少共享一条轴线；同容器对齐 ≤2 种；卡片操作区 margin-top:auto 锚底 | 参考： VP-25；VP-28；LAW-26

## layout-composition 坑点

[G-8] 间距刻度外任意值 — 症状： 13/15/18px 混入 8pt 体系，垂直节奏断裂 | 根因： 间距随手微调无系统可依 | 规避： 全部间距取 4 的倍数刻度（4/8/12/16/24/32/48/64） | 参考： LC-1；SD-5
[G-9] 组间组内间距无层级 — 症状： 标签被读成上一组的尾巴，模块边界消失 | 根因： 关系未由间距编码 | 规避： 组间:控件间:控件内 ≈ 32:16:8 递减；区块间距 ≥2× 区块内 padding | 参考： LC-2；LC-3
[G-10] 正文行长失控 — 症状： 全宽容器一行 100+ 字符，阅读丢行 | 根因： 正文容器无 max-width | 规避： 西文 45~75ch（约 65ch），中文 25~40 字/行 | 参考： LC-8；TY-6
[G-11] >3 行正文居中 — 症状： 长段落居中导致回行定位困难 | 根因： 标题/短文案的居中惯例被误用于正文 | 规避： 超过 3 行的正文一律左对齐（RTL 相反） | 参考： LC-7
[G-12] grid/flex 子项 min-width:0 缺失 — 症状： 长单词/URL 把轨道撑爆，相邻内容被挤压 | 根因： 子项默认 min-width:auto 不可收缩 | 规避： min-width:0 + overflow-wrap:break-word | 参考： LC-12
[G-13] 替换型内容无溢出防护 — 症状： 图片/表格/iframe 撑出横向滚动条 | 根因： 未设 max-width 或滚动容器 | 规避： img/video/table/pre/iframe 一律 max-width:100%，表格包滚动容器 | 参考： LC-11
[G-14] 媒体无尺寸占位 — 症状： 图片加载后布局跳动（CLS），用户点空按钮 | 根因： 无固有尺寸属性或宽高比占位 | 规避： width/height 属性或 CSS aspect-ratio 占位 | 参考： LC-13
[G-15] 全屏区块固定高度 — 症状： 小视口裁掉 CTA、移动端地址栏遮挡底部 | 根因： height:100vh 定值 | 规避： min-height + 内容驱动；移动端全屏用 svh/dvh | 参考： LC-14

## color-system 坑点

[G-16] 组件硬编码色值 — 症状： 换肤/深色模式/品牌迭代全站失效，需逐处改值 | 根因： hex 绕过 token 直接写进组件样式 | 规避： 色值只出现在 token 定义处，组件一律引用语义 token | 参考： CS-1
[G-17] 灰字正文对比不足 — 症状： #999 on 白底 ≈2.85:1 不可读，弱光/低视力用户崩溃 | 根因： muted 默认取 gray-400/500 档，且只对纯白验证 | 规避： 白底最浅合格灰 #767676（≈4.5:1）；灰底/彩底按真实背景重算 | 参考： CS-2；CS-17；UA-4
[G-18] 深色模式 naive invert — 症状： filter:invert 图片负片、品牌色变浊、阴影失效层级坍塌 | 根因： 全局反转冒充语义重映射 | 规避： 语义 token 整体重映射；表面越浮起越亮；品牌色提亮降饱和（#2563EB→#60A5FA） | 参考： CS-11；CS-13；CS-14
[G-19] 黄底白字 — 症状： #FACC15 上白字 ≈1.5:1 近乎隐形 | 根因： 高亮度底配浅色文字 | 规避： 高亮度底必配深色文字；渐变背景文字按最差区域校验 | 参考： CS-20
[G-20] lighten/darken 批量生成色阶 — 症状： 黄变土橄榄、蓝过电霓虹、档间感知断裂 | 根因： HSL 亮度等比缩放非线性于感知 | 规避： sRGB 混色或 OKLCH/HCT 感知空间，暗化允许 hue 微移 | 参考： CS-6
[G-21] 品牌色大面积滥用 — 症状： 品牌色渐变铺满 hero/卡片，强调失效、页面"吵" | 根因： 无面积配比约束 | 规避： 60-30-10（60% 中性底、30% 次级、10% 强调）；品牌色出场即有意义 | 参考： CS-7；SD-16
[G-22] 半透明文本色叠图 — 症状： rgba(255,255,255,.6) 文字随背景漂移，对比不可控 | 根因： 透明色与背景复合结果未校验 | 规避： 叠 ≥0.4 不透明 scrim 或改实色 tint | 参考： CS-15
[G-23] token 跳线直引 primitive — 症状： 组件写 var(--blue-500)，主题切换语义漂移 | 根因： 跳过语义层直引原始色阶 | 规避： primitive→semantic→component 分层，组件只消费语义层 | 参考： CS-4；SD-4
[G-61] 图表配色彩虹与序列色相化 — 症状： 分类图 9+ 色相相邻不可辨；趋势/热力图彩虹渐变读序混乱 | 根因： categorical/sequential 用反，色相当数值通道 | 规避： 分类 ≤8 类+「其他」；序列用明度单调色带（禁彩虹）；过色盲+灰度验证 | 参考： CS-21；CS-22；CS-24

## typography 坑点

[G-24] @font-face 忘 font-display — 症状： 弱网文字隐形数秒（FOIT），Lighthouse 报警、LCP 恶化 | 根因： 未声明加载期回退行为 | 规避： 正文 font-display:swap，非关键字体 optional | 参考： TY-1
[G-25] CJK 字体整包加载 — 症状： 中文站首屏下载数 MB 字体，移动端首屏 >10s | 根因： 中文字体未子集化 | 规避： 子集化或 unicode-range 分包后上线 | 参考： TY-14
[G-26] 中文正 letter-spacing — 症状： 方块字节奏撕裂、标点后双空隙 | 根因： 照搬西文字距惯例 | 规避： 中文 letter-spacing 仅允许 0 或负微调 | 参考： TY-8
[G-27] 字体栈顺序反 + 无通用族结尾 — 症状： 数字与拉丁字形发闷；指定字体全缺时全站回落衬线体 | 根因： 中文字体写在前、栈尾无 fallback | 规避： 西文在前中文在后，栈尾必接 sans-serif/serif/monospace | 参考： TY-2；TY-3
[G-28] line-height 单位陷阱 — 症状： 子元素行距过紧或过松（px 行高配 rem 字号是重灾区） | 根因： px/em/% 行高作为绝对值被继承 | 规避： body 用无单位 1.5；≥24px 标题显式收紧 1.05~1.25 | 参考： TY-4；TY-5
[G-29] word-break:break-all 滥用 — 症状： 英文单词/数字串被拦腰斩断（"2026111\n6"） | 根因： 把 break-all 当中文换行默认 | 规避： line-break:strict + overflow-wrap:break-word | 参考： TY-9
[G-30] line-height 撑控件高度 — 症状： 按钮/标签文本换行或加图标后错位溢出 | 根因： 用行高计算代替盒模型高度 | 规避： height/min-height + flex 垂直居中 | 参考： TY-10
[G-31] tabular-nums 缺失 — 症状： 计时器/价格/表格数值列逐位抖动、列宽跳动 | 根因： 比例宽数字为默认 | 规避： 变化数字启用 font-variant-numeric:tabular-nums | 参考： TY-7
[G-62] 62.5% rem hack 与流体字号用于正文 — 症状： 62.5% 破坏第三方嵌入与无障碍字号缩放；clamp 流体正文窄屏缩至不可读 | 根因： 换算 hack 冒充字号策略，流体缩放不限标题 | 规避： 禁 62.5%；clamp 仅限 ≥24px 标题，正文离散档位 | 参考： TY-22；TY-23
[G-63] 可变字体轴不设区间 — 症状： wght 100~900 全开被误用极端值；字体切换首行跳动 | 根因： @font-face 未声明轴区间与度量匹配 | 规避： 按轴声明区间；回退配 size-adjust/ascent-override | 参考： TY-24；TY-25

## style-design-system 坑点

[G-32] AI 蓝紫渐变品牌脸 — 症状： #667eea→#764ba2 渐变 hero/按钮，千篇一律模板感 | 根因： 无品牌输入时以训练分布默认值冒充设计结论 | 规避： 无品牌输入用中性克制方案并显式声明"未注入品牌" | 参考： SD-19
[G-33] token 命名按外观 — 症状： --color-blue 实存紫色，换品牌时全局替换爆炸 | 根因： 命名描述值而非功能 | 规避： 按功能命名（--color-action 合格，--color-blue 不合格） | 参考： SD-4
[G-34] 组件状态集不完整 — 症状： 只交付 default 态，键盘/触屏/异常路径不可用 | 根因： 状态完整性清单未核验即交付 | 规避： 五态齐备（default/hover/focus-visible/active/disabled），表单加 error，异步加 loading | 参考： SD-1
[G-35] 禁用态仅 opacity — 症状： 灰按钮仍可点击发起请求；与次级按钮混淆 | 根因： 只有视觉禁用无语义拦截 | 规避： disabled 属性/aria-disabled + JS 拦截 + 实色 tint + 禁用原因提示 | 参考： SD-13
[G-36] hover/选中引发布局位移 — 症状： hover 加粗/换边框导致文字重排、相邻元素跳动 | 根因： 状态变化改变盒尺寸 | 规避： 透明边框占位、不变字重，盒尺寸保持中性 | 参考： SD-14
[G-37] backdrop-filter 无降级 — 症状： 玻璃拟态在不支持浏览器退化为脏灰、文字不可读、低端机掉帧 | 根因： 未写 @supports 回退 | 规避： 高不透明度实色降级；同页玻璃元素 ≤2 类大面积 | 参考： SD-10
[G-38] emoji 与 SVG 图标混用 — 症状： 跨平台渲染不一、粗细不匀的拼贴感 | 根因： 图标来源不唯一 | 规避： 单一图标库统一 stroke 宽度与 linecap；emoji 不作 UI 图标 | 参考： SD-17

## interaction-motion 坑点

[G-39] transition: all + 一刀切时长 — 症状： 改一个 class 全属性 .3s 连带动画、布局波浪；hover 800ms 迟钝 | 根因： 模板默认值 `.3s ease` 直接进生产 | 规避： 显式属性列表；微反馈 100~150ms、常规 200~300ms、大转场 ≤450ms | 参考： IM-1；IM-2
[G-40] 入场 ease-in / 退出 ease-out 反用 — 症状： 下拉打开先僵后跳，关闭时赖着不走 | 根因： "ease-in＝渐入"字面义与函数义相反 | 规避： 入场 ease-out（快出慢停），退场 ease-in（快走） | 参考： IM-3
[G-41] 动画 layout 属性 — 症状： 汉堡菜单展开 30fps、滚动抖动 | 根因： top/left/width/height 触发重排重绘全管线 | 规避： 只动 transform/opacity；确需 height 用 FLIP 或 grid 0fr→1fr | 参考： IM-4
[G-42] 异步只写 happy path — 症状： 请求失败白屏/无限转圈，用户被锁死无反馈 | 根因： loading/success/error 三态不全，catch 空实现 | 规避： 三态齐全 + 重试出口；数据视图四态（空/加载/错误/成功） | 参考： IM-5；LC-20
[G-43] 乐观更新无回滚 + 提交无 pending 锁 — 症状： 点赞失败仍亮着；连点产生重复订单/重复付款 | 根因： 只做"乐观"没做确认/回滚半边；pending 期未锁定 | 规避： 失败还原 prev 快照 + toast；发起请求同步代码内立即 disabled；支付类禁乐观更新 | 参考： IM-6；IM-7
[G-44] prefers-reduced-motion 缺失 — 症状： 前庭障碍用户晕眩弃用 | 根因： 无障碍降级不在默认输出集 | 规避： reduce 下动画时长归零/取消位移，保留 opacity 淡入 | 参考： IM-9；UA-13
[G-45] JS/CSS 时长不同步 + transitionend 无兜底 — 症状： 动画被提前卸载截断；快速连点后组件卡在半开态 | 根因： timeout 与 transition-duration 两处各写各的；事件被打断时不派发 | 规避： 单一来源（读 CSS 变量）；transitionend + timeout 双保险 | 参考： IM-10
[G-46] 骨架屏不匹配真实内容 — 症状： 加载完成布局跳动 200px 致误点；快网下骨架闪现成噪声 | 根因： 骨架随手画未镜像组件尺寸；无最小显示延迟 | 规避： 骨架镜像结构+尺寸（含 aspect-ratio），延迟 200~300ms 再显示 | 参考： IM-13
[G-47] 竞态请求无取消 — 症状： 搜索慢响应旧结果覆盖新结果（结果回跳） | 根因： 响应到达序 ≠ 发出序，无 AbortController | 规避： useEffect cleanup 中 abort 过期请求，或请求标识比对 | 参考： IM-15
[G-48] onChange 校验轰炸 — 症状： 输入首字符即弹"邮箱格式错误"，边打边骂红 | 根因： 格式规则在输入中间态执行 | 规避： blur 首校验，error 态下 onChange 复查；提交时全量校验 + 聚焦第一个错误 | 参考： IM-16
[G-64] 嵌套滚动不收口 + 返回滚动位置丢 — 症状： 弹窗内滚动联动页面（串轴）；返回列表回顶部 | 根因： 弹层无 overscroll-behavior:contain；路由无滚动位置记忆 | 规避： 弹层滚动容器收口；列表缓存滚动位置返回恢复 | 参考： IM-24；IM-25
[G-65] 入场 stagger 不封顶 — 症状： 8 元素逐个入场拖 3s+，整体感瓦解 | 根因： 无编排，stagger 无上限 | 规避： stagger ≤50ms/项、组总时长 ≤600ms；大列表只编排骨架 | 参考： IM-21；IM-22；VP-34

## usability-accessibility 坑点

[G-49] outline:none 无替代焦点 — 症状： 键盘用户 Tab 导航"失明"，随机误触 | 根因： reset 移除焦点环且不补替代 | 规避： :focus-visible 2px outline + 2px offset，与背景对比 ≥3:1 | 参考： UA-1；SD-2
[G-50] div/span + onclick 代替 button — 症状： 键盘与读屏用户完全无法操作 | 根因： 按视觉形态选元素而非语义 | 规避： 原生 button/a/input；必须自定义时补 role + tabindex + Enter/Space 键盘事件 | 参考： UA-2
[G-51] 颜色为唯一信息载体 — 症状： 红绿色盲（男 ~8%）分不清成败状态、图表系列 | 根因： 语义只有色相一个通道 | 规避： 双通道编码（✓/✕、线型、文字），过 deuteranopia 模拟验证 | 参考： UA-3；CS-3；CS-10
[G-52] 触控目标 <24×24 — 症状： 移动端误触率高、老年/手抖用户点不中 | 根因： 命中区跟随视觉尺寸 | 规避： ≥24×24 CSS px（AA 底线），移动端 ≥44×44，padding/伪元素扩展热区 | 参考： UA-5；VP-5；LC-15
[G-53] 模态焦点四件套缺失 — 症状： Tab 穿透到遮罩下、ESC 无效、关闭后焦点丢到页首 | 根因： 只写视觉层不做焦点管理 | 规避： 打开焦点移入/焦点陷阱/ESC 关/关闭焦点返还 + role="dialog" aria-modal="true" | 参考： UA-11
[G-54] 动态更新无 aria-live — 症状： 购物车数量、错误 toast 读屏用户零感知 | 根因： DOM 变更默认对读屏静默 | 规避： 状态变化区域 aria-live="polite"，错误播报用 role="alert" | 参考： UA-12
[G-55] 正 tabindex 乱序 — 症状： Tab 顺序跳跃混乱，维护灾难 | 根因： 正值硬编码焦点顺序 | 规避： 只用 0 与 -1，顺序交给 DOM/感知顺序 | 参考： UA-14
[G-56] icon-only 按钮无 accessible name — 症状： 读屏只念"按钮"；语音用户说"点搜索"无响应 | 根因： 缺 aria-label 或可见标签文本 | 规避： aria-label 补全，且名称包含可见标签文本 | 参考： UA-15
[G-57] 错误信息三要素缺失 — 症状： "操作失败，请重试"——不知道哪错、为什么、怎么改 | 根因： 错误文案只报事实不给诊断与出路 | 规避： 什么错（具体）+ 为什么（可理解）+ 怎么办（行动）；定位到字段并聚焦第一个错误 | 参考： UA-8；UA-10
[G-58] 提交失败清空表单 — 症状： 网络错误一次丢 20 个字段，用户直接流失 | 根因： 失败分支也执行 reset()/跳转 | 规避： 仅成功后清理；失败保留数据 + localStorage 草稿自动保存 | 参考： UA-16；IM-20
[G-59] alert/confirm 原生弹窗 + 模糊确认文案 — 症状： confirm 被肌肉记忆秒关后执行不可恢复删除；"确定吗？+是/否"训练用户无脑确认 | 根因： 原生弹窗无上下文、无预览、无撤销 | 规避： 可恢复操作用 undo toast（≥5s）；不可恢复用内联二次确认 + 后果写入文案 + 动词按钮，危险键不设默认焦点 | 参考： UA-18；UA-9；IM-18

## 来源索引

| 来源 | 类型 | 路径/说明 |
|---|---|---|
| 7 子领域蒸馏 kb 的坑点小节 | [模型经验] | output/ui-ux-design-expert/kb/{visual-perception,layout-composition,color-system,typography,style-design-system,interaction-motion,usability-accessibility}.md |
| 7 子领域萃取语料 | [模型经验] | corpus/ui-ux-design/<sub>/elicited/*.md（阶段 1 产物） |
| R19 深化轮增补（G-60~G-65） | [模型经验] | corpus/ui-ux-design/<VP/CS/TY/IM>/elicited/08-*、09-*（六份深化语料，全名见各 kb 来源索引） |
| WCAG 2.2 条款号（G-49/50/51/52/53 引用） | [官方文档] | https://www.w3.org/WAI/standards-guidelines/wcag/ 、https://www.w3.org/TR/WCAG22/ |
| WebAIM WCAG Checklist（G-17 对比度阈值） | [官方文档] | https://webaim.org/standards/wcag/checklist |

验证声明：G-1~G-65（G-60~G-65 为 R19 深化轮）均于 2026-11-16 从上述来源蒸馏；未单独验证条目视为 [模型经验]，引用的 WCAG 条款号已经白名单文档锚定。

## 对账记录

| 轮次 | 结果 | 日期 |
|---|---|---|
| R19（深化轮，回溯补记） | 新增 G-60~G-65——原轮漏横切对账登记，本回溯补记 | 2026-11-17 |
| R6（项目评审第六轮） | 补账：确认 G-01~G-65 基线与 SKILL.md Top 坑点引用一致；本轮评审无新增坑点候选 | 2026-11-17 |
