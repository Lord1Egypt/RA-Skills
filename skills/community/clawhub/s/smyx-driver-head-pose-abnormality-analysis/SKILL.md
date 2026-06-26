---
name: "smyx-driver-head-pose-abnormality-analysis"
description: "Using an in-cabin DMS camera, the system analyzes the driver's head pose in real time, computing head pitch (down/up) and yaw (left/right turn). | 通过车载DMS摄像头实时分析驾驶员头部姿态，计算头部俯仰角（低头/抬头）和偏航角（左/右转头）。当低头角度超过阈值（默认>30°）且持续时间超过2秒（可能为看手机、查看物品），或侧视角度超过阈值（默认>45°）持续时间超过2秒（可能为与乘客聊天、看窗外）时，输出分心驾驶预警，联动语音提醒，预防交通事故。"
version: "1.0.2"
license: "MIT-0"
---

# Driver Head-Pose Abnormality (Head-Down / Side-View) | 驾驶员头部姿态异常（低头/侧视）检测

Using an in-cabin DMS camera, the system analyzes the driver's head pose in real time, computing head pitch (down/up) and yaw (left/right turn). When the head-down angle exceeds a threshold (default > 30°) and lasts more than 2 seconds (possibly looking at a phone or checking objects), or the side-view yaw angle exceeds a threshold (default > 45°) lasting more than 2 seconds (possibly chatting with passengers or looking out the window), it outputs a distracted-driving alert and triggers voice reminders, helping prevent traffic accidents. Application scenarios: passenger cars, commercial vehicles, ride-hailing fleets, freight fleets. The system monitors in real time; when long-duration head-down or head-side behavior is detected, it raises alerts and records distraction events. Skill features: distracted driving (especially looking down at a phone) has become a major cause of traffic accidents. AI real-time head-pose monitoring can promptly remind drivers to refocus and reduce accident risk. Can be integrated into dashcams, in-vehicle smart boxes, or fleet-management platforms to enhance driving safety.

通过车载DMS摄像头实时分析驾驶员头部姿态，计算头部俯仰角（低头/抬头）和偏航角（左/右转头）。当低头角度超过阈值（默认>30°）且持续时间超过2秒（可能为看手机、查看物品），或侧视角度超过阈值（默认>45°）持续时间超过2秒（可能为与乘客聊天、看窗外）时，输出分心驾驶预警，联动语音提醒，预防交通事故。应用场景：乘用车、商用车、网约车、货运车队。系统实时监测，当驾驶员出现长时间低头或侧头时发出警报，并记录分心事件。技能特点：分心驾驶（尤其是低头看手机）已成为交通事故的主要原因之一。通过AI实时检测头部姿态异常，可及时提醒驾驶员集中注意力，降低事故风险。该技能可集成到行车记录仪、车载智能盒子或车队管理平台中，提升驾驶安全水平。

## 🎯 AI 角色

**假设你是一个专业的驾驶员分心监测 AI。你的任务是分析驾驶员面部视频，计算头部姿态角（俯仰角 pitch、偏航角 yaw、翻滚角 roll），检测低头和侧视行为。当头部姿态超出预设阈值且持续时间超过设定值（默认 2 秒）时，输出分心预警。不要提供其他安全建议或医学诊断，仅输出基于头部姿态的检测结果。**

## 任务目标

