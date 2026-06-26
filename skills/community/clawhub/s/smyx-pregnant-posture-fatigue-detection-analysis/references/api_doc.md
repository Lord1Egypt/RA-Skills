# API 接口文档

此处用于存放孕妇久站/过度劳累识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动孕妇久站/过度劳累识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取姿态/劳累风险结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史劳累事件
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_PREGNANT_POSTURE_FATIGUE_DETECTION_ANALYSIS` - 孕妇久站/过度劳累识别

## 输入约束

- 摄像头：家庭客厅 / 厨房 / 卧室固定摄像头，覆盖孕妇主要活动区域，能看到全身轮廓
- 帧率 ≥ 5 FPS；分辨率 ≥ 480p；光照稳定
- 初次部署可在画面中**框选孕妇主要活动区域 ROI**（可选）
- 多人场景下建议结合体型/外观特征锁定主目标（如孕妇穿着特定颜色）
- 隐私敏感场景可启用人体轮廓模式

## 关键观测信号

- `subject_detected` - 是否检测到孕妇
- `posture` - 当前姿态分类（standing / sitting / squatting / bending / lying / walking）
- `continuous_standing_duration_min` - 当次连续站立时长（分钟）
- `bending_event_count_hourly` - 最近 1 小时弯腰次数
- `bending_event_count_daily` - 当日累计弯腰次数
- `lifting_object_event_count_daily` - 当日疑似搬重物动作次数（参考）
- `total_standing_duration_today_min` - 当日累计站立时长
- `sit_break_count_today` - 当日有效坐下休息次数

## 默认阈值（可由调用方覆盖）

- 连续站立阈值：**30 分钟**（continuous_standing_threshold_min）→ 触发"久站提醒"
- 弯腰频率阈值：**每小时 > 10 次** → 触发"频繁弯腰提醒"
- 搬重物动作 ≥ 1 次/天 → 友好提示"避免提搬重物"
- 站立判定中，短暂转身/换姿势 < 30 秒不打断连续计时
- 有效坐下休息：坐下 ≥ 3 分钟 → 重置连续站立计时

## 提醒类型

- `prolonged_standing` - 久站提醒（建议坐下休息）
- `frequent_bending` - 频繁弯腰提醒（建议减少弯腰动作 / 使用辅助工具）
- `heavy_lifting_suspected` - 疑似搬重物提醒
- `combined_fatigue_risk` - 多项异常同时出现（更高优先级）
- `normal` - 正常

## 输出字段（参考）

- `subject_detected` / `posture`
- `current_session` - 当次会话指标（continuous_standing_duration_min / bending_event_count_hourly）
- `daily_metrics` - 当日指标（total_standing_duration_today_min / bending_event_count_daily / lifting_object_event_count_daily / sit_break_count_today）
- `alert_type` - 提醒类型
- `alert_level` - 提醒级别（info / notice / warning）
- `alert_message` - 推送/语音播报文本（如"您已站立 30 分钟，建议坐下休息一会儿~"）
- `recommend_action` - 建议动作（voice_play_reminder / push_app_notice / suggest_rest / suggest_avoid_heavy_lifting / observe_only）

> 仅输出基于视觉的姿态与动作统计与友好提醒，不提供早产、胎盘早剥、腰背疼痛等具体医学诊断；如孕妇有腹痛、阴道出血、明显不适等情况请立即就医并由产科医生评估。
