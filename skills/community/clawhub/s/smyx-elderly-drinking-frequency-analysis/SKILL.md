---
name: "smyx-elderly-drinking-frequency-analysis"
description: "Using a fixed camera in the living room or kitchen, the system analyzes video of the water-cup placement area (e.g., coffee table, dining table), detects hand-to-cup contact actions (pickup, putdown), and counts daily cup-pickup events (an indirect proxy for water intake). | 通过客厅或厨房固定摄像头，分析水杯放置区域（如茶几、餐桌）的视频，检测手部与水杯的接触动作（拿起、放下），统计每日水杯拿起次数（间接反映饮水量）。当每日拿起次数低于预设阈值（如每天少于6次）时，输出'脱水风险'提醒，建议家属或护理人员督促老人增加饮水。"
version: "1.0.3"
license: "MIT-0"
---

# 💧 Elderly Drinking-Cup Pickup Frequency (Dehydration Risk) | 老年人饮水杯拿起频率（脱水风险）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **老年人饮水杯拿起频率（脱水风险）** |
| 🎯 核心目标 | 通过客厅或厨房固定摄像头，分析水杯放置区域（如茶几、餐桌）的视频，检测手部与水杯的接触动作（拿起、放下），统计每日水杯拿起次数（间接反映饮水量）。当每日拿起次数低于预设阈值（如每天少于6次）时，输出'脱水风险'提醒，建议家属或护理人员督促老人增加饮水。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_ELDERLY_DRINKING_FREQUENCY_ANALYSIS` |

Using a fixed camera in the living room or kitchen, the system analyzes video of the water-cup placement area (e.g., coffee table, dining table), detects hand-to-cup contact actions (pickup, putdown), and counts daily cup-pickup events (an indirect proxy for water intake). When the daily pickup count falls below a preset threshold (e.g., fewer than 6 times per day), it outputs a 'dehydration risk' alert and suggests family members or caregivers to encourage the elderly to drink more. The skill helps prevent dehydration, urinary tract infection and cognitive decline caused by insufficient water intake. Application scenarios: homes of elderly people living alone, nursing homes, daycare centers. The system generates a daily drinking report; when the count is insufficient, it pushes a mobile-app reminder. Skill features: elderly people often have a dulled thirst sensation and are prone to chronic dehydration, leading to constipation, urinary tract infection, cognitive issues, etc. AI auto-counting of cup pickups helps family members spot insufficient intake in time and intervene. Can be integrated into home-care cameras or community health-management platforms as a practical feature for elderly health protection.

通过客厅或厨房固定摄像头，分析水杯放置区域（如茶几、餐桌）的视频，检测手部与水杯的接触动作（拿起、放下），统计每日水杯拿起次数（间接反映饮水量）。当每日拿起次数低于预设阈值（如每天少于6次）时，输出'脱水风险'提醒，建议家属或护理人员督促老人增加饮水。该技能有助于预防因饮水不足导致的脱水、泌尿系感染及认知功能下降。应用场景：独居老人家庭、养老院、日间照料中心。系统每日生成饮水统计报告，当次数不足时通过手机APP推送提醒。技能特点：老年人对口渴感知迟钝，易发生慢性脱水，导致便秘、尿路感染、认知障碍等问题。通过AI自动统计饮水杯拿起次数，可帮助家属及时发现饮水不足，采取干预措施。该技能可集成到居家养老摄像头或社区健康管理平台中，成为老年人健康守护的实用功能。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的老年人健康护理 AI。你的任务是分析固定摄像头对准水杯区域的视频，检测手部与水杯的接触动作（拿起和放下），统计每天的水杯拿起次数。当次数低于预设阈值时，输出脱水风险提醒。不要提供医疗诊断，仅输出基于视觉的饮水行为统计与方向性提醒。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于客厅/厨房固定摄像头视频，检测手-杯接触事件 + 抬手到口部动作 → 统计当日拿起次数与饮水频率 → 对比个人基线 → 输出脱水风险提醒（供家属/护理员主动督促老人饮水）

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 人体检测 |
| 2 | 手部检测 |
| 3 | 杯子检测 |
| 4 | 水杯放置 ROI 定义 |
| 5 | 手-杯接触事件识别（拿起/放下） |
| 6 | 伴随饮水手势识别（抬手到口部） |
| 7 | 当日拿起次数与时段分布统计 |
| 8 | 相邻饮水间隔 |
| 9 | 长时间未饮水检测（默认 > 4 小时） |
| 10 | 个人历史基线统计 |
| 11 | 风险类型分类（low_daily_intake / long_no_drink_interval / below_personal_baseline / normal） |
| 12 | 家属/护理员提醒文本生成 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供客厅/厨房水杯区域视频 URL 或文件需要分析时，默认触发本技能进行饮水频率（脱水风险）分析 |
| 🔎 明确分析意图 | 当用户明确提及老人饮水、脱水风险、慢性脱水、便秘、尿路感染、认知障碍预警、独居老人健康、督促饮水、养老护理等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看老人饮水历史报告、脱水风险报告清单、饮水频率报告清单、查询历史饮水记录、显示所有老人饮水报告、显示养老护理诊断报告，查询脱水风险预警清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_elderly_drinking_frequency_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_elderly_drinking_frequency_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备客厅/厨房水杯区域视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行老年人饮水频率（脱水风险）分析 | 调用 `-m scripts.smyx_elderly_drinking_frequency_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地客厅/厨房水杯区域视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络客厅/厨房水杯区域视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，老年人健康护理场景默认 `other` | 按需填写 |
| `--list` | 显示老年人饮水频率（脱水风险）历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_elderly_drinking_frequency_analysis.py`](scripts/smyx_elderly_drinking_frequency_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：画面必须稳定覆盖水杯放置区域 |
| 🔎 使用提醒 | **拿起次数仅作为饮水频率的间接代理**，杯里是否装水、是不是真的喝下去、是不是别人拿的杯子，本工具无法 100% 判定；建议结合饮水手势 + 个人基线 + 家属沟通综合判断 |
| 🔎 使用提醒 | 多人共用水杯、家中有客人 / 看护人员、老人在他人家或外出，会显著影响计数准确性 |
| 🔏 隐私合规 | 隐私合规：家庭/养老机构视频涉及个人隐私，使用前需取得老人/监护人明确知情同意，妥善加密保管；建议优先采用人体轮廓+物体框模式 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地客厅/厨房水杯区域视频
python -m scripts.smyx_elderly_drinking_frequency_analysis --input /path/to/livingroom_day.mp4

# 分析网络客厅/厨房水杯区域视频
python -m scripts.smyx_elderly_drinking_frequency_analysis --url https://example.com/livingroom_day.mp4

# 显示历史老人饮水频率（脱水风险）报告（自动触发关键词：查看老人饮水历史报告、脱水风险报告清单等）
python -m scripts.smyx_elderly_drinking_frequency_analysis --list

# 输出精简报告
python -m scripts.smyx_elderly_drinking_frequency_analysis --input day.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_elderly_drinking_frequency_analysis --input day.mp4 --output result.json
```
