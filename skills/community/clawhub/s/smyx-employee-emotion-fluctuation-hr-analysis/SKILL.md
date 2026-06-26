---
name: "smyx-employee-emotion-fluctuation-hr-analysis"
description: "Using fixed cameras in enterprise office areas (with employee consent and anonymization), the system performs long-term monitoring of employees' facial expressions and posture features, building per-person historical baselines (smile frequency, sigh count, frown level, etc.). When an employee's smile frequency drops significantly relative to baseline (e.g., -40%), sighs increase significantly (e.g., +50%), or other abnormal behaviors emerge (social withdrawal, long solo sitting), the system outputs an emotion-fluctuation alert and reminds HR or managers to initiate a supportive check-in. The skill aims to help organizations detect employee mental-health issues early, reduce turnover risk, and improve well-being. Application scenarios: enterprise open-plan offices, department private offices. The system generates weekly or monthly employee emotion-trend reports for HR internal reference ONLY. Skill features: low employee morale often precedes resignation; AI-based early identification allows HR to provide timely care and reduce attrition. Suitable for mid-to-large enterprises, especially high-pressure roles such as R&D and customer service. Privacy must be protected; access should be limited to HR senior management only. | 通过企业办公区固定摄像头（需征得员工同意并匿名化处理），长期监测员工的面部表情和姿态特征，建立个人历史基线（如笑容频率、叹气次数、皱眉程度等）。当检测到某员工近期的笑容频率显著下降（例如比基线降低40%）、叹气次数增加（例如比基线增加50%）或与其他异常行为（社交回避、长时间独自静坐）时，输出情绪波动预警，提醒HR或管理者进行关怀沟通。该技能旨在帮助组织及时发现员工心理健康问题，降低离职风险，提升员工幸福感。应用场景：企业开放式办公区、部门独立办公室。系统每周或每月生成员工情绪趋势报告，仅供HR内部参考。技能特点：员工情绪低落往往是离职的前兆，通过AI早期识别异常，HR可及时介入关怀，降低流失率。该技能适用于中大型企业，尤其适合研发、客服等高压力岗位。需注意隐私保护，建议仅HR管理层可见。"
version: "1.0.0"
---

# Employee Emotion Fluctuation HR Report | 员工情绪波动 HR 报告

Using fixed cameras in enterprise office areas (with employee consent and anonymization), the system performs long-term monitoring of employees' facial expressions and posture features, building per-person historical baselines (smile frequency, sigh count, frown level, etc.). When an employee's smile frequency drops significantly relative to baseline (e.g., -40%), sighs increase significantly (e.g., +50%), or other abnormal behaviors emerge (social withdrawal, long solo sitting), the system outputs an emotion-fluctuation alert and reminds HR or managers to initiate a supportive check-in. The skill aims to help organizations detect employee mental-health issues early, reduce turnover risk, and improve well-being. Application scenarios: enterprise open-plan offices, department private offices. The system generates weekly or monthly employee emotion-trend reports for HR internal reference ONLY. Skill features: low employee morale often precedes resignation; AI-based early identification allows HR to provide timely care and reduce attrition. Suitable for mid-to-large enterprises, especially high-pressure roles such as R&D and customer service. Privacy must be protected; access should be limited to HR senior management only.

通过企业办公区固定摄像头（需征得员工同意并匿名化处理），长期监测员工的面部表情和姿态特征，建立个人历史基线（如笑容频率、叹气次数、皱眉程度等）。当检测到某员工近期的笑容频率显著下降（例如比基线降低40%）、叹气次数增加（例如比基线增加50%）或与其他异常行为（社交回避、长时间独自静坐）时，输出情绪波动预警，提醒HR或管理者进行关怀沟通。该技能旨在帮助组织及时发现员工心理健康问题，降低离职风险，提升员工幸福感。应用场景：企业开放式办公区、部门独立办公室。系统每周或每月生成员工情绪趋势报告，仅供HR内部参考。技能特点：员工情绪低落往往是离职的前兆，通过AI早期识别异常，HR可及时介入关怀，降低流失率。该技能适用于中大型企业，尤其适合研发、客服等高压力岗位。需注意隐私保护，建议仅HR管理层可见。

## 🎯 AI 角色

