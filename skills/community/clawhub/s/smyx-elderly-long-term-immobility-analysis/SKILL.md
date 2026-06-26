---
name: "smyx-elderly-long-term-immobility-analysis"
description: "Using fixed cameras in multiple zones of a solo-living elder's home (living room, bedroom, kitchen, bathroom, etc.), the system continuously analyzes the video streams to detect human activity (movement, limb actions, gestures, etc.). If no activity is detected within a configured time window (default 12 hours), the system outputs a 'long-term no activity' alert and can notify emergency contacts via app or phone. The skill helps detect immobilization caused by sudden illness (stroke, heart attack), falls, or syncope in time. Application scenarios: solo-living elder households, community elderly-care service centers. The system runs around the clock; when no human activity is detected beyond the preset duration (e.g., 12 hours), it automatically pushes an emergency alert to remind children, community grid workers, or care service institutions to visit. Skill features: when a solo-living elder has a sudden illness or fall and cannot call for help, long unnoticed time can cause severe consequences. AI-based long-term no-activity monitoring can trigger alerts within the golden rescue window and save lives. Can be integrated into smart-home security systems or elderly-care service platforms as the last line of defense for solo-living elders. | 通过独居老人家中的多个区域（客厅、卧室、厨房、卫生间等）固定摄像头，连续分析视频流，检测人体活动（包括移动、肢体动作、手势等）。若在设定的时间窗口内（默认12小时）未检测到任何活动，则输出'长期无活动'预警，并可通过APP或电话通知紧急联系人。该技能用于及时发现老人因突发疾病（如中风、心梗）、跌倒或晕厥导致的无法行动状况。应用场景：独居老人家庭、社区养老服务中心。系统全天候运行，当超过预设时间（如12小时）未检测到任何人体活动时，自动推送紧急预警，提醒子女、社区网格员或养老服务机构上门查看。技能特点：独居老人突发疾病或意外摔倒后无法起身求助，长时间未被发现可能造成严重后果。通过AI自动监测长期无活动，可在黄金救援时间内触发预警，挽救生命。该技能可集成到智能家居安防系统或养老服务平台中，成为独居老人安全防护的最后一道防线。"
version: "1.0.0"
---

# Elderly Long-Term Immobility Monitoring (>12h) | 老年人长期静止（超12小时）监测

Using fixed cameras in multiple zones of a solo-living elder's home (living room, bedroom, kitchen, bathroom, etc.), the system continuously analyzes the video streams to detect human activity (movement, limb actions, gestures, etc.). If no activity is detected within a configured time window (default 12 hours), the system outputs a 'long-term no activity' alert and can notify emergency contacts via app or phone. The skill helps detect immobilization caused by sudden illness (stroke, heart attack), falls, or syncope in time. Application scenarios: solo-living elder households, community elderly-care service centers. The system runs around the clock; when no human activity is detected beyond the preset duration (e.g., 12 hours), it automatically pushes an emergency alert to remind children, community grid workers, or care service institutions to visit. Skill features: when a solo-living elder has a sudden illness or fall and cannot call for help, long unnoticed time can cause severe consequences. AI-based long-term no-activity monitoring can trigger alerts within the golden rescue window and save lives. Can be integrated into smart-home security systems or elderly-care service platforms as the last line of defense for solo-living elders.

通过独居老人家中的多个区域（客厅、卧室、厨房、卫生间等）固定摄像头，连续分析视频流，检测人体活动（包括移动、肢体动作、手势等）。若在设定的时间窗口内（默认12小时）未检测到任何活动，则输出'长期无活动'预警，并可通过APP或电话通知紧急联系人。该技能用于及时发现老人因突发疾病（如中风、心梗）、跌倒或晕厥导致的无法行动状况。应用场景：独居老人家庭、社区养老服务中心。系统全天候运行，当超过预设时间（如12小时）未检测到任何人体活动时，自动推送紧急预警，提醒子女、社区网格员或养老服务机构上门查看。技能特点：独居老人突发疾病或意外摔倒后无法起身求助，长时间未被发现可能造成严重后果。通过AI自动监测长期无活动，可在黄金救援时间内触发预警，挽救生命。该技能可集成到智能家居安防系统或养老服务平台中，成为独居老人安全防护的最后一道防线。

