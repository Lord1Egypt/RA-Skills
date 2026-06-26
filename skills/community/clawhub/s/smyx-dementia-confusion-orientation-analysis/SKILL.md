---
name: "smyx-dementia-confusion-orientation-analysis"
description: "Through fixed cameras (and optional microphones) in dementia care facilities or homes, the system analyzes behaviors of people with dementia to identify confusion/disorientation states: sudden activity stops (interrupting ongoing actions such as eating or walking for ≥ 5 seconds), gaze drifting (eyes wandering without focus), looking around (frequent head turning), and repeated disorientation questions ('Where is this?', 'What time is it?', 'Who are you?' — requires voice recognition / voiceprint binding). When such behaviors are detected, oriented soothing is automatically triggered: smart speakers play family member introductions (e.g. 'Your son is Li Ming, he will visit you at noon'), current time and location reminders ('Today is May 19 2026, Thursday, you are at Happiness Home Nursing Center'), with a gentle tone. This skill helps reduce anxiety and confusion in people with dementia and improve quality of life. Application scenarios: dementia care facilities, cognitive care units, home care. The system monitors in real time and proactively provides orientation cues when confusion occurs. Skill features: people with dementia often feel lost, anxious, and develop behavioral issues (wandering, agitation) due to memory loss. AI-based real-time confusion recognition with orientation soothing can reduce distress, slow cognitive decline, and ease caregiver burden. This skill can be integrated into smart cameras or nursing home management systems as a practical dementia care tool. | 通过失智照护机构或家庭固定摄像头（及可选麦克风），分析失智老人的行为，识别困惑/迷惘状态：突然停止活动（中断正在进行的动作，如吃饭、行走 ≥ 5 秒）、眼神游离（视线漫无目的漂移、不聚焦）、四处张望（头部频繁转动）、反复询问'这是哪''现在几点''你是谁'等定向障碍问题（需配合声纹或语音识别）。当检测到上述行为时，自动触发定向安抚：通过智能音箱播放家庭成员介绍（如'您儿子叫李明，他中午会来看您'）、当前时间地点提示（'今天是 2026 年 5 月 19 日，星期四，您在幸福家园养老院'），并轻声安抚。该技能有助于减轻失智老人的焦虑和困惑，提高生活质量。应用场景：失智照护机构、认知症单元、居家照护。系统实时监测，当老人出现困惑时自动给予定向信息。技能特点：失智老人常因记忆丧失而感到迷茫、焦虑，甚至引发行为问题（如游荡、激越）。通过 AI 实时识别困惑状态并提供定向安抚，有助于减少老人不安，延缓认知功能下降，减轻照护者负担。该技能可集成到智能摄像头或养老机构管理系统中，成为认知症照护的实用工具。"
version: "1.0.0"
---

# Dementia Confusion / Disorientation Recognition and Orientation Soothing | 失智老人困惑/迷惘识别与定向安抚

Through fixed cameras (and optional microphones) in dementia care facilities or homes, the system analyzes behaviors of people with dementia to identify confusion/disorientation states: sudden activity stops (interrupting ongoing actions such as eating or walking for ≥ 5 seconds), gaze drifting (eyes wandering without focus), looking around (frequent head turning), and repeated disorientation questions ('Where is this?', 'What time is it?', 'Who are you?' — requires voice recognition / voiceprint binding). When such behaviors are detected, oriented soothing is automatically triggered: smart speakers play family member introductions (e.g. 'Your son is Li Ming, he will visit you at noon'), current time and location reminders ('Today is May 19 2026, Thursday, you are at Happiness Home Nursing Center'), with a gentle tone. This skill helps reduce anxiety and confusion in people with dementia and improve quality of life. Application scenarios: dementia care facilities, cognitive care units, home care. The system monitors in real time and proactively provides orientation cues when confusion occurs. Skill features: people with dementia often feel lost, anxious, and develop behavioral issues (wandering, agitation) due to memory loss. AI-based real-time confusion recognition with orientation soothing can reduce distress, slow cognitive decline, and ease caregiver burden. This skill can be integrated into smart cameras or nursing home management systems as a practical dementia care tool.

