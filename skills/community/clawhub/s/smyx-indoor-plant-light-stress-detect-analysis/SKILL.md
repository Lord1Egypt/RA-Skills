---
name: "smyx-indoor-plant-light-stress-detect-analysis"
description: "AI-powered indoor plant light stress detection from smart planter or fixed camera images (optionally combined with light sensor lux data). Detects morphological anomalies caused by low light (elongated internodes / etiolation, thin leaves, pale green color) or strong-light damage (leaf burn spots, scorched edges, curling, bleaching). Combined with optional lux sensor readings, it determines the current light stress type (insufficient / excessive / normal) and outputs adjustment suggestions (e.g. move to window, add shading, adjust grow-light duration). Scenarios: smart planters, indoor green plant care, home gardening, office plants. | 通过智能花盆或固定摄像头拍摄植物整体图像（也可选配光照传感器数据），利用AI视觉分析技术检测植物因光照不足引起的形态异常（如茎节间距拉长—徒长、叶片变薄、颜色浅绿）或因光照过强引起的损伤（叶片灼伤斑、焦边、卷曲、褪绿）。结合可选的光照传感器实时数据（勒克斯值），综合判断植物当前所受的光照胁迫类型（不足/过强/正常），并输出光照调整建议（如"增加光照，可移至窗边""遮阴，避免直射光"）。应用场景：智能花盆、室内绿植养护、家庭园艺、办公室植物。"
version: "1.0.1"
license: "MIT-0"
---

# ☀️ Indoor Plant Light Stress Detection | 室内植物光照不足/过强识别
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **室内植物光照不足/过强识别** |
| 🎯 核心目标 | 通过智能花盆或固定摄像头拍摄植物整体图像（也可选配光照传感器数据），利用AI视觉分析技术检测植物因光照不足引起的形态异常（如茎节间距拉长—徒长、叶片变薄、颜色浅绿）或因光照过强引起的损伤（叶片灼伤斑、焦边、卷曲、褪绿）。结合可选的光照传感器实时数据（勒克斯值），综合判断植物当前所受的光照胁迫类型（不足/过强/正常），并输出光照调整建议（如"增加光照，可移至窗边""遮阴，避免直射光"）。应用场景：智能花盆、室内绿植养护、家庭园艺、办公室植物。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_INDOOR_PLANT_LIGHT_STRESS_DETECT_ANALYSIS` |

AI-powered indoor plant light stress detection from smart planter or fixed camera images (optionally combined with light
sensor lux data). Detects morphological anomalies caused by low light (elongated internodes / etiolation, thin leaves,
pale green color) or strong-light damage (leaf burn spots, scorched edges, curling, bleaching). Combined with optional
lux sensor readings, it determines the current light stress type (insufficient / excessive / normal) and outputs
adjustment suggestions (e.g. move to window, add shading, adjust grow-light duration). Scenarios: smart planters, indoor
green plant care, home gardening, office plants.

通过智能花盆或固定摄像头拍摄植物整体图像（也可选配光照传感器数据），利用AI视觉分析技术检测植物因光照不足引起的形态异常（如茎节间距拉长—徒长、叶片变薄、颜色浅绿）或因光照过强引起的损伤（叶片灼伤斑、焦边、卷曲、褪绿）。结合可选的光照传感器实时数据（勒克斯值），综合判断植物当前所受的光照胁迫类型（不足/过强/正常），并输出光照调整建议（如"
增加光照，可移至窗边""遮阴，避免直射光"）。应用场景：智能花盆、室内绿植养护、家庭园艺、办公室植物。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | * *假设你是一个专业的植物光环境健康AI。你的任务是分析室内植物的图像（整体形态及叶片细节），检测因光照不足导致的徒长特征（茎节间距拉长、叶片稀疏、叶色浅绿）或因光照过强导致的灼伤特征（叶片黄褐色枯斑、焦边、卷曲、叶面白化），并可结合可选的光照传感器数据（勒克斯 lux 值），综合评估光照胁迫状态（不足 / 正常 / 过强），输出调整建议。不要提供具体设备参数，仅输出基于视觉（及可选传感器）的判断。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

通过室内植物的整体图像或视频进行光照胁迫识别，结合可选的环境光 lux 数据，输出光照胁迫类型评估及调整建议

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 徒长特征识别（节间拉长 / 叶片稀疏 / 颜色浅绿 / 弯向光源） |
| 2 | 强光灼伤识别（黄褐色枯斑 / 焦边 / 卷曲 / |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供室内植物的整体图像或视频需要光照诊断时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要光照胁迫诊断时，提及植物徒长、节间拉长、叶子变薄、叶色变浅、叶片灼伤、焦边、晒伤、白化、阳光太强、光照不足、补光灯、智能花盆光照等关键词，并且上传了图像或视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史光照报告、历史植物光照报告、光照胁迫报告清单、显示所有光照诊断报告、查询植物光环境记录 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_indoor_plant_light_stress_detect_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_indoor_plant_light_stress_detect_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备植物图像/视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行光照胁迫分析 | 调用 `-m scripts.smyx_indoor_plant_light_stress_detect_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地图像/视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络图像/视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，植物场景使用 other，默认 other | 按需填写 |
| `--list` | 显示光照胁迫历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_indoor_plant_light_stress_detect_analysis.py`](scripts/smyx_indoor_plant_light_stress_detect_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 文件要求：支持 jpg/png/mp4/avi/mov 格式，最大 10MB |
| 🔎 使用提醒 | 拍摄要求：建议拍摄植物整体及叶片特写两类画面，自然光或常规室内灯光下拍摄，避免过曝/过暗影响判断 |
| 🧑‍⚖️ 结果性质 | 分析结果仅供养护参考，不提供具体设备/补光产品型号建议 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地室内植物图像/视频
python -m scripts.smyx_indoor_plant_light_stress_detect_analysis --input /path/to/plant.jpg

# 分析网络植物图像/视频
python -m scripts.smyx_indoor_plant_light_stress_detect_analysis --url https://example.com/plant.jpg

# 显示历史分析报告/显示分析报告清单列表/显示历史光照报告（自动触发关键词：查看历史光照报告、历史报告、光照胁迫报告清单等）
python -m scripts.smyx_indoor_plant_light_stress_detect_analysis --list

# 输出精简报告
python -m scripts.smyx_indoor_plant_light_stress_detect_analysis --input plant.jpg --detail basic

# 保存结果到文件
python -m scripts.smyx_indoor_plant_light_stress_detect_analysis --input plant.jpg --output result.json
```
