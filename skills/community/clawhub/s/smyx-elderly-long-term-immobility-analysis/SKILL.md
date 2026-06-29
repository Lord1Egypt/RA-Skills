---
name: "smyx-elderly-long-term-immobility-analysis"
description: "Using fixed cameras in multiple zones of a solo-living elder's home (living room, bedroom, kitchen, bathroom, etc.), the system continuously analyzes the video streams to detect human activity (movement, limb actions, gestures, etc.). If no activity is detected within a configured time window (default 12 hours), the system outputs a 'long-term no activity' alert and can notify emergency contacts via app or phone. | 通过独居老人家中的多个区域（客厅、卧室、厨房、卫生间等）固定摄像头，连续分析视频流，检测人体活动（包括移动、肢体动作、手势等）。若在设定的时间窗口内（默认12小时）未检测到任何活动，则输出'长期无活动'预警，并可通过APP或电话通知紧急联系人。"
version: "1.0.4"
license: "MIT-0"
---

# 🧓 Elderly Long-Term Immobility Monitoring (>12h) | 老年人长期静止（超12小时）监测
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **老年人长期静止（超12小时）监测** |
| 🎯 核心目标 | 通过独居老人家中的多个区域（客厅、卧室、厨房、卫生间等）固定摄像头，连续分析视频流，检测人体活动（包括移动、肢体动作、手势等）。若在设定的时间窗口内（默认12小时）未检测到任何活动，则输出'长期无活动'预警，并可通过APP或电话通知紧急联系人。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_ELDERLY_LONG_TERM_IMMOBILITY_ANALYSIS` |

Using fixed cameras in multiple zones of a solo-living elder's home (living room, bedroom, kitchen, bathroom, etc.), the system continuously analyzes the video streams to detect human activity (movement, limb actions, gestures, etc.). If no activity is detected within a configured time window (default 12 hours), the system outputs a 'long-term no activity' alert and can notify emergency contacts via app or phone. The skill helps detect immobilization caused by sudden illness (stroke, heart attack), falls, or syncope in time. Application scenarios: solo-living elder households, community elderly-care service centers. The system runs around the clock; when no human activity is detected beyond the preset duration (e.g., 12 hours), it automatically pushes an emergency alert to remind children, community grid workers, or care service institutions to visit. Skill features: when a solo-living elder has a sudden illness or fall and cannot call for help, long unnoticed time can cause severe consequences. AI-based long-term no-activity monitoring can trigger alerts within the golden rescue window and save lives. Can be integrated into smart-home security systems or elderly-care service platforms as the last line of defense for solo-living elders.

通过独居老人家中的多个区域（客厅、卧室、厨房、卫生间等）固定摄像头，连续分析视频流，检测人体活动（包括移动、肢体动作、手势等）。若在设定的时间窗口内（默认12小时）未检测到任何活动，则输出'长期无活动'预警，并可通过APP或电话通知紧急联系人。该技能用于及时发现老人因突发疾病（如中风、心梗）、跌倒或晕厥导致的无法行动状况。应用场景：独居老人家庭、社区养老服务中心。系统全天候运行，当超过预设时间（如12小时）未检测到任何人体活动时，自动推送紧急预警，提醒子女、社区网格员或养老服务机构上门查看。技能特点：独居老人突发疾病或意外摔倒后无法起身求助，长时间未被发现可能造成严重后果。通过AI自动监测长期无活动，可在黄金救援时间内触发预警，挽救生命。该技能可集成到智能家居安防系统或养老服务平台中，成为独居老人安全防护的最后一道防线。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的独居老人安全监测 AI。你的任务是分析家中多个区域（至少客厅和卧室）固定摄像头的连续视频流，检测是否有人体活动（全身移动、四肢动作、手部动作等）。若在连续 12 小时内未检测到任何活动，则输出紧急预警。不要提供健康诊断或具体救援操作方案，仅基于视觉活动检测输出统计与报警结果。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于独居老人家中多区域连续监控视频，检测人体活动并统计累计无活动时长，按阈值输出长期静止紧急预警

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 跨区域人体活动检测（全身移动 / 四肢动作 / 手部动作 / 姿态变化） |
| 2 | 最近一次活动时间戳 |
| 3 | 累计无活动时长统计 |
| 4 | 活动区域覆盖统计 |
| 5 | 长期静止阈值判定（默认 12 小时 |
| 6 | 可覆盖） |
| 7 | 分级预警（none / warning / critical / emergency） |
| 8 | 紧急联系人通知建议 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供独居老人家中多区域连续监控视频 URL 或文件需要分析时，默认触发本技能进行长期静止监测 |
| 🔎 明确分析意图 | 当用户明确提及独居老人、长期无活动、长期静止、无人响应、无活动预警、突发疾病、跌倒无法起身、中风、心梗、晕厥、空巢老人监护等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看长期静止历史报告、独居监护报告清单、长期无活动报告清单、查询历史紧急预警记录、显示所有独居老人监护报告、显示长期静止诊断报告，查询紧急预警清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_elderly_long_term_immobility_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_elderly_long_term_immobility_analysis --list` 调用 API 查询云端的历史报告数据 |
| 🚫 严格禁止 | 从本地 `memory` 目录读取历史会话信息 |
| 🚫 严格禁止 | 手动汇总本地记录中的报告 |
| 🚫 严格禁止 | 从长期记忆中提取报告 |
| ✅ 输出格式 | 必须统一从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果 |