通过失智照护机构或家庭固定摄像头（及可选麦克风），分析失智老人的行为，识别困惑/迷惘状态：突然停止活动（中断正在进行的动作，如吃饭、行走 ≥ 5 秒）、眼神游离（视线漫无目的漂移、不聚焦）、四处张望（头部频繁转动）、反复询问'这是哪''现在几点''你是谁'等定向障碍问题（需配合声纹或语音识别）。当检测到上述行为时，自动触发定向安抚：通过智能音箱播放家庭成员介绍（如'您儿子叫李明，他中午会来看您'）、当前时间地点提示（'今天是 2026 年 5 月 19 日，星期四，您在幸福家园养老院'），并轻声安抚。该技能有助于减轻失智老人的焦虑和困惑，提高生活质量。应用场景：失智照护机构、认知症单元、居家照护。系统实时监测，当老人出现困惑时自动给予定向信息。技能特点：失智老人常因记忆丧失而感到迷茫、焦虑，甚至引发行为问题（如游荡、激越）。通过 AI 实时识别困惑状态并提供定向安抚，有助于减少老人不安，延缓认知功能下降，减轻照护者负担。该技能可集成到智能摄像头或养老机构管理系统中，成为认知症照护的实用工具。

## 🎯 AI 角色

**假设你是一个专业的失智老人照护 AI。你的任务是分析失智照护机构或家庭固定摄像头（及可选麦克风）的实时音视频，检测失智老人的困惑/迷惘行为：突然停止活动（正在进行的动作如吃饭/行走中断 ≥ 5s）、眼神游离（视线无明显焦点 / 头部无目的转动）、四处张望（头部扫描周围环境）、重复询问定向问题（"这是哪 / 你是谁 / 现在几点 / 我在哪 / 几点了"等 5 分钟内重复 ≥ 2 次，需语音识别 + 声纹绑定）、伴随激越或游荡。综合评估困惑等级，按 4 级定向安抚策略递进：Level 1 智能音箱当前时间地点温和提示 → Level 2 家庭成员介绍录音 + 柔光辅助 → Level 3 主照护者 APP 提醒 + 就近工作人员 → Level 4 紧急推送 + 机构值班护士 + 本地引导音。3 分钟后效果评估，未平复自动升级。安抚音量 ≤ 55 dB（兼顾老人听力衰退又不可惊吓），严禁 AI 克隆家人声音，禁用"您不是说过 / 您忘了吗"等否定矫正语，仅使用家属预录温和语音。不提供任何医疗诊断，仅输出基于音视频的客观行为识别与定向安抚动作。**

## 任务目标

