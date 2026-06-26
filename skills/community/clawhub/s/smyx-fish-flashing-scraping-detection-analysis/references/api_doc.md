# API 接口文档

此处用于存放鱼类擦缸/蹭底行为识别（外寄）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动鱼类擦缸/蹭底外寄风险识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取预警结果（摩擦频次 / 持续时长 / 接触位置 / 涉及鱼数）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史预警报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出预警报告
5. （可选）`/web/companion/v2/trigger-soothing-action` - 触发联动告警（用户 APP 推送 / 建议立即体表+鳃部检查 / 准备隔离检疫缸）

## 场景代码

- `SMYX_FISH_FLASHING_SCRAPING_DETECTION_ANALYSIS` - 鱼类擦缸/蹭底行为识别（外寄）

## 输入约束

- 摄像头：鱼缸固定摄像头 / 检疫缸专用摄像头 / 养殖池水下摄像头，**必须同时覆盖缸壁、底砂、造景石全景**（任何盲区可能漏判）
- 分辨率 ≥ 720p；**帧率 ≥ 25 FPS**（擦缸是高速瞬时动作，鱼体侧身闪动 < 0.5s）
- 光照：建议鱼缸照明常开 + 无强反光；底砂区域光线足够（暗区漏检率高）
- **核心采样窗口**：默认 1 分钟滚动窗口（频次统计单位），触发预警需 ≥ 10 秒持续观察
- 视野约束：必须覆盖**缸壁侧面 + 底砂全面 + 主要造景石**
- 多鱼缸/池场景按摄像头 ID 绑定到注册容器 ID
- **部署时必须录入**：鱼种、缸内总鱼数 N、缸底材质（裸缸 / 细砂 / 粗砂 / 火山石 / 水草泥）、造景石位置
- 用户必须授权部署；公共水族馆 / 养殖场需公示告知

## 关键观测信号

### 擦缸（Flashing - 侧身蹭缸壁）信号
- `flashing_events_count_per_minute` - **每分钟擦缸事件数**（核心指标）
- `flashing_event_duration_ms_avg` - 单次擦缸动作平均时长（毫秒，典型 100-500ms）
- `flashing_body_axis_tilt_deg_avg` - 鱼体翻身角度均值（侧身擦缸通常 60-90 度）
- `flashing_contact_surface` - 接触面（front_glass / side_glass / back_glass）
- `flashing_burst_speed_normalized` - 爆发速度归一化（典型加速度高于游动 2-3 倍）

### 蹭底（Scraping - 腹部/侧面蹭底砂）信号
- `scraping_events_count_per_minute` - **每分钟蹭底事件数**（核心指标）
- `scraping_event_duration_ms_avg` - 单次蹭底动作平均时长
- `scraping_body_contact_area` - 接触部位（abdomen / lateral_left / lateral_right / gill_cover）
- `scraping_substrate_type` - 接触底材类型（sand / gravel / decorative_rock / aquatic_plant）
- `scraping_repeated_at_same_spot` - 是否在同一位置反复蹭（强信号）

### 综合摩擦统计
- `total_friction_events_per_minute` - **总摩擦事件数（擦缸 + 蹭底）/ 分钟**（核心阈值 ≥ 5 次/分钟）
- `friction_persistent_duration_seconds` - **频繁摩擦持续时长**（核心阈值 ≥ 10 秒）
- `affected_fish_count` - 涉及摩擦行为的鱼数
- `affected_fish_ratio` - 涉及鱼数占总鱼数比例
- `cross_fish_synchronicity_score` - 多鱼同步异常评分（多鱼同时擦缸 → 全缸寄生虫怀疑度高）

### 上下文与排除信号（避免误报）
- `is_during_feeding` - 是否在投喂窗口内（争食可能短暂撞缸）
- `is_during_courtship_or_spawning` - 是否在繁殖期（求偶/产卵时鱼可能贴底/蹭石）
- `is_substrate_cleaning_species` - 是否食底栖型鱼种（鼠鱼/异型鱼/底栖鱼天然贴底觅食）
- `tank_recently_disturbed` - 鱼缸是否近期受外部惊吓（换水/搬家短暂应激）
- `water_temperature_change_detected` - 水温是否近期突变（应激）

## 综合判定

