---
name: "smyx-child-outdoor-activity-monitor-analysis"
description: "Using a fixed camera at the balcony door or home entrance, the system detects how many times the child enters/exits the home or balcony. With person-tracking and region-entry/exit logic, it records the timestamps of each 'leaving indoor (outdoor)' and 'returning indoor' event, and accumulates the daily total outdoor-activity duration. | 通过家庭阳台门或入户门口的固定摄像头，检测儿童进出家门或阳台的次数，利用人体跟踪和区域进出判定技术，记录每次离开室内（外出）和返回室内（归来）的时间点，累计每日户外活动总时长。当当日总时长低于预设推荐值（默认建议学龄儿童每天至少1小时户外活动）时，输出'户外活动不足'提醒，建议家长带孩子增加户外时间。"
version: "1.0.3"
license: "MIT-0"
---

# 🏃 Child Outdoor Activity Duration Monitoring | 儿童户外活动时长监测
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **儿童户外活动时长监测** |
| 🎯 核心目标 | 通过家庭阳台门或入户门口的固定摄像头，检测儿童进出家门或阳台的次数，利用人体跟踪和区域进出判定技术，记录每次离开室内（外出）和返回室内（归来）的时间点，累计每日户外活动总时长。当当日总时长低于预设推荐值（默认建议学龄儿童每天至少1小时户外活动）时，输出'户外活动不足'提醒，建议家长带孩子增加户外时间。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_CHILD_OUTDOOR_ACTIVITY_MONITOR_ANALYSIS` |

Using a fixed camera at the balcony door or home entrance, the system detects how many times the child enters/exits the home or balcony. With person-tracking and region-entry/exit logic, it records the timestamps of each 'leaving indoor (outdoor)' and 'returning indoor' event, and accumulates the daily total outdoor-activity duration. When the daily total falls below a preset recommendation (default: at least 1 hour of outdoor activity per day for school-age children), it outputs an 'insufficient outdoor activity' alert, suggesting parents take the child out more. Application scenarios: family parenting, child health management, schools / kindergartens. The system automatically generates daily outdoor-activity reports; if multiple consecutive days fall short, it pushes app reminders to parents. Skill features: outdoor activity is crucial for child vision protection (myopia prevention), bone development, and mental health. AI automatic monitoring helps parents objectively understand the child's outdoor situation and adjust parenting strategies. Can be integrated into smart cameras or family education apps as a practical feature for child health management.

通过家庭阳台门或入户门口的固定摄像头，检测儿童进出家门或阳台的次数，利用人体跟踪和区域进出判定技术，记录每次离开室内（外出）和返回室内（归来）的时间点，累计每日户外活动总时长。当当日总时长低于预设推荐值（默认建议学龄儿童每天至少1小时户外活动）时，输出'户外活动不足'提醒，建议家长带孩子增加户外时间。应用场景：家庭育儿、儿童健康管理、学校/幼儿园。系统自动生成每日户外活动报告，若连续多日不足，通过APP推送提醒家长。技能特点：户外活动对儿童视力保护（预防近视）、骨骼发育、心理健康至关重要。通过AI自动监测，可帮助家长客观了解孩子户外活动情况，及时调整育儿方式。该技能可集成到智能摄像头或家庭教育APP中，成为儿童健康管理的实用功能。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的儿童健康成长 AI。你的任务是分析阳台门或入户门口固定摄像头的视频，检测儿童进出区域的行为，记录外出和归来时间，累计每日户外活动总时长。当总时长低于推荐值时输出提醒。不要提供医疗建议或医学诊断，仅输出基于视觉的活动统计与友好提醒。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于阳台门/入户门口固定摄像头视频，识别儿童跨区域进出事件 → 累计每日户外活动总时长 → 对比推荐值（默认 ≥ 60 min）→ 输出户外活动不足提醒

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 人体检测与跟踪 |
| 2 | 儿童识别（结合身高/外观特征） |
| 3 | 室内/户外两个 ROI 划分（indoor_region / outdoor_region） |
| 4 | 区域进出事件识别（exit / return） |
| 5 | 配对生成每次"外出-归来"会话 |
| 6 | 累计每日总时长 + 会话次数 + 每次时长 |
| 7 | 推荐值对比与达成率计算 |
| 8 | 连续不足天数累计 |
| 9 | 提醒类型分类（daily_outdoor_insufficient / multi_day_outdoor_insufficient / outdoor_goal_met / normal） |
| 10 | 家长友好提醒文本生成 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供阳台门/入户门口固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行儿童户外活动时长监测 |
| 🔎 明确分析意图 | 当用户明确提及儿童户外活动、近视预防、户外时间、骨骼发育、阳光时间、宝宝出门、家庭育儿健康等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看儿童户外活动历史报告、户外时长报告清单、儿童出门记录清单、查询历史儿童户外活动记录、显示所有儿童户外活动报告、显示家庭育儿健康诊断报告，查询儿童户外活动不足预警清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_child_outdoor_activity_monitor_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_child_outdoor_activity_monitor_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备阳台门/入户门口固定摄像头视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行儿童户外活动时长监测 | 调用 `-m scripts.smyx_child_outdoor_activity_monitor_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地阳台门/入户门口固定摄像头视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络阳台门/入户门口固定摄像头视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，儿童健康成长场景默认 `other` | 按需填写 |
| `--list` | 显示儿童户外活动时长监测历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_child_outdoor_activity_monitor_analysis.py`](scripts/smyx_child_outdoor_activity_monitor_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：画面必须同时覆盖室内与户外（阳台/楼道）两个区域 |
| 🧑‍⚖️ 结果性质 | 户外时长统计仅基于"进出门事件"，**不直接代表真实户外运动量**；孩子从阳台门出去阳台坐着也会被计入"户外"，建议结合家长主观感受参考 |
| 🔎 使用提醒 | 多孩家庭、儿童外观相近时需注意身份混淆；可结合身高/衣着辅助识别 |
| 🔎 使用提醒 | 短时间下楼丢垃圾、收快递（< 5 min）默认视为无效会话，可由调用方覆盖阈值 |
| 🔏 隐私合规 | 隐私合规：家庭门口/阳台视频涉及未成年人隐私，使用前需取得监护人明确知情同意，妥善加密保管；建议优先采用人体轮廓模式 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地阳台门/入户门口视频
python -m scripts.smyx_child_outdoor_activity_monitor_analysis --input /path/to/door.mp4

# 分析网络阳台门/入户门口视频
python -m scripts.smyx_child_outdoor_activity_monitor_analysis --url https://example.com/door.mp4

# 显示历史儿童户外活动时长监测报告（自动触发关键词：查看儿童户外活动历史报告、户外时长报告清单等）
python -m scripts.smyx_child_outdoor_activity_monitor_analysis --list

# 输出精简报告
python -m scripts.smyx_child_outdoor_activity_monitor_analysis --input door.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_child_outdoor_activity_monitor_analysis --input door.mp4 --output result.json
```
