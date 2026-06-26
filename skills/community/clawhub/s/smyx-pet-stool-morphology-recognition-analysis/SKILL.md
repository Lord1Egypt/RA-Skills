---
name: "smyx-pet-stool-morphology-recognition-analysis"
description: "Triggers when a user provides an image/video URL or file of dog toilet area or outdoor dog-walking path for analysis; supports local uploads or network URLs to call server-side APIs for pet stool morphology recognition, analyzing stool color (brown, black, red, white), shape (formed, loose/soft, watery, granular hard), and the presence of blood or mucus, outputting standardized abnormal observation features to help early discovery of gastrointestinal diseases (without diagnosing diseases). Application scenarios: dog toilets, outdoor dog-walking path cameras, pet health monitoring, multi-pet households. | 当用户提供狗厕所或户外遛狗路径区域的粪便图像/视频时，触发本技能进行排便形态识别分析；支持通过上传本地文件或网络URL，调用服务端API识别粪便颜色（棕、黑、红、白）、形状（条状、稀糊、颗粒）、是否带血或粘液，输出异常特征观察结果，帮助早期发现肠胃疾病（不诊断疾病）。应用场景：狗厕所、遛狗路径摄像头、宠物健康监测、多宠家庭。"
version: "1.0.3"
license: "MIT-0"
---

# 💩 Pet Stool Morphology Recognition Analysis | 宠物排便形态识别（狗厕所/户外）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **宠物排便形态识别（狗厕所/户外）** |
| 🎯 核心目标 | 当用户提供狗厕所或户外遛狗路径区域的粪便图像/视频时，触发本技能进行排便形态识别分析；支持通过上传本地文件或网络URL，调用服务端API识别粪便颜色（棕、黑、红、白）、形状（条状、稀糊、颗粒）、是否带血或粘液，输出异常特征观察结果，帮助早期发现肠胃疾病（不诊断疾病）。应用场景：狗厕所、遛狗路径摄像头、宠物健康监测、多宠家庭。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_PET_STOOL_MORPHOLOGY_RECOGNITION_ANALYSIS` |

Triggers when a user provides an image/video URL or file of dog toilet area or outdoor dog-walking path for analysis;
supports local uploads or network URLs to call server-side APIs for pet stool morphology recognition, analyzing stool
color (brown, black, red, white), shape (formed, loose/soft, watery, granular hard), and the presence of blood or mucus,
outputting standardized abnormal observation features to help early discovery of gastrointestinal diseases (without
diagnosing diseases). Application scenarios: dog toilets, outdoor dog-walking path cameras, pet health monitoring,
multi-pet households.

当用户提供狗厕所或户外遛狗路径区域的粪便图像/视频时，触发本技能进行排便形态识别分析；支持通过上传本地文件或网络URL，调用服务端API识别粪便颜色（棕、黑、红、白）、形状（条状、稀糊、颗粒）、是否带血或粘液，输出异常特征观察结果，帮助早期发现肠胃疾病（不诊断疾病）。应用场景：狗厕所、遛狗路径摄像头、宠物健康监测、多宠家庭。

## 🤖 AI 角色 | AI Role
**你是一个专业的宠物健康监测AI。你的任务是基于宠物排便区域的图像或视频帧，分析粪便的形态特征（颜色、形状、有无带血或粘液），输出标准化观察结果。不要提供疾病诊断或治疗方案，仅客观描述粪便外观。
**

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/guide.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

通过狗厕所或户外遛狗路径区域的图像/视频进行宠物排便形态识别分析，获取标准化的观察结果和异常特征提示，帮助早期发现肠胃疾病

### 2. 🛠️ 能力范围

| 能力类型 | 具体能力 |
|---|---|
| 能力 1 | 图像/视频分析 |
| 能力 2 | 粪便颜色识别（棕 |
| 能力 3 | 黑 |
| 能力 4 | 红 |
| 能力 5 | 白） |
| 能力 6 | 粪便形状识别（条状 |
| 能力 7 | 稀糊 |
| 能力 8 | 颗粒） |
| 能力 9 | 带血/粘液检测 |
| 能力 10 | 异常特征输出 |
| 能力 11 | 肠胃健康风险提示 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供狗厕所或户外遛狗路径区域的图像/视频 URL 或文件需要分析时，默认触发本技能进行排便形态识别 |
| 🔎 明确分析意图 | 当用户明确需要进行宠物排便监测时，提及狗厕所、遛狗、户外排便、粪便分析、粪便颜色、粪便形状、便血、粘液便、稀便、肠胃异常等关键词，并且上传了图片/视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史排便报告、历史排便形态报告、排便分析报告清单、查询排便记录、显示所有狗厕所报告、显示排便形态识别报告，查询肠胃健康风险提示报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_pet_stool_morphology_recognition_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_pet_stool_morphology_recognition_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备图像/视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行排便形态识别分析 | 调用 `-m scripts.smyx_pet_stool_morphology_recognition_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地图像/视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络图像/视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 宠物类型，可选值：cat/dog/other，默认 dog | 按需填写 |
| `--list` | 显示宠物排便形态历史分析报告列表清单（可输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_pet_stool_morphology_recognition_analysis.py`](scripts/smyx_pet_stool_morphology_recognition_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 文件要求：支持 jpg/jpeg/png/bmp/webp 图像 与 mp4/avi/mov 视频，最大 10MB |
| 🧑‍⚖️ 结果性质 | 分析结果仅供健康参考，不提供疾病诊断或治疗建议 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 `reportImageUrl` 作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地狗厕所/户外排便图像或视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_pet_stool_morphology_recognition_analysis --input /path/to/dog_stool.jpg --pet-type dog

# 分析网络狗厕所/户外排便视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_pet_stool_morphology_recognition_analysis --url https://example.com/dog_stool.mp4 --pet-type dog

# 显示历史分析报告清单（自动触发关键词：查看历史排便报告、排便形态报告清单等）
python -m scripts.smyx_pet_stool_morphology_recognition_analysis --list

# 输出精简报告
python -m scripts.smyx_pet_stool_morphology_recognition_analysis --input dog_stool.jpg --pet-type dog --detail basic

# 保存结果到文件
python -m scripts.smyx_pet_stool_morphology_recognition_analysis --input dog_stool.jpg --pet-type dog --output result.json
```
