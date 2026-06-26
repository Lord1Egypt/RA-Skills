---
name: "smyx-transpiration-rate-estimation-analysis"
description: "AI-powered transpiration rate estimation for indoor plants. From smart planters or fixed cameras, uses thermal infrared images of leaves (preferred) — or regular RGB images combined with ambient temperature/humidity — to estimate the leaf-to-air temperature difference, combines radiation/humidity parameters (sensor or model-inferred), and computes a relative transpiration rate index (0-100%). Transpiration rate correlates with root water-uptake activity, indirectly reflecting root health and water transport capacity. Helps determine whether the plant is water-stressed, has damaged roots, or is under environmental stress. Scenarios: smart planters, indoor green plant care, plant factories, research greenhouses. | 通过智能花盆或固定摄像头采集植物叶片的红外热成像图像（或普通RGB图像结合环境温湿度数据），利用AI模型估算叶片温度与空气温度的差值，结合辐射、湿度等参数（可由传感器提供或模型内估），计算植物蒸腾速率的相对值（0-100%）。蒸腾速率与根系吸水活力正相关，可间接反映根系健康及水分输送能力。该技能有助于判断植物是否缺水、根系受损或环境胁迫。应用场景：智能花盆、室内绿植养护、植物工厂、科研温室。"
version: "1.0.1"
license: "MIT-0"
---

# 💧 Transpiration Rate Estimation | 室内绿植蒸腾速率估算
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **室内绿植蒸腾速率估算** |
| 🎯 核心目标 | 通过智能花盆或固定摄像头采集植物叶片的红外热成像图像（或普通RGB图像结合环境温湿度数据），利用AI模型估算叶片温度与空气温度的差值，结合辐射、湿度等参数（可由传感器提供或模型内估），计算植物蒸腾速率的相对值（0-100%）。蒸腾速率与根系吸水活力正相关，可间接反映根系健康及水分输送能力。该技能有助于判断植物是否缺水、根系受损或环境胁迫。应用场景：智能花盆、室内绿植养护、植物工厂、科研温室。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_TRANSPIRATION_RATE_ESTIMATION_ANALYSIS` |

AI-powered transpiration rate estimation for indoor plants. From smart planters or fixed cameras, uses thermal infrared images of leaves (preferred) — or regular RGB images combined with ambient temperature/humidity — to estimate the leaf-to-air temperature difference, combines radiation/humidity parameters (sensor or model-inferred), and computes a relative transpiration rate index (0-100%). Transpiration rate correlates with root water-uptake activity, indirectly reflecting root health and water transport capacity. Helps determine whether the plant is water-stressed, has damaged roots, or is under environmental stress. Scenarios: smart planters, indoor green plant care, plant factories, research greenhouses.

通过智能花盆或固定摄像头采集植物叶片的红外热成像图像（或普通RGB图像结合环境温湿度数据），利用AI模型估算叶片温度与空气温度的差值，结合辐射、湿度等参数（可由传感器提供或模型内估），计算植物蒸腾速率的相对值（0-100%）。蒸腾速率与根系吸水活力正相关，可间接反映根系健康及水分输送能力。该技能有助于判断植物是否缺水、根系受损或环境胁迫。应用场景：智能花盆、室内绿植养护、植物工厂、科研温室。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的植物生理 AI。你的任务是分析植物叶片的图像（热成像优先，或普通 RGB 结合环境温湿度），估算叶片-空气温差，并基于能量平衡原理估算蒸腾速率的相对值（0-100%），进而推断根系吸水活力。不要提供土壤水分具体数值，仅输出蒸腾速率指数和活力评估。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

通过室内植物叶片的红外热成像（优先）或 RGB 图像 + 可选环境温湿度数据，估算蒸腾速率相对值（0-100%），并推断根系吸水活力

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 叶片温度估算（热成像直接读取 / RGB 模型推断） |
| 2 | 叶片-空气温差计算 |
| 3 | 能量平衡蒸腾速率建模 |
| 4 | 蒸腾速率指数（0-100%） |
| 5 | 根系吸水活力等级（强 / 正常 / 偏弱 / 受阻） |
| 6 | 可能的胁迫类型提示（缺水 / 根系受损 / 高温高湿降低蒸腾 / 通风不足） |
| 7 | 养护方向建议 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供室内植物叶片的热成像图或普通 RGB 图像（可选附带环境温湿度数据）需要蒸腾分析时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要蒸腾 / 水分状态评估时，提及蒸腾速率、叶温、热成像、根系吸水、植物缺水预警、水分胁迫、根系活力、智能花盆水分等关键词，并且上传了图像或视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史蒸腾报告、历史蒸腾速率报告、蒸腾趋势清单、显示所有蒸腾分析报告、查询植物水分诊断记录 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_transpiration_rate_estimation_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_transpiration_rate_estimation_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备植物叶片图像/视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行蒸腾速率估算 | 调用 `-m scripts.smyx_transpiration_rate_estimation_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地图像/视频文件路径（热成像或 RGB） | 适用于本地文件分析 |
| `--url` | 网络图像/视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，植物场景使用 other，默认 other | 按需填写 |
| `--list` | 显示蒸腾速率历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_transpiration_rate_estimation_analysis.py`](scripts/smyx_transpiration_rate_estimation_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 文件要求：支持 jpg/png/mp4/avi/mov 格式，最大 10MB；热成像建议使用伪彩或可解码的辐射图 |
| 🔎 使用提醒 | 拍摄要求：固定机位、稳定光照时段采集；尽量避免热源干扰（暖气、灯具直射、玻璃反射） |
| 🧑‍⚖️ 结果性质 | 分析结果仅供养护参考，不提供土壤水分具体数值；持续异常建议结合土壤水分计或根系检查 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📁 格式支持 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown 表格格式输出，包含"报告名称"、"植物类别"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`蒸腾速率估算报告-{记录id}`形式拼接, "点击查看"列使用`[🔗 查看报告](reportImageUrl)`格式的超链接，用户点击即可直接跳转到对应的完整报告页面。 |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地热成像/RGB 叶片图像
python -m scripts.smyx_transpiration_rate_estimation_analysis --input /path/to/leaf_thermal.jpg

# 分析网络图像/视频
python -m scripts.smyx_transpiration_rate_estimation_analysis --url https://example.com/leaf.jpg

# 显示历史分析报告/显示分析报告清单列表/显示历史蒸腾报告（自动触发关键词：查看历史蒸腾报告、历史报告、蒸腾速率清单等）
python -m scripts.smyx_transpiration_rate_estimation_analysis --list

# 输出精简报告
python -m scripts.smyx_transpiration_rate_estimation_analysis --input leaf.jpg --detail basic

# 保存结果到文件
python -m scripts.smyx_transpiration_rate_estimation_analysis --input leaf.jpg --output result.json
```
