---
name: "smyx-anxiety-behavior-recognition-analysis"
description: "Using a fixed camera at home or in the office, the system analyzes daily videos of an individual (e.g., adult, adolescent) and detects anxiety-related behaviors: hand rubbing (repeated rubbing of both hands), nail biting (hand approaching mouth with biting motion), and pacing (repeated back-and-forth walking in a small area). It counts each behavior's frequency (events/hour) and total duration, and outputs an anxiety-behavior index (0-100). The skill helps users self-monitor anxiety states or assists counselors in evaluating intervention effectiveness. Application scenarios: home, office, counseling room, school. Real-time monitoring; when the anxiety-behavior index exceeds a threshold, a reminder is pushed (e.g., 'You showed more anxiety-related behaviors today — try a relaxation exercise'). Skill features: anxiety patients often display unconscious repetitive behaviors (hand-rubbing, nail-biting, pacing), which can serve as objective emotional indicators. AI auto-recording of frequency and trends helps users self-manage anxiety or provides data support for counselors. Can be integrated into smart-home cameras or mental-health APPs as a practical emotion-management tool. | 通过家庭或办公室的固定摄像头，分析个体（如成人、青少年）的日常行为视频，检测手部搓揉（双手反复摩擦）、指甲啃咬（手部靠近嘴部并有啃咬动作）、来回踱步（在狭小区域内反复折返行走）等焦虑相关行为。统计每种行为的频次（次/小时）和总持续时间，并输出焦虑行为指数（0-100）。该技能有助于用户自我觉察焦虑状态，或辅助心理咨询师评估干预效果。应用场景：家庭、办公室、心理咨询室、学校。系统实时监测，当焦虑行为指数超过阈值时推送提醒（如'您今日焦虑行为较多，建议进行放松练习'）。技能特点：焦虑症患者常有无意识的重复行为（搓手、咬指甲、踱步），这些行为可作为情绪状态的客观指标。通过AI自动记录频次和趋势，可帮助用户自我管理焦虑，或为心理咨询师提供数据支持。该技能可集成到智能家居摄像头或心理健康APP中，成为情绪健康管理的实用功能。"
version: "1.0.0"
---

# Anxiety-Related Behavior Recognition (Hand-rubbing / Nail-biting / Pacing) | 焦虑症相关行为（搓手、咬指甲、来回踱步）识别

Using a fixed camera at home or in the office, the system analyzes daily videos of an individual (e.g., adult, adolescent) and detects anxiety-related behaviors: hand rubbing (repeated rubbing of both hands), nail biting (hand approaching mouth with biting motion), and pacing (repeated back-and-forth walking in a small area). It counts each behavior's frequency (events/hour) and total duration, and outputs an anxiety-behavior index (0-100). The skill helps users self-monitor anxiety states or assists counselors in evaluating intervention effectiveness. Application scenarios: home, office, counseling room, school. Real-time monitoring; when the anxiety-behavior index exceeds a threshold, a reminder is pushed (e.g., 'You showed more anxiety-related behaviors today — try a relaxation exercise'). Skill features: anxiety patients often display unconscious repetitive behaviors (hand-rubbing, nail-biting, pacing), which can serve as objective emotional indicators. AI auto-recording of frequency and trends helps users self-manage anxiety or provides data support for counselors. Can be integrated into smart-home cameras or mental-health APPs as a practical emotion-management tool.

通过家庭或办公室的固定摄像头，分析个体（如成人、青少年）的日常行为视频，检测手部搓揉（双手反复摩擦）、指甲啃咬（手部靠近嘴部并有啃咬动作）、来回踱步（在狭小区域内反复折返行走）等焦虑相关行为。统计每种行为的频次（次/小时）和总持续时间，并输出焦虑行为指数（0-100）。该技能有助于用户自我觉察焦虑状态，或辅助心理咨询师评估干预效果。应用场景：家庭、办公室、心理咨询室、学校。系统实时监测，当焦虑行为指数超过阈值时推送提醒（如'您今日焦虑行为较多，建议进行放松练习'）。技能特点：焦虑症患者常有无意识的重复行为（搓手、咬指甲、踱步），这些行为可作为情绪状态的客观指标。通过AI自动记录频次和趋势，可帮助用户自我管理焦虑，或为心理咨询师提供数据支持。该技能可集成到智能家居摄像头或心理健康APP中，成为情绪健康管理的实用功能。

## 🎯 AI 角色

**假设你是一个专业的心理健康行为分析 AI。你的任务是分析固定摄像头的视频，检测特定焦虑相关行为：手部搓揉、指甲啃咬、来回踱步（路径重复）。统计这些行为的频次和持续时间，综合计算焦虑行为指数。不要提供医疗诊断，仅输出基于视觉的行为统计和趋势指标，并给出温和的自我关怀建议。**

## 任务目标

