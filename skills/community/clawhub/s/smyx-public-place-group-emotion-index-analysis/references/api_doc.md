# API 接口文档

此处用于存放公共场所群体情绪指数（展览/商场） API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动公共场所群体情绪指数分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取群体情绪分布 + 情绪指数 + 运营/安全建议
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史群体情绪报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告（含情绪分布堆叠图 / 区域热力图）

## 场景代码

- `SMYX_PUBLIC_PLACE_GROUP_EMOTION_INDEX_ANALYSIS` - 公共场所群体情绪指数（展览/商场）

## 输入约束

- 摄像头：商场出入口 / 收银区 / 主动线 / 展厅 / 候机厅 / 售票处等公共场所高位固定摄像头，能拍到顾客**正面或斜侧脸**
- 帧率 ≥ 5 FPS（推荐 10 FPS）；分辨率 ≥ 720p；光照稳定避免逆光
- 视频时长建议 ≥ 10 分钟，覆盖完整客流时段，过短样本无法稳定计算群体指数
- ROI 标定：可按区域划分多个子区域（如入口 / 收银 / 展品 A / 展品 B）以输出区域级情绪指数
- 多视角部署时建议每个区域至少 1 路摄像头
- **强匿名约束**：仅做匿名表情聚合统计，**禁止**人脸识别 / 人脸比对 / 身份绑定 / 跨摄像头跟踪

## 关键观测信号

- `face_detected_count` - 当前帧检测到的人脸数
- `emotion_distribution` - 6 类情绪分布（happy / calm / irritated / surprised / sad / fearful 占比）
- `positive_ratio` - 积极情绪占比（happy + calm）
- `negative_ratio` - 消极情绪占比（irritated + sad + fearful）
- `irritation_ratio` - 烦躁情绪占比（**安全预警关键指标**）
- `group_emotion_index` - 群体情绪指数（0-100，数值越高代表群体情绪越积极）
- `crowd_density_estimate` - 人群密度估计（参考指标，与烦躁占比联合判定）
- `dwell_time_estimate_sec` - 平均停留时长估计（展品/区域吸引力参考）

## 阈值与等级

- `≥ 70` - 群体情绪积极（positive）
- `50-69` - 群体情绪平稳（neutral）
- `30-49` - 群体情绪低落（low）→ 建议优化服务
- `< 30` 或 `irritation_ratio > 25%` - 群体情绪偏负面（negative）→ 推送运营优化或安全预警
- 最小样本保护：`face_detected_count < 5` 时输出 `insufficient_sample`，不发布群体指数

## 输出字段（参考）

- `time_window` / `place_type`（mall / exhibition / scenic_area / airport / museum / theme_park / other）
- `face_detected_count` / `crowd_density_estimate` / `dwell_time_estimate_sec`
- `emotion_distribution` / `positive_ratio` / `negative_ratio` / `irritation_ratio`
- `group_emotion_index` / `emotion_level` (positive / neutral / low / negative)
- `region_breakdown` - 区域级情绪指数数组（[{region_name, group_emotion_index, irritation_ratio, ...}]）
- `trend_vs_last_window` - 与上一时间窗变化（delta_pct）
- `alert_type` - 提醒类型（operation_optimize / safety_warning / improving / normal）
- `alert_level` - 提醒级别（info / notice / warning）
- `operation_suggestion` - 运营建议（如"收银区烦躁占比 32%、平均停留 4 分钟，建议增开 1 个收银台"）
- `safety_suggestion` - 安全建议（如"入口区域烦躁占比 38% 且密度偏高，建议增派 1 名安保安抚分流"）
- `emotion_heatmap_image_url` - 情绪指数区域热力图 URL（伪彩色叠加在场景平面图）

## 强制约束与红线

- ❌ **禁止**进行人脸识别 / 人脸比对 / 顾客身份绑定 / 跨摄像头身份跟踪
- ❌ **禁止**长期存储顾客原始视频或可识别人脸特征向量
- ❌ **禁止**将群体情绪结果用于针对个体顾客的差异化定价或服务歧视
- ✅ 仅输出**区域级匿名聚合**指标，作为运营优化与安全预警辅助参考
- ✅ 部署场所必须以**显著标识**告知公众使用了匿名情绪分析摄像头，并提供咨询联系方式
- ✅ 数据保存期限建议 ≤ 30 天，仅保留聚合指标，不保留原始视频

> 仅输出基于视觉的群体情绪聚合统计与运营/安全辅助参考，**不构成对任何个体顾客的情绪诊断或行为评价**；任何针对个体的服务调整必须经过当事人本人主动反馈与同意。
