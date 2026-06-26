# API 接口文档

此处用于存放老年人夜间离床时长与徘徊识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动老年人夜间离床/徘徊分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与预警信息
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史夜间监护记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_ELDERLY_NIGHT_BED_EXIT_WANDERING_ANALYSIS` - 老年人夜间离床时长与徘徊识别

## 输入约束

- 推荐使用卧室固定摄像头夜视模式（红外/低照度），覆盖床铺与走廊出入口
- 时间范围建议覆盖整夜（如 22:00 - 次日 07:00）
- 关键观测对象：床铺区域、人体目标、活动轨迹

## 关键检测事件

- 离床时间点（bed_exit_time）
- 上床时间点（bed_return_time）
- 单次离床时长（exit_duration_sec）
- 总离床时长（total_exit_duration_sec）
- 走廊/房间内来回行走轨迹（wandering_track）
- 徘徊持续时长（wandering_duration_sec）

## 默认安全阈值（可由调用方覆盖）

- 离床时长阈值：30 分钟（exit_duration_threshold_min）
- 徘徊持续阈值：10 分钟（wandering_duration_threshold_min）

## 输出字段（参考）

- `bed_exit_events` - 离床事件列表（含开始/结束时间、持续秒数）
- `total_exit_duration_min` - 当晚累计离床时长（分钟）
- `wandering_detected` - 是否检测到徘徊行为
- `wandering_duration_min` - 徘徊持续时长（分钟）
- `alert_level` - 预警等级（none / info / warning / critical）
- `alert_message` - 预警文本（如"3 号床张爷爷离床已 45 分钟，请及时查看"）

> 仅输出行为统计与预警信息，不提供医疗诊断或具体护理方案。
