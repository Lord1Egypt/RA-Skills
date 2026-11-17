---
name: "smyx-vomiting-regurgitation-detection-analysis"
description: "AI-powered pet vomiting and regurgitation detection from indoor fixed-camera video. Identifies rhythmic abdominal contractions, head-forward extension, and mouth opening actions, plus detects vomitus on the floor (food, hairball, bile). Records event time, frequency, and vomitus characteristics for early digestive issue discovery. Scenarios: daily home health monitoring, multi-pet households, senior pet care, animal hospital inpatient observation. | 通过室内固定摄像头分析宠物活动区域的连续视频，利用动作识别技术检测宠物的呕吐或反流行为（包括腹部节律性收缩、口部张合、头部前伸等典型动作），同时识别地面是否出现呕吐物（食物残渣、毛球、黄色胆汁等），记录发生时间、频次以及呕吐物特征。有助于主人及早发现宠物的消化系统问题，避免延误治疗。应用场景：宠物家庭日常健康监护、多宠家庭、老年宠物护理、宠物医院住院观察。"
version: "1.0.22"
license: "MIT-0"
---

# 🤢 Pet Vomiting / Regurgitation Detection | 宠物呕吐/反流行为识别
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **宠物呕吐/反流行为识别** |
| 🎯 核心目标 | 通过室内固定摄像头分析宠物活动区域的连续视频，利用动作识别技术检测宠物的呕吐或反流行为（包括腹部节律性收缩、口部张合、头部前伸等典型动作），同时识别地面是否出现呕吐物（食物残渣、毛球、黄色胆汁等），记录发生时间、频次以及呕吐物特征。有助于主人及早发现宠物的消化系统问题，避免延误治疗。应用场景：宠物家庭日常健康监护、多宠家庭、老年宠物护理、宠物医院住院观察。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_VOMITING_REGURGITATION_DETECTION_ANALYSIS` |

AI-powered pet vomiting and regurgitation detection from indoor fixed-camera video. Identifies rhythmic abdominal contractions, head-forward extension, and mouth opening actions, plus detects vomitus on the floor (food, hairball, bile). Records event time, frequency, and vomitus characteristics for early digestive issue discovery. Scenarios: daily home health monitoring, multi-pet households, senior pet care, animal hospital inpatient observation.

通过室内固定摄像头分析宠物活动区域的连续视频，利用动作识别技术检测宠物的呕吐或反流行为（包括腹部节律性收缩、口部张合、头部前伸等典型动作），同时识别地面是否出现呕吐物（食物残渣、毛球、黄色胆汁等），记录发生时间、频次以及呕吐物特征。有助于主人及早发现宠物的消化系统问题，避免延误治疗。应用场景：宠物家庭日常健康监护、多宠家庭、老年宠物护理、宠物医院住院观察。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的宠物消化健康AI。你的任务是分析室内固定摄像头的连续视频，检测宠物是否发生呕吐或反流行为，识别呕吐动作特征以及地面呕吐物出现情况，记录事件发生时间和频次。不要提供医疗诊断，仅输出基于视觉的行为观察结果。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

通过室内摄像头视频进行宠物呕吐/反流行为检测，识别典型呕吐动作和地面呕吐物，记录事件时间、频次和呕吐物特征

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 呕吐动作识别（腹部收缩 |
| 2 | 头部前伸 |
| 3 | 口部张合） |
| 4 | 反流行为区分 |
| 5 | 地面呕吐物检测与分类 |
| 6 | 事件时间戳记录 |
| 7 | 频次统计 |
| 8 | 呕吐物特征描述 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供宠物活动区域视频需要分析时，默认触发本技能进行呕吐/反流行为识别 |
| 🔎 明确分析意图 | 当用户明确需要呕吐监测时，提及呕吐、吐毛球、反流、干呕、消化异常等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史呕吐报告、历史呕吐监测报告、呕吐行为报告清单、显示所有呕吐报告、查询呕吐事件记录 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_vomiting_regurgitation_detection_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_vomiting_regurgitation_detection_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 3 | ⚙️ 执行呕吐/反流行为识别 | 调用 `-m scripts.smyx_vomiting_regurgitation_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看识别结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地宠物活动区域视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络宠物活动区域视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 宠物类型，可选值：cat/dog/other，默认 cat | 按需填写 |
| `--list` | 显示呕吐/反流行为识别历史报告列表清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🤢 呕吐 vs 反流：关键区别

