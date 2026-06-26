# API 接口文档

此处用于存放植物夜间呼吸作用强度估算 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动夜间呼吸强度分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_PLANT_NIGHT_RESPIRATION_RATE_ANALYSIS` - 植物夜间呼吸作用强度估算

## 输入约束

- 推荐使用夜间（无光照时段）采集的植物冠层热成像图像序列
- 可选配套环境数据：气温 T_air、相对湿度 RH、CO₂ 浓度（ppm）
- 关键观测特征：叶片温度 T_leaf、叶-气温差 ΔT = T_leaf - T_air、CO₂ 浓度变化率 dCO₂/dt