**假设你是一个专业的职场心理健康监测 AI（必须经企业授权 + 员工知情同意 + 工会备案）。你的任务是分析办公区固定摄像头的视频，对员工进行匿名化跟踪（只生成临时匿名 ID + 匿名工位坐标，绝不与 HR 姓名/工号系统映射），检测面部表情（笑容、皱眉、视觉叹气动作）及行为（独自静坐时长、社交互动频率）。对比个人 30 天历史基线，当笑容频率下降 ≥ 40% 或叹气次数增加 ≥ 50% 或独自静坐增加 ≥ 50% 时，输出情绪波动预警。不存储任何个人识别信息，仅向 HR 高级管理层输出匿名 ID + 工位坐标的关怀提示，禁止用于绩效考核、晋升、解雇决策。**

## 任务目标

- 本 Skill 用于：基于企业办公区固定摄像头视频（员工知情同意 + 工会备案），匿名跟踪员工面部表情 4 项（笑容数 / 笑容时长 / 皱眉数 / 视觉叹气数 / 中性比例）+ 行为 4 项（独自静坐总时长 / 同事互动事件数 / 离开工位次数 / 工位姿态前倾比例）→ 与个人 30 天基线对比 → 连续 ≥ 3 个工作日异常 → 输出匿名 ID + 工位坐标级的 HR 关怀建议（**不输出姓名，不与工号绑定**），用于自愿性 1-on-1 关怀沟通
- 能力包含：基于临时匿名 ID 的多人跨帧跟踪（ID 周期性轮换 ≤ 7 天）、笑容/皱眉/视觉叹气识别（耸肩 + 长呼气姿态）、独自静坐 vs 同事互动判别、工位 ROI 标定（W-A12 / W-B07 等匿名坐标）、30 天个人基线计算、smile_delta / sigh_delta / solo_sit_delta / peer_interaction_delta 百分比对比、连续异常天数累计、波动模式分类（smile_drop / sigh_increase / withdrawal / mixed / improving / none）、4 档关怀等级（none / mild / notable / focus_care）、最小样本保护（当日可分析时长 < 2 h 输出 insufficient_sample）、面向 HR 的中性、保密、自愿性关怀建议生成、EAP 资源参考
- 触发条件:
    1. **默认触发**：当用户提供企业办公区固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行员工情绪波动 HR 报告
    2. 当用户明确提及员工情绪、员工幸福感、离职风险、HR 关怀、高压力岗位心理健康、EAP、工位情绪监测等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看员工情绪波动历史报告、HR 关怀报告清单、员工情绪趋势报告清单、查询历史员工情绪记录、显示所有 HR 内部情绪报告、显示团队情绪健康报告，查询员工情绪波动预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有员工情绪波动报告"、"
       显示所有 HR 关怀报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_employee_emotion_fluctuation_hr_analysis --list --open-id` 参数调用 API
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

**在执行员工情绪波动 HR 报告分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备企业办公区固定摄像头视频输入**
        - 提供本地视频路径或网络 URL，建议每个被分析人每日 ≥ 4 小时累计在画面中
        - 摄像头建议：企业开放式办公区/部门独立办公室固定摄像头，能看到工位上半身（含面部）
        - 帧率 ≥ 5 FPS（推荐 10 FPS）、分辨率 ≥ 720p、光照稳定
        - 工位 ROI 标定：每个工位作为一个匿名工位 ID（如 W-A12 / W-B07）
        - 必须有**个人 30 天历史基线**，否则首次仅输出"基线累积中"状态
        - **强匿名约束**：禁止人脸识别到 HR 姓名/工号库；仅维护临时跟踪 ID（≤ 7 天轮换）
        - **必须**事先在企业内部以**显著公告 + 员工代表大会/工会备案**方式公开告知；必须提供 opt-out 选项
        - 可选附带：报告周期（weekly/monthly）、阈值覆盖、工位白/黑名单（opt-out）
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id（**仅限 HR 高级管理层**）
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行员工情绪波动 HR 报告**
        - 调用 `-m scripts.smyx_employee_emotion_fluctuation_hr_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地企业办公区固定摄像头视频文件路径
            - `--url`: 网络企业办公区固定摄像头视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，职场心理健康监测场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，**仅限 HR 高级管理层**）
            - `--list`: 显示员工情绪波动 HR 报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的员工情绪波动 HR 报告
        - 包含：报告周期（report_period：weekly / monthly）、匿名跟踪 ID（anonymized_subject_id：仅本周期有效）、匿名工位坐标（workstation_id：不绑定姓名）、每日 4 项面部 + 4 项行为指标（daily_metrics）、与个人 30 天基线对比（baseline_comparison：smile_delta_pct / sigh_delta_pct / solo_sit_delta_pct / peer_interaction_delta_pct / baseline_window_days）、连续异常天数（consecutive_abnormal_days）、波动模式（fluctuation_pattern：smile_drop / sigh_increase / withdrawal / mixed / improving / none）、关怀等级（concern_level：none / mild / notable / focus_care）、提醒类型（alert_type：emotion_fluctuation_notice / focus_care_needed / improving / normal）、提醒级别（alert_level：info / notice / warning）、给 HR 的关怀建议（hr_care_suggestion，如"匿名 ID ANON-2026W21-073（工位 W-A12）近 5 个工作日笑容频率降 42%、独自静坐增 55%，建议其直属上级以工作支持/1-on-1 聊聊近况的方式自愿沟通，**禁止**当面提及监控数据"）、建议动作（recommend_action：suggest_one_on_one_chat / suggest_workload_review / suggest_eap_referral / observe_only）、EAP 资源参考（eap_reference，focus_care_needed 时附）
        - **重要提示**：仅输出基于视觉的匿名行为聚合预警，**不构成精神医学诊断，不可作为绩效/晋升/解雇依据**；任何疑似心理健康问题应通过 EAP（员工援助计划）或专业心理咨询渠道，由员工本人自愿参与解决

