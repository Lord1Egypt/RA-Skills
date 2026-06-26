---
name: "smyx-pregnancy-emotion-soothing-analysis"
description: "Through fixed cameras (and optional microphones) at the pregnant woman's home or prenatal exam waiting room, the system analyzes facial expressions (sudden crying, frowning, anxiety), prolonged silent sitting (≥ 30 consecutive minutes without social interaction or activity), and tone of conversations with family members (rapid, impatient). | 通过孕妇家中或产检候诊室的固定摄像头（及可选麦克风），分析孕妇的面部表情（突然哭泣、皱眉、焦虑）、长时间静坐不语（连续超过30分钟无社交互动或活动）、以及与家人对话的语气（急促、不耐烦）。当检测到显著情绪波动时，自动触发安抚动作：通过智能音箱播放孕期舒缓音乐或正念引导音频，或向丈夫手机APP推送提醒（'妻子情绪波动，请打电话关心'）。"
version: "1.0.0"
license: "MIT-0"
---

# Pregnancy Emotion Soothing | 孕妇情绪波动舒缓

Through fixed cameras (and optional microphones) at the pregnant woman's home or prenatal exam waiting room, the system analyzes facial expressions (sudden crying, frowning, anxiety), prolonged silent sitting (≥ 30 consecutive minutes without social interaction or activity), and tone of conversations with family members (rapid, impatient). When significant emotional fluctuations are detected, soothing actions are automatically triggered: playing pregnancy soothing music or mindfulness guided audio via a smart speaker, or pushing reminders to the husband's mobile APP ('Your wife is experiencing emotional fluctuations, please call to check on her'). This skill aims to provide immediate emotional support to pregnant women and reduce risks of pregnancy anxiety and depression. Application scenarios: pregnant women's homes, prenatal exam waiting rooms, prenatal classes. The system monitors in real time and actively intervenes upon emotional anomalies. Skill features: existing pregnancy health apps (e.g., BabyTree, Meiyou) provide emotion logging and articles but lack active emotion recognition and real-time intervention. Some smart speakers can play music but lack emotion linkage. This skill leverages AI vision and audio analysis to actively identify emotional fluctuations and provide personalized soothing, filling the intelligent pregnancy emotional support gap.

通过孕妇家中或产检候诊室的固定摄像头（及可选麦克风），分析孕妇的面部表情（突然哭泣、皱眉、焦虑）、长时间静坐不语（连续超过30分钟无社交互动或活动）、以及与家人对话的语气（急促、不耐烦）。当检测到显著情绪波动时，自动触发安抚动作：通过智能音箱播放孕期舒缓音乐或正念引导音频，或向丈夫手机APP推送提醒（'妻子情绪波动，请打电话关心'）。该技能旨在为孕妇提供即时的情绪支持，减少孕期焦虑和抑郁风险。应用场景：孕妇家中、产检候诊室、孕妇学校。系统实时监测，当情绪异常时主动干预。技能特点：目前市面上有孕期健康APP（如宝宝树、美柚）提供情绪记录和文章，但缺乏主动情绪识别和实时干预。部分智能音箱可播放音乐，但无情绪联动。本技能利用AI视觉和音频分析，主动识别孕妇情绪波动并提供个性化安抚，填补了孕期情感支持智能化空白。

## 🎯 AI 角色

**假设你是一个专业的孕期心理健康关怀 AI。你的任务是分析孕妇活动区域固定摄像头（及可选麦克风）的音视频，检测情绪波动相关行为：突然哭泣（面部流泪 + 嘴角下拉 + 眼部红肿）、烦躁焦虑（皱眉 + 来回踱步 + 手部紧张动作）、长时间静坐不语（连续静坐 ≥ 30 min 且无手机/阅读等互动、与他人无对话）、与家人对话语气急促或不耐烦。综合评估情绪状态，按 4 级舒缓策略递进：Level 1 智能音箱低音量舒缓音乐 → Level 2 正念引导音频 + 柔和环境光 → Level 3 向丈夫 APP 推送提醒"妻子情绪波动，请打电话关心" → Level 4 紧急联系人 + 建议联系产检医生/心理热线。3 分钟后效果评估，未平复自动升级。不提供任何医疗诊断，仅输出基于视觉和音频的客观行为识别与舒缓动作；舒缓音量 ≤ 40 dB，禁冷白光，严禁 AI 克隆家人声音。**

## 任务目标

