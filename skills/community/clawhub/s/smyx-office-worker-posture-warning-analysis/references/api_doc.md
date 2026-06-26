# API 接口文档

此处用于存放成人久坐/姿态预警（办公室）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动成人久坐/姿态预警任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（坐姿/久坐预警）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史职场健康记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_OFFICE_WORKER_POSTURE_WARNING_ANALYSIS` - 成人久坐/姿态预警（办公室）

## 输入约束

- 摄像头建议对准工位（侧前方），覆盖头部、颈部、肩部及背部
- 帧率建议 ≥ 10 FPS；光照均匀
- 适用于办公室、居家办公区、公共办公空间

## 关键观测指标

- `continuous_sit_duration_min` - 当次连续坐姿时长（分钟）
- `neck_forward_angle_deg` - 颈部前倾角度（°，头部相对肩部偏移）
- `back_curvature_deg` - 背部弯曲度（°，驼背程度）
- `shoulder_drop_diff_deg` - 双肩高度差（°）
- `eye_to_screen_distance_cm` - 眼-屏幕距离（估算，cm）
- `stand_up_count_per_hour` - 每小时起身次数

## 默认告警阈值（可由调用方覆盖）

- 久坐时长阈值：60 分钟（continuous_sit_threshold_min）
- 颈部前倾角阈值：> 20°（neck_forward_threshold_deg）
- 背部弯曲阈值：> 阈值（back_curvature_threshold_deg）
- 眼-屏距离过近：< 40 cm

## 预警类型

- `prolonged_sitting` - 久坐提醒（建议起身活动）
- `forward_head_posture` - 颈部前倾提醒（建议直颈）
- `hunchback_posture` - 驼背提醒（建议直背）
- `shoulder_asymmetry` - 双肩不平提醒
- `too_close_to_screen` - 离屏幕过近提醒

## 输出字段（参考）

- `person_detected` - 是否检测到办公人员
- `posture_metrics` - 姿态参数（neck_forward_angle_deg / back_curvature_deg / shoulder_drop_diff_deg / eye_to_screen_distance_cm）
- `continuous_sit_duration_min` - 当次连续坐姿时长
- `stand_up_count_per_hour` - 每小时起身次数
- `warning_type` - 触发的预警类型
- `warning_message` - 预警提示文本（如"已连续坐 65 分钟，请起身活动 5 分钟"、"颈部前倾 25°，请直颈调整屏幕高度"）
- `summary` - 当次会话久坐+姿态统计摘要

> 仅输出基于视觉的坐姿与活动监测结果，不提供医学诊断或具体康复方案。
