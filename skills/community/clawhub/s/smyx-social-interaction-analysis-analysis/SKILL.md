---
name: "smyx-social-interaction-analysis-analysis"
description: "AI-powered pet social interaction analysis for multi-pet households. Uses pose recognition and behavior classification to detect cat-cat, dog-dog, and cat-dog interactions—sniffing, chasing, biting, fleeing, hiding, playing—then records duration, frequency, initiator and receiver to generate a social-behavior report. Helps owners understand pet relationships, spot aggression or stress sources, and promote harmonious cohabitation. Scenarios: multi-pet homes, pet boarding centers, pet daycare, animal behavior clinics. | 通过多宠家庭固定摄像头，分析宠物之间（猫-猫、狗-狗、猫-狗等）的互动视频，利用姿态识别和行为分类模型检测嗅闻、追逐、撕咬、逃跑、躲避、玩耍等行为类型，记录每种行为的持续时间、频次以及发起者，生成社交行为报告。帮助主人了解宠物间的社交关系，识别潜在的攻击行为或压力源，促进多宠和谐共处。应用场景：多宠家庭（多猫/多狗/猫狗混养）、宠物寄养中心、宠物日托班、宠物行为诊所。"
version: "1.0.12"
license: "MIT-0"
---

# 🐾 Pet Social Interaction Analysis | 宠物社交行为分析（与其他宠物互动）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **宠物社交行为分析（与其他宠物互动）** |
| 🎯 核心目标 | 通过多宠家庭固定摄像头，分析宠物之间（猫-猫、狗-狗、猫-狗等）的互动视频，利用姿态识别和行为分类模型检测嗅闻、追逐、撕咬、逃跑、躲避、玩耍等行为类型，记录每种行为的持续时间、频次以及发起者，生成社交行为报告。帮助主人了解宠物间的社交关系，识别潜在的攻击行为或压力源，促进多宠和谐共处。应用场景：多宠家庭（多猫/多狗/猫狗混养）、宠物寄养中心、宠物日托班、宠物行为诊所。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_SOCIAL_INTERACTION_ANALYSIS_ANALYSIS` |

AI-powered pet social interaction analysis for multi-pet households. Uses pose recognition and behavior classification to detect cat-cat, dog-dog, and cat-dog interactions—sniffing, chasing, biting, fleeing, hiding, playing—then records duration, frequency, initiator and receiver to generate a social-behavior report. Helps owners understand pet relationships, spot aggression or stress sources, and promote harmonious cohabitation. Scenarios: multi-pet homes, pet boarding centers, pet daycare, animal behavior clinics.

通过多宠家庭固定摄像头，分析宠物之间（猫-猫、狗-狗、猫-狗等）的互动视频，利用姿态识别和行为分类模型检测嗅闻、追逐、撕咬、逃跑、躲避、玩耍等行为类型，记录每种行为的持续时间、频次以及发起者，生成社交行为报告。帮助主人了解宠物间的社交关系，识别潜在的攻击行为或压力源，促进多宠和谐共处。应用场景：多宠家庭（多猫/多狗/猫狗混养）、宠物寄养中心、宠物日托班、宠物行为诊所。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的宠物行为学AI。你的任务是分析多宠家庭固定摄像头的视频，识别宠物之间的互动行为类型（嗅闻、追逐、撕咬、逃跑、躲避、玩耍等），记录每种行为的持续时间、频次、发起者和接收者，输出社交行为报告。不要提供医疗或训练建议，仅输出基于视觉的行为观察结果。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

通过多宠互动视频进行社交行为识别与量化，记录互动类型、参与者、持续时间和频次，输出社交关系报告

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 多宠个体识别与追踪 |
| 2 | 姿态识别 |
| 3 | 社交行为分类（友好/中性/对抗） |
| 4 | 发起者-接收者关系标注 |
| 5 | 互动时长与频次统计 |
| 6 | 社交关系评估 |
| 7 | 潜在冲突预警 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供多宠互动视频需要分析时，默认触发本技能进行社交行为分析 |
| 🔎 明确分析意图 | 当用户明确需要多宠社交评估时，提及多猫、多狗、猫狗混养、宠物打架、追逐、霸凌、互动等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史社交报告、历史互动报告、社交行为报告清单、显示所有社交报告、查询互动记录 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_social_interaction_analysis_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_social_interaction_analysis_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 3 | ⚙️ 执行社交行为分析 | 调用 `-m scripts.smyx_social_interaction_analysis_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地多宠互动视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络多宠互动视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 宠物类型，可选值：cat/dog/other，默认 cat | 按需填写 |
| `--list` | 显示社交行为分析历史报告列表清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🐾 互动行为分类体系

