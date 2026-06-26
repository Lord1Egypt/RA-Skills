# API 接口文档

此处用于存放温室环境与植物状态联动调控 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动温室联动调控分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与调控指令
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史调控记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_GREENHOUSE_CLIMATE_PLANT_FEEDBACK_ANALYSIS` - 温室环境与植物状态联动调控

## 输入约束

- 推荐使用温室内固定摄像头实时采集的植物冠层图像/视频（光照充足或夜间补光）
- 可选配套环境数据：光照强度 lux、空气温度 ℃、相对湿度 %、土壤湿度 %、CO₂ 浓度（ppm）
- 关键观测特征：叶片萎蔫角度、茎秆挺直度、叶色变化（黄化/卷曲/灼烧斑）

## 调控指令枚举（输出参考）

- IRRIGATE_ON / IRRIGATE_OFF - 灌溉水泵/电磁阀开关
- SHADE_OPEN / SHADE_CLOSE / SHADE_PARTIAL - 遮阳网开度
- FAN_ON / FAN_OFF - 风机启停
- WET_CURTAIN_ON / WET_CURTAIN_OFF - 湿帘启停
- HEATER_ON / HEATER_OFF - 加热器开关

> 仅输出动作指令及优先级（HIGH / MEDIUM / LOW），不输出具体 PID/开度数值。
