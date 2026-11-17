# Curated UIFlow2 Examples

这些示例是人工精选的 UIFlow2 程序，用于复用整体结构、状态管理和性能策略。
示例按 UI 体系和屏幕分辨率组织，不以某一款主机作为唯一适用范围。
每个条目单独记录验证状态；未标明硬件验证时，不要声称已经过真机测试。
API 名称、参数和兼容性仍以 `docs/` 为准；不要仅凭示例推断未记录的 API。

## Hourglass (Widgets, 135 x 240)

- 仓库源路径：`examples/widgets/hourglass_135x240.py`
- Skill 镜像：[assets/examples/widgets/hourglass_135x240.py](../assets/examples/widgets/hourglass_135x240.py)
- 能力点：IMU gravity mapping and filtering、button-driven state changes、off-screen Canvas rendering、grid-based particle simulation、allocation-conscious animation loop
- 参考条件（需同时满足）：目标屏幕为 135 x 240；请求包含持续动画、IMU/重力/倾斜、粒子/物理模拟、按钮暂停或重置、离屏 Canvas
- 结构精华：固定 4 x 4 网格和 bytearray mask，限制粒子数量与内存；IMU 滤波、dead zone 和方向映射，避免画面抖动；time.ticks_ms/ticks_diff 帧间隔控制，M5.update 持续运行；M5.Lcd.newCanvas 复用整帧后一次 push，按钮回调只置位状态
- 验证状态：开发者提供的参考实现；未记录真机验证
- 适用场景：Building a 135 x 240 Widgets animation, sensor-driven simulation, or frame-timed Canvas application.

## Weather (Widgets, 135 x 240)

- 仓库源路径：`examples/widgets/weather_135x240.py`
- Skill 镜像：[assets/examples/widgets/weather_135x240.py](../assets/examples/widgets/weather_135x240.py)
- 能力点：reuse of the existing UIFlow2 Wi-Fi connection、optional Wi-Fi fallback only when offline、HTTPS weather API requests and JSON parsing、cached offline display and refresh scheduling、off-screen Canvas dashboard rendering
- 参考条件（需同时满足）：目标屏幕为 135 x 240；请求包含天气/网络仪表盘、Wi-Fi、HTTP/HTTPS、周期刷新、缓存或 offline/stale 状态
- 结构精华：暗色 token 调色板和 135 x 240 紧凑信息层级；M5.Lcd.newCanvas 复用离屏画布，天气图标由基础图元组合；先复用 UIFlow2 已联网状态，Wi-Fi/HTTP 有限超时和异常降级；15 分钟刷新、Button A 手动刷新、缓存数据标记 offline
- 验证状态：开发者提供的参考实现；未记录真机验证
- 适用场景：Building a 135 x 240 Widgets dashboard, periodic API client, cached offline view, or weather application.

## Weather (M5UI/LVGL, 320 x 240)

- 仓库源路径：`examples/m5ui/weather_320x240.py`
- Skill 镜像：[assets/examples/m5ui/weather_320x240.py](../assets/examples/m5ui/weather_320x240.py)
- 能力点：M5UI page, Canvas, label, and button composition、reuse of the existing UIFlow2 Wi-Fi connection、optional Wi-Fi fallback only when offline、IP-based location with Shenzhen fallback、HTTPS weather requests, caching, and offline display
- 参考条件（需同时满足）：目标屏幕为 320 x 240 且使用 m5ui/LVGL；请求包含网络仪表盘、天气、HTTPS、缓存、offline/stale 或触控刷新
- 结构精华：M5Page + M5Canvas + M5Label/M5Button 的 parent=page 组合；M5Canvas 使用 RGB565 和 begin_draw/end_draw 批量提交；lv.text_get_size 计算数字、单位和右对齐文本位置；网络刷新显示 UPDATING/ONLINE/OFFLINE，保留缓存并回收内存
- 验证状态：开发者提供的参考实现；未记录真机验证
- 适用场景：Building a 320 x 240 M5UI/LVGL network dashboard, weather client, or cached offline view.

## Hourglass (M5UI/LVGL, 320 x 240)

- 仓库源路径：`examples/m5ui/hourglass_320x240.py`
- Skill 镜像：[assets/examples/m5ui/hourglass_320x240.py](../assets/examples/m5ui/hourglass_320x240.py)
- 能力点：M5UI page and touch button composition、IMU gravity mapping and filtering、double-buffered LVGL Canvas rendering、grid-based particle simulation、frame-timed allocation-conscious animation
- 参考条件（需同时满足）：目标屏幕为 320 x 240 且使用 m5ui/LVGL；请求包含自定义 Canvas 动画、IMU/重力/倾斜、粒子/物理模拟、双 Canvas、触摸暂停或补充
- 结构精华：M5UI page 下只占中间区域的 RGB565 LVGL Canvas，保留左右触控按钮；复用 lv.draw_* descriptor 和 layer，避免每帧创建对象；前后两个 Canvas 完整绘制后通过 HIDDEN 切换，避免空白帧；物理步数与渲染帧解耦，IMU 滤波后驱动固定网格粒子
- 验证状态：开发者提供的参考实现；未记录真机验证
- 适用场景：Building a 320 x 240 M5UI/LVGL animation, IMU-driven simulation, or custom LVGL Canvas renderer.
