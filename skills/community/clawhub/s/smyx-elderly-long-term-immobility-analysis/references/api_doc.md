# API 接口文档

此处用于存放老年人长期静止（超12小时）监测 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动老年人长期静止监测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与紧急预警
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史监测记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_ELDERLY_LONG_TERM_IMMOBILITY_ANALYSIS` - 老年人长期静止（超12小时）监测

## 输入约束

- 推荐覆盖独居老人家中至少 2 个常驻区域（如客厅 + 卧室），建议加入厨房、卫生间
- 摄像头建议全天候运行（含红外夜视），固定机位
- 视频可按区域分段上传，或上传整段长视频

## 关键检测事件

- 人体活动事件（全身移动 / 四肢动作 / 手部动作 / 姿态变化）
- 最近一次活动时间戳（last_motion_time）
- 累计无活动时长（idle_duration_sec）
- 跨区域活动覆盖统计（active_zones）

## 默认安全阈值（可由调用方覆盖）

- 长期静止阈值：12 小时（immobility_threshold_hour）
- 预警分级：
  - 6h ≤ idle < 12h → warning
  - idle ≥ 12h → critical
  - idle ≥ 24h → emergency

## 输出字段（参考）

- `last_motion_time` - 最近一次检测到活动的时间
- `idle_duration_hour` - 累计无活动时长（小时）
- `active_zones` - 监测期内出现过活动的区域列表
- `immobility_alert` - 是否触发长期静止预警
- `alert_level` - 预警等级（none / warning / critical / emergency）
- `alert_message` - 预警文本（如"独居张爷爷已 14 小时未检测到活动，建议立即联系上门查看"）
- `suggested_contacts` - 建议通知的联系人（子女 / 社区网格员 / 养老服务机构）

> 仅基于视觉活动检测输出统计与预警，不提供医疗诊断或具体救援操作方案。
