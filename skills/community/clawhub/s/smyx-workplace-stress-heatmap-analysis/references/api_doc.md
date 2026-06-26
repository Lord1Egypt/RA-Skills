# API 接口文档

此处用于存放职场员工压力群体热力图 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动职场员工压力群体热力图任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取区域级群体压力指数 + 热力图结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史热力图记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告（含伪彩色热力图）

## 场景代码

- `SMYX_WORKPLACE_STRESS_HEATMAP_ANALYSIS` - 职场员工压力群体热力图

## 输入约束

- 摄像头：企业开放式办公区 / 研发中心 / 客服中心固定摄像头，高位俯视或斜俯视，**画面应覆盖多个工位区域**
- 帧率 ≥ 2 FPS 即可（群体趋势分析无需高帧率）；分辨率 ≥ 720p；光照稳定
- 初次部署需在画面中**框选多个工位区域 ROI**（zone_id + zone_label，如 zone_A / zone_B / zone_C）
- 视频时长建议 ≥ 5 分钟，单点采样不足以反映群体趋势
- **强匿名约束**：不允许启用人脸识别 / 人脸比对 / 身份关联，**仅输出区域级聚合统计**

## 关键观测信号（区域级聚合，绝不绑定个人）

- `zone_id` / `zone_label` - 工位区域
- `person_count_in_zone` - 区域内可观测员工数（≥ 阈值才输出有效结果，避免单人识别）
- `facial_tension_score` - 区域内面部紧张特征均值（皱眉 + 嘴角下垂综合，0-1）
- `posture_rigidity_score` - 区域内姿态僵硬度（长时间保持同姿势 / 肩部耸起，0-1）
- `eye_rubbing_event_count_hourly` - 揉眼事件次数（疲劳信号，区域汇总）
- `forward_leaning_ratio` - 前倾坐姿比例
- `stress_index` - 综合群体压力指数（0-100，越高越紧张）
- `heatmap_color` - 伪彩色（green / yellow_green / yellow / orange / red）

## 阈值与等级

- `0-40` - 低压力（green）
- `40-60` - 中等压力（yellow_green / yellow）
- `60-80` - 高压力（orange）
- `80-100` - 极高压力（red）→ 触发管理者预警
- 单区域 `person_count_in_zone < 3` 时仅输出 "insufficient_sample"，不输出 stress_index（避免单人识别）

## 输出字段（参考）

- `time_window` - 采样时间窗口（如 "2026-05-23 14:00 ~ 15:00"）
- `zones` - 区域聚合数组（zone_id / zone_label / person_count_in_zone / facial_tension_score / posture_rigidity_score / eye_rubbing_event_count_hourly / forward_leaning_ratio / stress_index / heatmap_color）
- `office_overall_stress_index` - 整个办公区综合压力指数
- `top_pressure_zones` - 当前压力指数最高的若干区域
- `trend_vs_last_window` - 相比上一时间窗的变化（delta_pct）
- `alert_type` - 提醒类型（zone_high_stress / overall_high_stress / improving / normal）
- `alert_level` - 提醒级别（info / notice / warning）
- `manager_suggestion` - 管理者建议（如"zone_B 连续 3 个时段高压力，建议关注负责的项目排期、增加短茶歇"）
- `heatmap_image_url` - 伪彩色热力图 URL（叠加在办公区平面图上）

## 强制隐私约束

- ❌ **禁止**进行人脸识别 / 人脸比对 / 个人身份绑定
- ❌ **禁止**输出"某员工压力高"这类个体结论
- ❌ **禁止**长期存储原始视频或可识别个人特征的数据
- ✅ 仅输出**区域级聚合统计**与**热力图色块**
- ✅ 必须在部署前**面向全体员工公示并取得知情同意**，建议由 HR + 工会双方备案

> 仅输出基于视觉的群体行为聚合统计与友好提醒，**不提供员工个人心理诊断、绩效评价或任何个人画像**；任何针对个体的关怀沟通应由 HR / 直属经理依据自愿性问卷和访谈进行。
