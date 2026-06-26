# API 接口文档

此处用于存放鱼类游动姿态异常（侧游/倒立）识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动鱼类游姿异常检测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取异常游姿事件 + 异常时长占比
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史游姿监测报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出每日游姿健康报告
5. （可选）`/web/companion/v2/trigger-soothing-action` - 触发联动提醒（用户 APP 推送 / 智能鱼缸告警灯）

## 场景代码

- `SMYX_FISH_ABNORMAL_SWIMMING_DETECTION_ANALYSIS` - 鱼类游动姿态异常（侧游/倒立）识别

## 输入约束

- 摄像头：鱼缸侧面固定摄像头，能完整覆盖鱼缸主活动区域；建议正对鱼缸长边方向
- 帧率 ≥ 15 FPS（高速游动鱼类建议 ≥ 25 FPS）；分辨率 ≥ 720p
- 光照：建议保留鱼缸照明，避免反光过强干扰轴线识别；水浑浊度低
- 时段：可全天运行（默认 24h），夜间灯光关闭时段可切换红外辅助或自动暂停
- 多鱼缸场景按摄像头 ID 绑定到注册鱼缸 ID（每个鱼缸独立基线 + 鱼种清单）
- 多鱼场景按目标跟踪 + ReID 绑定到注册个体（每条鱼独立基线，可选）
- 用户必须授权部署；公共水族馆需公示告知

## 关键观测信号

### 视频（核心）
- `fish_count_detected` - 画面内被跟踪鱼数量
- `body_axis_angle_deg` - 鱼体轴线与水平面夹角（°，正常 ≤ 30°）
- `head_down_angle_deg` - 头部向下倾斜角度（°，倒立判定阈值 > 45°）
- `axial_rotation_event_count` - 绕自身纵轴连续翻转事件次数（≥ 2 圈/秒视为旋转事件）
- `side_swim_duration_sec` - 累计侧游时长（轴角 > 30° 持续时间）
- `upside_down_duration_sec` - 累计倒立时长（头部向下 > 45° 持续时间）
- `floating_duration_sec` - 漂浮时长（无主动游动，被动浮于水面或底部）
- `sinking_duration_sec` - 沉底时长（无主动游动，停留缸底）

### 衍生指标
- `abnormal_total_duration_sec` - 异常总时长（侧游 ∪ 倒立 ∪ 旋转 ∪ 异常漂浮/沉底）
- `observation_total_duration_sec` - 观察总时长
- `abnormal_ratio` - 异常占比 = abnormal_total / observation_total
- `swim_speed_anomaly_score` - 游速异常评分（0-100，过慢或抽搐式急加速）

## 场景判定

- `fish_swimming_normal` - 游姿正常
- `fish_side_swim_brief` - 短暂侧游（轴角 > 30° 但累计时长占比 < 5%）
- `fish_side_swim_persistent` - 持续侧游（异常占比 5%-20%）
- `fish_upside_down` - 倒立事件（头部向下 > 45°）
- `fish_axial_rotation` - 轴向旋转（疑似神经系统受损）
- `fish_floating_or_sinking` - 异常漂浮/沉底（疑似鱼鳔失调）
- `fish_swimming_strong_abnormal` - 显著异常（异常占比 > 20% 或多项叠加）

## 4 级告警策略递进

- Level 1（brief）：仅入库记录，不告警，纳入每日游姿趋势
- Level 2（persistent / 5%-20%）：用户 APP 轻提醒"鱼缸 X 号出现持续侧游，请观察并检查水质"
- Level 3（upside_down / axial_rotation / floating_or_sinking / 异常占比 > 20%）：用户 APP 重要告警 + 建议立即检查（水温、pH、氨氮、亚硝酸盐、溶氧、近期投喂量）
- Level 4（strong_abnormal / 连续 ≥ 2 日 ≥ Level 3）：紧急告警 + 建议立即换水/观察隔离/咨询观赏鱼兽医

## 单日告警上限

- Level 1：不限（仅入库）
- Level 2 × 6 / Level 3 × 3 / Level 4 不设上限

## 红线约束

- 禁止做"鱼鳔病 / 神经系统疾病 / 重金属中毒 / 立鳞病"等疾病诊断
- 禁止长期存储完整鱼缸视频（≤ 7 天，仅入库异常事件片段；公共水族馆按管理规定）
- 禁止用于商业广告 / AI 训练；禁第三方共享
- 禁止越权代用户调整智能鱼缸的加热/换水/投喂/灯光参数；任何水族设备控制变更必须由用户确认
- 异常占比、异常时长等指标必须基于真实视频帧统计；**禁止伪造或夸大异常数据**
- 不同鱼种正常游姿差异极大（如比目鱼天然侧卧、神仙鱼立泳、海马垂直游动）→ 必须按鱼种基线判定；**禁止使用通用阈值对特殊鱼种盲判**
- 鱼种基线需用户在部署时配置（鱼种清单 / 自定义阈值覆盖）

## 每日游姿健康报告字段

- `report_date` - 报告日期
- `tank_id` - 鱼缸 ID
- `observation_hours` - 当日观察总时长
- `species_baseline_loaded` - 是否加载鱼种基线
- `abnormal_ratio_today` - 当日异常占比
- `abnormal_ratio_7d_avg` - 近 7 日异常占比均值
- `abnormal_ratio_trend` - 趋势（rising / flat / falling）
- `top_abnormal_scenes` - 当日 Top 3 异常场景
- `recommended_actions` - 建议动作（检查水质 / 隔离 / 联系兽医等）
