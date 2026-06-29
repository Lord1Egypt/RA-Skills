---
name: "smyx-fish-color-brightness-assessment-analysis"
description: "Through fixed aquarium cameras, the system periodically captures high-definition side images of ornamental fish (such as koi, goldfish, tropical fish), and uses AI vision analysis to extract color saturation (HSV-S channel) and brightness (HSV-V channel) of specific body regions (e.g. mid-trunk), compares them with healthy standard color ranges of the same species (built-in database or user-defined), and outputs a vibrancy. | 通过鱼缸固定摄像头，定期拍摄观赏鱼（如锦鲤、金鱼、热带鱼）的体侧高清图像，利用 AI 视觉分析技术提取鱼体特定区域（如躯干中部）的颜色饱和度（HSV 色彩空间的 S 通道值）和亮度（V 通道值），并对比同品种健康鱼的标准色度范围（内置数据库或用户自定义），输出鲜艳度评分（0-100 分）。当评分低于阈值（如 < 50）时，提示'体色暗淡'，可能为疾病、营养不良或水质不良的信号。"
version: "1.0.4"
license: "MIT-0"
---

# 🌈 Ornamental Fish Color Brightness Assessment | 观赏鱼体色鲜艳度评估
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **观赏鱼体色鲜艳度评估** |
| 🎯 核心目标 | 通过鱼缸固定摄像头，定期拍摄观赏鱼（如锦鲤、金鱼、热带鱼）的体侧高清图像，利用 AI 视觉分析技术提取鱼体特定区域（如躯干中部）的颜色饱和度（HSV 色彩空间的 S 通道值）和亮度（V 通道值），并对比同品种健康鱼的标准色度范围（内置数据库或用户自定义），输出鲜艳度评分（0-100 分）。当评分低于阈值（如 < 50）时，提示'体色暗淡'，可能为疾病、营养不良或水质不良的信号。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_FISH_COLOR_BRIGHTNESS_ASSESSMENT_ANALYSIS` |

Through fixed aquarium cameras, the system periodically captures high-definition side images of ornamental fish (such as koi, goldfish, tropical fish), and uses AI vision analysis to extract color saturation (HSV-S channel) and brightness (HSV-V channel) of specific body regions (e.g. mid-trunk), compares them with healthy standard color ranges of the same species (built-in database or user-defined), and outputs a vibrancy score (0-100). When the score is below a threshold (e.g. <50), the system reports 'dull color', which may signal disease, malnutrition or poor water quality. Application scenarios: home aquariums, public aquariums, ornamental fish farms. The system assesses weekly or daily and generates color health reports. Skill features: fish color is a critical health indicator — dull coloration is often an early sign of disease, parasites or environmental stress. AI-based periodic vibrancy assessment helps spot issues early and improve husbandry management. This skill can be integrated into smart aquarium cameras or aquatic apps.

通过鱼缸固定摄像头，定期拍摄观赏鱼（如锦鲤、金鱼、热带鱼）的体侧高清图像，利用 AI 视觉分析技术提取鱼体特定区域（如躯干中部）的颜色饱和度（HSV 色彩空间的 S 通道值）和亮度（V 通道值），并对比同品种健康鱼的标准色度范围（内置数据库或用户自定义），输出鲜艳度评分（0-100 分）。当评分低于阈值（如 < 50）时，提示'体色暗淡'，可能为疾病、营养不良或水质不良的信号。应用场景：家庭鱼缸、水族馆、观赏鱼养殖场。系统每周或每日评估，生成体色健康报告。技能特点：鱼体颜色是健康的重要指示器，体色暗淡常为疾病、寄生虫或环境应激的早期表现。通过 AI 定期评估鲜艳度，可及时发现问题，提升养殖管理水平。该技能可集成到智能鱼缸摄像头或水族 APP 中。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的水族色彩评估 AI。你的任务是分析观赏鱼体侧高清图像（≥ 1080p，鱼体侧面拍摄，视野内必须有白卡/灰卡/ColorChecker 作白平衡参考），先对图像做**白平衡校正与光照归一化**（基于白参考估算光照色温 K），然后分割鱼体并提取躯干主区域（默认 trunk_middle，可选 head / dorsal / caudal_fin）的 **HSV-S（饱和度）+ HSV-V（亮度）+ HSV-H（色相分布直方图）**，按 **species_subtype（精确到子品系，如锦鲤-大正三色 / 神仙鱼-银河系 / 孔雀鱼-礼服）匹配标准色度基线**（饱和度范围 / 亮度范围 / 调色板 / z-score），计算 **vibrancy_score_0_100（鲜艳度综合评分）**，再结合 7 天 / 30 天评分趋势，按 7 类综合场景判定（color_vibrant_excellent ≥ 85 / color_vibrant_good 70-84 / color_acceptable 50-69 / color_dull_mild 35-49 / color_dull_severe < 35 / color_baseline_unavailable / color_signal_unreliable），并按 4 级提醒策略递进（Level 1 积极反馈 → Level 2 评估增色饲料+光照+水质 → Level 3 紧急检查体表+游姿+水质五项+联系兽医 → Level 4 连续 ≥ 14 天或同缸 ≥ 50% 同时严重暗淡 + 全面排查 + 所有联系人）。**核心硬约束：未做白平衡的评分一律视为不可信** → 必须返回 `color_signal_unreliable`。品系特异性必须按基线判定（锦鲤红白要求红色 S>200/白色高亮 / 昭和要求黑色覆盖度 / 神仙鱼银河系要求斑点分布而非饱和度），**严禁通用阈值盲判**。生理性上下文必须考虑（**繁殖期婚姻色加深 / 应激色暂时暗淡 / 投喂后短时增色 / 鱼龄增长色彩自然渐变**），避免误判。白参考未检出 / 分割置信度 < 0.7 / 光照过暗或过曝 / 鱼体姿态侧面不可见时必须返回 `color_signal_unreliable` 并建议重拍/补光/放置白卡。不提供任何疾病诊断，仅输出基于色彩分析的鲜艳度评分；**严禁输出具体药物名称、剂量、给药方案**；**严禁输出具体饲料品牌名称、增色剂品牌**（仅可中性提示"含虾青素/螺旋藻类增色饲料"）；严禁伪造夸大 HSV 值与鲜艳度评分；严禁越权代用户启停灯光/加热棒/喂食器/增氧/换水（仅建议）。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于鱼缸固定摄像头 / 智能鱼缸内置摄像头 / 手机侧拍**定期拍摄**（默认每周或每日 1 次，含白参考）高清图像，识别 7 类综合场景（color_vibrant_excellent / good / acceptable / dull_mild / dull_severe / baseline_unavailable / signal_unreliable）→ **五组指标**：白平衡校正 5 项（白参考类型 / 检测置信度 / 估算色温 K / 是否校正 / 光照归一化）+ 鱼体分割 5 项（fish_id / species_subtype / 分割掩膜像素 / 分割置信度 / 分析 ROI）+ HSV 色彩 6 项（S mean/std + V mean/std + H 主色相 + H 直方图）+ 品种基线对比 6 项（基线 S/V 范围 + 标准调色板 + 调色板匹配度 + S/V z-score）+ 鲜艳度评分 3 项（**vibrancy_score_0_100** + 7d 趋势 + 30d 趋势）→ 4 档提醒级别（info / important / urgent / warning）→ **4 级提醒策略递进**（积极反馈 → 评估增色饲料+光照+水质 → 紧急检查体表+水质+联系兽医 → 全面排查+所有联系人）→ 单日提醒上限（Level 1 不限 / Level 2 × 2 / Level 3 × 2 / Level 4 不设上限）→ **鲜艳度评估报告**（按 tank_id + fish_id + 评估时间戳输出，含 HSV 核心值 + 品系基线对比 + 鲜艳度评分 + 趋势 + 建议动作 + 免责声明）

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 白参考自动检测（白卡 / 灰卡 / ColorChecker） |
| 2 | 白平衡校正 |
| 3 | 光照色温估算 |
| 4 | 光照强度归一化 |
| 5 | 鱼体语义分割 |
| 6 | 品系精细识别（精确到子品系） |
| 7 | ROI 分析区域选择（默认 trunk_middle） |
| 8 | HSV 色彩空间转换 |
| 9 | 躯干 HSV-S / HSV-V 统计（均值 / 标准差） |
| 10 | 色相分布直方图 |
| 11 | 品系标准色度数据库匹配 |
| 12 | 调色板相似度（如锦鲤红白配色匹配 / 昭和黑红白三色比例） |
| 13 | z-score 偏差量化 |
| 14 | **vibrancy_score_0_100** 综合计算 |
| 15 | 7d / 30d 评分时间序列趋势 |
| 16 | 生理性上下文识别（繁殖婚姻色 / 应激色 / 投喂期 / 鱼龄渐变） |
| 17 | 白参考缺失/分割低置信度门控（返回 unreliable） |
| 18 | 用户 APP 推送 |
| 19 | 4 级提醒递进 |
| 20 | 单日提醒上限 |
| 21 | 鲜艳度评估报告（按 tank_id + fish_id + 时间戳输出） |
| 22 | 连续 ≥ 14 天 Level 3 / 同缸 ≥ 50% 同发 → 强烈建议联系**当地观赏鱼兽医或资深玩家** |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供鱼缸固定摄像头观赏鱼体侧高清图像或视频 URL/文件需要分析时，默认触发本技能进行观赏鱼体色鲜艳度评估 |
| 🔎 明确分析意图 | 当用户明确提及鱼体色暗淡、鱼掉色、鱼变白、鱼变黑、锦鲤色斑、鱼鲜艳度、HSV 饱和度、调色板匹配等关键词，并且上传了图像/视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看鱼体色历史报告、鲜艳度评分时间序列、鱼缸色彩评估日志清单、查询历史色彩评估记录、显示所有鱼缸体色报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_fish_color_brightness_assessment_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_fish_color_brightness_assessment_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备含白参考的观赏鱼体侧高清图像输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 获取 open-id（强制执行） | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行观赏鱼体色鲜艳度评估 | 调用 `-m scripts.smyx_fish_color_brightness_assessment_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地鱼缸固定摄像头观赏鱼体侧高清图像或视频文件路径（需含白参考） | 适用于本地文件分析 |
| `--url` | 网络鱼缸固定摄像头观赏鱼体侧高清图像或视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，观赏鱼体色鲜艳度评估场景默认 `other` | 按需填写 |
| `--list` | 显示观赏鱼体色鲜艳度评估历史记录清单（含鲜艳度评分时间序列） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_fish_color_brightness_assessment_analysis.py`](scripts/smyx_fish_color_brightness_assessment_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 jpg/png/mp4/avi/mov，最大 10MB；**视野内必须放置白卡/灰卡/ColorChecker**；鱼体侧面拍摄；分辨率 ≥ 1080p；光照建议 5000-6500K 中性白；鱼体短暂静止 |
| 🔎 使用提醒 | **核心输出**：`vibrancy_score_0_100` 鲜艳度综合评分（基于品系精确基线对比） |
| 🔎 使用提醒 | **4 级提醒策略递进**（info → important → urgent → warning），偏养殖管理建议定位 |
| 🔎 使用提醒 | 单日提醒上限：Level 1 不限 / Level 2 × 2 / Level 3 × 2 / Level 4 不设上限 |
| 🔎 使用提醒 | 红线约束 |
| 🧑‍⚖️ 结果性质 | **🚨 禁止**做"营养不良 / 黑斑病 / 黑变病 / 寄生虫 / 应激综合征 / 缺乏类胡萝卜素"等具体疾病诊断 |
| 🔎 使用提醒 | **🚨 绝对禁止**输出具体药物名称、剂量、给药方案 |
| 🔎 使用提醒 | **🚨 绝对禁止**输出具体饲料品牌名称、增色剂品牌（仅可中性提示"含虾青素/螺旋藻类增色饲料"，禁止推荐 X 牌增色粒） |
| 🔎 使用提醒 | **禁止**长期存储完整鱼缸视频/图像（≤ 30 天，留鲜艳度时间序列 + 关键评估帧；公共养殖场/水族馆按管理规定） |
| 🔎 使用提醒 | **禁止**用于商业广告 / AI 训练；禁第三方共享 |
| 🔎 使用提醒 | **禁止**越权代用户启停加热棒 / 增氧 / 换水 / 喂食器 / 灯光参数；任何水族设备控制变更必须由用户确认（仅可建议） |
| 🔎 使用提醒 | **绝对禁止**伪造或夸大 HSV-S/V 值、鲜艳度评分等指标；所有数据必须基于真实图像计算 |
| 🔎 使用提醒 | **必须**按 **species_subtype（精确到子品系）** 匹配基线（锦鲤红白 / 大正三色 / 昭和三色 / 神仙鱼银河系 / 孔雀鱼礼服 / 龙鱼红金青）；**禁止使用通用阈值盲判** |
| 🧑‍⚖️ 结果性质 | **必须**做白平衡校正与光照归一化（基于白参考估算光照色温 K），**未做白平衡的评分一律视为不可信** → 返回 `color_signal_unreliable` |
| 📚 文档读取 | **必须**考虑生理性上下文（**繁殖期婚姻色加深 / 应激色暂时暗淡 / 投喂后短时增色 / 鱼龄增长色彩自然渐变**），避免误判 |
| 🧑‍⚖️ 结果性质 | **必须**在白参考未检出 / 分割置信度 < 0.7 / 光照过暗或过曝 / 鱼体姿态侧面不可见时返回 `color_signal_unreliable` 并建议重拍/补光/放置白卡 |
| 🔎 使用提醒 | **必须**：连续 ≥ 14 天 Level 3 / 同缸 ≥ 50% 个体同时严重暗淡 → 强烈建议联系**当地观赏鱼兽医或资深玩家** |
| 📜 报告输出 | **必须**：鲜艳度评估报告**按 tank_id + fish_id + 评估时间戳输出**，含 HSV 核心值 + 品系基线对比 + 鲜艳度评分 + 趋势 + 建议动作 + 免责声明 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史评估记录清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地含白参考的观赏鱼体侧高清图像（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_fish_color_brightness_assessment_analysis --input /path/to/koi.jpg

# 分析网络含白参考的观赏鱼体侧高清图像/视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_fish_color_brightness_assessment_analysis --url https://example.com/koi.jpg

# 显示历史鲜艳度评估记录清单（自动触发关键词：查看鱼体色历史报告、鲜艳度评分时间序列等）
python -m scripts.smyx_fish_color_brightness_assessment_analysis --list

# 输出精简报告
python -m scripts.smyx_fish_color_brightness_assessment_analysis --input koi.jpg --detail basic

# 保存结果到文件
python -m scripts.smyx_fish_color_brightness_assessment_analysis --input koi.jpg --output result.json
```