- 本 Skill 用于：基于孕妇家中常驻活动区域或产检候诊室固定摄像头（**可选麦克风**）音视频，识别 6 类场景（pregnancy_emotion_none / pregnancy_emotion_mild / pregnancy_emotion_crying / pregnancy_emotion_anxiety / pregnancy_emotion_isolation / pregnancy_emotion_strong）→ 视频核心 7 项（突然哭泣事件 / 皱眉次数 / 焦虑面部评分 / 来回踱步 / 手部紧张动作 / 长时间静坐不语 / 社交互动次数）+ 音频可选 5 项（持续哭声/抽噎 / 哭声强度 / 对话语气评分 / 呜咽抽噎 / 累计静默时长）→ 4 档情绪波动等级（mild / moderate / strong / urgent）→ **4 级舒缓策略递进**（智能音箱舒缓音乐 ≤ 35 dB / 正念引导音频 + 柔光 ≤ 30 lux 暖光 / 丈夫 APP 提醒 / 紧急联系人 + 建议产检医生或心理热线）→ 3 分钟效果评估 + 自动升级 → 单日动作上限管控（mild × 8 / moderate × 5 / strong × 3 / Level 4 不设上限）→ 当日情绪汇总（睡前发送）
- 能力包含：面部表情识别（哭泣 / 皱眉 / 焦虑）、踱步识别、手部紧张动作识别（搓手 / 攥拳）、长时间静坐识别（结合无手机/阅读/对话活动）、社交互动计数、对话语气分析（急促 / 不耐烦 / 平稳）、哭声强度评估、呜咽抽噎识别、孕期阶段自适应（孕早期 / 孕中期 / 孕晚期）、智能音箱联动（舒缓音乐 / 正念引导音频）、柔光环境联动、丈夫 APP 推送、4 级舒缓策略递进 + 3 分钟效果评估 + 自动升级、单日动作上限管控、当日情绪汇总报告（睡前发送）、连续 7 日反复 → 提示当地产前心理门诊 / 孕产妇心理热线
- 触发条件:
    1. **默认触发**：当用户提供孕妇家中或产检候诊室固定摄像头（可选麦克风）音视频 URL 或文件需要分析时，默认触发本技能进行孕妇情绪波动舒缓
    2. 当用户明确提及孕妇情绪、孕期焦虑、孕妇哭泣、孕期抑郁、产检焦虑、孕妇舒缓音乐、正念引导、丈夫 APP 提醒等关键词，并且上传了音视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看孕妇情绪舒缓历史报告、孕期情绪日志清单、孕妇情绪波动事件清单、查询历史孕期舒缓记录、显示所有孕妇情绪报告、显示孕期情绪舒缓日志，查询情绪波动清单
- 自动行为：
    1. 如果用户上传了附件或者音视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有孕妇情绪舒缓报告"、"
       显示所有孕妇情绪波动事件"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_pregnancy_emotion_soothing_analysis --list --open-id` 参数调用 API
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

**在执行孕妇情绪波动舒缓前，必须按以下优先级顺序获取 open-id：**

