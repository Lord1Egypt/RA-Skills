---
name: uiflow2-ui-designer
description: Design, generate, beautify, optimize, or review UIFlow2 interfaces, graphics, dashboards, gauges, animations, round-screen layouts, e-paper screens, and LED-matrix experiences for M5Stack devices. Use with uiflow2-coder when MicroPython API correctness or hardware compatibility matters; do not use for generic web, mobile, or desktop UI.
---

# UIFlow2 UI Designer

为 M5Stack UIFlow2 设备设计有明确视觉层级、交互反馈和性能边界的界面。既可以从零生成，也可以审查并优化现有 MicroPython UI。默认用中文说明，代码和 API 名保持英文。

本 skill 负责设计决策；相邻的 `uiflow2-coder` 负责官方 API 事实。不要复制 Web 端布局、CSS 动效或字体假设到嵌入式屏幕。

## 硬边界

- 先确认目标板卡、旋转后的宽高、屏幕形状、显示类型、输入方式和内容优先级。缺少信息但仍可合理推进时，明确假设；只有会导致 API 或布局路线错误时才追问。
- 一个界面只选一个主要渲染体系；同一 LVGL 页面内的 m5ui 控件与 Canvas 属于同一体系，不要把 Widgets/LCD 对象混入其中。

### 接口选择速查

| 客观条件 | 直接选择 | 明确不要做 |
| --- | --- | --- |
| 能导入 `lvgl`、`m5ui`、`M5Page`，且需求有按钮/开关/列表/图表/多页/触摸 | `m5ui` 语义控件 | 不用 label 或 Canvas 假造可点击控件 |
| 已在 m5ui 页面内，只需自定义图标/静态图形/低频仪表/简单单缓冲动画 | 单个 `m5ui.M5Canvas` + `begin_draw()`/`end_draw()` | 不额外分配双 Canvas，不逐笔提交 |
| 连续整帧动画同时要求隐藏清屏/半成品帧，且 raw LVGL API、draw buffer 和 RAM 已确认 | raw `lv.canvas` + `lv.draw_buf_create()` 双缓冲 | 不把 `M5Canvas` 当作自动双缓冲 |
| m5ui/LVGL 不可导入，或已确认上层对象/内存不足，只需少量静态标签/图片/图元 | `M5.Widgets`；动画挂到 M5GFX Canvas | 不假设 Widgets 有 LVGL 语义按钮/开关/列表 |
| 没有可用上层能力，或目标是极简像素/局部图形 | `M5.Lcd`/`M5.Display.newCanvas()`，完成后一次 `push()` | 不在屏幕上逐笔绘制多步帧 |
- 写代码前读取相邻 coder skill 的官方资料。常用入口是 [m5ui overview](../uiflow2-coder/docs/m5ui/_overview.md)、[display](../uiflow2-coder/docs/hardware/display.md) 和 [Widgets overview](../uiflow2-coder/docs/widgets/_overview.md)。
- API、字体、控件参数或板卡支持范围无法从官方资料确认时，不要猜测。若相邻 coder skill 不存在，在仓库环境读取 `docs/source` 和 `m5stack/libs`；否则报告缺少依赖。
- 新建、重设计或美化可见界面时，先选择一个主视觉方向；风格用于指导层级、布局、色彩和控件状态，不是固定模板。
- 优先使用能表达交互语义的 m5ui 控件。`M5Label` 只用于没有专用组件的静态/
  只读文字或数值，`M5Canvas` 只用于专用控件不能表达的自定义图形，不能用松散
  标签和图元仿造已有控件。
- `M5.update()` 必须持续执行。动画和传感器更新使用有界帧率、`time.ticks_ms()` 和 `time.ticks_diff()`，不阻塞事件处理。
- 可见 UI 不能因为代码能运行就视为完成；如果仍像默认控件拼装、存在不协调背景、溢出或弱层级，继续优化。
- 不能仅凭代码或串口结果声称视觉 PASS。没有模拟器截图、新鲜相机画面或人工实机观察时，视觉结果标记为 `NOT RUN` 或 `PARTIAL`。

## 工作流

1. 建立显示和内容档案：板卡、旋转后尺寸、屏幕形状/类型、输入方式、RAM/PSRAM、语言字体、主任务、信息优先级和最长动态内容。
2. 新建、重设计或美化界面时，按 [design-directions.md](references/design-directions.md) 选择一个主视觉方向和布局变体；只有确有帮助时再加一个次要影响。
3. 若请求需要写 UI 代码或选择绘图接口，先按“接口选择速查”判断，再读 [api-patterns.md](references/api-patterns.md) 的命中小节和 [rendering-strategy.md](references/rendering-strategy.md) 做能力探测：
   - 有 `lvgl`、`m5ui.M5Page` 和所需控件时，优先用 m5ui 原生控件。
   - 需要自定义静态图形、图标或低频仪表时，在 m5ui 页面上使用单个 `m5ui.M5Canvas`，用 `begin_draw()`/`end_draw()` 批量提交。
   - 只有连续整帧动画需要无中间帧且已确认 buffer/RAM 时，才使用 raw `lv.canvas` + `lv.draw_buf_create()` 双缓冲；这是 LVGL 高级路径，不要把它当成普通 `M5Canvas` 调用。
   - m5ui 缺失、目标固件未冻结 LVGL 或资源预算不允许时，再用 `M5.Widgets` 的轻量组件；它没有 LVGL 的布局、样式和事件体系。
   - 只有上述方案不可用，或目标是极简/像素级绘图时才使用 `M5.Lcd`/`M5.Display`。多步绘制必须使用复用的 `M5.Lcd.newCanvas()`，不能直接逐笔画到屏幕。
