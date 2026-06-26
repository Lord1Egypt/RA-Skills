# API 接口文档

此处用于存放视频搜索分析 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 请求格式：multipart/form-data 支持文件上传
- 响应格式：JSON

## 主要接口

1. `/web/ai-analysis/v2/start-common-ai-analysis` - 启动AI分析任务
2. `/web/ai-analysis/v2/get-common-ai-analysis-result` - 获取分析结果
3. `/web/ai-analysis/page-common-ai-analysis-result` - 分页查询历史报告
4. `/ai/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `OPEN_VIDEO_SEARCH_ANALYSIS` - 开放平台视频搜索分析
