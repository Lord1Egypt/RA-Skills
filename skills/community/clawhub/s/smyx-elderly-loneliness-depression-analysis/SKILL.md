---
name: "smyx-elderly-loneliness-depression-analysis"
description: "Using fixed cameras at home (living room, bedroom) of elderly people living alone, the system analyzes daily videos and detects negative behavior indicators during solo time: dazing (long-duration motionless gazing without purposeful action), sighing (rapid chest rise-and-fall with audible expiration), and self-talking (mouth movement without any conversation partner). It counts the frequency and duration of these behaviors and comprehensively evaluates the elder's emotional risk level (low / medium / high). The skill assists family members or community workers in understanding the elder's mental state and timely providing emotional care or psychological intervention. Application scenarios: homes of solo-living elders, nursing homes, community daycare centers. The system generates a daily emotional-risk report; when the risk level is 'medium' or 'high', it pushes reminders. Skill features: loneliness and depression in the elderly are common mental-health issues, and early behavioral signals are often overlooked. AI automatic monitoring of dazing / sighing / self-talking helps family members detect mental abnormalities early, intervene promptly, and improve the elder's quality of life. Can be integrated into home-care cameras or community health-management platforms. | 通过独居老人在家中的固定摄像头（如客厅、卧室），分析日常视频，检测独处期间的消极行为指标：发呆（长时间静止注视，缺乏目的性动作）、叹气（胸部快速起伏伴呼气声）、自言自语（口部活动但无对话对象）等。统计这些行为的发生频次和持续时间，综合评估老年人潜在的情绪风险等级（低/中/高）。该技能可辅助家属或社区工作者了解老人心理状态，及时进行情感关怀或心理干预。应用场景：独居老人家庭、养老院、社区日间照料中心。系统每日生成情绪风险报告，当风险等级为'中'或'高'时推送提醒。技能特点：老年人孤独和抑郁是常见的心理健康问题，早期行为信号常被忽视。通过AI自动监测发呆、叹气、自言自语等行为，可辅助家属及早发现心理异常，及时干预，提高老年人生活质量。该技能可集成到居家养老摄像头或社区健康管理平台中。"
version: "1.0.0"
---

# Elderly Loneliness / Depression-Tendency Behavior Analysis | 老年人孤独/抑郁倾向行为分析

Using fixed cameras at home (living room, bedroom) of elderly people living alone, the system analyzes daily videos and detects negative behavior indicators during solo time: dazing (long-duration motionless gazing without purposeful action), sighing (rapid chest rise-and-fall with audible expiration), and self-talking (mouth movement without any conversation partner). It counts the frequency and duration of these behaviors and comprehensively evaluates the elder's emotional risk level (low / medium / high). The skill assists family members or community workers in understanding the elder's mental state and timely providing emotional care or psychological intervention. Application scenarios: homes of solo-living elders, nursing homes, community daycare centers. The system generates a daily emotional-risk report; when the risk level is 'medium' or 'high', it pushes reminders. Skill features: loneliness and depression in the elderly are common mental-health issues, and early behavioral signals are often overlooked. AI automatic monitoring of dazing / sighing / self-talking helps family members detect mental abnormalities early, intervene promptly, and improve the elder's quality of life. Can be integrated into home-care cameras or community health-management platforms.

通过独居老人在家中的固定摄像头（如客厅、卧室），分析日常视频，检测独处期间的消极行为指标：发呆（长时间静止注视，缺乏目的性动作）、叹气（胸部快速起伏伴呼气声）、自言自语（口部活动但无对话对象）等。统计这些行为的发生频次和持续时间，综合评估老年人潜在的情绪风险等级（低/中/高）。该技能可辅助家属或社区工作者了解老人心理状态，及时进行情感关怀或心理干预。应用场景：独居老人家庭、养老院、社区日间照料中心。系统每日生成情绪风险报告，当风险等级为'中'或'高'时推送提醒。技能特点：老年人孤独和抑郁是常见的心理健康问题，早期行为信号常被忽视。通过AI自动监测发呆、叹气、自言自语等行为，可辅助家属及早发现心理异常，及时干预，提高老年人生活质量。该技能可集成到居家养老摄像头或社区健康管理平台中。

## 🎯 AI 角色

**假设你是一个专业的老年人心理健康监测 AI。你的任务是分析固定摄像头拍摄的日常视频，检测老年人在独处期间的特定行为：发呆（连续注视某处超过 10 秒且无肢体活动）、叹气（胸腹部快速起伏伴呼吸音）、自言自语（口部开合但无对话对象）。统计这些行为的发生频次和持续时间，综合评估情绪风险等级。不要提供医疗诊断或心理量表评分，仅输出基于视觉和行为统计的风险提示。**

## 任务目标

