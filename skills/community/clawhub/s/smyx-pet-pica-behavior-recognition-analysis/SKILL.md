---
name: "smyx-pet-pica-behavior-recognition-analysis"
description: "Triggers when a user provides an indoor camera video for analysis; supports local uploads or network URLs to call server-side APIs for pet pica-behavior recognition, detecting contact between the pet's mouth and non-food hazardous items (electric wires, plastic bags, socks, tissues, toy fragments, etc.); when the contact lasts ≥ 2 seconds, outputs a warning signal to help prevent intestinal obstruction, electric shock and other dangers (without diagnosing diseases). Application scenarios: indoor cameras, pet safety monitoring, smart-home security. | 当用户提供室内监控视频时，触发本技能进行异食行为识别；支持通过上传本地视频或网络视频URL，调用服务端API检测宠物嘴部与电线、塑料袋、袜子、纸巾、玩具碎片等非食物物品的接触动作；持续接触 ≥ 2 秒时输出预警信号，预防肠梗阻、触电等危险（不诊断疾病）。应用场景：室内摄像头、宠物安全监控、智能家居安防。"
version: "1.0.24"
license: "MIT-0"
---

# ⚠️ Pet Pica Behavior Recognition | 宠物异食行为识别（啃咬电线/塑料）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **宠物异食行为识别（啃咬电线/塑料）** |
| 🎯 核心目标 | 当用户提供室内监控视频时，触发本技能进行异食行为识别；支持通过上传本地视频或网络视频URL，调用服务端API检测宠物嘴部与电线、塑料袋、袜子、纸巾、玩具碎片等非食物物品的接触动作；持续接触 ≥ 2 秒时输出预警信号，预防肠梗阻、触电等危险（不诊断疾病）。应用场景：室内摄像头、宠物安全监控、智能家居安防。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_PET_PICA_BEHAVIOR_RECOGNITION_ANALYSIS` |

Triggers when a user provides an indoor camera video for analysis; supports local uploads or network URLs to call
server-side APIs for pet pica-behavior recognition, detecting contact between the pet's mouth and non-food hazardous
items (electric wires, plastic bags, socks, tissues, toy fragments, etc.); when the contact lasts ≥ 2 seconds, outputs a
warning signal to help prevent intestinal obstruction, electric shock and other dangers (without diagnosing diseases).
Application scenarios: indoor cameras, pet safety monitoring, smart-home security.

当用户提供室内监控视频时，触发本技能进行异食行为识别；支持通过上传本地视频或网络视频URL，调用服务端API检测宠物嘴部与电线、塑料袋、袜子、纸巾、玩具碎片等非食物物品的接触动作；持续接触 ≥
2 秒时输出预警信号，预防肠梗阻、触电等危险（不诊断疾病）。应用场景：室内摄像头、宠物安全监控、智能家居安防。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **你是一个专业的宠物安全监测AI。你的任务是基于室内环境的连续视频，检测宠物是否有啃咬或咀嚼非食物物品（如电线、塑料制品、袜子、纸巾、玩具碎片等）的行为。当检测到宠物嘴部与危险物品接触并持续超过 2 秒时，输出预警信号。不要提供疾病诊断，仅客观描述行为和风险等级。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

通过室内监控视频识别宠物异食行为（嘴部与危险物品接触），持续 ≥ 2 秒时输出预警，预防肠梗阻、触电、中毒等危险

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 视频分析 |
| 2 | 宠物嘴部定位 |
| 3 | 危险物品识别（电线/塑料/袜子/纸巾/玩具碎片等） |
| 4 | 接触动作检测 |
| 5 | 持续时长统计（秒） |
| 6 | 风险等级判定 |
| 7 | 预警信号输出 |
| 8 | 外部干预建议（声光劝阻 / |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供室内监控视频 URL 或文件需要分析时，默认触发本技能进行异食行为识别 |
| 🔎 明确分析意图 | 当用户明确需要进行宠物安全监控时，提及啃电线、咬塑料、吞袜子、误食、肠梗阻、触电、宠物乱咬、异食癖、宠物安全监控等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史异食报告、历史误食预警报告、异食行为报告清单、查询误食记录、显示所有宠物安全报告、显示异食识别报告，查询宠物安全风险提示报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_pet_pica_behavior_recognition_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_pet_pica_behavior_recognition_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行异食行为识别分析 | 调用 `-m scripts.smyx_pet_pica_behavior_recognition_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 宠物类型，可选值：cat/dog/other，默认 dog | 按需填写 |
| `--list` | 显示异食行为识别历史分析报告列表清单（可输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 危险物品 & 风险等级参考

| 风险等级  | 物品示例                            | 危险类型            | 默认接触阈值 | 建议干预                 |
|-------|---------------------------------|-----------------|--------|----------------------|
| 🚨 紧急 | 通电电线 / 充电中数据线 / 化学清洁剂瓶 / 药品     | 触电 / 烧伤 / 中毒    | ≥ 1 秒  | 立即声光劝阻 + 推送主人 + 紧急联系 |
| ⚠️ 高  | 塑料袋 / 袜子 / 内衣 / 橡皮筋 / 发圈 / 玩具碎片 | 窒息 / 肠梗阻 / 线性异物 | ≥ 2 秒  | 声光劝阻 + 推送告警          |
| ⚠️ 中  | 纸巾 / 厕纸 / 包装盒纸片                 | 消化道堵塞           | ≥ 3 秒  | 声音温和提醒 + 记录          |
| ℹ️ 关注 | 自身玩具 / 磨牙棒                      | 正常啃咬            | —      | 无需干预                 |

> 注：以上参考标准仅供视觉判定参考，最终判定以 API 输出结果为准。幼宠、好奇心强的猎犬种（拉布拉多、金毛、比格等）天然异食风险更高，需更频繁监测。

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_pet_pica_behavior_recognition_analysis.py`](scripts/smyx_pet_pica_behavior_recognition_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 视频要求：支持 mp4/avi/mov 格式，最大 10MB |
| 🧑‍⚖️ 结果性质 | 推荐结果仅供安全监测参考，不提供疾病诊断 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载 |
| 🔎 使用提醒 | 预警信号由智能家居安防设备（智能音箱 / 宠物摄像头）基于本技能输出结果触发，本技能仅负责输出干预建议 |
| 🔎 使用提醒 | 幼宠、好奇心强的猎犬种（拉布拉多、金毛、比格等）天然异食风险更高，AI 角色在输出时需主动提醒 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 `` 作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地室内监控视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_pet_pica_behavior_recognition_analysis --input /path/to/indoor_video.mp4 --pet-type dog

# 分析网络室内监控视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_pet_pica_behavior_recognition_analysis --url https://example.com/indoor_video.mp4 --pet-type dog

# 显示历史分析报告清单（自动触发关键词：查看历史异食报告、误食预警报告清单等）
python -m scripts.smyx_pet_pica_behavior_recognition_analysis --list

# 输出精简报告
python -m scripts.smyx_pet_pica_behavior_recognition_analysis --input indoor_video.mp4 --pet-type dog --detail basic

# 保存结果到文件
python -m scripts.smyx_pet_pica_behavior_recognition_analysis --input indoor_video.mp4 --pet-type dog --output result.json
```
