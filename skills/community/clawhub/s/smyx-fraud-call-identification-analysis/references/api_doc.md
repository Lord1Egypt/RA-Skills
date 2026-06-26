# API 接口文档

此处用于存放诈骗电话识别分析 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 请求格式：支持文件上传，纯文本支持 application/json
- 响应格式：JSON

## 主要接口

1. `/web/fraud-analysis/v2/start-fraud-analysis` - 启动诈骗分析任务
2. `/web/fraud-analysis/v2/get-fraud-analysis-result` - 获取分析结果
3. `/web/fraud-analysis/page-fraud-analysis-result` - 分页查询历史报告
4. `/fraud/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `OPEN_FRAUD_CALL_IDENTIFICATION` - 开放平台诈骗电话识别分析
