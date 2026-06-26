# API 接口文档

此处用于存放观赏鱼体色鲜艳度评估 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动观赏鱼体色鲜艳度评估任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取评估结果（HSV-S/V 均值 + 鲜艳度评分 + 品种基线对比）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史评估报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出鲜艳度时间序列报告
5. （可选）`/web/companion/v2/trigger-soothing-action` - 触发联动提醒（用户 APP 推送 / 建议调整饲料/光照/水质）

## 场景代码

- `SMYX_FISH_COLOR_BRIGHTNESS_ASSESSMENT_ANALYSIS` - 观赏鱼体色鲜艳度评估

## 输入约束

- 摄像头：鱼缸固定摄像头 / 智能鱼缸内置摄像头 / 手机拍摄（侧面，垂直于鱼体侧面方向）
- 分辨率 ≥ 1080p（颜色饱和度评估需高色彩精度）
- **关键硬件要求**：**视野内必须放置已知白色参考物（白卡 / 灰卡 / 标准 ColorChecker）**，用于做**白平衡校正**与**光照归一化**（核心，否则环境灯光偏色会让评分失真）
- 拍摄角度：**鱼体侧面**（评估躯干主区域颜色），鱼体应位于视野中央，与背景对比清晰
- 光照：建议鱼缸照明常开 + **使用 5000-6500K 中性白光源**
- 鱼体拍摄时应**短暂静止**
- 多鱼缸场景按摄像头 ID 绑定到注册容器 ID
- **部署时必须录入**：鱼种 + 品系（决定标准色度数据库匹配，如锦鲤红白/大正三色/昭和三色、金鱼狮子头/兰寿、神仙鱼银河系/熊猫、孔雀鱼礼服/草尾、热带龙鱼红/金/青）
- 用户必须授权部署；公共养殖场 / 水族馆需公示告知

## 关键观测信号

### 白平衡校正与光照归一化（核心）
- `white_reference_type` - 白参考类型（white_card / gray_card / colorchecker / not_detected）
- `white_reference_detection_confidence` - 白参考检测置信度（0-1）
- `light_temperature_kelvin_estimated` - 估算光照色温（K）
- `wb_correction_applied` - 是否已做白平衡校正（bool）
- `light_intensity_normalized_score` - 光照强度归一化评分

### 鱼体区域分割
- `fish_id` - 鱼个体唯一标识（可选）
- `species_subtype` - 鱼种 + 品系（精确到子品系，如"锦鲤-大正三色"）
- `body_segmentation_mask_pixel_count` - 鱼体分割掩膜像素数
- `body_segmentation_confidence` - 分割置信度（0-1）
- `analysis_roi` - 分析区域（默认 trunk_middle，可选 head / dorsal / caudal_fin）

### HSV 色彩信号（核心）
- `hsv_s_mean` - 躯干区域**饱和度均值**
- `hsv_s_std` - 饱和度标准差
- `hsv_v_mean` - 躯干区域**亮度均值**
- `hsv_v_std` - 亮度标准差
- `hsv_h_dominant_hue_deg` - 主色相（0-360）
- `hsv_h_distribution_histogram` - 色相分布直方图（用于多色品种如锦鲤"红/白/黑"分区比例）

### 品种基线对比
- `species_subtype_baseline_s_range` - 该品系健康标准饱和度范围
- `species_subtype_baseline_v_range` - 该品系健康标准亮度范围
- `species_subtype_baseline_h_target_palette` - 该品系标准色相调色板
- `color_palette_match_score` - 与标准调色板的匹配度（0-100）
- `s_baseline_z_score` - 饱和度相对基线的 z-score
- `v_baseline_z_score` - 亮度相对基线的 z-score

### 鲜艳度综合评分
- `vibrancy_score_0_100` - **鲜艳度综合评分（0-100，核心输出）**
- `vibrancy_score_trend_7d` - 近 7 天评分变化趋势
- `vibrancy_score_trend_30d` - 近 30 天评分变化趋势

## 综合判定

