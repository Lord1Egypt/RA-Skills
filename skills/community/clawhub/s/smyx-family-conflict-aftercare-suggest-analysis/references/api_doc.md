# API 接口文档

此处用于存放夫妻/家人冲突后情绪缓和提示 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动冲突检测 + 平静窗口监测任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取冲突事件 + 冷静后缓和动作建议
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史冲突缓和提示事件清单
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整事件报告
5. （可选）`/web/companion/v2/trigger-aftercare-action` - 触发缓和动作（智能音箱轻柔音乐 / 家庭群关怀语推送）

## 场景代码

- `SMYX_FAMILY_CONFLICT_AFTERCARE_SUGGEST_ANALYSIS` - 夫妻/家人冲突后情绪缓和提示

## 输入约束

- 摄像头 + 麦克风：家庭客厅 / 厨房 / 餐厅等公共活动区域，**严禁部署在卧室、卫生间、儿童独立房间**
- 帧率 ≥ 5 FPS（推荐 10 FPS）；分辨率 ≥ 480p
- 音频：采样率 ≥ 16kHz，**必需**（用于分贝检测、音色情绪分析、摔门撞击声识别）
- 视频时长：实时流接入；离线分析建议 ≥ 30 分钟（覆盖完整冲突 → 平静窗口）
- ROI 标定：公共活动区域，识别但**不录制**或**仅缓存 ≤ 24 小时**即清理
- **必须**支持家庭主用户一句话/物理按键**整日关闭**功能（用于聚会等正常高分贝场景）

## 关键观测信号

### 音频（核心）
- `db_level_peak` - 分贝峰值（dBA）
- `db_level_sustained_duration_sec` - 持续 ≥ 阈值（默认 75 dB）的时长
- `shouting_voice_detected` - 喊叫/嘶吼声纹检测（与正常大笑、儿童欢闹声区分）
- `door_slam_event_count` - 摔门事件次数（撞击声 + 短暂低频共振）
- `object_impact_event_count` - 物体砸落/拍桌等撞击声
- `crying_audio_detected` - 哭泣声检测（成人或儿童）
- `silence_duration_sec` - 当前连续静音 / 低音量时长（用于平静窗口判定）

### 视频（辅助）
- `arm_swing_aggressive_count` - 大幅甩手 / 挥手势次数
- `pacing_back_and_forth` - 来回踱步事件（参考指标）
- `person_walked_out_event` - 有人离开画面（往往是冲突高潮）
- `physical_distance_minimum_m` - 两人最近物理距离（用于评估冲突烈度）
- `body_facing_away_duration_sec` - 转身背对持续时长（冷战指标）

### ⚠️ 红线信号（必须独立优先级输出，不可用缓和动作处理）
- `physical_violence_suspected` - **疑似肢体暴力**（推搡 / 挥拳 / 抓握等）
- `child_present_during_conflict` - 冲突现场**有未成年人**在场
- `weapon_or_dangerous_object_visible` - 出现刀具 / 重物等危险物
- `injury_visual_signs` - 出现摔倒 / 抚摸面部 / 蜷缩等疑似受伤征兆

## 阈值与冲突等级（默认值，可在配置中覆盖）

- `db_peak < 70 dB` 且无摔门 → **none**（无冲突）
- `db_peak 70-80 dB` 且 `sustained_duration ≥ 10s` → **mild_dispute**（轻度争论）
- `db_peak ≥ 80 dB` 且 `sustained_duration ≥ 10s` 或 摔门 1 次 → **conflict**（明显冲突）
- `db_peak ≥ 90 dB` 或 多次摔门/砸物 或 大幅甩手 ≥ 3 → **intense_conflict**（激烈冲突）
- 任一红线信号触发 → **critical_redline**（**立即转走"安全风险"路径**，不进入缓和流程）

## 平静窗口判定（aftercare 触发前置条件）

- `silence_duration_sec ≥ 600`（默认 10 分钟，可配置）
- 期间无新的 `mild_dispute / conflict / intense_conflict` 事件
- 物理距离回归常态 或 至少一人回到画面内
- 当**所有**条件满足才触发缓和动作

## 输出字段（参考）

- `event_id` / `conflict_start_time` / `conflict_end_time` / `conflict_duration_min`
- `audio_signals` / `video_signals`
- `conflict_level` - 冲突等级（none / mild_dispute / conflict / intense_conflict / critical_redline）
- `redline_flags` - 红线信号清单
- `calm_window_status` - 平静窗口状态（observing / met / reset_by_new_conflict）
- `calm_window_duration_sec`
- `aftercare_actions` - 缓和动作列表（每项含 action_type / message / target，例如：
    - `{action_type: "smart_speaker_soft_music", message: "为家里放一首舒缓的轻音乐", target: "living_room_speaker"}`
    - `{action_type: "smart_speaker_gentle_voice", message: "需要一杯茶吗？深呼吸，慢慢说，你们都是这个家最重要的人~", target: "living_room_speaker"}`
    - `{action_type: "family_app_push", message: "👋 给家人一个台阶：不如先各自冷静 5 分钟，再坐下来听对方说完三句话", target: "family_group_app"}`）
- `recommend_action` - 建议动作（trigger_soft_music / push_gentle_message / observe_only / escalate_safety_path）
- `safety_resource` - 当 critical_redline 触发时附**安全资源**：
    - 反家暴热线 **12338**
    - 全国妇联权益部
    - 报警 **110**（如有肢体暴力 + 儿童在场）
    - 全国心理援助热线 **400-161-9995**
    - 当地社区社工 / 司法所

## 强制约束与红线

- ❌ **禁止**部署在卧室、卫生间、儿童独立房间
- ❌ **禁止**录制并长期存储家庭对话原始音频；建议仅保留**分贝/事件指标**和不超过 24 小时的事件片段
- ❌ **禁止**做任何"婚姻/亲子关系评分"或"性格分析"
- ❌ **禁止**在 `intense_conflict` 期间播放音乐或语音介入（会激化情绪）；**必须等待平静窗口**
- ❌ **禁止**对疑似肢体暴力进行"缓和处理"——必须独立走**安全风险**路径
- ❌ **禁止**将冲突事件转发给除家庭主用户外的第三方（亲戚、邻居、外人）
- ✅ **必须**支持家庭主用户：一键关闭今日 / 整日关闭（用于聚会等正常高分贝场景）/ 永久退出
- ✅ **必须**在播放缓和动作前给予 3 秒非语言提示（如柔和铃声），避免突然出声二次惊吓
- ✅ **必须**在 `critical_redline` 触发时**立即**推送 **12338** 反家暴热线和 **110** 报警提示；有未成年人在场时优先级最高
- ✅ 缓和文案必须**中立、不指责任何一方**，避免"是 XX 错了"等评判性语言
- ✅ 同一事件单日缓和动作触发**上限 2 次**，避免过度介入

> 仅输出基于音视频的**客观冲突事件检测和缓和动作建议**，**不构成婚姻/亲子关系咨询或心理治疗**；任何疑似家庭暴力情况请立即拨打 **12338 反家暴热线**或 **110**，并联系专业社工/心理咨询师。
