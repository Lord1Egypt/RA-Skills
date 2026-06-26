# API 接口文档

此处用于存放水族箱内氨氮中毒视觉预兆（鱼浮头）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动鱼浮头/缺氧/氨氮中毒视觉预兆识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取预警结果（浮头条数、口开合频率、鳃盖幅度、持续时长）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史预警报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出预警报告
5. （可选）`/web/companion/v2/trigger-soothing-action` - 触发联动告警（用户 APP 紧急推送 / 智能鱼缸警报灯 / 建议立即增氧/换水/检测氨氮）

## 场景代码

- `SMYX_FISH_GASPING_AMMONIA_WARNING_ANALYSIS` - 水族箱内氨氮中毒视觉预兆（鱼浮头）

## 输入约束

- 摄像头：鱼缸固定摄像头 / 水族馆侧面观察摄像头 / 养殖池水面摄像头，**必须同时覆盖水面带和水中段**（鱼浮头是水面行为）
- 分辨率 ≥ 720p；**帧率 ≥ 25 FPS**（口部开合频率检测需 ≥ 2 Hz）
- 光照：建议鱼缸照明常开 + 无强反光；**水面波纹大可能误判，必须做光流稳定**
- **核心采样窗口**：默认 60 秒滚动窗口（用户可配置 30 - 300 秒）
- 视野约束：必须覆盖**水面完整投影**（任何水面盲区都可能漏判浮头）
- 多鱼缸/池场景按摄像头 ID 绑定到注册容器 ID
- **部署时必须录入**：鱼种、缸内总鱼数 N、鱼缸尺寸、是否开启氧气泵/过滤器（用于上下文加权）
- 用户必须授权部署；公共水族馆 / 养殖场需公示告知

## 关键观测信号

### 浮头行为信号（核心）
- `fish_at_surface_count` - 当前帧水面带（水面下 0-1 个体长）内的鱼数
- `fish_breaking_surface_count` - **检测到鱼嘴穿出水面**的鱼数（核心强信号）
- `fish_breaking_surface_ratio` - 浮头鱼数占总鱼数比例
- `surface_breaking_events_per_minute` - 每分钟浮头事件数（同条鱼反复探出累计）

### 呼吸异常信号
- `mouth_opening_frequency_hz` - **口部开合频率（Hz / 次/秒）**（异常阈值 > 2 Hz）
- `mouth_opening_amplitude_normalized` - 口张开幅度（体长归一化）
- `operculum_gill_beat_amplitude_normalized` - **鳃盖开合幅度**（体长归一化，异常增大）
- `operculum_gill_beat_rate_bpm` - 鳃盖呼吸频率（次/分钟，可与 respiratory_rate 技能交叉验证）

### 群体异常信号
- `total_fish_count_baseline` - 注册总鱼数
- `multi_fish_gasping_count` - **同时出现浮头/喘气的鱼数**（≥ 2 条为预警门槛）
- `multi_fish_gasping_duration_seconds` - 多鱼同时异常持续时长（≥ 60s 为核心预警阈值）
- `tank_oxygen_pump_running` - 氧气泵是否运行（如运行仍多鱼浮头，氨氮中毒怀疑度更高）

### 上下文与排除信号（避免误报）
- `is_air_breathing_species` - **是否能用气呼吸鱼种**（斗鱼 / 攀鲈 / 部分鳉鱼科 / 蛇头鱼天然偶尔到水面换气）
- `is_during_feeding` - 是否在投喂窗口内（生理性聚拢水面抢食非浮头）
- `is_surface_feeding_species` - 是否水面摄食型（孔雀鱼 / 鳉鱼科偏好水面）
- `water_surface_disturbance_level` - 水面扰动程度（强水流可能误判）
- `aquatic_plant_floating_at_surface` - 是否水草浮于水面（遮挡可能漏检）

## 综合判定

- `surface_behavior_normal` - 水面行为正常
- `single_fish_surface_breathing_short` - 单条鱼短暂到水面换气（气呼吸鱼种正常 / 投喂期）
- `single_fish_gasping_persistent` - 单条鱼持续浮头喘气（疑似该个体不适，非全缸问题）
- `multi_fish_gasping_moderate` - **多鱼同时浮头（≥ 2 条，持续 30-60s）**：早期预警
- `multi_fish_gasping_severe` - **多鱼同时浮头（≥ 2 条，持续 ≥ 60s）**：氨氮中毒/缺氧风险预警（核心）
- `whole_tank_gasping_emergency` - **全缸鱼同时浮头（≥ 80%，持续 ≥ 30s）**：紧急中毒事件
- `gasping_signal_unreliable` - 信号不可靠（水面波纹过大 / 水草遮挡 / 跟踪率 < 80%）

