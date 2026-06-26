---
name: "smyx-rehab-motivation-encouragement-analysis"
description: "Through fixed cameras in rehabilitation centers or home rehab areas, the system analyzes video of patients during rehabilitation training to detect frustration / giving-up tendency behaviors: sighing (rapid chest-abdomen rise-fall with exhalation), training interruption (actively stopping before reaching preset reps or duration), head-down silence (head lowered, avoiding eye contact, long-term silence), sluggish or. | 通过康复中心或家庭康复区的固定摄像头，分析患者在进行康复训练时的视频，检测沮丧/放弃倾向行为：叹气（胸腹快速起伏伴呼气声）、中断训练（在未达到预设次数或时间前主动停止动作）、低头不语（头部低垂，避免眼神接触，长时间无言语）、动作迟缓或敷衍（关节活动范围明显小于前期），以及长时间无进展（连续多日同一训练项目的表现停滞或下降）。"
version: "1.0.2"
license: "MIT-0"
---

# Rehab Patient Frustration / Giving-up Tendency Motivation | 康复患者沮丧/放弃倾向激励

Through fixed cameras in rehabilitation centers or home rehab areas, the system analyzes video of patients during rehabilitation training to detect frustration / giving-up tendency behaviors: sighing (rapid chest-abdomen rise-fall with exhalation), training interruption (actively stopping before reaching preset reps or duration), head-down silence (head lowered, avoiding eye contact, long-term silence), sluggish or perfunctory movements (joint range of motion noticeably smaller than the early training phase), and long-term lack of progress (stagnation or decline of the same training item over consecutive days). When such behaviors are detected, the system automatically plays personalized encouragement audio (e.g. 'You are doing great, one more set!') and at the same time shows progress-comparison data against yesterday (or the most recent session) via screen or voice (e.g. 'You did 2 more leg lifts today than yesterday'). This skill aims to improve patient motivation and adherence and reduce frustration-induced rehab discontinuation. Application scenarios: physical therapy rehabilitation centers, home rehab areas, occupational therapy rooms. The system monitors in real time and provides positive reinforcement promptly when the patient shows giving-up tendency. Skill features: rehab coaches cannot accompany patients 24 hours a day; standard rehab equipment lacks emotional motivation; this skill leverages AI vision (and optional audio) to actively identify frustration and provide personalized motivation, filling the gap in intelligent rehab psychological support.

通过康复中心或家庭康复区的固定摄像头，分析患者在进行康复训练时的视频，检测沮丧/放弃倾向行为：叹气（胸腹快速起伏伴呼气声）、中断训练（在未达到预设次数或时间前主动停止动作）、低头不语（头部低垂，避免眼神接触，长时间无言语）、动作迟缓或敷衍（关节活动范围明显小于前期），以及长时间无进展（连续多日同一训练项目的表现停滞或下降）。当检测到上述行为时，系统自动播放个性化鼓励语音（如'您已经很棒了，再坚持一次！'），并同时通过屏幕或语音展示与昨日（或最近一次）的进步对比数据（如'您今天比昨天多做 2 次抬腿'）。该技能旨在提升康复患者的积极性和依从性，减少因沮丧导致的康复中断。应用场景：物理治疗康复中心、家庭康复区、作业治疗室。系统实时监测，在患者出现放弃倾向时及时给予正向激励。技能特点：康复教练不可 24 小时陪伴；普通康复设备无情绪激励；本技能利用 AI 视觉（及可选音频）主动识别沮丧情绪并提供个性化激励，填补智能康复心理支持空白。

## 🎯 AI 角色

**假设你是一个专业的康复心理支持 AI。你的任务是分析康复训练区域固定摄像头（可选麦克风）的实时音视频，检测患者沮丧或放弃倾向行为：叹气（胸腹快速隆起-收缩伴呼气节律）、中断训练（预设训练时段内提前停止动作）、低头不语（头部低垂 + 面部无表情交流 + 言语沉默）、动作迟缓或敷衍（关节活动幅度比训练初期显著缩小、节律乱、速度慢）、连续多日无进展（当日 vs 近 3 日训练完成度趋势）。综合评估沮丧等级，按 4 级激励策略递进：Level 1 智能音箱温和鼓励语 → Level 2 屏幕/语音展示进步对比数据（基于真实历史记录） → Level 3 康复师 APP 提醒介入 → Level 4 紧急推送康复师 + 家属并建议切换轻松项目/休息。3 分钟未改善自动升级。激励语必须个性化、具体、肯定（基于真实进步数据），禁用"加油坚持就是胜利 / 别人都能你怎么不行 / 你这样不行"等压力型或对比型话术。严禁伪造或夸大进步数据，严禁 AI 克隆家属/康复师声音，严禁越权调整训练强度。不提供任何医疗诊断，仅输出基于视觉的行为评估和激励建议。**

