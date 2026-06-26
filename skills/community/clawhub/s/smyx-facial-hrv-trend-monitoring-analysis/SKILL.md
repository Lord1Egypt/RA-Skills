---
name: "smyx-facial-hrv-trend-monitoring-analysis"
description: "Using everyday cameras (laptop camera, smartphone front camera, smart mirror), the system records 30-60 seconds of facial video and uses remote photoplethysmography (rPPG) to extract subtle color variations from facial skin micro-circulation, from which it computes heart-rate-variability (HRV) metrics including SDNN (standard deviation of all normal sinus RR intervals) and RMSSD (root mean square of successive RR-interval. | 通过日常摄像头（如电脑摄像头、手机前置摄像头）拍摄面部视频（30-60秒），利用光电容积描记技术（远程光电容积描记术，rPPG）提取面部皮肤微循环的微弱色度变化，从中计算心率变异性（HRV）指标，包括SDNN（全部正常窦性心搏间期的标准差）、RMSSD（相邻心搏间期差值的均方根）等。该技能可用于压力评估、心血管健康监测及疲劳管理。"
version: "1.0.2"
license: "MIT-0"
---

# 💓 Adult Facial HRV Trend Monitoring (rPPG) | 成人心率变异性（HRV）趋势监测（面部）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **成人心率变异性（HRV）趋势监测（面部）** |
| 🎯 核心目标 | 通过日常摄像头（如电脑摄像头、手机前置摄像头）拍摄面部视频（30-60秒），利用光电容积描记技术（远程光电容积描记术，rPPG）提取面部皮肤微循环的微弱色度变化，从中计算心率变异性（HRV）指标，包括SDNN（全部正常窦性心搏间期的标准差）、RMSSD（相邻心搏间期差值的均方根）等。该技能可用于压力评估、心血管健康监测及疲劳管理。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_FACIAL_HRV_TREND_MONITORING_ANALYSIS` |

Using everyday cameras (laptop camera, smartphone front camera, smart mirror), the system records 30-60 seconds of facial video and uses remote photoplethysmography (rPPG) to extract subtle color variations from facial skin micro-circulation, from which it computes heart-rate-variability (HRV) metrics including SDNN (standard deviation of all normal sinus RR intervals) and RMSSD (root mean square of successive RR-interval differences). It supports long-term trend analysis and generates daily/weekly HRV curves. Applicable to stress assessment, cardiovascular health monitoring and fatigue management. Application scenarios: home health monitoring, enterprise employee health management, physical-examination centers, smart mirrors. Users sit still in front of the camera for 1 minute daily; the system computes HRV and records the trend, pushing 'high stress' or 'fatigue accumulation' reminders when HRV drops significantly. Skill features: HRV is a key indicator of autonomic-nervous-system health, related to stress, fatigue and cardiovascular risk. Contact-free measurement via everyday cameras lowers the usage threshold and lets more people keep track of their recovery state and stress level. Can serve as a value-add feature in smart-office or smart elderly-care scenarios.

通过日常摄像头（如电脑摄像头、手机前置摄像头）拍摄面部视频（30-60秒），利用光电容积描记技术（远程光电容积描记术，rPPG）提取面部皮肤微循环的微弱色度变化，从中计算心率变异性（HRV）指标，包括SDNN（全部正常窦性心搏间期的标准差）、RMSSD（相邻心搏间期差值的均方根）等。支持长期趋势分析，生成每日/每周HRV变化曲线。该技能可用于压力评估、心血管健康监测及疲劳管理。应用场景：居家健康监测、企业员工健康管理、体检中心、智能镜子。用户每日对着摄像头静坐1分钟，系统自动计算HRV并记录趋势，当HRV显著下降时推送'压力过大'或'疲劳累积'提醒。技能特点：HRV是衡量自主神经系统健康的重要指标，与压力、疲劳、心血管风险相关。通过日常摄像头无接触测量，可降低使用门槛，让更多人持续关注自身恢复状态和压力水平，助力健康管理。该技能可作为增值功能集成到智慧办公、健康养老等场景。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的生理信号分析 AI。你的任务是分析人脸面部视频，使用远程光电容积描记技术（rPPG）提取皮肤微循环波动信号，计算心率变异性（HRV）指标。输出 SDNN、RMSSD 以及长期趋势（需结合历史数据）。不要提供医疗诊断或临床心血管评估，仅输出基于信号处理的定量指标与趋势提示。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于 30-60 秒静坐面部视频，通过 rPPG 提取脉搏波 → 计算 HRV 指标 → 结合历史数据生成长期趋势

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 面部检测 + ROI（前额/双颊）选择 |
| 2 | RGB 时序提取 |
| 3 | 带通滤波 + POS/CHROM 算法提取 BVP |
| 4 | RR 间期序列 |
| 5 | 平均心率（HR） |
| 6 | SDNN |
| 7 | RMSSD |
| 8 | pNN50 |
| 9 | LF/HF 比 |
| 10 | 信号质量评级（high / medium / low） |
| 11 | HRV 综合得分（0-100） |
| 12 | 近 7 天趋势（rising / stable / declining）+ 变化百分比 |
| 13 | 压力/疲劳累积提示 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供成人静坐 30-60 秒面部视频 URL 或文件需要分析时，默认触发本技能进行 HRV 趋势监测 |
| 🔎 明确分析意图 | 当用户明确提及 HRV、心率变异性、SDNN、RMSSD、rPPG、远程光电容积描记、压力评估、自主神经、疲劳累积、智能镜子心率等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看 HRV 历史报告、心率变异性报告清单、面部 HRV 趋势报告清单、查询历史 HRV 记录、显示所有 HRV 报告、显示自主神经监测诊断报告，查询压力疲劳趋势预警清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_facial_hrv_trend_monitoring_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_facial_hrv_trend_monitoring_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备成人静坐面部视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行成人面部 HRV 趋势监测 | 调用 `-m scripts.smyx_facial_hrv_trend_monitoring_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地成人静坐面部视频文件路径（30-60秒） | 适用于本地文件分析 |
| `--url` | 网络成人静坐面部视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，rPPG 生理信号分析场景默认 `other` | 按需填写 |
| `--list` | 显示成人面部 HRV 历史监测报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_facial_hrv_trend_monitoring_analysis.py`](scripts/smyx_facial_hrv_trend_monitoring_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：帧率必须 ≥ 25 FPS，否则 HRV 指标可信度大幅下降 |
| 🔎 使用提醒 | HRV 受运动、咖啡因、情绪、体位等多因素影响，建议每日同时段、同条件测量便于趋势纵向对比 |
| 🧑‍⚖️ 结果性质 | 检测结果仅作为个人健康趋势参考，本工具不替代心电图等医疗级心律评估，更不替代医生诊断 |
| 🔏 隐私合规 | 隐私合规：面部视频涉及生物特征隐私，使用前需取得本人同意，并妥善保管/加密相关录像 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地 30-60 秒静坐面部视频
python -m scripts.smyx_facial_hrv_trend_monitoring_analysis --input /path/to/sit_30s.mp4

# 分析网络 30-60 秒静坐面部视频
python -m scripts.smyx_facial_hrv_trend_monitoring_analysis --url https://example.com/sit_30s.mp4

# 显示历史 HRV 趋势监测报告（自动触发关键词：查看 HRV 历史报告、心率变异性报告清单等）
python -m scripts.smyx_facial_hrv_trend_monitoring_analysis --list

# 输出精简报告
python -m scripts.smyx_facial_hrv_trend_monitoring_analysis --input sit.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_facial_hrv_trend_monitoring_analysis --input sit.mp4 --output result.json
```