## 4 级告警策略递进

- Level 1（surface_behavior_normal / single_fish_surface_breathing_short）：仅入库或不提示
- Level 2（single_fish_gasping_persistent）：用户 APP 重要提示，建议**单独观察该鱼，评估是否隔离至检疫缸**
- Level 3（multi_fish_gasping_moderate）：紧急告警，建议**立即检测水质（氨氮 NH3/NH4+、亚硝酸盐 NO2-、pH、溶氧 DO、温度）+ 立即开启/加强增氧 + 准备换水**
- Level 4（multi_fish_gasping_severe / whole_tank_gasping_emergency）：**🚨 最高紧急告警 + 推送家庭/管理人员所有联系人** + 强烈建议**立即采取多措并举**：① 立即开足增氧泵/加气盘 ② 立即换 1/3~1/2 水（**温度 pH 匹配，禁止冷水直冲**） ③ 立即检测氨氮 NH3/亚硝酸盐 NO2- ④ 检查滤材是否堵塞/硝化系统是否崩溃 ⑤ **联系当地观赏鱼兽医或水产技术员**

## 单日告警上限

- Level 1 不限 / Level 2 × 4 / Level 3 × 6（紧急事件可能密集）/ Level 4 **不设上限**（生命安全优先）

## 红线约束

- **🚨 禁止**做"氨氮中毒确诊 / 亚硝酸盐中毒确诊 / 鳃病确诊 / 寄生虫确诊"等**具体疾病诊断**（仅可输出"视觉预兆/风险预警"语义）
- **🚨 绝对禁止**输出具体药物名称、剂量、给药方案（**严禁推荐硝化菌液具体品牌、解氨剂、亚甲基蓝等任何药剂**）
- **禁止**长期存储完整鱼缸视频（≤ 7 天，仅入库浮头事件片段；公共水族馆/养殖场按管理规定）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户启停增氧泵 / 加热棒 / 换水 / 投药 / 灯光参数；**任何水族设备控制变更必须由用户确认**（仅可建议）
- 浮头条数、口开合频率、鳃盖幅度等指标必须基于真实视频帧分析；**禁止伪造或夸大指标**
- 鱼种特异性：**气呼吸鱼种**（斗鱼 / 攀鲈 / 部分鳉鱼科 / 蛇头鱼）天然偶尔到水面换气、**水面摄食鱼**（孔雀鱼 / 鳉鱼科）天然偏好水面 → 必须按鱼种基线判定；**严禁通用阈值盲判气呼吸鱼种为浮头**
- 必须考虑生理性上下文：**投喂窗口聚拢水面抢食 / 强水流冲到水面带 / 水温过高暂时到水面 / 鱼苗自然集群于水面** → 不可直接告警
- 水面波纹过大 / 水草浮于水面遮挡 / 跟踪率 < 80% → 必须返回 `gasping_signal_unreliable` 并建议调整摄像头/清理水面遮挡
- 必须告知用户：AI 视觉识别仅供参考，**最终诊断与处理需用户立即检测水质并由专业兽医/水产技术员确认**

## 输出报告字段

- `report_date` - 报告日期
- `tank_id` - 鱼缸/养殖池 ID
- `species` - 鱼种
- `total_fish_count_baseline` - 注册总鱼数
- `multi_fish_gasping_count` - 同时浮头鱼数
- `multi_fish_gasping_duration_seconds` - 多鱼同时异常持续时长
- `mouth_opening_frequency_hz` - 口开合频率
- `operculum_gill_beat_amplitude_normalized` - 鳃盖幅度
- `composite_scene` - 综合判定
- `alert_level` - 告警等级
- `recommended_actions` - 建议动作（**测水质 NH3/NO2-/DO/pH + 增氧 + 换水 + 检查滤材 + 联系兽医**，绝不含具体药物）
- `disclaimer` - 免责声明
