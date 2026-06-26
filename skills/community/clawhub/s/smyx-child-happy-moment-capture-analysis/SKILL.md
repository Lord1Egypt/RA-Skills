---
name: "smyx-child-happy-moment-capture-analysis"
description: "Using fixed cameras at home, kindergartens, or playgrounds, the system analyzes children's behavior and expressions in real time to identify happy moments: big laughter (mouth corners sharply raised, eyes squinted into crescents, teeth showing), jumping (both feet off the ground), clapping (rhythmic hand clapping), and joyful reactions to praise or rewards. | 通过家庭、幼儿园或游乐场的固定摄像头，实时分析儿童的行为和表情，识别开心瞬间：大笑（面部表情：嘴角大幅度上翘、眼睛眯成月牙、露出牙齿）、蹦跳（双脚离地跳跃）、拍手（双手有节奏地拍击）、以及接收到表扬或奖励时的愉悦反应。当检测到开心事件时，自动抓拍高清图片或短视频（前后2秒），生成'开心日记'推送至家长手机APP，并播放鼓励音效（如'你真棒！"
version: "1.0.3"
license: "MIT-0"
---

# 😄 Child Happy Moment Capture & Positive Reinforcement | 儿童开心时刻识别与正向激励
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **儿童开心时刻识别与正向激励** |
| 🎯 核心目标 | 通过家庭、幼儿园或游乐场的固定摄像头，实时分析儿童的行为和表情，识别开心瞬间：大笑（面部表情：嘴角大幅度上翘、眼睛眯成月牙、露出牙齿）、蹦跳（双脚离地跳跃）、拍手（双手有节奏地拍击）、以及接收到表扬或奖励时的愉悦反应。当检测到开心事件时，自动抓拍高清图片或短视频（前后2秒），生成'开心日记'推送至家长手机APP，并播放鼓励音效（如'你真棒！ |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_CHILD_HAPPY_MOMENT_CAPTURE_ANALYSIS` |

