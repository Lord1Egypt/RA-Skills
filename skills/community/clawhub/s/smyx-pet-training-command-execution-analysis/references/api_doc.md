# API 接口文档

此处用于存放宠物训练指令执行识别（坐/卧/等）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/ai-analysis/v2/start-common-ai-analysis` - 启动训练指令执行识别分析任务
2. `/web/ai-analysis/get-common-ai-analysis-result` - 获取分析结果
3. `/web/ai-analysis/page-common-ai-analysis-result` - 分页查询历史报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_PET_TRAINING_COMMAND_EXECUTION_ANALYSIS` - 宠物训练指令执行识别（坐/卧/等）

## 设备联动

- 输出包含：指令名称、指令发出时间、宠物完成姿态、姿态匹配度、响应延迟（秒）
- 未执行成功时，可由智能训狗设备根据本技能输出结果触发声控重复提示
