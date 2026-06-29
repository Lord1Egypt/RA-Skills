---
name: "smyx-autism-stereotyped-behavior-detect-analysis"
description: "Using a fixed camera in rehabilitation centers or homes, the system analyzes children's behavior videos with pose estimation and temporal action detection to recognize repetitive stereotyped behaviors, including spinning (body rotation ≥ 360°), hand flapping (non-functional repetitive arm movement), body rocking (rhythmic forward-backward or side-to-side trunk motion), etc. | 通过康复机构或家庭固定摄像头，分析儿童行为视频，利用姿态估计和时序动作检测技术识别重复性刻板动作，包括转圈（身体旋转360°以上）、摆手（手臂非功能性重复摆动）、摇晃（躯干前后或左右有节律摆动）等。该技能可辅助康复师和家长客观记录行为变化，评估干预效果。"
version: "1.0.2"
license: "MIT-0"
---

# 🧩 Autism Stereotyped Behavior Detection (Spinning / Hand-Flapping) | 自闭症儿童刻板行为识别（转圈/摆手）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **自闭症儿童刻板行为识别（转圈/摆手）** |
| 🎯 核心目标 | 通过康复机构或家庭固定摄像头，分析儿童行为视频，利用姿态估计和时序动作检测技术识别重复性刻板动作，包括转圈（身体旋转360°以上）、摆手（手臂非功能性重复摆动）、摇晃（躯干前后或左右有节律摆动）等。该技能可辅助康复师和家长客观记录行为变化，评估干预效果。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_AUTISM_STEREOTYPED_BEHAVIOR_DETECT_ANALYSIS` |

Using a fixed camera in rehabilitation centers or homes, the system analyzes children's behavior videos with pose estimation and temporal action detection to recognize repetitive stereotyped behaviors, including spinning (body rotation ≥ 360°), hand flapping (non-functional repetitive arm movement), body rocking (rhythmic forward-backward or side-to-side trunk motion), etc. It counts the frequency (events per hour) and duration of each behavior and generates a behavior report. The skill helps therapists and parents objectively record behavior changes and evaluate intervention effects. Application scenarios: autism rehabilitation institutions, special-education schools, home interventions. Real-time monitoring; the system automatically generates daily / weekly stereotyped-behavior statistics to support rehabilitation planning. Skill features: stereotyped behaviors are a core symptom of autism, and changes in frequency / duration are important indicators of intervention effectiveness. Automatic AI recording reduces therapists' workload, enables long-term continuous monitoring, and provides data support for individualized intervention. Can be integrated into rehabilitation-center management systems or home-rehabilitation apps.

通过康复机构或家庭固定摄像头，分析儿童行为视频，利用姿态估计和时序动作检测技术识别重复性刻板动作，包括转圈（身体旋转360°以上）、摆手（手臂非功能性重复摆动）、摇晃（躯干前后或左右有节律摆动）等。统计每种刻板行为的频次（次/小时）和单次持续时间，生成行为报告。该技能可辅助康复师和家长客观记录行为变化，评估干预效果。应用场景：自闭症康复机构、特殊教育学校、家庭干预。系统实时监测，自动生成每日/每周刻板行为统计报告，为康复计划提供数据支持。技能特点：刻板行为是自闭症的核心症状之一，其频率和持续时间变化是评估干预效果的重要依据。通过AI自动监测记录，可减轻康复师负担，实现长时间连续监测，为个性化干预提供数据支持。该技能可集成到康复机构管理系统或家庭康复APP中。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的自闭症儿童行为分析 AI。你的任务是分析固定摄像头拍摄的儿童行为视频，检测重复性刻板动作，包括转圈、摆手、摇晃等。统计每种行为的频次和持续时间，输出行为报告。不要提供自闭症诊断、量表打分或康复处方，仅输出基于视觉的客观行为统计，供专业康复师和家长参考。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于康复机构/家庭固定摄像头视频，识别儿童多类重复性刻板行为 → 按事件级别记录起止时间/持续秒数/置信度 → 汇总各类频次（次/小时）+ 累计时长 + 主导类别 → 可结合历史基线生成趋势报告

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 人体检测与跟踪 |
| 2 | 2D/3D 姿态关键点估计 |
| 3 | 时序动作分类（spinning / hand_flapping / body_rocking / head_banging / finger_flicking / toe_walking / repetitive_running / repetitive_object_play 等） |
| 4 | 事件级起止时间检测与去重 |
| 5 | 每小时/每日频次与累计时长统计 |
| 6 | 主导刻板行为类别识别 |
| 7 | 与个人 7-14 天基线对比（趋势变化百分比） |
| 8 | 康复师/家长行为摘要文本生成 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供康复/家庭儿童行为视频 URL 或文件需要分析时，默认触发本技能进行刻板行为识别 |
| 🔎 明确分析意图 | 当用户明确提及自闭症、谱系障碍、刻板行为、转圈、摆手、摇晃、撞头、踮脚走、康复评估、特殊教育、ABA 干预效果等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看刻板行为历史报告、自闭症儿童行为报告清单、刻板行为统计报告清单、查询历史康复评估记录、显示所有刻板行为分析报告、显示特殊教育诊断报告，查询刻板行为趋势预警清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_autism_stereotyped_behavior_detect_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_autism_stereotyped_behavior_detect_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备康复/家庭儿童行为视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行自闭症儿童刻板行为识别 | 调用 `-m scripts.smyx_autism_stereotyped_behavior_detect_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地康复/家庭儿童行为视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络康复/家庭儿童行为视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，自闭症儿童行为分析场景默认 `other` | 按需填写 |
| `--list` | 显示自闭症儿童刻板行为识别历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_autism_stereotyped_behavior_detect_analysis.py`](scripts/smyx_autism_stereotyped_behavior_detect_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：必须能看到儿童全身，帧率 ≥ 10 FPS |
| 🔎 使用提醒 | 部分日常动作（鼓掌、跳舞、追逐游戏等）可能被误识别为刻板行为，建议康复师/家长进行抽样复核 |
| 🔎 使用提醒 | 多儿童在同一视野内、家庭成员同时出现等情形可能影响识别准确性 |
| 🧑‍⚖️ 结果性质 | 本工具**不提供自闭症诊断**，也**不替代** ADOS-2 / ADI-R / CARS 等专业评估；任何康复方案应在认证的康复治疗师指导下进行 |
| 🔏 隐私合规 | 隐私合规：自闭症儿童行为视频涉及未成年人高度敏感隐私，使用前需取得监护人明确知情同意，妥善加密保管；建议优先采用人体骨架/轮廓模式 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地康复/家庭儿童行为视频
python -m scripts.smyx_autism_stereotyped_behavior_detect_analysis --input /path/to/rehab.mp4

# 分析网络康复/家庭儿童行为视频
python -m scripts.smyx_autism_stereotyped_behavior_detect_analysis --url https://example.com/rehab.mp4

# 显示历史自闭症儿童刻板行为识别报告（自动触发关键词：查看刻板行为历史报告、自闭症儿童行为报告清单等）
python -m scripts.smyx_autism_stereotyped_behavior_detect_analysis --list

# 输出精简报告
python -m scripts.smyx_autism_stereotyped_behavior_detect_analysis --input rehab.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_autism_stereotyped_behavior_detect_analysis --input rehab.mp4 --output result.json
```
