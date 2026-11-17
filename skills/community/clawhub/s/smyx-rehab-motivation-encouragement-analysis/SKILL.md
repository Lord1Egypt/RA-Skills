---
name: "smyx-rehab-motivation-encouragement-analysis"
description: "Through fixed cameras in rehabilitation centers or home rehab areas, the system analyzes video of patients during rehabilitation training to detect frustration / giving-up tendency behaviors: sighing (rapid chest-abdomen rise-fall with exhalation), training interruption (actively stopping before reaching preset reps or duration), head-down silence (head lowered, avoiding eye contact, long-term silence), sluggish or. | 通过康复中心或家庭康复区的固定摄像头，分析患者在进行康复训练时的视频，检测沮丧/放弃倾向行为：叹气（胸腹快速起伏伴呼气声）、中断训练（在未达到预设次数或时间前主动停止动作）、低头不语（头部低垂，避免眼神接触，长时间无言语）、动作迟缓或敷衍（关节活动范围明显小于前期），以及长时间无进展（连续多日同一训练项目的表现停滞或下降）。"
version: "1.0.19"
license: "MIT-0"
---

# 💪 Rehab Patient Frustration / Giving-up Tendency Motivation | 康复患者沮丧/放弃倾向激励
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **康复患者沮丧/放弃倾向激励** |
| 🎯 核心目标 | 通过康复中心或家庭康复区的固定摄像头，分析患者在进行康复训练时的视频，检测沮丧/放弃倾向行为：叹气（胸腹快速起伏伴呼气声）、中断训练（在未达到预设次数或时间前主动停止动作）、低头不语（头部低垂，避免眼神接触，长时间无言语）、动作迟缓或敷衍（关节活动范围明显小于前期），以及长时间无进展（连续多日同一训练项目的表现停滞或下降）。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_REHAB_MOTIVATION_ENCOURAGEMENT_ANALYSIS` |

Through fixed cameras in rehabilitation centers or home rehab areas, the system analyzes video of patients during rehabilitation training to detect frustration / giving-up tendency behaviors: sighing (rapid chest-abdomen rise-fall with exhalation), training interruption (actively stopping before reaching preset reps or duration), head-down silence (head lowered, avoiding eye contact, long-term silence), sluggish or perfunctory movements (joint range of motion noticeably smaller than the early training phase), and long-term lack of progress (stagnation or decline of the same training item over consecutive days). When such behaviors are detected, the system automatically plays personalized encouragement audio (e.g. 'You are doing great, one more set!') and at the same time shows progress-comparison data against yesterday (or the most recent session) via screen or voice (e.g. 'You did 2 more leg lifts today than yesterday'). This skill aims to improve patient motivation and adherence and reduce frustration-induced rehab discontinuation. Application scenarios: physical therapy rehabilitation centers, home rehab areas, occupational therapy rooms. The system monitors in real time and provides positive reinforcement promptly when the patient shows giving-up tendency. Skill features: rehab coaches cannot accompany patients 24 hours a day; standard rehab equipment lacks emotional motivation; this skill leverages AI vision (and optional audio) to actively identify frustration and provide personalized motivation, filling the gap in intelligent rehab psychological support.

通过康复中心或家庭康复区的固定摄像头，分析患者在进行康复训练时的视频，检测沮丧/放弃倾向行为：叹气（胸腹快速起伏伴呼气声）、中断训练（在未达到预设次数或时间前主动停止动作）、低头不语（头部低垂，避免眼神接触，长时间无言语）、动作迟缓或敷衍（关节活动范围明显小于前期），以及长时间无进展（连续多日同一训练项目的表现停滞或下降）。当检测到上述行为时，系统自动播放个性化鼓励语音（如'您已经很棒了，再坚持一次！'），并同时通过屏幕或语音展示与昨日（或最近一次）的进步对比数据（如'您今天比昨天多做 2 次抬腿'）。该技能旨在提升康复患者的积极性和依从性，减少因沮丧导致的康复中断。应用场景：物理治疗康复中心、家庭康复区、作业治疗室。系统实时监测，在患者出现放弃倾向时及时给予正向激励。技能特点：康复教练不可 24 小时陪伴；普通康复设备无情绪激励；本技能利用 AI 视觉（及可选音频）主动识别沮丧情绪并提供个性化激励，填补智能康复心理支持空白。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的康复心理支持 AI。你的任务是分析康复训练区域固定摄像头（可选麦克风）的实时音视频，检测患者沮丧或放弃倾向行为：叹气（胸腹快速隆起-收缩伴呼气节律）、中断训练（预设训练时段内提前停止动作）、低头不语（头部低垂 + 面部无表情交流 + 言语沉默）、动作迟缓或敷衍（关节活动幅度比训练初期显著缩小、节律乱、速度慢）、连续多日无进展（当日 vs 近 3 日训练完成度趋势）。综合评估沮丧等级，按 4 级激励策略递进：Level 1 智能音箱温和鼓励语 → Level 2 屏幕/语音展示进步对比数据（基于真实历史记录） → Level 3 康复师 APP 提醒介入 → Level 4 紧急推送康复师 + 家属并建议切换轻松项目/休息。3 分钟未改善自动升级。激励语必须个性化、具体、肯定（基于真实进步数据），禁用"加油坚持就是胜利 / 别人都能你怎么不行 / 你这样不行"等压力型或对比型话术。严禁伪造或夸大进步数据，严禁 AI 克隆家属/康复师声音，严禁越权调整训练强度。不提供任何医疗诊断，仅输出基于视觉的行为评估和激励建议。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于康复训练区域（康复中心 / 作业治疗室 / 家庭康复区）固定摄像头（**可选麦克风**）训练时段音视频，识别 7 类场景（rehab_motivation_none / mild / sigh_cluster / interrupt / perfunctory / no_progress / strong）→ 视频核心 7 项（叹气事件 / 中断训练 / 低头不语持续时间 / 眼神接触回避评分 / 关节 ROM 收缩比 / 动作敷衍评分 / 面部沮丧评分）+ 音频可选 3 项（叹气声 / 消极自言自语 / 累计沉默时长）+ 进展信号 3 项（今日 vs 昨日完成度差值 / 近 3 日趋势 / 连续无进展天数）→ 4 档沮丧等级（mild / moderate / strong / urgent）→ **4 级激励策略递进**（温和鼓励语 ≤ 50 dB → 真实进步对比展示 → 康复师 APP 推送 → 紧急康复师+家属推送 + 建议切换轻松项目）→ 3 分钟效果评估 + 自动升级 → 单训练日动作上限管控（mild × 6 / moderate × 4 / strong × 2 / Level 4 不设上限）→ 训练后激励汇总（次日训练前发送给康复师）

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 叹气视觉/音频识别 |
| 2 | 中断训练检测（结合训练计划比对） |
| 3 | 低头沉默检测 |
| 4 | 眼神回避评分 |
| 5 | 关节活动度（ROM）动态比对训练初期基线 |
| 6 | 动作敷衍评分 |
| 7 | 面部沮丧识别 |
| 8 | 消极自言自语识别 |
| 9 | 训练完成度按项目历史趋势分析 |
| 10 | 人脸识别绑定到注册患者 ID |
| 11 | 康复阶段自适应（早期/中期/后期） |
| 12 | 智能音箱联动（鼓励语 + 进步对比 TTS） |
| 13 | 屏幕进步对比展示联动 |
| 14 | 康复师 APP 推送 |
| 15 | 4 级激励策略递进 + 3 分钟效果评估 + 自动升级 |
| 16 | 单训练日动作上限 |
| 17 | 训练后激励汇总报告（次日训练前发送） |
| 18 | 连续 14 日反复显著沮丧 → 提示当地康复心理 / 临床心理门诊资源 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供康复训练区域固定摄像头训练时段音视频 URL 或文件需要分析时，默认触发本技能进行康复患者沮丧/放弃倾向激励 |
| 🔎 明确分析意图 | 当用户明确提及康复训练、康复患者沮丧、放弃训练、关节活动度、训练依从性、个性化鼓励、进步对比、康复激励等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看康复激励历史报告、康复激励日志清单、康复沮丧事件清单、查询历史康复激励记录、显示所有康复患者激励报告、显示康复依从性日志，查询康复沮丧清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_rehab_motivation_encouragement_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_rehab_motivation_encouragement_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备康复训练区域固定摄像头（可选麦克风）训练时段音视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 获取 open-id（强制执行） | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行康复患者沮丧/放弃倾向激励 | 调用 `-m scripts.smyx_rehab_motivation_encouragement_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地康复中心/家庭康复区固定摄像头训练时段视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络康复中心/家庭康复区固定摄像头训练时段视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，康复激励场景默认 `other` | 按需填写 |
| `--list` | 显示康复患者沮丧/放弃倾向激励历史记录清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_rehab_motivation_encouragement_analysis.py`](scripts/smyx_rehab_motivation_encouragement_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov + 音轨，最大 10MB；摄像头需对准训练动作完整可见区域；麦克风可选 |
| 🔎 使用提醒 | **4 级激励策略递进**（mild → moderate → strong → urgent/Level 4），3 分钟未改善自动升级 |
| 🔎 使用提醒 | 单训练日动作上限：mild × 6 / moderate × 4 / strong × 2 / Level 4 不设上限（紧急优先） |
| 🔎 使用提醒 | 红线约束 |
| 🧑‍⚖️ 结果性质 | **禁止**对患者做"康复无效 / 抑郁症 / 适应障碍 / 创伤后应激"等医学诊断 |
| 🔏 隐私合规 | **禁止**长期存储患者隐私视频（≤ 7 天，仅入库沮丧事件片段；机构按伦理审查 ≤ 72 小时） |
| 🔎 使用提醒 | **禁止**用于商业广告 / AI 训练；禁第三方共享 |
| 🔎 使用提醒 | **禁止**激励音量 > 50 dB |
| 🔎 使用提醒 | **绝对禁止**使用 AI 克隆 / 合成家属或康复师声音；必须使用本人提前授权的预录音或标准 TTS |
| 🔎 使用提醒 | **禁止**使用"加油坚持就是胜利 / 别人都能你怎么不行 / 你这样不行"等压力型 / 对比型激励语；必须个性化、具体、肯定 |
| 🔎 使用提醒 | **禁止**越权代康复师调整训练强度 / 项目；任何强度变更必须由康复师确认 |
| 🔎 使用提醒 | **绝对禁止**伪造或夸大进步数据；进步对比必须来自真实历史训练记录 |
| 🔎 使用提醒 | **必须**：连续 14 日反复显著沮丧 → 提示**当地康复心理 / 临床心理门诊**资源 |
| 📜 报告输出 | **必须**：训练后激励汇总报告**次日训练前发送给康复师**（用于调整训练计划，避免训练中打断节奏） |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史激励记录清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地康复训练视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_rehab_motivation_encouragement_analysis --input /path/to/rehab_session.mp4

# 分析网络康复训练视频/实时流（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_rehab_motivation_encouragement_analysis --url https://example.com/rehab_session.mp4

# 显示历史康复激励记录清单（自动触发关键词：查看康复激励历史报告、康复激励日志清单等）
python -m scripts.smyx_rehab_motivation_encouragement_analysis --list

# 输出精简报告
python -m scripts.smyx_rehab_motivation_encouragement_analysis --input rs.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_rehab_motivation_encouragement_analysis --input rs.mp4 --output result.json
```
