# API 接口文档

此处用于存放植物整体活力指数（综合评分）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动植物活力指数评估任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（活力评分 + 趋势）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史活力评分记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_PLANT_VITALITY_INDEX_ANALYSIS` - 植物整体活力指数（综合评分）

## 输入约束

- 推荐使用每日同一角度、同一时段的连续植物图像（最少最近 3-7 天）
- 单图也可输出当次评分，但无法给出趋势
- 可选附带环境数据：光照 lux、气温 ℃、相对湿度 %、土壤湿度 %
- 可选附带生长指标：新芽数、叶面积（cm²）、上次浇水/施肥时间

## 评分维度（融合）

- 叶片颜色（叶绿素指数）—— 越绿越饱满分越高
- 叶片形态（舒展度、叶片大小）
- 新芽萌发数
- 叶面积增长率（基于序列）
- 整体株型紧凑度

## 输出字段（参考）

- `vitality_score` - 活力总分（0-100）
- `vitality_grade` - 活力等级（excellent / good / fair / poor）
- `trend` - 近期趋势（rising / stable / declining）
- `trend_change_pct` - 近 7 天变化百分比（如 -15%）
- `sub_scores` - 子维度分数（chlorophyll / morphology / new_buds / growth_rate）
- `alert_hint` - 活力下降阈值告警提示

> 仅输出综合评分与趋势，不提供具体养护操作建议（如施肥配方、修剪方案）。
