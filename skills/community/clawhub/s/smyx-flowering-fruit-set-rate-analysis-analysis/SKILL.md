---
name: "smyx-flowering-fruit-set-rate-analysis-analysis"
description: "AI-powered flowering and fruit-set rate analysis for tomato / chili plants. From home grow-box or mobile phone images of flowering/fruit clusters, uses object-detection models to count open flowers (fully-opened corolla with visible stamens) and successfully-set young fruits (enlarged ovary, ~0.5-1cm green baby fruits), and computes fruit-set rate = young fruits / flowers × 100%. Helps growers evaluate pollination, nutrition and environmental adaptability, and guides hand-assisted pollination or water/fertilizer adjustment. Scenarios: home smart grow-boxes, greenhouses, balcony vegetable gardens. | 通过家庭种植箱或手机拍摄的植株花果图像（包含花穗、果实区域），利用AI视觉目标检测模型识别开放花朵（花冠完全展开、雄蕊可见）的数量以及已坐果的小果（子房膨大、直径约0.5-1cm的绿色幼果）数量，计算坐果率（小果数/花朵数 × 100%）。该技能帮助种植者评估授粉效果、营养状况及环境适应性，指导人工辅助授粉或调整水肥管理。应用场景：家庭智能种植箱、温室大棚、阳台菜园。"
version: "1.0.3"
license: "MIT-0"
---

# 🌼 Flowering & Fruit Set Rate Analysis | 番茄/辣椒开花坐果率分析
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **番茄/辣椒开花坐果率分析** |
| 🎯 核心目标 | 通过家庭种植箱或手机拍摄的植株花果图像（包含花穗、果实区域），利用AI视觉目标检测模型识别开放花朵（花冠完全展开、雄蕊可见）的数量以及已坐果的小果（子房膨大、直径约0.5-1cm的绿色幼果）数量，计算坐果率（小果数/花朵数 × 100%）。该技能帮助种植者评估授粉效果、营养状况及环境适应性，指导人工辅助授粉或调整水肥管理。应用场景：家庭智能种植箱、温室大棚、阳台菜园。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_FLOWERING_FRUIT_SET_RATE_ANALYSIS_ANALYSIS` |

AI-powered flowering and fruit-set rate analysis for tomato / chili plants. From home grow-box or mobile phone images of flowering/fruit clusters, uses object-detection models to count open flowers (fully-opened corolla with visible stamens) and successfully-set young fruits (enlarged ovary, ~0.5-1cm green baby fruits), and computes fruit-set rate = young fruits / flowers × 100%. Helps growers evaluate pollination, nutrition and environmental adaptability, and guides hand-assisted pollination or water/fertilizer adjustment. Scenarios: home smart grow-boxes, greenhouses, balcony vegetable gardens.

通过家庭种植箱或手机拍摄的植株花果图像（包含花穗、果实区域），利用AI视觉目标检测模型识别开放花朵（花冠完全展开、雄蕊可见）的数量以及已坐果的小果（子房膨大、直径约0.5-1cm的绿色幼果）数量，计算坐果率（小果数/花朵数 × 100%）。该技能帮助种植者评估授粉效果、营养状况及环境适应性，指导人工辅助授粉或调整水肥管理。应用场景：家庭智能种植箱、温室大棚、阳台菜园。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的园艺作物生产 AI。你的任务是分析番茄或辣椒植株的花果区域图像，检测并计数开放花朵（花冠完全展开、雄蕊可见）和已坐果的小果（子房膨大、直径约 0.5–1 cm 的绿色幼果），计算坐果率（小果数 / 花朵数 × 100%）。不要提供具体化肥用量，仅输出数量和比率。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

通过番茄 / 辣椒花果区域图像或视频进行开花及坐果率分析，输出花朵 / 幼果计数与坐果率

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 开放花朵识别与计数 |
| 2 | 已坐果小果识别与计数（子房膨大 |
| 3 | 绿色幼果） |
| 4 | 坐果率计算（小果数 / 花朵数 × 100%） |
| 5 | 坐果率等级评估（低 / 中 / 高 / 优秀） |
| 6 | 授粉与水肥调整方向建议（人工辅助授粉 / 振动授粉 / 调整温度湿度等） |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供番茄、辣椒、茄子等花果类蔬菜的花果区域图像或视频时，默认触发本技能 |
| 🔎 明确分析意图 | 当用户明确需要坐果率评估时，提及番茄坐果率、辣椒坐果率、落花、授粉不良、坐果差、幼果掉落、花朵数量、人工授粉、振动授粉、坐果监测等关键词，并且上传了图像或视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史坐果率报告、历史开花报告、坐果率趋势清单、显示所有坐果分析报告、查询花果监测记录 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_flowering_fruit_set_rate_analysis_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_flowering_fruit_set_rate_analysis_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备花果区域图像/视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行开花坐果率分析 | 调用 `-m scripts.smyx_flowering_fruit_set_rate_analysis_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地图像/视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络图像/视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，蔬果场景使用 other，默认 other | 按需填写 |
| `--list` | 显示开花坐果历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_flowering_fruit_set_rate_analysis_analysis.py`](scripts/smyx_flowering_fruit_set_rate_analysis_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 文件要求：支持 jpg/png/mp4/avi/mov 格式，最大 10MB |
| 🔎 使用提醒 | 拍摄要求：建议自然光下、距离 30-60 cm 正面拍摄花穗 / 果序，避免重叠遮挡；多角度补拍可提升计数精度 |
| 🧑‍⚖️ 结果性质 | 分析结果仅供种植决策参考，不提供具体化肥用量与农药使用方案 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📁 格式支持 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown 表格格式输出，包含"报告名称"、"作物品种"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`开花坐果率分析报告-{记录id}`形式拼接, "点击查看"列使用`[🔗 查看报告]()`格式的超链接，用户点击即可直接跳转到对应的完整报告页面。 |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地番茄/辣椒花果图像
python -m scripts.smyx_flowering_fruit_set_rate_analysis_analysis --input /path/to/tomato_flower.jpg

# 分析网络花果图像/视频
python -m scripts.smyx_flowering_fruit_set_rate_analysis_analysis --url https://example.com/chili_flower.jpg

# 显示历史分析报告/显示分析报告清单列表/显示历史坐果率报告（自动触发关键词：查看历史坐果率报告、历史报告、开花坐果报告清单等）
python -m scripts.smyx_flowering_fruit_set_rate_analysis_analysis --list

# 输出精简报告
python -m scripts.smyx_flowering_fruit_set_rate_analysis_analysis --input tomato.jpg --detail basic

# 保存结果到文件
python -m scripts.smyx_flowering_fruit_set_rate_analysis_analysis --input tomato.jpg --output result.json
```
