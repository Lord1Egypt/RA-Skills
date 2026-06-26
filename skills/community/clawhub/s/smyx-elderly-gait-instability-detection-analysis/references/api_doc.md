# API 接口文档

此处用于存放老年人步态不稳/小碎步识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动老年人步态不稳识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与跌倒风险等级
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史步态分析记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_ELDERLY_GAIT_INSTABILITY_DETECTION_ANALYSIS` - 老年人步态不稳/小碎步识别

## 输入约束

- 摄像头建议固定于走廊或客厅，覆盖一段直线行走路径（侧面或正面均可）
- 时长建议 ≥ 5 秒（推荐 10-30 秒），帧率 ≥ 25 FPS
- 老年人需在视频中完成至少 3-5 步连续行走，光照均匀、背景简洁
- 可选附带：身高（用于像素 → cm 换算）、年龄、是否使用助行器

## 关键观测指标

- `step_length_cm` - 步幅长度（cm，估算）
- `gait_speed_m_s` - 步速（m/s）
- `cadence_steps_min` - 步频（步/分钟）
- `trunk_sway_deg` - 躯干左右摇摆角度（°）
- `step_length_variability` - 步幅变异性（CV）
- `double_support_ratio` - 双支撑相占比（%）

## 跌倒风险等级判定（仅作筛查提示）

- `low` - 步幅、步速、躯干稳定均处于正常范围
- `medium` - 步幅偏小 / 步速偏慢 / 躯干摇摆增大 任一指标异常
- `high` - 多项指标同时异常，或步幅显著缩小（小碎步典型表现）+ 躯干摇摆过大

## 输出字段（参考）

- `person_detected` - 是否检测到行走人体
- `walking_detected` - 是否检测到直线行走片段
- `gait_metrics` - 各步态参数数值（step_length_cm / gait_speed_m_s / cadence_steps_min / trunk_sway_deg / step_length_variability / double_support_ratio）
- `gait_pattern` - 步态特征描述（normal / short_steps / wide_sway / slow / mixed）
- `fall_risk_level` - 跌倒风险等级（low / medium / high）
- `risk_factors` - 触发风险等级的关键因子
- `alert_message` - 提示文本（如"检测到小碎步 + 躯干左右摇摆增大，跌倒风险偏高，建议加强陪护或就医评估"）
- `medical_followup_hint` - 医疗复核/康复建议（仅作提示，非诊断）

> 仅输出基于视频的步态客观指标与风险分级，不提供医学诊断；如疑似帕金森、肌少症或近期发生跌倒，请前往专业医疗机构评估。
