# API 接口文档

此处用于存放宠物步态分析（跛行/关节炎） API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动步态分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_GAIT_ANALYSIS_LAMENESS_ANALYSIS` - 宠物步态分析（跛行/关节炎）