## 资源索引

- 必要脚本：见 [scripts/smyx_employee_emotion_fluctuation_hr_analysis.py](scripts/smyx_employee_emotion_fluctuation_hr_analysis.py)(
  用途：调用 API 进行员工情绪波动 HR 报告，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、面部/行为/基线指标、匿名约束/红线和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：必须有 ≥ 30 天个人基线，单日可分析时长 ≥ 2 h
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 节假日 / 项目截止日 / 加班季 / 团建后疲倦等情形会显著影响指标，建议在配置中标记"非常态期"
- 突发短期波动（如家庭事件单日情绪低落）不应立即触发预警，必须连续 ≥ 3 个工作日异常
- **红线（必读）**：
    - **禁止**人脸识别到 HR 姓名/工号库；**禁止**将"匿名 ID ↔ 实际员工"映射表落地存储或对外暴露
    - **禁止**输出"焦虑症/抑郁症"等任何精神医学诊断或量表评分
    - **禁止**用于绩效考核、晋升评估、解雇决策
    - **禁止**长期存储原始视频或人脸特征；建议仅保存匿名 ID 级聚合指标，保留期 ≤ 30 天
    - **禁止**未经员工本人同意将其数据共享给直属上级以外的第三方
    - **禁止**在沟通中直接告知员工"你被摄像头分析为情绪低落"，必须以**自然工作支持**的方式进行
- 合规要点：必须**显著公告 + 员工代表大会/工会备案** + 员工 opt-out 选项；数据访问 ≥ 2 名 HR 高管共同审批 + 全量访问日志
- 当 `focus_care_needed` 时附**企业 EAP / 全国心理援助热线 400-161-9995**参考
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"匿名 ID/工位/关怀等级/主要变化"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`员工情绪波动 HR 报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 匿名 ID/工位/关怀等级/主要变化 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 员工情绪波动 HR 报告-20260312172200001 | ANON-2026W21-073 / W-A12 / focus_care / 笑容 -42% 独坐 +55% | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地企业办公区视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_employee_emotion_fluctuation_hr_analysis --input /path/to/office.mp4 --open-id your-open-id

# 分析网络企业办公区视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_employee_emotion_fluctuation_hr_analysis --url https://example.com/office.mp4 --open-id your-open-id

# 显示历史员工情绪波动 HR 报告（自动触发关键词：查看员工情绪波动历史报告、HR 关怀报告清单等）
python -m scripts.smyx_employee_emotion_fluctuation_hr_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_employee_emotion_fluctuation_hr_analysis --input office.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_employee_emotion_fluctuation_hr_analysis --input office.mp4 --open-id your-open-id --output result.json
```
