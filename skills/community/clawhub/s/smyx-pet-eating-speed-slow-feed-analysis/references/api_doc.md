# API 接口文档

此处用于存放宠物进食速度检测与慢食干预 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/ai-analysis/v2/start-common-ai-analysis` - 启动进食速度检测分析任务
2. `/web/ai-analysis/get-common-ai-analysis-result` - 获取分析结果
3. `/web/ai-analysis/page-common-ai-analysis-result` - 分页查询历史报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_PET_EATING_SPEED_SLOW_FEED_ANALYSIS` - 宠物进食速度检测与慢食干预

## 干预联动

- 触发条件：进食速度 ＜ 安全阈值（默认 30 秒/碗）
- 外部干预通道：智能慢食碗隔板弹出 / 语音播报提醒（由设备侧基于报告结果实施）
