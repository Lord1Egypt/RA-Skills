---
name: "smyx-depression-behavioral-markers-analysis"
description: "Using fixed home cameras (bedroom and dining area), the system analyzes the multi-day behavior pattern of elderly people or solo-living individuals, detecting daily lying-in-bed duration (continuous lying > 20 hours per day) and a sharp drop in eating frequency / duration (e.g., daily eating-action count below 50% of personal baseline). | 通过家庭固定摄像头（卧室和餐厅区域），分析老年人或独居者连续多日的行为模式，检测卧床时长（连续卧床超过20小时/天）以及进食频次/时长骤减（如每日进食动作次数低于历史基线的50%）。当这些行为变化持续超过设定天数（如3天）时，输出行为变化报告，提醒家属或社区医生关注可能存在的抑郁倾向或其他健康问题。"
version: "1.0.3"
license: "MIT-0"
---

# 🌧️ Depression Behavioral Markers (Long Immobility & Appetite Change) | 抑郁症辅助行为标记（长时间不动、食欲改变）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **抑郁症辅助行为标记（长时间不动、食欲改变）** |
| 🎯 核心目标 | 通过家庭固定摄像头（卧室和餐厅区域），分析老年人或独居者连续多日的行为模式，检测卧床时长（连续卧床超过20小时/天）以及进食频次/时长骤减（如每日进食动作次数低于历史基线的50%）。当这些行为变化持续超过设定天数（如3天）时，输出行为变化报告，提醒家属或社区医生关注可能存在的抑郁倾向或其他健康问题。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_DEPRESSION_BEHAVIORAL_MARKERS_ANALYSIS` |

Using fixed home cameras (bedroom and dining area), the system analyzes the multi-day behavior pattern of elderly people or solo-living individuals, detecting daily lying-in-bed duration (continuous lying > 20 hours per day) and a sharp drop in eating frequency / duration (e.g., daily eating-action count below 50% of personal baseline). When these behavioral changes persist beyond a configured threshold (e.g., 3 days), the system outputs a behavioral-change report to remind family members or community doctors about possible depressive tendency or other health issues. This skill is ONLY a behavioral-observation aid and is NOT a medical diagnostic tool. Application scenarios: solo-living elderly homes, remote mental-health monitoring, community elderly care. The system generates a daily behavior summary and pushes alerts when an abnormal pattern is detected. Skill features: depression in the elderly often presents as decreased activity, reduced appetite, and increased bed time. AI auto-monitoring of these behavior changes can issue early signals before family or doctors notice, supporting timely intervention, reducing suicide risk, and improving quality of life. Can be integrated into home-care cameras or health-management platforms as a practical mental-health monitoring tool.

通过家庭固定摄像头（卧室和餐厅区域），分析老年人或独居者连续多日的行为模式，检测卧床时长（连续卧床超过20小时/天）以及进食频次/时长骤减（如每日进食动作次数低于历史基线的50%）。当这些行为变化持续超过设定天数（如3天）时，输出行为变化报告，提醒家属或社区医生关注可能存在的抑郁倾向或其他健康问题。该技能仅为行为观察辅助工具，不作为医学诊断依据。应用场景：独居老人家庭、精神健康远程监测、社区养老。系统每日生成行为摘要，当检测到异常行为模式时推送提醒。技能特点：老年人抑郁症常表现为活动减少、食欲下降、卧床时间增多。通过AI自动监测这些行为变化，可在家属或医生尚未察觉时发出早期信号，有助于及时干预，降低自杀风险，改善生活质量。该技能可集成到居家养老摄像头或健康管理平台中，成为精神健康监测的实用工具。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的老年人行为健康监测 AI。你的任务是分析家庭固定摄像头（卧室和餐厅区域）的连续视频（至少 24 小时），检测卧床时长（统计一天内卧床总时长）以及进食行为（识别手部抓握餐具送入口中的动作次数和时长）。对比历史基线（过去 7-14 天的个人平均数据），当卧床时长超过 20 小时/天或进食动作次数/时长低于基线的 50% 时，输出行为变化报告。不要提供医疗诊断，仅输出基于视觉的行为统计和变化提示。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于家庭卧室 + 餐厅双区域固定摄像头连续 ≥ 24 小时视频，统计每日卧床总时长 + 离床事件次数 + 进食动作次数 + 进食总时长 + 完整餐次数 → 与个人 7-14 天基线对比 → 连续异常 ≥ 3 天 → 输出行为变化报告 + 家属/社区医生友好提醒

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 人体检测 + 床位 ROI 卧位识别（lying_in_bed_duration_daily_min） |
| 2 | 离床事件计数 |
| 3 | 手部抓握餐具送入口动作识别（eating_action_count_daily） |
| 4 | 餐次数与进食总时长统计 |
| 5 | 餐后剩余食物比例估计（参考） |
| 6 | 个人 7-14 天基线均值/标准差计算 |
| 7 | 连续异常天数累计 |
| 8 | 行为异常模式分类（hypersomnia_immobility / appetite_loss / both / none） |
| 9 | 风险信号等级判定（none → strong_signal） |
| 10 | 家属/社区医生友好提醒文本生成 |
| 11 | 心理援助热线参考 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供家庭卧室 + 餐厅区域固定摄像头连续 ≥ 24 小时视频 URL 或文件需要分析时，默认触发本技能进行抑郁症辅助行为标记分析 |
| 🔎 明确分析意图 | 当用户明确提及老年人抑郁、长时间卧床、食欲下降、不爱吃饭、整天躺着、活动减少、精神健康远程监测、社区养老心理等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看抑郁行为标记历史报告、卧床/食欲变化报告清单、行为变化报告清单、查询历史行为变化记录、显示所有抑郁辅助行为报告、显示精神健康行为诊断报告，查询抑郁辅助预警清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_depression_behavioral_markers_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_depression_behavioral_markers_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备家庭卧室 + 餐厅区域固定摄像头连续视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行抑郁症辅助行为标记分析 | 调用 `-m scripts.smyx_depression_behavioral_markers_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地家庭固定摄像头（卧室+餐厅区域，≥24h）视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络家庭固定摄像头（卧室+餐厅区域，≥24h）视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，老年人行为健康监测场景默认 `other` | 按需填写 |
| `--list` | 显示抑郁症辅助行为标记历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_depression_behavioral_markers_analysis.py`](scripts/smyx_depression_behavioral_markers_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频；**关键约束**：单次分析必须 ≥ 24 小时连续记录，且必须同时覆盖卧室与餐厅 |
| 🔎 使用提醒 | 单日感冒、发烧、近期手术康复期、外出旅行等情形会显著影响卧床与进食指标，建议在配置中标记"非常态期"以暂停告警 |
| 🔎 使用提醒 | 老人在外用餐（如子女家、社区食堂）会导致 eating_action_count_daily 显著低估，需结合家庭日程综合判定 |
| 🧑‍⚖️ 结果性质 | 红线约束：**禁止**输出抑郁症诊断、量表评分（GDS-15 / PHQ-9）、用药建议或处方；**禁止**长期存储原始视频；**禁止**将"行为变化"等同于"确诊抑郁症" |
| 🔎 使用提醒 | 当出现 `strong_signal` 或老人有任何自伤/自杀言语或行为时，**必须**在提醒中附**心理援助热线 010-82951332 / 400-161-9995**并强烈建议家属立即介入 |
| 🔏 隐私合规 | 隐私合规：卧室视频涉及高度敏感个人隐私，使用前需取得老人本人明确知情同意，妥善加密保管；建议优先采用人体轮廓 + 面部马赛克模式 + 仅保存指标统计 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地连续 24h+ 卧室+餐厅视频
python -m scripts.smyx_depression_behavioral_markers_analysis --input /path/to/24h_home.mp4

# 分析网络连续 24h+ 卧室+餐厅视频
python -m scripts.smyx_depression_behavioral_markers_analysis --url https://example.com/24h_home.mp4

# 显示历史抑郁症辅助行为标记报告（自动触发关键词：查看抑郁行为标记历史报告、行为变化报告清单等）
python -m scripts.smyx_depression_behavioral_markers_analysis --list

# 输出精简报告
python -m scripts.smyx_depression_behavioral_markers_analysis --input 24h.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_depression_behavioral_markers_analysis --input 24h.mp4 --output result.json
```
