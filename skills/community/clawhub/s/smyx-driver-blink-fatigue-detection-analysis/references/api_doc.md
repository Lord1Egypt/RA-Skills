# API 接口文档

此处用于存放驾驶员眨眼频率与闭眼时长检测 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动驾驶员疲劳监测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取疲劳监测结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史疲劳事件
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_DRIVER_BLINK_FATIGUE_DETECTION_ANALYSIS` - 驾驶员眨眼频率与闭眼时长检测

## 输入约束

- 摄像头：车载 DMS 摄像头（红外/IR-cut 优先）
- 安装位置：方向盘上方 / A 柱 / 仪表台上方，正对驾驶员面部
- 帧率：≥ 30 FPS（推荐）；分辨率 ≥ 480p
- 必须能稳定看到双眼区域；夜间/隧道场景启用红外补光
- 支持戴普通眼镜，墨镜会显著影响检测

## 关键观测指标

- `eye_state` - 眼部状态时序（open / closed / partial）
- `blink_count_per_minute` - 每分钟眨眼次数（次/分钟）
- `avg_blink_duration_ms` - 平均单次眨眼持续时长（毫秒）
- `max_closed_eye_duration_ms` - 单次最长闭眼时长（毫秒）
- `microsleep_count` - 微睡眠事件次数（单次闭眼 > 2s）
- `perclos` - PERCLOS（80% 阈值下，单位时间内闭眼帧占比）

## 正常/异常阈值（可由调用方覆盖）

- 正常眨眼频率：15-20 次/分钟
- 眨眼频率偏低告警阈值：< 10 次/分钟
- 单次闭眼超过 2 秒 → 触发微睡眠预警
- PERCLOS > 0.15 → 中度疲劳；> 0.30 → 重度疲劳

## 预警类型

- `low_blink_rate` - 眨眼频率过低
- `microsleep` - 微睡眠（单次闭眼 > 2s）
- `prolonged_eye_closure` - 长时间闭眼（> 3s）
- `high_perclos` - PERCLOS 超阈值（持续疲劳）
- `eyes_off_road` - 视线长时间偏离前方（参考）

## 输出字段（参考）

- `driver_detected` - 是否检测到驾驶员
- `eye_visible` - 双眼是否可见（戴墨镜/遮挡时为 false）
- `blink_metrics` - 眨眼相关指标（blink_count_per_minute / avg_blink_duration_ms / max_closed_eye_duration_ms / microsleep_count / perclos）
- `fatigue_level` - 疲劳等级（normal / mild / moderate / severe）
- `warning_type` - 触发的预警类型
- `warning_message` - 预警提示文本（如"驾驶员眨眼频率仅 8 次/分钟且出现 1 次 2.4 秒微睡眠，请立即靠边休息"）
- `recommend_action` - 建议的座舱联动动作（voice_alert / seat_vibrate / fleet_upload）

> 仅输出基于视觉的驾驶员疲劳指标与预警，不提供医学诊断或睡眠障碍诊断；预警仅供辅助提醒，驾驶员对车辆操作负全责。
