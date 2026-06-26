# API 接口文档

此处用于存放水培植物营养液浓度视觉评估 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动水培营养液浓度评估任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与调整建议
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史评估记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_HYDROPONIC_NUTRIENT_ASSESSMENT_ANALYSIS` - 水培植物营养液浓度视觉评估

## 输入约束

- 推荐分别拍摄根系（透明容器内）与叶片（新叶+老叶）的高清图像
- 拍摄环境建议光照均匀、镜头无水雾，避免反光遮挡根须
- 关键观测特征：
    - 根须颜色（白色健康 / 黄色初期胁迫 / 褐色严重胁迫 / 黑色腐烂）
    - 根尖状态（饱满白尖 / 萎缩 / 发黑）
    - 叶片：叶尖灼伤、叶缘焦枯、叶片黄化、卷曲

## 输出字段（参考）

- `root_color_grade` - 根系颜色等级（healthy / mild_stress / severe_stress / rot）
- `leaf_burn_signs` - 叶片灼伤体征（叶尖灼伤 / 叶缘焦枯 / 黄化 / 卷曲）
- `nutrient_status` - 营养液浓度判断（适宜 / 偏浓 / 偏稀 / 严重过浓 / 严重过稀）
- `adjust_advice` - 调整建议（如"加入清水稀释"、"补充浓缩营养液"、"立即换液并清洗根系"）

> 仅基于视觉特征给出定性结论，不输出具体 EC / ppm 数值。
