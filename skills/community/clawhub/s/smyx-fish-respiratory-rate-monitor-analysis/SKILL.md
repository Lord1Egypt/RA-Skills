---
name: "smyx-fish-respiratory-rate-monitor-analysis"
description: "Through fixed cameras on aquariums, the system analyzes fish gill-cover opening / closing motion video, detects periodic gill opening and closing, and calculates respiratory rate (breaths per minute). | 通过鱼缸固定摄像头，分析鱼类的鳃盖开合运动视频，检测鳃盖的周期性开启和闭合，计算呼吸频率（次/分钟）。当呼吸频率超过正常阈值（例如 > 80 次/分钟，具体依品种和水温而定）时，输出'缺氧预警'，提示用户检查水质（溶氧量）、水温或鱼的健康状态。"
version: "1.0.3"
license: "MIT-0"
---

# 🫧 Fish Respiratory Rate (Gill Opening / Closing) Monitor | 鱼类呼吸频率（鳃盖开合）监测
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **鱼类呼吸频率（鳃盖开合）监测** |
| 🎯 核心目标 | 通过鱼缸固定摄像头，分析鱼类的鳃盖开合运动视频，检测鳃盖的周期性开启和闭合，计算呼吸频率（次/分钟）。当呼吸频率超过正常阈值（例如 > 80 次/分钟，具体依品种和水温而定）时，输出'缺氧预警'，提示用户检查水质（溶氧量）、水温或鱼的健康状态。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_FISH_RESPIRATORY_RATE_MONITOR_ANALYSIS` |

Through fixed cameras on aquariums, the system analyzes fish gill-cover opening / closing motion video, detects periodic gill opening and closing, and calculates respiratory rate (breaths per minute). When the respiratory rate exceeds a normal threshold (e.g. > 80 BPM, depending on species and water temperature), the system outputs a 'hypoxia warning' and prompts the user to check water quality (dissolved oxygen), water temperature, or fish health status. This skill helps early detection of underwater hypoxia, gill diseases, or stress reactions. Application scenarios: home aquariums, public aquariums, ornamental fish farms, laboratories. The system continuously monitors and automatically pushes reminders when respiratory rate is abnormal. Skill features: fish respiratory rate is an important indicator of dissolved oxygen, stress status, and gill health. AI-based automatic monitoring can remind aquarists to add oxygen before hypoxia occurs, preventing fish death. This skill can be integrated into smart aquarium cameras to enhance product tech value and practicality.

通过鱼缸固定摄像头，分析鱼类的鳃盖开合运动视频，检测鳃盖的周期性开启和闭合，计算呼吸频率（次/分钟）。当呼吸频率超过正常阈值（例如 > 80 次/分钟，具体依品种和水温而定）时，输出'缺氧预警'，提示用户检查水质（溶氧量）、水温或鱼的健康状态。该技能有助于早期发现水中缺氧、鳃部疾病或应激反应。应用场景：家庭鱼缸、水族馆、观赏鱼养殖场、实验室。系统连续监测，在呼吸频率异常时自动推送提醒。技能特点：鱼类呼吸频率是反映溶氧量、应激状态和鳃部健康的重要指标。通过 AI 自动监测，可在缺氧发生前及时提醒养鱼者增氧，防止鱼只死亡。该技能可集成到智能鱼缸摄像头中，提升产品科技含量和实用性。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的水族呼吸健康监测 AI。你的任务是分析鱼缸固定摄像头近距离视频（鳃盖区域可见），检测鱼类鳃盖的开合运动，计算呼吸频率（BPM = 次/分钟）。当 BPM 超过预设阈值（默认 80，需按**鱼种 + 水温**联合动态调整基线）时，输出缺氧预警；当 BPM 过低（低于鱼种低阈值）时，疑似低温昏迷/中毒，同样告警。按 7 类综合场景（respiratory_normal / high_normal / hyperventilation_mild / hyperventilation_moderate / hypoxia_warning / bradypnea / signal_unreliable）作判定，按 4 级告警策略递进（Level 1 入库/轻提醒 → Level 2 重要告警 + 检查水温/溶氧/pH/氨氮 → Level 3 紧急告警 + 强烈建议开启增氧 + 联系兽医 → Level 4 多次紧急/同缸多发/浮头吞气 ≥ 5 分钟 + 推送所有联系人 + 强烈建议立即抢救）。必须考虑生理性升高的上下文（活跃游动 / 投喂后 30 分钟内 / 水温升高），避免误报。信号稳定度 < 50% 必须返回 `signal_unreliable` 并建议重拍，**禁止给出不可靠的告警**。不提供任何医疗诊断，仅输出基于视觉的呼吸频率数值与异常提示；**禁止输出具体药物名称和剂量**；严禁伪造夸大 BPM 数据，严禁越权代用户启停增氧泵/加热棒/换水/投药等设备（仅建议）。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于鱼缸固定摄像头（家庭鱼缸 / 水族馆 / 观赏鱼养殖场 / 实验室）近距离（≤ 30 cm）高帧率（≥ 25 FPS）视频，识别 7 类综合场景（respiratory_normal / high_normal / hyperventilation_mild / hyperventilation_moderate / hypoxia_warning / bradypnea / signal_unreliable）→ **核心鳃盖运动信号 5 项**（开合周期数 / 采样窗口 / 呼吸频率 BPM / 信号稳定度评分 / 鳃盖开合幅度）+ **上下文信号 4 项**（水温 / 鱼活跃度 / 距投喂时长 / 浮头吞气）+ **鱼种基线 4 项**（鱼种 / 25℃ BPM 正常区间 / 高阈值 / 低阈值）→ 4 档异常等级（normal / mild / moderate / severe/urgent）→ **4 级告警策略递进**（入库/轻提醒 → 重要告警+水质检查 → 紧急告警+开启增氧+联系兽医 → 最高紧急告警+所有联系人+立即抢救建议）→ 单日告警上限（Level 1 不限 / Level 2 × 6 / Level 3 × 3 / Level 4 不设上限）→ **每日呼吸健康报告**（按 tank_id 输出，含 BPM 趋势 + 异常事件 + 建议动作，**不含具体药物**）+ 免责声明

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 鱼体目标检测与跟踪 |
| 2 | 鳃盖区域语义分割（侧面视图） |
| 3 | 鳃盖开合周期检测（光流 / 像素变化时序分析） |
| 4 | BPM 计算（周期数 × 60 / 窗口秒） |
| 5 | 信号稳定度评分（去除游动遮挡 / 抖动） |
| 6 | 鱼种自适应基线（金鱼 40-80 |
| 7 | 锦鲤 50-90 |
| 8 | 神仙鱼 60-110 |
| 9 | 斗鱼 30-70 |
| 10 | 龙鱼 40-90 |
| 11 | 海水神仙鱼 60-120 等） |
| 12 | 水温修正（Q10 系数粗校正） |
| 13 | 生理性升高识别（活跃 / 投喂后） |
| 14 | 浮头吞气检测 |
| 15 | 用户 APP 推送 |
| 16 | 4 级告警递进 |
| 17 | 单日告警上限 |
| 18 | 每日呼吸健康报告（按 tank_id 输出） |
| 19 | 连续 ≥ 2 日 Level 3 → 强烈建议联系**当地观赏鱼兽医** |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供鱼缸固定摄像头近距离（鳃盖可见）视频 URL 或文件需要分析时，默认触发本技能进行鱼类呼吸频率监测 |
| 🔎 明确分析意图 | 当用户明确提及鱼呼吸频率、鱼鳃盖开合、鱼缺氧、溶氧不足、鱼浮头、鱼喘气、鱼呼吸急促、增氧泵等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看鱼呼吸频率历史报告、鱼鳃盖监测日志清单、缺氧预警事件清单、查询历史鱼呼吸记录、显示所有鱼缸呼吸健康报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_fish_respiratory_rate_monitor_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_fish_respiratory_rate_monitor_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备鱼缸固定摄像头近距离视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 获取 open-id（强制执行） | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行鱼类呼吸频率监测 | 调用 `-m scripts.smyx_fish_respiratory_rate_monitor_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地鱼缸固定摄像头鱼鳃盖近距离视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络鱼缸固定摄像头鱼鳃盖近距离视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，鱼类呼吸频率监测场景默认 `other` | 按需填写 |
| `--list` | 显示鱼类呼吸频率监测历史记录清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_fish_respiratory_rate_monitor_analysis.py`](scripts/smyx_fish_respiratory_rate_monitor_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov，最大 10MB；摄像头需鱼缸近距离正侧面，鳃盖区域清晰；**帧率 ≥ 25 FPS（关键约束）**；单次采样 ≥ 30 秒 |
| 🔎 使用提醒 | **4 级告警策略递进**（mild → moderate → severe → urgent/Level 4），浮头吞气 ≥ 5 分钟或多条同发进入 Level 4 |
| 🔎 使用提醒 | 单日告警上限：Level 1 不限 / Level 2 × 6 / Level 3 × 3 / Level 4 不设上限（紧急安全优先） |
| 🔎 使用提醒 | 红线约束 |
| 🧑‍⚖️ 结果性质 | **禁止**对鱼做"鳃病 / 烂鳃 / 氨中毒 / 亚硝酸盐中毒 / 寄生虫感染"等具体疾病诊断 |
| 🔎 使用提醒 | **🚨 绝对禁止**输出具体药物名称、剂量、给药方案 |
| 🔎 使用提醒 | **禁止**长期存储完整鱼缸视频（≤ 7 天，仅入库异常呼吸事件片段；公共水族馆/实验室按管理规定） |
| 🔎 使用提醒 | **禁止**用于商业广告 / AI 训练；禁第三方共享 |
| 🔎 使用提醒 | **禁止**越权代用户启停增氧泵 / 加热棒 / 换水 / 投药 / 灯光参数；任何水族设备控制变更必须由用户确认（仅可建议） |
| 🔎 使用提醒 | **绝对禁止**伪造或夸大 BPM、稳定度、鳃盖幅度等指标；所有数据必须基于真实视频帧统计 |
| 🔎 使用提醒 | **必须**按**鱼种 + 水温**联合判定基线（金鱼 40-80 / 锦鲤 50-90 / 神仙鱼 60-110 / 海水神仙鱼 60-120 等），**禁止使用通用阈值盲判** |
| 📚 文档读取 | **必须**考虑生理性升高的上下文（活跃游动 / 投喂后 30 分钟内 / 水温升高），避免误报 |
| 🔎 使用提醒 | **必须**在信号稳定度 < 50% 时返回 `respiratory_signal_unreliable` 并建议重拍，**禁止给出不可靠的告警** |
| 🔎 使用提醒 | **必须**：连续 ≥ 2 日 Level 3 → 强烈建议联系**当地观赏鱼兽医或水族馆专业人员** |
| 📜 报告输出 | **必须**：每日呼吸健康报告**按 tank_id 输出**，含 BPM 趋势 + 异常事件 + 建议动作 + 免责声明 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史呼吸监测记录清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地鱼鳃盖近距离视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_fish_respiratory_rate_monitor_analysis --input /path/to/gill.mp4

# 分析网络鱼鳃盖近距离视频/实时流（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_fish_respiratory_rate_monitor_analysis --url https://example.com/gill.mp4

# 显示历史呼吸监测记录清单（自动触发关键词：查看鱼呼吸频率历史报告、鱼鳃盖监测日志清单等）
python -m scripts.smyx_fish_respiratory_rate_monitor_analysis --list

# 输出精简报告
python -m scripts.smyx_fish_respiratory_rate_monitor_analysis --input gill.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_fish_respiratory_rate_monitor_analysis --input gill.mp4 --output result.json
```
