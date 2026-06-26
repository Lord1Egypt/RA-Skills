# API 接口文档

此处用于存放成人面部疲劳/压力指数分析 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动成人面部疲劳/压力指数分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（疲劳/压力指数）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史疲劳指数记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_ADULT_FACIAL_FATIGUE_STRESS_INDEX_ANALYSIS` - 成人面部疲劳/压力指数分析

## 输入约束

- 推荐使用正面、平视、清晰、光照均匀的成人面部图像或 3-10 秒短视频
- 拍摄距离 30-80 cm，五官区域清晰，避免厚重妆容/滤镜干扰
- 适用于智能镜子、办公室健康屏、手机自拍、健康管理 APP

## 关键观测特征

- `eye_bag_area` - 眼袋面积（下眼睑浮肿/阴影面积，归一化）
- `dark_circle_grayscale` - 黑眼圈灰度（眼眶暗沉程度，0-1）
- `mouth_corner_drop_deg` - 嘴角下垂角度（口角与水平线夹角，°）
- `glabellar_frown_lines_score` - 眉间川字纹评分（0-1）
- `skin_dullness_score` - 整体肌肤暗沉度（参考）

## 疲劳/压力指数分级（0-100）

- 0-30 - 状态良好（good）
- 30-50 - 轻度疲劳（mild_fatigue）
- 50-70 - 中度疲劳/压力（moderate_stress）
- 70-100 - 重度疲劳/高压（high_stress）

## 输出字段（参考）

- `face_detected` - 是否检测到正面面部
- `feature_metrics` - 各项面部特征数值（eye_bag_area / dark_circle_grayscale / mouth_corner_drop_deg / glabellar_frown_lines_score / skin_dullness_score）
- `fatigue_stress_score` - 疲劳/压力综合指数（0-100）
- `fatigue_stress_level` - 等级（good / mild_fatigue / moderate_stress / high_stress）
- `top_contributing_features` - 主要贡献特征排序
- `suggestion_hint` - 方向性建议（如"建议补水休息"、"今晚早睡"、"短暂深呼吸/放松训练"）
- `medical_followup_hint` - 医疗复核提示（持续高分建议体检）

> 仅输出基于面部视觉的客观评分与方向性建议，不提供医学诊断或临床压力评估；如长期高分伴明显躯体症状，请咨询专业医生。
