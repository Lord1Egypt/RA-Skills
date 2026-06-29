# API 接口文档

此处用于存放爬宠活动量昼夜节律分析 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动爬宠 24h 节律分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（24 小时活动分布 / 高峰时段 / 节律判定）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史节律记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出节律分析报告

## 场景代码

- `SMYX_REPTILE_CIRCADIAN_ACTIVITY_ANALYSIS` - 爬宠活动量昼夜节律分析

## 输入约束

- 摄像头：爬宠箱 / 饲养缸 / 养殖场 / 科研观察固定摄像头（**必须固定机位、固定视野**，避免相机移动污染运动统计）
- 视频时长：**必须 ≥ 24 小时**（覆盖完整昼夜周期）；推荐连续 7 天观察以识别多日趋势
- 分辨率 ≥ 720p；帧率 ≥ 5 FPS（节律分析对帧率要求较低，但需稳定）
- **照明硬约束**：必须配备**红外/IR 夜视摄像头**（夜间无可见光时仍能采集运动），且夜间禁止补可见光（破坏夜行性物种节律）
- 必须录入摄像头时区与视频起止时间（含时区）
- 多缸场景按摄像头 ID + 个体 ID 双重绑定
- **部署时必须录入**：物种（豹纹守宫/鬃狮蜥/壁虎/玉米蛇/球蟒/草龟/苏卡达/睫角守宫等）、**物种自然节律标签**（昼行性 / 夜行性 / 暮晨性 crepuscular）、当前 UVB/灯光开关时刻、温度梯度方案、上次喂食时间、是否处于蜕皮/抱蛋/产卵期

## 关键观测信号

### 24 小时运动统计
- `hourly_activity_array[24]` - **24 小时活动量数组**（核心指标，每小时一个浮点数 0-1，归一化运动像素比例 OR 帧差绝对值之和归一化）
- `total_motion_pixels_24h` - 全天累计运动像素
- `effective_observation_hours` - 有效观察小时数（剔除遮挡/相机离线/暗到无 IR 信号的小时）
- `frame_diff_method` - 帧差算法（abs_diff / mog2 / knn）
- `motion_threshold_used` - 使用的运动检测阈值（用于复现）

### 高峰与节律特征
- `peak_hours_top3` - **活动高峰前 3 时段**（核心指标，如 [22, 23, 0] 表示晚 10 点-午夜 0 点）
- `quiet_hours_top3` - 最沉寂前 3 时段
- `light_period_activity_ratio` - **白天（06:00-18:00）活动量占比**
- `dark_period_activity_ratio` - **夜间（18:00-06:00）活动量占比**
- `crepuscular_window_activity_ratio` - 晨昏（05:00-07:00 + 17:00-19:00）活动量占比

### 节律一致性
- `species_natural_rhythm` - 物种自然节律标签（diurnal_daytime / nocturnal_nighttime / crepuscular_dawn_dusk）
- `observed_rhythm_classified` - 观察到的节律分类
- `rhythm_consistency_score_0_100` - **节律一致性评分 0-100**（核心指标：100 = 与物种自然节律完全一致 / < 50 = 显著颠倒）
- `rhythm_inversion_detected` - 是否检测到昼夜颠倒
- `consecutive_inversion_days` - 连续颠倒天数（多日跟踪）

### 上下文与排除信号
- `is_during_shedding_period` - 是否处于蜕皮期（蜕皮期活动整体下降，非节律紊乱）
- `is_during_brumation_or_hibernation` - 是否处于休眠/冬眠期（冷血动物特有，整体活动接近 0）
- `is_during_gravid_or_egg_laying` - 是否处于抱蛋/产卵期（雌性活动剧增寻找产蛋点）
- `recent_environmental_change` - 近期环境变更（新缸 / 新光照 / 温度调整 < 7 天，应激期活动异常）
- `light_schedule_recorded` - 是否记录灯光开关时刻
- `night_disturbance_detected` - 夜间是否检测到外部光照/振动干扰（人为夜灯 / 路灯射入 / 声响）
- `camera_stable` - 摄像头是否稳定（机位移动会污染帧差）
- `ir_visible_during_dark` - 黑暗时段是否有 IR 视觉
- `observation_signal_acceptable` - 整体观察信号是否合格

## 综合判定

