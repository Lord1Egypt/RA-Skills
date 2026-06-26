---
name: "smyx-teen-screen-addiction-detection-analysis"
description: "Using fixed cameras at home, study rooms or schools, the system analyzes adolescents' posture while using phones or gaming devices: head pitch angle (downward > 45°) and hand-holding-device posture (hand grasp + bent arm). It counts daily cumulative screen-looking time. When continuous screen-looking exceeds a configured threshold (e.g., single session > 30 minutes, or daily total > 2 hours), a 'phone/game addiction' reminder is generated, suggesting parental guidance and healthy eye-use habits. This helps prevent adolescent myopia, cervical-spine issues and gaming addiction. Application scenarios: family study, adolescent bedroom, study rooms, school classrooms. The system monitors in real time and pushes reminders via mobile APP or links to smart devices to issue voice prompts when over-time use is detected. Skill features: long head-down phone use among adolescents easily causes myopia, cervical-spine disease and social barriers. AI auto-monitoring and reminders help parents objectively understand their child's eye-use habits, enabling timely intervention and protecting vision. Can be integrated into smart-home cameras or family-education APPs as a practical family-health management tool. | 通过家庭、自习室或学校固定摄像头，分析青少年使用手机或游戏设备的姿势，检测头部低垂角度（俯仰角大于45°）以及手持设备的姿态（手部抓握且手臂弯曲），统计每日累计低头看屏幕的时长。当连续低头时长超过设定阈值（如单次超过30分钟，或日累计超过2小时）时，输出'沉迷手机/游戏'提醒，建议家长干预并引导健康用眼习惯。该技能有助于预防青少年近视、颈椎问题及游戏成瘾。应用场景：家庭书房、青少年卧室、自习室、学校教室。系统实时监测，当沉迷行为超时时通过手机APP推送提醒或联动智能设备发出语音提示。技能特点：青少年长时间低头看手机，易导致近视、颈椎病、社交障碍等。通过AI自动监测并提醒，可帮助家长客观了解孩子用眼习惯，及时干预，保护视力健康。该技能可集成到智能家居摄像头或家庭教育APP中，成为家庭健康管理的实用工具。"
version: "1.0.0"
---

# Teen Phone / Game Screen Addiction Detection | 青少年沉迷手机/游戏行为识别

Using fixed cameras at home, study rooms or schools, the system analyzes adolescents' posture while using phones or gaming devices: head pitch angle (downward > 45°) and hand-holding-device posture (hand grasp + bent arm). It counts daily cumulative screen-looking time. When continuous screen-looking exceeds a configured threshold (e.g., single session > 30 minutes, or daily total > 2 hours), a 'phone/game addiction' reminder is generated, suggesting parental guidance and healthy eye-use habits. This helps prevent adolescent myopia, cervical-spine issues and gaming addiction. Application scenarios: family study, adolescent bedroom, study rooms, school classrooms. The system monitors in real time and pushes reminders via mobile APP or links to smart devices to issue voice prompts when over-time use is detected. Skill features: long head-down phone use among adolescents easily causes myopia, cervical-spine disease and social barriers. AI auto-monitoring and reminders help parents objectively understand their child's eye-use habits, enabling timely intervention and protecting vision. Can be integrated into smart-home cameras or family-education APPs as a practical family-health management tool.

通过家庭、自习室或学校固定摄像头，分析青少年使用手机或游戏设备的姿势，检测头部低垂角度（俯仰角大于45°）以及手持设备的姿态（手部抓握且手臂弯曲），统计每日累计低头看屏幕的时长。当连续低头时长超过设定阈值（如单次超过30分钟，或日累计超过2小时）时，输出'沉迷手机/游戏'提醒，建议家长干预并引导健康用眼习惯。该技能有助于预防青少年近视、颈椎问题及游戏成瘾。应用场景：家庭书房、青少年卧室、自习室、学校教室。系统实时监测，当沉迷行为超时时通过手机APP推送提醒或联动智能设备发出语音提示。技能特点：青少年长时间低头看手机，易导致近视、颈椎病、社交障碍等。通过AI自动监测并提醒，可帮助家长客观了解孩子用眼习惯，及时干预，保护视力健康。该技能可集成到智能家居摄像头或家庭教育APP中，成为家庭健康管理的实用工具。

