# API 接口文档

此处用于存放婴幼儿踢被/蹬被识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动婴儿踢被识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与覆盖状态
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史踢被预警记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_INFANT_BLANKET_KICK_DETECTION_ANALYSIS` - 婴幼儿踢被/蹬被识别

## 输入约束

- 摄像头建议固定于婴儿床上方俯视拍摄，覆盖婴儿全身及周边床面
- 夜间需启用红外/微光模式，帧率建议 ≥ 10 FPS
- 时段建议覆盖夜间睡眠主要时段（如 20:00 - 次日 07:00）

## 被子覆盖状态

- `full_cover` - 完整覆盖（≥ 80%）
- `partial_cover` - 部分覆盖（50% - 80%）
- `low_cover` - 覆盖不足（< 50%，触发预警）
- `no_cover` - 被子完全踢开 / 不在身体上

## 关键检测事件

- `kick_motion` - 踢腿/蹬腿动作（连续幅度较大）
- `blanket_slip` - 被子下滑事件
- `blanket_off_body` - 被子离开身体事件
- `coverage_below_threshold` - 覆盖率持续低于阈值（默认 50%）

## 默认阈值（可由调用方覆盖）

- 覆盖率告警阈值：50%（coverage_threshold_pct）
- 持续秒数阈值：30 秒（low_cover_duration_threshold_sec）

## 输出字段（参考）

- `infant_detected` - 是否检测到婴儿
- `blanket_coverage_pct` - 当前被子覆盖比例（%）
- `coverage_state` - 覆盖状态（full_cover / partial_cover / low_cover / no_cover）
- `kick_events` - 踢被事件列表（时间戳 + 持续时长）
- `low_cover_duration_sec` - 当次覆盖不足持续秒数
- `alert_level` - 预警等级（none / info / warning）
- `alert_message` - 预警文本（如"宝宝被子已被踢开，建议盖被或提高室温"）
- `smart_home_hint` - 联动智能家居建议（如"建议自动提高室温 1℃"）

> 仅输出基于视觉的被子覆盖状态与踢被事件，不提供医疗建议或具体处置方案。
