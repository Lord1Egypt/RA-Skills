---
name: "smyx-public-place-group-emotion-index-analysis"
description: "Using fixed cameras in malls, exhibition halls, scenic areas and other public places, the system analyzes facial expressions of multiple people in the scene in real time (with anonymized expression recognition only), aggregates the distribution of emotions (happy, calm, irritated, surprised, sad, fearful, etc.), and computes an overall group-emotion index (0-100; higher = more positive). | 通过商场、展览馆、景区等公共场所的固定摄像头，实时分析场景中多人的面部表情（使用匿名化表情识别），统计各类情绪（愉悦、平静、烦躁、惊讶、悲伤等）的分布比例，计算整体情绪指数（0-100，数值越高代表群体情绪越积极）。该技能可帮助运营方了解顾客满意度、优化服务布局，或用于公共安全预警（如烦躁情绪比例过高可能预示冲突风险）。"
version: "1.0.3"
license: "MIT-0"
---

# 👥 Public Place Group Emotion Index (Exhibition / Mall) | 公共场所群体情绪指数（展览/商场）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **公共场所群体情绪指数（展览/商场）** |
| 🎯 核心目标 | 通过商场、展览馆、景区等公共场所的固定摄像头，实时分析场景中多人的面部表情（使用匿名化表情识别），统计各类情绪（愉悦、平静、烦躁、惊讶、悲伤等）的分布比例，计算整体情绪指数（0-100，数值越高代表群体情绪越积极）。该技能可帮助运营方了解顾客满意度、优化服务布局，或用于公共安全预警（如烦躁情绪比例过高可能预示冲突风险）。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_PUBLIC_PLACE_GROUP_EMOTION_INDEX_ANALYSIS` |

Using fixed cameras in malls, exhibition halls, scenic areas and other public places, the system analyzes facial expressions of multiple people in the scene in real time (with anonymized expression recognition only), aggregates the distribution of emotions (happy, calm, irritated, surprised, sad, fearful, etc.), and computes an overall group-emotion index (0-100; higher = more positive). This skill helps operators understand customer satisfaction, optimize service layout, or trigger public-safety warnings (e.g., a high irritation ratio may indicate conflict risk). Application scenarios: shopping malls, exhibition halls, museums, theme parks, airport waiting halls. The system periodically generates group-emotion reports to support management decisions. Skill features: understanding customer emotions enables malls to promptly adjust services (e.g., open more checkouts, improve air conditioning, optimize traffic flow) and boost satisfaction; for exhibitions, it assesses exhibit appeal; for public safety, it warns against group irritation that may escalate into conflict. AI anonymous analysis delivers valuable insights while protecting privacy and is an essential capability of smart malls and smart scenic areas. Can be integrated into existing security systems or business-analytics platforms.

通过商场、展览馆、景区等公共场所的固定摄像头，实时分析场景中多人的面部表情（使用匿名化表情识别），统计各类情绪（愉悦、平静、烦躁、惊讶、悲伤等）的分布比例，计算整体情绪指数（0-100，数值越高代表群体情绪越积极）。该技能可帮助运营方了解顾客满意度、优化服务布局，或用于公共安全预警（如烦躁情绪比例过高可能预示冲突风险）。应用场景：购物中心、展览馆、博物馆、主题公园、机场候机厅。系统定期生成群体情绪报告，辅助管理决策。技能特点：了解顾客情绪能帮助商场及时调整服务（如增加收银台、改善空调、优化动线），提升满意度；对展览馆可评估展品吸引力；对公共安全可预警群体暴躁可能引发的冲突。通过AI匿名分析，在保护隐私的前提下获取有价值的数据洞察，是智慧商场、智慧景区的重要功能。该技能可集成到现有安防系统或商业分析平台中。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的公共场所群体情绪分析 AI。你的任务是分析固定摄像头的视频，检测画面中多个人的面部表情（匿名化处理，不识别个人身份），统计各类情绪（愉悦、平静、烦躁、惊讶、悲伤、恐惧等）的出现频率，计算整体情绪指数，并按区域输出运营优化与安全预警建议。不要识别或存储个人特征，仅输出群体层面的匿名统计。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于商场/展览馆/景区/机场/博物馆/主题公园等公共场所固定摄像头视频，匿名统计 6 类情绪分布 + 群体情绪指数（0-100）+ 按区域输出指数 → 输出运营优化建议（收银/空调/动线/展品吸引力）与公共安全预警（烦躁占比过高可能预示冲突风险）

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 匿名人脸表情检测（**不做身份识别/比对/跟踪**） |
| 2 | 6 类情绪分类（happy / calm / irritated / surprised / sad / fearful） |
| 3 | 积极/消极/烦躁比例计算 |
| 4 | 人群密度估计 |
| 5 | 平均停留时长估计 |
| 6 | 区域 ROI 划分与区域级情绪指数（region_breakdown） |
| 7 | 与上一时间窗对比 |
| 8 | 4 档情绪等级判定（positive ≥ 70 / neutral 50-69 / low 30-49 / negative < 30 或烦躁 > 25%） |
| 9 | 最小样本保护（face_detected_count < 5 输出 insufficient_sample） |
| 10 | 运营优化与安全预警双通道建议 |
| 11 | 区域级情绪指数热力图 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供商场/展览馆/景区等公共场所固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行公共场所群体情绪指数分析 |
| 🔎 明确分析意图 | 当用户明确提及商场顾客情绪、展品吸引力、景区满意度、群体暴躁、安全预警、智慧商场、智慧景区、客流情绪洞察等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看群体情绪历史报告、群体情绪指数报告清单、商场/展览/景区情绪报告清单、查询历史群体情绪记录、显示所有群体情绪分析报告、显示客流情绪洞察报告，查询群体情绪预警清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_public_place_group_emotion_index_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_public_place_group_emotion_index_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备公共场所固定摄像头视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行公共场所群体情绪指数分析 | 调用 `-m scripts.smyx_public_place_group_emotion_index_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地公共场所固定摄像头视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络公共场所固定摄像头视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，公共场所群体情绪分析场景默认 `other` | 按需填写 |
| `--list` | 显示公共场所群体情绪指数历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_public_place_group_emotion_index_analysis.py`](scripts/smyx_public_place_group_emotion_index_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：能拍到顾客正面或斜侧脸、覆盖目标区域 |
| 🔎 使用提醒 | 戴口罩、戴墨镜、低头看手机、背对摄像头等情形会显著降低可识别人脸数，建议在指标中标注 `face_detected_count` 以便解读 |
| 🔎 使用提醒 | 短时局部表情（如顾客接电话短暂皱眉）不应单独触发负面预警，建议使用时间窗均值 |
| 🔎 使用提醒 | 最小样本保护：`face_detected_count < 5` 时输出 `insufficient_sample`，**禁止**发布群体指数 |
| 🔎 使用提醒 | 红线约束：**禁止**人脸识别 / 人脸比对 / 身份绑定 / 跨摄像头跟踪；**禁止**长期存储顾客原始视频或人脸特征向量；**禁止**将群体情绪用于针对个体顾客的差异化定价或服务歧视 |
| 🔎 使用提醒 | 合规要点：部署场所必须以**显著标识**告知公众使用了匿名情绪分析摄像头，并提供咨询联系方式；数据保存期限建议 ≤ 30 天，仅保留聚合指标 |
| 🧑‍⚖️ 结果性质 | 安全预警仅作为人工值守的辅助参考，**禁止**单纯依据情绪指数自动触发警报或干预 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地公共场所视频
python -m scripts.smyx_public_place_group_emotion_index_analysis --input /path/to/mall.mp4

# 分析网络公共场所视频
python -m scripts.smyx_public_place_group_emotion_index_analysis --url https://example.com/mall.mp4

# 显示历史公共场所群体情绪指数报告（自动触发关键词：查看群体情绪历史报告、群体情绪指数报告清单等）
python -m scripts.smyx_public_place_group_emotion_index_analysis --list

# 输出精简报告
python -m scripts.smyx_public_place_group_emotion_index_analysis --input mall.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_public_place_group_emotion_index_analysis --input mall.mp4 --output result.json
```