- 本 Skill 用于：基于车载 DMS 摄像头驾驶员面部视频，实时计算头部姿态角 + 检测低头/侧视行为 + 按持续时间阈值输出分心预警
- 能力包含：驾驶员面部检测、头部关键点定位、3D 头部姿态估计（pitch / yaw / roll）、低头/侧视事件识别（角度阈值 + 持续时间阈值）、分心事件累计统计、预警类型分类（head_down_distraction / head_side_distraction / head_roll_abnormality）、座舱联动动作建议（voice_alert / fleet_upload / event_record）
- 触发条件:
    1. **默认触发**：当用户提供车载 DMS 驾驶员面部视频 URL 或文件需要分析时，默认触发本技能进行头部姿态异常检测
    2. 当用户明确提及驾驶员分心、低头看手机、侧头、看窗外、头部姿态、pitch/yaw、DMS、车载摄像头、分心驾驶、网约车安全等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看驾驶员分心历史报告、分心驾驶预警清单、头部姿态异常报告清单、查询历史低头事件、显示所有头部姿态报告、显示车队分心诊断报告，查询分心驾驶事件清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有分心驾驶报告"、"
       显示所有头部姿态异常报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_driver_head_pose_abnormality_analysis --list --open-id` 参数调用 API
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

**在执行驾驶员头部姿态异常检测前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备车载 DMS 驾驶员面部视频输入**
        - 提供本地车载 DMS 视频路径或网络 URL
        - 摄像头建议：DMS 摄像头（红外/IR-cut 优先）、安装在方向盘上方/A 柱/仪表台上方，正对驾驶员面部
        - 视频帧率 **必须 ≥ 25 FPS**、分辨率 ≥ 480p、能稳定看到面部及头部轮廓
        - 夜间/隧道场景启用红外补光；戴帽子/口罩/墨镜可能影响姿态估计稳定性
        - 可选附带：驾驶员姓名/工号、车队 ID、车型、行车段、阈值覆盖（head_down_threshold_deg / head_side_threshold_deg / distraction_duration_threshold_sec）
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行驾驶员头部姿态异常检测**
        - 调用 `-m scripts.smyx_driver_head_pose_abnormality_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地车载 DMS 驾驶员面部视频文件路径
            - `--url`: 网络车载 DMS 驾驶员面部视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，驾驶员分心监测场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示驾驶员头部姿态异常历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的驾驶员头部姿态异常检测报告
        - 包含：是否检测到驾驶员（driver_detected）、头部姿态角（head_pose_angles：pitch_deg / yaw_deg / roll_deg）、低头分心事件列表（head_down_events，含开始时间/持续秒数/最大角度）、侧视分心事件列表（head_side_events，含开始时间/持续秒数/最大角度/方向 left/right）、累计分心时长（total_distraction_duration_sec）、分心事件总次数（distraction_event_count）、预警类型（warning_type：head_down_distraction / head_side_distraction / head_roll_abnormality）、预警提示文本（如"驾驶员低头 3.2 秒（最大 -38°），疑似看手机，请立即抬头注视前方"）、建议座舱联动动作（recommend_action：voice_alert / fleet_upload / event_record）
        - **重要提示**：仅输出基于头部姿态的检测结果与方向性预警，不提供其他安全建议或医学诊断；预警仅供辅助提醒，驾驶员对车辆操作负全责

## 资源索引

- 必要脚本：见 [scripts/smyx_driver_head_pose_abnormality_analysis.py](scripts/smyx_driver_head_pose_abnormality_analysis.py)(
  用途：调用 API 进行驾驶员头部姿态异常（低头/侧视）检测，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、头部姿态阈值定义和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：帧率必须 ≥ 25 FPS 且能稳定看到面部及头部轮廓
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 检测结果仅作为驾驶员辅助安全提醒，本工具不替代驾驶员主动观察与判断；预警发生时应立即抬头注视前方道路
- 戴帽子/口罩/墨镜、严重逆光、剧烈震动等场景会显著降低头部姿态估计的可靠性
- 隐私合规：车载驾驶员视频涉及个人生物特征隐私，使用前需取得驾驶员/员工知情同意，车队部署应遵循当地隐私法规并妥善保管/加密相关录像
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"预警类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`驾驶员头部姿态异常报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 预警类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 驾驶员头部姿态异常报告-20260312172200001 | head_down_distraction（低头 3.2s / -38°） | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地车载 DMS 驾驶员视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_driver_head_pose_abnormality_analysis --input /path/to/dms.mp4 --open-id your-open-id

# 分析网络车载 DMS 驾驶员视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_driver_head_pose_abnormality_analysis --url https://example.com/dms.mp4 --open-id your-open-id

# 显示历史驾驶员头部姿态异常报告（自动触发关键词：查看驾驶员分心历史报告、分心驾驶预警清单等）
python -m scripts.smyx_driver_head_pose_abnormality_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_driver_head_pose_abnormality_analysis --input dms.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_driver_head_pose_abnormality_analysis --input dms.mp4 --open-id your-open-id --output result.json
```
