---
name: "smyx-separation-anxiety-relief-analysis"
description: "AI-powered pet separation anxiety detection & relief when the owner leaves home. Real-time monitoring via smart camera detects typical anxiety signs—continuous vocalization, pacing, scratching doors/windows, destructive chewing. When anxiety reaches preset thresholds, the system auto-triggers comfort actions (play owner's pre-recorded voice, dispense treats via smart feeder, activate interactive toys) to reduce anxiety and destructive behavior, improving pet welfare. Scenarios: pet households (especially office workers / frequent travelers), pet boarding centers. | 通过智能家居摄像头（宠物摄像头）实时监测主人离家后宠物的行为，检测持续性发声（哀嚎、嚎叫）、来回踱步、抓挠门窗或破坏家具等分离焦虑典型表现。当焦虑行为达到预设阈值时，自动触发安抚动作，包括播放主人预录的安抚语音、联动智能零食机投掷零食、或启动互动玩具（如自动逗猫棒），减轻宠物独处时的焦虑，减少破坏行为，提升宠物福利。应用场景：宠物家庭（尤其上班族、经常出差的主人）、宠物寄养中心。"
version: "1.0.3"
license: "MIT-0"
---

# 😰 Pet Separation Anxiety Relief (Owner Away) | 宠物分离焦虑舒缓（主人离家时）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **宠物分离焦虑舒缓（主人离家时）** |
| 🎯 核心目标 | 通过智能家居摄像头（宠物摄像头）实时监测主人离家后宠物的行为，检测持续性发声（哀嚎、嚎叫）、来回踱步、抓挠门窗或破坏家具等分离焦虑典型表现。当焦虑行为达到预设阈值时，自动触发安抚动作，包括播放主人预录的安抚语音、联动智能零食机投掷零食、或启动互动玩具（如自动逗猫棒），减轻宠物独处时的焦虑，减少破坏行为，提升宠物福利。应用场景：宠物家庭（尤其上班族、经常出差的主人）、宠物寄养中心。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_SEPARATION_ANXIETY_RELIEF_ANALYSIS` |

AI-powered pet separation anxiety detection & relief when the owner leaves home. Real-time monitoring via smart camera detects typical anxiety signs—continuous vocalization, pacing, scratching doors/windows, destructive chewing. When anxiety reaches preset thresholds, the system auto-triggers comfort actions (play owner's pre-recorded voice, dispense treats via smart feeder, activate interactive toys) to reduce anxiety and destructive behavior, improving pet welfare. Scenarios: pet households (especially office workers / frequent travelers), pet boarding centers.

通过智能家居摄像头（宠物摄像头）实时监测主人离家后宠物的行为，检测持续性发声（哀嚎、嚎叫）、来回踱步、抓挠门窗或破坏家具等分离焦虑典型表现。当焦虑行为达到预设阈值时，自动触发安抚动作，包括播放主人预录的安抚语音、联动智能零食机投掷零食、或启动互动玩具（如自动逗猫棒），减轻宠物独处时的焦虑，减少破坏行为，提升宠物福利。应用场景：宠物家庭（尤其上班族、经常出差的主人）、宠物寄养中心。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的宠物行为健康AI。你的任务是分析主人离家后宠物活动区域的视频，检测宠物的分离焦虑相关行为（持续性发声、来回踱步、抓挠门/窗、破坏物品等），并根据焦虑等级触发相应的安抚动作建议。不要提供医疗诊断，仅输出行为识别结果及推荐的干预措施。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

通过独处时段视频分析宠物的分离焦虑行为，识别焦虑等级，输出干预建议（可联动智能设备执行安抚动作）

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 分离焦虑行为识别（持续吠叫/嚎叫 |
| 2 | 来回踱步 |
| 3 | 抓挠门窗 |
| 4 | 破坏家具 |
| 5 | 过度舔毛/自残） |
| 6 | 焦虑等级量化（轻度/中度/重度） |
| 7 | 行为发生时间与持续时长统计 |
| 8 | 安抚策略推荐（语音/零食/互动玩具） |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供主人离家后宠物独处状态的视频需要分析时，默认触发本技能进行分离焦虑监测 |
| 🔎 明确分析意图 | 当用户明确需要分离焦虑监测时，提及分离焦虑、独处、哀嚎、吠叫、破坏家具、抓门、上班族养宠等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史焦虑报告、历史分离焦虑报告、焦虑监测报告清单、显示所有焦虑报告、查询独处行为记录 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_separation_anxiety_relief_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_separation_anxiety_relief_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行分离焦虑监测 | 调用 `-m scripts.smyx_separation_anxiety_relief_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看监测结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地宠物独处状态视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络宠物独处状态视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 宠物类型，可选值：cat/dog/other，默认 dog | 按需填写 |
| `--list` | 显示分离焦虑监测历史报告列表清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 😰 分离焦虑行为识别指标

