# API 接口文档

此处用于存放儿童开心时刻识别与正向激励 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动儿童开心时刻识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取开心事件清单 + 抓拍片段 + 鼓励语
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史快乐合集
4. `/health/order/api/getReportDetailExport?id={id}` - 导出每日/每周快乐合集
5. （可选）`/web/companion/v2/trigger-positive-reinforcement` - 触发即时鼓励音效（智能音箱 / 儿童手表）

## 场景代码

- `SMYX_CHILD_HAPPY_MOMENT_CAPTURE_ANALYSIS` - 儿童开心时刻识别与正向激励

## 输入约束

- 摄像头：家庭客厅 / 幼儿园教室 / 游乐场 / 亲子活动中心固定摄像头，能拍到儿童面部和全身
- 帧率 ≥ 10 FPS（推荐 15-25 FPS，便于抓拍清晰快照）；分辨率 ≥ 720p（推荐 1080p）
- 音频（可选，但强烈推荐）：用于识别笑声强度；采样率 ≥ 16kHz
- 视频时长：实时流接入；离线分析单段建议 ≥ 5 分钟
- 抓拍前后**各 2 秒**短视频片段，照片 ≥ 1080p
- 多人场景需按目标跟踪绑定到家庭注册儿童 ID（家庭场景）或匿名儿童编号（公共场景）
- 公共场景（幼儿园/游乐场）**必须**确保所有出现儿童的家长**预先签署影像采集同意书**

## 关键观测信号

### 面部表情
- `big_smile_intensity` - 大笑强度（嘴角上翘幅度 + 眼睛眯成月牙 + 露牙 综合分 0-100）
- `genuine_smile_detected` - 杜兴式真笑判定（嘴 + 眼周肌肉同时收缩 = Duchenne smile）
- `smile_duration_sec` - 单次笑容持续时长

### 肢体动作
- `jumping_event_count` - 蹦跳次数（双脚同时离地）
- `clapping_event_count` - 拍手次数（双手有节奏拍击 ≥ 2 次）
- `dancing_or_twirling_event` - 跳舞/转圈事件（参考指标）
- `hug_event_count` - 拥抱事件次数（与家人/小朋友）
- `arms_raised_celebration_event` - 双手高举庆祝（如赢得游戏）

### 音频（可选）
- `laughter_audio_intensity` - 笑声音频强度（dB + 频谱欢快度）
- `cheer_or_excited_voice_count` - 欢呼/兴奋声次数

### 上下文
- `social_context` - 社交上下文（with_parent / with_peer / with_teacher / alone_play）
- `triggered_by` - 触发上下文（praise_from_adult / new_toy / game_win / pet_interaction / unknown，**仅用于推送文案，不做记录**）

## 抓拍触发规则（多信号融合，避免误抓）

- **happy_event_triggered = true** 需满足以下任一组合：
    1. `big_smile_intensity ≥ 70` 且 `smile_duration_sec ≥ 1.5`
    2. `jumping_event_count` 单次 + `genuine_smile_detected = true`
    3. `clapping_event_count ≥ 2` + `laughter_audio_intensity ≥ 阈值`
    4. `arms_raised_celebration_event = true` + `cheer_or_excited_voice_count ≥ 1`
- **happy_event_intensity_level** - 开心强度（mild / notable / peak）

## 输出字段（参考）

- `event_id` / `event_timestamp` / `child_id`（家庭注册儿童 / 公共场景匿名编号）
- `social_context` / `triggered_by`
- `signal_breakdown` - 信号详情（面部 + 肢体 + 音频）
- `happy_event_intensity_level` - 强度（mild / notable / peak）
- `snapshot_photo_url` - 高清抓拍照片 URL（关键瞬间帧，建议家长可一键删除）
- `clip_video_url` - 前后 2 秒短视频片段 URL
- `encouragement_action` - 鼓励动作（每项含 action_type / message / target，例如：
    - `{action_type: "smart_speaker_voice", message: "宝贝你真棒！妈妈/爸爸看到了哦~", target: "living_room_speaker"}`
    - `{action_type: "play_celebration_sound", message: "欢快音效 1.5 秒（避免突兀过响）", target: "living_room_speaker"}`
    - `{action_type: "parent_app_push", message: "📸 抓拍到宝贝的开心瞬间！正在游乐场和小伙伴拍手大笑~", target: "parent_phone_app"}`）
- `daily_happiness_collection` - 当日快乐合集（每日 22:00 自动汇总当日 ≥ notable 的事件）
- `weekly_happiness_collection` - 每周快乐合集（每周日晚 21:00 自动生成 3-5 段精选回顾）
- `recommend_action` - 建议动作（push_snapshot_to_parent / generate_daily_collection / generate_weekly_collection / play_encouragement_audio）

## 强制约束与红线

- ❌ **禁止**对儿童做"性格内向 / 外向 / 高情商 / 抑郁倾向"等任何心理评估或贴标签
- ❌ **禁止**将儿童影像用于商业广告、人脸识别训练数据集、AIGC 训练
- ❌ **禁止**向家长以外的第三方共享儿童影像（亲戚需家长授权才能查看）
- ❌ **禁止**长期存储未被家长保存的原始视频；建议未确认保存的抓拍片段 ≤ 7 天自动清理
- ❌ **禁止**在抓拍中保留疑似负面或尴尬瞬间（如哭泣、摔倒、衣物不整）即使误判
- ❌ **禁止**鼓励音效音量过响或频率过高，避免打断孩子专注力或形成依赖
- ✅ **必须**为家长提供：一键删除单个抓拍 / 暂停今日抓拍 / 永久退出该功能 的简单入口
- ✅ **必须**抓拍片段保存前由系统进行**安全审核**（仅露面+正向情绪+衣着整齐才入库）
- ✅ 公共场景必须**事先获得所有出场儿童的家长书面同意**，否则启用人脸马赛克
- ✅ 鼓励音效建议每次播放间隔 ≥ 5 分钟，**避免过度强化**形成"表演式快乐"

> 仅输出基于视觉与（可选）音频的客观开心瞬间识别和正向激励抓拍，**不构成任何心理评估或性格分析**；正向激励应作为亲子互动的暖心补充，**不能替代真实陪伴**。
