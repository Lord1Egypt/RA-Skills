---
name: "smyx-elderly-toilet-time-abnormal-analysis"
description: "Using a camera installed at the bathroom doorway (or inside the bathroom only detecting human silhouettes, without capturing private details), the system uses human detection and entry/exit tracking to identify when an elderly person enters or leaves the toilet and calculates the continuous occupancy time. | 通过在卫生间门口（或内部仅检测人体，不采集隐私细节）安装的摄像头，利用人体检测和进出跟踪技术，识别老年人进入和离开卫生间的时刻，计算连续占用时间。当占用时间超过预设安全阈值（默认30分钟）时，输出异常预警，通知家属或护理人员及时查看，预防老年人因跌倒、突发疾病（如中风、心梗）或体力不支导致的无法自主移动等意外。"
version: "1.0.16"
license: "MIT-0"
---

# 🚽 Elderly Toilet Time Abnormal Detection (>30 min) | 老年人如厕时间异常（超30分钟）识别
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **老年人如厕时间异常（超30分钟）识别** |
| 🎯 核心目标 | 通过在卫生间门口（或内部仅检测人体，不采集隐私细节）安装的摄像头，利用人体检测和进出跟踪技术，识别老年人进入和离开卫生间的时刻，计算连续占用时间。当占用时间超过预设安全阈值（默认30分钟）时，输出异常预警，通知家属或护理人员及时查看，预防老年人因跌倒、突发疾病（如中风、心梗）或体力不支导致的无法自主移动等意外。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_ELDERLY_TOILET_TIME_ABNORMAL_ANALYSIS` |

Using a camera installed at the bathroom doorway (or inside the bathroom only detecting human silhouettes, without capturing private details), the system uses human detection and entry/exit tracking to identify when an elderly person enters or leaves the toilet and calculates the continuous occupancy time. When occupancy exceeds a preset safety threshold (default 30 minutes), the system outputs an abnormal alert and notifies family members or caregivers to check in time, preventing accidents such as falls, sudden illness (stroke, heart attack) or exhaustion that may prevent the elderly from moving by themselves. Application scenarios: solo-living elder households, nursing homes, senior apartments. The system runs automatically; if the elderly stay in the toilet for more than 30 minutes without coming out, urgent reminders are pushed via app suggesting an on-site check. Skill features: sudden illness or falls during toileting that prevent the elderly from calling for help is a common safety risk. Automatic occupancy-time monitoring helps detect anomalies in time and gain rescue time. Can be integrated into nursing-home management systems or home-security platforms to enhance elderly safety.

通过在卫生间门口（或内部仅检测人体，不采集隐私细节）安装的摄像头，利用人体检测和进出跟踪技术，识别老年人进入和离开卫生间的时刻，计算连续占用时间。当占用时间超过预设安全阈值（默认30分钟）时，输出异常预警，通知家属或护理人员及时查看，预防老年人因跌倒、突发疾病（如中风、心梗）或体力不支导致的无法自主移动等意外。应用场景：独居老人家庭、养老院、老年公寓。系统自动监测，若老人进入卫生间超过30分钟未出，通过APP推送紧急提醒并建议上门查看。技能特点：老年人如厕时突发疾病或跌倒后无法呼救是常见安全隐患。通过自动监测停留时间，可及时发现异常，争取救援时间。该技能可集成到养老院管理系统或居家安防平台中，提升老人安全保障水平。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的老年人安全监测 AI。你的任务是分析卫生间门口（或内部仅检测人体轮廓）固定摄像头的视频，检测老年人的进入和离开事件，计算每次在卫生间内的连续停留时间。当停留时间超过预设阈值（默认 30 分钟）时，输出异常预警。为保护隐私，系统可对画面进行模糊化处理，仅识别人体进出。不要提供医疗诊断或具体救援操作方案，仅输出基于人体进出的统计与预警结果。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于卫生间门口/内部隐私化人体监控视频，识别老人进出事件并统计连续停留时长，按阈值输出异常预警

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 人体检测与跟踪（隐私化处理：模糊化/像素化/仅轮廓） |
| 2 | 进入/离开事件识别 |
| 3 | 连续停留时长统计 |
| 4 | 当日如厕会话历史 |
| 5 | 阈值判定（默认 30 分钟 |
| 6 | 可覆盖） |
| 7 | 分级预警（none / info / warning / critical） |
| 8 | 紧急联系人通知建议 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供卫生间门口/内部隐私化人体监控视频 URL 或文件需要分析时，默认触发本技能进行如厕停留时间监测 |
| 🔎 明确分析意图 | 当用户明确提及如厕、卫生间、洗手间、马桶、老人如厕时间长、卫生间跌倒、独居老人安全、长时间未出、停留时间监测等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看如厕时间历史报告、卫生间停留报告清单、老人如厕监护报告清单、查询历史如厕异常记录、显示所有如厕监测报告、显示老人卫生间监护诊断报告，查询如厕异常预警清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_elderly_toilet_time_abnormal_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_elderly_toilet_time_abnormal_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备卫生间门口/内部隐私化监控视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行老年人如厕时间异常识别 | 调用 `-m scripts.smyx_elderly_toilet_time_abnormal_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地卫生间门口/内部隐私化人体监控视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络卫生间门口/内部隐私化人体监控视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，老人居家安全场景默认 `other` | 按需填写 |
| `--list` | 显示老人如厕时间异常历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_elderly_toilet_time_abnormal_analysis.py`](scripts/smyx_elderly_toilet_time_abnormal_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；建议安装于门口或在内部启用画面模糊化 |
| 🔎 使用提醒 | 触发紧急预警时，请立即通过电话/上门方式人工核实，本工具仅作辅助监测 |
| 🔏 隐私合规 | 隐私合规：卫生间是高度敏感区域，强烈推荐安装于门口；如必须在内部，应仅检测人体轮廓并对原始画面做模糊化/像素化处理，避免采集任何隐私细节；使用前需取得被监护人或家属知情同意 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地卫生间门口监控视频
python -m scripts.smyx_elderly_toilet_time_abnormal_analysis --input /path/to/toilet_door.mp4

# 分析网络卫生间门口监控视频
python -m scripts.smyx_elderly_toilet_time_abnormal_analysis --url https://example.com/toilet_door.mp4

# 显示历史如厕监测报告（自动触发关键词：查看如厕时间历史报告、卫生间停留报告清单等）
python -m scripts.smyx_elderly_toilet_time_abnormal_analysis --list

# 输出精简报告
python -m scripts.smyx_elderly_toilet_time_abnormal_analysis --input toilet.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_elderly_toilet_time_abnormal_analysis --input toilet.mp4 --output result.json
```
