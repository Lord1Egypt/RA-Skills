# API 接口文档

此处用于存放儿童坐姿不良（驼背/歪头）实时提醒 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动儿童坐姿不良识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与语音提醒指令
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史坐姿监测记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_CHILD_POOR_POSTURE_DETECTION_ANALYSIS` - 儿童坐姿不良（驼背/歪头）实时提醒

## 输入约束

- 摄像头建议为智能台灯内置摄像头或书桌上方摄像头
- 视野需覆盖儿童上半身（肩部至头部）
- 视频帧率建议 ≥ 15 FPS；光照均匀，避免逆光

## 关键观测指标

- `cobb_angle_deg` - 脊柱弯曲角度估算（Cobb 角，°）
- `head_tilt_deg` - 头部侧倾角度（°）
- `shoulder_horizontal_offset_deg` - 双肩水平偏差（°）
- `eye_to_desk_distance_cm` - 眼睛与书面距离（估算，cm）

## 默认告警阈值（可由调用方覆盖）

- 驼背：Cobb 角 > 10°
- 歪头：头部侧倾角 > 15°
- 持续时长触发阈值：5 秒（hold_duration_threshold_sec）
- 用眼距离过近：< 25 cm（建议触发"距离过近"提醒）

## 不良姿态类型

- `hunchback` - 驼背
- `head_tilt` - 歪头
- `forward_head` - 头部前伸
- `shoulder_asymmetry` - 双肩不平
- `too_close_to_desk` - 离书面过近

## 输出字段（参考）

- `child_detected` - 是否检测到儿童
- `posture_metrics` - 姿态参数（cobb_angle_deg / head_tilt_deg / shoulder_horizontal_offset_deg / eye_to_desk_distance_cm）
- `poor_posture_type` - 当前不良姿态类型
- `hold_duration_sec` - 不良姿态持续秒数
- `voice_prompt` - 语音提醒指令文本（如"请坐直"、"头抬正"、"眼睛离书本远一点"）
- `event_time` - 事件时间戳
- `snapshot_url` - 现场快照 URL
- `summary` - 当次会话不良姿态统计（每类型次数/总持续时长）

> 仅输出基于视觉的姿态分析结果与语音提醒指令，不提供医疗诊断或具体矫正训练方案。
