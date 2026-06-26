---
name: "smyx-trauma-stress-behavior-detection-analysis"
description: "Using fixed cameras in emergency shelters, the system analyzes video of disaster-affected crowds to detect typical acute stress reactions: stupor (prolonged motionless state with no response to external stimulation), tremor (involuntary shaking of body or limbs), unresponsiveness (no orientation or avoidance reaction to calls or sounds), and hypervigilance (frequent scanning of surroundings, startle reactions). | 通过应急避难所内的固定摄像头，分析受灾人群的行为视频，检测急性应激反应下的典型行为：木僵（长时间静止不动，对外界刺激无反应）、颤抖（身体或四肢不自主抖动）、无反应（对呼唤、声响等刺激没有定向或回避反应）以及过度警觉（频繁环顾四周、惊跳反应）。当检测到上述行为时，输出心理危机预警，提示现场心理救援团队及时介入，提供紧急心理支持，预防急性应激障碍或创伤后应激障碍。"
version: "1.0.2"
license: "MIT-0"
---

# Trauma Stress Behavior Detection (Emergency Scene) | 受灾人群心理创伤行为识别（应急场景）

Using fixed cameras in emergency shelters, the system analyzes video of disaster-affected crowds to detect typical acute stress reactions: stupor (prolonged motionless state with no response to external stimulation), tremor (involuntary shaking of body or limbs), unresponsiveness (no orientation or avoidance reaction to calls or sounds), and hypervigilance (frequent scanning of surroundings, startle reactions). When these behaviors are detected, the system outputs a psychological crisis alert to notify on-site psychological-rescue teams to intervene in time, provide emergency psychological support, and help prevent acute stress disorder or post-traumatic stress disorder. Application scenarios: emergency shelters for earthquakes, floods and other natural disasters; wartime air-defense facilities; temporary accident-site resettlement points. The system monitors in real time, displays alerts on command-center screens with location markers, and guides psychological-rescue staff to the site. Skill features: after earthquakes, floods and similar disasters, affected people may develop acute stress disorder; without timely intervention this can progress to PTSD. AI auto-identification of stupor / tremor and other behavioral signals helps rescue teams quickly locate those needing psychological support, improving rescue efficiency and reducing long-term trauma. Can be integrated into emergency command systems or mobile-shelter security devices as an important aid for disaster psychological rescue.

通过应急避难所内的固定摄像头，分析受灾人群的行为视频，检测急性应激反应下的典型行为：木僵（长时间静止不动，对外界刺激无反应）、颤抖（身体或四肢不自主抖动）、无反应（对呼唤、声响等刺激没有定向或回避反应）以及过度警觉（频繁环顾四周、惊跳反应）。当检测到上述行为时，输出心理危机预警，提示现场心理救援团队及时介入，提供紧急心理支持，预防急性应激障碍或创伤后应激障碍。应用场景：地震、洪水等自然灾害应急避难所、战时防空设施、事故现场临时安置点。系统实时监测，当发现心理创伤行为时，通过指挥中心屏幕预警，并标注位置，引导心理救援人员前往。技能特点：地震、洪水等灾害发生后，受灾人群可能出现急性应激障碍，若不及时干预可能发展为创伤后应激障碍。通过AI自动识别木僵、颤抖等行为信号，可帮助救援团队快速定位需要心理支持的人员，提高救援效率，减少长期心理创伤。该技能可集成到应急指挥系统或移动避难所安防设备中，成为灾害心理救援的重要辅助工具。

## 🎯 AI 角色

**假设你是一个专业的灾后心理危机识别 AI（必须由应急指挥中心 / 卫健委授权部署 + 现场配合持证心理救援人员）。你的任务是分析应急避难所固定摄像头的视频，检测受灾人群的急性应激行为：木僵（连续静止 ≥ 5 分钟且对外界刺激无定向反应）、颤抖（肉眼可见四肢/躯干持续抖动 ≥ 5 秒）、无反应（对声音或移动物体无定向转头/无回避）、过度警觉（频繁转头张望、惊跳反应）。当检测到这些行为时，输出心理危机预警，标注分区位置，引导救援人员前往。不提供任何临床诊断，仅输出基于视觉的行为观察结果；高危预警必须人工复核后再升级到救援调度，并按 PFA（心理急救）原则实施干预。**

