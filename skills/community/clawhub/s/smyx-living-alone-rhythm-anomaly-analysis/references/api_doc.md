# API 接口文档

此处用于存放独居者作息规律异常分析 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动独居者作息规律异常分析任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取作息分析结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史作息记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_LIVING_ALONE_RHYTHM_ANOMALY_ANALYSIS` - 独居者作息规律异常分析

## 输入约束

- 摄像头：家庭客厅或卧室固定摄像头，覆盖独居者夜间主要活动区域
- **必须支持低光/红外/微光夜视模式**，能在熄灯后继续采集人体活动
- 视频时段建议覆盖 22:00 - 次日 06:00 完整夜间
- 帧率 ≥ 5 FPS（人体活动检测无需高帧率）
- 隐私敏感场景应做马赛克处理（仅识别人体轮廓即可）

## 关键观测信号

- `lights_off_time` - 当晚熄灯时间（本地时间，HH:MM）
- `lights_off_brightness_delta` - 熄灯时画面亮度突降幅度
- `presence_in_bed_after_lights_off_sec` - 熄灯后留在床上的时长（秒）
- `early_morning_motion_count` - 0-6 点期间人体活动事件次数
- `early_morning_motion_duration_sec` - 0-6 点期间累计活动时长（秒）
- `total_dark_motion_events` - 全夜熄灯后总活动次数

## 历史基线字段

- `baseline_window_days` - 基线时间窗口（默认 7-14 天）
- `baseline_lights_off_time_avg` - 历史平均熄灯时间
- `baseline_early_morning_motion_avg` - 历史平均凌晨活动次数
- `baseline_early_morning_motion_std` - 历史凌晨活动次数标准差

## 默认异常阈值（可由调用方覆盖）

- 熄灯延迟阈值：当晚熄灯时间 比基线晚 **> 2 小时**
- 凌晨活动异常阈值：凌晨活动次数 **超过基线均值 + 2 × 标准差**
- 持续天数阈值：异常连续出现 **≥ 2 天** 才推送家属（避免单次偶发）

## 异常类型

- `late_lights_off` - 熄灯显著延迟
- `frequent_early_morning_motion` - 凌晨活动频次显著增多
- `prolonged_dark_motion` - 凌晨累计活动时长过长
- `combined_rhythm_disruption` - 多项异常同时出现（更高优先级）

## 输出字段（参考）

- `subject_detected` - 是否检测到独居者
- `current_metrics` - 当晚作息指标（lights_off_time / early_morning_motion_count / early_morning_motion_duration_sec）
- `baseline_metrics` - 历史基线指标（baseline_lights_off_time_avg / baseline_early_morning_motion_avg / baseline_early_morning_motion_std）
- `deviation` - 当晚相对基线的偏差（delta_lights_off_hours / motion_z_score）
- `anomaly_type` - 异常类型
- `anomaly_continuous_days` - 异常连续天数
- `alert_level` - 提醒级别（notice / warning / urgent）
- `alert_message` - 推送给家属的文本（如"老人近 3 晚平均凌晨 2 点才熄灯，且凌晨活动次数从 1.2 上升至 5 次，建议电话关心是否睡眠/身体不适"）

> 仅输出基于视觉的作息参数与偏离提示，不提供失眠症、抑郁症、夜间谵妄等具体医学诊断；连续异常建议由家属/社区/医生进一步评估。
