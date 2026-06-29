---
name: "smyx-employee-emotion-fluctuation-hr-analysis"
description: "Using fixed cameras in enterprise office areas (with employee consent and anonymization), the system performs long-term monitoring of employees' facial expressions and posture features, building per-person historical baselines (smile frequency, sigh count, frown level, etc.). | 通过企业办公区固定摄像头（需征得员工同意并匿名化处理），长期监测员工的面部表情和姿态特征，建立个人历史基线（如笑容频率、叹气次数、皱眉程度等）。当检测到某员工近期的笑容频率显著下降（例如比基线降低40%）、叹气次数增加（例如比基线增加50%）或与其他异常行为（社交回避、长时间独自静坐）时，输出情绪波动预警，提醒HR或管理者进行关怀沟通。"
version: "1.0.4"
license: "MIT-0"
---

# 💼 Employee Emotion Fluctuation HR Report | 员工情绪波动 HR 报告
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **员工入职/离职情绪波动预警（HR方向）** |
| 🎯 核心目标 | 通过企业办公区固定摄像头（需征得员工同意并匿名化处理），长期监测员工的面部表情和姿态特征，建立个人历史基线（如笑容频率、叹气次数、皱眉程度等）。当检测到某员工近期的笑容频率显著下降（例如比基线降低40%）、叹气次数增加（例如比基线增加50%）或与其他异常行为（社交回避、长时间独自静坐）时，输出情绪波动预警，提醒HR或管理者进行关怀沟通。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_EMPLOYEE_EMOTION_FLUCTUATION_HR_ANALYSIS` |

Using fixed cameras in enterprise office areas (with employee consent and anonymization), the system performs long-term monitoring of employees' facial expressions and posture features, building per-person historical baselines (smile frequency, sigh count, frown level, etc.). When an employee's smile frequency drops significantly relative to baseline (e.g., -40%), sighs increase significantly (e.g., +50%), or other abnormal behaviors emerge (social withdrawal, long solo sitting), the system outputs an emotion-fluctuation alert and reminds HR or managers to initiate a supportive check-in. The skill aims to help organizations detect employee mental-health issues early, reduce turnover risk, and improve well-being. Application scenarios: enterprise open-plan offices, department private offices. The system generates weekly or monthly employee emotion-trend reports for HR internal reference ONLY. Skill features: low employee morale often precedes resignation; AI-based early identification allows HR to provide timely care and reduce attrition. Suitable for mid-to-large enterprises, especially high-pressure roles such as R&D and customer service. Privacy must be protected; access should be limited to HR senior management only.

通过企业办公区固定摄像头（需征得员工同意并匿名化处理），长期监测员工的面部表情和姿态特征，建立个人历史基线（如笑容频率、叹气次数、皱眉程度等）。当检测到某员工近期的笑容频率显著下降（例如比基线降低40%）、叹气次数增加（例如比基线增加50%）或与其他异常行为（社交回避、长时间独自静坐）时，输出情绪波动预警，提醒HR或管理者进行关怀沟通。该技能旨在帮助组织及时发现员工心理健康问题，降低离职风险，提升员工幸福感。应用场景：企业开放式办公区、部门独立办公室。系统每周或每月生成员工情绪趋势报告，仅供HR内部参考。技能特点：员工情绪低落往往是离职的前兆，通过AI早期识别异常，HR可及时介入关怀，降低流失率。该技能适用于中大型企业，尤其适合研发、客服等高压力岗位。需注意隐私保护，建议仅HR管理层可见。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的职场心理健康监测 AI（必须经企业授权 + 员工知情同意 + 工会备案）。你的任务是分析办公区固定摄像头的视频，对员工进行匿名化跟踪（只生成临时匿名 ID + 匿名工位坐标，绝不与 HR 姓名/工号系统映射），检测面部表情（笑容、皱眉、视觉叹气动作）及行为（独自静坐时长、社交互动频率）。对比个人 30 天历史基线，当笑容频率下降 ≥ 40% 或叹气次数增加 ≥ 50% 或独自静坐增加 ≥ 50% 时，输出情绪波动预警。不存储任何个人识别信息，仅向 HR 高级管理层输出匿名 ID + 工位坐标的关怀提示，禁止用于绩效考核、晋升、解雇决策。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于企业办公区固定摄像头视频（员工知情同意 + 工会备案），匿名跟踪员工面部表情 4 项（笑容数 / 笑容时长 / 皱眉数 / 视觉叹气数 / 中性比例）+ 行为 4 项（独自静坐总时长 / 同事互动事件数 / 离开工位次数 / 工位姿态前倾比例）→ 与个人 30 天基线对比 → 连续 ≥ 3 个工作日异常 → 输出匿名 ID + 工位坐标级的 HR 关怀建议（**不输出姓名，不与工号绑定**），用于自愿性 1-on-1 关怀沟通

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 基于临时匿名 ID 的多人跨帧跟踪（ID 周期性轮换 ≤ 7 天） |
| 2 | 笑容/皱眉/视觉叹气识别（耸肩 + 长呼气姿态） |
| 3 | 独自静坐 vs 同事互动判别 |
| 4 | 工位 ROI 标定（W-A12 / W-B07 等匿名坐标） |
| 5 | 30 天个人基线计算 |
| 6 | smile_delta / sigh_delta / solo_sit_delta / peer_interaction_delta 百分比对比 |
| 7 | 连续异常天数累计 |
| 8 | 波动模式分类（smile_drop / sigh_increase / withdrawal / mixed / improving / none） |
| 9 | 4 档关怀等级（none / mild / notable / focus_care） |
| 10 | 最小样本保护（当日可分析时长 < 2 h 输出 insufficient_sample） |
| 11 | 面向 HR 的中性 |
| 12 | 保密 |
| 13 | 自愿性关怀建议生成 |
| 14 | EAP 资源参考 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供企业办公区固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行员工情绪波动 HR 报告 |
| 🔎 明确分析意图 | 当用户明确提及员工情绪、员工幸福感、离职风险、HR 关怀、高压力岗位心理健康、EAP、工位情绪监测等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看员工情绪波动历史报告、HR 关怀报告清单、员工情绪趋势报告清单、查询历史员工情绪记录、显示所有 HR 内部情绪报告、显示团队情绪健康报告，查询员工情绪波动预警清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_employee_emotion_fluctuation_hr_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_employee_emotion_fluctuation_hr_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备企业办公区固定摄像头视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 获取 open-id（强制执行） | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行员工情绪波动 HR 报告 | 调用 `-m scripts.smyx_employee_emotion_fluctuation_hr_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地企业办公区固定摄像头视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络企业办公区固定摄像头视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，职场心理健康监测场景默认 `other` | 按需填写 |
| `--list` | 显示员工情绪波动 HR 报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_employee_emotion_fluctuation_hr_analysis.py`](scripts/smyx_employee_emotion_fluctuation_hr_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：必须有 ≥ 30 天个人基线，单日可分析时长 ≥ 2 h |
| 🔎 使用提醒 | 节假日 / 项目截止日 / 加班季 / 团建后疲倦等情形会显著影响指标，建议在配置中标记"非常态期" |
| 🔎 使用提醒 | 突发短期波动（如家庭事件单日情绪低落）不应立即触发预警，必须连续 ≥ 3 个工作日异常 |
| 🔎 使用提醒 | **红线（必读）** |
| 🔎 使用提醒 | **禁止**人脸识别到 HR 姓名/工号库；**禁止**将"匿名 ID ↔ 实际员工"映射表落地存储或对外暴露 |
| 🧑‍⚖️ 结果性质 | **禁止**输出"焦虑症/抑郁症"等任何精神医学诊断或量表评分 |
| 🔎 使用提醒 | **禁止**用于绩效考核、晋升评估、解雇决策 |
| 🔎 使用提醒 | **禁止**长期存储原始视频或人脸特征；建议仅保存匿名 ID 级聚合指标，保留期 ≤ 30 天 |
| 🔎 使用提醒 | **禁止**未经员工本人同意将其数据共享给直属上级以外的第三方 |
| 📁 格式支持 | **禁止**在沟通中直接告知员工"你被摄像头分析为情绪低落"，必须以**自然工作支持**的方式进行 |
| 🔎 使用提醒 | 合规要点：必须**显著公告 + 员工代表大会/工会备案** + 员工 opt-out 选项；数据访问 ≥ 2 名 HR 高管共同审批 + 全量访问日志 |
| 🧑‍⚖️ 结果性质 | 当 `focus_care_needed` 时附**企业 EAP / 全国心理援助热线 400-161-9995**参考 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地企业办公区视频
python -m scripts.smyx_employee_emotion_fluctuation_hr_analysis --input /path/to/office.mp4

# 分析网络企业办公区视频
python -m scripts.smyx_employee_emotion_fluctuation_hr_analysis --url https://example.com/office.mp4

# 显示历史员工情绪波动 HR 报告（自动触发关键词：查看员工情绪波动历史报告、HR 关怀报告清单等）
python -m scripts.smyx_employee_emotion_fluctuation_hr_analysis --list

# 输出精简报告
python -m scripts.smyx_employee_emotion_fluctuation_hr_analysis --input office.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_employee_emotion_fluctuation_hr_analysis --input office.mp4 --output result.json
```
