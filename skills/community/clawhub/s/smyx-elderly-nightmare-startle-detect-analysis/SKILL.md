---
name: "smyx-elderly-nightmare-startle-detect-analysis"
description: "Using a fixed bedroom camera (infrared night vision + microphone), the system analyzes elderly nighttime sleep video and detects abnormal events such as sudden sitting-up (quick lying-to-sitting transition), screams (high-pitched short cries), and arm-thrashing (purposeless rapid arm movements), and records the occurrence time, frequency and duration of each event. | 通过卧室固定摄像头（红外夜视），分析老年人夜间睡眠视频，检测突然坐起（快速从躺卧变为坐立）、惊叫声音（高频短促叫声）以及挥舞手臂（无目的性的快速手臂动作）等行为，记录发生时间、频次及持续时间。该技能可帮助家属或护理人员了解老人夜间睡眠质量，识别可能的梦魇、快速眼动期睡眠行为障碍等异常现象，为医疗评估提供参考。"
version: "1.0.2"
license: "MIT-0"
---

# Elderly Sleep Nightmare / Startle Detection | 老年人睡眠中间惊醒/梦魇行为识别

Using a fixed bedroom camera (infrared night vision + microphone), the system analyzes elderly nighttime sleep video and detects abnormal events such as sudden sitting-up (quick lying-to-sitting transition), screams (high-pitched short cries), and arm-thrashing (purposeless rapid arm movements), and records the occurrence time, frequency and duration of each event. This skill helps family members or caregivers understand the elderly person's nighttime sleep quality and identify possible nightmares or REM-sleep Behavior Disorder (RBD), providing reference data for medical evaluation. Application scenarios: home elderly care, nursing homes, neurology sleep monitoring. The system relays monitoring through the night and generates a sleep-abnormality event report. Skill features: frequent nighttime awakenings or nightmares in the elderly may be early manifestations of neurological diseases such as RBD. AI auto-recording of abnormal events provides objective data for physicians, supporting early diagnosis of Parkinson's disease and other neurodegenerative conditions. Can be integrated into smart-home cameras or elderly-care monitoring platforms as an important health-warning tool.

通过卧室固定摄像头（红外夜视），分析老年人夜间睡眠视频，检测突然坐起（快速从躺卧变为坐立）、惊叫声音（高频短促叫声）以及挥舞手臂（无目的性的快速手臂动作）等行为，记录发生时间、频次及持续时间。该技能可帮助家属或护理人员了解老人夜间睡眠质量，识别可能的梦魇、快速眼动期睡眠行为障碍等异常现象，为医疗评估提供参考。应用场景：居家养老、养老院、神经内科睡眠监测。系统夜间接力监测，生成睡眠异常事件报告。技能特点：老年人夜间频繁惊醒、梦魇可能是快速眼动期睡眠行为障碍（RBD）等神经系统疾病的早期表现。通过AI自动记录异常行为，可为医生提供客观数据，帮助早期诊断帕金森病等神经退行性疾病。该技能可集成到智能家居摄像头或养老监护平台中，成为健康预警的重要工具。

## 🎯 AI 角色

**假设你是一个专业的老年人睡眠行为监测 AI。你的任务是分析卧室固定摄像头的夜间视频（含音频），检测老年人睡眠中的异常行为，包括突然坐起、惊叫声音、无目的挥舞手臂、踢腿等。记录每次事件的起止时间、持续时长，统计夜间总频次与高发时段。不要提供医疗诊断，仅输出基于视觉和音频的行为事件统计，并在频繁或疑似 RBD 模式时附神经内科/睡眠门诊就诊建议。**

## 任务目标

- 本 Skill 用于：基于卧室固定摄像头（红外夜视 + 麦克风）夜间睡眠音视频（建议 ≥ 6 小时），识别异常事件（突然坐起 / 无目的挥臂 / 踢腿 / 离床 / 惊叫 / 梦呓 / 异常粗重呼吸）→ 输出事件清单 + 时间线 + 频次密度 + 高发时段 + 睡眠连续性评分 → 推断行为模式（pure_nightmare / suspect_rbd / general_arousal / mixed / none）+ 风险信号等级 + 家属友好摘要 + 神经内科/睡眠门诊就诊建议
- 能力包含：人体姿态识别（躺卧 → 坐立快速切换检测，< 2 秒）、无目的快速挥臂识别、踢腿识别、离床检测（参考）、音频惊叫识别（频谱 + 短时能量）、梦呓 / 异常粗重呼吸识别（参考）、事件时间线生成（含证据短片 ≤ 30 秒）、每小时事件密度统计、高发时段定位（如 03:00-04:00 REM 期）、睡眠连续性评分、行为模式分类、4 档风险信号（none / mild / notable / strong）、家属友好摘要文本生成、专科就诊建议生成
- 触发条件:
    1. **默认触发**：当用户提供卧室固定摄像头（红外夜视、含麦克风）夜间睡眠音视频 URL 或文件需要分析时，默认触发本技能进行老年人睡眠中间惊醒/梦魇行为识别
    2. 当用户明确提及老人夜间惊醒、梦魇、说梦话、半夜坐起、半夜叫喊、挥臂踢腿、RBD、快速眼动行为障碍、帕金森早期、睡眠门诊等关键词，并且上传了音视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看睡眠异常历史报告、夜间惊醒/梦魇报告清单、老人睡眠事件清单、查询历史睡眠异常记录、显示所有夜间异常分析报告、显示睡眠监测报告，查询睡眠异常预警清单
