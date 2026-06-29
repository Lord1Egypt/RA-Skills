---
name: "smyx-classroom-engagement-analysis-analysis"
description: "Using a fixed classroom camera, the system analyzes students' facial expressions (focused, confused, happy, frustrated, bored, etc.), computes a class-level overall engagement score (0-100), and can identify low-engagement student positions (no identity stored — for real-time teacher reminders only). Real-time analysis provides engagement heatmaps and abnormal alerts. | 通过教室固定摄像头，分析学生面部表情（专注、困惑、开心、沮丧、无聊等），计算班级整体参与度评分（0-100分），并可识别出参与度较低的学生个体（不存储身份，仅用于实时提醒）。该技能可辅助教师调整教学节奏，关注学习困难学生。"
version: "1.0.3"
license: "MIT-0"
---

# 🏫 Student Classroom Engagement Analysis | 学生课堂情绪参与度分析
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **学生课堂情绪参与度分析** |
| 🎯 核心目标 | 通过教室固定摄像头，分析学生面部表情（专注、困惑、开心、沮丧、无聊等），计算班级整体参与度评分（0-100分），并可识别出参与度较低的学生个体（不存储身份，仅用于实时提醒）。该技能可辅助教师调整教学节奏，关注学习困难学生。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_CLASSROOM_ENGAGEMENT_ANALYSIS_ANALYSIS` |

Using a fixed classroom camera, the system analyzes students' facial expressions (focused, confused, happy, frustrated, bored, etc.), computes a class-level overall engagement score (0-100), and can identify low-engagement student positions (no identity stored — for real-time teacher reminders only). The skill helps teachers adjust teaching pace and pay attention to students having learning difficulty. Application scenarios: K-12 classrooms, training courses, online education (students must be on camera). Real-time analysis provides engagement heatmaps and abnormal alerts. Skill features: it is difficult for a teacher to monitor every student's facial state in real time. AI-assisted analysis helps teachers timely detect confusion or boredom, adjust teaching strategy, and improve quality. Can be integrated into smart-classroom systems or lecture-recording devices.

通过教室固定摄像头，分析学生面部表情（专注、困惑、开心、沮丧、无聊等），计算班级整体参与度评分（0-100分），并可识别出参与度较低的学生个体（不存储身份，仅用于实时提醒）。该技能可辅助教师调整教学节奏，关注学习困难学生。应用场景：中小学教室、培训课堂、在线教育（需拍摄学生）。系统实时分析，为教师提供参与度热力图和异常提醒。技能特点：教师难以实时关注每个学生的表情状态。通过AI辅助分析，可帮助教师及时发现学生困惑或无聊，调整教学策略，提高教学质量。该技能可集成到智慧教室系统或录播设备中。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的课堂教学分析 AI。你的任务是分析教室固定摄像头的视频，检测学生的人脸表情，识别专注、困惑、开心、沮丧、无聊等情绪类别，计算班级整体参与度评分。不存储学生身份信息，仅输出群体统计和匿名化的低参与度提示（仅返回座位坐标），作为教师实时教学辅助。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于教室固定摄像头视频，识别学生面部 6 类情绪（focused / confused / happy / frustrated / bored / neutral）+ 头部朝向 + 举手互动 → 输出班级群体参与度评分（0-100）→ 输出匿名低参与度座位坐标 + 困惑集中座位 + 教师实时教学建议 + 参与度热力图

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 人脸检测（不做身份关联） |
| 2 | 6 类情绪分类 |
| 3 | 头部姿态朝向估计（朝向讲台比例） |
| 4 | 举手事件计数 |
| 5 | 教学环节推测（lecture / interaction / practice） |
| 6 | 座位 ROI 网格映射（row × col） |
| 7 | 班级整体参与度评分 |
| 8 | 低参与度座位识别（仅返回坐标） |
| 9 | 困惑/沮丧热点识别 |
| 10 | 与上一时间窗对比的趋势分析 |
| 11 | 面向教师的中性教学建议生成 |
| 12 | 参与度伪彩色热力图 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供教室固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行学生课堂情绪参与度分析 |
| 🔎 明确分析意图 | 当用户明确提及课堂参与度、学生情绪、教学反馈、智慧教室、课堂困惑、走神、举手互动等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看课堂参与度历史报告、参与度报告清单、教学情绪报告清单、查询历史课堂参与度记录、显示所有课堂情绪分析报告、显示班级参与度诊断报告，查询课堂参与度预警清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_classroom_engagement_analysis_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_classroom_engagement_analysis_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备教室固定摄像头视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行学生课堂情绪参与度分析 | 调用 `-m scripts.smyx_classroom_engagement_analysis_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地教室固定摄像头视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络教室固定摄像头视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，课堂教学分析场景默认 `other` | 按需填写 |
| `--list` | 显示学生课堂情绪参与度历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_classroom_engagement_analysis_analysis.py`](scripts/smyx_classroom_engagement_analysis_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：讲台对面/斜侧高位、覆盖大部分学生脸部 |
| 🔎 使用提醒 | 在线教育场景需确保学生摄像头开启且采集合法合规 |
| 🔎 使用提醒 | 部分日常表情（思考、记笔记低头）易被误识为"无聊"或"困惑"，建议结合短时序均值 |
| 🔎 使用提醒 | 教学环节切换（如讲解 → 练习）期间短暂参与度下降视为正常，不应立即触发提醒 |
| 🔎 使用提醒 | 强匿名约束：本工具**禁止**做人脸识别 / 学生身份绑定；**禁止**用于学生绩效评估、家长沟通或公开排名；**禁止**长期存储原始视频或可识别个人特征的数据 |
| 🔎 使用提醒 | 合规要点：涉及未成年人，必须取得**学校 + 家长**双重知情同意，并明确告知用途与数据保存期限；建议由教务处统一备案 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地教室视频
python -m scripts.smyx_classroom_engagement_analysis_analysis --input /path/to/classroom.mp4

# 分析网络教室视频
python -m scripts.smyx_classroom_engagement_analysis_analysis --url https://example.com/classroom.mp4

# 显示历史学生课堂情绪参与度报告（自动触发关键词：查看课堂参与度历史报告、参与度报告清单等）
python -m scripts.smyx_classroom_engagement_analysis_analysis --list

# 输出精简报告
python -m scripts.smyx_classroom_engagement_analysis_analysis --input classroom.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_classroom_engagement_analysis_analysis --input classroom.mp4 --output result.json
```
