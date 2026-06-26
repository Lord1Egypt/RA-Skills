---
name: "smyx-elderly-loneliness-comfort-analysis"
description: "Using a fixed camera in the home of a solitary-living elderly person or in a private nursing-home room, the system analyzes daily activity video and detects loneliness-related behaviors: prolonged solitude (no social interaction), static gazing (long-time fixation with no purposeful activity), sighing (rapid chest/abdomen rise-fall with exhale), and talking-to-self (mouth activity with no conversation partner). It computes a composite loneliness index (0-100). When the index exceeds a threshold, warm-companionship actions are automatically triggered: playing pre-recorded warm voice messages from children via smart speakers, playing the elder's favorite old songs, or pushing reminders to the children's mobile app (e.g., 'Dad seems lonely today — a video call is recommended'). The skill aims to relieve loneliness and improve mental well-being. Application scenarios: homes of solitary-living elderly, private nursing-home rooms, community day-care centers. The system monitors in real time and intervenes proactively when the loneliness index exceeds threshold. Skill features: chronic loneliness is a major risk factor for depression and cognitive decline in older adults. AI auto-identification of loneliness signals followed by timely voice care or reminders to children can effectively alleviate negative emotions and improve quality of life. Can be integrated into smart cameras or elderly-care service platforms as a key emotional-support feature of 'smart aging'. | 通过独居老人家中或养老院单人房的固定摄像头，分析老人日常行为视频，检测孤独相关行为：长时间独处（无社交互动）、静止发呆（长时间凝视一处无目的活动）、叹气（胸腹快速起伏伴呼气）、自言自语（口部活动但无对话对象）等。综合计算孤独指数（0-100），当指数超过阈值时自动触发温暖陪伴动作：通过智能音箱播放子女预录的温馨语音、播放老人喜爱老歌、或向子女手机APP推送提醒（'父亲今天显得孤独，建议视频通话'）。该技能旨在缓解老人孤独感，提升心理健康。应用场景：独居老人家庭、养老院单人房、社区日间照料中心。系统实时监测，当孤独指数超标时主动干预。技能特点：长期孤独是老年人抑郁、认知下降的重要风险因素。通过AI自动识别孤独信号并及时给予语音关怀或提醒子女，可有效缓解老人负面情绪，提升生活质量。该技能可集成到智能摄像头或养老服务平台中，成为'智慧养老'情感支持的关键功能。"
version: "1.0.0"
---

# Elderly Loneliness Detection & Warm Companionship | 独居老人孤独情绪识别与温暖陪伴

Using a fixed camera in the home of a solitary-living elderly person or in a private nursing-home room, the system analyzes daily activity video and detects loneliness-related behaviors: prolonged solitude (no social interaction), static gazing (long-time fixation with no purposeful activity), sighing (rapid chest/abdomen rise-fall with exhale), and talking-to-self (mouth activity with no conversation partner). It computes a composite loneliness index (0-100). When the index exceeds a threshold, warm-companionship actions are automatically triggered: playing pre-recorded warm voice messages from children via smart speakers, playing the elder's favorite old songs, or pushing reminders to the children's mobile app (e.g., 'Dad seems lonely today — a video call is recommended'). The skill aims to relieve loneliness and improve mental well-being. Application scenarios: homes of solitary-living elderly, private nursing-home rooms, community day-care centers. The system monitors in real time and intervenes proactively when the loneliness index exceeds threshold. Skill features: chronic loneliness is a major risk factor for depression and cognitive decline in older adults. AI auto-identification of loneliness signals followed by timely voice care or reminders to children can effectively alleviate negative emotions and improve quality of life. Can be integrated into smart cameras or elderly-care service platforms as a key emotional-support feature of 'smart aging'.

通过独居老人家中或养老院单人房的固定摄像头，分析老人日常行为视频，检测孤独相关行为：长时间独处（无社交互动）、静止发呆（长时间凝视一处无目的活动）、叹气（胸腹快速起伏伴呼气）、自言自语（口部活动但无对话对象）等。综合计算孤独指数（0-100），当指数超过阈值时自动触发温暖陪伴动作：通过智能音箱播放子女预录的温馨语音、播放老人喜爱老歌、或向子女手机APP推送提醒（'父亲今天显得孤独，建议视频通话'）。该技能旨在缓解老人孤独感，提升心理健康。应用场景：独居老人家庭、养老院单人房、社区日间照料中心。系统实时监测，当孤独指数超标时主动干预。技能特点：长期孤独是老年人抑郁、认知下降的重要风险因素。通过AI自动识别孤独信号并及时给予语音关怀或提醒子女，可有效缓解老人负面情绪，提升生活质量。该技能可集成到智能摄像头或养老服务平台中，成为'智慧养老'情感支持的关键功能。