## 🎯 AI 角色

**假设你是一个专业的青少年健康行为监测 AI。你的任务是分析固定摄像头的视频，检测青少年头部姿态（俯仰角）和手持设备姿势，判断是否正在低头看手机或玩游戏。统计单次连续低头时长和每日累计时长，当超过阈值时输出温和、尊重的提醒，并区分写作业 / 看书 / 网课等正常学习行为不计入沉迷时长。不要提供医疗诊断，仅输出基于视觉的行为统计。**

## 任务目标

- 本 Skill 用于：基于家庭/自习室/学校固定摄像头视频，识别头部俯仰角（> 45° 视为低头看屏幕）+ 手部抓握设备姿态（手机/平板/掌机）+ 手臂弯曲 → 区分 `looking_at_screen` / `normal_reading` / `writing` / `lifting_head` / `other` 姿态 → 统计单次连续低头时长 + 日累计时长 + 段次数 + 最长单段 + 夜间时长 → 输出 4 档沉迷等级（normal / mild / notable / heavy）+ 友好提醒 + 给家长的日报摘要
- 能力包含：人体关键点 + 头部姿态估计（pitch 角）、手部抓握检测、手臂弯曲姿态判定、设备边界框检测（参考）、姿态状态多分类（含 normal_reading / writing 排除项）、连续低头时长统计、日累计/段次数/最长单段/夜间时长统计、单次阈值（30 min / 60 min）与日累计阈值（2 h / 4 h）双触发、夜间熬夜玩屏幕提醒（22:00-06:00 ≥ 30 min）、温和友好提醒文本生成、家长日报摘要、温和动作建议（push_eye_break / push_parent_notice / suggest_outdoor_activity / suggest_bedtime / observe_only）
- 触发条件:
    1. **默认触发**：当用户提供家庭/自习室/学校固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行青少年沉迷手机/游戏行为识别
    2. 当用户明确提及孩子沉迷手机、孩子玩游戏太久、低头看屏幕、护眼提醒、青少年熬夜玩游戏、家长干预、用眼健康等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看孩子沉迷手机历史报告、青少年屏幕时长报告清单、家长日报清单、查询历史沉迷行为记录、显示所有屏幕沉迷分析报告、显示青少年用眼健康报告，查询沉迷行为预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有青少年屏幕沉迷报告"、"
       显示所有家长日报"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_teen_screen_addiction_detection_analysis --list --open-id` 参数调用 API
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