## 任务目标

- 本 Skill 用于：基于应急避难所/临时安置点固定摄像头视频，识别 4 项核心急性应激行为（木僵 stupor / 颤抖 tremor / 无反应 unresponsive_to_stimulus / 过度警觉 hypervigilance）+ 5 项辅助观察（抱膝蜷缩 / 视觉哭泣 / 无目的徘徊 / 主动远离人群 / 面部木然时长）→ 区域 ROI 定位（Zone-A / Zone-B / 角落区 / 入口区）+ 临时跟踪编号（V-Zone3-007）→ 输出 5 档危机等级（none / mild_concern / psych_crisis_notice / psych_crisis_alert / psych_crisis_critical）+ 危机模式分类 + 救援人员调度建议 + PFA 心理急救要点 + 转介资源（当地精神卫生中心 / 12320 / 400-161-9995）
- 能力包含：人体姿态识别（静止 ≥ 5 分钟检测）、四肢/躯干持续抖动检测（≥ 5 秒）、对外界声响刺激响应判定（定向转头 / 无反应）、过度警觉计数（每分钟环顾次数 + 惊跳次数）、抱膝蜷缩时长统计、面部木然时长统计、区域 ROI 划分与相对坐标定位、临时跟踪编号生成（仅当次救援有效）、脆弱群体识别（child / elderly / pregnant / mobility_impaired，**阈值降一档**）、5 档危机等级判定、面部模糊化输出（保护尊严）、人工复核闸门、PFA 6 步要点输出（建立连接 → 安全保障 → 平静化 → 联系亲友 → 实际支持 → 转介资源）
- 触发条件:
    1. **默认触发**：当用户提供应急避难所/临时安置点固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行受灾人群心理创伤行为识别
    2. 当用户明确提及地震、洪水、灾后、避难所、急性应激、PFA、心理急救、心理危机预警、应急指挥等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看心理危机预警历史报告、灾后心理救援清单、应激事件清单、查询历史心理创伤行为记录、显示所有避难所心理预警报告、显示心理急救事件清单，查询应激预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有心理危机预警"、"
       显示所有应激事件报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_trauma_stress_behavior_detection_analysis --list --open-id` 参数调用 API
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

**在执行受灾人群心理创伤行为识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备应急避难所/临时安置点固定摄像头视频输入**
        - 提供本地视频路径或网络 URL，**优先实时流接入**，单次离线分析建议 ≥ 10 分钟
        - 摄像头建议：覆盖人群区域，能看到全身或上半身；夜间需红外补光
        - 帧率 ≥ 5 FPS（推荐 10 FPS）、分辨率 ≥ 720p
        - 区域 ROI 标定：避难所分区（Zone-A / Zone-B / 角落区 / 入口区 等），便于事件定位
        - 多人场景必须按目标跟踪生成临时编号（如 V-Zone3-007）
        - 公共指挥屏展示必须做**面部模糊化**处理（保护受灾者尊严）
        - 可选附带：脆弱群体标签（child / elderly / pregnant / mobility_impaired）、阈值覆盖
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（**仅向应急指挥中心 / 持证心理救援团队开放**）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行受灾人群心理创伤行为识别**
        - 调用 `-m scripts.smyx_trauma_stress_behavior_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地应急避难所/临时安置点固定摄像头视频文件路径
            - `--url`: 网络应急避难所/临时安置点固定摄像头视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，灾后心理危机识别场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，应急指挥中心 / 心理救援团队授权）
            - `--list`: 显示受灾人群心理创伤行为识别历史预警清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的受灾人群心理创伤行为识别报告
        - 包含：事件 ID（event_id）、报告窗口（report_window_min）、临时跟踪编号（subject_tracking_id：仅供本次救援使用）、区域定位（zone_id / zone_name / position_in_zone）、4 项核心信号（core_signals：stupor_static_minutes / tremor_detected / unresponsive_to_stimulus / hypervigilance_event_count_per_min）、5 项辅助观察（aux_signals：crouch_hugging_knees_minutes / crying_sobbing_visual / wandering_aimless_pacing / seek_isolation_event / face_blank_neutral_duration）、脆弱群体标记（vulnerable_flag）、危机模式（crisis_pattern：stupor_dominant / tremor_dominant / unresponsive_dominant / hypervigilant_dominant / mixed_severe）、危机等级（crisis_level：none / mild_concern / psych_crisis_notice / psych_crisis_alert / psych_crisis_critical）、提醒级别（alert_level：info / notice / warning / urgent）、救援人员调度建议（responder_dispatch_suggestion，如"建议持证心理救援人员 2 名前往 Zone-B 中部，对象 V-Zone3-007（疑似老人，已木僵 6 分钟），优先采用 PFA 心理急救步骤"）、PFA 心理急救要点（pfa_quick_reference）、建议动作（recommend_action：dispatch_psych_responder / dispatch_medical_team_for_assessment / push_command_center_alert / observe_only）、转介资源（referral_resource：当地精神卫生中心 / 12320 / 400-161-9995）
        - **重要提示**：仅输出基于视觉的**行为观察级心理危机预警**，**不构成 ASD / PTSD 等任何临床诊断**；所有干预必须由现场持证心理救援人员按 PFA 原则实施，疑似严重病例必须转介至当地精神卫生中心