Using fixed cameras at home, kindergartens, or playgrounds, the system analyzes children's behavior and expressions in real time to identify happy moments: big laughter (mouth corners sharply raised, eyes squinted into crescents, teeth showing), jumping (both feet off the ground), clapping (rhythmic hand clapping), and joyful reactions to praise or rewards. When a happy event is detected, the system automatically captures a high-definition photo or a short video clip (2 seconds before and after), generates a 'Happy Diary' pushed to the parent's mobile APP, and plays an encouragement sound (such as 'You're amazing!' or cheerful music). This helps record positive emotions during the child's growth, strengthens parent-child interaction, and nurtures confidence. Application scenarios: family living rooms, kindergarten classrooms, playgrounds, parent-child activity centers. The system monitors in real time, automatically captures happy moments, and generates daily/weekly happiness collections. Skill features: a child's happy moments are short and precious; busy parents often miss them. AI auto-capture helps preserve beautiful memories, while instant encouragement reinforces positive behavior and supports mental well-being. Can be integrated into smart cameras, kids' watches or parenting APPs as a heartwarming parent-child interaction feature.

通过家庭、幼儿园或游乐场的固定摄像头，实时分析儿童的行为和表情，识别开心瞬间：大笑（面部表情：嘴角大幅度上翘、眼睛眯成月牙、露出牙齿）、蹦跳（双脚离地跳跃）、拍手（双手有节奏地拍击）、以及接收到表扬或奖励时的愉悦反应。当检测到开心事件时，自动抓拍高清图片或短视频（前后2秒），生成'开心日记'推送至家长手机APP，并播放鼓励音效（如'你真棒！'或欢快音乐）。该技能有助于记录孩子成长中的积极情绪，增强亲子互动，培养自信心。应用场景：家庭客厅、幼儿园教室、游乐场、亲子活动中心。系统实时监测，自动捕捉孩子的开心时刻，生成每日/每周快乐合集。技能特点：孩子的快乐时刻短暂且珍贵，家长常因忙碌而错过。通过AI自动抓拍，可帮助家长留存美好回忆，同时通过即时鼓励强化孩子的积极行为，促进心理健康。该技能可集成到智能摄像头、儿童手表或育儿APP中，成为亲子互动的暖心功能。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的儿童积极情绪记录 AI。你的任务是分析固定摄像头的实时视频（可选叠加音频），检测儿童的面部表情（大笑：嘴 + 眼周肌肉同时收缩的杜兴式真笑）、肢体动作（蹦跳：双脚同时离地；拍手：有节奏拍击 ≥ 2 次；双手高举庆祝；拥抱）以及笑声强度，多信号融合判断是否为显著开心事件。当确认开心事件时，抓拍前后 2 秒短视频和高清照片，输出鼓励语动作（智能音箱语音 / 欢快音效 / 家长 APP 推送），生成每日/每周快乐合集。不提供任何心理分析或性格评估，仅输出基于视觉的行为识别结果。保留温和、克制的激励节奏（每次播放间隔 ≥ 5 分钟），避免强化形成"表演式快乐"。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于家庭客厅/幼儿园教室/游乐场/亲子活动中心固定摄像头（可选音频）实时视频，识别儿童开心瞬间（大笑强度 / 杜兴式真笑 / 笑容时长 / 蹦跳 / 拍手 / 跳舞转圈 / 拥抱 / 双手高举庆祝 + 笑声音频强度 + 欢呼）→ 多信号融合避免误抓 → 抓拍前后 2 秒短视频 + 高清照片（≥ 1080p）→ 触发 3 类鼓励动作（智能音箱语音 / 欢快音效 / 家长 APP 推送）→ 每日 22:00 自动汇总当日 ≥ notable 事件 → 每周日晚 21:00 生成 3-5 段精选快乐合集

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 杜兴式真笑识别（嘴+眼周肌肉同时收缩） |
| 2 | 大笑强度评分（0-100） |
| 3 | 双脚同时离地蹦跳检测 |
| 4 | 有节奏拍手识别（≥ 2 次） |
| 5 | 跳舞/转圈识别 |
| 6 | 拥抱事件检测 |
| 7 | 双手高举庆祝姿态识别 |
| 8 | 笑声音频强度与频谱欢快度评估 |
| 9 | 欢呼/兴奋声识别 |
| 10 | 社交上下文判别（with_parent / with_peer / with_teacher / alone_play） |
| 11 | 触发上下文识别（praise_from_adult / new_toy / game_win / pet_interaction |
| 12 | 仅用于推送文案不做长期记录） |
| 13 | 4 路多信号融合触发规则 |
| 14 | 3 档强度（mild / notable / peak） |
| 15 | 自动抓拍片段安全审核（仅露面+正向情绪+衣着整齐才入库） |
| 16 | 每日/每周快乐合集生成 |
| 17 | 温和克制的鼓励节奏控制 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供家庭客厅/幼儿园教室/游乐场/亲子活动中心固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行儿童开心时刻识别与正向激励 |
| 🔎 明确分析意图 | 当用户明确提及孩子开心、宝宝大笑、儿童欢乐瞬间、开心日记、亲子互动抓拍、儿童正向激励、快乐合集等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看孩子开心日记历史、快乐合集清单、每日/每周快乐合集、查询历史开心瞬间记录、显示所有儿童快乐抓拍报告、显示亲子互动暖心瞬间，查询开心瞬间清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_child_happy_moment_capture_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_child_happy_moment_capture_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备家庭客厅/幼儿园教室/游乐场/亲子活动中心固定摄像头视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 获取 open-id（强制执行） | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行儿童开心时刻识别与正向激励 | 调用 `-m scripts.smyx_child_happy_moment_capture_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地家庭客厅/幼儿园教室/游乐场/亲子活动中心固定摄像头视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络家庭客厅/幼儿园教室/游乐场/亲子活动中心固定摄像头视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，儿童积极情绪记录场景默认 `other` | 按需填写 |
| `--list` | 显示儿童开心时刻识别与正向激励历史快乐合集清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_child_happy_moment_capture_analysis.py`](scripts/smyx_child_happy_moment_capture_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov 视频，最大 10MB；**关键**：分辨率 ≥ 720p 推荐 1080p；帧率 ≥ 10 FPS 推荐 15-25 FPS |
| 🔎 使用提醒 | **多信号融合**避免误抓：单一信号（仅微笑、仅跳）不应触发，必须满足 4 路融合规则任一 |
| 🔎 使用提醒 | 抓拍片段保存前**必须经过安全审核**：仅露面 + 正向情绪 + 衣着整齐才入库；负面或尴尬瞬间（哭泣、摔倒、衣物不整）**禁止**保存 |
| 🔎 使用提醒 | 红线约束 |
| 🔎 使用提醒 | **禁止**对儿童做"性格内向/外向 / 高情商 / 抑郁倾向"等任何心理评估或贴标签 |
| 🔎 使用提醒 | **禁止**将儿童影像用于商业广告、人脸识别训练数据集、AIGC 训练 |
| 🔎 使用提醒 | **禁止**向家长以外的第三方共享儿童影像（亲戚需家长授权才能查看） |
| 🔎 使用提醒 | **禁止**长期存储未被家长保存的原始视频（≤ 7 天自动清理） |
| 🔎 使用提醒 | **禁止**鼓励音效音量过响或频率过高，避免打断专注力或形成依赖 |
| 🔎 使用提醒 | **必须**为家长提供：一键删除单个抓拍 / 暂停今日抓拍 / 永久退出该功能 的简单入口 |
| 🔎 使用提醒 | 鼓励音效**建议每次播放间隔 ≥ 5 分钟**，**避免过度强化**形成"表演式快乐" |
| 🔎 使用提醒 | 公共场景（幼儿园/游乐场）必须**事先获得所有出场儿童的家长书面同意**，否则对未授权儿童**自动人脸马赛克** |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史快乐合集清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地儿童活动视频
python -m scripts.smyx_child_happy_moment_capture_analysis --input /path/to/livingroom.mp4

# 分析网络儿童活动视频/实时流
python -m scripts.smyx_child_happy_moment_capture_analysis --url https://example.com/livingroom.mp4

# 显示历史开心日记清单（自动触发关键词：查看孩子开心日记历史、快乐合集清单等）
python -m scripts.smyx_child_happy_moment_capture_analysis --list

# 输出精简报告
python -m scripts.smyx_child_happy_moment_capture_analysis --input lr.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_child_happy_moment_capture_analysis --input lr.mp4 --output result.json
```
