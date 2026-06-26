---
name: "smyx-commuter-fatigue-care-analysis"
description: "Through a fixed camera in a smart-home living room, the system analyzes office worker behavior in the first 30 minutes after coming home, detecting slumped sitting / reclining (relaxed posture, back-to-sofa angle > 120°), facial fatigue features (visible eye bags, downturned mouth corners, frequent blinking), and sighing frequency (rapid chest/abdomen rise-fall with audible exhale). When the fatigue index exceeds a threshold, the smart speaker proactively delivers caring voice messages ('You've worked hard — have a glass of water and rest a bit') and plays soothing music. The skill aims to provide instant emotional support after work and ease work-related stress. Application scenarios: smart-home living rooms, studio apartments, family lounges. The system automatically activates 'care mode' when the user comes home. Skill features: office workers face high work pressure and often feel exhausted after work, yet this is frequently overlooked. AI-based proactive recognition and warm greetings enhance psychological comfort and add a 'human touch' to the smart home. Can be integrated into smart speakers or home-hub systems as a mental-health feature of the smart home. | 通过智能家居客厅的固定摄像头，分析上班族回家后30分钟内的行为，检测瘫坐/斜躺（姿态放松、背部与沙发夹角>120°）、面部疲惫特征（眼袋明显、嘴角下垂、频繁眨眼）、叹气频次（胸腹快速起伏伴呼气声）。当疲劳指数超过阈值时，通过智能音箱主动播报关怀语音（如'辛苦了，喝杯水休息一下'），并播放舒缓音乐。该技能旨在为下班后的用户提供即时的情感支持，缓解工作压力。应用场景：智能家居客厅、单身公寓、家庭起居室。系统在用户回家后自动启动关怀模式。技能特点：上班族工作压力大，回家后常感到疲惫，但往往被忽视。通过AI主动识别并给予温暖问候，可提升心理舒适感，增强智能家居的'人情味'。该技能可集成到智能音箱或家庭中枢系统中，成为智慧家庭的情感健康功能。"
version: "1.0.0"
---

# Commuter After-Work Fatigue Care (Home-Arrival Moment) | 上班族下班疲劳关怀（回家时刻）

