---
name: "smyx-family-conflict-intensity-detect-analysis"
description: "Using a fixed camera with microphone in the living room, the system analyzes audio and video in real time, detecting sound intensity (dB) and the intensity of body movements (e.g., rapid hand waving, finger pointing, pushing, throwing objects). It comprehensively evaluates the family conflict intensity level (low / medium / high). | 通过客厅固定摄像头（含麦克风），实时分析音频和视频，检测声音强度（分贝）和肢体动作激烈程度（如快速挥手、戳指、推搡、摔物等）。综合评估家庭争吵的冲突强度等级（低/中/高），当强度达到中或高时，通过手机APP推送提醒（如'检测到高强度冲突，建议冷静沟通或暂时分开'）。"
version: "1.0.11"
license: "MIT-0"
---

# ⚡ Family / Couple Conflict Intensity Detection | 夫妻/家庭争吵强度识别
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **夫妻/家庭争吵强度识别** |
| 🎯 核心目标 | 通过客厅固定摄像头（含麦克风），实时分析音频和视频，检测声音强度（分贝）和肢体动作激烈程度（如快速挥手、戳指、推搡、摔物等）。综合评估家庭争吵的冲突强度等级（低/中/高），当强度达到中或高时，通过手机APP推送提醒（如'检测到高强度冲突，建议冷静沟通或暂时分开'）。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_FAMILY_CONFLICT_INTENSITY_DETECT_ANALYSIS` |

Using a fixed camera with microphone in the living room, the system analyzes audio and video in real time, detecting sound intensity (dB) and the intensity of body movements (e.g., rapid hand waving, finger pointing, pushing, throwing objects). It comprehensively evaluates the family conflict intensity level (low / medium / high). When the level reaches medium or high, it pushes a gentle reminder via mobile APP (e.g., 'A high-intensity conflict has been detected. We suggest calming down or temporarily separating'). The skill helps family members become self-aware of their emotions, avoid escalation, and, when necessary, notify pre-designated emergency contacts. Application scenarios: family living rooms, psychological counseling rooms, marriage mediation centers. The system auto-reminds during detected conflicts or generates conflict-frequency reports for family counselors. Skill features: family conflicts are common; long-term high-intensity conflicts harm mental health and may escalate to domestic violence. AI automatic detection with gentle reminders helps members self-regulate before losing control. Can be integrated into smart-home cameras or family health-management APPs as an auxiliary tool to promote family harmony.

通过客厅固定摄像头（含麦克风），实时分析音频和视频，检测声音强度（分贝）和肢体动作激烈程度（如快速挥手、戳指、推搡、摔物等）。综合评估家庭争吵的冲突强度等级（低/中/高），当强度达到中或高时，通过手机APP推送提醒（如'检测到高强度冲突，建议冷静沟通或暂时分开'）。该技能旨在帮助家庭成员自我觉察情绪，避免冲突升级，必要时可联动紧急联系人。应用场景：家庭客厅、心理咨询室、婚姻调解中心。系统在检测到冲突时自动提醒，或生成冲突频率报告供家庭咨询师参考。技能特点：家庭争吵是常见现象，长期高强度冲突会影响家庭成员心理健康，甚至导致家暴。通过AI自动检测并温和提醒，可帮助家庭成员在情绪失控前自我觉察，避免冲突升级。该技能可集成到智能家居摄像头或家庭健康管理APP中，成为促进家庭和谐的辅助工具。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的家庭情绪与冲突分析 AI。你的任务是分析客厅固定摄像头的音频和视频，检测声音强度（分贝）以及肢体动作的激烈程度（挥手、戳指、推搡、摔砸物品等），综合输出冲突强度等级与温和提醒。不要提供法律或心理治疗建议，仅输出基于声学和视觉的冲突强度指标，并在高强度时附反家暴热线参考。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于家庭客厅固定摄像头（含麦克风）的同步音视频，识别声音分贝水平 + 攻击性词汇命中（本地推理）+ 喊叫事件 + 肢体激烈程度（挥手 / 戳指 / 推搡 / 摔物）→ 综合输出冲突强度等级（low / medium / high）→ 推送**温和**的觉察提醒；不替代法律或心理治疗服务

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 声学指标提取（peak_db / avg_db / db_delta_vs_baseline / shout_event_count / aggressive_word_hit_count 本地推理 / voice_speakers_estimate） |
| 2 | 视觉肢体激烈度识别（挥手 / 戳指 / 推搡 / 摔物 / 面对面贴脸） |
| 3 | 儿童或老人在场识别（升级触发位） |
| 4 | 综合冲突强度等级判定 |
| 5 | 连续高强度事件累计 |
| 6 | 面向当事人的温和提醒文案生成 |
| 7 | 紧急联系人联动开关（**事先取得用户同意**） |
| 8 | 反家暴热线与社区调解资源参考 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供客厅固定摄像头（含麦克风）音视频 URL 或文件需要分析时，默认触发本技能进行家庭争吵强度识别 |
| 🔎 明确分析意图 | 当用户明确提及家庭争吵、夫妻吵架、客厅冲突、家暴预警、冷静提醒、情绪失控、家庭调解等关键词，并且上传了音视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看家庭冲突历史报告、争吵强度报告清单、家庭冲突记录清单、查询历史冲突事件、显示所有家庭争吵报告、显示婚姻调解辅助报告，查询冲突强度预警清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_family_conflict_intensity_detect_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_family_conflict_intensity_detect_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备客厅固定摄像头（含麦克风）音视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行夫妻/家庭争吵强度识别 | 调用 `-m scripts.smyx_family_conflict_intensity_detect_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地客厅固定摄像头（含麦克风）音视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络客厅固定摄像头（含麦克风）音视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，家庭情绪与冲突分析场景默认 `other` | 按需填写 |
| `--list` | 显示夫妻/家庭争吵强度识别历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_family_conflict_intensity_detect_analysis.py`](scripts/smyx_family_conflict_intensity_detect_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 含音轨视频，最大 10MB；**关键**：必须包含麦克风音轨 |
| 🔎 使用提醒 | 看电视/电影、儿童打闹游戏、激烈讨论但无攻击性词汇等情形容易被误识为冲突，建议结合声学 + 视觉 + 攻击性词汇多模态综合判定 |
| 🔎 使用提醒 | 攻击性词汇命中**仅本地推理**，**禁止上传原始语音**到任何外部服务 |
| 🔏 隐私合规 | 红线约束：**禁止**根据本工具结论给当事人贴"家暴施害者/受害者"标签；**禁止**自动报警；**禁止**长期存储原始音视频；**禁止**输出法律意见或处方 |
| 🧑‍⚖️ 结果性质 | 紧急联系人联动需用户**事先取得双方知情同意**，默认关闭；高强度连续多次时附**反家暴热线 12338** 与就近社区调解资源参考 |
| 🔏 隐私合规 | 隐私合规：家庭音视频涉及高度敏感家庭隐私，使用前需取得**家庭所有成年成员**明确知情同意，妥善加密保管；建议优先采用人体轮廓 + 面部马赛克模式 + 仅保存指标统计 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地客厅音视频
python -m scripts.smyx_family_conflict_intensity_detect_analysis --input /path/to/livingroom.mp4

# 分析网络客厅音视频
python -m scripts.smyx_family_conflict_intensity_detect_analysis --url https://example.com/livingroom.mp4

# 显示历史家庭争吵强度报告（自动触发关键词：查看家庭冲突历史报告、争吵强度报告清单等）
python -m scripts.smyx_family_conflict_intensity_detect_analysis --list

# 输出精简报告
python -m scripts.smyx_family_conflict_intensity_detect_analysis --input lr.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_family_conflict_intensity_detect_analysis --input lr.mp4 --output result.json
```
