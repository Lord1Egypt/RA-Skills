# API 接口文档

此处用于存放孕妇情绪波动舒缓 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动孕妇情绪波动检测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取情绪波动事件 + 舒缓动作清单
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史舒缓记录清单
4. `/health/order/api/getReportDetailExport?id={id}` - 导出孕期情绪舒缓日志报告
5. （可选）`/web/companion/v2/trigger-soothing-action` - 触发联动舒缓动作（智能音箱播放舒缓音乐 / 正念引导音频 / 丈夫 APP 推送提醒）

## 场景代码

- `SMYX_PREGNANCY_EMOTION_SOOTHING_ANALYSIS` - 孕妇情绪波动舒缓

## 输入约束

- 摄像头：孕妇家中常驻活动区域（客厅 / 卧室 / 书房）或产检候诊室固定摄像头
- 帧率 ≥ 10 FPS；分辨率 ≥ 720p；优先正面或 30° 内侧脸
- 音频可选：采样率 ≥ 16kHz（用于哭声 / 对话语气 / 抽噎识别）；若不接入麦克风，仅依赖视觉信号
- 时段：可全天运行（默认 07:00 - 23:00），夜间睡眠时段自动暂停
- 多孕妇家庭/候诊室按目标跟踪绑定到注册孕妇 ID（每位孕妇独立基线）
- 孕妇本人必须授权部署，并明确告知同住家人；候诊室部署需医院公示

## 关键观测信号

### 音频（可选）
- `crying_continuous_sec` - 持续哭声/抽噎时长
- `crying_intensity` - 哭声强度（0-100）
- `voice_tone_score` - 对话语气评分（急促 / 不耐烦 / 平稳）
- `whimper_event_count` - 呜咽 / 抽噎事件
- `silent_duration_min` - 累计静默时长（无对话）

### 视频（核心）
- `sudden_crying_event` - 突然哭泣事件（面部流泪 + 嘴角下拉 + 眼部红肿）
- `frown_event_count` - 皱眉事件次数
- `anxiety_facial_score` - 焦虑面部评分（0-100）
- `pacing_back_forth_event` - 来回踱步事件
- `hand_tension_detected` - 手部紧张动作（搓手 / 攥拳）
- `long_silent_sitting_min` - 长时间静坐不语（连续 ≥ 30 分钟无社交互动/手机/阅读等活动）
- `social_interaction_event_count` - 期间社交互动次数（与他人对话/手机/阅读）

## 场景判定

- `pregnancy_emotion_none` - 情绪平稳
- `pregnancy_emotion_mild` - 轻度波动（短暂皱眉 / 短时静默 / 偶发抽噎）
- `pregnancy_emotion_crying` - 突然哭泣事件
- `pregnancy_emotion_anxiety` - 焦虑烦躁（皱眉 + 踱步 + 手部紧张）
- `pregnancy_emotion_isolation` - 长时间静坐不语（≥ 30 min 无社交活动）
- `pregnancy_emotion_strong` - 显著情绪波动（多项叠加）

## 4 级舒缓策略递进

- Level 1（mild）：智能音箱低音量播放孕期舒缓音乐（≤ 35 dB）
- Level 2（moderate）：切换正念引导音频（呼吸引导 / 冥想），并轻柔环境光辅助
- Level 3（crying / anxiety / isolation）：在 Level 2 基础上向丈夫手机 APP 推送提醒"妻子情绪波动，请打电话关心"
- Level 4（strong / 持续不缓解）：紧急推送丈夫/紧急联系人，并建议联系产检医生或心理热线

## 单日动作上限

- mild × 8 / moderate × 5 / strong × 3 / Level 4 不设上限

## 红线约束

- 禁止做"孕期抑郁症 / 焦虑障碍 / 产前抑郁"等医学诊断
- 禁止长期存储孕妇隐私音视频（≤ 7 天，仅入库情绪波动片段）
- 禁止用于商业广告 / AI 训练；禁第三方共享
- 禁止舒缓音量 > 40 dB
- 严禁 AI 克隆 / 合成丈夫或家人声音冒充本人录音
- 候诊室场景：必须公示告知，提供退出机制