| 特征 | 呕吐（Vomiting） | 反流（Regurgitation） |
|------|------------------|----------------------|
| 触发机制 | 主动，涉及腹部强烈收缩 | 被动，无明显腹部用力 |
| 动作特征 | 干呕→腹部节律收缩→头部前伸→排出 | 食管被动排出，动作较轻 |
| 排出物 | 部分消化食物、胆汁、泡沫 | 未消化食物、黏液 |
| 时间 | 可在进食后数小时 | 通常在进食后不久 |
| 常见原因 | 胃肠炎、中毒、胰腺炎、毛球 | 食管扩张、食管异物 |

> **区分意义**：呕吐和反流涉及不同疾病方向，准确区分有助于兽医初步判断。

## 🟡 呕吐物类型与可能提示

| 呕吐物类型 | 外观特征 | 可能原因 |
|------------|----------|----------|
| 🐛 毛球 | 圆柱形，主要为毛发 | 猫咪正常排毛球；频繁则需关注 |
| 🍖 食物残渣 | 可辨认的未消化食物 | 进食过快、食物不耐受 |
| 💛 黄色胆汁 | 黄色液体，空腹常见 | 空腹呕吐、胆汁性呕吐综合征 |
| 🤍 白色泡沫 | 白色黏稠泡沫 | 胃酸过多、空腹干呕 |
| 🔴 带血 | 红色或咖啡色 | ⚠️ 胃出血、溃疡、异物划伤，需立即就医 |
| 🟫 异物 | 含塑料、线绳等 | ⚠️ 误食异物，需立即就医 |

## 🚨 预警分级

| 等级 | 触发条件 | 建议 |
|------|----------|------|
| 🟢 偶发 | 24小时内 1 次，呕吐物为毛球或食物 | 观察，注意饮食和饮水量 |
| 🟡 频发 | 24小时内 2-3 次，或连续两天呕吐 | 建议预约兽医检查 |
| 🟠 严重 | 24小时内 ≥4 次，呕吐物含胆汁或泡沫 | 尽快就医，注意补充水分 |
| 🔴 危急 | 呕吐物带血，或伴精神萎靡/拒食 | ⚠️ 立即就医，警惕中毒、肠梗阻 |

## 💡 高风险群体关注

| 类别 | 重点关注原因 |
|------|--------------|
| 多宠家庭 | 难以及时发现哪个宠物呕吐，AI 可区分个体 |
| 老年宠物 | 慢性肾病、肿瘤等可表现为频繁呕吐 |
| 幼宠 | 易误食异物，呕吐后脱水风险更高 |
| 长毛猫 | 毛球症高发，需定期梳毛辅助 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_vomiting_regurgitation_detection_analysis.py`](scripts/smyx_vomiting_regurgitation_detection_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 视频要求：支持 mp4/avi/mov 格式，最大 10MB；建议时长 ≥ 30 秒 |
| 🔎 使用提醒 | 摄像头需固定且视角覆盖宠物活动区域及地面，移动/手持拍摄可能影响检测效果 |
| 🧑‍⚖️ 结果性质 | **识别结果仅供行为观察参考，不提供医疗诊断**；频繁呕吐或呕吐物带血建议立即就医 |
| 🔎 使用提醒 | 宠物可能做出类似呕吐的伸懒腰、咳嗽等动作，存在一定误检可能，建议结合呕吐物确认 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载 |
| 📜 报告输出 | 当显示历史识别报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地宠物活动区域视频
python -m scripts.smyx_vomiting_regurgitation_detection_analysis --input /path/to/pet_room.mp4 --pet-type cat

# 分析网络宠物活动区域视频
python -m scripts.smyx_vomiting_regurgitation_detection_analysis --url https://example.com/pet_room.mp4 --pet-type cat

# 显示历史识别报告/显示报告清单列表（自动触发关键词：查看历史呕吐报告、呕吐报告清单等）
python -m scripts.smyx_vomiting_regurgitation_detection_analysis --list

# 输出精简报告
python -m scripts.smyx_vomiting_regurgitation_detection_analysis --input video.mp4 --pet-type cat --detail basic

# 保存结果到文件
python -m scripts.smyx_vomiting_regurgitation_detection_analysis --input video.mp4 --pet-type cat --output result.json
```
