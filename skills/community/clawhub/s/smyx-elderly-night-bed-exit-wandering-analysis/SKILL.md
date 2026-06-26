---
name: "smyx-elderly-night-bed-exit-wandering-analysis"
description: "Using fixed cameras (infrared night vision) in nursing-home or home bedrooms, the system continuously monitors elderly bed-exit status and activity trajectory at night. | 通过养老院或居家卧室的固定摄像头（红外夜视），夜间连续监测老年人的离床状态和活动轨迹。输出异常预警，可联动护理人员手机或护士站大屏，防止老人走失、跌倒或发生意外。"
version: "1.0.1"
license: "MIT-0"
---

# 🛏️ Elderly Night Bed-Exit & Wandering Detection | 老年人夜间离床时长与徘徊识别
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **老年人夜间离床时长与徘徊识别** |
| 🎯 核心目标 | 通过养老院或居家卧室的固定摄像头（红外夜视），夜间连续监测老年人的离床状态和活动轨迹。输出异常预警，可联动护理人员手机或护士站大屏，防止老人走失、跌倒或发生意外。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_ELDERLY_NIGHT_BED_EXIT_WANDERING_ANALYSIS` |

Using fixed cameras (infrared night vision) in nursing-home or home bedrooms, the system continuously monitors elderly bed-exit status and activity trajectory at night. It identifies bed-exit start time, total bed-exit duration, whether the person repeatedly walks back and forth in the hallway or room (wandering), and judges whether preset safety thresholds (e.g., bed-exit > 30 min or wandering > 10 min) are exceeded. Abnormal alerts are pushed to caregivers' phones or the nurse-station big screen to prevent wandering away, falls, or accidents. Application scenarios: nursing homes, home-based elderly care, community day-care centers. The system runs automatically at night; when bed-exit lasts too long or repeated wandering occurs, it pushes alerts via app or care system (e.g., 'Grandpa Zhang in bed 3 has been out of bed for 45 minutes, please check in time'). Skill features: prolonged night bed-exit (e.g., fall after getting up) and wandering (e.g., night roaming by elders with cognitive impairment) are high-risk events in elderly care. AI real-time monitoring enables timely warnings, reduces accidents, and improves caregiving efficiency. Can be integrated into nursing-home management systems or smart-home security platforms.

通过养老院或居家卧室的固定摄像头（红外夜视），夜间连续监测老年人的离床状态和活动轨迹。识别离床开始时间、离床总时长、是否在走廊或房间内反复来回走动（徘徊），并判断是否超过预设的安全阈值（如离床>30分钟或徘徊>10分钟）。输出异常预警，可联动护理人员手机或护士站大屏，防止老人走失、跌倒或发生意外。应用场景：养老院、居家养老、社区日间照料中心。系统在夜间自动运行，当老人离床时间过长或出现反复徘徊行为时，通过APP或护理系统推送提醒（如'3号床张爷爷离床已45分钟，请及时查看'）。技能特点：夜间离床时间过长（如老人下床后跌倒无法起身）和徘徊（如认知障碍老人夜间游荡）是养老院和居家养老中的高风险事件。通过AI实时监测，可及时预警，减少意外发生，提升护理效率。该技能可集成到养老院管理系统或智能家居安防平台。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的老年人夜间行为安全 AI。你的任务是分析卧室或走廊摄像头的夜间视频（红外模式），检测老年人是否离开床铺，记录离床的总时长，并识别是否存在反复来回走动的徘徊行为。当离床时长超过设定阈值（如 30 分钟）或徘徊持续时间超过阈值（如 10 分钟）时，输出异常预警。不要提供医疗诊断或具体护理操作方案，仅输出行为统计与报警信息。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于夜间红外卧室/走廊监控视频，检测老年人离床事件、累计离床时长与徘徊行为，并按安全阈值输出预警

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 床铺区域分割 |
| 2 | 人体检测与跟踪 |
| 3 | 离床/上床事件识别 |
| 4 | 离床时长统计 |
| 5 | 活动轨迹分析 |
| 6 | 徘徊识别（反复来回走动） |
| 7 | 安全阈值判定（默认离床>30 分钟 / 徘徊>10 分钟 |
| 8 | 可覆盖） |
| 9 | 分级预警（none/info/warning/critical） |
| 10 | 预警文本生成 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供卧室/走廊夜间监控视频 URL 或文件需要分析时，默认触发本技能进行老年人夜间离床/徘徊识别 |
| 🔎 明确分析意图 | 当用户明确提及离床、起夜、夜间起床、徘徊、夜游、卧室监控、夜间监护、养老院夜班、护士站、走失预警、跌倒风险等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看夜间离床历史报告、徘徊预警报告清单、夜间监护报告清单、查询历史离床记录、显示所有夜间离床报告、显示老人夜间监护诊断报告，查询夜间预警清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_elderly_night_bed_exit_wandering_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_elderly_night_bed_exit_wandering_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备夜间监控视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行夜间离床/徘徊识别 | 调用 `-m scripts.smyx_elderly_night_bed_exit_wandering_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地卧室/走廊夜间监控视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络夜间监控视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，老年人夜间监护场景默认 `other` | 按需填写 |
| `--list` | 显示老年人夜间离床/徘徊历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_elderly_night_bed_exit_wandering_analysis.py`](scripts/smyx_elderly_night_bed_exit_wandering_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；建议夜视模式、覆盖整夜时段 |
| 🧑‍⚖️ 结果性质 | 预警结果仅作为护理参考，疑似跌倒/失踪请立即人工核实并采取紧急行动 |
| 🔏 隐私合规 | 隐私合规：夜间卧室视频涉及个人隐私，使用前需取得被监护人或家属知情同意 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地夜间监控视频
python -m scripts.smyx_elderly_night_bed_exit_wandering_analysis --input /path/to/night_room.mp4

# 分析网络夜间监控视频
python -m scripts.smyx_elderly_night_bed_exit_wandering_analysis --url https://example.com/night_room.mp4

# 显示历史夜间监护报告/徘徊预警报告清单（自动触发关键词：查看夜间离床历史报告、徘徊预警报告清单等）
python -m scripts.smyx_elderly_night_bed_exit_wandering_analysis --list

# 输出精简报告
python -m scripts.smyx_elderly_night_bed_exit_wandering_analysis --input night.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_elderly_night_bed_exit_wandering_analysis --input night.mp4 --output result.json
```
