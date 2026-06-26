# API 接口文档

此处用于存放爬宠体温调节行为识别（晒点/躲避）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动爬宠体温调节行为识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果（温区停留时长 / 移动频次 / 温区偏好 / 活动节律）
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史温区利用报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出每日温区利用报告
5. （可选）`/web/companion/v2/trigger-soothing-action` - 触发联动提醒（用户 APP 推送 / 建议调整加热设备布局）

## 场景代码

- `SMYX_REPTILE_THERMOREGULATION_BEHAVIOR_ANALYSIS` - 爬宠体温调节行为识别（晒点/躲避）

## 输入约束

- 摄像头：爬宠箱固定摄像头 / 智能爬宠箱内置摄像头 / 养殖场监控摄像头
- 分辨率 ≥ 720p；帧率 ≥ 15 FPS（体温调节行为非高速动作，15 FPS 足够）
- **关键硬件要求**：**视野必须同时覆盖晒点区（加热灯下方高温区域）+ 躲避区（洞穴/掩体/冷区）+ 中间过渡区**（三个温区全部可见才能完整统计）
- 拍摄角度：俯拍或斜俯拍（可清晰看到宠物位置与温区边界）
- 光照：加热灯/UVB 灯正常开启时拍摄（关闭时无法区分温区）
- **核心采样窗口**：默认连续 ≥ 2 小时（体温调节是慢节律行为，1 小时内可能无法建立完整节律）
- 多箱场景按摄像头 ID 绑定到注册容器 ID
- **部署时必须录入**：宠物物种（豹纹守宫 / 鬃狮蜥 / 蓝舌石龙子 / 玉米蛇 / 球蟒 / 红腿象龟 / 苏卡达等）、晒点温度（用户设定值）、冷区温度（用户设定值）、加热设备类型（加热灯 / 陶瓷加热器 / 加热垫）、UVB 灯类型与开启时段、躲避区数量与位置
- 用户必须授权部署；养殖场需公示告知

## 关键观测信号

### 温区停留统计
- `basking_zone_duration_ratio` - **晒点区停留时长占比**（核心指标，正常 30-60% 因物种而异）
- `hiding_zone_duration_ratio` - **躲避区停留时长占比**（核心指标，正常 10-40% 因物种而异）
- `cool_zone_duration_ratio` - 冷区停留时长占比
- `transition_zone_duration_ratio` - 过渡区停留时长占比
- `basking_session_count` - 晒点区进入次数
- `basking_session_duration_minutes_avg` - 单次晒点停留平均时长（分钟）
- `hiding_session_duration_minutes_avg` - 单次躲避停留平均时长（分钟）

### 移动与穿梭统计
- `zone_transitions_per_hour` - **每小时温区移动次数**（核心指标）
- `basking_to_hiding_transitions` - 晒点→躲避直接移动次数
- `hiding_to_basking_transitions` - 躲避→晒点直接移动次数
- `frequent_shuttling_flag` - **频繁穿梭标志**（> 10 次/小时，可能温度梯度不合理或应激）

### 活动节律
- `activity_peak_hour` - 活动高峰时段（小时）
- `basking_peak_hour` - 晒点高峰时段（通常与 UVB 灯/加热灯开启时段一致）
- `diurnal_nocturnal_pattern` - 昼夜活动模式（昼行 / 夜行 / 晨昏行）
- `activity_rhythm_consistency_score` - 活动节律一致性评分（与同物种正常节律的偏差度）

### 温区偏好综合
- `thermal_preference_label` - **温区偏好标签**（basking_preferred / hiding_preferred / **frequent_shuttling** / balanced / **abnormal_immobility**）
- `thermal_preference_z_score` - 温区偏好相对物种基线的 z-score

### 上下文与排除信号
- `is_uv_bulb_on` - UVB 灯是否开启（关闭时爬宠不出晒点属正常）
- `is_heating_device_on` - 加热设备是否开启
- `is_during_shedding_cycle` - 是否处于蜕皮期（蜕皮期偏好躲避属正常）
- `is_during_brimation` - 是否处于冬眠/冬化期（活动大幅减少属正常）
- `is_newly_introduced` - 是否新入缸适应期（应激多躲属正常）
- `is_feeding_day` - 是否喂食日（喂食后可能增加晒点停留助消化）
- `ambient_room_temperature_c` - 室温（影响冷区实际温度）

## 综合判定

