# API 接口文档

此处用于存放儿童睡前情绪安抚（怕黑/噩梦后） API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动儿童睡前情绪安抚检测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取不安事件 + 安抚动作清单
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史安抚记录清单
4. `/health/order/api/getReportDetailExport?id={id}` - 导出夜间安抚日志报告
5. （可选）`/web/companion/v2/trigger-soothing-action` - 触发联动安抚动作（小夜灯 / 智能音箱故事 / 摇篮曲 / 家长 APP 推送）

## 场景代码

- `SMYX_CHILD_BEDTIME_SOOTHING_ANALYSIS` - 儿童睡前情绪安抚（怕黑/噩梦后）

## 输入约束

- 摄像头：儿童卧室 / 婴儿房固定摄像头，**必须支持红外夜视**，能看到床上区域
- 帧率 ≥ 10 FPS；分辨率 ≥ 720p；红外波段建议 850 nm（对睡眠干扰小）
- 音频**必需**：采样率 ≥ 16kHz（用于哭声 / "妈妈" 呼喊 / 尖叫识别）
- 时段：仅在配置的**睡眠窗口**内启用（默认 19:00 - 07:00），白天自动暂停
- 多孩家庭按目标跟踪绑定到注册儿童 ID（每个孩子独立基线）
- 婴儿（≤ 12 月）必须额外开启**婴儿专用模式**：阈值更敏感、安抚动作更轻柔、必要时同步唤醒家长
- 家长必须授权部署，并明确告知家庭其他成员（如保姆、外祖父母）

## 关键观测信号

### 音频（核心）
- `crying_continuous_sec` - 持续哭声时长
- `crying_intensity` - 哭声强度（0-100，结合分贝 + 频谱情绪）
- `call_mom_dad_count` - 呼喊"妈妈/爸爸/妈咪"次数
- `scream_event_count` - 尖叫事件次数（突发高频高强度声）
- `whimper_event_count` - 呜咽 / 抽噎事件（轻度不安信号）
- `sleep_breathing_regular` - 呼吸节奏规律性（参考指标，区分睡熟 vs 醒着）

### 视频（核心）
- `body_curl_up_detected` - 蜷缩抱腿姿态（怕黑典型表现）
- `looking_around_event_count` - 四处张望次数（黑暗中睁眼搜索）
- `sudden_sit_up_event` - 突然坐起事件（噩梦惊醒典型）
- `trembling_visual_detected` - 肢体颤抖（恐惧伴随）
- `hugging_plush_toy` - 主动抱毛绒玩具（自我安抚行为，参考）
- `pull_cover_over_head` - 拉被子蒙头（怕黑参考）
- `out_of_bed_event` - 下床事件（独立优先级，避免摔伤）

### 上下文
- `is_within_sleep_window` - 是否在睡眠窗口内
- `time_since_last_soothing_min` - 距离上次安抚动作的时间

## 场景判定与不安等级

- **bedtime_unrest_mild** - 睡前不安（轻度）：呜咽 / 抱毛绒玩具 / 蜷缩，无哭喊
- **bedtime_unrest_crying** - 睡前哭闹：持续哭声 ≥ 30 秒 或 呼喊"妈妈/爸爸" ≥ 2 次
- **dark_fear** - 怕黑：蜷缩 + 四处张望 + 蒙头/抱玩具 任两项 + 在卧室关灯后 ≤ 30 分钟内
- **nightmare_wakeup** - 噩梦惊醒：突然坐起 + 尖叫/急促哭声 + 颤抖 任两项
- **out_of_bed_safety** - 下床（独立优先级）：触发家长 APP 推送 + 调亮小夜灯，避免摔伤
- **none** - 无不安信号 / 在睡熟状态

## 安抚动作策略（轻 → 重逐级递进）

- **Level 1（mild）**：极柔小夜灯（≤ 5 lux 暖光）+ 极轻摇篮曲（≤ 35 dB）
- **Level 2（moderate）**：小夜灯（≤ 10 lux 暖光）+ **妈妈预录故事** / 白噪音
- **Level 3（strong：noctmare/scream）**：小夜灯（≤ 20 lux）+ 妈妈预录"宝贝，妈妈在这里，做了梦对吗？没事了哦~"语音 + **同时推送家长 APP** "noctmare 提醒，建议过去陪伴"
- **Level 4（out_of_bed/persist ≥ 5min）**：**立即推送家长 APP + 主屏震动**，建议家长亲自到场，AI 仅辅助

