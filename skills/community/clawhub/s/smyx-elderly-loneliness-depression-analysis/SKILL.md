---
name: "smyx-elderly-loneliness-depression-analysis"
description: "Using fixed cameras at home (living room, bedroom) of elderly people living alone, the system analyzes daily videos and detects negative behavior indicators during solo time: dazing (long-duration motionless gazing without purposeful action), sighing (rapid chest rise-and-fall with audible expiration), and self-talking (mouth movement without any conversation partner). | 通过独居老人在家中的固定摄像头（如客厅、卧室），分析日常视频，检测独处期间的消极行为指标：发呆（长时间静止注视，缺乏目的性动作）、叹气（胸部快速起伏伴呼气声）、自言自语（口部活动但无对话对象）等。该技能可辅助家属或社区工作者了解老人心理状态，及时进行情感关怀或心理干预。"
version: "1.0.11"
license: "MIT-0"
---

# 🧓 Elderly Loneliness / Depression-Tendency Behavior Analysis | 老年人孤独/抑郁倾向行为分析
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **老年人孤独/抑郁倾向行为分析** |
| 🎯 核心目标 | 通过独居老人在家中的固定摄像头（如客厅、卧室），分析日常视频，检测独处期间的消极行为指标：发呆（长时间静止注视，缺乏目的性动作）、叹气（胸部快速起伏伴呼气声）、自言自语（口部活动但无对话对象）等。该技能可辅助家属或社区工作者了解老人心理状态，及时进行情感关怀或心理干预。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_ELDERLY_LONELINESS_DEPRESSION_ANALYSIS` |

Using fixed cameras at home (living room, bedroom) of elderly people living alone, the system analyzes daily videos and detects negative behavior indicators during solo time: dazing (long-duration motionless gazing without purposeful action), sighing (rapid chest rise-and-fall with audible expiration), and self-talking (mouth movement without any conversation partner). It counts the frequency and duration of these behaviors and comprehensively evaluates the elder's emotional risk level (low / medium / high). The skill assists family members or community workers in understanding the elder's mental state and timely providing emotional care or psychological intervention. Application scenarios: homes of solo-living elders, nursing homes, community daycare centers. The system generates a daily emotional-risk report; when the risk level is 'medium' or 'high', it pushes reminders. Skill features: loneliness and depression in the elderly are common mental-health issues, and early behavioral signals are often overlooked. AI automatic monitoring of dazing / sighing / self-talking helps family members detect mental abnormalities early, intervene promptly, and improve the elder's quality of life. Can be integrated into home-care cameras or community health-management platforms.

通过独居老人在家中的固定摄像头（如客厅、卧室），分析日常视频，检测独处期间的消极行为指标：发呆（长时间静止注视，缺乏目的性动作）、叹气（胸部快速起伏伴呼气声）、自言自语（口部活动但无对话对象）等。统计这些行为的发生频次和持续时间，综合评估老年人潜在的情绪风险等级（低/中/高）。该技能可辅助家属或社区工作者了解老人心理状态，及时进行情感关怀或心理干预。应用场景：独居老人家庭、养老院、社区日间照料中心。系统每日生成情绪风险报告，当风险等级为'中'或'高'时推送提醒。技能特点：老年人孤独和抑郁是常见的心理健康问题，早期行为信号常被忽视。通过AI自动监测发呆、叹气、自言自语等行为，可辅助家属及早发现心理异常，及时干预，提高老年人生活质量。该技能可集成到居家养老摄像头或社区健康管理平台中。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的老年人心理健康监测 AI。你的任务是分析固定摄像头拍摄的日常视频，检测老年人在独处期间的特定行为：发呆（连续注视某处超过 10 秒且无肢体活动）、叹气（胸腹部快速起伏伴呼吸音）、自言自语（口部开合但无对话对象）。统计这些行为的发生频次和持续时间，综合评估情绪风险等级。不要提供医疗诊断或心理量表评分，仅输出基于视觉和行为统计的风险提示。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于独居老人客厅/卧室固定摄像头视频（可选麦克风），识别独处期间的消极行为指标 → 统计频次/累计时长 → 与个人基线对比 → 综合输出情绪风险等级（低/中/高）+ 友好提醒

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 人体检测与独处时间窗口判定（画面中仅有老人本人） |
| 2 | 发呆事件识别（连续静止注视 ≥ 10s 且无肢体活动） |
| 3 | 叹气事件识别（胸腹快速起伏 + 可选呼气声） |
| 4 | 自言自语识别（口部活动 + 无对话对象 + 可选低音量语音） |
| 5 | 社交互动时长统计（反向指标） |
| 6 | 卧床时长（参考指标） |
| 7 | 与个人 7-14 天基线对比 |
| 8 | 连续异常天数累计 |
| 9 | 风险等级综合判定 |
| 10 | 家属/社工友好提醒文本生成 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供独居老人活动区域固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行孤独/抑郁倾向行为分析 |
| 🔎 明确分析意图 | 当用户明确提及老年人孤独、独居老人抑郁、发呆、叹气、自言自语、心理关怀、情绪低落、社区养老健康等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看老人孤独/抑郁历史报告、情绪风险报告清单、独居老人心理报告清单、查询历史情绪风险记录、显示所有老人孤独行为报告、显示养老心理健康诊断报告，查询情绪风险预警清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_elderly_loneliness_depression_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_elderly_loneliness_depression_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备独居老人活动区域固定摄像头视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行老年人孤独/抑郁倾向行为分析 | 调用 `-m scripts.smyx_elderly_loneliness_depression_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地独居老人活动区域固定摄像头视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络独居老人活动区域固定摄像头视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，老年人心理健康监测场景默认 `other` | 按需填写 |
| `--list` | 显示老年人孤独/抑郁倾向行为历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_elderly_loneliness_depression_analysis.py`](scripts/smyx_elderly_loneliness_depression_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：必须能看到老人上半身与面部 |
| 🔎 使用提醒 | 老人看电视/看书/打盹与"发呆"在视觉上易混淆，建议结合时长 + 周期性运动 + 面部表情综合判定 |
| 🔎 使用提醒 | 多代同堂、保姆陪护等场景需启用"独处时间窗口"过滤，否则会低估孤独风险 |
| 🔎 使用提醒 | 本工具不构成抑郁症筛查工具，**不替代** GDS-15 / PHQ-9 / 心理咨询师评估 |
| 🔏 隐私合规 | 隐私合规：独居老人家庭视频涉及高度敏感个人隐私，使用前需取得老人本人明确知情同意，妥善加密保管；建议优先采用人体轮廓 + 面部马赛克模式 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地独居老人活动区域视频
python -m scripts.smyx_elderly_loneliness_depression_analysis --input /path/to/livingroom.mp4

# 分析网络独居老人活动区域视频
python -m scripts.smyx_elderly_loneliness_depression_analysis --url https://example.com/livingroom.mp4

# 显示历史老年人孤独/抑郁倾向行为报告（自动触发关键词：查看老人孤独/抑郁历史报告、情绪风险报告清单等）
python -m scripts.smyx_elderly_loneliness_depression_analysis --list

# 输出精简报告
python -m scripts.smyx_elderly_loneliness_depression_analysis --input lr.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_elderly_loneliness_depression_analysis --input lr.mp4 --output result.json
```
