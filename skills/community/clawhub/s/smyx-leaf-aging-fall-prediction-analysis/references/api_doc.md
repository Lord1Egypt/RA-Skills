# API 接口文档

此处用于存放室内绿植叶片老化/脱落预测 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动叶片老化/脱落预测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与脱落风险预测
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史预测记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_LEAF_AGING_FALL_PREDICTION_ANALYSIS` - 室内绿植叶片老化/脱落预测

## 输入约束

- 推荐使用每天同一角度、同一时段的连续叶片图像（至少过去 7 天）
- 关键观测特征：叶色变化（绿→黄→褐）、叶面光泽度、叶柄基部离层角度
- 可选附带：植物名称/品种、放置环境（光照、湿度）、上次施肥/浇水时间

## 输出字段（参考）

- `aging_index` - 叶片老化指数（0-100%）
- `predicted_fall_window` - 预测脱落时间窗口（如 "未来 3-5 天"）
- `at_risk_leaves` - 即将脱落的叶片定位/编号
- `aging_cause_hint` - 老化原因提示（自然衰老 / 缺水胁迫 / 光照不足 / 营养缺乏等）
- `care_suggestion` - 养护方向建议（提高湿度、调整光照、修剪建议等，非具体化学方案）
