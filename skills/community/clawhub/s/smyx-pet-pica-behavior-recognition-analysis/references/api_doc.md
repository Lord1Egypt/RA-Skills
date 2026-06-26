# API 接口文档

此处用于存放宠物异食行为识别（啃咬电线/塑料）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/ai-analysis/v2/start-common-ai-analysis` - 启动异食行为识别分析任务
2. `/web/ai-analysis/get-common-ai-analysis-result` - 获取分析结果
3. `/web/ai-analysis/page-common-ai-analysis-result` - 分页查询历史报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_PET_PICA_BEHAVIOR_RECOGNITION_ANALYSIS` - 宠物异食行为识别（啃咬电线/塑料）

## 危险物品类别（建议覆盖）

- 电线 / 充电线 / 数据线（触电、电烧伤风险）
- 塑料袋 / 塑料瓶盖 / 塑料碎片（窒息、肠梗阻风险）
- 袜子 / 内衣 / 抹布（肠梗阻高发）
- 纸巾 / 厕纸（堵塞消化道风险）
- 玩具碎片 / 橡皮筋 / 发圈（线性异物，猫高发）
- 药品包装 / 化学清洁剂瓶（中毒风险）

## 设备联动

- 持续接触 ≥ 2 秒 即触发预警信号
- 输出可直接由智能家居安防设备（智能音箱、宠物摄像头）消费，实现声光劝阻或推送告警
