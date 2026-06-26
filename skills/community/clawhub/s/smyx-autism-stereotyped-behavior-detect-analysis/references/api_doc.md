# API 接口文档

此处用于存放自闭症儿童刻板行为识别（转圈/摆手）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动自闭症儿童刻板行为识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取刻板行为统计结果
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史行为记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_AUTISM_STEREOTYPED_BEHAVIOR_DETECT_ANALYSIS` - 自闭症儿童刻板行为识别（转圈/摆手）

## 输入约束

- 摄像头：康复机构 / 特殊教育学校 / 家庭固定摄像头，覆盖儿童主要活动区域，**能看到全身**
- 帧率 ≥ 10 FPS（推荐 15-30 FPS）；分辨率 ≥ 480p；光照稳定
- 多儿童场景下建议结合外观特征锁定主目标（如儿童穿着特定颜色衣物）
- 视频时长建议 ≥ 5 分钟，时序动作识别窗口需要足够样本
- 隐私敏感场景可启用人体骨架模式

## 刻板行为类别（支持扩展）

| behavior_class | 中文 | 识别要点 |
|----------------|------|----------|
| `spinning` | 转圈 | 身体围绕垂直轴连续旋转 ≥ 360° |
| `hand_flapping` | 摆手 | 手臂/手腕非功能性高频重复摆动 |
| `body_rocking` | 摇晃 | 躯干前后/左右有节律摆动 |
| `head_banging` | 撞头 | 头部反复触碰墙/家具（高优先级） |
| `finger_flicking` | 手指弹打 | 手指反复快速弹打 |
| `toe_walking` | 踮脚走 | 持续脚尖着地走路 |
| `repetitive_running` | 重复奔跑 | 沿固定路线反复短距离奔跑 |
| `repetitive_object_play` | 重复操作物体 | 反复开关、拍打、排列固定物体 |

## 关键观测指标

- `subject_detected` - 是否检测到儿童
- `pose_keypoints_visible` - 关键点是否充分可见
- `behavior_events` - 行为事件列表（含 behavior_class / start_time / end_time / duration_sec / confidence）
- `per_class_count_hourly` - 每类行为每小时频次（次/小时）
- `per_class_total_duration_today_sec` - 每类行为当日累计持续时间
- `total_stereotyped_duration_today_sec` - 当日累计所有刻板行为时长
- `dominant_behavior_class` - 当日主导刻板行为类别

## 历史基线字段（可选）

- `baseline_window_days` - 基线窗口（默认 7-14 天）
- `baseline_per_class_avg_hourly` - 各类行为每小时基线均值
- `baseline_per_class_std_hourly` - 各类行为每小时标准差

## 输出字段（参考）

- `subject_detected` / `pose_keypoints_visible`
- `behavior_events` - 完整事件序列
- `summary_metrics` - 汇总指标（per_class_count_hourly / per_class_total_duration_today_sec / total_stereotyped_duration_today_sec / dominant_behavior_class）
- `trend_vs_baseline` - 当前 vs 基线变化（per_class_delta_pct）
- `intervention_hint` - 用于康复师/家长的方向性参考（descriptive_only，**不构成处方**）
- `report_message` - 文本摘要（如"今日转圈 14 次，摆手 23 次，相比基线下降 30%，建议康复师评估当前干预方案"）

> 仅输出基于视觉的客观行为统计，**不提供自闭症诊断、量表打分、康复处方**；任何诊断与干预方案必须由专业医生/认证康复治疗师评估制定。
