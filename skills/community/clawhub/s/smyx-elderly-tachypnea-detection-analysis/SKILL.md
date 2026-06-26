---
name: "smyx-elderly-tachypnea-detection-analysis"
description: "Using a fixed bedroom camera (infrared or low-light), the system analyzes chest/abdominal motion of the elderly at rest (sleeping or quietly lying down) and computes the respiratory rate (breaths per minute). | 通过卧室固定摄像头（红外或微光），在老年人静息（睡眠或静卧）状态下分析其胸腹部起伏运动，计算呼吸频率（次/分钟）。当呼吸频率超过正常上限（默认24次/分，老年人静息正常值一般为12-20次/分）时，输出'呼吸急促'预警，提示家属或护理人员关注老年人是否有心肺疾病、发热或呼吸系统感染等潜在问题。"
version: "1.0.1"
license: "MIT-0"
---

# Elderly Tachypnea / Dyspnea Detection | 老年人呼吸急促/困难识别

Using a fixed bedroom camera (infrared or low-light), the system analyzes chest/abdominal motion of the elderly at rest (sleeping or quietly lying down) and computes the respiratory rate (breaths per minute). When the respiratory rate exceeds a preset upper bound (default 24 bpm; the normal resting range for the elderly is generally 12-20 bpm), the system outputs a 'tachypnea' alert, reminding family members or caregivers to pay attention to possible cardiopulmonary diseases, fever, or respiratory infections. Application scenarios: home-based elderly care, nursing homes, rehabilitation wards. The system monitors continuously; when an elevated respiratory rate persists, alerts are pushed proactively. Skill features: tachypnea is an early signal of pneumonia, heart failure, acute exacerbation of COPD and other conditions. AI auto-monitoring helps families detect problems in time and avoid delayed treatment. Can be integrated into smart cameras or elderly-care platforms to improve at-home health safety.

通过卧室固定摄像头（红外或微光），在老年人静息（睡眠或静卧）状态下分析其胸腹部起伏运动，计算呼吸频率（次/分钟）。当呼吸频率超过正常上限（默认24次/分，老年人静息正常值一般为12-20次/分）时，输出'呼吸急促'预警，提示家属或护理人员关注老年人是否有心肺疾病、发热或呼吸系统感染等潜在问题。应用场景：居家养老、养老院、康复病房。系统持续监测，发现呼吸频率持续升高时主动推送警报。技能特点：呼吸急促是肺炎、心衰、慢阻肺急性加重等疾病的早期信号。通过AI自动监测，可帮助家属及时发现问题，避免延误治疗。该技能可集成到智能摄像头或养老平台中，提升老年人居家健康安全水平。

## 🎯 AI 角色

**假设你是一个专业的老年人呼吸健康监测 AI。你的任务是分析老年人静息状态下胸腹部的视频，检测呼吸周期，计算呼吸频率（次/分钟）。当呼吸频率超过阈值（默认 24 次/分）时，输出预警。不要提供医疗诊断或临床建议，仅输出基于视觉的呼吸频率数值与异常提示。**

## 任务目标

- 本 Skill 用于：基于老年人静息（睡眠/静卧）状态下胸腹部监控视频，提取呼吸频率，按阈值评估呼吸急促/困难风险
- 能力包含：人体卧姿检测、胸腹起伏轮廓识别、微小位移信号提取（可结合视频放大）、呼吸周期检测、呼吸频率（次/分钟）计算、节律评估（regular / irregular / paradoxical）、信号质量评级（high / medium / low）、风险等级判定（normal / mild / warning / critical）
- 触发条件:
    1. **默认触发**：当用户提供老年人静息状态胸腹部监控视频 URL 或文件需要分析时，默认触发本技能进行呼吸急促识别
    2. 当用户明确提及呼吸急促、呼吸困难、气促、呼吸频率监测、胸闷、肺炎前兆、心衰、慢阻肺、夜间气短等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看呼吸急促历史报告、呼吸频率报告清单、老人呼吸监测报告清单、查询历史呼吸记录、显示所有呼吸急促报告、显示老人呼吸健康诊断报告，查询呼吸风险预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有呼吸急促报告"、"
       显示所有呼吸频率报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_elderly_tachypnea_detection_analysis --list --open-id` 参数调用 API
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

**在执行老年人呼吸急促/困难识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备老年人静息状态胸腹部视频输入**
        - 提供本地静息状态视频路径或网络 URL
        - 摄像头建议固定于卧室上方/侧方，覆盖胸腹部区域
        - 老人需处于静息状态（睡眠或静卧），视频时长建议 ≥ 30 秒（推荐 60 秒），帧率 ≥ 15 FPS；夜间启用红外/微光模式
        - 可选附带：被监护人姓名、体温、近期是否有发热/咳嗽/胸闷等症状、阈值覆盖（rr_alert_threshold_bpm）
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行老年人呼吸急促/困难识别**
        - 调用 `-m scripts.smyx_elderly_tachypnea_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地老年人静息状态胸腹部监控视频文件路径
            - `--url`: 网络老年人静息状态胸腹部监控视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，老年人呼吸健康监测场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示老年人呼吸急促历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的呼吸急促识别报告
        - 包含：是否检测到躺卧人体（person_detected）、是否处于静息状态（is_resting）、呼吸频率（respiratory_rate_bpm，次/分钟）、呼吸节律（respiratory_pattern：regular / irregular / paradoxical）、胸腹起伏幅度（chest_amplitude_pixel）、信号质量（signal_quality：high / medium / low）、风险等级（risk_level：normal / mild / warning / critical）、提示文本（如"检测到老人静息呼吸频率 26 次/分，超过 24 次/分阈值，建议关注是否有发热、肺炎或心衰等情况，必要时就医"）、医疗复核提示
        - **重要提示**：仅输出基于视觉的呼吸频率数值与异常提示，不提供医学诊断；如疑似肺炎、心衰、慢阻肺急性加重请及时就医

## 资源索引

- 必要脚本：见 [scripts/smyx_elderly_tachypnea_detection_analysis.py](scripts/smyx_elderly_tachypnea_detection_analysis.py)(
  用途：调用 API 进行老年人呼吸急促/困难识别分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范、呼吸频率分级和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；建议夜视模式、≥ 30 秒、覆盖胸腹部
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 触发紧急预警时，请立即通过电话/上门方式人工核实，本工具仅作辅助监测，必要时拨打 120
- 隐私合规：卧室视频涉及个人隐私，使用前需取得被监护人或家属知情同意，并妥善保管/加密相关录像
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"呼吸频率"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`呼吸急促识别报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 呼吸频率 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 呼吸急促识别报告-20260312172200001 | 26 次/分（warning） | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地静息胸腹部监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_elderly_tachypnea_detection_analysis --input /path/to/chest.mp4 --open-id your-open-id

# 分析网络静息胸腹部监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_elderly_tachypnea_detection_analysis --url https://example.com/chest.mp4 --open-id your-open-id

# 显示历史呼吸急促识别报告（自动触发关键词：查看呼吸急促历史报告、呼吸频率报告清单等）
python -m scripts.smyx_elderly_tachypnea_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_elderly_tachypnea_detection_analysis --input chest.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_elderly_tachypnea_detection_analysis --input chest.mp4 --open-id your-open-id --output result.json
```
