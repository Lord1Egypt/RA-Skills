# API 接口文档

此处用于存放鱼类聚集/离群行为识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动鱼类聚集/离群行为识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取离群检测结果（离群个体清单 + 离群距离 + 持续时长）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史离群行为报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出离群行为报告
5. （可选）`/web/companion/v2/trigger-soothing-action` - 触发联动提醒（用户 APP 推送 / 智能鱼缸告警灯 / 提示隔离至检疫缸建议）

## 场景代码

- `SMYX_FISH_ISOLATION_DETECTION_ANALYSIS` - 鱼类聚集/离群行为识别

## 输入约束

- 摄像头：鱼缸固定摄像头 / 养殖池上方摄像头 / 检疫缸全景摄像头，建议**俯拍或大角度斜视**（保证 2D 位置投影稳定）
- 分辨率 ≥ 720p；**帧率 ≥ 10 FPS**（位置跟踪需稳定）
- 光照：建议鱼缸照明开启 + 无强反光；水质清澈（浑浊度低）
- **核心采样窗口**：连续观察 ≥ 1 小时（用户可配置 30 分钟 - 24 小时滚动窗口）
- 视野约束：必须覆盖整个鱼缸/养殖池**完整水平投影**（任何 dead zone 都可能误判为"离群"）
- 多鱼缸/池场景按摄像头 ID 绑定到注册容器 ID
- **多鱼场景必须接入 ReID**（多目标跟踪 + 重识别），每条鱼建立稳定 fish_id
- **部署时必须录入**：鱼种清单、群体大小 N（用户输入或首次自动统计取众数）、每条鱼体长校准（像素 ↔ cm，可单次手动校准或自动学习）
- 用户必须授权部署；公共水族馆 / 养殖场需公示告知

## 关键观测信号

### 群体几何信号
- `tracked_fish_count` - 当前帧成功跟踪到的鱼数
- `total_fish_count_baseline` - 容器注册总鱼数（基线）
- `school_centroid_xy` - 鱼群质心（所有鱼 2D 位置均值）
- `school_dispersion_score` - 群体分散度（所有鱼到质心距离的标准差，体长归一化）
- `school_compactness_score` - 群体紧密度（0-100，越高越紧密；夜行鱼休息时自然偏低）

### 个体离群信号（每条 fish_id 独立）
- `fish_id` - 个体唯一标识（ReID 输出）
- `fish_body_length_px` - 该鱼当前体长（像素，自动估计）
- `fish_position_xy` - 该鱼当前 2D 位置
- `distance_to_centroid_body_lengths` - 与质心欧氏距离（**以体长为单位**，核心指标）
- `over_threshold_flag` - 是否超过阈值（默认 > 10 倍体长）
- `over_threshold_duration_min` - 持续超阈时长（分钟，跨帧累计）

### 上下文信号（避免误报）
- `is_natural_solitary_species` - 是否独居鱼种（斗鱼 / 大型龙鱼 / 部分慈鲷天然独居）
- `is_breeding_period` - 是否繁殖期（公鱼护卵 / 母鱼离群产卵）
- `is_territory_corner_fish` - 是否为领地型缸角守卫鱼（"离群"实为正常占地）
- `is_during_feeding` - 是否在投喂窗口内（短时聚拢/分散为生理性）
- `tank_has_strong_water_flow` - 是否有强水流区（被冲到角落可能误判）
- `tank_temperature_gradient_detected` - 是否检测到温度不均（鱼可能聚于舒适温区，余者"离群"）

## 综合判定

- `schooling_normal` - 群体正常聚集
- `schooling_loose` - 群体偏松散（但无明显离群个体）
- `isolation_short` - 短时离群（> 10 倍体长但 < 1 小时）
- `isolation_persistent` - **持续离群**（> 10 倍体长且 ≥ 1 小时，核心告警场景）
- `isolation_corner_stuck` - 角落呆滞（离群 + 长时间几乎不动，疑似严重不适）
- `multiple_isolated_individuals` - 多鱼同时离群（疑似全缸应激 / 水质恶化）
- `isolation_signal_unreliable` - 信号不可靠（ReID 断裂 / 视野遮挡 / 浑浊度过高 / 跟踪 < 80% 鱼数）

## 4 级告警策略递进

- Level 1（isolation_short / schooling_loose）：仅入库或用户 APP 轻提醒"观察某条鱼是否长期离群"
- Level 2（isolation_persistent，单条）：用户 APP 重要告警，建议**目视检查该鱼体表 / 游姿 / 呼吸 / 摄食活跃度**，并**评估是否隔离至检疫缸**
- Level 3（isolation_corner_stuck / 连续 ≥ 2 日 isolation_persistent）：紧急告警，**强烈建议立即隔离至检疫缸 + 检查水质（溶氧/pH/氨氮/温度梯度）**，并提示联系**当地观赏鱼兽医**
- Level 4（multiple_isolated_individuals / 同缸 ≥ 3 条同时持续离群）：最高紧急告警 + 推送家庭/管理人员所有联系人 + 强烈建议**立即全面排查（水质 + 体表 + 游姿 + 呼吸 + 摄食）+ 联系专业人员**

## 单日告警上限

- Level 1 不限 / Level 2 × 6 / Level 3 × 3 / Level 4 不设上限

## 红线约束

- **禁止**做"寄生虫 / 细菌感染 / 鳃病 / 肠炎 / 应激综合征"等具体疾病诊断
- **禁止**输出具体药物名称、剂量、给药方案
- **禁止**长期存储完整鱼缸/养殖池视频（≤ 7 天，仅入库离群事件片段与轨迹摘要；公共水族馆/养殖场按管理规定）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户启停隔离泵 / 加热棒 / 换水 / 投药 / 灯光参数；任何水族设备控制变更必须由用户确认（仅可建议）
- 离群距离、持续时长、群体分散度等指标必须基于真实视频帧跟踪；**禁止伪造或夸大指标**
- 鱼种特异性：**独居鱼种（斗鱼 / 大型龙鱼 / 部分慈鲷）天然不集群** → 必须按鱼种基线判定；**禁止使用通用 10 倍体长阈值盲判独居鱼种**
- 必须考虑生理性离群上下文：**繁殖期护卵 / 母鱼产卵 / 领地型缸角守卫 / 投喂前后短时聚拢分散 / 强水流区被冲 / 温度梯度造成的舒适区聚集** → 不可直接告警
- **必须**在 ReID 跟踪率 < 80% 或视野遮挡严重时返回 `isolation_signal_unreliable`，并建议重拍 / 调整摄像头角度；**禁止给出不可靠告警**
- 必须告知用户：AI 行为识别仅供参考，**最终诊断与治疗方案需专业水族兽医确认**

## 输出报告字段

- `report_date` - 报告日期
- `tank_id` - 鱼缸/养殖池/检疫缸 ID
- `species` - 鱼种
- `total_fish_count_baseline` - 注册总鱼数
- `school_compactness_score` - 群体紧密度
- `isolated_fish_list` - 离群个体清单（每条含 fish_id / distance_to_centroid_body_lengths / over_threshold_duration_min / 缩略图轨迹）
- `composite_scene` - 综合判定
- `alert_level` - 告警等级
- `recommended_actions` - 建议动作（观察 / 隔离检疫缸 / 检查水质 / 联系兽医，**不含药物**）
- `disclaimer` - 免责声明
