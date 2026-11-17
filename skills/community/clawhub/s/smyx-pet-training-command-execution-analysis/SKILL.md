---
name: "smyx-pet-training-command-execution-analysis"
description: "Triggers when a user provides a training-area video of a pet for analysis; supports local uploads or network URLs to call server-side APIs for command-execution recognition, detecting whether the pet's body posture matches the issued commands (Sit / Down / Stay), comparing posture timing against command timestamps, and judging execution success. When the command is not executed, the result can trigger an external voice repeat-prompt signal (not a medical / behavior-therapy advice). Application scenarios: smart dog-training devices, remote pet training, behavior correction. | 当用户提供训练区域视频时，触发本技能进行姿态-指令匹配分析；支持通过上传本地视频或网络视频URL，调用服务端API检测宠物身体姿态是否符合“坐/卧/等”指令标准，对比指令发出时间，判断是否执行成功；未执行时可由外部设备触发声控重复提示信号（不提供疾病诊断或行为治疗方案）。应用场景：智能训狗设备、宠物远程训练、行为矫正。"
version: "1.0.17"
license: "MIT-0"
---

# 🎓 Pet Training Command Execution Recognition | 宠物训练指令执行识别（坐/卧/等）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **宠物训练指令执行识别（坐/卧/等）** |
| 🎯 核心目标 | 当用户提供训练区域视频时，触发本技能进行姿态-指令匹配分析；支持通过上传本地视频或网络视频URL，调用服务端API检测宠物身体姿态是否符合“坐/卧/等”指令标准，对比指令发出时间，判断是否执行成功；未执行时可由外部设备触发声控重复提示信号（不提供疾病诊断或行为治疗方案）。应用场景：智能训狗设备、宠物远程训练、行为矫正。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_PET_TRAINING_COMMAND_EXECUTION_ANALYSIS` |

Triggers when a user provides a training-area video of a pet for analysis; supports local uploads or network URLs to
call server-side APIs for command-execution recognition, detecting whether the pet's body posture matches the issued
commands (Sit / Down / Stay), comparing posture timing against command timestamps, and judging execution success. When
the command is not executed, the result can trigger an external voice repeat-prompt signal (not a medical /
behavior-therapy advice). Application scenarios: smart dog-training devices, remote pet training, behavior correction.

当用户提供训练区域视频时，触发本技能进行姿态-指令匹配分析；支持通过上传本地视频或网络视频URL，调用服务端API检测宠物身体姿态是否符合“坐/卧/等”指令标准，对比指令发出时间，判断是否执行成功；未执行时可由外部设备触发声控重复提示信号（不提供疾病诊断或行为治疗方案）。应用场景：智能训狗设备、宠物远程训练、行为矫正。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **你是一个专业的宠物行为分析AI。你的任务是基于训练区域的连续视频，分析宠物在指令发出后的姿态变化，判断其是否按指令完成了“坐”“卧”“等”动作。不要提供疾病诊断或行为治疗方案，仅客观描述姿态与指令的匹配程度。 ** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

通过训练区域视频识别宠物对“坐 / 卧 / 等”指令的执行情况，输出姿态-指令匹配结果与响应延迟数据，辅助远程训练，提高服从性

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 视频分析 |
| 2 | 姿态识别（坐姿/卧姿/站立/等待静止） |
| 3 | 指令时间戳对比 |
| 4 | 响应延迟统计（秒） |
| 5 | 姿态匹配度评分（0~ |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供训练区域视频 URL 或文件需要分析时，默认触发本技能进行训练指令执行识别 |
| 🔎 明确分析意图 | 当用户明确需要进行训练评估时，提及坐下、趴下、卧下、等一下、训狗、宠物训练、指令执行、服从性、行为矫正、训练打卡等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史训练报告、历史指令执行报告、训练记录清单、查询训练进度、显示所有训狗报告、显示指令执行报告，查询训练成功率报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_pet_training_command_execution_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_pet_training_command_execution_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 3 | ⚙️ 执行训练指令执行识别分析 | 调用 `-m scripts.smyx_pet_training_command_execution_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 宠物类型，可选值：cat/dog/other，默认 dog | 按需填写 |
| `--list` | 显示训练指令执行历史分析报告列表清单（可输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🎓 指令姿态识别参考标准 | Command Posture Reference
| 指令      | 标准姿态             | 完成判定                    | 响应延迟参考   |
|---------|------------------|-------------------------|----------|
| 坐（Sit）  | 后腿坐地、前腿伸直、躯干竖直   | 姿态匹配度 ≥ 70 且保持 ≥ 1 秒    | ≤ 3 秒为良好 |
| 卧（Down） | 四肢着地、腹部贴近地面、头部放低 | 姿态匹配度 ≥ 70 且保持 ≥ 1 秒    | ≤ 4 秒为良好 |
| 等（Stay） | 当前姿态保持不变、无位移     | 静止时长 ≥ 指令要求时长（默认 ≥ 5 秒） | 无位移视为成功  |

| 执行结果    | 含义              | 建议干预                     |
|---------|-----------------|--------------------------|
| ✅ 成功    | 姿态匹配 & 在响应窗口内完成 | 给予奖励（语音/零食）              |
| ⚠️ 部分成功 | 姿态正确但响应延迟过长     | 鼓励 + 缩短指令-奖励间隔           |
| 🚨 未执行  | 未达到姿态匹配或超时      | **触发外部声控重复提示**，必要时降低指令难度 |

> 注：以上参考标准仅作为视觉识别参考，最终判定以 API 输出结果为准。猫等小动物的指令训练标准差异较大，需结合品种特点综合判断。

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_pet_training_command_execution_analysis.py`](scripts/smyx_pet_training_command_execution_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 视频要求：支持 mp4/avi/mov 格式，最大 10MB，建议覆盖完整指令-响应过程 |
| 🧑‍⚖️ 结果性质 | 分析结果仅供训练效果参考，不提供疾病诊断或行为治疗方案 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载 |
| 🔎 使用提醒 | 声控重复提示信号由智能训狗设备基于本技能的输出结果触发，本技能仅负责输出干预建议 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 `` 作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地训练区域视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_pet_training_command_execution_analysis --input /path/to/training_video.mp4 --pet-type dog

# 分析网络训练区域视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_pet_training_command_execution_analysis --url https://example.com/training_video.mp4 --pet-type dog

# 显示历史分析报告清单（自动触发关键词：查看历史训练报告、指令执行报告清单等）
python -m scripts.smyx_pet_training_command_execution_analysis --list

# 输出精简报告
python -m scripts.smyx_pet_training_command_execution_analysis --input training_video.mp4 --pet-type dog --detail basic

# 保存结果到文件
python -m scripts.smyx_pet_training_command_execution_analysis --input training_video.mp4 --pet-type dog --output result.json
```
