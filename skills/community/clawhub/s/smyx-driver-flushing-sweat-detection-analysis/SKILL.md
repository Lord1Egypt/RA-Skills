---
name: "smyx-driver-flushing-sweat-detection-analysis"
description: "Using an in-cabin DMS camera, the system analyzes the driver's facial video in real time, detecting skin color variation (flush index, derived from red-channel ratio in RGB or skin-color models) and sweat-droplet / reflective area (via image texture and reflection features). | 通过车载DMS摄像头实时分析驾驶员面部视频，检测面部肤色变化（潮红指数，通过RGB色空间中的红色分量比例或肤色模型）以及汗珠/反光面积（通过图像纹理和反射特征）。当潮红指数显著升高（可能提示血压升高、发热或情绪激动）或出汗区域面积超过阈值（可能提示热应激、低血糖或心脏问题）时，输出健康风险提醒，建议驾驶员停车休息或就医。"
version: "1.0.3"
license: "MIT-0"
---

# 🥵 Driver Facial Flushing / Sweat Abnormality Detection | 驾驶员面部潮红/出汗异常检测
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **驾驶员面部潮红/出汗异常检测** |
| 🎯 核心目标 | 通过车载DMS摄像头实时分析驾驶员面部视频，检测面部肤色变化（潮红指数，通过RGB色空间中的红色分量比例或肤色模型）以及汗珠/反光面积（通过图像纹理和反射特征）。当潮红指数显著升高（可能提示血压升高、发热或情绪激动）或出汗区域面积超过阈值（可能提示热应激、低血糖或心脏问题）时，输出健康风险提醒，建议驾驶员停车休息或就医。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_DRIVER_FLUSHING_SWEAT_DETECTION_ANALYSIS` |

Using an in-cabin DMS camera, the system analyzes the driver's facial video in real time, detecting skin color variation (flush index, derived from red-channel ratio in RGB or skin-color models) and sweat-droplet / reflective area (via image texture and reflection features). When the flush index rises significantly (possibly indicating elevated blood pressure, fever or strong emotion) or the sweating area exceeds the threshold (possibly indicating heat stress, hypoglycemia or cardiac issues), it outputs a health-risk reminder and suggests the driver to rest or seek medical help. The skill aims to help drivers stay aware of their physical state and avoid accidents caused by sudden illness. Application scenarios: passenger cars, commercial vehicles, ride-hailing fleets, freight fleets. Real-time monitoring; when flushing or heavy sweating is detected, it voice-prompts 'please pay attention to your physical state, rest is recommended' or pushes the event to the fleet-management platform. Skill features: sudden illness of drivers (e.g., heart attack, heatstroke, hypoglycemia) often leads to vehicle loss of control and major accidents. AI real-time monitoring of facial flushing and abnormal sweating provides an early reminder for drivers to take a break or seek help, reducing accident risk. Can serve as a value-add feature on DMS systems, especially suitable for commercial and ride-hailing fleets.

通过车载DMS摄像头实时分析驾驶员面部视频，检测面部肤色变化（潮红指数，通过RGB色空间中的红色分量比例或肤色模型）以及汗珠/反光面积（通过图像纹理和反射特征）。当潮红指数显著升高（可能提示血压升高、发热或情绪激动）或出汗区域面积超过阈值（可能提示热应激、低血糖或心脏问题）时，输出健康风险提醒，建议驾驶员停车休息或就医。该技能旨在辅助驾驶员关注自身健康，避免因突发疾病引发事故。应用场景：乘用车、商用车、网约车、货运车队。系统实时监测，当检测到面部潮红或大量出汗时，通过语音提示'请注意身体状态，建议休息'或推送至车队管理平台。技能特点：驾驶员突发疾病（如心梗、中暑、低血糖）往往会导致车辆失控，引发重大事故。通过AI实时监测面部潮红和出汗异常，可早期提醒驾驶员关注自身状态，采取休息或求助措施，降低事故风险。该技能可作为DMS系统的增值功能，提升车辆主动安全水平，尤其适合营运车辆和网约车平台。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的驾驶员健康监测 AI。你的任务是分析驾驶员面部视频，检测面部潮红指数（肤色中红色分量的变化）和出汗区域（汗珠或皮肤反光面积）。当潮红指数超过阈值或出汗面积超过预设比例时，输出健康风险提醒。不要提供医疗诊断或具体临床判断，仅输出基于视觉的异常现象提示。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于车载 DMS 摄像头驾驶员面部视频，实时检测面部潮红指数与出汗反光面积，按阈值输出健康风险提醒

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 驾驶员面部检测 |
| 2 | 面部 ROI 分区（额头/双颊/鼻翼） |
| 3 | 潮红指数计算（RGB 红色分量比 / 肤色模型偏移） |
| 4 | 潮红面积比 |
| 5 | 汗珠/反光面积比 |
| 6 | 皮肤纹理粗糙度 |
| 7 | 基线值与变化幅度 |
| 8 | 异常等级判定 |
| 9 | 座舱联动动作建议（voice_alert / fleet_upload / event_record） |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供车载 DMS 驾驶员面部视频 URL 或文件需要分析时，默认触发本技能进行潮红/出汗异常检测 |
| 🔎 明确分析意图 | 当用户明确提及驾驶员健康、面部潮红、出汗异常、突发疾病、心梗预警、中暑预警、低血糖、DMS 健康监测、营运车辆健康等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看驾驶员健康历史报告、潮红预警清单、出汗异常报告清单、查询历史驾驶员健康事件、显示所有驾驶员健康报告、显示车队健康诊断报告，查询驾驶员健康事件清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_driver_flushing_sweat_detection_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_driver_flushing_sweat_detection_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备车载 DMS 驾驶员面部视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行驾驶员面部潮红/出汗异常检测 | 调用 `-m scripts.smyx_driver_flushing_sweat_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地车载 DMS 驾驶员面部视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络车载 DMS 驾驶员面部视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，驾驶员健康监测场景默认 `other` | 按需填写 |
| `--list` | 显示驾驶员面部潮红/出汗异常历史分析报告列表清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_driver_flushing_sweat_detection_analysis.py`](scripts/smyx_driver_flushing_sweat_detection_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：必须有彩色 RGB 通道，纯红外通道无法识别潮红 |
| 🧑‍⚖️ 结果性质 | 检测结果仅作为驾驶员辅助健康提醒，本工具不替代体温计、血压计、血糖仪、心电图等医疗设备，更不替代医生诊断 |
| 🔎 使用提醒 | 受光照、车窗有色膜、肤色个体差异影响较大，建议结合基线值与持续时间综合判定 |
| 🔏 隐私合规 | 隐私合规：车载驾驶员视频涉及个人生物特征隐私，使用前需取得驾驶员/员工知情同意，车队部署应遵循当地隐私法规并妥善保管/加密相关录像 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地车载 DMS 驾驶员视频
python -m scripts.smyx_driver_flushing_sweat_detection_analysis --input /path/to/dms.mp4

# 分析网络车载 DMS 驾驶员视频
python -m scripts.smyx_driver_flushing_sweat_detection_analysis --url https://example.com/dms.mp4

# 显示历史驾驶员潮红/出汗异常报告（自动触发关键词：查看驾驶员健康历史报告、潮红预警清单等）
python -m scripts.smyx_driver_flushing_sweat_detection_analysis --list

# 输出精简报告
python -m scripts.smyx_driver_flushing_sweat_detection_analysis --input dms.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_driver_flushing_sweat_detection_analysis --input dms.mp4 --output result.json
```
