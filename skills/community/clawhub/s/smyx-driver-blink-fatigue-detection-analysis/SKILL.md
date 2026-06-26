---
name: "smyx-driver-blink-fatigue-detection-analysis"
description: "Using an in-cabin DMS camera, the system analyzes the driver's facial video in real time, detects eye open/closed state, calculates blink rate per minute (normal range 15-20 blinks/min), and identifies single-blink closure duration. When blink rate drops abnormally low (e.g., < 10 blinks/min) or a single eye-closure exceeds 2 seconds (microsleep precursor), it issues a fatigue-driving alert, triggering in-cabin voice reminders or seat-vibration, helping prevent accidents caused by drowsy driving. Application scenarios: passenger cars, commercial vehicles, ride-hailing fleets, freight fleets. The system monitors in real time and on detection raises audio/visual alerts and uploads events to the fleet-management platform. Skill features: drowsy driving is a major cause of traffic accidents. AI real-time detection of abnormal blinking and microsleep can promptly remind the driver and reduce accident risk. Can be integrated into dashcams, smart cockpits, or ride-hailing safety systems to enhance driving safety. | 通过车载DMS摄像头实时分析驾驶员面部视频，检测眼部开闭状态，计算每分钟眨眼频率（正常约为15-20次/分钟），并识别闭眼持续时间。当眨眼频率异常降低（如<10次/分钟）或出现单次闭眼超过2秒（微睡眠前兆）时，输出疲劳驾驶预警，联动车内语音提醒或震动座椅，预防因疲劳导致的事故。应用场景：乘用车、商用车、网约车、货运车队。系统实时监测，当检测到疲劳迹象时发出声光报警，并上传至车队管理平台。技能特点：疲劳驾驶是交通事故的重要原因。通过AI实时检测眨眼异常和微睡眠，可及时提醒驾驶员，降低事故风险。该技能可集成到行车记录仪、智能座舱或网约车安全系统中，提升驾驶安全。"
version: "1.0.0"
---

# Driver Blink-Rate & Eye-Closure Fatigue Detection | 驾驶员眨眼频率与闭眼时长检测

Using an in-cabin DMS camera, the system analyzes the driver's facial video in real time, detects eye open/closed state, calculates blink rate per minute (normal range 15-20 blinks/min), and identifies single-blink closure duration. When blink rate drops abnormally low (e.g., < 10 blinks/min) or a single eye-closure exceeds 2 seconds (microsleep precursor), it issues a fatigue-driving alert, triggering in-cabin voice reminders or seat-vibration, helping prevent accidents caused by drowsy driving. Application scenarios: passenger cars, commercial vehicles, ride-hailing fleets, freight fleets. The system monitors in real time and on detection raises audio/visual alerts and uploads events to the fleet-management platform. Skill features: drowsy driving is a major cause of traffic accidents. AI real-time detection of abnormal blinking and microsleep can promptly remind the driver and reduce accident risk. Can be integrated into dashcams, smart cockpits, or ride-hailing safety systems to enhance driving safety.

通过车载DMS摄像头实时分析驾驶员面部视频，检测眼部开闭状态，计算每分钟眨眼频率（正常约为15-20次/分钟），并识别闭眼持续时间。当眨眼频率异常降低（如<10次/分钟）或出现单次闭眼超过2秒（微睡眠前兆）时，输出疲劳驾驶预警，联动车内语音提醒或震动座椅，预防因疲劳导致的事故。应用场景：乘用车、商用车、网约车、货运车队。系统实时监测，当检测到疲劳迹象时发出声光报警，并上传至车队管理平台。技能特点：疲劳驾驶是交通事故的重要原因。通过AI实时检测眨眼异常和微睡眠，可及时提醒驾驶员，降低事故风险。该技能可集成到行车记录仪、智能座舱或网约车安全系统中，提升驾驶安全。

## 🎯 AI 角色

**假设你是一个专业的驾驶员疲劳监测 AI。你的任务是分析驾驶员面部视频，检测眼部状态（睁开/闭合），计算眨眼频率（次/分钟）和单次闭眼持续时间。当眨眼频率低于正常阈值或出现长时间闭眼时，输出疲劳预警。不要提供医疗诊断或睡眠障碍诊断，仅输出基于视觉的疲劳指标与方向性预警提示。**

## 任务目标