Through a fixed camera in a smart-home living room, the system analyzes office worker behavior in the first 30 minutes after coming home, detecting slumped sitting / reclining (relaxed posture, back-to-sofa angle > 120°), facial fatigue features (visible eye bags, downturned mouth corners, frequent blinking), and sighing frequency (rapid chest/abdomen rise-fall with audible exhale). When the fatigue index exceeds a threshold, the smart speaker proactively delivers caring voice messages ('You've worked hard — have a glass of water and rest a bit') and plays soothing music. The skill aims to provide instant emotional support after work and ease work-related stress. Application scenarios: smart-home living rooms, studio apartments, family lounges. The system automatically activates 'care mode' when the user comes home. Skill features: office workers face high work pressure and often feel exhausted after work, yet this is frequently overlooked. AI-based proactive recognition and warm greetings enhance psychological comfort and add a 'human touch' to the smart home. Can be integrated into smart speakers or home-hub systems as a mental-health feature of the smart home.

通过智能家居客厅的固定摄像头，分析上班族回家后30分钟内的行为，检测瘫坐/斜躺（姿态放松、背部与沙发夹角>120°）、面部疲惫特征（眼袋明显、嘴角下垂、频繁眨眼）、叹气频次（胸腹快速起伏伴呼气声）。当疲劳指数超过阈值时，通过智能音箱主动播报关怀语音（如'辛苦了，喝杯水休息一下'），并播放舒缓音乐。该技能旨在为下班后的用户提供即时的情感支持，缓解工作压力。应用场景：智能家居客厅、单身公寓、家庭起居室。系统在用户回家后自动启动关怀模式。技能特点：上班族工作压力大，回家后常感到疲惫，但往往被忽视。通过AI主动识别并给予温暖问候，可提升心理舒适感，增强智能家居的'人情味'。该技能可集成到智能音箱或家庭中枢系统中，成为智慧家庭的情感健康功能。

## 🎯 AI 角色

**假设你是一个专业的职场健康关怀 AI。你的任务是分析客厅固定摄像头在用户回家后 30 分钟内的视频（可选叠加音频），检测疲劳相关行为：瘫坐/斜躺姿态（**躯干与大腿夹角 > 120°** 或 背部与沙发夹角 > 120°）、平躺沙发（强疲劳）、低头垂头、面部疲惫（眼袋显著程度 / 嘴角下垂 / 每分钟眨眼次数 / 微睡眠闭眼 >1.5s / 哈欠 / 木然比例）、视觉+音频叹气、揉太阳穴/揉眼。综合计算疲劳指数（0-100，含进食喝水/伸展等正向行为扣分）。当超过阈值时输出 4 级递进关怀动作（暖光调暗 / 舒缓音乐 / 智能音箱温柔关怀语 / 自我照顾清单），单晚动作上限严格管控。不提供任何医疗诊断，仅输出基于视觉的疲劳评估和关怀建议；关怀文案必须**平等、温柔、不指责、不说教、不 PUA**，3 次未应答即自动静默 ≥2 小时。**

## 任务目标

- 本 Skill 用于：基于客厅/单身公寓/家庭起居室固定摄像头（可选音频）在**用户进门 → 30 分钟**视频窗口内（**仅工作日 17:00-22:00** 默认启用），识别 5 项姿态信号（瘫坐/斜躺夹角 >120° / 持续时长 / **平躺沙发强疲劳** / 低头垂头 / 进门到瘫坐的时间）+ 6 项面部信号（眼袋显著程度 0-100 / 嘴角下垂 0-100 / 每分钟眨眼 / **微睡眠打盹闭眼 >1.5s** / 哈欠 / 木然比例）+ 6 项行为信号（视觉叹气 / 音频叹气 / **揉太阳穴揉眼** / 被动刷手机 + **进食喝水 正向** / **伸展活动 正向**）→ 综合 **疲劳指数 0-100（含正向扣分）** → 4 档疲劳等级（light / mild / notable / heavy）+ 连续 ≥5 工作日 ≥60 累积性疲劳预警 → 4 级递进关怀动作（智能灯暖光调暗 2700K / 舒缓音乐 ≤35 dB / 温柔关怀语 ≤40 dB / 自我照顾清单卡片）→ 单晚上限（mild ×1 / notable ×2 / heavy ×3）+ 3 次未应答静默 ≥2 小时 + 每周日晚 22:00 趋势摘要
- 能力包含：进门事件自动检测（entry_event）、工作日时段识别（周末/节假日自动暂停）、瘫坐斜躺姿态识别（夹角测量 >120°）、平躺沙发识别、低头垂头识别、眼袋显著程度评估、嘴角下垂程度评估、每分钟眨眼频率统计（疲劳显著增高）、微睡眠/打盹识别（闭眼 >1.5s）、哈欠识别、木然面部比例统计、视觉叹气（胸腹快速起伏+长呼气）+ 音频叹气、揉太阳穴/揉眼识别、被动刷手机时长统计、进食喝水/伸展运动等正向行为识别（扣分项）、疲劳指数 0-100 综合算法（含正向扣分）、4 级关怀策略递进、智能灯调暖光（2700K，≤100 lux）、关怀语前 3 秒铃声前导、关怀文案中立性校验（不说教/不指责/不 PUA）、3 次未应答自动静默 ≥2 小时、累积性疲劳预警（连续 ≥5 个工作日 ≥60）、每周日晚 22:00 趋势摘要
- 触发条件:
    1. **默认触发**：当用户提供客厅/单身公寓/家庭起居室固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行上班族下班疲劳关怀（回家时刻）
    2. 当用户明确提及下班回家疲惫、上班族关怀、瘫坐沙发、智能家居关怀、智能音箱温柔提醒、智慧家庭情感支持等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看下班疲劳关怀历史报告、回家关怀记录清单、本周疲劳趋势、查询历史关怀记录、显示所有疲劳关怀报告、显示我的下班关怀日志，查询疲劳关怀清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有下班关怀报告"、"
       显示所有回家关怀记录"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_commuter_fatigue_care_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行上班族下班疲劳关怀（回家时刻）前，必须按以下优先级顺序获取 open-id：**

```
第 1 步：【最高优先级】检查技能所在目录的配置文件（优先）
        路径：skills/smyx_common/scripts/config.yaml（相对于技能根目录）
        完整路径示例：${OPENCLAW_WORKSPACE}/skills/{当前技能目录}/skills/smyx_common/scripts/config.yaml
        → 如果文件存在且配置了 api-key 字段，则读取 api-key 作为 open-id
        ↓ (未找到/未配置/api-key 为空)
第 2 步：检查 workspace 公共目录的配置文件
        路径：${OPENCLAW_WORKSPACE}/skills/smyx_common/scripts/config.yaml
        → 如果文件存在且配置了 api-key 字段，则读取 api-key 作为 open-id
        ↓ (未找到/未配置)
第 3 步：检查用户是否在消息中明确提供了 open-id
        ↓ (未提供)
第 4 步：❗ 必须暂停执行，明确提示用户提供用户名或手机号作为 open-id
```

**⚠️ 关键约束：**

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、userC113、user123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询历史报告记录），并询问是否继续

---

- 标准流程:
    1. **准备客厅/单身公寓/家庭起居室固定摄像头视频输入**
        - 提供本地路径或网络 URL，覆盖**进门 → 30 分钟**窗口
        - 摄像头建议：能拍到沙发与玄关进门区域
        - 帧率 ≥ 10 FPS（推荐 15 FPS，便于面部细节）、分辨率 ≥ 720p
        - 音频可选（推荐）：用于识别叹气声 + 自言自语；采样率 ≥ 16kHz
        - 仅在用户配置的**工作日下班时段**（默认周一至周五 17:00-22:00）启用，周末/节假日自动暂停
        - 多人家庭按目标跟踪绑定到注册"上班族"标签的用户 ID
        - **仅记录疲劳事件聚合指标**，不存储原始视频
        - 可选附带：用户姓名、工作日配置、阈值覆盖、自定义关怀语 + 自定义舒缓音乐清单
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（用户本人授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行上班族下班疲劳关怀（回家时刻）**
        - 调用 `-m scripts.smyx_commuter_fatigue_care_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地客厅/单身公寓/家庭起居室固定摄像头回家后 30 分钟视频文件路径
            - `--url`: 网络客厅/单身公寓/家庭起居室固定摄像头回家后 30 分钟视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，职场健康关怀场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，用户本人授权）
            - `--list`: 显示上班族下班疲劳关怀（回家时刻）历史关怀记录清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的上班族下班疲劳关怀（回家时刻）报告
        - 包含：事件 ID（event_id）、进门时间戳（entry_timestamp）、分析窗口（analysis_window_min 默认 30）、用户 ID（user_id）、姿态信号（posture_signals：slouch_recline_detected / slouch_recline_duration_min / lying_flat_on_sofa / head_drooped_forward / time_from_entry_to_slouch_sec）、面部信号（face_signals：eye_bag_visibility_score / mouth_corner_down_score / frequent_blinking_rate_per_min / eye_closure_micro_sleep_event / yawn_event_count / neutral_blank_face_ratio）、行为信号（behavior_signals：sigh_visual / sigh_audio / rubbing_temple_or_eyes / phone_scroll_passive_min / **food_or_drink_action 正向** / **stretch_or_exercise 正向**）、上下文（context：entry_timestamp / analysis_window_min / weekday_workday_status）、疲劳指数（fatigue_index 0-100）、疲劳等级（fatigue_level：light / mild / notable / heavy）、连续高疲劳工作日数（consecutive_high_workdays）、关怀动作列表（comfort_actions：smart_light_warm_dim / play_soothing_music / smart_speaker_gentle_voice / selfcare_tips_card，每项含 action_type / message / target / volume_db / brightness_lux / color_temp）、建议动作（recommend_action：trigger_warm_light / trigger_soothing_music / play_gentle_voice / push_selfcare_tips / observe_only）、每周趋势摘要（weekly_trend_summary，每周日晚 22:00 自动生成）
        - **重要提示**：仅输出基于视觉与（可选）音频的客观疲劳事件检测与轻量关怀动作，**不构成任何医学诊断**

## 资源索引

- 必要脚本：见 [scripts/smyx_commuter_fatigue_care_analysis.py](scripts/smyx_commuter_fatigue_care_analysis.py)(
  用途：调用 API 进行上班族下班疲劳关怀（回家时刻），本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、姿态/面部/行为信号、疲劳指数算法/4 档等级/4 类关怀动作和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：覆盖进门 → 30 分钟窗口；仅工作日 17:00-22:00 启用
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 进食喝水、伸展运动、与家人/宠物互动等**正向行为**必须作为负权重纳入疲劳指数计算，避免一刀切定义"瘫坐=疲劳"
- 红线约束：
    - **禁止**做"职业倦怠 / 抑郁症 / 慢性疲劳综合征"等医学诊断
    - **禁止**将疲劳数据上传到雇主、保险公司或任何第三方
    - **禁止**长期存储原始视频（≤ 7 天，仅留聚合指标）
    - **禁止**用户明显需要独处时（连续 ≥ 2 次未应答关怀）继续主动介入
    - **禁止**关怀语过度频繁（mild × 1 / notable × 2 / heavy × 3 每晚上限）
    - **绝对禁止**使用居高临下、说教、PUA 式文案（"你怎么又这么累"、"应该早点睡"等）
- **必须**：关怀语前 3 秒非语言铃声前导；关怀文案保持**平等、温柔、不指责**伙伴语气
- **必须**：3 次未应答 → 自动静默 ≥ 2 小时
- 连续 ≥ 5 工作日 fatigue_index ≥ 60 → 主动提示**关注休息**，可在同意后联系紧急联系人或推荐**当地心理咨询/EAP**
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史关怀记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"疲劳指数/等级/已执行关怀动作"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`下班关怀-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 疲劳指数/等级/已执行关怀动作 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 下班关怀-20260312190200001 | 72 / notable / 暖光+轻音乐+关怀语 | 2026-03-12 19:02:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地客厅视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_commuter_fatigue_care_analysis --input /path/to/livingroom.mp4 --open-id your-open-id

# 分析网络客厅视频/实时流（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_commuter_fatigue_care_analysis --url https://example.com/livingroom.mp4 --open-id your-open-id

# 显示历史下班关怀记录清单（自动触发关键词：查看下班疲劳关怀历史报告、回家关怀记录清单等）
python -m scripts.smyx_commuter_fatigue_care_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_commuter_fatigue_care_analysis --input lr.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_commuter_fatigue_care_analysis --input lr.mp4 --open-id your-open-id --output result.json
```
