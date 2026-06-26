# API 接口文档

此处用于存放儿童打瞌睡/疲劳检测 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动儿童疲劳检测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（疲劳指数 + 提醒）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史疲劳检测记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_CHILD_DROWSINESS_FATIGUE_DETECTION_ANALYSIS` - 儿童打瞌睡/疲劳检测

## 输入约束

- 摄像头建议正对儿童面部（教室或书桌正前方/智能台灯内置）
- 视频帧率建议 ≥ 15 FPS，确保眼部状态采样精度
- 光照均匀，避免逆光或镜片反光遮挡眼部

## 关键观测指标

- `perclos` - 单位时间内眼睛闭合超过 80% 的时间占比（0-1）
- `eye_closure_duration_sec` - 最长一次连续闭眼秒数
- `blink_rate_per_min` - 眨眼频次（次/分钟）
- `nod_frequency_per_min` - 点头次数（次/分钟，快速下点后抬起）
- `head_drop_angle_deg` - 单次最大头部下垂角度（°）
- `eye_region_glossiness_drop` - 眼部光泽度变化（参考特征）

## 疲劳指数（0-100，综合得分）

- 0-30 - 清醒（alert）
- 30-50 - 轻度疲劳（mild_fatigue）
- 50-70 - 中度疲劳（moderate_fatigue）
- 70-100 - 重度疲劳/疑似打瞌睡（drowsy）

## 默认告警阈值（可由调用方覆盖）

- PERCLOS 阈值：> 0.4 触发疲劳预警
- 连续闭眼阈值：> 2 秒（疑似瞌睡）
- 疲劳指数阈值：> 70 → 触发语音提醒

## 输出字段（参考）

- `child_detected` - 是否检测到儿童
- `fatigue_metrics` - 各项疲劳指标数值（perclos / eye_closure_duration_sec / blink_rate_per_min / nod_frequency_per_min / head_drop_angle_deg）
- `fatigue_score` - 综合疲劳指数（0-100）
- `fatigue_level` - 疲劳等级（alert / mild_fatigue / moderate_fatigue / drowsy）
- `drowsiness_events` - 打瞌睡事件列表（时间戳 + 持续秒数 + 类型）
- `voice_prompt` - 语音提醒文本（如"小朋友，休息一下吧"）
- `summary` - 当次会话疲劳统计摘要

> 仅输出基于视觉的疲劳评估结果与方向性休息提醒，不提供医学诊断或睡眠障碍诊断。