- 自动行为：
    1. 如果用户上传了附件或者音视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有老人睡眠异常报告"、"
       显示所有夜间惊醒报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_elderly_nightmare_startle_detect_analysis --list --open-id` 参数调用 API
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

**在执行老年人睡眠中间惊醒/梦魇行为识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备卧室固定摄像头（红外夜视、含麦克风）夜间睡眠音视频输入**
        - 提供本地音视频路径或网络 URL，**单次分析建议 ≥ 6 小时**，覆盖完整睡眠时段（如 22:00 → 次日 07:00）
        - 摄像头建议：卧室固定摄像头，**必须支持红外夜视（IR）**，**必须含麦克风**，能完整拍到老人在床的上半身
        - 帧率 ≥ 5 FPS、分辨率 ≥ 480p、音频采样率 ≥ 16kHz
        - ROI 标定：床位 ROI（bed_region）
        - 多人共眠场景（如老两口）需按目标跟踪
        - 隐私敏感场景必须启用人体轮廓 + 面部马赛克模式
        - 可选附带：老人姓名、年龄、既往用药、是否已有 PSG 检查结果、阈值覆盖
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行老年人睡眠中间惊醒/梦魇行为识别**
        - 调用 `-m scripts.smyx_elderly_nightmare_startle_detect_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地卧室固定摄像头（红外夜视、含麦克风）夜间睡眠音视频文件路径
            - `--url`: 网络卧室固定摄像头（红外夜视、含麦克风）夜间睡眠音视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，老年人睡眠行为监测场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示老年人睡眠中间惊醒/梦魇行为识别历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的老年人睡眠中间惊醒/梦魇行为识别报告
        - 包含：监测时间窗（sleep_window）、在床时长（bed_occupied_minutes）、视觉事件（visual_events：sudden_sit_up_event_count / arm_thrashing_event_count / kick_leg_event_count / out_of_bed_event_count / total_event_duration_sec）、音频事件（audio_events：scream_event_count / mumble_or_talking_in_sleep_count / loud_breathing_event_count）、异常事件时间线（event_timeline，每条含 start_ts / end_ts / type / duration_sec / evidence_snippet_url，**原始视频不留存**）、异常事件总次数（total_abnormal_event_count）、每小时事件密度（event_density_per_hour）、高发时段（peak_event_hour）、睡眠连续性评分（sleep_continuity_score：0-100）、行为模式（abnormal_pattern：pure_nightmare / suspect_rbd / general_arousal / mixed / none）、风险信号等级（risk_signal_level：none / mild / notable / strong）、提醒类型（alert_type：sleep_abnormal_notable / sleep_abnormal_frequent / suspect_rbd_pattern / improving / normal）、提醒级别（alert_level：info / notice / warning）、家属友好摘要（family_summary，如"昨晚老人在 03:12 突然坐起并伴随短促叫声 1 次，03:38 出现挥舞手臂约 8 秒；夜间共 3 次异常事件，建议白天观察精神状态，若反复出现建议就诊神经内科睡眠门诊"）、建议动作（recommend_action：push_family_summary / suggest_record_diary / suggest_consult_sleep_clinic / suggest_neurology_consult / observe_only）、临床参考（clinical_reference，frequent 或 suspect_rbd_pattern 时附）
        - **重要提示**：仅输出基于视觉与音频的客观行为事件统计，**不构成 RBD / 帕金森病 / 阿尔茨海默病 / 睡眠呼吸暂停等任何医学诊断**；任何疑似神经退行性疾病或睡眠障碍的判定与治疗必须由神经内科 / 睡眠专科医生结合 PSG 等专业检查制定

## 资源索引

- 必要脚本：见 [scripts/smyx_elderly_nightmare_startle_detect_analysis.py](scripts/smyx_elderly_nightmare_startle_detect_analysis.py)(
  用途：调用 API 进行老年人睡眠中间惊醒/梦魇行为识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、视觉/音频事件阈值/行为模式分类/红线约束和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 含音轨视频，最大 10MB；**关键**：必须红外夜视 + 麦克风音轨；时长建议 ≥ 6 小时
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 单次喷嚏、咳嗽、翻身、起夜如厕等正常生理活动不应计入异常事件
- 双人共眠时需正确归属事件到老人，避免家属/伴侣的动作被误归
- 红线约束：**禁止**输出 RBD / 帕金森病 / 阿尔茨海默病 / 睡眠呼吸暂停综合征等任何医学诊断；**禁止**根据本工具结果调整药物；**禁止**长期存储夜间原始视频
- 数据保管：建议仅保存事件片段证据（≤ 30 秒）+ 指标统计，原始视频流不入库
- 当出现 `frequent` 或 `suspect_rbd_pattern` 时，**必须**在摘要中附"建议尽快就诊神经内科 / 睡眠门诊进行 PSG（多导睡眠图）检查"
- 隐私合规：卧室夜间视频涉及高度敏感个人隐私，使用前需取得**老人本人**明确知情同意，妥善加密保管；建议优先采用人体轮廓 + 面部马赛克模式
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"事件数/行为模式/高发时段"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`老人睡眠异常报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 事件数/行为模式/高发时段 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 老人睡眠异常报告-20260312172200001 | 5 次 / suspect_rbd / 03:00-04:00 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地夜间睡眠音视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_elderly_nightmare_startle_detect_analysis --input /path/to/night_sleep.mp4 --open-id your-open-id

# 分析网络夜间睡眠音视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_elderly_nightmare_startle_detect_analysis --url https://example.com/night_sleep.mp4 --open-id your-open-id

# 显示历史老年人睡眠中间惊醒/梦魇报告（自动触发关键词：查看睡眠异常历史报告、夜间惊醒/梦魇报告清单等）
python -m scripts.smyx_elderly_nightmare_startle_detect_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_elderly_nightmare_startle_detect_analysis --input ns.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_elderly_nightmare_startle_detect_analysis --input ns.mp4 --open-id your-open-id --output result.json
```
