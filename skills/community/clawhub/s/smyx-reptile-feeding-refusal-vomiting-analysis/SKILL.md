---
name: "smyx-reptile-feeding-refusal-vomiting-analysis"
description: "Through fixed enclosure cameras, the system analyzes feeding-time and post-feeding videos of reptiles (snakes, lizards, turtles) to detect prey-attack behavior, successful swallowing, and regurgitation (vomiting). | 通过爬宠箱固定摄像头，分析喂食时及喂食后一段时间的视频，检测爬行动物（如蛇、蜥蜴、龟）的进食行为：是否主动攻击猎物（如鼠、昆虫）、是否成功吞食、以及是否在进食后短时间内将食物吐出（反吐）。当宠物对猎物无视、逃避（拒食）或将已吞入的食物吐出时，记录异常事件并输出提示。"
version: "1.0.3"
license: "MIT-0"
---

# 🐍 Reptile Feeding Refusal / Vomiting Detection | 爬宠进食拒绝/呕吐识别
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **爬宠进食拒绝/呕吐识别** |
| 🎯 核心目标 | 通过爬宠箱固定摄像头，分析喂食时及喂食后一段时间的视频，检测爬行动物（如蛇、蜥蜴、龟）的进食行为：是否主动攻击猎物（如鼠、昆虫）、是否成功吞食、以及是否在进食后短时间内将食物吐出（反吐）。当宠物对猎物无视、逃避（拒食）或将已吞入的食物吐出时，记录异常事件并输出提示。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_REPTILE_FEEDING_REFUSAL_VOMITING_ANALYSIS` |

Through fixed enclosure cameras, the system analyzes feeding-time and post-feeding videos of reptiles (snakes, lizards, turtles) to detect prey-attack behavior, successful swallowing, and regurgitation (vomiting). If the reptile ignores or avoids prey within a set window (default 30 min after offering), it is judged as feeding refusal; if it regurgitates swallowed prey within a short period (default 2 h after swallowing), it is judged as vomiting. The skill helps early detection of digestive tract disease, stress, inappropriate temperature, or parasitic infection. Application scenarios: vivariums, breeding tanks, reptile farms. The system monitors during feeding periods and pushes alerts upon refusal or vomiting. Skill features: feeding refusal and vomiting are common reptile health issues that may result from improper temperature, intestinal blockage, parasites, or infectious disease. AI-based automatic recording helps keepers intervene early and prevent deterioration. This skill can be integrated into smart vivariums or reptile-keeping apps.

通过爬宠箱固定摄像头，分析喂食时及喂食后一段时间的视频，检测爬行动物（如蛇、蜥蜴、龟）的进食行为：是否主动攻击猎物（如鼠、昆虫）、是否成功吞食、以及是否在进食后短时间内将食物吐出（反吐）。当宠物对猎物无视、逃避（拒食）或将已吞入的食物吐出时，记录异常事件并输出提示。该技能有助于早期发现爬宠的消化道疾病、应激、环境温度不适或寄生虫感染。应用场景：爬宠箱、饲养缸、爬行动物养殖场。系统在喂食时段自动监测，当出现拒食或呕吐时向饲养者推送提醒。技能特点：拒食和呕吐是爬宠常见的健康问题，可能由温度不当、肠道堵塞、寄生虫或传染病引起。通过 AI 自动记录，可提醒饲养者及时干预，避免病情恶化。该技能可集成到智能爬宠箱或饲养管理 APP 中。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的爬行动物健康监测 AI。你的任务是分析爬宠箱固定摄像头的喂食视频（正对喂食区域，分辨率 ≥ 720p，帧率 ≥ 20 FPS），围绕"投喂瞬间 t0"展开两个独立但相关的判定窗口：① **拒食窗口（t0 ~ t0+30 分钟）**：检测攻击事件（蛇咬击/缠绕、蜥蜴/龟扑咬）+ 吞食事件（猎物从口腔送入食道完成下咽）；窗口内 attack=0 且 swallow=0 → `refusal_judged`。② **呕吐窗口（吞食时间点 ~ +2 小时）**：检测反吐事件（反刍吐出全猎物/部分/液体），反吐物外观分类。按 **species（精确到物种：球蟒 / 玉米蛇 / 红尾蚺 / 王蛇 / 豹纹守宫 / 鬃狮蜥 / 蓝舌石龙子 / 红腿象龟 / 苏卡达 / 缅陆等）匹配进食生理基线**，按 7 类综合场景判定（feeding_normal_attack_swallow / feeding_normal_delayed_attack / refusal_in_physiological_context / **refusal_abnormal** / **vomiting_event** / **vomiting_with_environmental_cause** / feeding_signal_unreliable），按 4 级提醒策略递进（Level 1 积极反馈 → Level 2 生理性正常无需干预 → Level 3 异常拒食检查温度湿度 UVB+猎物状态+大小+7 天后再试 → Level 4 呕吐立即停喂 24-72h+检查消化温度+观察精神排泄+联系兽医）。**核心物种特异性硬约束**：**大型蛇类**（球蟒 / 红尾蚺 / 王蛇等）一次喂食后**数日至两周不进食属正常**；**冬化期物种**（部分龟类、玉米蛇）**整季拒食属正常**；**蜕皮期**所有爬宠均可能拒食；**繁殖期**雄性可能拒食；**抱卵/产前**雌性常拒食 → **严禁通用阈值盲判生理性拒食为异常**。生理性上下文必须考虑（**蜕皮 / 冬化 / 距上次成功喂食 < 72h / 繁殖期 / 抱卵期 / 新入缸应激 / 环境温度异常**），避免误报。视野遮挡 / 光照不足 / 跟踪率 < 80% / 投喂时间未录入 → 必须返回 `feeding_signal_unreliable`。不提供任何疾病诊断，仅输出基于视觉的进食行为记录；**严禁输出具体药物名称、剂量、给药方案、灌肠剂、催吐剂、止吐药**；**严禁输出"强制开口喂食""灌食""饥饿疗法 X 天"等具体操作剂量**；严禁伪造夸大攻击/吞食/反吐事件；严禁越权代用户投喂或启停设备（仅建议）。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于爬宠箱固定摄像头**喂食时段及后续视频**（默认投喂 t0 → 拒食判定 t0+30 分钟 → 呕吐判定吞食+2 小时），识别 7 类综合场景（feeding_normal_attack_swallow / feeding_normal_delayed_attack / refusal_in_physiological_context / refusal_abnormal / vomiting_event / vomiting_with_environmental_cause / feeding_signal_unreliable）→ **五组指标**：攻击 4 项（猎物出现 + 攻击次数 + 攻击延迟 + 置信度）+ 吞食 3 项（**吞食次数** + 完整吞食时长 + 置信度）+ 反吐 4 项（**是否反吐** + 反吐延迟 + 反吐物外观 + 置信度）+ 拒食判定 3 项（**refusal_judged** + 无视时长 + 主动逃避检测）+ 排除上下文 7 项（蜕皮 / 冬化 / 距上次进食 / 繁殖 / 抱卵 / 温度适宜 / 新入缸）→ 4 档提醒级别（info / notice / important / urgent）→ **4 级提醒策略递进**（积极反馈 → 生理性正常 → 异常拒食检查环境+猎物+7 天后再试 → 呕吐紧急停喂+检查消化温度+兽医）→ 单日提醒上限（Level 1 不限 / Level 2 × 4 / Level 3 × 3 / **Level 4 × 5 呕吐每次必报**）→ **拒食/呕吐事件报告**（按 enclosure_id + feed_time 输出，含攻击/吞食/反吐事件 + 拒食判定 + 建议动作 + 免责声明）

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 投喂时刻 t0 自动识别（猎物投入瞬间） |
| 2 | 猎物目标检测（活鼠 / 乳鼠 / 蟋蟀 / 面包虫 / 杜比亚 / 蔬果） |
| 3 | 爬宠目标跟踪 |
| 4 | 攻击行为检测（咬击瞬间 + 缠绕姿态） |
| 5 | 吞食行为检测（口腔张大 + 颈部蠕动 + 猎物逐步消失） |
| 6 | **反吐事件检测**（吞食后口腔反向蠕动 + 猎物/部分/液体重新出现） |
| 7 | 拒食窗口计时（30 分钟无攻击无吞食） |
| 8 | 生理性上下文识别（蜕皮 / 冬化 / 72h 内已喂 / 繁殖 / 抱卵 / 新入缸 / 温度异常） |
| 9 | 视野与光照门控 |
| 10 | 用户 APP 推送 |
| 11 | 4 级提醒递进 |
| 12 | 单日提醒上限 |
| 13 | 事件报告（按 enclosure_id + feed_time 输出） |
| 14 | 连续 ≥ 2 次 Level 3 → 强烈建议联系**专业爬宠兽医** |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供爬宠箱喂食视频 URL 或文件需要分析时，默认触发本技能进行爬宠拒食/呕吐识别 |
| 🔎 明确分析意图 | 当用户明确提及爬宠拒食、爬宠不吃东西、爬宠吐了、反吐、呕吐、爬宠开食、爬宠喂食异常等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看爬宠拒食/呕吐历史报告、喂食异常事件清单、查询历史拒食呕吐记录、显示所有爬宠喂食异常报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_reptile_feeding_refusal_vomiting_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_reptile_feeding_refusal_vomiting_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备爬宠箱喂食视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 获取 open-id（强制执行） | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行爬宠拒食/呕吐识别 | 调用 `-m scripts.smyx_reptile_feeding_refusal_vomiting_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地爬宠箱喂食视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络爬宠箱喂食视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，爬宠拒食/呕吐场景默认 `other` | 按需填写 |
| `--list` | 显示爬宠拒食/呕吐异常事件历史记录清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_reptile_feeding_refusal_vomiting_analysis.py`](scripts/smyx_reptile_feeding_refusal_vomiting_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov，最大 10MB；摄像头需**正对喂食区域，无遮挡**；帧率 ≥ 20 FPS；覆盖**投喂瞬间 → 30 分钟拒食窗口 → 吞食后 2 小时呕吐窗口** |
| 🔎 使用提醒 | **核心双窗口**：拒食窗口（t0 ~ t0+30 分钟）+ 呕吐窗口（吞食时间 ~ +2 小时） |
| 🔎 使用提醒 | **核心输出**：`refusal_judged` + `vomit_event_detected` + 综合场景标签 |
| 🔎 使用提醒 | **4 级提醒策略递进**（info → notice → important → urgent），呕吐事件直接进入 Level 4 |
| 🔎 使用提醒 | 单日提醒上限：Level 1 不限 / Level 2 × 4 / Level 3 × 3 / **Level 4 × 5（呕吐每次必报，不可压制）** |
| 🔎 使用提醒 | 红线约束 |
| 🧑‍⚖️ 结果性质 | **🚨 禁止**做"隐孢子虫病 / 库道虫病 / OPMV / 蛇类传染性脑膜炎 / 肠道堵塞 / 代谢性骨病"等具体疾病诊断 |
| 🔎 使用提醒 | **🚨 绝对禁止**输出具体药物名称、剂量、给药方案、灌肠剂、催吐剂、止吐药 |
| 🔎 使用提醒 | **🚨 绝对禁止**输出"强制开口喂食""灌食""饥饿疗法 X 天"等具体操作剂量（任何操作必须由兽医现场判断） |
| 🔎 使用提醒 | **禁止**长期存储完整爬宠箱视频（≤ 14 天，仅入库喂食事件 + 异常事件片段；养殖场按管理规定） |
| 🔎 使用提醒 | **禁止**用于商业广告 / AI 训练；禁第三方共享 |
| 🔎 使用提醒 | **禁止**越权代用户投喂 / 启停加热灯 / UVB / 加热垫 / 灯光参数；任何设备控制变更必须由用户确认（仅可建议） |
| 🔎 使用提醒 | **绝对禁止**伪造或夸大攻击次数、吞食次数、反吐事件等指标；所有数据必须基于真实视频帧分析 |
| 🔎 使用提醒 | **必须**按 **species 进食生理基线**判定（大型蛇类一次喂食后数日至两周不进食属正常 / 冬化期整季拒食属正常 / 蜕皮期可拒食 / 繁殖期雄性可拒食 / 抱卵产前雌性可拒食）；**严禁通用阈值盲判生理性拒食为异常** |
| 📚 文档读取 | **必须**考虑生理性上下文（**蜕皮 / 冬化 / 距上次成功喂食 < 72h / 繁殖期 / 抱卵期 / 新入缸应激 / 环境温度异常**），避免误报 |
| 🔎 使用提醒 | **必须**在视野遮挡 / 光照不足 / 跟踪率 < 80% / 投喂时间未录入时返回 `feeding_signal_unreliable` 并建议调整摄像头或补充投喂时间录入 |
| 🔎 使用提醒 | **必须**：连续 ≥ 2 次 Level 3 → 强烈建议联系**专业爬宠兽医** |
| 📜 报告输出 | **必须**：拒食/呕吐事件报告**按 enclosure_id + feed_time 输出**，含攻击/吞食/反吐事件 + 拒食判定 + 建议动作 + 免责声明 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史拒食/呕吐事件记录清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地爬宠箱喂食视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_reptile_feeding_refusal_vomiting_analysis --input /path/to/feeding.mp4

# 分析网络爬宠箱喂食视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_reptile_feeding_refusal_vomiting_analysis --url https://example.com/feeding.mp4

# 显示历史拒食/呕吐事件记录清单（自动触发关键词：查看爬宠拒食/呕吐历史报告等）
python -m scripts.smyx_reptile_feeding_refusal_vomiting_analysis --list

# 输出精简报告
python -m scripts.smyx_reptile_feeding_refusal_vomiting_analysis --input feeding.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_reptile_feeding_refusal_vomiting_analysis --input feeding.mp4 --output result.json
```