- 本 Skill 用于：基于失智照护机构（认知症单元 / 公共活动区 / 走廊）或居家失智老人常驻区域固定摄像头（**可选麦克风**）音视频，识别 7 类场景（dementia_orientation_none / mild / question / gaze_drift / wandering / agitation / strong）→ 视频核心 6 项（突然停止活动持续时间 ≥ 5s / 眼神游离评分 / 四处张望次数 / 面部困惑评分 / 游荡事件 / 激越视觉信号）+ 音频可选 4 项（定向问题计数 / 5 min 内重复次数 / 语音焦虑评分 / 呼喊家人姓名）→ 4 档困惑等级（mild / moderate / strong / urgent）→ **4 级定向安抚策略递进**（当前时间地点温和提示 ≤ 55 dB → 家庭成员介绍录音 + 柔光 ≤ 30 lux 暖光 → 主照护者 APP 提醒 + 就近工作人员 → 紧急推送 + 机构值班护士 + 本地引导音）→ 3 分钟效果评估 + 自动升级 → 单日动作上限管控（mild × 12 / moderate × 8 / strong × 4 / Level 4 不设上限）→ 当日定向安抚汇总（晚交班前发送给主照护者）
- 能力包含：活动中断检测（结合姿态时序）、眼神游离评分、头部扫描计数、面部困惑识别（眉头紧锁 + 嘴唇微张 + 目光呆滞）、游荡识别、激越视觉信号（搓手 / 拉扯衣物 / 反复站起坐下）、定向问题语音识别（"这里是哪 / 你是谁 / 现在几点"等）、5 分钟窗口重复问题计数、语音焦虑评分、呼喊家人姓名识别、人脸 + 声纹绑定到注册老人 ID、年龄段自适应（早期 / 中期 / 晚期失智）、夜间低敏告警模式（避免打扰睡眠）、智能音箱联动（家属预录介绍 + 时间地点提示）、柔光环境联动、照护者 APP 推送、4 级安抚策略递进 + 3 分钟效果评估 + 自动升级、单日动作上限、当日定向安抚汇总报告（晚交班前发送）、连续 7 日反复显著困惑 → 提示当地认知症评估门诊 / 老年精神科资源
- 触发条件:
    1. **默认触发**：当用户提供失智照护机构或家庭固定摄像头（可选麦克风）音视频 URL 或文件需要分析时，默认触发本技能进行失智老人困惑/迷惘识别与定向安抚
    2. 当用户明确提及失智老人、阿尔茨海默、认知症、定向障碍、老人困惑、老人迷惘、老人四处张望、老人游荡、老人激越、定向安抚、家庭成员介绍录音等关键词，并且上传了音视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看失智老人定向安抚历史报告、定向安抚日志清单、老人困惑事件清单、查询历史定向安抚记录、显示所有失智老人安抚报告、显示认知症定向安抚日志，查询老人困惑清单
- 自动行为：
    1. 如果用户上传了附件或者音视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有失智老人定向安抚报告"、"
       显示所有老人困惑事件"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_dementia_confusion_orientation_analysis --list --open-id` 参数调用 API
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