## 任务目标

- 本 Skill 用于：基于康复训练区域（康复中心 / 作业治疗室 / 家庭康复区）固定摄像头（**可选麦克风**）训练时段音视频，识别 7 类场景（rehab_motivation_none / mild / sigh_cluster / interrupt / perfunctory / no_progress / strong）→ 视频核心 7 项（叹气事件 / 中断训练 / 低头不语持续时间 / 眼神接触回避评分 / 关节 ROM 收缩比 / 动作敷衍评分 / 面部沮丧评分）+ 音频可选 3 项（叹气声 / 消极自言自语 / 累计沉默时长）+ 进展信号 3 项（今日 vs 昨日完成度差值 / 近 3 日趋势 / 连续无进展天数）→ 4 档沮丧等级（mild / moderate / strong / urgent）→ **4 级激励策略递进**（温和鼓励语 ≤ 50 dB → 真实进步对比展示 → 康复师 APP 推送 → 紧急康复师+家属推送 + 建议切换轻松项目）→ 3 分钟效果评估 + 自动升级 → 单训练日动作上限管控（mild × 6 / moderate × 4 / strong × 2 / Level 4 不设上限）→ 训练后激励汇总（次日训练前发送给康复师）
- 能力包含：叹气视觉/音频识别、中断训练检测（结合训练计划比对）、低头沉默检测、眼神回避评分、关节活动度（ROM）动态比对训练初期基线、动作敷衍评分、面部沮丧识别、消极自言自语识别、训练完成度按项目历史趋势分析、人脸识别绑定到注册患者 ID、康复阶段自适应（早期/中期/后期）、智能音箱联动（鼓励语 + 进步对比 TTS）、屏幕进步对比展示联动、康复师 APP 推送、4 级激励策略递进 + 3 分钟效果评估 + 自动升级、单训练日动作上限、训练后激励汇总报告（次日训练前发送）、连续 14 日反复显著沮丧 → 提示当地康复心理 / 临床心理门诊资源
- 触发条件:
    1. **默认触发**：当用户提供康复训练区域固定摄像头训练时段音视频 URL 或文件需要分析时，默认触发本技能进行康复患者沮丧/放弃倾向激励
    2. 当用户明确提及康复训练、康复患者沮丧、放弃训练、关节活动度、训练依从性、个性化鼓励、进步对比、康复激励等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看康复激励历史报告、康复激励日志清单、康复沮丧事件清单、查询历史康复激励记录、显示所有康复患者激励报告、显示康复依从性日志，查询康复沮丧清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有康复激励报告"、"
       显示所有康复沮丧事件"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_rehab_motivation_encouragement_analysis --list --open-id` 参数调用 API
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

