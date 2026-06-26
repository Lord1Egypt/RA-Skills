# API 接口文档

此处用于存放老年人孤独/抑郁倾向行为分析 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动老年人孤独/抑郁倾向行为分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取消极行为统计 + 情绪风险结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史情绪风险记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_ELDERLY_LONELINESS_DEPRESSION_ANALYSIS` - 老年人孤独/抑郁倾向行为分析

## 输入约束

- 摄像头：独居老人家中客厅 / 卧室 / 起居室固定摄像头，覆盖老人主要日常活动区域，**能看到上半身和面部**
- 帧率 ≥ 5 FPS（推荐 10-15 FPS）；分辨率 ≥ 480p；光照稳定
- 可选附带麦克风（用于叹气声 / 自言自语判定）
- 多人场景下可结合"独处时间窗口"过滤（仅在画面中无他人时统计）
- 隐私敏感场景可启用人体轮廓 + 面部马赛克模式

## 关键观测信号

- `subject_detected` - 是否检测到老人
- `solo_window` - 当前是否处于独处时间窗口（画面中仅有老人）
- `daze_event_count` - 发呆事件次数（连续注视某处 ≥ 10s 且无肢体活动）
- `daze_total_duration_min` - 发呆累计时长
- `sigh_event_count_hourly` - 每小时叹气次数（胸腹快速起伏 + 呼气声）
- `sigh_event_count_daily` - 当日累计叹气次数
- `self_talk_event_count_daily` - 自言自语次数（口部活动 + 画面中无对话对象）
- `social_interaction_minutes_daily` - 当日有效社交互动总时长（参考反向指标）
- `lying_in_bed_duration_daily_min` - 当日卧床时长（参考）

## 阈值与风险等级

- `low` - 各项消极行为均接近基线、社交互动正常
- `medium` - 1-2 项消极行为显著高于基线（例如发呆 > 60 min/天，或叹气 > 10 次/小时）
- `high` - 多项消极行为同时偏高 + 社交互动显著下降 + 连续 ≥ 3 天

## 输出字段（参考）

- `subject_detected` / `solo_window`
- `behavior_metrics` - 当日各项消极行为统计
- `baseline_comparison` - 与个人 7-14 天基线对比（per_item_delta_pct）
- `consecutive_abnormal_days` - 连续异常天数
- `risk_level` - 情绪风险等级（low / medium / high）
- `alert_type` - 提醒类型（loneliness_risk / depression_tendency_suspected / normal）
- `alert_level` - 提醒级别（info / notice / warning）
- `alert_message` - 推送给家属/社工的友好文本（如"妈妈今天独自发呆约 1 小时，叹气次数比平时多了一倍，建议今晚视频通话陪她聊聊"）
- `recommend_action` - 建议动作（push_family_notice / suggest_video_call / suggest_community_visit / observe_only）

> 仅输出基于视觉/音频的客观行为统计与友好提醒，**不提供抑郁症诊断、心理量表评分（如 GDS-15、PHQ-9）或处方**；任何诊断与治疗方案必须由精神科医生或心理咨询师评估制定；若老人出现明显自我伤害言语或行为请立即联系专业机构。