- `rhythm_normal_aligned` - 节律正常（与物种自然节律一致，一致性 ≥ 80）
- `rhythm_mildly_shifted` - 节律轻微偏移（一致性 60-79，活动高峰偏移 1-2 小时）
- `rhythm_moderately_disrupted` - 节律中度紊乱（一致性 40-59，活动分布扁平化或部分颠倒）
- `rhythm_severely_inverted` - **节律严重颠倒**（一致性 < 40，昼行性物种夜间高峰 / 夜行性物种白天高峰）
- `rhythm_context_shedding_or_brumation` - 蜕皮/休眠期上下文，活动整体下降属正常
- `rhythm_context_gravid_or_environmental_change` - 抱蛋/产卵期或近期环境变更，活动异常属临时
- `rhythm_signal_unreliable` - 信号不可靠（观察时长 < 24h / 摄像头机位移动 / 夜间无 IR / 长时间遮挡 / 灯光时刻未录入）

## 4 级提醒策略递进

- Level 1（rhythm_normal_aligned）：仅入库
- Level 2（rhythm_mildly_shifted / rhythm_context_*）：温和提示，建议**继续观察 3-7 天 + 确认灯光时刻是否符合物种推荐 + 排查夜间是否有偶发干扰**
- Level 3（rhythm_moderately_disrupted）：紧急提示，建议**检查光照周期（UVB / 主灯开关时刻）+ 排查夜间光照/声响/振动干扰 + 检查温度梯度是否正确 + 观察食欲精神 + 连续多日跟踪**
- Level 4（rhythm_severely_inverted + 连续 ≥ 3 天）：最高紧急提示，建议**全面排查光照周期与物种推荐是否吻合 + 隔离夜间外部干扰 + 调整光照计时器至物种自然节律 + 若伴随食欲下降或消瘦，建议联系爬宠兽医排查健康问题**

## 单日提醒上限

- Level 1 不限 / Level 2 × 2 / Level 3 × 3 / Level 4 × 5

## 红线约束

- **🚨 禁止**做"昼夜节律失调综合征 / 代谢性骨病 MBD / 抑郁 / 应激反应"等**具体医学诊断**
- **🚨 绝对禁止**输出具体药物名称、剂量、镇静剂品牌、褪黑素剂量、中草药品牌
- **🚨 绝对禁止**输出"自行关闭主灯""自行延长 UVB 时长至 N 小时""自行投喂助眠饲料""自行注射褪黑素"等任何具体环境/医疗指令；**仅建议用户检查并按物种手册调整**
- **🚨 严禁伪造或夸大活动量数据**；所有数据必须基于真实帧差/光流统计；统计窗口、阈值、算法必须可复现
- **禁止**长期存储完整爬宠箱 24h 视频（≤ 14 天，留每小时活动量数组 + 节律事件关键截图；养殖场/科研按管理规定）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户启停灯光计时器 / UVB / 加热垫 / 喷雾；任何环境控制变更必须由用户确认（仅可建议）
- 必须考虑生理性上下文：**蜕皮期 / 休眠/冬眠期 / 抱蛋产卵期 / 近期环境变更 < 7 天** → 必须排除非节律紊乱混淆
- 物种自然节律基线必须录入：**昼行性**（鬃狮蜥/绿鬣蜥/草龟/苏卡达） / **夜行性**（豹纹守宫/壁虎/玉米蛇/球蟒/睫角守宫） / **暮晨性**（部分蛇类）→ 严禁用通用节律盲判
- 夜间禁止补可见光评估夜行性物种（必须使用 IR 红外，否则信号 unreliable）
- 摄像头机位移动 / 长时间遮挡 / 观察时长 < 24h / 夜间无 IR 视觉 / 灯光开关时刻未录入 → 必须返回 `rhythm_signal_unreliable`
- 必须告知用户：AI 节律分析仅供参考，**持续异常或伴随明显健康征兆需联系专业爬宠兽医（可能涉及代谢性疾病 / 神经系统问题）**

## 输出报告字段

- `report_date`、`enclosure_id`、`individual_id`、`species`、`species_natural_rhythm`、`hourly_activity_array[24]`、`peak_hours_top3`、`quiet_hours_top3`、`light_period_activity_ratio`、`dark_period_activity_ratio`、`rhythm_consistency_score_0_100`、`rhythm_inversion_detected`、`consecutive_inversion_days`、`composite_scene`、`alert_level`、`recommended_actions`（检查光照周期 / 排查夜间干扰 / 调整光照计时器至物种自然节律 / 检查温度梯度 / 观察食欲精神 / 联系爬宠兽医，**不含具体药物/具体灯光时刻数字/具体投喂物**），`disclaimer`
