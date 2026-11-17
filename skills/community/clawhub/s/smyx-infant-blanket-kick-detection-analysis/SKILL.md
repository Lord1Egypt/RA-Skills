---
name: "smyx-infant-blanket-kick-detection-analysis"
description: "Using a night-time camera (infrared or low-light) above the crib, the system analyzes in real time the coverage of the blanket on the infant's body. It checks whether the blanket coverage is below a preset threshold (e.g., 50%) or recognizes the kicking motions that cause the blanket to slip off, then outputs an alert. | 通过婴儿床夜间摄像头（红外或微光），实时分析婴儿身体及被子的覆盖情况。可联动智能家居设备（如自动调高室温、推送提醒至父母手机），预防婴儿着凉。"
version: "1.0.21"
license: "MIT-0"
---

# 🛌 Infant Blanket Kick Detection | 婴幼儿踢被/蹬被识别
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **婴幼儿踢被/蹬被识别** |
| 🎯 核心目标 | 通过婴儿床夜间摄像头（红外或微光），实时分析婴儿身体及被子的覆盖情况。可联动智能家居设备（如自动调高室温、推送提醒至父母手机），预防婴儿着凉。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_INFANT_BLANKET_KICK_DETECTION_ANALYSIS` |

Using a night-time camera (infrared or low-light) above the crib, the system analyzes in real time the coverage of the blanket on the infant's body. It checks whether the blanket coverage is below a preset threshold (e.g., 50%) or recognizes the kicking motions that cause the blanket to slip off, then outputs an alert. The skill can interoperate with smart-home devices (e.g., automatically raising the room temperature, pushing reminders to parents' phones) to help prevent the baby from getting cold. Application scenarios: infant bedrooms, neonatal monitoring rooms. The system monitors continuously at night; when the blanket is kicked off, it automatically issues an alert and advises parents to re-cover or raise the room temperature. Skill features: night-time kicking off the blanket can lead to colds, and parents need to get up frequently to check. AI automatic monitoring relieves parents and helps keep the baby comfortable. A practical add-on feature for smart baby-monitoring products.

通过婴儿床夜间摄像头（红外或微光），实时分析婴儿身体及被子的覆盖情况。检测被子覆盖面积是否小于预设阈值（如50%），或识别婴儿的踢腿动作导致被子滑落，输出预警信息。可联动智能家居设备（如自动调高室温、推送提醒至父母手机），预防婴儿着凉。应用场景：婴儿卧室、新生儿监护室。系统夜间持续监测，当被子大面积踢开时，自动发出预警并建议家长盖被或提高室温。技能特点：婴儿夜间踢被容易导致着凉感冒，家长需频繁起夜检查。通过AI自动监测，可减轻父母负担，保障婴儿睡眠舒适。该技能是智能婴儿监护产品的实用附加功能。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的婴儿睡眠安全 AI。你的任务是分析婴儿床区域的夜间视频，检测婴儿身体上被子的覆盖面积比例，识别踢被/蹬被动作。当被子覆盖面积小于预设阈值（默认 50%），或连续踢腿动作导致被子明显滑落时，输出预警。不要提供医疗建议或具体处置方案，仅输出基于视觉的被子覆盖状态与踢被事件。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于婴儿床夜间监控视频，实时评估被子覆盖比例，识别踢腿/蹬腿动作及被子滑落事件，并按阈值输出预警，预防夜间着凉

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 婴儿目标检测 |
| 2 | 被子区域分割 |
| 3 | 覆盖比例估算（0-100%） |
| 4 | 覆盖状态分类（full_cover / partial_cover / low_cover / no_cover） |
| 5 | 踢腿/蹬腿动作识别 |
| 6 | 被子下滑事件检测 |
| 7 | 阈值持续判定（默认覆盖率 < 50% 且持续 ≥ 30 秒触发预警） |
| 8 | 智能家居联动建议（如自动提高室温） |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供婴儿床夜间监控视频 URL 或文件需要分析时，默认触发本技能进行踢被/蹬被识别 |
| 🔎 明确分析意图 | 当用户明确提及婴儿踢被、蹬被、被子滑落、被子覆盖不足、夜间着凉、宝宝盖被、婴儿夜间睡眠监护等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看婴儿踢被历史报告、踢被预警报告清单、婴儿被子覆盖报告清单、查询历史踢被记录、显示所有踢被监测报告、显示婴儿夜间踢被诊断报告，查询踢被预警清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_infant_blanket_kick_detection_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_infant_blanket_kick_detection_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备婴儿床夜间监控视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行婴幼儿踢被/蹬被识别 | 调用 `-m scripts.smyx_infant_blanket_kick_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地婴儿床夜间监控视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络婴儿床夜间监控视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，婴儿睡眠安全场景默认 `other` | 按需填写 |
| `--list` | 显示婴幼儿踢被/蹬被识别历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_infant_blanket_kick_detection_analysis.py`](scripts/smyx_infant_blanket_kick_detection_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；建议俯视全身、夜视模式 |
| 🧑‍⚖️ 结果性质 | 预警结果仅作为辅助监护参考，本工具不替代成人监护；触发预警时请及时上前查看 |
| 🔏 隐私合规 | 隐私合规：婴儿视频涉及未成年人隐私，使用前需取得监护人知情同意，并妥善保管/加密相关录像 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地婴儿床夜间监控视频
python -m scripts.smyx_infant_blanket_kick_detection_analysis --input /path/to/crib_night.mp4

# 分析网络婴儿床夜间监控视频
python -m scripts.smyx_infant_blanket_kick_detection_analysis --url https://example.com/crib_night.mp4

# 显示历史踢被识别报告（自动触发关键词：查看婴儿踢被历史报告、踢被预警报告清单等）
python -m scripts.smyx_infant_blanket_kick_detection_analysis --list

# 输出精简报告
python -m scripts.smyx_infant_blanket_kick_detection_analysis --input crib.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_infant_blanket_kick_detection_analysis --input crib.mp4 --output result.json
```