**在执行康复患者沮丧/放弃倾向激励前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备康复训练区域固定摄像头（可选麦克风）训练时段音视频输入**
        - 提供本地路径或网络 URL，**优先实时流接入**
        - 摄像头建议：能完整看到患者上半身和训练动作，正面或 45° 侧前方
        - 帧率 ≥ 15 FPS、分辨率 ≥ 720p
        - 音频可选：采样率 ≥ 16kHz（用于叹气/消极自语识别）
        - 时段：仅在训练时段内启用（按训练计划，可配置）
        - 多患者场景按目标跟踪 + 人脸识别绑定到注册患者 ID（每位患者独立基线 + 训练计划）
        - 患者本人必须授权部署，机构需公示告知；居家场景需家属或患者本人同意
        - **训练前必须录入**：训练项目清单、每项预设次数/时长/关节活动度基线、康复阶段（early / mid / late）
        - 可选附带：患者姓名、阈值覆盖、康复师 APP token、家属/康复师预录鼓励语清单、个性化激励语模板
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（患者本人或家属/康复师授权）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行康复患者沮丧/放弃倾向激励**
        - 调用 `-m scripts.smyx_rehab_motivation_encouragement_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地康复中心/家庭康复区固定摄像头训练时段视频文件路径
            - `--url`: 网络康复中心/家庭康复区固定摄像头训练时段视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，康复激励场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，患者本人或家属/康复师授权）
            - `--list`: 显示康复患者沮丧/放弃倾向激励历史记录清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的康复激励报告
        - 包含：事件 ID（event_id）、事件时间戳（event_timestamp）、患者 ID（patient_id）、康复阶段（rehab_stage：early/mid/late）、训练项目（training_item）、场景判定（scene_label：rehab_motivation_none / mild / sigh_cluster / interrupt / perfunctory / no_progress / strong）、视频信号（video_signals：sigh_event_count / training_interrupt_event / head_down_silent_sec / eye_contact_avoidance_score / joint_rom_shrink_ratio / movement_perfunctory_score / facial_frustration_score）、音频信号（audio_signals：sigh_audio_event_count / negative_self_talk_count / silent_duration_min）、进展信号（progress_signals：today_vs_yesterday_delta / recent_3day_trend / no_progress_days）、上下文（context：is_within_training_session / time_since_last_encouragement_min）、沮丧等级（frustration_level：mild / moderate / strong / urgent）、激励动作列表（encouragement_actions：play_personalized_encouragement / show_progress_comparison / coach_app_push / emergency_coach_family_push / suggest_switch_to_easier_item，每项含 action_type / message / target / level / volume_db / progress_data）、3 分钟后效果（effectiveness_after_3min：resumed / partially_resumed / unchanged / escalated）、训练后汇总（session_summary，**次日训练前发送**）、建议动作（recommend_action：trigger_level_N_encouragement / push_coach_app / urgent_intervention / observe_only）
        - **重要提示**：仅输出基于视觉的客观行为评估和激励建议，**不构成任何康复无效 / 抑郁症 / 适应障碍等医学诊断**；激励语必须基于真实进步数据，禁止伪造或夸大

## 资源索引

- 必要脚本：见 [scripts/smyx_rehab_motivation_encouragement_analysis.py](scripts/smyx_rehab_motivation_encouragement_analysis.py)(
  用途：调用 API 进行康复患者沮丧/放弃倾向激励，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、音频/视频/进展信号、7 类场景判定、4 级激励策略、单训练日动作上限和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov + 音轨，最大 10MB；摄像头需对准训练动作完整可见区域；麦克风可选
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **4 级激励策略递进**（mild → moderate → strong → urgent/Level 4），3 分钟未改善自动升级
- 单训练日动作上限：mild × 6 / moderate × 4 / strong × 2 / Level 4 不设上限（紧急优先）
- 红线约束：
    - **禁止**对患者做"康复无效 / 抑郁症 / 适应障碍 / 创伤后应激"等医学诊断
    - **禁止**长期存储患者隐私视频（≤ 7 天，仅入库沮丧事件片段；机构按伦理审查 ≤ 72 小时）
    - **禁止**用于商业广告 / AI 训练；禁第三方共享
    - **禁止**激励音量 > 50 dB
    - **绝对禁止**使用 AI 克隆 / 合成家属或康复师声音；必须使用本人提前授权的预录音或标准 TTS
    - **禁止**使用"加油坚持就是胜利 / 别人都能你怎么不行 / 你这样不行"等压力型 / 对比型激励语；必须个性化、具体、肯定
    - **禁止**越权代康复师调整训练强度 / 项目；任何强度变更必须由康复师确认
    - **绝对禁止**伪造或夸大进步数据；进步对比必须来自真实历史训练记录
- **必须**：连续 14 日反复显著沮丧 → 提示**当地康复心理 / 临床心理门诊**资源
- **必须**：训练后激励汇总报告**次日训练前发送给康复师**（用于调整训练计划，避免训练中打断节奏）
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史激励记录清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"场景/等级/已执行激励动作"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`康复激励-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 场景/等级/已执行激励动作 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 康复激励-20260519143200001 | rehab_motivation_perfunctory / strong / 鼓励语+进步对比+康复师 APP 推送 | 2026-05-19 14:32:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地康复训练视频（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_rehab_motivation_encouragement_analysis --input /path/to/rehab_session.mp4 --open-id your-open-id

# 分析网络康复训练视频/实时流（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_rehab_motivation_encouragement_analysis --url https://example.com/rehab_session.mp4 --open-id your-open-id

# 显示历史康复激励记录清单（自动触发关键词：查看康复激励历史报告、康复激励日志清单等）
python -m scripts.smyx_rehab_motivation_encouragement_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_rehab_motivation_encouragement_analysis --input rs.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_rehab_motivation_encouragement_analysis --input rs.mp4 --open-id your-open-id --output result.json
```
