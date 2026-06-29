# API 接口文档

此处用于存放宠物口腔抓拍与牙龈红肿识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/ai-analysis/v2/start-common-ai-analysis` - 启动口腔抓拍与牙龈红肿识别分析任务
2. `/web/ai-analysis/get-common-ai-analysis-result` - 获取分析结果
3. `/web/ai-analysis/page-common-ai-analysis-result` - 分页查询历史报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_PET_ORAL_SNAPSHOT_GUM_REDNESS_ANALYSIS` - 宠物口腔抓拍与牙龈红肿识别

## 抓拍触发说明

- 设备侧建议：在宠物打哈欠、舔嘴、张嘴等口部张开动作时自动触发抓拍
- 本技能消费抓拍图像/视频帧，输出牙龈颜色与牙结石覆盖面积评估
