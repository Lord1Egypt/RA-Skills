# API 接口文档

此处用于存放老年人睡眠中间惊醒/梦魇行为识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动老年人睡眠中间惊醒/梦魇行为识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取异常事件清单 + 频次统计 + 睡眠质量摘要
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史夜间睡眠异常报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_ELDERLY_NIGHTMARE_STARTLE_DETECT_ANALYSIS` - 老年人睡眠中间惊醒/梦魇行为识别

## 输入约束

- 摄像头：卧室固定摄像头，**必须支持红外夜视**（IR），**必须含麦克风**（惊叫识别依赖音频）；能完整拍到老人在床的上半身
- 帧率 ≥ 5 FPS（夜间统计无需高帧率）；分辨率 ≥ 480p；音频采样率 ≥ 16kHz
- 视频时长：建议覆盖完整睡眠时段（22:00 → 次日 07:00 左右），**单次分析建议 ≥ 6 小时**
- ROI 标定：床位 ROI（bed_region）
- 多人共眠场景（如老两口）需按目标跟踪，避免事件归属错误
- 隐私敏感场景必须启用人体轮廓 + 面部马赛克模式

## 关键观测信号

### 视觉
- `sudden_sit_up_event_count` - 突然坐起事件次数（快速从躺卧→坐立，<2 秒完成）
- `arm_thrashing_event_count` - 无目的快速挥舞手臂事件次数（疑似 RBD 表现）
- `kick_leg_event_count` - 踢腿事件次数（参考指标）
- `out_of_bed_event_count` - 离床事件次数（参考指标，与 wandering 技能配合）
- `total_event_duration_sec` - 全部异常事件累计时长

### 音频
- `scream_event_count` - 高频短促叫声次数（基于频谱+短时能量）
- `mumble_or_talking_in_sleep_count` - 梦呓/说梦话次数（参考指标）
- `loud_breathing_event_count` - 异常粗重呼吸事件（参考指标，可能与睡眠呼吸暂停相关）

### 综合
- `sleep_window` - 监测时间窗（如 22:00-07:00）
- `total_abnormal_event_count` - 异常事件总次数
- `event_density_per_hour` - 每小时事件密度
- `peak_event_hour` - 异常事件高发时段（如 03:00-04:00，REM 期密集）
- `sleep_continuity_score` - 睡眠连续性评分（0-100，越高越连续）

## 阈值与等级

- `0-1 次/夜` - normal（正常）
- `2-3 次/夜` - mild（轻度）
- `4-7 次/夜` - notable（较频繁）→ 建议记录跟踪
- `≥ 8 次/夜` 或 `单晚出现 ≥ 1 次 arm_thrashing + scream` 组合 - frequent（频繁）→ 建议尽快就诊神经内科 / 睡眠门诊
- 单次喷嚏 / 咳嗽 / 翻身等正常生理活动不应计入异常事件

## 输出字段（参考）

- `sleep_window` / `bed_occupied_minutes`
- `visual_events` / `audio_events`
- `event_timeline` - 异常事件时间线（每条含 start_ts / end_ts / type / duration_sec / evidence_snippet_url，原始视频不留存）
- `total_abnormal_event_count` / `event_density_per_hour` / `peak_event_hour`
- `sleep_continuity_score`
- `abnormal_pattern` - 行为模式（pure_nightmare / suspect_rbd / general_arousal / mixed / none）
- `risk_signal_level` - 风险信号等级（none / mild / notable / strong）
- `alert_type` - 提醒类型（sleep_abnormal_notable / sleep_abnormal_frequent / suspect_rbd_pattern / improving / normal）
- `alert_level` - 提醒级别（info / notice / warning）
- `family_summary` - 家属友好摘要（如"昨晚老人在 03:12 突然坐起并伴随短促叫声 1 次，03:38 出现挥舞手臂约 8 秒；夜间共 3 次异常事件，建议白天观察精神状态，若反复出现建议就诊神经内科睡眠门诊"）
- `recommend_action` - 建议动作（push_family_summary / suggest_record_diary / suggest_consult_sleep_clinic / suggest_neurology_consult / observe_only）
- `clinical_reference` - 当 frequent 或 suspect_rbd_pattern 时附**神经内科 / 睡眠门诊就诊建议** + 中国睡眠研究会等参考资源

## 强制约束与红线

- ❌ **禁止**输出 RBD / 帕金森病 / 阿尔茨海默病 / 睡眠呼吸暂停综合征等任何医学诊断结论
- ❌ **禁止**根据本工具结果调整药物
- ❌ **禁止**长期存储夜间原始视频；建议仅保存事件片段证据（短片，≤ 30 秒）+ 指标统计
- ✅ 出现 frequent 或 suspect_rbd_pattern 时附**神经内科 / 睡眠门诊** 就诊建议
- ✅ 建议家属将事件清单作为**就诊参考资料**，由专科医生结合 PSG（多导睡眠图）等专业检查最终判定

> 仅输出基于视觉与音频的客观行为事件统计，**不构成 RBD / 帕金森病 / 阿尔茨海默病 / 睡眠呼吸暂停等任何医学诊断**；任何疑似神经退行性疾病或睡眠障碍的判定与治疗必须由神经内科 / 睡眠专科医生结合 PSG 等专业检查制定。