- 升级条件：同一信号在 Level 1/2 安抚后 ≥ 3 分钟未平复 → 自动升级一级
- 单晚同一儿童安抚动作触发**上限**：mild × 5、moderate × 3、strong × 2、Level 4 不设上限（安全优先）

## 输出字段（参考）

- `event_id` / `event_timestamp` / `child_id` / `child_age_band`（infant ≤12m / toddler 1-3y / preschool 3-6y / school 6-12y）
- `scene_label` - 场景判定（bedtime_unrest_mild / bedtime_unrest_crying / dark_fear / nightmare_wakeup / out_of_bed_safety / none）
- `audio_signals` / `video_signals` / `context`
- `unrest_level` - 不安等级（mild / moderate / strong / out_of_bed）
- `soothing_actions` - 安抚动作列表（每项含 action_type / message / target / level / volume_db / brightness_lux，例如：
    - `{action_type: "night_light_on", brightness_lux: 5, color_temp: "warm_2700K", target: "child_room_light", level: 1}`
    - `{action_type: "play_mom_recorded_story", message: "妈妈预录《晚安月亮》故事 5 分钟", volume_db: 35, target: "child_room_speaker", level: 2}`
    - `{action_type: "play_lullaby", message: "《摇啊摇》摇篮曲", volume_db: 30, target: "child_room_speaker", level: 2}`
    - `{action_type: "play_white_noise", message: "白噪音雨声", volume_db: 30, target: "child_room_speaker", level: 2}`
    - `{action_type: "parent_app_push", message: "孩子刚被噩梦惊醒，已轻声安抚中，建议过去陪伴", target: "parent_phone_app", level: 3}`
    - `{action_type: "parent_app_urgent_push", message: "⚠️ 孩子已下床，请立即查看", target: "parent_phone_app", level: 4}`）
- `effectiveness_after_3min` - 3 分钟后效果（settled / partially_settled / unchanged / escalated）
- `nightly_summary` - 当晚汇总（次日清晨自动生成：不安事件次数 + 类型分布 + 安抚成功率 + 建议）
- `recommend_action` - 建议动作（trigger_level_N_soothing / push_parent_app / urgent_parent_intervention / observe_only）

## 强制约束与红线

- ❌ **禁止**对儿童做任何"睡眠障碍 / 夜惊症 / 焦虑症"等医学诊断
- ❌ **禁止**长期存储儿童夜间视频；建议仅保留 ≤ 7 天 + 仅入库不安事件片段
- ❌ **禁止**将儿童夜间视频/音频用于商业广告、AI 训练数据集
- ❌ **禁止**向家长以外的第三方共享（亲戚需家长授权才能查看）
- ❌ **禁止**夜间使用冷白光（≥ 4000K）或亮度 > 30 lux 的小夜灯，会打断褪黑素分泌
- ❌ **禁止**安抚音量超过 40 dB（接近耳语水平），避免影响睡眠或惊醒孩子
- ❌ **禁止**使用 AI 克隆/合成妈妈/爸爸声音冒充家长录音；预录语音**必须由家长本人录制**
- ❌ **禁止**对 **out_of_bed** 事件仅做"语音安抚"——必须立即推送家长 APP（避免摔伤）
- ✅ **必须**婴儿（≤ 12 月）开启专用模式：阈值更敏感 + 安抚更轻柔 + **strong 及以上必须同步唤醒家长**
- ✅ **必须**为家长提供：一键暂停今晚 / 调整睡眠窗口 / 永久退出 入口
- ✅ **必须**：噩梦惊醒后**首条安抚语**应为家长本人预录的稳定语音（不用合成音）
- ✅ 当夜噩梦惊醒 ≥ 3 次或连续 7 晚反复发生 → 提示家长**当地儿童心理门诊**或**儿科睡眠门诊**资源
- ✅ 当晚汇总报告必须**只在次日清晨**发送（避免家长夜里被唤醒焦虑加深）

> 仅输出基于音视频的客观不安事件检测与轻柔安抚动作，**不构成任何儿童睡眠/心理医学诊断**；频繁夜惊或长期睡眠困难请咨询当地**儿科睡眠门诊**或**儿童心理科**专业医师。
