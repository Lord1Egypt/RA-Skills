# API 接口文档

此处用于存放宠物赛跑/竞赛作弊识别（起跑/窜道） API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动赛道犯规检测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_RACE_FOUL_DETECTION_ANALYSIS` - 宠物赛跑/竞赛作弊识别（起跑/窜道）