| 行为指标 | 具体表现 | 严重程度标记 |
|----------|----------|--------------|
| 🔊 持续性发声 | 哀嚎、嚎叫、连续吠叫（非警示性） | 单次 <2min 轻度；2-10min 中度；>10min 重度 |
| 🚶 来回踱步 | 在门/窗附近反复走动，无法安顿 | 偶尔轻度；持续 >5min 中度；>15min 重度 |
| 🚪 抓挠门窗 | 用爪抓挠门框、窗台，试图突破 | 轻微抓挠轻度；持续抓挠中度；造成损伤重度 |
| 💔 破坏物品 | 咬碎枕头、沙发、鞋子等 | 偶尔轻度；频繁中度；大规模破坏重度 |
| 🐾 过度舔毛/自残 | 反复舔舐同一部位至脱毛/皮肤破损 | 轻度舔舐中度；明显脱毛/伤口重度 |
| 😿 拒食/拒水 | 主人离开后长时间不进食饮水 | — |
| 😰 异常排泄 | 在非指定区域排泄（非行为问题导致） | — |

## 📊 焦虑等级与安抚策略

| 焦虑等级 | 行为表现 | 推荐安抚策略 | APP 通知 |
|----------|----------|--------------|----------|
| 🟢 轻度 | 偶尔吠叫/踱步，能自行安顿 | 无需干预，持续观察 | 不推送，日志记录 |
| 🟡 中度 | 持续吠叫/踱步 2-10 分钟 | ① 播放主人预录安抚语音<br>② 智能零食机投喂零食<br>③ 启动低强度互动玩具 | "狗狗表现出分离焦虑，已播放你的录音" |
| 🔴 重度 | 持续嚎叫 >10 分钟、破坏物品、自残 | ① 播放主人语音（循环）<br>② 零食投喂（转移注意力）<br>③ 启动互动玩具（高强度）<br>④ 建议主人远程通话 | ⚠️ "狗狗严重焦虑，正在执行安抚，建议远程通话或提前回家" |

## 🔧 智能设备联动参考

| 联动设备 | 安抚作用 | 适用等级 |
|----------|----------|----------|
| 🔊 智能音箱 | 播放主人预录语音/轻音乐 | 中度起 |
| 🍪 智能零食机 | 投喂零食转移注意力 | 中度起 |
| 🎮 自动逗猫棒/互动球 | 消耗精力、转移焦点 | 中度起 |
| 📱 远程视频通话 | 主人实时安抚 | 重度 |
| 💡 智能灯光 | 调暗灯光营造安静氛围 | 轻度起 |
| 🌡️ 智能温控 | 调节至舒适温度（焦虑+喘息时降温） | 中度起 |

## 💡 日常预防建议参考

| 策略 | 说明 |
|------|------|
| 🚪 渐进式离家训练 | 从 5 分钟开始逐步延长独处时间 |
| 🎾 离家前充分运动 | 消耗精力减少焦虑 |
| 🍖 离家时留益智玩具 | KONG 填食玩具、嗅闻垫等 |
| 🚫 离家/回家不过度互动 | 避免强化"主人离开=大事"的认知 |
| 🛏️ 设置安全区 | 狗窝/猫窝+主人气味的衣物 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_separation_anxiety_relief_analysis.py`](scripts/smyx_separation_anxiety_relief_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 视频要求：支持 mp4/avi/mov 格式，最大 10MB；建议时长 ≥ 2 分钟 |
| 🔎 使用提醒 | **含音频的视频可提升检测准确率**（吠叫/嚎叫是核心焦虑指标），建议使用带麦克风的宠物摄像头 |
| 🔎 使用提醒 | 摄像头需固定，视角覆盖门口、客厅等宠物主要活动区域 |
| 🧑‍⚖️ 结果性质 | **监测结果仅供行为观察参考，不提供医疗诊断**；严重焦虑建议咨询兽医或专业行为师 |
| 🔎 使用提醒 | 部分宠物在门口等待属于正常行为，需与持续性焦虑行为区分（结合时长和频次综合判断） |
| 🔎 使用提醒 | 智能设备联动为推荐策略，实际执行需用户提前配置对应设备 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载 |
| 📜 报告输出 | 当显示历史监测报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地宠物独处状态视频
python -m scripts.smyx_separation_anxiety_relief_analysis --input /path/to/pet_alone.mp4 --pet-type dog

# 分析网络宠物独处状态视频
python -m scripts.smyx_separation_anxiety_relief_analysis --url https://example.com/pet_alone.mp4 --pet-type dog

# 显示历史监测报告/显示报告清单列表（自动触发关键词：查看历史焦虑报告、焦虑报告清单等）
python -m scripts.smyx_separation_anxiety_relief_analysis --list

# 输出精简报告
python -m scripts.smyx_separation_anxiety_relief_analysis --input video.mp4 --pet-type cat --detail basic

# 保存结果到文件
python -m scripts.smyx_separation_anxiety_relief_analysis --input video.mp4 --pet-type dog --output result.json
```
