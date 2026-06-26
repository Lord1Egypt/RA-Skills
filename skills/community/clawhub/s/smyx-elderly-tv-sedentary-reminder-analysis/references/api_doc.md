# API 接口文档

此处用于存放老年人电视观看时长与久坐关联 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动老年人电视观看时长与久坐关联分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取观看时长与久坐结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史观看记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_ELDERLY_TV_SEDENTARY_REMINDER_ANALYSIS` - 老年人电视观看时长与久坐关联

## 输入约束

- 摄像头：客厅固定摄像头，**画面应同时覆盖沙发区域与电视方向**（侧前方/对角线视角）
- 帧率 ≥ 5 FPS；分辨率 ≥ 480p；光照稳定
- 初次部署可在画面中**框选两个 ROI**：
  - `sofa_region` - 沙发坐姿区域
  - `tv_region` - 电视屏幕区域（用于判断面部朝向）
- 视频时段建议覆盖白天/晚间观看时段
- 隐私敏感场景可启用人体轮廓模式

## 关键观测信号

- `subject_in_sofa` - 老人是否处于沙发坐姿区域
- `posture` - 姿态分类（sitting / standing / lying / leaving）
- `face_orientation_to_tv` - 面部是否朝向 tv_region（true / false / unknown）
- `tv_on_estimate` - 电视画面是否处于"亮"状态（基于 tv_region 亮度变化推断，可选）
- `continuous_tv_watch_duration_min` - 当次连续坐着看电视时长（分钟）
- `stand_up_events_today` - 当日起身次数（离开沙发）
- `total_tv_watch_duration_today_min` - 当日累计电视观看时长（分钟）
- `longest_continuous_session_min` - 当日最长一次连续观看时长

## 默认阈值（可由调用方覆盖）

- 连续观看时长阈值：**120 分钟**（continuous_tv_watch_threshold_min）→ 触发久坐活动提醒
- 起身判定阈值：离开沙发 ≥ 60 秒 → 重置连续观看计时
- 当日累计观看过长阈值：> 360 分钟（6 小时） → 触发"观看总时长偏长"提醒
- 短暂头部转动/取物不算"离开沙发"，需结合姿态变化

## 提醒类型

- `continuous_watch_too_long` - 连续观看时长超阈值（核心久坐提醒）
- `daily_total_watch_too_long` - 当日累计观看时长偏长
- `normal` - 正常

## 输出字段（参考）

- `subject_detected` - 是否检测到老人
- `sofa_region_defined` / `tv_region_defined` - 两个 ROI 是否已定义
- `current_session` - 当次会话指标（continuous_tv_watch_duration_min / posture / face_orientation_to_tv）
- `daily_metrics` - 当日指标（total_tv_watch_duration_today_min / stand_up_events_today / longest_continuous_session_min）
- `alert_type` - 提醒类型
- `alert_level` - 提醒级别（notice / warning）
- `alert_message` - 推送/语音播报文本（如"张爷爷，您已经看了 2 小时电视，起来活动一下吧"）
- `recommend_action` - 建议动作（voice_play_reminder / push_app_notice / suggest_stretch / observe_only）

> 仅输出基于视觉的观看与坐姿行为统计与友好提醒，不提供深静脉血栓 / 腰背疼痛 / 代谢紊乱等医学诊断或处方；如老人有明显腿肿、胸闷等不适请就医。