## 🎯 AI 角色

**假设你是一个专业的老年人心理健康关怀 AI。你的任务是分析独居老人活动区域的固定摄像头视频（可选叠加音频），检测孤独相关行为：连续独处时长（无他人进入画面）、长时间静止凝视（≥ 10 分钟无肢体活动）、叹气次数（视觉胸腹起伏+长呼气，音频可补强）、自言自语频次（口部活动但无对话对象）。综合计算孤独指数（0-100，含哼歌/电话通话等正向行为扣分项），当超过阈值时输出温暖陪伴动作建议：智能音箱播放子女预录温馨语音、播放老人喜爱老歌、子女 APP 推送提醒。不提供任何医疗诊断，仅输出基于行为统计的结果，并尊重老人"一句话关闭今日提醒"的意愿。**

## 任务目标

- 本 Skill 用于：基于独居老人家中/养老院单人房固定摄像头（可选音频）视频，识别孤独相关行为（连续独处时长 / 当日累计独处 / 长时间静止凝视 / 视觉+音频叹气 / 自言自语 / 皱眉木然面部比例）+ 正向行为（笑容 / 哼歌 / 电话通话）→ 综合计算 **孤独指数（0-100，含正向扣分）** + 14 天个人基线对比 → 输出 4 档孤独等级（light / mild / notable / heavy）+ 4 类温暖陪伴动作建议（智能音箱子女语音 / 老歌播放 / 子女 APP 推送 / 社区日间照料推荐）+ 给子女的友好摘要
- 能力包含：人体姿态识别（独处/静止/凝视判定）、独居判定（≥ 30 分钟仅老人一人）、视觉叹气识别（胸腹起伏+长呼气姿态）、自言自语识别（口部活动+无对话对象在场）、笑容识别、哼歌/唱歌识别（可选音频）、电话/视频通话识别、社交互动事件识别（家人/护工进入、视频通话画面、宠物互动）、目的性活动判别（家务/看电视+点头反馈/园艺/阅读）、孤独指数 0-100 综合算法、14 天个人基线对比、4 档孤独等级、温和前导（"今天为您播放……" 3 秒）+ 老人一句话关闭意愿支持、子女预录语音播放（**禁止 AI 克隆声音**）、heavy 且子女长期无回应时推送社区/街道老龄办资源
- 触发条件:
    1. **默认触发**：当用户提供独居老人家中/养老院单人房固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行独居老人孤独情绪识别与温暖陪伴
    2. 当用户明确提及独居老人、孤独、空巢、子女陪伴、老人发呆、老人唉声叹气、智能音箱关怀、智慧养老、社区日间照料等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看独居老人孤独历史报告、子女关怀日报清单、老人情感关怀报告清单、查询历史孤独情绪记录、显示所有独居老人陪伴报告、显示老人情绪关怀报告，查询孤独情绪预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有独居老人孤独报告"、"
       显示所有子女关怀日报"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_elderly_loneliness_comfort_analysis --list --open-id` 参数调用 API
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