- 本 Skill 用于：基于家庭/办公室固定摄像头视频，识别焦虑相关重复行为（hand_rubbing / nail_biting / pacing）→ 输出每类行为频次/总持续时间 + 焦虑行为指数（0-100）+ 与个人基线对比 + 自我觉察提醒
- 能力包含：人体检测与手部关键点估计、双手反复摩擦事件识别、手部接近嘴部 + 啃咬动作识别（nail_biting）、行人轨迹分析与"狭小区域内反复折返"踱步识别（pacing_loop_count）、行为事件时间线生成（用于趋势可视化）、个人 7-14 天基线对比、综合焦虑行为指数计算、4 档焦虑表现等级（calm / mild / notable / high）、主导行为识别（dominant_behavior）、温和自我关怀建议生成（放松练习 / 深呼吸 / 户外散步）、心理援助热线参考
- 触发条件:
    1. **默认触发**：当用户提供家庭/办公室固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行焦虑症相关行为识别
    2. 当用户明确提及焦虑、搓手、咬指甲、来回踱步、紧张、坐立不安、放松练习、心理咨询数据、自我觉察等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看焦虑行为历史报告、焦虑行为指数报告清单、搓手/咬指甲/踱步记录清单、查询历史焦虑行为记录、显示所有焦虑行为分析报告、显示情绪健康趋势报告，查询焦虑行为预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有焦虑行为报告"、"
       显示所有焦虑行为指数报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_anxiety_behavior_recognition_analysis --list --open-id` 参数调用 API
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

**在执行焦虑症相关行为识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备家庭/办公室固定摄像头视频输入**
        - 提供本地视频路径或网络 URL，建议时长 ≥ 5 分钟
        - 摄像头建议：家庭书房/客厅/办公室/心理咨询室/学校教室固定摄像头，**能看到上半身（含手部）+ 完整下肢踱步路径**
        - 帧率 ≥ 15 FPS（推荐 20-30 FPS）、分辨率 ≥ 720p、光照稳定
        - 踱步识别需保证摄像头能看到 ≥ 2-3 米的可行走区域
        - 多人场景需按目标跟踪；隐私敏感场景必须启用人体轮廓 + 面部马赛克模式
        - 可选附带：被分析人姓名、年龄、近期事件（如考试季/项目截止）、阈值覆盖、个人基线开关
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行焦虑症相关行为识别**
        - 调用 `-m scripts.smyx_anxiety_behavior_recognition_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地家庭/办公室固定摄像头视频文件路径
            - `--url`: 网络家庭/办公室固定摄像头视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，心理健康行为分析场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示焦虑症相关行为识别历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的焦虑症相关行为识别报告
        - 包含：画面中人数（subject_count）、统计时间窗（analysis_window_min）、手部行为统计（hand_metrics：hand_rubbing_event_count / hand_rubbing_total_duration_sec / nail_biting_event_count / nail_biting_total_duration_sec）、踱步行为统计（pacing_metrics：pacing_event_count / pacing_total_duration_sec / pacing_loop_count）、行为事件时间线（behavior_event_timeline，用于趋势可视化）、焦虑行为指数（anxiety_behavior_index：0-100）、与个人基线对比（baseline_comparison：baseline_window_days / delta_vs_baseline_pct）、焦虑表现等级（anxiety_level：calm / mild / notable / high）、当前最突出的焦虑行为（dominant_behavior：hand_rubbing / nail_biting / pacing / mixed）、提醒类型（alert_type：anxiety_notable / anxiety_high / improving / normal）、提醒级别（alert_level：info / notice / warning）、自我关怀建议（self_care_suggestion，如"您今日焦虑行为较多，建议进行 5 分钟深呼吸或正念练习"）、建议动作（recommend_action：push_relaxation_reminder / suggest_breathing_exercise / suggest_walk_outdoors / suggest_seek_professional_help / observe_only）、心理援助热线参考（helpline_reference，high 等级时附）
        - **重要提示**：仅输出基于视觉的客观行为统计与自我觉察提醒，**不构成焦虑症诊断、GAD-7 / SAS / HAMA 等量表评分或治疗方案**；任何焦虑症确诊与治疗必须由精神科医生 / 心理治疗师评估制定；若伴有持续胸闷、心悸、惊恐发作等躯体化症状，请及时就医或拨打**全国心理援助热线 400-161-9995**

## 资源索引

- 必要脚本：见 [scripts/smyx_anxiety_behavior_recognition_analysis.py](scripts/smyx_anxiety_behavior_recognition_analysis.py)(
  用途：调用 API 进行焦虑症相关行为识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、3 类焦虑行为定义/焦虑行为指数阈值/红线约束和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：能看到上半身（含手部）+ 完整下肢踱步路径
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 工作搓手取暖、吃零食时手部靠近嘴部、来回走动取物等情形易被误识为焦虑行为，建议结合短时序均值与上下文判定
- 一次性短暂行为（如紧张前的搓手 30 秒）不应触发高焦虑报警；建议结合多个时间窗均值
- 红线约束：**禁止**输出焦虑症诊断、量表评分（GAD-7 / SAS / HAMA）、用药建议或处方；**禁止**将"焦虑行为指数高"等同于"确诊焦虑症"；**禁止**长期存储原始视频；**禁止**未经本人同意向第三方推送其个人焦虑数据
- 当出现 `high` 等级或伴随躯体化症状（胸闷 / 心悸 / 惊恐发作）时，**必须**在提醒中附**心理援助热线 400-161-9995**并建议本人尽快就医
- 隐私合规：使用前需取得本人明确知情同意，妥善加密保管；建议优先采用人体轮廓 + 面部马赛克模式 + 仅保存指标统计
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"焦虑指数/主导行为"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`焦虑相关行为识别报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 焦虑指数/主导行为 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 焦虑相关行为识别报告-20260312172200001 | 62 (notable) / dominant=hand_rubbing | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地家庭/办公室视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_anxiety_behavior_recognition_analysis --input /path/to/office.mp4 --open-id your-open-id

# 分析网络家庭/办公室视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_anxiety_behavior_recognition_analysis --url https://example.com/office.mp4 --open-id your-open-id

# 显示历史焦虑症相关行为识别报告（自动触发关键词：查看焦虑行为历史报告、焦虑行为指数报告清单等）
python -m scripts.smyx_anxiety_behavior_recognition_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_anxiety_behavior_recognition_analysis --input office.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_anxiety_behavior_recognition_analysis --input office.mp4 --open-id your-open-id --output result.json
```