- `color_vibrant_excellent` - 鲜艳度极佳（≥ 85）
- `color_vibrant_good` - 鲜艳度良好（70-84）
- `color_acceptable` - 可接受（50-69）
- `color_dull_mild` - **体色暗淡轻度**（35-49）
- `color_dull_severe` - **体色暗淡严重**（< 35）
- `color_baseline_unavailable` - 该品系暂无标准基线（仅输出客观 HSV 值，不评分鲜艳度）
- `color_signal_unreliable` - 信号不可靠（白参考未检出 / 分割置信度 < 0.7 / 光照过暗或过曝 / 鱼体姿态侧面不可见）

## 4 级提醒策略递进（侧重养殖管理建议，非疾病诊断）

- Level 1（excellent / good）：仅入库 + 积极反馈"鲜艳度优秀，继续保持当前管理方式"
- Level 2（acceptable / dull_mild）：重要提示，建议**评估增色饲料（中性提示"含虾青素/螺旋藻类"，禁止具体品牌）/ 检查光照（光谱完整性 + 色温 + 周期）/ 检查水质（NH3/NO2-/pH/KH）**
- Level 3（dull_severe，单次）：紧急提示，建议**立即检查体表 + 游姿 + 摄食活跃度 + 水质五项 + 投喂记录**，并联系**当地观赏鱼兽医或资深玩家**
- Level 4（dull_severe 连续 ≥ 14 天 / 同缸 ≥ 50% 个体同时严重暗淡）：最高紧急提示 + 推送所有管理人员 + 强烈建议**全面排查**

## 单日提醒上限

- Level 1 不限 / Level 2 × 2 / Level 3 × 2 / Level 4 不设上限

## 红线约束

- **🚨 禁止**做"营养不良 / 黑斑病 / 黑变病 / 寄生虫 / 应激综合征 / 缺乏类胡萝卜素"等**具体疾病诊断**
- **🚨 绝对禁止**输出具体药物名称、剂量、给药方案
- **🚨 绝对禁止**输出具体饲料品牌名称、增色剂品牌（仅可中性提示"含虾青素/螺旋藻类增色饲料"，**禁止推荐 X 牌增色粒**）
- **禁止**长期存储完整鱼缸视频/图像（≤ 30 天，留鲜艳度时间序列 + 关键评估帧）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户启停加热棒 / 增氧 / 换水 / 喂食器 / 灯光参数；任何水族设备控制变更必须由用户确认
- HSV-S/V 值、鲜艳度评分等指标必须基于真实图像计算；**禁止伪造或夸大评分**
- 品系特异性：不同品系标准色度差异极大（锦鲤红白要求红色 S>200/白色高亮，昭和要求黑色覆盖度，神仙鱼银河系要求斑点分布而非饱和度）→ 必须**按 species_subtype 精确匹配基线**；**严禁通用阈值盲判**
- 必须考虑光照与白平衡上下文：暖光（< 4000K）让黄/红偏强、冷光（> 7000K）让蓝/绿偏强、**未做白平衡的评分一律视为不可信**
- 必须考虑生理性上下文：**繁殖期婚姻色加深 / 应激色暂时暗淡 / 投喂后短时增色 / 鱼龄增长色彩自然渐变** → 不可直接告警
- 白参考未检出 / 分割置信度 < 0.7 / 光照过暗或过曝 / 鱼体姿态侧面不可见 → 必须返回 `color_signal_unreliable` 并建议重拍/补光/放置白卡

## 输出报告字段

- `report_date` - 报告日期
- `tank_id` - 鱼缸 ID
- `species_subtype` - 鱼种 + 品系
- `fish_id` - 鱼个体（可选）
- `white_balance_calibration` - 白平衡校正信息
- `body_roi` - 分析区域
- `hsv_values` - HSV 核心值
- `species_subtype_baseline_comparison` - 品系基线对比
- `vibrancy_score_0_100` - **鲜艳度综合评分**
- `vibrancy_trend_7d` / `vibrancy_trend_30d` - 近期趋势
- `composite_scene` - 综合判定
- `alert_level` - 提醒等级
- `recommended_actions` - 建议动作（评估增色饲料/光照/水质 / 检查体表 / 联系兽医，**不含药物与品牌**）
- `disclaimer` - 免责声明