**在执行独居老人孤独情绪识别与温暖陪伴前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备独居老人客厅/卧室/养老院单人房固定摄像头视频输入**
        - 提供本地视频路径或网络 URL，覆盖白天活跃时段（08:00-22:00），**单次分析建议 ≥ 4 小时**
        - 摄像头建议：能看到老人主要活动区域（沙发/餐桌/床位/阳台/厨房）
        - 帧率 ≥ 5 FPS（推荐 10 FPS）、分辨率 ≥ 480p、夜间需红外补光
        - 音频可选（强烈推荐）：用于识别叹气声 + 自言自语 + 哼歌；采样率 ≥ 16kHz
        - ROI 标定：主要活动区域
        - **独居判定**：连续 ≥ 30 分钟画面仅有老人一人 → independent_status = true
        - 隐私敏感场景建议启用人体轮廓 + 面部马赛克模式
        - 可选附带：老人姓名/年龄、子女预录语音清单、老人喜爱老歌清单、阈值覆盖
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行独居老人孤独情绪识别与温暖陪伴**
        - 调用 `-m scripts.smyx_elderly_loneliness_comfort_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地独居老人客厅/卧室/养老院单人房固定摄像头视频文件路径
            - `--url`: 网络独居老人客厅/卧室/养老院单人房固定摄像头视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，老年人心理健康关怀场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示独居老人孤独情绪识别与温暖陪伴历史报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的独居老人孤独情绪识别与温暖陪伴报告
        - 包含：时间窗（time_window）、独居状态（independent_status）、行为指标（behavioral_metrics：solo_duration_minutes / daily_solo_total_minutes / static_gaze_duration_minutes / purposeful_activity_minutes / social_interaction_event_count）、视觉指标（visual_metrics：sigh_visual_event_count / talking_to_self_event_count / frown_neutral_face_ratio / smile_event_count_daily）、音频指标（audio_metrics：sigh_audio_event_count / talking_to_self_audio_event_count / **singing_humming_event_count 正向指标** / phone_call_minutes）、孤独指数（loneliness_index 0-100）、孤独等级（loneliness_level：light / mild / notable / heavy）、与个人 14 天基线对比（comparison_to_baseline_pct）、连续高指数天数（consecutive_high_days）、提醒类型（alert_type：light_no_action / mild_comfort_audio / notable_comfort_plus_app / heavy_strong_care / improving）、提醒级别（alert_level：info / notice / warning）、温暖陪伴动作列表（comfort_actions：smart_speaker_voice / play_favorite_song / children_app_push，每项含 action_type / message / target）、给子女的友好摘要（family_summary，如"今天母亲在客厅独处 6 小时，下午 14:30-15:20 期间静坐凝视窗外约 50 分钟、叹气 7 次，孤独指数 72；已为她播放邓丽君老歌并推送了您预录的语音，建议晚上视频通话，或周末抽空回家陪她吃顿饭"）、建议动作（recommend_action：trigger_smart_speaker_comfort / push_children_video_call_suggestion / suggest_community_volunteer_visit / observe_only）、社区资源（community_resource，heavy 且子女长期无回应时附）
        - **重要提示**：仅输出基于视觉与（可选）音频的客观行为统计与温暖陪伴动作，**不构成老年抑郁症等精神医学诊断**；任何疑似心理健康问题应转介当地老年精神科或社区心理服务

## 资源索引

- 必要脚本：见 [scripts/smyx_elderly_loneliness_comfort_analysis.py](scripts/smyx_elderly_loneliness_comfort_analysis.py)(
  用途：调用 API 进行独居老人孤独情绪识别与温暖陪伴，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、行为/视觉/音频指标、孤独指数算法/4 档等级/4 类温暖动作和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：覆盖老人主要活动区域；时长建议 ≥ 4 小时
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 哼歌/唱歌、电话视频通话、笑容等正向行为**必须**作为负权重纳入孤独指数计算，避免一刀切定义"独处=孤独"
- 老人午睡、看自己喜欢的电视节目并有积极面部反馈 等不应误判为"静止凝视"或孤独
- 红线约束：**禁止**输出"老年抑郁症 / 孤独症"等精神医学诊断或量表评分；**禁止**未经老人与子女双方同意便部署；**禁止**将老人视频/音频用于商业广告或大数据画像；**禁止**长期存储原始视频（≤ 7 天，仅留聚合指标）
- **必须**：智能音箱发声前给予 3 秒温和前导（如"今天为您播放……"）；支持老人一句话关闭今日提醒
- **绝对禁止**使用 AI 克隆/合成子女声音冒充子女语音；子女预录语音必须由子女本人录制
- 当 heavy 且子女连续 ≥ 3 天无回应时，主动提示**社区/街道老龄办**资源
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"孤独指数/等级/已执行陪伴动作"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`独居老人孤独关怀报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 孤独指数/等级/已执行陪伴动作 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 独居老人孤独关怀报告-20260312172200001 | 72 / notable / 子女语音+老歌+APP 推送 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地老人活动区域视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_elderly_loneliness_comfort_analysis --input /path/to/livingroom.mp4 --open-id your-open-id

# 分析网络老人活动区域视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_elderly_loneliness_comfort_analysis --url https://example.com/livingroom.mp4 --open-id your-open-id

# 显示历史独居老人孤独关怀报告（自动触发关键词：查看独居老人孤独历史报告、子女关怀日报清单等）
python -m scripts.smyx_elderly_loneliness_comfort_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_elderly_loneliness_comfort_analysis --input lr.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_elderly_loneliness_comfort_analysis --input lr.mp4 --open-id your-open-id --output result.json
```