## 🎯 AI 角色

**假设你是一个专业的独居老人安全监测 AI。你的任务是分析家中多个区域（至少客厅和卧室）固定摄像头的连续视频流，检测是否有人体活动（全身移动、四肢动作、手部动作等）。若在连续 12 小时内未检测到任何活动，则输出紧急预警。不要提供健康诊断或具体救援操作方案，仅基于视觉活动检测输出统计与报警结果。**

## 任务目标

- 本 Skill 用于：基于独居老人家中多区域连续监控视频，检测人体活动并统计累计无活动时长，按阈值输出长期静止紧急预警
- 能力包含：跨区域人体活动检测（全身移动 / 四肢动作 / 手部动作 / 姿态变化）、最近一次活动时间戳、累计无活动时长统计、活动区域覆盖统计、长期静止阈值判定（默认 12 小时，可覆盖）、分级预警（none / warning / critical / emergency）、紧急联系人通知建议
- 触发条件:
    1. **默认触发**：当用户提供独居老人家中多区域连续监控视频 URL 或文件需要分析时，默认触发本技能进行长期静止监测
    2. 当用户明确提及独居老人、长期无活动、长期静止、无人响应、无活动预警、突发疾病、跌倒无法起身、中风、心梗、晕厥、空巢老人监护等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看长期静止历史报告、独居监护报告清单、长期无活动报告清单、查询历史紧急预警记录、显示所有独居老人监护报告、显示长期静止诊断报告，查询紧急预警清单
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有长期静止报告"、"
       显示所有独居老人监护报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_elderly_long_term_immobility_analysis --list --open-id` 参数调用 API
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

**在执行老年人长期静止监测前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备多区域监控视频输入**
        - 提供本地居家多区域监控视频文件路径或网络 URL
        - 建议覆盖至少 2 个常驻区域（客厅 + 卧室），可加入厨房、卫生间
        - 摄像头建议全天候运行（含红外夜视），视频可按区域分段或上传整段长视频
        - 可选附带：被监护人姓名、紧急联系人列表、阈值覆盖（immobility_threshold_hour）
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行长期静止监测**
        - 调用 `-m scripts.smyx_elderly_long_term_immobility_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地居家多区域监控视频文件路径
            - `--url`: 网络居家多区域监控视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，独居老人监护场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示老年人长期静止历史监测报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的长期静止监测报告
        - 包含：最近一次活动时间（last_motion_time）、累计无活动时长（idle_duration_hour）、活动区域覆盖列表（active_zones）、长期静止预警标志（immobility_alert）、预警等级（none / warning / critical / emergency）、预警文本（如"独居张爷爷已 14 小时未检测到活动，建议立即联系上门查看"）、建议通知的紧急联系人
        - **重要提示**：仅基于视觉活动检测输出统计与预警，不提供医疗诊断或具体救援操作方案

## 资源索引

- 必要脚本：见 [scripts/smyx_elderly_long_term_immobility_analysis.py](scripts/smyx_elderly_long_term_immobility_analysis.py)(
  用途：调用 API 进行老年人长期静止（超 12 小时）监测分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范、阈值定义和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 mp4/avi/mov 视频，最大 10MB；建议夜视模式 + 整日时间段
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 触发紧急预警时，请立即通过电话/上门方式人工核实，本工具仅作辅助监测
- 隐私合规：居家多区域视频涉及个人隐私，使用前需取得被监护人或家属知情同意；卫生间等敏感区域建议改用毫米波雷达/PIR 传感器替代视觉
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"被监护人"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`长期静止监测报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 被监护人 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 长期静止监测报告-20260312172200001 | 独居张爷爷 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地居家多区域监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_elderly_long_term_immobility_analysis --input /path/to/home_multi_zone.mp4 --open-id your-open-id

# 分析网络居家多区域监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_elderly_long_term_immobility_analysis --url https://example.com/home_multi_zone.mp4 --open-id your-open-id

# 显示历史长期静止监测报告（自动触发关键词：查看长期静止历史报告、独居监护报告清单等）
python -m scripts.smyx_elderly_long_term_immobility_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_elderly_long_term_immobility_analysis --input home.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_elderly_long_term_immobility_analysis --input home.mp4 --open-id your-open-id --output result.json
```
