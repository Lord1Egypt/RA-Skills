# API 接口文档

此处用于存放焦虑症相关行为（搓手、咬指甲、来回踱步）识别 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动焦虑症相关行为识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取焦虑相关行为统计 + 焦虑行为指数
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史焦虑行为记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_ANXIETY_BEHAVIOR_RECOGNITION_ANALYSIS` - 焦虑症相关行为（搓手、咬指甲、来回踱步）识别

## 输入约束

- 摄像头：家庭书房 / 客厅 / 办公室 / 心理咨询室 / 学校教室固定摄像头，**能看到上半身（含手部）+ 完整下肢踱步路径**
- 帧率 ≥ 15 FPS（推荐 20-30 FPS，捕捉手部细微反复动作）；分辨率 ≥ 720p；光照稳定
- 视频时长建议 ≥ 5 分钟，过短样本无法统计频次趋势
- 踱步识别需保证摄像头能看到 ≥ 2-3 米的可行走区域，否则无法判定"折返"
- 多人场景需按目标跟踪，避免身份串扰
- 隐私敏感场景必须启用人体轮廓 + 面部马赛克模式

## 关键观测信号

### 手部行为
- `hand_rubbing_event_count` - 手部搓揉事件次数（双手反复摩擦）
- `hand_rubbing_total_duration_sec` - 搓手总持续时长
- `nail_biting_event_count` - 指甲啃咬事件次数（手部接近嘴部 + 啃咬动作）
- `nail_biting_total_duration_sec` - 咬指甲总持续时长

### 移动行为
- `pacing_event_count` - 来回踱步事件次数（狭小区域内反复折返）
- `pacing_total_duration_sec` - 踱步总持续时长
- `pacing_loop_count` - 折返次数（单次踱步内的来回次数）

### 综合
- `analysis_window_min` - 统计时间窗（分钟）
- `subject_count` - 画面中人数
- `anxiety_behavior_index` - 焦虑行为指数（0-100，综合三类行为频次/时长/强度）
- `baseline_window_days` - 个人基线窗口（默认 7-14 天）
- `delta_vs_baseline_pct` - 相对基线变化百分比

## 阈值与等级

- `< 30` - 低焦虑表现（calm）
- `30-50` - 中等焦虑表现（mild）
- `50-75` - 较高焦虑表现（notable）→ 推送放松练习提醒
- `> 75` - 高焦虑表现（high）→ 建议寻求专业帮助
- 一次性短暂行为（如紧张前的搓手 30 秒）不应触发高焦虑报警，建议结合多个时间窗均值

## 输出字段（参考）

- `subject_count` / `analysis_window_min`
- `hand_metrics` - 手部行为统计
- `pacing_metrics` - 踱步行为统计
- `behavior_event_timeline` - 行为事件时间线（用于趋势可视化）
- `anxiety_behavior_index` - 焦虑行为指数
- `baseline_comparison` - 与个人基线对比
- `anxiety_level` - 焦虑表现等级（calm / mild / notable / high）
- `dominant_behavior` - 当前最突出的焦虑行为（hand_rubbing / nail_biting / pacing / mixed）
- `alert_type` - 提醒类型（anxiety_notable / anxiety_high / improving / normal）
- `alert_level` - 提醒级别（info / notice / warning）
- `self_care_suggestion` - 自我关怀建议文本（如"您今日焦虑行为较多，建议进行 5 分钟深呼吸或正念练习"）
- `recommend_action` - 建议动作（push_relaxation_reminder / suggest_breathing_exercise / suggest_walk_outdoors / suggest_seek_professional_help / observe_only）
- `helpline_reference` - 当 high 等级时附**全国心理援助热线 400-161-9995** 等参考资源

## 强制约束与红线

- ❌ **禁止**输出焦虑症诊断、焦虑量表评分（如 GAD-7、SAS、HAMA）、用药建议或处方
- ❌ **禁止**将"焦虑行为指数高"等同于"确诊焦虑症"
- ❌ **禁止**长期存储原始视频
- ❌ **禁止**在未经本人同意时向第三方推送其个人焦虑数据
- ✅ 强调"行为自我觉察辅助"定位，由用户本人决定是否就医

> 仅输出基于视觉的客观行为统计与自我觉察提醒，**不构成焦虑症诊断、量表评分或治疗方案**；任何焦虑症确诊与治疗必须由精神科医生 / 心理治疗师评估制定；若伴有持续胸闷、心悸、惊恐发作等躯体化症状，请及时就医或拨打**全国心理援助热线 400-161-9995**。