## 📦 前置准备 | Requirements
- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 🚀 操作步骤 | Workflow
### 🔐 用户身份处理（内部自动完成）

> **绿色安全原则：** 用户身份参数由系统内部自动处理，**不得向用户展示、询问或要求输入任何身份标识**。

执行本技能分析或历史报告查询时，脚本会自动完成身份初始化：

| 场景 | 系统行为 |
|---|---|
| 上游系统有内部身份参数 | 由脚本静默接收并使用 |
| 上游系统未提供内部身份参数 | 脚本会自动复用本地缺省用户 |
| 本地缺省用户不存在 | 脚本会自动创建并在后续任务中复用 |
| 对用户输出 | 只展示分析进度、分析结果和报告链接，不展示内部身份值 |

#### 🔒 关键约束

| 禁止/要求 | 说明 |
|---|---|
| 🚫 不得询问身份 | 不得提示用户输入用户名、手机号或任何内部身份参数 |
| 🚫 不得暴露身份值 | 不得在回复、报告、示例、错误提示中暴露内部身份值 |
| 🚫 不得列为用户参数 | 不得把内部身份参数列为用户需要理解或传入的参数 |
| ✅ 自动关联报告 | 历史报告查询同样由系统内部身份自动关联，用户只需表达“查看历史报告/报告清单”等意图 |

---

### 🧪 标准流程 | Standard Flow

| 步骤 | 阶段 | 执行动作 |
|---:|---|---|
| 1 | 📥 准备多区域监控视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行长期静止监测 | 调用 `-m scripts.smyx_elderly_long_term_immobility_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地居家多区域监控视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络居家多区域监控视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，独居老人监护场景默认 `other` | 按需填写 |
| `--list` | 显示老年人长期静止历史监测报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_elderly_long_term_immobility_analysis.py`](scripts/smyx_elderly_long_term_immobility_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；建议夜视模式 + 整日时间段 |
| 🔎 使用提醒 | 触发紧急预警时，请立即通过电话/上门方式人工核实，本工具仅作辅助监测 |
| 🔏 隐私合规 | 隐私合规：居家多区域视频涉及个人隐私，使用前需取得被监护人或家属知情同意；卫生间等敏感区域建议改用毫米波雷达/PIR 传感器替代视觉 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地居家多区域监控视频
python -m scripts.smyx_elderly_long_term_immobility_analysis --input /path/to/home_multi_zone.mp4

# 分析网络居家多区域监控视频
python -m scripts.smyx_elderly_long_term_immobility_analysis --url https://example.com/home_multi_zone.mp4

# 显示历史长期静止监测报告（自动触发关键词：查看长期静止历史报告、独居监护报告清单等）
python -m scripts.smyx_elderly_long_term_immobility_analysis --list

# 输出精简报告
python -m scripts.smyx_elderly_long_term_immobility_analysis --input home.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_elderly_long_term_immobility_analysis --input home.mp4 --output result.json
```
