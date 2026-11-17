# Review Passes — 可独立调用的审查过程

> 4 个 pass 可在任何时间点对**任意 HTML 文件**运行，不依赖生产流。
> 单 agent 顺序执行，不引入子 agent（遵循 SkillForge Core Constraint #5：扩 Reference，不扩 Agent）。
> 生产流的 [CP4 Pre-flight](./mode-2-prototype.md#pre-flight-check-cp4-sub-checklist--run-before-declaring-done) 是"出厂前自检"，这里是"独立质检站"——可审别人写的 HTML、可审上线前的产物、可审迭代后的回归。

---

## 何时用哪个 pass

| 触发词 | pass |
|--------|------|
| 无障碍 / accessibility / a11y / WCAG / 键盘导航 / 对比度 / 焦点环 | **Pass 1: Accessibility** |
| AI 味 / slop / 模板感 / 太像 AI 生成 / 不够特别 | **Pass 2: AI-Slop** |
| 层级不清 / hierarchy / 节奏乱 / rhythm / 排版乱 / 信息主次模糊 | **Pass 3: Hierarchy & Rhythm** |
| 交互状态不全 / interaction states / hover 没反应 / 按钮状态缺失 | **Pass 4: Interaction States** |
| 全面审查 / polish / 上线前检查 / 帮我把关 | **全量审查**（4 pass 顺序执行，见文末） |

---

## 通用执行流程（所有 pass 共享）

```
Phase 1 — 定位文件
  1. 用户指定了文件 → 用那个
  2. 未指定 → 当前会话最近修改的 HTML 文件
  3. 都没有 → 问用户要审哪个文件
  读文件全文 + 引用的 CSS/tokens/组件文件，解析出真实值。

Phase 2 — 单遍扫描
  逐条应用该 pass 的检查项。报告每一个发现，含置信度和严重度。
  覆盖优先——过滤在 Phase 3 做，不要在扫描阶段自我审查"这个太小就不报了"。

Phase 3 — 修复 + 总结
  直接修。多选项合理的（如换哪个非 Inter 字体），选最稳的默认 + 在总结里标注。
  总结格式：发现 N 项 / 已修 M 项 / 待用户确认 K 项。
```

---

## Pass 1: Accessibility（无障碍）

> **XDesign 此前零覆盖的硬技能缺口。** WCAG AA 是地板不是天花板。

### A1. 对比度与颜色

| 检查项 | 规则 | 失败动作 |
|--------|------|----------|
| 正文对比度 | 正文字号 <18px：与背景对比度 ≥ 4.5:1 | 加深文字色或换背景 |
| 大字对比度 | ≥18px bold 或 ≥24px：≥ 3:1 | 同上 |
| UI 组件对比度 | 按钮/图标/焦点环与相邻背景：≥ 3:1 | 同上 |
| 纯白纯黑 | `#FFFFFF` 文字 on `#000000` 背景 → 告警（建议 `#FAFAFA` / `#1A1A1A`） | 改为柔和的色调 |
| 仅颜色信号 | 状态仅靠颜色区分（红绿、蓝灰无图标无文字） | 加图标或文字标签 |
| 色盲危险组合 | 红+绿、蓝+黄同亮度并列 | 加图案/文字/图标区分 |

### A2. 语义 HTML 与结构

| 检查项 | 规则 | 失败动作 |
|--------|------|----------|
| 唯一 H1 | 全文恰好一个 `<h1>` | 多余的降级或删 |
| 标题不跳级 | 禁止 `<h2>` 直接到 `<h4>` | 补 `<h3>` 或调整层级 |
| 按钮 vs div | 可点击元素用 `<button>` 而非 `<div onclick>` | 换成 `<button>` |
| 链接 vs div | 跳转用 `<a href>` 而非 `<div>` 模拟 | 换成 `<a>` |
| label 关联 | 每个 `<input id="x">` 有 `<label for="x">`（或 `aria-label`） | 补 label |
| alt 文本 | 装饰图 `alt=""`；有意义图描述内容（"耳机侧视图"非"product"） | 修 alt |
| ARIA 纪律 | 能用语义 HTML 就别用 ARIA；`role="button"` 的 `<div>` 应直接是 `<button>` | 换语义元素 |

### A3. 键盘导航与焦点

| 检查项 | 规则 | 失败动作 |
|--------|------|----------|
| 键盘可达 | 所有可点击元素 Tab 可达 | 加 `tabindex="0"` 或换语义元素 |
| Tab 顺序 | 跟随阅读顺序（上到下、左到右）；`tabindex > 0` 告警 | 移除正整数 tabindex |
| 键盘交互 | Modal Escape 关闭；下拉 Enter/Space 打开、方向键导航；表单 Enter 提交 | 补键盘事件 |
| 焦点环 | `outline: none` 必须有替代；优先 `:focus-visible` 而非 `:focus`；替代环对比度 ≥ 3:1 | 恢复焦点环 |
| 跳转链接 | 有大量重复导航的页面，推荐首个可聚焦元素是 "Skip to main content" | 加 skip link |

### A4. 动效与表单

| 检查项 | 规则 | 失败动作 |
|--------|------|----------|
| reduced-motion | >200ms 的动效需有 `@media (prefers-reduced-motion: reduce)` 降级（粒度：保留 opacity/color，移除 transform） | 加降级块 |
| 无闪烁 | >3 次/秒的闪烁可诱发光敏性癫痫 → 必须有暂停控件或删除 | 删除或减速 |
| 表单错误具体 | "邮箱格式无效"而非"无效"；错误信息与字段通过 `aria-describedby` 关联 | 改文案 + 加关联 |
| 必填标记 | `required` 属性 + 文字/图标，非仅靠颜色 | 加 `required` + 文字 |
| 输入类型 | 邮箱用 `type="email"`，电话用 `type="tel"`，配 `autocomplete` | 改 type |
| 命中区 | 触屏按钮/链接 ≥ 44×44px | 改尺寸 |

---

## Pass 2: AI-Slop（反模板味）

> 检测"AI 生成模板感"的视觉套路。生成时的避免规则见 [mode-2-prototype.md Anti-AI-Slop Rules](./mode-2-prototype.md#anti-ai-slop-rules-with-why-and-boundaries) 与 [Design Preference Layer](./mode-2-prototype.md#design-preference-layer-deeper-bias-correction)。本 pass 提供**生成后的检测视角**。

### S1. 视觉套路扫描

逐条对照下表，命中即报告。每条规则的"为何是 slop"与"合法例外"见 mode-2-prototype.md 对应章节。

| # | 检测项 | 扫描方法 |
|---|--------|----------|
| 1 | 激进渐变（彩虹/3+色/紫粉/橙粉大面渐变） | 搜 `linear-gradient` / `radial-gradient`，检查色标数与色相 |
| 2 | emoji 当装饰（标题/按钮/列表前的 🚀✅🎉） | 搜 emoji 字符，核对品牌是否真用 |
| 3 | 圆角+左边框卡片（`border-radius` + `border-left: 4px` 当默认卡） | 搜该 CSS 组合 |
| 4 | 手绘 SVG 人物/场景（劣质插画） | 检查 `<svg>` 内的人物/抽象图形 |
| 5 | CSS 剪影代替真实产品图 | 检查 hardware 产物是否用了真实照片（参 [Brand Asset Protocol](./brand-asset-protocol.md)） |
| 6 | Inter/Roboto/Arial/Fraunces 当默认字体 | 搜 `font-family`，无品牌理由则告警 |
| 7 | 暗蓝底+通用霓虹光（`#0D1117` + generic glow） | 检查暗色主题是否为此懒散组合 |
| 8 | 暖编辑风当默认（奶油底+衬线+陶土橙，无品牌理由） | 检查 dashboard/devtool/fintech 是否误用 |

### S2. 深层偏好偏差扫描

对照 [Design Preference Layer](./mode-2-prototype.md#design-preference-layer-deeper-bias-correction) 四维表（typography / color / layout / motion），逐项检查：

- **Typography**：是否用衬线标榜"创意"？是否在无衬线标题里塞随机衬线单词？是否 Inter 无处不在？斜体 descender 是否被裁切？
- **Color**：高端消费品是否千篇一律暖米色？设计中段是否出现新强调色（drift）？强调色饱和度是否 >80%？
- **Layout**：英雄区是否居中+暗渐变 mesh？是否三张等高 feature 卡？是否每页都分体头？
- **Motion**：是否有无目的的无限滚动 marquee？是否每个元素都 fade-in？是否有无叙事目的的粒子背景？

### S3. 修复原则

- 每个命中项：先确认是否属于"品牌自身使用该模式"的合法例外——是则跳过
- 不确定时，选最稳的默认替代 + 在总结里标注，让用户覆盖
- **不要过度拦截**：电影级打光、暖调赛博、暗叙事场景不是 slop——只有"暗蓝+通用霓虹"这个懒散组合才是

**溢出提示：** slop 命中项常伴随层级问题（三张等高 feature 卡既是 layout slop 也是节奏单调）。若 S2 Layout 维度命中 ≥2 项，建议跑 Pass 3 复核层级与节奏。

---

## Pass 3: Hierarchy & Rhythm（层级与节奏）

> 层级引导视线，节奏让设计显得刻意。两者是"刻意"与"AI 生成"最关键的分水岭。

### H1. 层级检查

对每个屏幕/幻灯/大区块：

| 检查项 | 规则 |
|--------|------|
| 主-次-三级可识别 | 能说出"用户先看什么、再看什么、第三看什么"；说不清 = 层级失败 |
| 尺寸分化 | 标题显著大于正文；主 CTA 大于次级动作；相似内容尺寸一致 |
| 颜色层级 | 主操作用品牌饱和色；次级用中性；弱化内容用浅灰 |
| 字重层级 | 标题 bold、正文 regular；全 bold = 无重点；全 regular = 无强调 |
| 位置 | 左上角优先（LTR 语言）；主内容在黄金区位，别埋在右下 |
| 密度信号 | 重要元素周围留白多；支撑内容间距紧 |
| **5 秒测试** | 首次用户 5 秒内能否看懂"看什么 + 做什么"；不能 = 眼睛没有清晰路径 |

### H2. 节奏检查

对整个文件：

| 检查项 | 规则 |
|--------|------|
| 间距比例尺 | 所有 padding/margin/gap 落在 4px 或 8px 倍数；`7px`/`18px`/`13px` 等杂值告警 |
| 字号比例尺 | 所有 font-size 来自定义的 type scale；`17px`/`23px` 等杂值告警 |
| 重复 | 应该相似的区块（卡片网格、列表项）共享 padding/gap/字号/结构 |
| 刻意变化 | 长页面应偶尔打破模式（换背景/加宽/居中 CTA）；全统一 = 单调，全变化 = 混乱 |
| 配色纪律 | 全产品 3-5 色（含 tint/shade）；8+ 不同色或多个近似蓝灰 = 告警 |
| 对齐 | 元素对齐网格；偏移几像素若是"像手滑"而非刻意 = 告警 |

### H3. 修复原则

- 杂乱间距 → 吸附到最近的 scale 值；无 scale 则定义一个（4 或 8 倍数）
- 扁平层级 → 引入对比（标题更大、CTA 更突出）
- 反转层级 → 交换信号（弱化元素降色、重要元素归位）
- 单调 → 在某一节引入刻意打破；混乱 → 收敛到最强模式

---

## Pass 4: Interaction States（交互状态）

> XDesign 此前近空白。一个按钮只有 default 态 = 半成品。

### I1. 盘点交互元素

遍历文件，列出所有：
- `<button>` / `<a>` / `<input>` / `<select>` / `<textarea>`
- `[role="button"]` / `[onclick]` / 任何绑定了事件的元素

### I2. 六态完整性

对每个交互元素验证：

| 状态 | 规则 | 缺失动作 |
|------|------|----------|
| default | 有明确的默认外观 | 定义基础样式 |
| hover | 鼠标悬停有反馈（必须在 `@media (hover: hover) and (pointer: fine)` 内，触屏安全） | 加 hover 样式 + 媒体查询守护 |
| active | 按下瞬间有反馈（如 `transform: scale(0.97)`） | 加 active 样式 |
| disabled | 禁用态需 `cursor: not-allowed` + `opacity` 降低 + 视觉区分（非仅变灰） | 补完整 disabled 样式 |
| focus | 键盘聚焦有可见环（用 `:focus-visible` 非 `:focus`），对比度 ≥ 3:1 | 加 focus-visible 样式 |
| loading | 提交类按钮需有 loading 反馈（spinner / 文案变化 / disabled） | 加 loading 态 |

### I3. 过渡与反馈

| 检查项 | 规则 |
|--------|------|
| 过渡时长 | 状态变化 150-300ms；入场/出场可更长（参 [animation-standards.md](./animation-standards.md) #13 时长边界） |
| 属性限定 | 只过渡 `transform` 和 `opacity`（参 #15），禁止 `transition: all`（参 #11） |
| 缓动曲线 | 入场用 `ease-out`，移动用 `ease-in-out`，颜色/透明度用 `ease`（参 #12） |
| 动作反馈 | 成功/错误确认需可见且通过 `aria-live` 公告给辅助技术 |
| 无死按钮 | 所有 `<button>` 必须绑定真实行为；无行为的占位按钮加 `disabled` 或删除 |

### I4. reduced-motion 检查

确认所有过渡/动效有 `@media (prefers-reduced-motion: reduce)` 降级，粒度遵循 [animation-standards.md Reduced-Motion Granularity](./animation-standards.md#reduced-motion-granularity)：保留 opacity/color，移除 transform/position。

---

## 全量审查（4 pass 顺序执行）

当用户要求"全面审查 / polish / 上线前把关"时，按序跑 4 个 pass，然后聚合：

```
Step 1 — 顺序执行 Pass 1→2→3→4，各自产出 findings 列表
Step 2 — 去重：多个 pass 报同一问题（如焦点环缺失同时被 P1 和 P4 命中）→ 合并为一条
Step 3 — 分级：
  Blocker  — 无障碍硬伤（对比度不达标、键盘不可达、焦点环删除、缺 label）→ 必须全修
  Quality  — AI slop 套路、层级断裂、交互态缺失 → 必须全修
  Polish   — 细微改进（色调整移、间距收紧）→ 范围内则改，超范围则标注
Step 4 — 修复：先 Blocker，再 Quality，最后 Polish
Step 5 — 复验（关键）：修完后对高风险区回头检查——
  - 对比度修复是否冲淡了品牌色？
  - 焦点环添加是否与相邻内容重叠？
  - 层级调整后主 CTA 是否真的显眼了？
  有问题继续修；不确定的标注给用户。
Step 6 — 总结：Verdict（可上线 / 待用户确认 / 需再迭代）+ 各级修复数 + 待确认项
```

**复验不可跳过。** 修复本身会引入新问题——不复验的 polish pass 等于没做。
