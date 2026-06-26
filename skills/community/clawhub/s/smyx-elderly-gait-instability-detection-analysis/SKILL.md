---
name: "smyx-elderly-gait-instability-detection-analysis"
description: "Using a fixed camera in a hallway or living room to record video of an elderly person walking in a straight line, AI pose estimation and gait analysis extract parameters such as step length (cm), gait speed (m/s), trunk sway angle (left-right tilt), and cadence to evaluate gait stability. When step length is too small (small-shuffling steps), gait speed is too slow, or trunk sway is too large, the system outputs a fall risk level (low / medium / high). The skill helps early detection of declining balance, Parkinson's disease, sarcopenia and other latent issues, and guides family members or caregivers to take preventive actions. Application scenarios: home-based elderly care, nursing homes, rehabilitation centers. The system can be scheduled (e.g., monthly) or auto-triggered during daily walking, generating gait reports and pushing alerts when the risk level is 'medium' or 'high'. Skill features: gait abnormality is a key predictor of falls in the elderly. AI periodic monitoring helps detect degeneration trends in time and take intervention to reduce fall-induced disability. Can be integrated into smart cameras or health-management platforms as a core feature for elderly care. | 通过走廊或客厅的固定摄像头拍摄老年人直线行走的视频，利用AI姿态估计和步态分析技术检测步幅长度（cm）、步速（m/s）、躯干摇摆角度（左右倾斜度）以及步频等参数，评估步态稳定性。当步幅过小（小碎步）、步速过慢、躯干摇摆幅度过大时，输出跌倒风险等级（低/中/高）。该技能有助于早期发现老年人平衡能力下降、帕金森病、肌少症等潜在问题，指导家属或护理人员采取预防措施。应用场景：居家养老、养老院、康复中心。系统定期（如每月）或在老年人日常行走时自动触发检测，生成步态报告，当风险等级为'中'或'高'时推送提醒。技能特点：步态异常是老年人跌倒的重要预测因子。通过AI定期监测，可及早发现退化趋势，采取干预措施，降低跌倒致残率。该技能可集成到智能摄像头或健康管理平台中，成为养老监护的核心功能。"
version: "1.0.0"
---

# Elderly Gait Instability / Shuffling Step Detection | 老年人步态不稳/小碎步识别

Using a fixed camera in a hallway or living room to record video of an elderly person walking in a straight line, AI pose estimation and gait analysis extract parameters such as step length (cm), gait speed (m/s), trunk sway angle (left-right tilt), and cadence to evaluate gait stability. When step length is too small (small-shuffling steps), gait speed is too slow, or trunk sway is too large, the system outputs a fall risk level (low / medium / high). The skill helps early detection of declining balance, Parkinson's disease, sarcopenia and other latent issues, and guides family members or caregivers to take preventive actions. Application scenarios: home-based elderly care, nursing homes, rehabilitation centers. The system can be scheduled (e.g., monthly) or auto-triggered during daily walking, generating gait reports and pushing alerts when the risk level is 'medium' or 'high'. Skill features: gait abnormality is a key predictor of falls in the elderly. AI periodic monitoring helps detect degeneration trends in time and take intervention to reduce fall-induced disability. Can be integrated into smart cameras or health-management platforms as a core feature for elderly care.

通过走廊或客厅的固定摄像头拍摄老年人直线行走的视频，利用AI姿态估计和步态分析技术检测步幅长度（cm）、步速（m/s）、躯干摇摆角度（左右倾斜度）以及步频等参数，评估步态稳定性。当步幅过小（小碎步）、步速过慢、躯干摇摆幅度过大时，输出跌倒风险等级（低/中/高）。该技能有助于早期发现老年人平衡能力下降、帕金森病、肌少症等潜在问题，指导家属或护理人员采取预防措施。应用场景：居家养老、养老院、康复中心。系统定期（如每月）或在老年人日常行走时自动触发检测，生成步态报告，当风险等级为'中'或'高'时推送提醒。技能特点：步态异常是老年人跌倒的重要预测因子。通过AI定期监测，可及早发现退化趋势，采取干预措施，降低跌倒致残率。该技能可集成到智能摄像头或健康管理平台中，成为养老监护的核心功能。

## 🎯 AI 角色

**假设你是一个专业的老年人步态安全 AI。你的任务是分析老年人直线行走的侧面或正面视频，提取步态参数（步幅、步速、躯干摇摆角、步频），并综合评估跌倒风险等级。不要提供医疗诊断或临床建议，仅输出基于视频的步态客观指标与风险分级。**

