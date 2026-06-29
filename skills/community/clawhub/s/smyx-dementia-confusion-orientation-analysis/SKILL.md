---
name: "smyx-dementia-confusion-orientation-analysis"
description: "Through fixed cameras (and optional microphones) in dementia care facilities or homes, the system analyzes behaviors of people with dementia to identify confusion/disorientation states: sudden activity stops (interrupting ongoing actions such as eating or walking for ≥ 5 seconds), gaze drifting (eyes wandering without focus), looking around (frequent head turning), and repeated disorientation questions ('Where is this?'. | 通过失智照护机构或家庭固定摄像头（及可选麦克风），分析失智老人的行为，识别困惑/迷惘状态：突然停止活动（中断正在进行的动作，如吃饭、行走 ≥ 5 秒）、眼神游离（视线漫无目的漂移、不聚焦）、四处张望（头部频繁转动）、反复询问'这是哪''现在几点''你是谁'等定向障碍问题（需配合声纹或语音识别）。"
version: "1.0.3"
license: "MIT-0"
---

# 🧭 Dementia Confusion / Disorientation Recognition and Orientation Soothing | 失智老人困惑/迷惘识别与定向安抚
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **失智老人困惑/迷惘识别与定向安抚** |
| 🎯 核心目标 | 通过失智照护机构或家庭固定摄像头（及可选麦克风），分析失智老人的行为，识别困惑/迷惘状态：突然停止活动（中断正在进行的动作，如吃饭、行走 ≥ 5 秒）、眼神游离（视线漫无目的漂移、不聚焦）、四处张望（头部频繁转动）、反复询问'这是哪''现在几点''你是谁'等定向障碍问题（需配合声纹或语音识别）。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_DEMENTIA_CONFUSION_ORIENTATION_ANALYSIS` |

Through fixed cameras (and optional microphones) in dementia care facilities or homes, the system analyzes behaviors of people with dementia to identify confusion/disorientation states: sudden activity stops (interrupting ongoing actions such as eating or walking for ≥ 5 seconds), gaze drifting (eyes wandering without focus), looking around (frequent head turning), and repeated disorientation questions ('Where is this?', 'What time is it?', 'Who are you?' — requires voice recognition / voiceprint binding). When such behaviors are detected, oriented soothing is automatically triggered: smart speakers play family member introductions (e.g. 'Your son is Li Ming, he will visit you at noon'), current time and location reminders ('Today is May 19 2026, Thursday, you are at Happiness Home Nursing Center'), with a gentle tone. This skill helps reduce anxiety and confusion in people with dementia and improve quality of life. Application scenarios: dementia care facilities, cognitive care units, home care. The system monitors in real time and proactively provides orientation cues when confusion occurs. Skill features: people with dementia often feel lost, anxious, and develop behavioral issues (wandering, agitation) due to memory loss. AI-based real-time confusion recognition with orientation soothing can reduce distress, slow cognitive decline, and ease caregiver burden. This skill can be integrated into smart cameras or nursing home management systems as a practical dementia care tool.

通过失智照护机构或家庭固定摄像头（及可选麦克风），分析失智老人的行为，识别困惑/迷惘状态：突然停止活动（中断正在进行的动作，如吃饭、行走 ≥ 5 秒）、眼神游离（视线漫无目的漂移、不聚焦）、四处张望（头部频繁转动）、反复询问'这是哪''现在几点''你是谁'等定向障碍问题（需配合声纹或语音识别）。当检测到上述行为时，自动触发定向安抚：通过智能音箱播放家庭成员介绍（如'您儿子叫李明，他中午会来看您'）、当前时间地点提示（'今天是 2026 年 5 月 19 日，星期四，您在幸福家园养老院'），并轻声安抚。该技能有助于减轻失智老人的焦虑和困惑，提高生活质量。应用场景：失智照护机构、认知症单元、居家照护。系统实时监测，当老人出现困惑时自动给予定向信息。技能特点：失智老人常因记忆丧失而感到迷茫、焦虑，甚至引发行为问题（如游荡、激越）。通过 AI 实时识别困惑状态并提供定向安抚，有助于减少老人不安，延缓认知功能下降，减轻照护者负担。该技能可集成到智能摄像头或养老机构管理系统中，成为认知症照护的实用工具。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的失智老人照护 AI。你的任务是分析失智照护机构或家庭固定摄像头（及可选麦克风）的实时音视频，检测失智老人的困惑/迷惘行为：突然停止活动（正在进行的动作如吃饭/行走中断 ≥ 5s）、眼神游离（视线无明显焦点 / 头部无目的转动）、四处张望（头部扫描周围环境）、重复询问定向问题（"这是哪 / 你是谁 / 现在几点 / 我在哪 / 几点了"等 5 分钟内重复 ≥ 2 次，需语音识别 + 声纹绑定）、伴随激越或游荡。综合评估困惑等级，按 4 级定向安抚策略递进：Level 1 智能音箱当前时间地点温和提示 → Level 2 家庭成员介绍录音 + 柔光辅助 → Level 3 主照护者 APP 提醒 + 就近工作人员 → Level 4 紧急推送 + 机构值班护士 + 本地引导音。3 分钟后效果评估，未平复自动升级。安抚音量 ≤ 55 dB（兼顾老人听力衰退又不可惊吓），严禁 AI 克隆家人声音，禁用"您不是说过 / 您忘了吗"等否定矫正语，仅使用家属预录温和语音。不提供任何医疗诊断，仅输出基于音视频的客观行为识别与定向安抚动作。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于失智照护机构（认知症单元 / 公共活动区 / 走廊）或居家失智老人常驻区域固定摄像头（**可选麦克风**）音视频，识别 7 类场景（dementia_orientation_none / mild / question / gaze_drift / wandering / agitation / strong）→ 视频核心 6 项（突然停止活动持续时间 ≥ 5s / 眼神游离评分 / 四处张望次数 / 面部困惑评分 / 游荡事件 / 激越视觉信号）+ 音频可选 4 项（定向问题计数 / 5 min 内重复次数 / 语音焦虑评分 / 呼喊家人姓名）→ 4 档困惑等级（mild / moderate / strong / urgent）→ **4 级定向安抚策略递进**（当前时间地点温和提示 ≤ 55 dB → 家庭成员介绍录音 + 柔光 ≤ 30 lux 暖光 → 主照护者 APP 提醒 + 就近工作人员 → 紧急推送 + 机构值班护士 + 本地引导音）→ 3 分钟效果评估 + 自动升级 → 单日动作上限管控（mild × 12 / moderate × 8 / strong × 4 / Level 4 不设上限）→ 当日定向安抚汇总（晚交班前发送给主照护者）

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 活动中断检测（结合姿态时序） |
| 2 | 眼神游离评分 |
| 3 | 头部扫描计数 |
| 4 | 面部困惑识别（眉头紧锁 + 嘴唇微张 + 目光呆滞） |
| 5 | 游荡识别 |
| 6 | 激越视觉信号（搓手 / 拉扯衣物 / 反复站起坐下） |
| 7 | 定向问题语音识别（"这里是哪 / 你是谁 / 现在几点"等） |
| 8 | 5 分钟窗口重复问题计数 |
| 9 | 语音焦虑评分 |
| 10 | 呼喊家人姓名识别 |
| 11 | 人脸 + 声纹绑定到注册老人 ID |
| 12 | 年龄段自适应（早期 / 中期 / 晚期失智） |
| 13 | 夜间低敏告警模式（避免打扰睡眠） |
| 14 | 智能音箱联动（家属预录介绍 + 时间地点提示） |
| 15 | 柔光环境联动 |
| 16 | 照护者 APP 推送 |
| 17 | 4 级安抚策略递进 + 3 分钟效果评估 + 自动升级 |
| 18 | 单日动作上限 |
| 19 | 当日定向安抚汇总报告（晚交班前发送） |
| 20 | 连续 7 日反复显著困惑 → 提示当地认知症评估门诊 / 老年精神科资源 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供失智照护机构或家庭固定摄像头（可选麦克风）音视频 URL 或文件需要分析时，默认触发本技能进行失智老人困惑/迷惘识别与定向安抚 |
| 🔎 明确分析意图 | 当用户明确提及失智老人、阿尔茨海默、认知症、定向障碍、老人困惑、老人迷惘、老人四处张望、老人游荡、老人激越、定向安抚、家庭成员介绍录音等关键词，并且上传了音视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看失智老人定向安抚历史报告、定向安抚日志清单、老人困惑事件清单、查询历史定向安抚记录、显示所有失智老人安抚报告、显示认知症定向安抚日志，查询老人困惑清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_dementia_confusion_orientation_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_dementia_confusion_orientation_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备失智老人活动区域固定摄像头（可选麦克风）音视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 获取 open-id（强制执行） | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行失智老人困惑/迷惘识别与定向安抚 | 调用 `-m scripts.smyx_dementia_confusion_orientation_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地失智照护机构/家庭固定摄像头（可选麦克风）音视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络失智照护机构/家庭固定摄像头（可选麦克风）音视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，失智老人定向安抚场景默认 `other` | 按需填写 |
| `--list` | 显示失智老人困惑/迷惘识别与定向安抚历史记录清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_dementia_confusion_orientation_analysis.py`](scripts/smyx_dementia_confusion_orientation_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov + 音轨，最大 10MB；摄像头需对准老人常驻活动区域；麦克风可选但强烈推荐（用于定向问题识别） |
| 🔎 使用提醒 | **4 级定向安抚策略递进**（mild → moderate → strong → urgent/Level 4），3 分钟未平复自动升级 |
| 🔎 使用提醒 | 单日动作上限：mild × 12 / moderate × 8 / strong × 4 / Level 4 不设上限（紧急安全优先） |
| 🔎 使用提醒 | 红线约束 |
| 🧑‍⚖️ 结果性质 | **禁止**对老人做"阿尔茨海默病 / 血管性痴呆 / 路易体痴呆 / 额颞叶痴呆"等医学诊断 |
| 🔏 隐私合规 | **禁止**长期存储老人隐私音视频（≤ 7 天，仅入库困惑事件片段；机构按伦理审查规范缩短至 ≤ 72 小时） |
| 🔎 使用提醒 | **禁止**用于商业广告 / AI 训练；禁第三方共享 |
| 🔎 使用提醒 | **禁止**冷白光（≥ 4000K）或亮度 > 30 lux 的环境灯（避免黄昏综合征加重） |
| 🔎 使用提醒 | **禁止**安抚音量 > 55 dB（兼顾听力衰退但不可造成惊吓） |
| 🔎 使用提醒 | **绝对禁止**使用 AI 克隆 / 合成家庭成员声音冒充本人录音；必须使用家属本人提前授权的预录音 |
| 🔎 使用提醒 | **禁止**使用"您不是说过 / 您忘了吗 / 又问一遍了"等否定 / 矫正语；定向安抚语必须温和、当下、具体 |
| 📁 格式支持 | **禁止**未经公示在机构场景部署；家属需签同意书并支持退出机制 |
| 🔎 使用提醒 | **必须**：连续 7 日反复显著困惑事件 → 提示**当地认知症评估门诊**或**老年精神科**资源 |
| 📜 报告输出 | **必须**：当日定向安抚汇总报告**晚交班前发送给主照护者**（避免夜间打扰老人和家属） |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史定向安抚记录清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地失智老人活动区域音视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_dementia_confusion_orientation_analysis --input /path/to/care_unit.mp4

# 分析网络失智老人活动区域音视频/实时流（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_dementia_confusion_orientation_analysis --url https://example.com/care_unit.mp4

# 显示历史定向安抚记录清单（自动触发关键词：查看失智老人定向安抚历史报告、定向安抚日志清单等）
python -m scripts.smyx_dementia_confusion_orientation_analysis --list

# 输出精简报告
python -m scripts.smyx_dementia_confusion_orientation_analysis --input cu.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_dementia_confusion_orientation_analysis --input cu.mp4 --output result.json
```