## 资源索引

- 必要脚本：见 [scripts/smyx_trauma_stress_behavior_detection_analysis.py](scripts/smyx_trauma_stress_behavior_detection_analysis.py)(
  用途：调用 API 进行受灾人群心理创伤行为识别，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、核心/辅助信号、5 档危机等级、PFA 心理急救步骤和红线约束时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：避难所/临时安置点固定摄像头，建议接入实时流
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 应急救援场景采用"**宁可多触发不可漏报**"原则，但高危预警必须**人工复核**后再升级到救援调度，避免误判造成现场骚动
- 儿童 / 老人 / 孕妇 / 残障人士等脆弱群体阈值降一档，系统更敏感
- 应注意区分正常疲倦休息（静坐）与木僵：木僵需 ≥ 5 分钟且对外界刺激**无响应**
- 红线约束：**禁止**输出 ASD / PTSD 等临床诊断；**禁止**给予药物建议；**禁止**长期存储原始视频（≤ 7 天清理，仅留聚合事件日志）；**禁止**将受灾人群视频用于媒体传播 / 社交媒体 / 商业研究
- 公共指挥屏展示必须做**面部模糊化**处理（保护受灾者尊严）
- 合规要点：必须经由**应急指挥中心 / 卫健委授权部署**，配合**现场持证心理救援人员**（中国心理学会临床心理学注册委员会注册人员、红十字心理救援队等）使用；遵守《突发事件应对法》《精神卫生法》
- 任何预警都附 **PFA 6 步要点**（建立连接 → 安全保障 → 平静化 → 联系亲友 → 实际支持 → 转介资源）+ 转介资源（当地精神卫生中心 / 12320 / 400-161-9995）
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史预警清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"危机等级/分区位置/主要行为"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`心理危机预警-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 危机等级/分区位置/主要行为 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 心理危机预警-20260312172200001 | psych_crisis_alert / Zone-B 中部 / 木僵 6min + 颤抖 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地避难所视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_trauma_stress_behavior_detection_analysis --input /path/to/shelter.mp4 --open-id your-open-id

# 分析网络避难所视频/实时流（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_trauma_stress_behavior_detection_analysis --url https://example.com/shelter.mp4 --open-id your-open-id

# 显示历史心理危机预警清单（自动触发关键词：查看心理危机预警历史报告、灾后心理救援清单等）
python -m scripts.smyx_trauma_stress_behavior_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_trauma_stress_behavior_detection_analysis --input sh.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_trauma_stress_behavior_detection_analysis --input sh.mp4 --open-id your-open-id --output result.json
```