**在执行青少年沉迷手机/游戏行为识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备家庭/自习室/学校固定摄像头视频输入**
        - 提供本地视频路径或网络 URL，建议时长 ≥ 30 分钟以稳定统计单次连续低头
        - 摄像头建议：家庭书房 / 青少年卧室 / 自习室 / 学校教室固定摄像头，**侧面或斜侧上半身**视角（便于计算头部俯仰角与手臂姿态）
        - 帧率 ≥ 5 FPS（推荐 10 FPS）、分辨率 ≥ 480p、光照稳定（夜间偷玩场景需红外补光）
        - 多人场景需按目标跟踪，避免身份串扰
        - 隐私敏感场景必须启用人体轮廓 + 面部马赛克模式
        - 可选附带：青少年姓名 / 年龄、阈值覆盖（单次 / 日累计 / 夜间）、写作业时段白名单
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行青少年沉迷手机/游戏行为识别**
        - 调用 `-m scripts.smyx_teen_screen_addiction_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地家庭/自习室/学校固定摄像头视频文件路径
            - `--url`: 网络家庭/自习室/学校固定摄像头视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，青少年健康行为监测场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示青少年沉迷手机/游戏行为识别历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的青少年沉迷手机/游戏行为识别报告
        - 包含：时间窗（time_window）、画面中人数（subject_count）、当前姿态（current_posture：looking_at_screen / normal_reading / writing / lifting_head / other）、头部俯仰角（head_pitch_angle_deg）、手部抓握设备（hand_holding_device_detected）、当前连续低头时长（current_continuous_screen_min）、当日累计看屏幕总时长（daily_total_screen_min）、独立看屏幕段次数（session_count_today）、最长单段（longest_session_today_min）、夜间看屏幕时长（night_screen_minutes）、沉迷等级（addiction_level：normal / mild / notable / heavy）、设备类型猜测（dominant_device_guess：phone / tablet / handheld_console / unknown，仅用于提示文案）、提醒类型（alert_type：looking_too_long_session / looking_too_long_critical / addiction_warning / addiction_critical / late_night_warning / normal）、提醒级别（alert_level：info / notice / warning）、友好提醒（friendly_reminder，如"宝贝，你已经连续看屏幕 45 分钟了，眼睛该休息啦~ 起来走 3 分钟、看看 6 米外的窗外吧"）、家长日报摘要（parent_summary，如"今日累计看屏幕 2 小时 35 分（已超 2 小时阈值），最长单段 52 分钟，建议在饭后约定 30 分钟亲子户外散步"）、建议动作（recommend_action：push_eye_break / push_parent_notice / suggest_outdoor_activity / suggest_bedtime / observe_only）
        - **重要提示**：仅输出基于视觉的客观姿态与时长统计与温和家庭提醒，**不构成游戏成瘾的精神医学诊断**；任何疑似行为成瘾的判定与干预必须由专业心理医生评估制定

## 资源索引

- 必要脚本：见 [scripts/smyx_teen_screen_addiction_detection_analysis.py](scripts/smyx_teen_screen_addiction_detection_analysis.py)(
  用途：调用 API 进行青少年沉迷手机/游戏行为识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、姿态阈值/单次与日累计阈值/写作业排除项与红线约束和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：侧面/斜侧上半身视角，可观察头部俯仰角与手臂姿态
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **必须**正确区分写作业 / 看书 / 网课（前方有书本/课本、头部朝下但角度多在 30-45° 之间）与"低头看屏幕"，避免将正常学习行为误报为沉迷
- 短时低头取物、写字时短暂低头等情形不应计入连续低头段；建议连续 ≥ 5 分钟才计为 1 段
- 红线约束：**禁止**输出"游戏成瘾症"等精神医学诊断或量表评分；**禁止**长期存储青少年原始视频；**禁止**未经监护人同意将数据提供给学校或第三方；**禁止**使用强惩罚性语言
- 涉及未成年人，必须取得**监护人 + 青少年本人**双重知情同意；建议提前与孩子沟通用途与边界，避免成为家庭冲突导火索
- 友好提醒文案统一使用**温和、尊重、可执行**的措辞（如"眼睛该休息啦~ 起来走 3 分钟"），**避免**指责性表达
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"沉迷等级/累计时长/最长单段"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`青少年屏幕沉迷报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 沉迷等级/累计时长/最长单段 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 青少年屏幕沉迷报告-20260312172200001 | notable / 日累计 2h35m / 最长 52min | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地青少年使用屏幕视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_teen_screen_addiction_detection_analysis --input /path/to/study_room.mp4 --open-id your-open-id

# 分析网络青少年使用屏幕视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_teen_screen_addiction_detection_analysis --url https://example.com/study_room.mp4 --open-id your-open-id

# 显示历史青少年沉迷手机/游戏报告（自动触发关键词：查看孩子沉迷手机历史报告、家长日报清单等）
python -m scripts.smyx_teen_screen_addiction_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_teen_screen_addiction_detection_analysis --input sr.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_teen_screen_addiction_detection_analysis --input sr.mp4 --open-id your-open-id --output result.json
```
