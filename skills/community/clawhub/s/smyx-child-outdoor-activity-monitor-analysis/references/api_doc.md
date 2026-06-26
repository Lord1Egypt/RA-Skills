# API 接口文档

此处用于存放儿童户外活动时长监测 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动儿童户外活动时长监测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取户外活动统计结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史户外活动记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_CHILD_OUTDOOR_ACTIVITY_MONITOR_ANALYSIS` - 儿童户外活动时长监测

## 输入约束

- 摄像头：家庭阳台门 / 入户门口 / 楼道门口固定摄像头，对准门口/阳台门通道区域
- 帧率 ≤ 10 FPS 即可（事件检测无需高帧率）；分辨率 ≥ 480p
- 摄像头需可同时清晰看到"门内侧"和"门外侧/阳台外侧"两个区域
- 初次部署在画面中**框选两个 ROI**：
  - `indoor_region` - 室内区域
  - `outdoor_region` - 户外区域（阳台/楼道外/楼下）
- 建议儿童佩戴可识别特征（如颜色/身高），用于在多人场景下区分识别

## 关键观测信号

- `indoor_region_defined` / `outdoor_region_defined` - 两个 ROI 是否已定义
- `child_detected` - 是否检测到儿童
- `exit_events` - 儿童离开室内事件列表（含时间戳）
- `return_events` - 儿童返回室内事件列表（含时间戳）
- `outdoor_session_count_today` - 当日户外外出次数（一次外出+归来计 1 次）
- `outdoor_session_durations_today` - 各次户外时长列表（分钟）
- `total_outdoor_duration_today_min` - 当日累计户外活动总时长（分钟）
- `last_exit_time` / `last_return_time` - 最近一次外出/归来时间

## 默认推荐与阈值（可由调用方覆盖）

- 学龄儿童建议每日户外活动 **≥ 60 分钟**（recommended_outdoor_min_default = 60）
- 低于推荐值且时间已到 18:00 → 触发"今日户外活动不足"提醒
- 连续 ≥ 3 天低于推荐值 → 升级提醒至 warning
- 单次外出 < 5 分钟 默认视为无效会话（如下楼丢垃圾、收快递等，可由调用方覆盖）

## 提醒类型

- `daily_outdoor_insufficient` - 当日户外活动不足
- `multi_day_outdoor_insufficient` - 连续多日户外不足
- `outdoor_goal_met` - 当日已达成户外活动推荐量
- `normal` - 正常

## 输出字段（参考）

- `child_detected` / `indoor_region_defined` / `outdoor_region_defined`
- `today_metrics` - 当日指标（outdoor_session_count_today / outdoor_session_durations_today / total_outdoor_duration_today_min / last_exit_time / last_return_time）
- `recommended_outdoor_min` - 推荐户外时长（min）
- `goal_completion_pct` - 当日达成率（0-1）
- `consecutive_insufficient_days` - 连续不足天数
- `alert_type` - 提醒类型
- `alert_level` - 提醒级别（info / notice / warning）
- `alert_message` - 推送给家长的文本（如"宝宝今天累计户外活动只有 25 分钟，离推荐 60 分钟还有差距，下午带 TA 去公园玩一会儿吧~"）
- `recommend_action` - 建议动作（push_app_notice / suggest_outdoor_plan / observe_only）

> 仅输出基于视觉的进出门事件统计与友好提醒，不直接代表真实运动量；如儿童视力/骨骼发育/情绪问题已较明显，请咨询专业医生。