- 本 Skill 用于：基于车载 DMS 摄像头驾驶员面部视频，实时检测眼部开闭状态、计算眨眼频率与闭眼时长，识别微睡眠等疲劳前兆并输出预警
- 能力包含：驾驶员面部检测、眼部 ROI 关键点定位、眼部开闭分类（open / closed / partial）、每分钟眨眼次数统计、平均/最长闭眼时长、微睡眠（单次闭眼 > 2s）识别、PERCLOS 计算、疲劳等级判定（normal / mild / moderate / severe）、座舱联动动作建议（voice_alert / seat_vibrate / fleet_upload）
- 触发条件:
    1. **默认触发**：当用户提供车载 DMS 驾驶员面部视频 URL 或文件需要分析时，默认触发本技能进行疲劳检测
    2. 当用户明确提及驾驶员疲劳、疲劳驾驶、眨眼频率、闭眼时长、微睡眠、PERCLOS、DMS、车载摄像头、行车安全、网约车安全等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看驾驶员疲劳历史报告、疲劳驾驶预警清单、驾驶员监测报告清单、查询历史微睡眠事件、显示所有疲劳驾驶报告、显示车队安全诊断报告，查询疲劳驾驶事件清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有疲劳驾驶报告"、"
       显示所有驾驶员疲劳报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_driver_blink_fatigue_detection_analysis --list --open-id` 参数调用 API
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

**在执行驾驶员眨眼频率与闭眼时长检测前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备车载 DMS 驾驶员面部视频输入**
        - 提供本地车载 DMS 视频路径或网络 URL
        - 摄像头建议：DMS 摄像头（红外/IR-cut 优先）、安装在方向盘上方/A 柱/仪表台上方，正对驾驶员面部
        - 视频帧率 **必须 ≥ 25 FPS（推荐 30 FPS）**、分辨率 ≥ 480p、能稳定看到双眼区域
        - 夜间/隧道场景启用红外补光；支持戴普通眼镜，墨镜会显著影响检测
        - 可选附带：驾驶员姓名/工号、车队 ID、车型、行车段（高速/城市/夜间）、阈值覆盖
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行驾驶员眨眼/闭眼疲劳检测**
        - 调用 `-m scripts.smyx_driver_blink_fatigue_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地车载 DMS 驾驶员面部视频文件路径
            - `--url`: 网络车载 DMS 驾驶员面部视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，驾驶员疲劳监测场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示驾驶员疲劳监测历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的驾驶员疲劳检测报告
        - 包含：是否检测到驾驶员（driver_detected）、双眼是否可见（eye_visible）、眨眼相关指标（blink_metrics：blink_count_per_minute / avg_blink_duration_ms / max_closed_eye_duration_ms / microsleep_count / perclos）、疲劳等级（fatigue_level：normal / mild / moderate / severe）、预警类型（warning_type：low_blink_rate / microsleep / prolonged_eye_closure / high_perclos / eyes_off_road）、预警提示文本（如"驾驶员眨眼频率仅 8 次/分钟且出现 1 次 2.4 秒微睡眠，请立即靠边休息"）、建议座舱联动动作（recommend_action：voice_alert / seat_vibrate / fleet_upload）
        - **重要提示**：仅输出基于视觉的驾驶员疲劳指标与方向性预警，不提供医学诊断或睡眠障碍诊断；预警仅供辅助提醒，驾驶员对车辆操作负全责

## 资源索引

- 必要脚本：见 [scripts/smyx_driver_blink_fatigue_detection_analysis.py](scripts/smyx_driver_blink_fatigue_detection_analysis.py)(
  用途：调用 API 进行驾驶员眨眼频率与闭眼时长检测，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口规范、PERCLOS/微睡眠阈值定义和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：帧率必须 ≥ 25 FPS 且能稳定看到双眼
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 检测结果仅作为驾驶员辅助安全提醒，本工具不替代驾驶员主动观察与判断；预警发生时应立即靠边安全休息
- 戴墨镜、严重逆光、面部遮挡、强烈眩光等场景会显著降低检测可靠性
- 隐私合规：车载驾驶员视频涉及个人生物特征隐私，使用前需取得驾驶员/员工知情同意，车队部署应遵循当地隐私法规并妥善保管/加密相关录像
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"疲劳等级"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`驾驶员眨眼疲劳检测报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 疲劳等级 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 驾驶员眨眼疲劳检测报告-20260312172200001 | severe（眨眼 8/min + 1 次 2.4s 微睡眠） | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地车载 DMS 驾驶员视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_driver_blink_fatigue_detection_analysis --input /path/to/dms.mp4 --open-id your-open-id

# 分析网络车载 DMS 驾驶员视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_driver_blink_fatigue_detection_analysis --url https://example.com/dms.mp4 --open-id your-open-id

# 显示历史驾驶员疲劳检测报告（自动触发关键词：查看驾驶员疲劳历史报告、疲劳驾驶预警清单等）
python -m scripts.smyx_driver_blink_fatigue_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_driver_blink_fatigue_detection_analysis --input dms.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_driver_blink_fatigue_detection_analysis --input dms.mp4 --open-id your-open-id --output result.json
```
