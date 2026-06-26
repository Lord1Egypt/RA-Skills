# API 接口文档

此处用于存放老年人如厕时间异常（超30分钟）识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动老年人如厕时间异常监测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与异常预警
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史如厕监护记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_ELDERLY_TOILET_TIME_ABNORMAL_ANALYSIS` - 老年人如厕时间异常（超30分钟）识别

## 输入约束

- 推荐摄像头安装于卫生间门口（首选）
- 如必须安装在卫生间内部，**仅检测人体轮廓**，画面建议做模糊化/像素化处理，禁止采集隐私细节
- 24 小时全天候采集（含红外夜视）
- 视频帧率建议 ≥ 10 FPS

## 关键检测事件

- `enter_toilet` - 进入卫生间事件（含时间戳）
- `exit_toilet` - 离开卫生间事件（含时间戳）
- `current_occupancy_sec` - 当前连续停留秒数
- `occupancy_session` - 完整一次停留会话（起止时间 + 持续秒数）

## 默认安全阈值（可由调用方覆盖）

- 如厕停留预警阈值：30 分钟（toilet_duration_threshold_min）
- 分级预警：
  - 20-30min → info（接近阈值）
  - 30-60min → warning（异常）
  - ≥ 60min → critical（紧急，疑似突发疾病/跌倒）

## 输出字段（参考）

- `person_detected` - 是否检测到人体
- `is_in_toilet` - 当前是否在卫生间内
- `enter_time` - 本次进入时间
- `current_duration_min` - 本次停留时长（分钟）
- `occupancy_history` - 当日如厕会话历史
- `abnormal_alert` - 是否触发停留时间异常预警
- `alert_level` - 预警等级（none / info / warning / critical）
- `alert_message` - 预警文本（如"老人已在卫生间停留 35 分钟，建议立即上门查看"）
- `suggested_contacts` - 建议通知的联系人（子女 / 护理人员 / 社区网格员）

> 仅基于人体进出与停留时长输出统计与预警，不提供医疗诊断；为保护隐私，原始画面建议在采集端做模糊化/像素化处理。
