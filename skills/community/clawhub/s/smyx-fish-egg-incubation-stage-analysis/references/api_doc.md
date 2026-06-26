# API 接口文档

此处用于存放鱼卵孵化状态识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动鱼卵孵化状态识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取孵化阶段分类（未受精/早期/中期/晚期/破壳）+ 预计孵化时间窗
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史孵化状态报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出孵化状态报告
5. （可选）`/web/companion/v2/trigger-soothing-action` - 触发联动提醒（用户 APP 推送 / 智能繁殖缸告警灯 / 提示准备丰年虾/分离亲鱼建议）

## 场景代码

- `SMYX_FISH_EGG_INCUBATION_STAGE_ANALYSIS` - 鱼卵孵化状态识别

## 输入约束

- 摄像头：繁殖缸固定摄像头 / **微距镜头**（≥ 3 倍光学微距）/ 智能繁殖缸内置微距
- 分辨率 ≥ 1080p（鱼卵直径 0.5-2 mm，眼睛点 <0.3 mm，需高清才能可靠识别）；帧率不强制要求（图像模式即可，建议每 6 小时 ≥ 1 张）
- 光照：建议**冷白补光灯 + 透过卵层背光**，避免直射强光；水质清澈无杂质
- 拍摄角度：俯拍卵团或正侧面贴近卵层，焦距对准卵团中心
- 输入类型：支持高清图像（jpg/png）或视频；视频自动抽帧
- 多繁殖缸场景按摄像头 ID 绑定到注册繁殖缸 ID + 鱼种 + 产卵时间戳（用于换算孵化龄）
- **部署时必须录入**：鱼种（决定孵化总时长基线，如斑马鱼 48-72h / 神仙鱼 60-72h / 七彩 60-72h / 锦鲤 96-120h@20℃）、产卵时间戳、繁殖缸水温（决定孵化速度）
- 用户必须授权部署；公共育苗场/实验室需公示告知

## 关键观测信号

### 卵颜色信号（核心）
- `egg_count_total` - 视野内可识别鱼卵总数
- `egg_transparent_ratio` - 透明卵比例（早期受精正常）
- `egg_white_opaque_ratio` - **发白/灰白卵比例**（未受精或死亡卵典型特征）
- `egg_black_dead_ratio` - 发黑死亡卵比例
- `egg_yellow_yolk_visible_ratio` - 可见黄色卵黄囊比例（中期典型）

### 胚胎发育信号
- `eye_spot_detected_count` - **检测到胚胎眼睛点的卵数**（黑色小点，晚期标志）
- `eye_spot_detected_ratio` - 眼睛点检出比例
- `embryo_movement_detected` - 是否检测到胚胎抽动（破壳前数小时）
- `hatching_event_detected` - 是否检测到破壳事件（卵壳破裂 + 鱼苗游出）

### 上下文与基线
- `species` - 鱼种
- `species_total_hatch_hours_at_baseline_temp` - 该鱼种在基线水温下的孵化总时长（如 25℃ 斑马鱼 ≈ 60h）
- `water_temperature_c` - 当前水温
- `hours_since_spawn` - 距产卵时间（小时，温度修正后估算孵化龄）

## 综合判定（孵化阶段）

- `incubation_unfertilized` - **未受精**（发白/灰白卵比例 > 70% 且持续 ≥ 24h 无颜色进展）
- `incubation_early` - **早期**（< 30% 孵化总时长，主体透明 + 黄色卵黄囊不明显）
- `incubation_mid` - **中期**（30-70% 总时长，黄色卵黄囊清晰 + 胚胎轮廓可见）
- `incubation_late_eyespot` - **晚期-眼睛点**（70-90% 总时长，**黑色眼睛点出现 ≥ 50% 卵**，预计 24h 内破壳）
- `incubation_pre_hatch` - **临破壳**（> 90% 总时长，胚胎抽动 + 眼睛点清晰）
- `incubation_hatching` - **正在破壳**（检测到破壳事件 + 鱼苗游出）
- `incubation_mass_failure` - **大面积失败**（发白/发黑卵 ≥ 60% 且超过预期孵化时间）
- `incubation_signal_unreliable` - 信号不可靠（焦距未对准/光照不足/卵团遮挡/浑浊度过高）

## 4 级提醒策略递进（孵化阶段更偏"育苗助手"，非健康告警）

- Level 1（early / mid）：仅入库 + 用户 APP 进度提示"孵化进展正常，距预计破壳还有 X 小时"
- Level 2（late_eyespot / pre_hatch）：重要提示，"**已出现眼睛点，预计 24 小时内孵化，请准备丰年虾无节幼体 / 蛋黄水 / 草履虫开口饵料 + 准备分离亲鱼防吞食**"
- Level 3（hatching）：紧急提示，"**正在破壳，请打开微弱光照、停止充气避免幼苗被吸入过滤器、准备鱼苗缸隔离**"
- Level 4（unfertilized / mass_failure）：重要预警，"**未受精或大面积孵化失败（≥ 60%），建议清理坏卵防霉污染水质 + 检查亲鱼健康状态/水温/光照周期 + 联系经验丰富的水族繁殖者**"

## 单日提醒上限

- Level 1 不限（仅进度更新）/ Level 2 × 4 / Level 3 × 6（破壳事件可能密集）/ Level 4 × 2

## 红线约束

- **禁止**做"水霉感染 / 真菌污染 / 受精率不足"等具体疾病或繁殖学诊断
- **禁止**输出具体药物名称、剂量、给药方案（特别是**严禁推荐甲基蓝、二氯异氰尿酸钠 等防霉化学剂**）
- **禁止**长期存储完整鱼缸视频/图像（≤ 14 天，仅入库孵化阶段事件帧；公共育苗场/实验室按管理规定）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户启停加热棒 / 增氧 / 换水 / 投药 / 灯光参数；任何水族设备控制变更必须由用户确认（仅可建议）
- 颜色比例、眼睛点检出比例等指标必须基于真实图像识别；**禁止伪造或夸大指标**
- 鱼种特异性：不同鱼种孵化总时长、卵颜色基线差异极大（斑马鱼透明小卵 vs 神仙鱼黄褐色粘性卵 vs 七彩仙人黄色卵 vs 鼠鱼银白色卵）→ 必须按**鱼种 + 水温**联合判定；**禁止使用通用阈值盲判**
- 必须考虑光照偏差上下文：背光偏色 / 白平衡漂移会让透明卵看起来"发白" → 必须做白平衡校正
- 焦距未对准 / 卵团遮挡 / 浑浊度过高 → 必须返回 `incubation_signal_unreliable`，**禁止给出不可靠的失败判定**
- 必须告知用户：AI 识别仅供参考，**最终繁殖决策与水质处理需用户结合现场实际或专业繁殖者意见**

## 输出报告字段

- `report_date` - 报告日期
- `tank_id` - 繁殖缸 ID
- `species` - 鱼种
- `spawn_time` - 产卵时间戳
- `water_temperature_c` - 当前水温
- `hours_since_spawn` - 距产卵时长（小时）
- `egg_count_total` - 卵总数
- `egg_color_distribution` - 颜色分布比例（透明/发白/发黑/黄色卵黄囊）
- `eye_spot_detected_ratio` - 眼睛点检出比例
- `composite_scene` - 孵化阶段判定
- `estimated_hatching_window_hours` - 预计破壳时间窗（小时）
- `alert_level` - 提醒等级
- `recommended_actions` - 建议动作（准备丰年虾/分离亲鱼/清理坏卵/停止充气，**不含具体化学药物**）
- `disclaimer` - 免责声明
