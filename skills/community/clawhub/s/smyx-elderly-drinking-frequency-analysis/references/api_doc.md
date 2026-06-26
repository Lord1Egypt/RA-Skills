# API 接口文档

此处用于存放老年人饮水杯拿起频率（脱水风险）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动老年人饮水频率分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取饮水统计与脱水风险结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史饮水记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_ELDERLY_DRINKING_FREQUENCY_ANALYSIS` - 老年人饮水杯拿起频率（脱水风险）

## 输入约束

- 摄像头：客厅 / 厨房 / 卧室固定摄像头，**画面应稳定覆盖老人常放水杯的区域（茶几/餐桌/床头柜）**
- 帧率 ≥ 5 FPS；分辨率 ≥ 480p；光照尽量稳定
- 视频时段建议覆盖一整天（08:00 - 22:00）或多段拼接覆盖白天
- 杯子轮廓/区域可在初次部署时由用户在画面中框选 ROI（cup_region），提升识别准确度
- 隐私敏感场景应启用人体轮廓模式

## 关键观测信号

- `cup_region_defined` - 是否定义了水杯放置区域 ROI
- `cup_pickup_events` - 杯子被拿起事件列表（含时间戳 + 持续秒数 + 是否伴随饮水手势）
- `cup_pickup_count_daily` - 当日累计拿起次数
- `drink_gesture_count_daily` - 伴随抬手到口部的"疑似饮水"动作次数
- `interval_between_drinks_min` - 相邻两次拿起的平均间隔（分钟）
- `last_pickup_time` - 最近一次拿起时间

## 历史基线字段

- `baseline_window_days` - 基线时间窗口（默认 7-14 天）
- `baseline_daily_pickup_avg` - 历史平均每日拿起次数
- `baseline_daily_pickup_std` - 历史拿起次数标准差

## 默认阈值（可由调用方覆盖）

- 每日最低拿起次数阈值：< 6 次 → 触发"脱水风险"提醒
- 长时间未饮水阈值：连续 > 4 小时未拿起 → 触发"长时间未饮水"提醒
- 个性化基线偏离阈值：当日次数 < 基线均值 - 2 × 标准差 → 触发"较平时显著下降"提醒

## 风险/提醒类型

- `low_daily_intake` - 当日饮水次数过少（脱水风险）
- `long_no_drink_interval` - 长时间未饮水
- `below_personal_baseline` - 较个人历史基线显著下降
- `normal` - 正常

## 输出字段（参考）

- `subject_detected` - 是否检测到老人
- `cup_region_defined` / `cup_visible` - 水杯区域 / 杯子可见性
- `daily_metrics` - 当日指标（cup_pickup_count_daily / drink_gesture_count_daily / interval_between_drinks_min / last_pickup_time）
- `baseline_metrics` - 历史基线（baseline_daily_pickup_avg / baseline_daily_pickup_std）
- `risk_type` - 风险类型（low_daily_intake / long_no_drink_interval / below_personal_baseline / normal）
- `risk_level` - 风险等级（safe / notice / warning）
- `alert_message` - 推送给家属的文本（如"老人今日只拿了 3 次水杯，已 5 小时未喝水，建议提醒老人增加饮水"）
- `recommended_action` - 建议动作（remind_to_drink / family_call_check / observe_only）

> 仅输出基于视觉的饮水行为统计与方向性提醒，**不直接代表实际饮水量**（杯里可能没装水/可能是别人拿杯子），不提供脱水症 / 泌尿系统感染 / 认知障碍等具体医学诊断；连续低饮水或老人有明显不适请及时就医。