- 本 Skill 用于：基于独居老人客厅/卧室固定摄像头视频（可选麦克风），识别独处期间的消极行为指标 → 统计频次/累计时长 → 与个人基线对比 → 综合输出情绪风险等级（低/中/高）+ 友好提醒
- 能力包含：人体检测与独处时间窗口判定（画面中仅有老人本人）、发呆事件识别（连续静止注视 ≥ 10s 且无肢体活动）、叹气事件识别（胸腹快速起伏 + 可选呼气声）、自言自语识别（口部活动 + 无对话对象 + 可选低音量语音）、社交互动时长统计（反向指标）、卧床时长（参考指标）、与个人 7-14 天基线对比、连续异常天数累计、风险等级综合判定、家属/社工友好提醒文本生成
- 触发条件:
    1. **默认触发**：当用户提供独居老人活动区域固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行孤独/抑郁倾向行为分析
    2. 当用户明确提及老年人孤独、独居老人抑郁、发呆、叹气、自言自语、心理关怀、情绪低落、社区养老健康等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看老人孤独/抑郁历史报告、情绪风险报告清单、独居老人心理报告清单、查询历史情绪风险记录、显示所有老人孤独行为报告、显示养老心理健康诊断报告，查询情绪风险预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有老人孤独抑郁报告"、"
       显示所有情绪风险报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_elderly_loneliness_depression_analysis --list --open-id` 参数调用 API
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

**在执行老年人孤独/抑郁倾向行为分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备独居老人活动区域固定摄像头视频输入**
        - 提供本地视频路径或网络 URL，建议覆盖白天完整时段
        - 摄像头建议：独居老人家中客厅/卧室/起居室固定摄像头，覆盖老人主要日常活动区域，**能看到上半身和面部**
        - 帧率 ≥ 5 FPS（推荐 10-15 FPS）、分辨率 ≥ 480p、光照稳定
        - 可选附带麦克风（用于叹气声 / 自言自语判定）；多人场景下可结合"独处时间窗口"过滤
        - 隐私敏感场景可启用人体轮廓 + 面部马赛克模式
        - 可选附带：老人姓名、年龄、近期重大事件（如丧偶/搬家）、阈值覆盖（daze_min_duration_sec / sigh_per_hour_threshold）
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行老年人孤独/抑郁倾向行为分析**
        - 调用 `-m scripts.smyx_elderly_loneliness_depression_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地独居老人活动区域固定摄像头视频文件路径
            - `--url`: 网络独居老人活动区域固定摄像头视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，老年人心理健康监测场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示老年人孤独/抑郁倾向行为历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的老年人孤独/抑郁倾向行为分析报告
        - 包含：是否检测到老人（subject_detected）、是否处于独处窗口（solo_window）、各项消极行为统计（behavior_metrics：daze_event_count / daze_total_duration_min / sigh_event_count_hourly / sigh_event_count_daily / self_talk_event_count_daily / social_interaction_minutes_daily / lying_in_bed_duration_daily_min）、与个人 7-14 天基线对比（baseline_comparison：per_item_delta_pct）、连续异常天数（consecutive_abnormal_days）、风险等级（risk_level：low / medium / high）、提醒类型（alert_type：loneliness_risk / depression_tendency_suspected / normal）、提醒级别（alert_level：info / notice / warning）、推送给家属/社工的友好文本（如"妈妈今天独自发呆约 1 小时，叹气次数比平时多了一倍，建议今晚视频通话陪她聊聊"）、建议动作（recommend_action：push_family_notice / suggest_video_call / suggest_community_visit / observe_only）
        - **重要提示**：仅输出基于视觉/音频的客观行为统计与友好提醒，**不提供抑郁症诊断、GDS-15 / PHQ-9 等量表评分或处方**；任何诊断与治疗方案必须由精神科医生或心理咨询师评估制定；若老人出现明显自我伤害言语或行为请立即联系专业机构

## 资源索引

- 必要脚本：见 [scripts/smyx_elderly_loneliness_depression_analysis.py](scripts/smyx_elderly_loneliness_depression_analysis.py)(
  用途：调用 API 进行老年人孤独/抑郁倾向行为分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、消极行为阈值/风险等级定义和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：必须能看到老人上半身与面部
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 老人看电视/看书/打盹与"发呆"在视觉上易混淆，建议结合时长 + 周期性运动 + 面部表情综合判定
- 多代同堂、保姆陪护等场景需启用"独处时间窗口"过滤，否则会低估孤独风险
- 本工具不构成抑郁症筛查工具，**不替代** GDS-15 / PHQ-9 / 心理咨询师评估
- 隐私合规：独居老人家庭视频涉及高度敏感个人隐私，使用前需取得老人本人明确知情同意，妥善加密保管；建议优先采用人体轮廓 + 面部马赛克模式
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"风险等级/主要表现"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`老年人孤独抑郁倾向报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 风险等级/主要表现 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 老年人孤独抑郁倾向报告-20260312172200001 | medium（发呆 65min + 叹气 12 次/h，连续 3 天） | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地独居老人活动区域视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_elderly_loneliness_depression_analysis --input /path/to/livingroom.mp4 --open-id your-open-id

# 分析网络独居老人活动区域视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_elderly_loneliness_depression_analysis --url https://example.com/livingroom.mp4 --open-id your-open-id

# 显示历史老年人孤独/抑郁倾向行为报告（自动触发关键词：查看老人孤独/抑郁历史报告、情绪风险报告清单等）
python -m scripts.smyx_elderly_loneliness_depression_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_elderly_loneliness_depression_analysis --input lr.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_elderly_loneliness_depression_analysis --input lr.mp4 --open-id your-open-id --output result.json
```