4. 定义最小 token 集和页面结构：背景、表面、主/辅强调色、文本、状态色、间距、圆角、边框、字体层级、主视觉中心和操作区。
5. 在写代码前规划最长文字、normal/pressed/focused/selected/disabled 状态，以及 loading/empty/error/offline/success 页面状态。
6. 读取所需官方 API 文档后生成或优化代码；显式协调页面与可见控件背景、已验证的 part/state、滚动行为和触摸命中区。
7. 审计交互与动效：每个看起来可操作的控件必须有回调或明确禁用；每个动画必须有触发条件、目标、持续时间、结束条件和性能预算。
8. 对新建、重设计、美化或明确要求视觉验收的任务，按 [visual-quality-gate.md](references/visual-quality-gate.md) 检查渲染结果并迭代；局部 API 修复只做受影响区域的静态检查。没有渲染证据时保持 `NOT RUN`/`PARTIAL`。

## 参考资料路由

- 不要一次加载全部参考资料；先用本页的客观条件选择需要的文件。
- 目标是 EPD、圆屏、16 x 16 Matrix、旋转/尺寸未知或触控边界时读 [display-profiles.md](references/display-profiles.md)；普通已知矩形 LCD 可直接使用本页规则。
- 新建页面、整页重设计、美化、CJK/字体、token 或默认背景协调时读 [visual-system.md](references/visual-system.md)；只改一个已确认 API 时跳过。
- 新建页面或明显改风格时读 [design-directions.md](references/design-directions.md)；只修一个控件的尺寸/颜色时跳过。
- 选择控件、Canvas、图表或降级接口时读 [api-patterns.md](references/api-patterns.md)；写代码时只读命中的小节。
- 只有请求包含连续动画、转场、粒子、传感器驱动效果或闪烁时读 [motion-and-effects.md](references/motion-and-effects.md)。
- 只有需要仪表盘、列表、圆屏、EPD 或 Matrix 版式时读 [layout-recipes.md](references/layout-recipes.md)。
- 审查/重写现有界面时读 [review-checklist.md](references/review-checklist.md)；新建、重设计、美化或用户明确要求视觉验收时读 [visual-quality-gate.md](references/visual-quality-gate.md)。只改不影响像素的单个 API 时跳过。无渲染证据时仍只能报告 `NOT RUN`/`PARTIAL`。

## 设计结果要求

- 层级一眼可辨：每屏一个主任务、一个主视觉焦点，次要信息明显降级。
- 坐标来自屏幕尺寸、边距、网格和文本测量，不靠大量无规律 magic numbers。
- 文本在真实字体下测量；长内容有换行、裁切、省略或滚动策略，不能覆盖相邻元素。
- 专用控件优先于标签或 Canvas 仿造；控件外观、状态和行为必须一致。
- 颜色不作为唯一状态信号；关键状态同时使用文字、图形、亮度、轮廓或运动变化。
- 交互控件有稳定尺寸和按压反馈；动画只解释状态变化，不持续抢占注意力。
- 静态元素只绘制一次；动态区域优先使用 LVGL 局部刷新或复用的离屏 Canvas。直接调用底层绘图时要证明不会暴露中间帧。
- 页面、控件及其可见 part/state 背景协调；不得遗留默认白块、默认蓝色或意外滚动条。
- 界面要有一个与用途匹配的设计概念，但装饰不能牺牲信息密度、可读性、功耗或帧率。

## 禁止清单

- 禁止混用不同 UI 体系管理同一批界面元素。
- 禁止照搬 HTML、CSS、Tailwind、SVG icon library、hover、cursor 或浏览器响应式规则。
- 禁止使用 emoji 充当图标；使用图形 primitive、像素图标或已验证的本地图片资源。
- 禁止假设所有 LVGL 字体、CJK 字体、触摸屏或 PSRAM 在所有板卡上可用。
- 禁止为了“高级感”堆叠渐变、阴影、描边和持续动画；每种效果必须有信息或交互目的。
- 禁止在主循环持续 `fillScreen()`、`clear()`、重新初始化控件或分配全屏 buffer。
- 禁止在 EPD 上设计连续动画，或在 16 x 16 matrix 上套用普通文本界面。

## 回答方式

用户要代码时先给可运行代码，再简要说明视觉方向、关键 token、查过的官方文档和验证步骤。用户要审查时先列 P0/P1/P2 问题和证据，再给最小修改建议。始终区分静态检查、运行通过和视觉实机验证。
