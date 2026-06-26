# API 接口文档

此处用于存放新生儿黄疸筛查（面部皮肤颜色）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动新生儿黄疸筛查任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取黄疸风险分析结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史筛查记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_NEONATAL_JAUNDICE_SCREENING_ANALYSIS` - 新生儿黄疸筛查（面部皮肤颜色）

## 输入约束

- 设备：新生儿监护器 / 婴儿摄像头 / 手机后置摄像头
- 图像/视频要求：高清、正面、五官清晰、面部完整可见
- **光照要求**：自然白光最佳；**严禁使用偏色 LED 光（黄光夜灯、暖光等会引起严重误判）**
- 拒绝厚妆 / 滤镜；新生儿建议在喂奶或安静状态下采集
- 视频时长 3-10 秒 或 单张 1-3 MB 高清图均可
- 推荐附带可见参考色卡放在面颊旁，便于颜色校正（白平衡校准）

## 关键观测特征

- `face_visible` - 是否检测到清晰新生儿面部
- `sclera_visible` - 巩膜（眼白）是否可见
- `sclera_yellowness_index` - 巩膜黄染指数（0-1，越大越黄）
- `skin_yellowness_index` - 面部皮肤黄染指数（基于色度空间 Lab b* 通道 / YCbCr 色度偏移）
- `skin_color_lab_b` - 皮肤 Lab b* 通道值（反映黄-蓝偏向）
- `estimated_bilirubin_mg_dl` - 估算胆红素水平（mg/dL，仅参考）
- `light_quality_score` - 光照质量评分（low / medium / high，过低时不出具风险）
- `color_card_calibrated` - 是否进行了色卡白平衡校准

## 风险等级分级

- `low_risk` - 低风险（皮肤/巩膜无明显黄染）
- `medium_risk` - 中风险（建议门诊经皮胆红素或血清胆红素复测）
- `high_risk` - 高风险（建议**立即就医复测**，警惕高胆红素血症 / 核黄疸风险）
- `inconclusive` - 不确定（光照差 / 面部遮挡 / 巩膜不可见等，无法出具结论）

## 默认阈值（可由调用方覆盖）

- 中风险：`skin_yellowness_index ∈ [0.30, 0.55]` 或 `sclera_yellowness_index ∈ [0.20, 0.40]`
- 高风险：`skin_yellowness_index > 0.55` 或 `sclera_yellowness_index > 0.40`
- 光照质量阈值：light_quality_score < 0.4 → 强制返回 `inconclusive`

## 输出字段（参考）

- `infant_detected` / `face_visible` / `sclera_visible`
- `feature_metrics` - 黄染相关特征（sclera_yellowness_index / skin_yellowness_index / skin_color_lab_b / estimated_bilirubin_mg_dl）
- `light_quality_score` / `color_card_calibrated`
- `jaundice_risk_level` - 风险等级（low_risk / medium_risk / high_risk / inconclusive）
- `risk_confidence` - 置信度（0-1）
- `recommended_action` - 建议动作（home_observe / clinic_recheck / urgent_hospital_visit / recapture_better_light）
- `alert_message` - 推送给家长的文本（如"宝宝面部黄染指数 0.62，巩膜可见明显黄色，建议尽快前往新生儿科复测胆红素"）

> 仅输出基于视觉的黄疸风险初筛提示，**不替代** 经皮胆红素仪 / 血清胆红素 / 医生面诊；中高风险务必尽快就医，由专业医生评估并制定干预方案。
