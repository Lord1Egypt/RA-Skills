---
name: "smyx-chinese-herbal-ingredient-trend-analysis"
description: "AI-powered active-ingredient accumulation trend assessment for medicinal herbs (e.g. honeysuckle, wolfberry, astragalus, danshen). Uses high-resolution leaf images captured by fixed cameras or drones in TCM cultivation bases, analyzes leaf color saturation, hue angle, relative chlorophyll content (estimated via color indices) and leaf thickness (inferred from edge focus / silhouette), and compares against the cultivar's standard reference atlas (typical features at peak active-ingredient stage) to output an accumulation trend level (Low / Medium / High / Peak). Helps determine the optimal harvest window and improve herb quality. Scenarios: TCM planting bases, GAP bases, herb cooperatives, raw-material bases for pharmaceutical companies. | 通过中药种植基地的固定摄像头或无人机拍摄药用植物（如金银花、枸杞、黄芪、丹参等）叶片的高清图像，利用AI视觉分析技术评估叶片颜色饱和度、色相角、叶绿素相对含量（通过颜色指数估算）以及叶片厚度（通过边缘聚焦或侧影估算），与品种标准图谱（特定生长阶段/有效成分积累峰值期的典型特征）进行对比，输出有效成分积累趋势等级（低/中/高/峰值）。该技能有助于确定最佳采收期，提高药材品质。应用场景：中药种植基地、GAP种植基地、中药材合作社、药企原料基地。"
version: "1.0.3"
license: "MIT-0"
---

# 🌿 Chinese Herbal Active Ingredient Trend Analysis | 中草药有效成分积累趋势评估
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **中草药有效成分积累趋势评估** |
| 🎯 核心目标 | 通过中药种植基地的固定摄像头或无人机拍摄药用植物（如金银花、枸杞、黄芪、丹参等）叶片的高清图像，利用AI视觉分析技术评估叶片颜色饱和度、色相角、叶绿素相对含量（通过颜色指数估算）以及叶片厚度（通过边缘聚焦或侧影估算），与品种标准图谱（特定生长阶段/有效成分积累峰值期的典型特征）进行对比，输出有效成分积累趋势等级（低/中/高/峰值）。该技能有助于确定最佳采收期，提高药材品质。应用场景：中药种植基地、GAP种植基地、中药材合作社、药企原料基地。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_CHINESE_HERBAL_INGREDIENT_TREND_ANALYSIS` |

AI-powered active-ingredient accumulation trend assessment for medicinal herbs (e.g. honeysuckle, wolfberry, astragalus,
danshen). Uses high-resolution leaf images captured by fixed cameras or drones in TCM cultivation bases, analyzes leaf
color saturation, hue angle, relative chlorophyll content (estimated via color indices) and leaf thickness (inferred
from edge focus / silhouette), and compares against the cultivar's standard reference atlas (typical features at peak
active-ingredient stage) to output an accumulation trend level (Low / Medium / High / Peak). Helps determine the optimal
harvest window and improve herb quality. Scenarios: TCM planting bases, GAP bases, herb cooperatives, raw-material bases
for pharmaceutical companies.

通过中药种植基地的固定摄像头或无人机拍摄药用植物（如金银花、枸杞、黄芪、丹参等）叶片的高清图像，利用AI视觉分析技术评估叶片颜色饱和度、色相角、叶绿素相对含量（通过颜色指数估算）以及叶片厚度（通过边缘聚焦或侧影估算），与品种标准图谱（特定生长阶段/有效成分积累峰值期的典型特征）进行对比，输出有效成分积累趋势等级（低/中/高/峰值）。该技能有助于确定最佳采收期，提高药材品质。应用场景：中药种植基地、GAP种植基地、中药材合作社、药企原料基地。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的中草药栽培与质量评价 AI。你的任务是分析药用植物叶片的高清图像，评估叶片颜色饱和度、绿色深度（或红/黄/蓝色相）、叶绿素指数（如归一化植被指数模拟值）以及叶片厚度（可通过叶缘清晰度/聚焦深度间接推断），并与该品种的标准参考图谱（含有效成分积累高峰期的典型特征）进行比对，输出当前有效成分积累趋势等级。不要提供化学检测数据，仅基于视觉特征给出预测。 ** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

通过药用植物叶片的高清图像/视频进行有效成分积累趋势评估，输出趋势等级与采收时机建议

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 叶片颜色饱和度评估 |
| 2 | 色相角分析 |
| 3 | 叶绿素相对含量估算（颜色指数模拟） |
| 4 | 叶片厚度间接推断（边缘聚焦/侧影） |
| 5 | 与品种标准图谱比对 |
| 6 | 有效成分积累趋势等级判定（低 / |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供药用植物（金银花 / 枸杞 / 黄芪 / 丹参 / 三七 / 黄芩 / 板蓝根等）叶片的图像或视频需要趋势评估时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要采收时机评估时，提及中药材、药用植物、有效成分、采收期、GAP 基地、金银花、枸杞、黄芪、丹参、叶绿素含量、品质趋势、最佳采收等关键词，并且上传了图像或视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史中药趋势报告、历史有效成分报告、中药材趋势清单、显示所有采收期评估报告、查询药材趋势记录 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_chinese_herbal_ingredient_trend_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_chinese_herbal_ingredient_trend_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备药用植物叶片图像/视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行趋势评估分析 | 调用 `-m scripts.smyx_chinese_herbal_ingredient_trend_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地图像/视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络图像/视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，中药材场景使用 other，默认 other | 按需填写 |
| `--list` | 显示有效成分趋势历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_chinese_herbal_ingredient_trend_analysis.py`](scripts/smyx_chinese_herbal_ingredient_trend_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 文件要求：支持 jpg/png/mp4/avi/mov 格式，最大 10MB |
| 🔎 使用提醒 | 拍摄要求：建议在晴朗自然光下、避免强反光，叶片正面平展、聚焦清晰；同一植株多期对比效果最佳 |
| 🧑‍⚖️ 结果性质 | 分析结果仅供采收决策参考，正式品质评定请配合 HPLC / 国标 / 药典等专业化学检测 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地药用植物叶片图像/视频
python -m scripts.smyx_chinese_herbal_ingredient_trend_analysis --input /path/to/herb_leaf.jpg

# 分析网络药用植物叶片图像/视频
python -m scripts.smyx_chinese_herbal_ingredient_trend_analysis --url https://example.com/herb_leaf.jpg

# 显示历史分析报告/显示分析报告清单列表/显示历史中药趋势报告（自动触发关键词：查看历史中药趋势报告、历史报告、有效成分趋势清单等）
python -m scripts.smyx_chinese_herbal_ingredient_trend_analysis --list

# 输出精简报告
python -m scripts.smyx_chinese_herbal_ingredient_trend_analysis --input herb.jpg --detail basic

# 保存结果到文件
python -m scripts.smyx_chinese_herbal_ingredient_trend_analysis --input herb.jpg --output result.json
```
