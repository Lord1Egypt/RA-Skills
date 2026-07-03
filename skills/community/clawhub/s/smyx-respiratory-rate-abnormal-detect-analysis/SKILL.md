---
name: "smyx-respiratory-rate-abnormal-detect-analysis"
description: "AI-powered non-contact pet respiratory rate monitoring at rest. Detects thoracic-abdominal motion via a fixed camera, calculates breaths-per-minute, and compares against species/body-size resting norms; triggers early-warning when abnormal (e.g. dog >30 bpm, cat >40 bpm, or <8 bpm). Helps detect cardiopulmonary, respiratory or heat-stress risks early. Scenarios: home night monitoring, animal hospital wards, pet boarding centers. | 通过宠物窝或休息区固定摄像头，在宠物静息状态下分析其胸腹部起伏运动，自动计算呼吸频率（次/分钟），并与该物种/体型的正常静息呼吸范围进行对比；若检测到呼吸过快（如犬>30次/分钟，猫>40次/分钟）或过慢（<8次/分钟），则输出健康预警，建议主人观察或就医。有助于早期发现呼吸系统、心脏或热应激等潜在问题。应用场景：宠物家庭夜间监护、宠物医院住院部、宠物寄养中心。"
version: "1.0.3"
license: "MIT-0"
---

# 🫁 Pet Respiratory Rate Abnormal Detection (Resting) | 宠物呼吸频率异常监测（静息）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **宠物呼吸频率异常监测（静息）** |
| 🎯 核心目标 | 通过宠物窝或休息区固定摄像头，在宠物静息状态下分析其胸腹部起伏运动，自动计算呼吸频率（次/分钟），并与该物种/体型的正常静息呼吸范围进行对比；若检测到呼吸过快（如犬>30次/分钟，猫>40次/分钟）或过慢（<8次/分钟），则输出健康预警，建议主人观察或就医。有助于早期发现呼吸系统、心脏或热应激等潜在问题。应用场景：宠物家庭夜间监护、宠物医院住院部、宠物寄养中心。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_RESPIRATORY_RATE_ABNORMAL_DETECT_ANALYSIS` |

AI-powered non-contact pet respiratory rate monitoring at rest. Detects thoracic-abdominal motion via a fixed camera,
calculates breaths-per-minute, and compares against species/body-size resting norms; triggers early-warning when
abnormal (e.g. dog >30 bpm, cat >40 bpm, or <8 bpm). Helps detect cardiopulmonary, respiratory or heat-stress risks
early. Scenarios: home night monitoring, animal hospital wards, pet boarding centers.

通过宠物窝或休息区固定摄像头，在宠物静息状态下分析其胸腹部起伏运动，自动计算呼吸频率（次/分钟），并与该物种/体型的正常静息呼吸范围进行对比；若检测到呼吸过快（如犬>
30次/分钟，猫>40次/分钟）或过慢（<8次/分钟），则输出健康预警，建议主人观察或就医。有助于早期发现呼吸系统、心脏或热应激等潜在问题。应用场景：宠物家庭夜间监护、宠物医院住院部、宠物寄养中心。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的宠物呼吸健康监测AI。你的任务是分析宠物静息状态下的胸腹部视频，检测呼吸周期，计算呼吸频率，并与种属、体型的正常静息呼吸范围进行比对，输出异常预警。不要提供医疗诊断，仅输出呼吸频率数值及超出正常范围的提示。 ** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

通过宠物静息状态视频进行胸腹部起伏分析，计算静息呼吸频率（次/分钟），与种属/体型正常范围对比，输出异常预警和呼吸波形记录

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 胸腹部运动检测 |
| 2 | 呼吸周期识别 |
| 3 | 静息呼吸频率计算（RR/min） |
| 4 | 种属/体型范围比对 |
| 5 | 异常预警分级 |
| 6 | 持续监测与趋势分析 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供宠物静息（睡眠/静卧）状态视频需要分析时，默认触发本技能进行呼吸频率监测 |
| 🔎 明确分析意图 | 当用户明确需要呼吸频率监测时，提及呼吸频率、呼吸次数、呼吸异常、静息呼吸、胸腹起伏、夜间监护等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史呼吸监测报告、历史呼吸报告、呼吸频率报告清单、显示所有呼吸报告、查询呼吸异常记录 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_respiratory_rate_abnormal_detect_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_respiratory_rate_abnormal_detect_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 3 | ⚙️ 执行呼吸频率监测 | 调用 `-m scripts.smyx_respiratory_rate_abnormal_detect_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看监测结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地静息状态视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络静息状态视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 宠物类型，可选值：cat/dog/other，默认 cat | 按需填写 |
| `--list` | 显示呼吸频率监测历史报告列表清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 📊 静息呼吸频率正常范围参考

