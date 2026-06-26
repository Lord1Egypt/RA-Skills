# API 接口文档

此处用于存放鱼类呼吸频率（鳃盖开合）监测 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动鱼类呼吸频率监测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取呼吸频率监测结果（次/分钟 + 异常判定 + 缺氧等级）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史呼吸频率监测报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出呼吸频率监测报告
5. （可选）`/web/companion/v2/trigger-soothing-action` - 触发联动提醒（用户 APP 推送 / 智能鱼缸告警灯 / 触发增氧设备建议提示）

## 场景代码

- `SMYX_FISH_RESPIRATORY_RATE_MONITOR_ANALYSIS` - 鱼类呼吸频率（鳃盖开合）监测

## 输入约束

- 摄像头：鱼缸固定摄像头，能近距离（≤ 30 cm）清晰拍摄鱼鳃盖区域
- 分辨率 ≥ 720p；**帧率 ≥ 25 FPS**（鳃盖开合频率高，需高帧率才能可靠采样；正常 20-80 次/分钟 ≈ 0.3-1.3 Hz）
- 光照：建议鱼缸照明开启 + 无强反光；水质清澈
- 拍摄角度：优先正侧面（鳃盖运动幅度最大）；鳃盖区域完整可见
- 单次有效采样窗口：≥ 30 秒（建议 60 秒），用于稳定计算 BPM
- 多鱼缸场景按摄像头 ID 绑定到注册鱼缸 ID（每个鱼缸独立鱼种 + 水温记录）
- 多鱼场景按目标跟踪 + ReID 绑定到注册个体（每条鱼独立基线，可选）
- 用户必须授权部署；公共水族馆 / 实验室需公示告知

## 关键观测信号

### 鳃盖运动信号（核心）
- `gill_open_close_cycle_count` - 采样窗口内鳃盖开合周期数
- `sampling_window_sec` - 采样窗口时长（秒）
- `respiratory_rate_bpm` - 呼吸频率（次/分钟，= cycle_count × 60 / window_sec）
- `bpm_signal_stability_score` - 信号稳定度评分（0-100，去除游动遮挡 / 帧间抖动后的有效采样比例）
- `gill_opening_amplitude_score` - 鳃盖开合幅度评分（0-100，反映呼吸深度）

### 上下文信号
- `water_temperature_c` - 水温（℃，用户输入或智能鱼缸传感器；同物种水温越高 BPM 越高）
- `fish_activity_level` - 鱼活跃度（resting / normal / active；活跃时 BPM 升高为生理性）
- `time_since_feeding_min` - 距上次投喂时长（分钟，投喂后 30 分钟内 BPM 生理性升高）
- `surface_gasping_detected` - 是否检测到浮头吞气（缺氧典型征兆）

### 鱼种基线（必须配置）
- `species` - 鱼种标识（金鱼 / 锦鲤 / 神仙鱼 / 斗鱼 / 龙鱼 / 海水鱼 等）
- `bpm_baseline_at_25c` - 25℃ 下该鱼种的正常 BPM 区间（如金鱼 40-80）
- `bpm_threshold_high` - 高阈值（默认 80，按鱼种 + 水温动态调整）
- `bpm_threshold_low` - 低阈值（呼吸过缓也异常，疑似低温昏迷 / 中毒）

## 综合判定

- `respiratory_normal` - 呼吸频率正常
- `respiratory_high_normal` - 偏高但属于生理性（活跃 / 投喂后 30 分钟内）
- `respiratory_hyperventilation_mild` - 呼吸急促轻度（BPM 超阈值 1.1-1.3 倍）
- `respiratory_hyperventilation_moderate` - 呼吸急促中度（1.3-1.6 倍 + 鳃盖大开合）
- `respiratory_hypoxia_warning` - 缺氧预警（BPM > 阈值 1.6 倍 / 浮头吞气）
- `respiratory_bradypnea` - 呼吸过缓（BPM < 低阈值，疑似低温/中毒/濒死）
- `respiratory_signal_unreliable` - 信号不可靠（稳定度 < 50%，建议重拍）

## 4 级告警策略递进

- Level 1（hyperventilation_mild / high_normal）：仅入库记录或用户 APP 轻提醒"鱼缸 X 号呼吸偏快，请观察水质"
- Level 2（hyperventilation_moderate）：用户 APP 重要告警，建议**检查水温、溶氧、pH、氨氮**
- Level 3（hypoxia_warning / bradypnea）：紧急告警，**强烈建议立即开启增氧设备 / 部分换水 / 降低密度**，并提示联系**当地观赏鱼兽医**
- Level 4（连续 ≥ 2 次 Level 3 / 同缸多条鱼同时缺氧 / 浮头吞气持续 ≥ 5 分钟）：最高紧急告警 + 推送家庭/管理人员所有联系人 + 强烈建议**立即抢救**（开启增氧泵 + 大幅换水 + 降低喂食）

## 单日告警上限

- Level 1 不限（仅入库或轻提醒）/ Level 2 × 6 / Level 3 × 3 / Level 4 不设上限

## 红线约束

- **禁止**做"鳃病 / 烂鳃 / 氨中毒 / 亚硝酸盐中毒 / 寄生虫感染"等具体疾病诊断
- **禁止**输出具体药物名称、剂量、给药方案
- **禁止**长期存储完整鱼缸视频（≤ 7 天，仅入库异常呼吸事件片段；公共水族馆 / 实验室按管理规定）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户启停增氧泵 / 加热棒 / 换水 / 投药 / 灯光参数；任何水族设备控制变更必须由用户确认（仅可建议）
- BPM、稳定度、鳃盖幅度等指标必须基于真实视频帧统计；**禁止伪造或夸大指标**
- 鱼种特异性：不同鱼种 BPM 基线差异极大（金鱼 40-80 vs 海水神仙鱼 60-120）→ 必须按**鱼种 + 水温**联合判定基线；**禁止使用通用阈值盲判**
- 水温升高、活跃游动、刚投喂后 30 分钟内会出现生理性 BPM 升高 → 必须在上下文中标注并避免误报
- 信号稳定度 < 50% 时必须返回 `respiratory_signal_unreliable` 并建议重拍，**禁止给出不可靠的告警**

## 输出报告字段

- `report_date` - 报告日期
- `tank_id` - 鱼缸 ID
- `species` - 鱼种
- `water_temperature_c` - 水温
- `respiratory_rate_bpm` - 当次呼吸频率
- `bpm_baseline_range` - 鱼种 + 水温对应正常区间
- `bpm_signal_stability_score` - 信号稳定度
- `composite_scene` - 综合判定
- `alert_level` - 告警等级
- `recommended_actions` - 建议动作（开启增氧 / 检查水温 / 部分换水 / 降低密度 / 联系兽医，**不含药物**）
- `disclaimer` - 免责声明
