# API 接口文档

此处用于存放受灾人群心理创伤行为识别（应急场景）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权（**仅向应急指挥中心 / 持证心理救援团队开放**）
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动受灾人群心理创伤行为识别任务（应急级别）
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取急性应激行为预警 + 定位 + 救援引导建议
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史心理危机预警清单
4. `/health/order/api/getReportDetailExport?id={id}` - 导出指挥中心完整事件报告

## 场景代码

- `SMYX_TRAUMA_STRESS_BEHAVIOR_DETECTION_ANALYSIS` - 受灾人群心理创伤行为识别（应急场景）

## 输入约束

- 摄像头：应急避难所 / 战时防空设施 / 事故现场临时安置点的固定摄像头，覆盖人群区域，能看到全身或上半身
- 帧率 ≥ 5 FPS（推荐 10 FPS）；分辨率 ≥ 720p；夜间需红外补光
- 视频时长：**实时流接入**，建议 1 分钟滚动窗口持续分析；单次离线分析建议 ≥ 10 分钟
- 多人场景必须按目标跟踪生成临时编号（如 V-Zone3-007），便于现场救援人员二次定位
- 区域 ROI 标定：避难所分区（Zone-A / Zone-B / 角落区 / 入口区 等），用于事件定位
- 应急场景**允许且必须**进行视觉行为识别，但应做**面部模糊化**输出给现场指挥屏（保护受灾者尊严）

## 关键观测信号（4 项核心 + 辅助）

### 核心急性应激行为
- `stupor_static_minutes` - 木僵：连续静止 ≥ 5 分钟且对外界声响 / 走动刺激无定向反应
- `tremor_detected` - 颤抖：肉眼可见四肢或躯干持续不自主抖动（≥ 5 秒）
- `unresponsive_to_stimulus` - 无反应：对周围呼唤、声响、移动物体**无定向转头 / 无回避**
- `hypervigilance_event_count_per_min` - 过度警觉：每分钟频繁环顾四周次数 + 惊跳反应次数

### 辅助观察
- `crouch_hugging_knees_minutes` - 抱膝蜷缩时长（参考指标）
- `crying_sobbing_visual` - 视觉哭泣行为（参考指标，含掩面动作）
- `wandering_aimless_pacing` - 无目的徘徊（参考指标）
- `seek_isolation_event` - 主动远离人群独处（参考指标）
- `face_blank_neutral_duration` - 面部表情木然时长

### 现场环境
- `subject_count_in_zone` - 区域内人数（用于事件密度计算）
- `responder_in_view` - 是否有救援人员在视野内（影响优先级排序）

## 阈值与等级（应急救援场景，**宁可多触发不可漏报**）

- 单一信号出现 → **mild_concern**（轻度关注）
- 单一信号持续 ≥ 5 分钟 → **psych_crisis_notice**（心理危机提示）
- 2 项及以上核心信号同时出现 → **psych_crisis_alert**（心理危机预警 ⚠️）
- 4 项核心信号同时出现 或 任一信号持续 ≥ 10 分钟 → **psych_crisis_critical**（心理危机紧急 🚨，**立刻派员**）
- 儿童 / 老人 / 孕妇 / 残障人士等脆弱群体阈值降一档（系统更敏感）

## 输出字段（参考）

- `event_id` / `report_window_min`
- `subject_tracking_id` - 临时跟踪编号（仅供本次救援使用，如 V-Zone3-007）
- `zone_id` / `zone_name` / `position_in_zone` - 区域定位与相对坐标，便于现场救援
- `core_signals` - 4 项核心信号当前状态与持续时长
- `aux_signals` - 5 项辅助观察当前状态
- `vulnerable_flag` - 是否疑似脆弱群体（child / elderly / pregnant / mobility_impaired / unknown）
- `crisis_pattern` - 危机模式（stupor_dominant / tremor_dominant / unresponsive_dominant / hypervigilant_dominant / mixed_severe）
- `crisis_level` - 危机等级（none / mild_concern / psych_crisis_notice / psych_crisis_alert / psych_crisis_critical）
- `alert_type` - 提醒类型
- `alert_level` - 提醒级别（info / notice / warning / urgent）
- `responder_dispatch_suggestion` - 救援人员调度建议（如"建议持证心理救援人员 2 名前往 Zone-B 中部，对象 V-Zone3-007（疑似老人，已木僵 6 分钟），优先采用 PFA 心理急救步骤"）
- `pfa_quick_reference` - PFA（Psychological First Aid）心理急救要点提示（如"建立连接 → 安全保障 → 平静化 → 联系亲友 → 实际支持 → 转介资源"）
- `recommend_action` - 建议动作（dispatch_psych_responder / dispatch_medical_team_for_assessment / push_command_center_alert / observe_only）
- `referral_resource` - 后续转介资源（当地精神卫生中心 / 12320 卫生热线 / 全国心理援助热线 400-161-9995）

## 强制约束与红线

- ❌ **禁止**输出"急性应激障碍 ASD / 创伤后应激障碍 PTSD"等任何临床诊断结论；仅输出**行为观察预警**
- ❌ **禁止**给予药物建议（如镇静剂 / 抗焦虑药），任何药物干预必须由现场医疗团队处方
- ❌ **禁止**在公共指挥屏未脱敏地展示受灾者面部
- ❌ **禁止**将受灾人群视频用于非救援用途（媒体传播 / 社交媒体 / 商业研究等）
- ❌ **禁止**长期存储原始视频；建议救援结束后 ≤ 7 天清理，仅保留聚合事件日志用于事后救援评估
- ✅ **必须**经由应急指挥中心 / 卫健委授权后部署，受灾者具备充分知情即被默许参与（应急豁免，但事后告知）
- ✅ **必须**配合现场持证心理救援人员（如中国心理学会临床心理学注册工作委员会注册人员、红十字心理救援队等）使用
- ✅ 高危信号必须**人工复核**后再升级到救援调度，避免误判造成现场骚动
- ✅ 必须遵守《突发事件应对法》《精神卫生法》及当地灾害响应规程

> 仅输出基于视觉的**行为观察级心理危机预警**，**不构成 ASD / PTSD 等任何临床诊断**；所有干预必须由现场持证心理救援人员按 PFA（心理急救）原则实施，疑似严重病例必须转介至当地精神卫生中心进行专业评估。