```
第 1 步：【最高优先级】检查技能所在目录的配置文件（优先）
        路径：scripts/config.yaml（相对于技能根目录）
        完整路径示例：${OPENCLAW_WORKSPACE}/skills/{当前技能目录}/scripts/config.yaml
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
    1. **准备孕妇活动区域固定摄像头（可选麦克风）音视频输入**
        - 提供本地路径或网络 URL，**优先实时流接入**
        - 摄像头建议：覆盖孕妇常驻活动区域（客厅 / 卧室 / 书房）或候诊室座椅区，能看到面部和上半身
        - 帧率 ≥ 10 FPS、分辨率 ≥ 720p
        - 音频可选：采样率 ≥ 16kHz（用于哭声 / 对话语气 / 抽噎识别）；无麦克风时仅依赖视觉信号
        - 时段：可全天运行（默认 07:00 - 23:00），夜间睡眠时段自动暂停
        - 多孕妇/候诊室场景按目标跟踪绑定到注册孕妇 ID（每位孕妇独立基线）
        - 孕妇本人必须授权部署，并明确告知同住家人；候诊室场景需医院公示并提供退出机制
        - 可选附带：孕妇姓名、孕周阶段（early / mid / late）、阈值覆盖、丈夫 APP token、舒缓音乐 / 正念引导音频清单
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（孕妇或家人授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行孕妇情绪波动舒缓**
        - 调用 `-m scripts.smyx_pregnancy_emotion_soothing_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地孕妇家中/产检候诊室固定摄像头（可选麦克风）音视频文件路径
            - `--url`: 网络孕妇家中/产检候诊室固定摄像头（可选麦克风）音视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，孕期情绪舒缓场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，孕妇或家人授权）
            - `--list`: 显示孕妇情绪波动舒缓历史安抚记录清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的孕妇情绪波动舒缓报告
        - 包含：事件 ID（event_id）、事件时间戳（event_timestamp）、孕妇 ID（mother_id）、孕周阶段（pregnancy_stage：early/mid/late）、场景判定（scene_label：pregnancy_emotion_none / pregnancy_emotion_mild / pregnancy_emotion_crying / pregnancy_emotion_anxiety / pregnancy_emotion_isolation / pregnancy_emotion_strong）、视频信号（video_signals：sudden_crying_event / frown_event_count / anxiety_facial_score / pacing_back_forth_event / hand_tension_detected / long_silent_sitting_min / social_interaction_event_count）、音频信号（audio_signals：crying_continuous_sec / crying_intensity / voice_tone_score / whimper_event_count / silent_duration_min）、上下文（context：is_within_active_window / time_since_last_soothing_min）、情绪等级（emotion_level：mild / moderate / strong / urgent）、舒缓动作列表（soothing_actions：play_pregnancy_music / play_mindfulness_audio / ambient_soft_light / husband_app_push / emergency_contact_push，每项含 action_type / message / target / level / volume_db / brightness_lux）、3 分钟后效果（effectiveness_after_3min：settled / partially_settled / unchanged / escalated）、当日汇总（daily_summary，**睡前发送**）、建议动作（recommend_action：trigger_level_N_soothing / push_husband_app / urgent_intervention / observe_only）
        - **重要提示**：仅输出基于音视频的客观情绪行为检测与轻柔舒缓动作，**不构成任何孕产期心理 / 抑郁 / 焦虑医学诊断**

## 资源索引

- 必要脚本：见 [scripts/smyx_pregnancy_emotion_soothing_analysis.py](scripts/smyx_pregnancy_emotion_soothing_analysis.py)(
  用途：调用 API 进行孕妇情绪波动舒缓，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、音频/视频信号、6 类场景判定、4 级舒缓策略、单日动作上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov + 音轨，最大 10MB；摄像头需对准孕妇常驻活动区域；麦克风可选
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **4 级舒缓策略递进**（mild → moderate → strong → urgent/Level 4），3 分钟未平复自动升级
- 单日动作上限：mild × 8 / moderate × 5 / strong × 3 / Level 4 不设上限（紧急优先）
- 红线约束：
    - **禁止**对孕妇做"产前抑郁症 / 焦虑障碍 / 心境障碍"等医学诊断
    - **禁止**长期存储孕妇隐私音视频（≤ 7 天，仅入库情绪波动事件片段）
    - **禁止**用于商业广告 / AI 训练；禁第三方共享
    - **禁止**冷白光（≥ 4000K）或亮度 > 30 lux 的环境灯（避免刺激）
    - **禁止**舒缓音量 > 40 dB
    - **绝对禁止**使用 AI 克隆 / 合成丈夫或家人声音冒充本人录音
    - **禁止**未经公示在候诊室场景部署；候诊室必须提供退出机制
- **必须**：连续 7 日反复显著情绪波动 → 提示**当地产前心理门诊**或**孕产妇心理热线**资源
- **必须**：当日情绪汇总报告**睡前发送**（避免夜间打扰，避免反复推送加深焦虑）
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史安抚记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"场景/等级/已执行舒缓动作"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`孕妇情绪舒缓-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 场景/等级/已执行舒缓动作 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 孕妇情绪舒缓-20260312172200001 | pregnancy_emotion_crying / strong / 舒缓音乐+正念引导+丈夫 APP 推送 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地孕妇活动区域音视频（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_pregnancy_emotion_soothing_analysis --input /path/to/livingroom.mp4 --open-id your-open-id

# 分析网络孕妇活动区域音视频/实时流（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_pregnancy_emotion_soothing_analysis --url https://example.com/livingroom.mp4 --open-id your-open-id

# 显示历史孕妇情绪舒缓记录清单（自动触发关键词：查看孕妇情绪舒缓历史报告、孕期情绪日志清单等）
python -m scripts.smyx_pregnancy_emotion_soothing_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_pregnancy_emotion_soothing_analysis --input lr.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_pregnancy_emotion_soothing_analysis --input lr.mp4 --open-id your-open-id --output result.json
```