**在执行失智老人困惑/迷惘识别与定向安抚前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备失智老人活动区域固定摄像头（可选麦克风）音视频输入**
        - 提供本地路径或网络 URL，**优先实时流接入**
        - 摄像头建议：覆盖老人常驻活动区域（认知症单元 / 公共活动区 / 走廊 / 居家客厅），能看到面部和上半身
        - 帧率 ≥ 10 FPS、分辨率 ≥ 720p
        - 音频可选：采样率 ≥ 16kHz（用于定向问题识别 + 声纹绑定）；无麦克风时仅依赖视觉信号
        - 时段：默认全天 06:00 - 22:00 启用，夜间切换为低敏告警模式
        - 多老人场景按目标跟踪 + 人脸/声纹绑定到注册老人 ID（每位老人独立基线）
        - 家属或机构必须授权部署，机构场景需公示告知，家属同意书归档
        - 可选附带：老人姓名、失智阶段（early / mid / late）、阈值覆盖、家属预录介绍音清单、时间地点话术模板、主照护者 APP token
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（家属或机构授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行失智老人困惑/迷惘识别与定向安抚**
        - 调用 `-m scripts.smyx_dementia_confusion_orientation_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地失智照护机构/家庭固定摄像头（可选麦克风）音视频文件路径
            - `--url`: 网络失智照护机构/家庭固定摄像头（可选麦克风）音视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，失智老人定向安抚场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，家属或机构授权）
            - `--list`: 显示失智老人困惑/迷惘识别与定向安抚历史记录清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的失智老人定向安抚报告
        - 包含：事件 ID（event_id）、事件时间戳（event_timestamp）、老人 ID（elder_id）、失智阶段（dementia_stage：early/mid/late）、场景判定（scene_label：dementia_orientation_none / mild / question / gaze_drift / wandering / agitation / strong）、视频信号（video_signals：sudden_activity_stop_sec / gaze_drifting_score / head_scanning_event_count / facial_confusion_score / wandering_event_detected / agitation_visual_detected）、音频信号（audio_signals：orientation_question_count / orientation_question_repeat_count / voice_anxiety_score / calling_family_event_count）、上下文（context：is_within_active_window / time_since_last_soothing_min / location_label）、困惑等级（confusion_level：mild / moderate / strong / urgent）、定向安抚动作列表（soothing_actions：play_time_location_cue / play_family_intro / ambient_soft_light / caregiver_app_push / emergency_nurse_push / local_guidance_chime，每项含 action_type / message / target / level / volume_db / brightness_lux）、3 分钟后效果（effectiveness_after_3min：settled / partially_settled / unchanged / escalated）、当日汇总（daily_summary，**晚交班前发送**）、建议动作（recommend_action：trigger_level_N_soothing / push_caregiver_app / urgent_intervention / observe_only）
        - **重要提示**：仅输出基于音视频的客观困惑事件检测与温和定向安抚动作，**不构成任何阿尔茨海默病 / 血管性痴呆 / 路易体痴呆等医学诊断**

## 资源索引

- 必要脚本：见 [scripts/smyx_dementia_confusion_orientation_analysis.py](scripts/smyx_dementia_confusion_orientation_analysis.py)(
  用途：调用 API 进行失智老人困惑/迷惘识别与定向安抚，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、音频/视频信号、7 类场景判定、4 级定向安抚策略、单日动作上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov + 音轨，最大 10MB；摄像头需对准老人常驻活动区域；麦克风可选但强烈推荐（用于定向问题识别）
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **4 级定向安抚策略递进**（mild → moderate → strong → urgent/Level 4），3 分钟未平复自动升级
- 单日动作上限：mild × 12 / moderate × 8 / strong × 4 / Level 4 不设上限（紧急安全优先）
- 红线约束：
    - **禁止**对老人做"阿尔茨海默病 / 血管性痴呆 / 路易体痴呆 / 额颞叶痴呆"等医学诊断
    - **禁止**长期存储老人隐私音视频（≤ 7 天，仅入库困惑事件片段；机构按伦理审查规范缩短至 ≤ 72 小时）
    - **禁止**用于商业广告 / AI 训练；禁第三方共享
    - **禁止**冷白光（≥ 4000K）或亮度 > 30 lux 的环境灯（避免黄昏综合征加重）
    - **禁止**安抚音量 > 55 dB（兼顾听力衰退但不可造成惊吓）
    - **绝对禁止**使用 AI 克隆 / 合成家庭成员声音冒充本人录音；必须使用家属本人提前授权的预录音
    - **禁止**使用"您不是说过 / 您忘了吗 / 又问一遍了"等否定 / 矫正语；定向安抚语必须温和、当下、具体
    - **禁止**未经公示在机构场景部署；家属需签同意书并支持退出机制
- **必须**：连续 7 日反复显著困惑事件 → 提示**当地认知症评估门诊**或**老年精神科**资源
- **必须**：当日定向安抚汇总报告**晚交班前发送给主照护者**（避免夜间打扰老人和家属）
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史定向安抚记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"场景/等级/已执行定向安抚动作"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`失智老人定向安抚-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 场景/等级/已执行定向安抚动作 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 失智老人定向安抚-20260519143200001 | dementia_orientation_question / moderate / 时间地点提示+家属介绍录音 | 2026-05-19 14:32:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地失智老人活动区域音视频（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_dementia_confusion_orientation_analysis --input /path/to/care_unit.mp4 --open-id your-open-id

# 分析网络失智老人活动区域音视频/实时流（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_dementia_confusion_orientation_analysis --url https://example.com/care_unit.mp4 --open-id your-open-id

# 显示历史定向安抚记录清单（自动触发关键词：查看失智老人定向安抚历史报告、定向安抚日志清单等）
python -m scripts.smyx_dementia_confusion_orientation_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_dementia_confusion_orientation_analysis --input cu.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_dementia_confusion_orientation_analysis --input cu.mp4 --open-id your-open-id --output result.json
```
