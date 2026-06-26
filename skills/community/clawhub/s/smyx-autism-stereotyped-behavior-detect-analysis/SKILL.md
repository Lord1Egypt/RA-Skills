---
name: "smyx-autism-stereotyped-behavior-detect-analysis"
description: "Using a fixed camera in rehabilitation centers or homes, the system analyzes children's behavior videos with pose estimation and temporal action detection to recognize repetitive stereotyped behaviors, including spinning (body rotation ≥ 360°), hand flapping (non-functional repetitive arm movement), body rocking (rhythmic forward-backward or side-to-side trunk motion), etc. | 通过康复机构或家庭固定摄像头，分析儿童行为视频，利用姿态估计和时序动作检测技术识别重复性刻板动作，包括转圈（身体旋转360°以上）、摆手（手臂非功能性重复摆动）、摇晃（躯干前后或左右有节律摆动）等。该技能可辅助康复师和家长客观记录行为变化，评估干预效果。"
version: "1.0.1"
license: "MIT-0"
---

# Autism Stereotyped Behavior Detection (Spinning / Hand-Flapping) | 自闭症儿童刻板行为识别（转圈/摆手）

Using a fixed camera in rehabilitation centers or homes, the system analyzes children's behavior videos with pose estimation and temporal action detection to recognize repetitive stereotyped behaviors, including spinning (body rotation ≥ 360°), hand flapping (non-functional repetitive arm movement), body rocking (rhythmic forward-backward or side-to-side trunk motion), etc. It counts the frequency (events per hour) and duration of each behavior and generates a behavior report. The skill helps therapists and parents objectively record behavior changes and evaluate intervention effects. Application scenarios: autism rehabilitation institutions, special-education schools, home interventions. Real-time monitoring; the system automatically generates daily / weekly stereotyped-behavior statistics to support rehabilitation planning. Skill features: stereotyped behaviors are a core symptom of autism, and changes in frequency / duration are important indicators of intervention effectiveness. Automatic AI recording reduces therapists' workload, enables long-term continuous monitoring, and provides data support for individualized intervention. Can be integrated into rehabilitation-center management systems or home-rehabilitation apps.

通过康复机构或家庭固定摄像头，分析儿童行为视频，利用姿态估计和时序动作检测技术识别重复性刻板动作，包括转圈（身体旋转360°以上）、摆手（手臂非功能性重复摆动）、摇晃（躯干前后或左右有节律摆动）等。统计每种刻板行为的频次（次/小时）和单次持续时间，生成行为报告。该技能可辅助康复师和家长客观记录行为变化，评估干预效果。应用场景：自闭症康复机构、特殊教育学校、家庭干预。系统实时监测，自动生成每日/每周刻板行为统计报告，为康复计划提供数据支持。技能特点：刻板行为是自闭症的核心症状之一，其频率和持续时间变化是评估干预效果的重要依据。通过AI自动监测记录，可减轻康复师负担，实现长时间连续监测，为个性化干预提供数据支持。该技能可集成到康复机构管理系统或家庭康复APP中。

## 🎯 AI 角色

**假设你是一个专业的自闭症儿童行为分析 AI。你的任务是分析固定摄像头拍摄的儿童行为视频，检测重复性刻板动作，包括转圈、摆手、摇晃等。统计每种行为的频次和持续时间，输出行为报告。不要提供自闭症诊断、量表打分或康复处方，仅输出基于视觉的客观行为统计，供专业康复师和家长参考。**

## 任务目标

