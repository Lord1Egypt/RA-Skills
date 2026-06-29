---
name: "smyx-fish-fry-growth-measurement-analysis"
description: "Through fixed cameras of fry tanks (a known-size reference object such as a scale ruler, standard coin or calibration board must be placed in the view), the system periodically (e.g. daily or weekly) captures fry images and uses AI vision analysis to measure body length (from snout to tail-fin tip, in mm), record individual growth rate (mm/day) and draw the growth curve. | 通过鱼苗缸固定摄像头（需放置已知尺寸的参照物，如刻度尺、标准硬币或标定板），定期（如每天或每周）拍摄鱼苗图像，利用 AI 视觉分析技术测量鱼苗体长（从吻端到尾鳍末端，单位 mm），记录个体的生长速率（mm/天），并绘制生长曲线。系统自动采集图像，生成生长报告，异常时提示（如生长停滞）。"
version: "1.0.3"
license: "MIT-0"
---

# 📏 Fish Fry Growth Rate Measurement (via Reference Object) | 鱼苗生长速度测量（通过参照物）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **鱼苗生长速度测量（通过参照物）** |
| 🎯 核心目标 | 通过鱼苗缸固定摄像头（需放置已知尺寸的参照物，如刻度尺、标准硬币或标定板），定期（如每天或每周）拍摄鱼苗图像，利用 AI 视觉分析技术测量鱼苗体长（从吻端到尾鳍末端，单位 mm），记录个体的生长速率（mm/天），并绘制生长曲线。系统自动采集图像，生成生长报告，异常时提示（如生长停滞）。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_FISH_FRY_GROWTH_MEASUREMENT_ANALYSIS` |

Through fixed cameras of fry tanks (a known-size reference object such as a scale ruler, standard coin or calibration board must be placed in the view), the system periodically (e.g. daily or weekly) captures fry images and uses AI vision analysis to measure body length (from snout to tail-fin tip, in mm), record individual growth rate (mm/day) and draw the growth curve. This skill helps aquaculturists or ornamental fish breeders evaluate fry health and feed conversion ratio, and timely adjust feeding strategy. Application scenarios: fry rearing tanks, aquaculture farms, ornamental fish breeding farms, laboratories. The system automatically captures images, generates growth reports, and alerts on anomalies (such as stunted growth). Skill features: growth rate is a critical indicator for fry health and feeding optimization. AI-based periodic measurement and growth-curve plotting helps farmers detect slow growth early, adjust management and improve survival rate and yield. This skill can be integrated into smart fry tanks or aquaculture management apps.

通过鱼苗缸固定摄像头（需放置已知尺寸的参照物，如刻度尺、标准硬币或标定板），定期（如每天或每周）拍摄鱼苗图像，利用 AI 视觉分析技术测量鱼苗体长（从吻端到尾鳍末端，单位 mm），记录个体的生长速率（mm/天），并绘制生长曲线。该技能有助于水产养殖者或观赏鱼繁育者评估鱼苗健康状况、饲料转化率，及时调整投喂策略。应用场景：鱼苗培育缸、水产养殖场、观赏鱼繁殖场、实验室。系统自动采集图像，生成生长报告，异常时提示（如生长停滞）。技能特点：生长速率是评估鱼苗健康、优化投喂的关键指标。通过 AI 自动定期测量并绘制生长曲线，可帮助养殖者及时发现生长迟缓问题，调整管理措施，提高成活率和产量。该技能可集成到智能鱼苗缸或养殖管理 APP 中。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的水产养殖生长监测 AI。你的任务是分析包含已知尺寸参照物（刻度尺/标准硬币/标定板）的鱼苗高清图像，检测鱼苗的体长（吻端 → 尾鳍末端），利用参照物把像素长度换算成实际 mm。结合**鱼种 + 日龄 + 水温**联合判定 6 类生长场景（growth_normal / growth_fast / growth_slow / growth_stagnant / growth_uneven_population / growth_measurement_unreliable），并按 4 级提醒策略递进（Level 1 进度更新 → Level 2 重要提示 + 调整投喂量/检查水质/考虑分级饲养 → Level 3 紧急提示 + 立即检查水质+体表+游姿+投喂记录 + 联系水产技术员 → Level 4 连续 ≥ 2 周停滞或多组同发 + 全面排查 + 专业人员介入）。**核心硬约束：参照物必须与鱼苗位于同一水平面，摄像头必须严格俯拍垂直向下**，否则透视畸变会让 mm 换算失真，必须返回 `growth_measurement_unreliable`。鱼种特异性必须按基线判定（斑马鱼 0.3-0.5mm/d / 罗非鱼 0.8-1.5mm/d / 锦鲤幼苗 0.5-1.0mm/d / 神仙鱼 0.3-0.6mm/d），**严禁通用阈值盲判**。鱼体姿态弯曲会导致体长低估，必须过滤或纠正。参照物检测置信度 < 0.8 / 多数鱼姿态弯曲 / 视野遮挡严重时必须返回 `growth_measurement_unreliable` 并建议重拍。不提供任何疾病诊断，仅输出基于视觉的体长测量值与统计；**严禁输出具体药物名称、剂量和饲料品牌推荐**（仅可中性建议如"调整粒径/调整投喂量"）；严禁伪造夸大体长 / 生长速率 / CV%；严禁越权代用户启停喂食器/加热棒/增氧/换水/灯光（仅建议）。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于鱼苗缸固定摄像头 / 智能鱼苗缸内置摄像头 / 手机微距镜头**定期拍摄**（默认每日或每周，含已知尺寸参照物）高清图像，识别 6 类生长场景（growth_normal / fast / slow / stagnant / uneven_population / signal_unreliable）→ **四组指标**：参照物校准 5 项（type / known_mm / 像素长度 / pixel_per_mm / 检测置信度）+ 鱼苗测量 7 项（吻端坐标 / 尾鳍末端坐标 / 像素长度 / 实际 mm / 测量置信度 / 姿态伸直 / fry_id）+ 群体统计 6 项（measured_count / mean / std / CV% / p10 / p50 / p90）+ 生长速率 4 项（上次测量日期 / 距上次天数 / mm/day / 生长曲线点列表）→ 4 档提醒级别（info / important / urgent / warning）→ **4 级提醒策略递进**（仅入库进度更新 → 调整投喂/分级饲养 → 紧急检查水质+体表+联系技术员 → 全面排查+专业介入）→ 单日提醒上限（Level 1 不限 / Level 2 × 2 / Level 3 × 2 / Level 4 不设上限）→ **生长报告**（按 tank_id 输出，含本次测量值 + 群体统计 + 生长曲线 + 建议动作 + 免责声明）

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 参照物自动检测与识别（直尺刻度 / 标准硬币圆形 / 棋盘格标定板） |
| 2 | **亚像素级 pixel_per_mm 校准** |
| 3 | 鱼苗目标检测 |
| 4 | 鱼苗吻端 / 尾鳍末端关键点检测 |
| 5 | 姿态弯曲过滤（脊柱曲率 > 阈值则该样本剔除或做曲线补偿） |
| 6 | 体长像素 → mm 换算 |
| 7 | 群体统计（均值 / 标准差 / CV% / 分位数） |
| 8 | 跨次时间序列存档与生长曲线绘制 |
| 9 | 鱼种自适应基线（生长速率基线表 + 日龄修正 + 水温 Q10 修正） |
| 10 | 用户 APP 推送 |
| 11 | 4 级提醒递进 |
| 12 | 单日提醒上限 |
| 13 | 生长报告（按 tank_id + 测量时间戳输出） |
| 14 | CV% 群体均匀度评估（驱动分级饲养建议） |
| 15 | 连续 ≥ 2 周 Level 3 → 强烈建议联系**当地水产养殖技术员或观赏鱼繁育专家** |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供含参照物（刻度尺/标准硬币/标定板）的鱼苗缸高清图像或视频 URL/文件需要分析时，默认触发本技能进行鱼苗生长速度测量 |
| 🔎 明确分析意图 | 当用户明确提及鱼苗体长、鱼苗生长速度、生长曲线、生长停滞、生长迟缓、CV 均匀度、分级饲养等关键词，并且上传了图像/视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看鱼苗生长历史报告、鱼苗缸生长曲线日志清单、生长停滞事件清单、查询历史鱼苗测量记录、显示所有鱼苗缸生长报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_fish_fry_growth_measurement_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_fish_fry_growth_measurement_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备含参照物的鱼苗高清图像输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 获取 open-id（强制执行） | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行鱼苗生长速度测量 | 调用 `-m scripts.smyx_fish_fry_growth_measurement_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地鱼苗缸固定摄像头含参照物的高清图像或视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络鱼苗缸固定摄像头含参照物的高清图像或视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，鱼苗生长速度测量场景默认 `other` | 按需填写 |
| `--list` | 显示鱼苗生长速度测量历史记录清单（含历次体长 + 生长曲线） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_fish_fry_growth_measurement_analysis.py`](scripts/smyx_fish_fry_growth_measurement_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 jpg/png/mp4/avi/mov，最大 10MB；**视野内必须放置已知尺寸参照物**；**严格俯拍**（参照物与鱼苗同一水平面）；分辨率 ≥ 1080p；鱼苗短暂静止或在透明计数槽中 |
| 🔎 使用提醒 | **4 级提醒策略递进**（info → important → urgent → warning），连续 ≥ 2 周停滞或多组同发进入更高级别 |
| 🔎 使用提醒 | 单日提醒上限：Level 1 不限 / Level 2 × 2 / Level 3 × 2 / Level 4 不设上限 |
| 🔎 使用提醒 | 红线约束 |
| 🧑‍⚖️ 结果性质 | **禁止**对鱼苗做"营养不良 / 肠炎 / 寄生虫 / 应激综合征 / 遗传缺陷"等具体疾病诊断 |
| 🔎 使用提醒 | **🚨 绝对禁止**输出具体药物名称、剂量、给药方案 |
| 🔎 使用提醒 | **🚨 绝对禁止**输出具体饲料品牌名称推荐（仅可中性建议如"调整粒径"、"调整投喂量"） |
| 🔎 使用提醒 | **禁止**长期存储完整鱼苗缸视频/图像（≤ 30 天，留生长曲线 + 关键测量帧；公共养殖场/实验室按管理规定） |
| 🔎 使用提醒 | **禁止**用于商业广告 / AI 训练；禁第三方共享 |
| 🔎 使用提醒 | **禁止**越权代用户启停加热棒 / 增氧 / 换水 / 喂食器 / 灯光参数；任何水族设备控制变更必须由用户确认（仅可建议） |
| 🔎 使用提醒 | **绝对禁止**伪造或夸大体长、生长速率、CV% 等指标；所有数据必须基于真实图像测量 |
| 🔎 使用提醒 | **必须**按**鱼种 + 日龄 + 水温**联合判定基线（斑马鱼 0.3-0.5mm/d / 罗非鱼 0.8-1.5mm/d / 锦鲤幼苗 0.5-1.0mm/d / 神仙鱼 0.3-0.6mm/d）；**禁止使用通用阈值盲判** |
| 🔎 使用提醒 | **必须**做透视畸变校验：参照物与鱼苗不在同一水平面 / 摄像头不垂直俯拍 → 返回 `growth_measurement_unreliable` |
| 🔎 使用提醒 | **必须**做姿态过滤：鱼体弯曲会导致体长低估，必须过滤或纠正 |
| 🔎 使用提醒 | **必须**在参照物未检出 / 检测置信度 < 0.8 / 多数鱼姿态弯曲 / 视野遮挡严重时返回 `growth_measurement_unreliable`，**禁止给出不可靠的生长停滞告警** |
| 🔎 使用提醒 | **必须**：连续 ≥ 2 周 Level 3 → 强烈建议联系**当地水产养殖技术员或观赏鱼繁育专家** |
| 📜 报告输出 | **必须**：生长报告**按 tank_id + 测量时间戳输出**，含本次测量值 + 群体统计 + 生长曲线 + 建议动作 + 免责声明 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史生长记录清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地含参照物的鱼苗高清图像（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_fish_fry_growth_measurement_analysis --input /path/to/fry.jpg

# 分析网络含参照物的鱼苗高清图像/视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_fish_fry_growth_measurement_analysis --url https://example.com/fry.jpg

# 显示历史生长测量记录清单（自动触发关键词：查看鱼苗生长历史报告、鱼苗缸生长曲线日志清单等）
python -m scripts.smyx_fish_fry_growth_measurement_analysis --list

# 输出精简报告
python -m scripts.smyx_fish_fry_growth_measurement_analysis --input fry.jpg --detail basic

# 保存结果到文件
python -m scripts.smyx_fish_fry_growth_measurement_analysis --input fry.jpg --output result.json
```
