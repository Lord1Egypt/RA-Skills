# API 接口文档

此处用于存放独居老人孤独情绪识别与温暖陪伴 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动独居老人孤独情绪识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取孤独指数 + 温暖陪伴动作建议
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史孤独情绪关怀报告
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告
5. （可选）`/web/companion/v2/trigger-comfort-action` - 触发联动温暖陪伴动作（智能音箱语音 / 子女 APP 推送）

## 场景代码

- `SMYX_ELDERLY_LONELINESS_COMFORT_ANALYSIS` - 独居老人孤独情绪识别与温暖陪伴

## 输入约束

- 摄像头：独居老人客厅 / 卧室 / 养老院单人房 / 日间照料中心固定摄像头，能看到老人主要活动区域
- 帧率 ≥ 5 FPS（推荐 10 FPS）；分辨率 ≥ 480p；夜间需红外补光
- 音频（可选，但强烈推荐）：用于识别叹气声 + 自言自语；采样率 ≥ 16kHz
- 视频时长：建议覆盖白天活跃时段（08:00 - 22:00），**单次分析建议 ≥ 4 小时**
- ROI 标定：主要活动区域（沙发区 / 餐桌 / 床位 / 阳台 / 厨房）
- **独居判定**：连续 ≥ 30 分钟画面中仅有老人一人 → independent_status = true（若有家人/护工进入即重置）
- 隐私敏感场景建议启用人体轮廓 + 面部马赛克模式

## 关键观测信号

### 行为
- `solo_duration_minutes` - 当前连续独处时长（无他人进入画面）
- `daily_solo_total_minutes` - 当日累计独处总时长
- `static_gaze_duration_minutes` - 长时间静止凝视一处（≥ 10 分钟，无肢体活动）
- `purposeful_activity_minutes` - 有目的活动总时长（做家务、看电视 + 笑/点头反馈、园艺、阅读等）
- `social_interaction_event_count` - 社交互动事件数（家人/护工进入、视频通话画面、宠物互动）

### 视觉
- `sigh_visual_event_count` - 视觉叹气次数（胸腹快速起伏伴长呼气姿态）
- `talking_to_self_event_count` - 自言自语视觉事件次数（口部活动但无对话对象在场）
- `frown_neutral_face_ratio` - 皱眉/木然面部比例（参考指标）
- `smile_event_count_daily` - 当日笑容次数（正向指标）

### 音频（可选）
- `sigh_audio_event_count` - 音频叹气事件
- `talking_to_self_audio_event_count` - 自言自语音频事件
- `singing_humming_event_count` - 哼歌/唱歌事件（**正向指标**，孤独指数 ↓）
- `phone_call_minutes` - 电话/视频通话时长（正向指标）

### 综合
- `loneliness_index` - 孤独指数（0-100，**正向行为会扣分**）
- `comparison_to_baseline_pct` - 与个人 14 天基线对比

## 阈值与等级（默认值，可在配置中覆盖）

- `loneliness_index 0-29` - light（轻度，正常社交）→ 不干预
- `loneliness_index 30-49` - mild（轻度孤独）→ 建议温和陪伴（播放老歌）
- `loneliness_index 50-69` - notable（较明显孤独）→ 主动播放子女预录温馨语音 + 子女 APP 提示
- `loneliness_index 70-100` - heavy（重度孤独）→ 强力关怀（推送子女建议本周视频通话或回家探望 + 社区义工提醒）
- 连续 ≥ 4 小时无社交互动 + 静止凝视 ≥ 1 小时 + 叹气 ≥ 5 次 → 升级提醒

## 输出字段（参考）

- `time_window` / `independent_status`
- `behavioral_metrics` / `visual_metrics` / `audio_metrics`（音频可选）
- `loneliness_index` / `loneliness_level`
- `comparison_to_baseline_pct` / `consecutive_high_days` - 连续高指数天数
- `alert_type` - 提醒类型（light_no_action / mild_comfort_audio / notable_comfort_plus_app / heavy_strong_care / improving）
- `alert_level` - 提醒级别（info / notice / warning）
- `comfort_actions` - 温暖陪伴动作列表（每项含 action_type / message / target，例如：
    - `{action_type: "smart_speaker_voice", message: "妈妈，是小芳，我今天忙完了打给您哈，您先听听咱俩去年录的那段~", target: "living_room_speaker"}`
    - `{action_type: "play_favorite_song", message: "邓丽君《月亮代表我的心》", target: "living_room_speaker"}`
    - `{action_type: "children_app_push", message: "今天母亲显得有些孤独，建议视频通话或回家陪伴", target: "child_phone_app"}`）
- `family_summary` - 给子女的友好摘要（如"今天母亲在客厅独处 6 小时，下午 14:30-15:20 期间静坐凝视窗外约 50 分钟、叹气 7 次，孤独指数 72；已为她播放邓丽君老歌并推送了您预录的语音，建议晚上视频通话，或周末抽空回家陪她吃顿饭"）
- `recommend_action` - 建议动作（trigger_smart_speaker_comfort / push_children_video_call_suggestion / suggest_community_volunteer_visit / observe_only）
- `community_resource` - 当 heavy 且子女长期无回应时，附**当地社区日间照料 / 街道老龄办** 资源提示

## 强制约束与红线

- ❌ **禁止**输出"老年抑郁症 / 孤独症"等任何精神医学诊断或量表评分
- ❌ **禁止**未经老人本人**和**子女双方同意便部署摄像头
- ❌ **禁止**将老人视频/音频用于商业广告或大数据画像
- ❌ **禁止**长期存储老人原始视频；建议仅保留 ≤ 7 天，且仅留聚合指标
- ❌ **禁止**强迫推送频率过高，避免老人对智能音箱产生抵触
- ✅ **必须**在每个智能音箱发声前给予 3 秒"今天为您播放……"温和前导，避免突兀惊吓
- ✅ **必须**支持老人一句话关闭今日提醒（如"好啦，我没事"）
- ✅ 当孤独指数持续 ≥ 70 但子女连续 ≥ 3 天无回应时，主动提示**社区/街道老龄办**资源
- ✅ 子女预录语音必须由子女本人录制，**禁止**使用 AI 克隆/合成子女声音冒充

> 仅输出基于视觉与（可选）音频的客观行为统计与温暖陪伴动作，**不构成老年抑郁症等精神医学诊断**；任何疑似心理健康问题应转介当地老年精神科或社区心理服务，最终评估由专业医师作出。
