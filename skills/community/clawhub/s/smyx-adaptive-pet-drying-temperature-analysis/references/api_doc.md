# API 接口文档

此处用于存放宠物烘干温度自适应推荐 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/ai-analysis/v2/start-common-ai-analysis` - 启动品种+毛发密度识别与烘干曲线推荐任务
2. `/web/ai-analysis/get-common-ai-analysis-result` - 获取分析结果
3. `/web/ai-analysis/page-common-ai-analysis-result` - 分页查询历史报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_ADAPTIVE_PET_DRYING_TEMPERATURE_ANALYSIS` - 宠物烘干温度自适应推荐

## 设备联动

- 推荐结果包含温度（℃）与时长（分钟）曲线，可直接被智能烘干箱/吹水机消费
- 设备侧依据推荐曲线动态调节风温/风速，防止烫伤