- `thermoregulation_balanced` - 温区利用正常均衡（符合物种基线）
- `basking_preferred_normal` - 偏好晒点但属正常范围（消化期 / UVB 开启期）
- `hiding_preferred_normal` - 偏好躲避但属正常范围（蜕皮期 / 新入缸 / 夜行种昼间）
- `frequent_shuttling_abnormal` - **频繁穿梭异常**（> 10 次/小时，可能温度梯度不合理或应激）
- `excessive_hiding` - **过度躲避**（躲避占比 > 70%，持续 ≥ 48 小时，非蜕皮/冬化/新入缸 → 疑似疾病/寄生虫/环境不适）
- `excessive_basking` - **过度晒点**（晒点占比 > 80%，持续 ≥ 48 小时 → 疑似温度不足/消化问题/代谢异常）
- `abnormal_immobility` - **异常不动**（任一温区长时间静止不动，> 4 小时无区域转换 → 疑似严重疾病/深度应激/温度极端不适）
- `thermoregulation_signal_unreliable` - 信号不可靠（加热/UVB 设备关闭 / 视野未覆盖所有温区 / 跟踪率 < 80%）

## 4 级提醒策略递进（侧重环境优化与福利改善，非疾病诊断）

- Level 1（balanced / basking_preferred_normal / hiding_preferred_normal）：仅入库 + 用户 APP 积极反馈"温区利用正常，当前环境设置适宜"
- Level 2（frequent_shuttling_abnormal）：重要提示，建议**评估温度梯度（晒点/冷区温差是否在物种适宜范围内）/ 检查加热设备是否故障或位置不当 / 评估躲避区数量是否足够**
- Level 3（excessive_hiding / excessive_basking）：紧急提示，建议**立即检查环境参数（晒点温度/冷区温度/UVB 强度/湿度）+ 近距离观察宠物体表/食欲/排泄 / 如持续 ≥ 72 小时则联系爬宠兽医**
- Level 4（abnormal_immobility）：最高紧急提示 + 推送所有管理人员 + 强烈建议**立即检查宠物反应（轻轻触碰是否有反应）/ 立即测各温区实际温度 / 联系爬宠兽医（异常不动可能是严重疾病信号）**

## 单日提醒上限

- Level 1 不限 / Level 2 × 3 / Level 3 × 4 / Level 4 不设上限

## 红线约束

- **🚨 禁止**做"代谢性骨病 / 呼吸道感染 / 寄生虫感染 / 应激综合征 / 消化停滞"等**具体疾病诊断**
- **🚨 绝对禁止**输出具体药物名称、剂量、给药方案
- **禁止**长期存储完整爬宠箱视频（≤ 14 天，留温区利用时间序列 + 关键行为片段；养殖场按管理规定）
- **禁止**用于商业广告 / AI 训练；禁第三方共享
- **禁止**越权代用户启停加热灯 / UVB 灯 / 加热垫 / 喷雾 / 灯光参数；任何设备控制变更必须由用户确认（仅可建议）
- 温区停留占比 / 移动频次等指标必须基于真实视频帧分析；**禁止伪造或夸大指标**
- 物种特异性：**夜行种**（豹纹守宫 / 鞭尾蜥 / 部分壁虎）昼间多躲避属正常、**昼行种**（鬃狮蜥 / 蓝舌 / 变色龙 / 水龙）昼间应多晒点、**晨昏行种**（某些石龙子 / 守宫）早晚活动高峰 → 必须**按物种基线判定**；**严禁通用阈值盲判夜行种昼间躲避为异常**
- 必须考虑生理性上下文：**蜕皮期偏好躲避（湿度需求）/ 冬化/冬眠期活动极低 / 新入缸应激期 / 喂食后增加晒点助消化 / 繁殖期行为变化** → 不可直接告警
- UVB / 加热设备关闭时 → 无法区分温区 → 必须返回 `thermoregulation_signal_unreliable` 并建议在设备开启后重新分析
- 视野未覆盖所有温区（晒点/躲避/冷区缺一）/ 跟踪率 < 80% → 必须返回 `thermoregulation_signal_unreliable` 并建议调整摄像头
- 必须告知用户：AI 行为分析仅供参考，**最终环境优化与疾病判断需用户结合现场观察并由专业爬宠兽医确认**

## 输出报告字段

- `report_date` - 报告日期
- `enclosure_id` - 爬宠箱 ID
- `species` - 宠物物种
- `basking_temp_setting_c` - 晒点温度设定
- `cool_zone_temp_setting_c` - 冷区温度设定
- `basking_zone_duration_ratio` - 晒点区停留占比
- `hiding_zone_duration_ratio` - 躲避区停留占比
- `zone_transitions_per_hour` - 每小时移动次数
- `thermal_preference_label` - 温区偏好标签
- `activity_rhythm_consistency_score` - 节律一致性
- `composite_scene` - 综合判定
- `alert_level` - 提醒等级
- `recommended_actions` - 建议动作（评估温度梯度 / 检查设备 / 观察体表食欲排泄 / 联系爬宠兽医，**不含药物**）
- `disclaimer` - 免责声明
