# API 接口文档

此处用于存放儿童睡眠中频繁翻身/噩梦识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动儿童夜间翻身/噩梦识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与睡眠质量评估
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史夜间睡眠记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_CHILD_NIGHTMARE_ROLLOVER_DETECTION_ANALYSIS` - 儿童睡眠中频繁翻身/噩梦识别

## 输入约束

- 摄像头建议固定于儿童床上方/侧方，覆盖全身；夜间启用红外/微光模式
- 必须含**音频通道**（用于哭声/梦话识别）
- 视频帧率建议 ≥ 10 FPS；时段建议覆盖整夜（如 20:00 - 次日 07:00）

## 关键检测对象

- 姿态/身体朝向变化（翻身事件）
- 哭声音频特征（音调 / 频率 / 持续时间）
- 梦话/呓语（睡眠中语音识别）
- 突发肢体大幅度动作（疑似噩梦惊跳）

## 关键事件

- `rollover` - 翻身事件（含时间戳，单次/累计）
- `cry` - 哭声事件（含时间戳 + 持续秒数 + 强度）
- `sleep_talk` - 梦话事件
- `body_jerk` - 突发肢体大幅度动作（疑似噩梦惊跳）

## 默认告警阈值（可由调用方覆盖）

- 翻身频率阈值：> 3 次/小时 → 触发"睡眠不安"
- 哭声强度阈值：超过预设 → 触发"可能做噩梦"
- 梦话频次阈值：≥ 3 次/小时 → 触发"睡眠不安"

## 输出字段（参考）

- `child_detected` - 是否检测到儿童
- `sleep_duration_min` - 累计睡眠时长（分钟）
- `rollover_count` - 累计翻身次数
- `rollover_rate_per_hour` - 翻身频率（次/小时）
- `cry_events` - 哭声事件列表（时间戳 + 持续秒数 + 强度）
- `sleep_talk_events` - 梦话事件列表
- `body_jerk_events` - 突发肢体动作事件
- `sleep_quality_score` - 睡眠质量综合得分（0-100）
- `sleep_quality_grade` - 等级（excellent / good / fair / poor）
- `nightmare_alert` - 是否触发噩梦/睡眠不安预警
- `alert_message` - 预警文本（如"宝宝近 1 小时翻身 5 次并伴有哭声，可能做噩梦，请前往安抚"）

> 仅输出基于视觉与听觉的睡眠行为统计，不提供医学诊断或睡眠障碍诊断；如儿童长期睡眠质量差，请咨询专业儿科或睡眠医学医生。