### 友好行为 🟢

| 行为 | 特征描述 | 社交含义 |
|------|----------|----------|
| 嗅闻 | 互相嗅闻头部/尾部/身体 | 正常社交问候、信息交换 |
| 蹭头/摩擦 | 头部或身体主动蹭对方 | 亲昵标记、信任表达 |
| 依偎/靠拢 | 身体贴近躺卧或坐在一起 | 亲密关系、安全感 |
| 互相舔毛 | 一方主动舔舐另一方 | 社交联结、等级关系 |
| 玩耍互动 | 交替追逐、扑咬（无攻击性） | 友好社交、精力释放 |

### 中性行为 🟡

| 行为 | 特征描述 | 社交含义 |
|------|----------|----------|
| 平行活动 | 同空间各自活动，无直接互动 | 共存但不亲密 |
| 旁观 | 一方注视另一方但未参与 | 好奇或评估 |
| 绕行 | 一方绕开另一方行走 | 避免冲突的礼貌行为 |
| 资源共享 | 同时使用食盆/猫砂盆但无争抢 | 关系可接受 |

### 对抗行为 🔴

| 行为 | 特征描述 | 社交含义 |
|------|----------|----------|
| 追逐 | 一方持续追赶另一方（非玩耍） | 霸凌、领地驱赶 |
| 撕咬/攻击 | 带攻击意图的扑咬、拍打 | 直接攻击，需干预 |
| 威胁姿态 | 哈气、弓背、低吼、露齿 | 警告、防御 |
| 逃跑 | 一方快速逃离另一方 | 恐惧、被霸凌 |
| 躲避 | 一方长期躲在角落/高处 | 持续受压、缺乏安全感 |

## 🚨 冲突预警分级

| 等级 | 触发条件 | 建议 |
|------|----------|------|
| 🟢 和谐 | 友好行为 > 70%，对抗 < 10% | 社交关系良好，维持现状 |
| 🟡 轻度紧张 | 对抗 10%-25%，偶有追逐 | 增加资源（食盆/猫砂盆/休息区），观察趋势 |
| 🟠 明显冲突 | 对抗 25%-50%，某方持续被追 | 建议增加垂直空间/隔离区，考虑行为咨询 |
| 🔴 严重霸凌 | 对抗 > 50%，某方长期躲避 | ⚠️ 建议立即隔离，寻求专业行为矫正 |

## 💡 多宠家庭环境优化建议参考

| 问题 | 可能原因 | 环境调整方向 |
|------|----------|--------------|
| 食盆争抢 | 资源不足 | 增加食盆数量，分散放置 |
| 猫砂盆冲突 | 猫砂盆太少 | N+1 原则（猫数量+1个砂盆） |
| 追逐/驱赶 | 领地不足 | 增加垂直空间（猫爬架/高架） |
| 躲避不出 | 缺乏安全区 | 设置专属躲避窝/高台 |
| 狗追猫 | 狩猎本能 | 猫狗分离活动区，设置猫专属通道 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_social_interaction_analysis_analysis.py`](scripts/smyx_social_interaction_analysis_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 视频要求：支持 mp4/avi/mov 格式，最大 10MB；建议时长 ≥ 1 分钟 |
| 🔎 使用提醒 | **画面中需同时包含多只宠物**，单只宠物视频无法进行互动分析 |
| 🔎 使用提醒 | 摄像头需固定，视角覆盖宠物主要活动区域；移动拍摄可能影响个体追踪与行为识别 |
| 🧑‍⚖️ 结果性质 | **分析结果仅供行为观察参考，不提供医疗或训练建议**；严重冲突建议咨询专业行为师 |
| 🔎 使用提醒 | 玩耍与攻击行为在视觉上存在一定重叠（如玩耍中的扑咬），需结合频次、持续时间和双方反应综合判断 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地多宠互动视频
python -m scripts.smyx_social_interaction_analysis_analysis --input /path/to/multi_pet.mp4 --pet-type cat

# 分析网络多宠互动视频
python -m scripts.smyx_social_interaction_analysis_analysis --url https://example.com/multi_pet.mp4 --pet-type dog

# 显示历史分析报告/显示报告清单列表（自动触发关键词：查看历史社交报告、互动报告清单等）
python -m scripts.smyx_social_interaction_analysis_analysis --list

# 输出精简报告
python -m scripts.smyx_social_interaction_analysis_analysis --input video.mp4 --pet-type cat --detail basic

# 保存结果到文件
python -m scripts.smyx_social_interaction_analysis_analysis --input video.mp4 --pet-type cat --output result.json
```
