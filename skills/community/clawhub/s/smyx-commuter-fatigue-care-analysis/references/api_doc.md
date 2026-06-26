# API 接口文档

此处用于存放上班族下班疲劳关怀（回家时刻） API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动下班回家疲劳关怀检测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取疲劳指数 + 关怀动作建议
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史关怀记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出周/月疲劳趋势报告
5. （可选）`/web/companion/v2/trigger-comfort-action` - 触发联动关怀动作（智能音箱关怀语 / 舒缓音乐 / 智能灯调暖光）

## 场景代码

- `SMYX_COMMUTER_FATIGUE_CARE_ANALYSIS` - 上班族下班疲劳关怀（回家时刻）

## 输入约束

- 摄像头：智能家居客厅 / 单身公寓 / 家庭起居室固定摄像头，能拍到沙发与玄关进门区域
- 帧率 ≥ 10 FPS（推荐 15 FPS，便于面部细节）；分辨率 ≥ 720p
- 音频（可选，推荐）：用于识别叹气声 + 自言自语抱怨；采样率 ≥ 16kHz
- 触发窗口：用户**进门 → 30 分钟**（自动检测进门事件 entry_event）
- 工作日识别：仅在用户配置的**工作日下班时段**（默认周一至周五 17:00-22:00）启用，周末/请假/节假日自动暂停
- 多人家庭按目标跟踪绑定到注册"上班族"标签的用户 ID
- 隐私优先：仅记录**疲劳事件聚合指标**，不存储原始视频

## 关键观测信号

### 姿态（核心）
- `slouch_recline_detected` - 瘫坐/斜躺（**背部与沙发夹角 > 120°** 或 躯干与大腿夹角 > 120°）
- `slouch_recline_duration_min` - 瘫坐/斜躺持续时长
- `lying_flat_on_sofa` - 平躺沙发（强疲劳信号）
- `head_drooped_forward` - 低头垂头姿态
- `time_from_entry_to_slouch_sec` - 进门到瘫坐的时间（越短越疲劳）

### 面部（核心）
- `eye_bag_visibility_score` - 眼袋显著程度（0-100）
- `mouth_corner_down_score` - 嘴角下垂程度（0-100）
- `frequent_blinking_rate_per_min` - 每分钟眨眼次数（疲劳时显著增高）
- `eye_closure_micro_sleep_event` - 微睡眠/打盹事件（闭眼 > 1.5 秒）
- `yawn_event_count` - 哈欠次数
- `neutral_blank_face_ratio` - 木然/呆滞面部比例

### 行为
- `sigh_visual_event_count` - 视觉叹气次数（胸腹快速起伏 + 长呼气姿态）
- `sigh_audio_event_count` - 音频叹气事件（可选）
- `rubbing_temple_or_eyes_event` - 揉太阳穴/揉眼次数（疲劳缓解动作）
- `phone_scroll_passive_min` - 被动刷手机时长（参考指标）
- `food_or_drink_action_event` - 进食/喝水主动行为（**正向指标**：自我照顾）
- `stretch_or_exercise_event` - 伸展/活动事件（**正向指标**）

### 上下文
- `entry_timestamp` - 进门时间戳
- `analysis_window_min` - 当前分析窗口（默认 30 min）
- `weekday_workday_status` - 是否为工作日

## 阈值与疲劳等级（默认值，可在配置中覆盖）

- `fatigue_index 0-29` - **light**（轻度疲劳）→ 不主动介入
- `fatigue_index 30-49` - **mild**（明显疲劳）→ 调暖光 + 极轻舒缓音乐
- `fatigue_index 50-69` - **notable**（较高疲劳）→ 温和关怀语音（"辛苦啦，先喝杯水吧~"）+ 舒缓音乐
- `fatigue_index 70-100` - **heavy**（重度疲劳）→ 关怀语音 + 推荐自我照顾动作清单（5 分钟肩颈拉伸 / 热水澡 / 早睡）
- 连续 ≥ 5 个工作日 fatigue_index ≥ 60 → 提示**累积性疲劳预警**，建议关注休息节奏

## 输出字段（参考）

- `event_id` / `entry_timestamp` / `analysis_window_min` / `user_id`
- `posture_signals` / `face_signals` / `behavior_signals` / `context`
- `fatigue_index` - 疲劳指数（0-100，含正向行为扣分）
- `fatigue_level` - 疲劳等级（light / mild / notable / heavy）
- `consecutive_high_workdays` - 连续高疲劳工作日数
- `comfort_actions` - 关怀动作列表（每项含 action_type / message / target / volume_db / brightness_lux / color_temp，例如：
    - `{action_type: "smart_light_warm_dim", brightness_lux: 80, color_temp: "warm_2700K", target: "living_room_light"}`
    - `{action_type: "play_soothing_music", message: "钢琴轻音乐 15 分钟（建议《River Flows in You》）", volume_db: 35, target: "living_room_speaker"}`
    - `{action_type: "smart_speaker_gentle_voice", message: "今天辛苦啦，先喝杯水休息一下吧~ 想我给你放点轻音乐吗？", volume_db: 40, target: "living_room_speaker"}`
    - `{action_type: "selfcare_tips_card", message: "今天疲劳指数较高，建议：1) 5 分钟肩颈拉伸 2) 一杯温水 3) 洗个热水澡 4) 早点睡哦~", target: "tv_card / phone_app"}`）
- `recommend_action` - 建议动作（trigger_warm_light / trigger_soothing_music / play_gentle_voice / push_selfcare_tips / observe_only）
- `weekly_trend_summary` - 每周日晚 22:00 自动生成本周疲劳趋势摘要

## 强制约束与红线

- ❌ **禁止**做"职业倦怠 / 抑郁症 / 慢性疲劳综合征"等任何医学诊断
- ❌ **禁止**将疲劳数据上传到雇主、保险公司或任何第三方平台
- ❌ **禁止**长期存储原始视频；建议仅保留 ≤ 7 天且仅入库聚合指标
- ❌ **禁止**在用户明显需要独处时（连续 ≥ 2 次未应答关怀）继续主动介入
- ❌ **禁止**关怀语过度频繁，单晚关怀动作上限：mild × 1、notable × 2、heavy × 3
- ❌ **禁止**使用居高临下、说教、PUA 式的关怀文案（如"你怎么又这么累"、"应该早点睡"等指令式语气）
- ✅ **必须**支持用户：一键暂停今晚 / 暂停整周 / 永久退出 / 自定义关怀语和音乐 入口
- ✅ **必须**：关怀语音前给予 3 秒非语言提示（如柔和铃声），避免突兀
- ✅ **必须**关怀文案保持**平等、温柔、不指责**的伙伴语气
- ✅ 连续 ≥ 5 个工作日 fatigue_index ≥ 60 → 主动提示**关注休息**，并可在同意后联系紧急联系人或推荐**当地心理咨询/EAP**
- ✅ 关怀动作若 3 次未被理睬 → 自动进入静默模式 ≥ 2 小时

> 仅输出基于视觉与（可选）音频的客观疲劳事件检测与轻量关怀动作，**不构成任何医学诊断**；长期重度疲劳或情绪低落请咨询**职业心理咨询师**或**当地精神科**专业医师。
