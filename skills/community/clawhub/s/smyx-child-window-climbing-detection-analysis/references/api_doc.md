# API 接口文档

此处用于存放儿童攀爬窗户/阳台识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动儿童攀爬窗户/阳台识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与紧急预警
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史预警记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_CHILD_WINDOW_CLIMBING_DETECTION_ANALYSIS` - 儿童攀爬窗户/阳台识别

## 输入约束

- 摄像头必须正对窗户、阳台、护栏等高坠风险区域
- 24 小时全天候采集（含红外夜视），覆盖儿童活动半径
- 视频帧率建议 ≥ 15 FPS，确保动作捕捉的实时性

## 关键检测行为

- 攀爬窗户（climbing_window）：脚部蹬踩窗台/扶手
- 跨越护栏（crossing_railing）：身体跨越阳台护栏
- 身体探出窗外（lean_out_window）：上半身越过窗框
- 抓握窗台边缘（grip_window_edge）：手部抓住窗框/护栏外侧
- 危险姿态（risky_posture）：失衡 / 单脚悬空 / 头部探出

## 输出字段（参考）

- `child_detected` - 是否检测到儿童
- `risk_action` - 触发的危险行为类型（climbing_window / crossing_railing / lean_out_window / grip_window_edge / risky_posture）
- `confidence` - 危险行为置信度
- `event_time` - 事件发生时间戳
- `snapshot_url` - 现场快照 URL（建议同步推送 APP）
- `alert_level` - 预警等级（warning / critical / emergency）
- `alert_message` - 紧急预警文本（如"检测到儿童正在攀爬阳台护栏，请立即制止"）

> 仅输出行为识别结果与预警信息，不提供其他安全建议或具体处置方案。