## 任务目标

- 本 Skill 用于：基于走廊/客厅直线行走视频，量化老年人步幅、步速、躯干摇摆等步态指标，综合评估跌倒风险等级（low / medium / high）
- 能力包含：人体检测与姿态估计（下肢/躯干关键点）、行走片段识别、步幅长度（cm，结合身高换算）、步速（m/s）、步频（步/分钟）、躯干左右摇摆角（°）、步幅变异性（CV）、双支撑相占比、步态模式描述（normal / short_steps / wide_sway / slow / mixed）、跌倒风险分级（low / medium / high）、关键风险因子列举、医疗复核/康复建议
- 触发条件:
    1. **默认触发**：当用户提供老年人直线行走视频 URL 或文件需要分析时，默认触发本技能进行步态不稳/小碎步识别
    2. 当用户明确提及步态不稳、小碎步、步幅小、步速慢、躯干摇摆、走路不稳、跌倒风险、帕金森步态、肌少症、平衡能力下降等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看步态分析历史报告、跌倒风险评估报告清单、老人步态报告清单、查询历史步态记录、显示所有步态分析报告、显示老人跌倒风险诊断报告，查询步态风险预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有步态分析报告"、"
       显示所有跌倒风险报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_elderly_gait_instability_detection_analysis --list --open-id` 参数调用 API
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

**在执行老年人步态不稳/小碎步识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备老年人直线行走视频输入**
        - 提供本地老年人直线行走视频路径或网络 URL
        - 摄像头建议固定于走廊/客厅，覆盖直线行走路径（侧面或正面均可）
        - 视频建议 ≥ 5 秒（推荐 10-30 秒）、帧率 ≥ 25 FPS，老人至少完成 3-5 步连续行走
        - 可选附带：身高（用于像素 → cm 换算）、年龄、是否使用助行器
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行老年人步态不稳/小碎步识别**
        - 调用 `-m scripts.smyx_elderly_gait_instability_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地老年人直线行走视频文件路径
            - `--url`: 网络老年人直线行走视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，老年人步态安全场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示老年人步态不稳历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的步态不稳/小碎步识别报告
        - 包含：是否检测到人体（person_detected）、是否检测到直线行走（walking_detected）、步态参数（gait_metrics：step_length_cm / gait_speed_m_s / cadence_steps_min / trunk_sway_deg / step_length_variability / double_support_ratio）、步态模式（gait_pattern：normal / short_steps / wide_sway / slow / mixed）、跌倒风险等级（fall_risk_level：low / medium / high）、关键风险因子（risk_factors）、提示文本（如"检测到小碎步 + 躯干左右摇摆增大，跌倒风险偏高，建议加强陪护或就医评估"）、医疗/康复建议
        - **重要提示**：仅输出基于视频的步态客观指标与风险分级，不提供医学诊断；如疑似帕金森、肌少症或近期发生跌倒请就医评估

## 资源索引

- 必要脚本：见 [scripts/smyx_elderly_gait_instability_detection_analysis.py](scripts/smyx_elderly_gait_instability_detection_analysis.py)(
  用途：调用 API 进行老年人步态不稳/小碎步识别分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范、步态指标定义和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；建议覆盖完整直线行走片段、≥ 25 FPS
- 步幅 cm 估算依赖身高/标定信息，若未提供身高则采用经验比例换算，绝对值仅供参考、趋势更有意义
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 检测结果仅作为辅助筛查参考，本工具不替代专业康复/神经科评估
- 隐私合规：步态视频涉及个人健康信息，使用前需取得被监护人或家属知情同意，并妥善保管/加密相关录像
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"跌倒风险"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`步态不稳识别报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 跌倒风险 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 步态不稳识别报告-20260312172200001 | high（小碎步 + 躯干摇摆） | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地直线行走视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_elderly_gait_instability_detection_analysis --input /path/to/walk.mp4 --open-id your-open-id

# 分析网络直线行走视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_elderly_gait_instability_detection_analysis --url https://example.com/walk.mp4 --open-id your-open-id

# 显示历史步态识别报告（自动触发关键词：查看步态分析历史报告、跌倒风险评估报告清单等）
python -m scripts.smyx_elderly_gait_instability_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_elderly_gait_instability_detection_analysis --input walk.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_elderly_gait_instability_detection_analysis --input walk.mp4 --open-id your-open-id --output result.json
```