- `friction_normal` - 摩擦行为正常（≤ 2 次/分钟，零星活动）
- `friction_low_baseline` - 低频摩擦（3-4 次/分钟，可能为底栖鱼正常或轻度不适）
- `friction_warning_mild` - **摩擦预警轻度**（5-7 次/分钟，持续 ≥ 10s，触发预警门槛）
- `friction_warning_severe` - **摩擦预警严重**（≥ 8 次/分钟，持续 ≥ 30s，**强烈外寄怀疑**）
- `friction_whole_tank_outbreak` - **全缸爆发**（≥ 50% 鱼同时频繁摩擦，**全缸寄生虫爆发风险**）
- `friction_courtship_or_substrate_species` - 繁殖期/底栖鱼正常行为（不告警）
- `friction_signal_unreliable` - 信号不可靠（光照不足 / 跟踪率 < 80% / 视野盲区 / 帧率 < 25 FPS）

## 4 级告警策略递进

- Level 1（normal / low_baseline / courtship_or_substrate_species）：仅入库或不提示
- Level 2（warning_mild）：重要提示，建议**立即近距离观察鱼体表（白点 / 充血 / 黏液增多）+ 鳃部颜色 + 食欲变化**
- Level 3（warning_severe，单次）：紧急告警，建议**立即体表 + 鳃部 + 鳍条全面观察 + 测水质 NH3/NO2-/pH/温度 + 准备隔离检疫缸 + 联系当地观赏鱼兽医**（**禁止推荐具体寄生虫药品**）
- Level 4（whole_tank_outbreak / warning_severe 持续 ≥ 24 小时）：**🚨 最高紧急告警 + 推送所有管理人员** + 强烈建议**立即隔离全缸 + 测水质五项 + 联系专业兽医现场检疫（外寄虫体鉴定需镜检，AI 视觉无法替代）**

## 单日告警上限

- Level 1 不限 / Level 2 × 4 / Level 3 × 6 / Level 4 **不设上限**（外寄爆发可几天内全军覆没）

## 红线约束

- **🚨 禁止**做"小瓜虫病 / 白点病 / 车轮虫病 / 三代虫病 / 指环虫病 / 锚头蚤病"等**具体寄生虫病确诊**（外寄虫体鉴定必须显微镜镜检，AI 视觉仅可输出"行为预兆/外寄风险"）
- **🚨 绝对禁止**输出具体药物名称、剂量、给药方案（**严禁推荐甲硝唑、敌百虫、硫酸铜、孔雀石绿、戊二醛、福尔马林、亚甲基蓝等任何抗寄生虫药剂**）
- **🚨 绝对禁止**输出"升温至 30℃ 治疗白点病""加盐 0.3% 治疗"等具体疗法（任何疗法剂量必须由兽医现场判断）
- **禁止**长期存储完整鱼缸视频（≤ 7 天，仅入库摩擦事件片段；公共水族馆/养殖场按管理规定）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户启停加热棒 / 增氧 / 换水 / 投药 / 灯光参数；任何水族设备控制变更必须由用户确认（仅可建议）
- 摩擦频次 / 持续时长 / 涉及鱼数等指标必须基于真实视频帧分析；**禁止伪造或夸大指标**
- 鱼种特异性：**底栖鱼种**（鼠鱼 / 异型鱼 / 清道夫 / 部分鳉鱼） 天然贴底觅食、**繁殖期**（七彩 / 鹦鹉 / 慈鲷类）贴底/蹭石产卵预备 → 必须按鱼种和生理周期基线判定；**严禁通用阈值盲判底栖鱼为外寄**
- 必须考虑生理性上下文：**投喂窗口争食撞缸 / 换水后短暂应激 / 水温骤变 / 新鱼入缸适应期** → 不可直接告警
- 光照不足 / 跟踪率 < 80% / 视野盲区（缸壁背面 / 底砂死角）/ 帧率 < 25 FPS → 必须返回 `friction_signal_unreliable` 并建议补光/调整摄像头
- 必须告知用户：AI 视觉识别仅供参考，**外寄虫体最终确诊与处理需用户立即观察体表并由专业兽医镜检**

## 输出报告字段

- `report_date` - 报告日期
- `tank_id` - 鱼缸/养殖池 ID
- `species` - 鱼种
- `total_fish_count_baseline` - 注册总鱼数
- `substrate_type` - 缸底材质
- `flashing_events_count_per_minute` - 擦缸频次
- `scraping_events_count_per_minute` - 蹭底频次
- `total_friction_events_per_minute` - 总摩擦频次
- `friction_persistent_duration_seconds` - 频繁摩擦持续时长
- `affected_fish_count` - 涉及鱼数
- `cross_fish_synchronicity_score` - 多鱼同步评分
- `composite_scene` - 综合判定
- `alert_level` - 告警等级
- `recommended_actions` - 建议动作（体表观察 / 鳃部观察 / 测水质 / 准备隔离检疫缸 / 联系兽医镜检，**绝不含具体药物、剂量、品牌、温度疗法、加盐剂量**）
- `disclaimer` - 免责声明