- 本 Skill 用于：基于康复机构/家庭固定摄像头视频，识别儿童多类重复性刻板行为 → 按事件级别记录起止时间/持续秒数/置信度 → 汇总各类频次（次/小时）+ 累计时长 + 主导类别 → 可结合历史基线生成趋势报告
- 能力包含：人体检测与跟踪、2D/3D 姿态关键点估计、时序动作分类（spinning / hand_flapping / body_rocking / head_banging / finger_flicking / toe_walking / repetitive_running / repetitive_object_play 等）、事件级起止时间检测与去重、每小时/每日频次与累计时长统计、主导刻板行为类别识别、与个人 7-14 天基线对比（趋势变化百分比）、康复师/家长行为摘要文本生成
- 触发条件:
    1. **默认触发**：当用户提供康复/家庭儿童行为视频 URL 或文件需要分析时，默认触发本技能进行刻板行为识别
    2. 当用户明确提及自闭症、谱系障碍、刻板行为、转圈、摆手、摇晃、撞头、踮脚走、康复评估、特殊教育、ABA 干预效果等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看刻板行为历史报告、自闭症儿童行为报告清单、刻板行为统计报告清单、查询历史康复评估记录、显示所有刻板行为分析报告、显示特殊教育诊断报告，查询刻板行为趋势预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有刻板行为报告"、"
       显示所有自闭症儿童行为报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_autism_stereotyped_behavior_detect_analysis --list --open-id` 参数调用 API
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

**在执行自闭症儿童刻板行为识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备康复/家庭儿童行为视频输入**
        - 提供本地视频路径或网络 URL，建议时长 ≥ 5 分钟
        - 摄像头建议：康复机构/特殊教育学校/家庭固定摄像头，覆盖儿童主要活动区域，**能看到全身**
        - 帧率 ≥ 10 FPS（推荐 15-30 FPS）、分辨率 ≥ 480p、光照稳定
        - 多儿童场景下建议结合外观特征锁定主目标；隐私敏感场景可启用人体骨架模式
        - 可选附带：儿童年龄、康复阶段、当前干预方案（如 ABA / DTT / 结构化教学）、关注的目标行为类别清单
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行自闭症儿童刻板行为识别**
        - 调用 `-m scripts.smyx_autism_stereotyped_behavior_detect_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地康复/家庭儿童行为视频文件路径
            - `--url`: 网络康复/家庭儿童行为视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，自闭症儿童行为分析场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示自闭症儿童刻板行为识别历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的自闭症儿童刻板行为识别报告
        - 包含：是否检测到儿童（subject_detected）、关键点是否充分可见（pose_keypoints_visible）、完整行为事件序列（behavior_events：含 behavior_class / start_time / end_time / duration_sec / confidence）、汇总指标（summary_metrics：per_class_count_hourly / per_class_total_duration_today_sec / total_stereotyped_duration_today_sec / dominant_behavior_class）、相对基线变化（trend_vs_baseline：per_class_delta_pct）、康复师/家长方向性参考（intervention_hint，**descriptive_only，不构成处方**）、文本摘要（如"今日转圈 14 次，摆手 23 次，相比基线下降 30%，建议康复师评估当前干预方案"）
        - **重要提示**：仅输出基于视觉的客观行为统计，**不提供自闭症诊断、ADOS / ADI-R 等量表打分、康复处方**；任何诊断与干预方案必须由专业医生 / 认证康复治疗师评估制定

## 资源索引

- 必要脚本：见 [scripts/smyx_autism_stereotyped_behavior_detect_analysis.py](scripts/smyx_autism_stereotyped_behavior_detect_analysis.py)(
  用途：调用 API 进行自闭症儿童刻板行为识别（转圈/摆手），本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、刻板行为类别表与阈值定义和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：必须能看到儿童全身，帧率 ≥ 10 FPS
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 部分日常动作（鼓掌、跳舞、追逐游戏等）可能被误识别为刻板行为，建议康复师/家长进行抽样复核
- 多儿童在同一视野内、家庭成员同时出现等情形可能影响识别准确性
- 本工具**不提供自闭症诊断**，也**不替代** ADOS-2 / ADI-R / CARS 等专业评估；任何康复方案应在认证的康复治疗师指导下进行
- 隐私合规：自闭症儿童行为视频涉及未成年人高度敏感隐私，使用前需取得监护人明确知情同意，妥善加密保管；建议优先采用人体骨架/轮廓模式
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"主导行为/频次"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`自闭症儿童刻板行为识别报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 主导行为/频次 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 自闭症儿童刻板行为识别报告-20260312172200001 | hand_flapping 23 次 / 较基线 ↓30% | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地康复/家庭儿童行为视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_autism_stereotyped_behavior_detect_analysis --input /path/to/rehab.mp4 --open-id your-open-id

# 分析网络康复/家庭儿童行为视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_autism_stereotyped_behavior_detect_analysis --url https://example.com/rehab.mp4 --open-id your-open-id

# 显示历史自闭症儿童刻板行为识别报告（自动触发关键词：查看刻板行为历史报告、自闭症儿童行为报告清单等）
python -m scripts.smyx_autism_stereotyped_behavior_detect_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_autism_stereotyped_behavior_detect_analysis --input rehab.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_autism_stereotyped_behavior_detect_analysis --input rehab.mp4 --open-id your-open-id --output result.json
```
