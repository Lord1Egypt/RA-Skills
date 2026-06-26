# API 接口文档

此处用于存放老年人厨房忘关火识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动厨房忘关火识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与紧急预警
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史厨房安全记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_KITCHEN_STOVE_LEFT_ON_DETECTION_ANALYSIS` - 老年人厨房忘关火识别

## 输入约束

- 摄像头必须固定于厨房，能够清晰拍摄到灶台区域
- 24 小时全天候采集（建议含红外/热成像通道用于火焰/热源识别）
- 视频帧率建议 ≥ 10 FPS

## 关键检测对象

- 厨房人体活动（人体检测 + 在区域内时长）
- 灶台火焰（可见光火焰特征）
- 灶台热源（红外/热成像高温区域）
- 烟雾（可选，与火焰特征联合判断）

## 关键事件

- `person_in_kitchen` - 厨房内有人
- `person_left_kitchen` - 人员离开厨房（无活动时间开始计时）
- `flame_on` - 灶火处于开启状态
- `flame_off` - 灶火关闭

## 默认安全阈值（可由调用方覆盖）

- 厨房无人 + 灶火开启持续阈值：10 分钟（unattended_flame_threshold_min）
- 分级预警：
  - 5-10min → info（接近阈值，可发短提醒）
  - 10-20min → warning（异常，建议联动关阀）
  - ≥ 20min → critical（紧急，立即通知 + 强制关阀）

## 输出字段（参考）

- `kitchen_person_present` - 当前厨房内是否有人
- `flame_status` - 灶火状态（on / off / unknown）
- `unattended_duration_min` - 无人看管 + 灶火开启持续分钟
- `event_history` - 当次/当日事件序列
- `unattended_flame_alert` - 是否触发忘关火预警
- `alert_level` - 预警等级（none / info / warning / critical）
- `alert_message` - 预警文本（如"厨房无人 12 分钟但灶火仍开启，请立即查看，建议关闭燃气阀"）
- `smart_valve_hint` - 联动智能燃气阀建议（如"建议自动关闭燃气阀门"）

> 仅输出基于视觉的人员活动 + 灶火状态判断与预警，不提供其他安全建议或具体处置方案。
