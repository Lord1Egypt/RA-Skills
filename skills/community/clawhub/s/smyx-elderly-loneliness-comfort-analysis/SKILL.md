---
name: "smyx-elderly-loneliness-comfort-analysis"
description: "Using a fixed camera in the home of a solitary-living elderly person or in a private nursing-home room, the system analyzes daily activity video and detects loneliness-related behaviors: prolonged solitude (no social interaction), static gazing (long-time fixation with no purposeful activity), sighing (rapid chest/abdomen rise-fall with exhale), and talking-to-self (mouth activity with no conversation partner). | 通过独居老人家中或养老院单人房的固定摄像头，分析老人日常行为视频，检测孤独相关行为：长时间独处（无社交互动）、静止发呆（长时间凝视一处无目的活动）、叹气（胸腹快速起伏伴呼气）、自言自语（口部活动但无对话对象）等。"
version: "1.0.2"
license: "MIT-0"
---

# 🤗 Elderly Loneliness Detection & Warm Companionship | 独居老人孤独情绪识别与温暖陪伴
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **独居老人孤独情绪识别与温暖陪伴** |
| 🎯 核心目标 | 通过独居老人家中或养老院单人房的固定摄像头，分析老人日常行为视频，检测孤独相关行为：长时间独处（无社交互动）、静止发呆（长时间凝视一处无目的活动）、叹气（胸腹快速起伏伴呼气）、自言自语（口部活动但无对话对象）等。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_ELDERLY_LONELINESS_COMFORT_ANALYSIS` |

Using a fixed camera in the home of a solitary-living elderly person or in a private nursing-home room, the system analyzes daily activity video and detects loneliness-related behaviors: prolonged solitude (no social interaction), static gazing (long-time fixation with no purposeful activity), sighing (rapid chest/abdomen rise-fall with exhale), and talking-to-self (mouth activity with no conversation partner). It computes a composite loneliness index (0-100). When the index exceeds a threshold, warm-companionship actions are automatically triggered: playing pre-recorded warm voice messages from children via smart speakers, playing the elder's favorite old songs, or pushing reminders to the children's mobile app (e.g., 'Dad seems lonely today — a video call is recommended'). The skill aims to relieve loneliness and improve mental well-being. Application scenarios: homes of solitary-living elderly, private nursing-home rooms, community day-care centers. The system monitors in real time and intervenes proactively when the loneliness index exceeds threshold. Skill features: chronic loneliness is a major risk factor for depression and cognitive decline in older adults. AI auto-identification of loneliness signals followed by timely voice care or reminders to children can effectively alleviate negative emotions and improve quality of life. Can be integrated into smart cameras or elderly-care service platforms as a key emotional-support feature of 'smart aging'.

通过独居老人家中或养老院单人房的固定摄像头，分析老人日常行为视频，检测孤独相关行为：长时间独处（无社交互动）、静止发呆（长时间凝视一处无目的活动）、叹气（胸腹快速起伏伴呼气）、自言自语（口部活动但无对话对象）等。综合计算孤独指数（0-100），当指数超过阈值时自动触发温暖陪伴动作：通过智能音箱播放子女预录的温馨语音、播放老人喜爱老歌、或向子女手机APP推送提醒（'父亲今天显得孤独，建议视频通话'）。该技能旨在缓解老人孤独感，提升心理健康。应用场景：独居老人家庭、养老院单人房、社区日间照料中心。系统实时监测，当孤独指数超标时主动干预。技能特点：长期孤独是老年人抑郁、认知下降的重要风险因素。通过AI自动识别孤独信号并及时给予语音关怀或提醒子女，可有效缓解老人负面情绪，提升生活质量。该技能可集成到智能摄像头或养老服务平台中，成为'智慧养老'情感支持的关键功能。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的老年人心理健康关怀 AI。你的任务是分析独居老人活动区域的固定摄像头视频（可选叠加音频），检测孤独相关行为：连续独处时长（无他人进入画面）、长时间静止凝视（≥ 10 分钟无肢体活动）、叹气次数（视觉胸腹起伏+长呼气，音频可补强）、自言自语频次（口部活动但无对话对象）。综合计算孤独指数（0-100，含哼歌/电话通话等正向行为扣分项），当超过阈值时输出温暖陪伴动作建议：智能音箱播放子女预录温馨语音、播放老人喜爱老歌、子女 APP 推送提醒。不提供任何医疗诊断，仅输出基于行为统计的结果，并尊重老人"一句话关闭今日提醒"的意愿。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于独居老人家中/养老院单人房固定摄像头（可选音频）视频，识别孤独相关行为（连续独处时长 / 当日累计独处 / 长时间静止凝视 / 视觉+音频叹气 / 自言自语 / 皱眉木然面部比例）+ 正向行为（笑容 / 哼歌 / 电话通话）→ 综合计算 **孤独指数（0-100，含正向扣分）** + 14 天个人基线对比 → 输出 4 档孤独等级（light / mild / notable / heavy）+ 4 类温暖陪伴动作建议（智能音箱子女语音 / 老歌播放 / 子女 APP 推送 / 社区日间照料推荐）+ 给子女的友好摘要

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 人体姿态识别（独处/静止/凝视判定） |
| 2 | 独居判定（≥ 30 分钟仅老人一人） |
| 3 | 视觉叹气识别（胸腹起伏+长呼气姿态） |
| 4 | 自言自语识别（口部活动+无对话对象在场） |
| 5 | 笑容识别 |
| 6 | 哼歌/唱歌识别（可选音频） |
| 7 | 电话/视频通话识别 |
| 8 | 社交互动事件识别（家人/护工进入 |
| 9 | 视频通话画面 |
| 10 | 宠物互动） |
| 11 | 目的性活动判别（家务/看电视+点头反馈/园艺/阅读） |
| 12 | 孤独指数 0-100 综合算法 |
| 13 | 14 天个人基线对比 |
| 14 | 4 档孤独等级 |
| 15 | 温和前导（"今天为您播放……" 3 秒）+ 老人一句话关闭意愿支持 |
| 16 | 子女预录语音播放（**禁止 AI 克隆声音**） |
| 17 | heavy 且子女长期无回应时推送社区/街道老龄办资源 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供独居老人家中/养老院单人房固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行独居老人孤独情绪识别与温暖陪伴 |
| 🔎 明确分析意图 | 当用户明确提及独居老人、孤独、空巢、子女陪伴、老人发呆、老人唉声叹气、智能音箱关怀、智慧养老、社区日间照料等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看独居老人孤独历史报告、子女关怀日报清单、老人情感关怀报告清单、查询历史孤独情绪记录、显示所有独居老人陪伴报告、显示老人情绪关怀报告，查询孤独情绪预警清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_elderly_loneliness_comfort_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_elderly_loneliness_comfort_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备独居老人客厅/卧室/养老院单人房固定摄像头视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行独居老人孤独情绪识别与温暖陪伴 | 调用 `-m scripts.smyx_elderly_loneliness_comfort_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地独居老人客厅/卧室/养老院单人房固定摄像头视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络独居老人客厅/卧室/养老院单人房固定摄像头视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，老年人心理健康关怀场景默认 `other` | 按需填写 |
| `--list` | 显示独居老人孤独情绪识别与温暖陪伴历史报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_elderly_loneliness_comfort_analysis.py`](scripts/smyx_elderly_loneliness_comfort_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：覆盖老人主要活动区域；时长建议 ≥ 4 小时 |
| 🔎 使用提醒 | 哼歌/唱歌、电话视频通话、笑容等正向行为**必须**作为负权重纳入孤独指数计算，避免一刀切定义"独处=孤独" |
| 🔎 使用提醒 | 老人午睡、看自己喜欢的电视节目并有积极面部反馈 等不应误判为"静止凝视"或孤独 |
| 🧑‍⚖️ 结果性质 | 红线约束：**禁止**输出"老年抑郁症 / 孤独症"等精神医学诊断或量表评分；**禁止**未经老人与子女双方同意便部署；**禁止**将老人视频/音频用于商业广告或大数据画像；**禁止**长期存储原始视频（≤ 7 天，仅留聚合指标） |
| 📁 格式支持 | **必须**：智能音箱发声前给予 3 秒温和前导（如"今天为您播放……"）；支持老人一句话关闭今日提醒 |
| 🔎 使用提醒 | **绝对禁止**使用 AI 克隆/合成子女声音冒充子女语音；子女预录语音必须由子女本人录制 |
| 🔎 使用提醒 | 当 heavy 且子女连续 ≥ 3 天无回应时，主动提示**社区/街道老龄办**资源 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地老人活动区域视频
python -m scripts.smyx_elderly_loneliness_comfort_analysis --input /path/to/livingroom.mp4

# 分析网络老人活动区域视频
python -m scripts.smyx_elderly_loneliness_comfort_analysis --url https://example.com/livingroom.mp4

# 显示历史独居老人孤独关怀报告（自动触发关键词：查看独居老人孤独历史报告、子女关怀日报清单等）
python -m scripts.smyx_elderly_loneliness_comfort_analysis --list

# 输出精简报告
python -m scripts.smyx_elderly_loneliness_comfort_analysis --input lr.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_elderly_loneliness_comfort_analysis --input lr.mp4 --output result.json
```