| 物种/体型           | 正常静息范围（次/分钟） | 偏快预警 | 严重异常      |
|-----------------|--------------|------|-----------|
| 🐱 成猫           | 16-40        | >40  | >60 或 <8  |
| 🐶 小型犬（<10kg）   | 18-34        | >35  | >50 或 <8  |
| 🐶 中型犬（10-25kg） | 15-30        | >30  | >45 或 <8  |
| 🐶 大型犬（>25kg）   | 10-28        | >30  | >40 或 <8  |
| 🐶/🐱 幼宠（<6月）   | 20-50        | >50  | >70 或 <10 |

> 数据仅供算法基线参考，具体应结合个体体重、年龄、品种（短鼻品种基线略高）和兽医建议判断。

## 🚨 异常预警分级

| 等级      | 触发条件                     | 建议                    |
|---------|--------------------------|-----------------------|
| 🟢 正常   | 在正常范围内，节律规律              | 持续监测                  |
| 🟡 轻度偏快 | 超出上限 10% 以内，节律规律         | 观察是否环境过热或刚结束运动        |
| 🟠 偏快   | 超出上限 10%-30%，持续 5 分钟     | 建议联系兽医评估              |
| 🔴 严重异常 | 超出上限 >30% 或低于下限，或节律明显不规律 | ⚠️ 立即就医检查，警惕心衰、肺炎、热射病 |

## 💡 高风险品种重点关注

| 品种类型               | 重点关注原因                |
|--------------------|-----------------------|
| 短鼻犬猫（英斗、波斯、加菲、巴哥等） | 上呼吸道阻塞，呼吸基线偏高，易出现热应激  |
| 老年宠物（>7岁）          | 心肺功能下降，呼吸异常常为早期心衰信号   |
| 既往心脏病史             | 静息呼吸频率持续 >30/分钟为肺水肿预警 |
| 肥胖宠物               | 胸廓压迫导致呼吸代偿性增快         |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_respiratory_rate_abnormal_detect_analysis.py`](scripts/smyx_respiratory_rate_abnormal_detect_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 视频要求：支持 mp4/avi/mov 格式，最大 10MB；**建议时长 ≥ 60 秒**以保证呼吸周期统计的稳定性 |
| 🧑‍⚖️ 结果性质 | **必须为静息状态**（睡眠/静卧 ≥ 1 分钟），活动状态下结果无参考意义 |
| 🧑‍⚖️ 结果性质 | 监测结果仅供健康参考，**不提供医疗诊断或治疗建议**；持续异常建议及时就医 |
| 🔎 使用提醒 | 短鼻品种基线呼吸频率偏高，请结合个体差异综合判断 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载 |
| 📜 报告输出 | 当显示历史监测报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地静息状态视频
python -m scripts.smyx_respiratory_rate_abnormal_detect_analysis --input /path/to/sleeping_pet.mp4 --pet-type cat

# 分析网络静息状态视频
python -m scripts.smyx_respiratory_rate_abnormal_detect_analysis --url https://example.com/sleeping_pet.mp4 --pet-type dog

# 显示历史监测报告/显示报告清单列表（自动触发关键词：查看历史呼吸监测报告、呼吸报告清单等）
python -m scripts.smyx_respiratory_rate_abnormal_detect_analysis --list

# 输出精简报告
python -m scripts.smyx_respiratory_rate_abnormal_detect_analysis --input rest.mp4 --pet-type cat --detail basic

# 保存结果到文件
python -m scripts.smyx_respiratory_rate_abnormal_detect_analysis --input rest.mp4 --pet-type cat --output result.json
```
