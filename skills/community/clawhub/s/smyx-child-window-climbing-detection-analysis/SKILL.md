---
name: "smyx-child-window-climbing-detection-analysis"
description: "Using fixed cameras in living rooms or child-activity areas (aimed at windows or balconies), AI pose estimation and object detection analyze the video in real time to recognize whether a child is climbing windows, leaning out, or gripping window-sill edges. | 通过家庭客厅或儿童活动区域的固定摄像头（需对准窗户或阳台），利用AI姿态估计和目标检测技术实时分析视频，识别儿童是否发生攀爬窗户、身体探出窗外、抓握窗台边缘等危险行为，当检测到危险动作时立即输出预警，联动手机APP推送警报或触发声光报警器。该技能可有效预防儿童坠楼事故。"
version: "1.0.2"
license: "MIT-0"
---

# Child Window/Balcony Climbing Detection | 儿童攀爬窗户/阳台识别

Using fixed cameras in living rooms or child-activity areas (aimed at windows or balconies), AI pose estimation and object detection analyze the video in real time to recognize whether a child is climbing windows, leaning out, or gripping window-sill edges. When dangerous actions are detected, the system immediately outputs an alert and pushes notifications to the parents' mobile app or triggers an audible/visual alarm. The skill effectively helps prevent child fall-from-height accidents. Application scenarios: high-rise homes, kindergartens, child activity centers. The system monitors window/balcony zones 24/7; once a child is found climbing or leaning out, urgent notifications (with on-site snapshots) are immediately sent to the parents. Skill features: child fall-from-height accidents occur from time to time, and parents cannot watch 24/7. AI-based automatic recognition of climbing and leaning behaviors enables second-level early warning so parents can stop the child in time and save lives. Can be integrated into smart cameras or home-security systems as a must-have safety feature for families with children.

通过家庭客厅或儿童活动区域的固定摄像头（需对准窗户或阳台），利用AI姿态估计和目标检测技术实时分析视频，识别儿童是否发生攀爬窗户、身体探出窗外、抓握窗台边缘等危险行为，当检测到危险动作时立即输出预警，联动手机APP推送警报或触发声光报警器。该技能可有效预防儿童坠楼事故。应用场景：家庭住宅（高层）、幼儿园、儿童活动中心。系统24小时监测窗户/阳台区域，一旦识别到儿童攀爬或身体探出，立即向家长手机发送紧急通知（含现场快照）。技能特点：儿童坠楼事故时有发生，家长难以24小时盯守。通过AI视觉自动识别攀爬和探出行为，可在事发前秒级预警，帮助家长及时制止，挽救生命。该技能可集成到智能摄像头或家庭安防系统中，成为有孩家庭的标配安全功能。

## 🎯 AI 角色

**假设你是一个专业的儿童居家安全 AI。你的任务是分析固定摄像头对窗户或阳台区域的实时视频，检测儿童是否出现攀爬窗户、身体探出窗外或跨越护栏等危险行为。当危险行为置信度超过阈值时，输出紧急预警。不要提供其他安全建议或具体处置方案，仅输出行为识别结果与预警信息。**

## 任务目标

- 本 Skill 用于：基于对准窗户/阳台的固定摄像头视频，实时识别儿童攀爬、跨栏、探身、抓握窗台等高坠风险行为，秒级输出预警
- 能力包含：儿童目标检测（区分儿童与成人）、人体姿态估计、攀爬窗户识别、跨越护栏识别、身体探出窗外识别、抓握窗台边缘识别、危险姿态判定（失衡 / 单脚悬空 / 头部探出）、置信度阈值过滤、现场快照生成、分级预警（warning / critical / emergency）、紧急预警文本生成
- 触发条件:
    1. **默认触发**：当用户提供窗户/阳台区域监控视频 URL 或文件需要分析时，默认触发本技能进行儿童攀爬识别
    2. 当用户明确提及儿童攀爬、阳台危险、窗户安全、儿童坠楼预防、跨越护栏、探身窗外、儿童看护、儿童安全、高层住宅安全等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看儿童攀爬历史报告、攀爬预警报告清单、儿童窗户安全报告清单、查询历史儿童攀爬记录、显示所有儿童安全预警报告、显示儿童攀爬诊断报告，查询儿童危险行为预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有儿童攀爬报告"、"
       显示所有攀爬预警报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_child_window_climbing_detection_analysis --list --open-id` 参数调用 API
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

**在执行儿童攀爬窗户/阳台识别前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备窗户/阳台监控视频输入**
        - 提供本地窗户/阳台区域监控视频文件路径或网络 URL
        - 摄像头必须正对窗户、阳台、护栏等高坠风险区域；建议 24 小时全天候采集（含红外夜视）
        - 视频帧率建议 ≥ 15 FPS，确保动作捕捉的实时性
        - 可选附带：被监护儿童年龄、楼层、紧急联系人列表
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行儿童攀爬窗户/阳台识别**
        - 调用 `-m scripts.smyx_child_window_climbing_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地窗户/阳台区域监控视频文件路径
            - `--url`: 网络窗户/阳台监控视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，儿童居家安全场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示儿童攀爬窗户/阳台历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的儿童攀爬危险行为预警报告
        - 包含：是否检测到儿童（child_detected）、触发的危险行为类型（risk_action：climbing_window / crossing_railing / lean_out_window / grip_window_edge / risky_posture）、置信度（confidence）、事件时间戳（event_time）、现场快照 URL（snapshot_url）、预警等级（warning / critical / emergency）、紧急预警文本（如"检测到儿童正在攀爬阳台护栏，请立即制止"）
        - **重要提示**：仅输出行为识别结果与预警信息，不提供其他安全建议或具体处置方案

## 资源索引

- 必要脚本：见 [scripts/smyx_child_window_climbing_detection_analysis.py](scripts/smyx_child_window_climbing_detection_analysis.py)(
  用途：调用 API 进行儿童攀爬窗户/阳台识别分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范、危险行为类型和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；建议正对窗户/阳台、帧率 ≥ 15 FPS
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 预警结果仅作为儿童安全监护的辅助预警工具，本工具不能替代成人监护；触发紧急预警时请立即上前制止
- 隐私合规：儿童视频涉及未成年人隐私，使用前需取得监护人知情同意，并妥善保管/加密相关录像
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"危险行为"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`儿童攀爬窗户阳台预警报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 危险行为 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 儿童攀爬窗户阳台预警报告-20260312172200001 | 攀爬阳台护栏 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地窗户/阳台监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_child_window_climbing_detection_analysis --input /path/to/balcony.mp4 --open-id your-open-id

# 分析网络窗户/阳台监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_child_window_climbing_detection_analysis --url https://example.com/balcony.mp4 --open-id your-open-id

# 显示历史儿童攀爬预警报告（自动触发关键词：查看儿童攀爬历史报告、攀爬预警报告清单等）
python -m scripts.smyx_child_window_climbing_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_child_window_climbing_detection_analysis --input balcony.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_child_window_climbing_detection_analysis --input balcony.mp4 --open-id your-open-id --output result.json
```
