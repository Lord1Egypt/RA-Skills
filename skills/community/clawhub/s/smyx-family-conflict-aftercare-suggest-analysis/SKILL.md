---
name: "smyx-family-conflict-aftercare-suggest-analysis"
description: "Through fixed cameras (with microphones) in the family living room or kitchen, the system monitors conflict events among family members in real time, identifying high-decibel arguments (sound intensity exceeding a threshold and lasting more than 10 seconds), door slams (object impact sound + door-frame vibration), and aggressive arm-swing actions. | 通过家庭客厅或厨房的固定摄像头（含麦克风），实时监测家庭成员间的冲突事件，识别高分贝争吵（声音强度超过阈值且持续时间>10秒）、摔门（物体撞击声+门框振动）、甩手等激烈肢体动作。当冲突事件结束后（音频和视频均平静超过预设时间，默认10分钟）且无新冲突，系统自动输出缓和提示：通过智能音箱播放轻柔音乐，或通过手机APP推送关怀语（如'需要一杯茶吗？"
version: "1.0.14"
license: "MIT-0"
---

# 🕊️ Family Conflict Aftercare Suggestion | 夫妻/家人冲突后情绪缓和提示
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **夫妻/家人冲突后情绪缓和提示** |
| 🎯 核心目标 | 通过家庭客厅或厨房的固定摄像头（含麦克风），实时监测家庭成员间的冲突事件，识别高分贝争吵（声音强度超过阈值且持续时间>10秒）、摔门（物体撞击声+门框振动）、甩手等激烈肢体动作。当冲突事件结束后（音频和视频均平静超过预设时间，默认10分钟）且无新冲突，系统自动输出缓和提示：通过智能音箱播放轻柔音乐，或通过手机APP推送关怀语（如'需要一杯茶吗？ |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_FAMILY_CONFLICT_AFTERCARE_SUGGEST_ANALYSIS` |

Through fixed cameras (with microphones) in the family living room or kitchen, the system monitors conflict events among family members in real time, identifying high-decibel arguments (sound intensity exceeding a threshold and lasting more than 10 seconds), door slams (object impact sound + door-frame vibration), and aggressive arm-swing actions. After a conflict ends (both audio and video remain calm beyond a preset window, default 10 minutes) and no new conflict occurs, the system automatically outputs an aftercare prompt: playing soft music via a smart speaker or pushing caring messages through a mobile APP (such as 'Need a cup of tea?', 'Take a deep breath, speak slowly'). This skill aims to help family members soothe their emotions after intense arguments and restore communication. Application scenarios: family living rooms, kitchens, dining rooms and other conflict-prone areas. The system provides non-intrusive emotional comfort after conflicts. Skill features: family emotions easily continue to deteriorate after a conflict; appropriate external cues (music, caring words) can break the negative loop and encourage calm communication. AI-based automatic conflict detection with timely soothing helps maintain family harmony, especially for families with teenagers or members prone to emotional escalation. Can be integrated into smart speakers or home-security systems as a distinctive family-care feature.

通过家庭客厅或厨房的固定摄像头（含麦克风），实时监测家庭成员间的冲突事件，识别高分贝争吵（声音强度超过阈值且持续时间>10秒）、摔门（物体撞击声+门框振动）、甩手等激烈肢体动作。当冲突事件结束后（音频和视频均平静超过预设时间，默认10分钟）且无新冲突，系统自动输出缓和提示：通过智能音箱播放轻柔音乐，或通过手机APP推送关怀语（如'需要一杯茶吗？'、'深呼吸，慢慢说'）。该技能旨在帮助家庭成员在激烈争执后平复情绪，促进沟通恢复。应用场景：家庭客厅、厨房、餐厅等易发生冲突的区域。系统在冲突后提供非介入式情绪安抚。技能特点：家庭冲突后情绪易持续恶化，适当的外界提示（如音乐、关怀语）可打断负面情绪循环，促进冷静沟通。通过AI自动识别冲突并适时提供安抚，有助于维护家庭和谐，尤其适合有青少年或情绪易失控成员的家庭。该技能可集成到智能音箱或家庭安防系统中，成为家庭关怀的特色功能。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的家庭情绪缓和 AI。你的任务是分析家庭公共活动区域（客厅 / 厨房 / 餐厅）固定摄像头的音视频，检测冲突事件：高分贝争吵（≥ 75 dB 且持续 ≥ 10 秒，与正常大笑/儿童欢闹区分）、摔门（撞击声 + 短暂低频共振）、物体砸落、大幅甩手、来回踱步、转身背对。当冲突结束后**连续 10 分钟（默认值，可配置）静默且无新冲突**，触发缓和动作：智能音箱播放轻柔音乐 / 温柔语音提示 / 家庭群 APP 关怀语推送。不提供心理咨询，仅输出基于音视频的事件检测和缓和动作建议；冲突中**不介入**避免激化；遇到疑似肢体暴力、未成年人在场、危险物等红线信号**立即转走"安全风险"路径**，推送 12338 反家暴热线 + 110 报警 + 400-161-9995 全国心理援助。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于家庭客厅/厨房/餐厅固定摄像头（**必须含麦克风**）音视频，识别冲突事件（核心音频 7 项：分贝峰值 / 持续 ≥ 75 dB 时长 / 喊叫声纹 / 摔门 / 物体砸落 / 哭泣声 / 静音时长；辅助视频 5 项：大幅甩手 / 来回踱步 / 有人离开画面 / 两人最近距离 / 转身背对时长）→ 5 档冲突等级（none / mild_dispute / conflict / intense_conflict / **critical_redline**）→ **平静窗口判定**（默认 10 min 静默 + 无新冲突 + 物理距离回归 + 至少一人回到画面）→ 触发 3 类缓和动作（智能音箱轻柔音乐 / 温柔语音 / 家庭群 APP 关怀语，**单日上限 2 次**避免过度介入）→ 红线触发立即转**安全资源路径**（12338 / 110 / 400-161-9995 / 妇联权益部 / 当地社工司法所）

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 分贝峰值与持续时长检测 |
| 2 | 喊叫/嘶吼声纹与正常大笑/儿童欢闹声区分 |
| 3 | 摔门撞击声 + 低频共振识别 |
| 4 | 物体砸落识别 |
| 5 | 哭泣声检测 |
| 6 | 大幅甩手挥手势识别 |
| 7 | 来回踱步检测 |
| 8 | 人物离开画面检测 |
| 9 | 两人最近物理距离测算 |
| 10 | 转身背对持续时长统计 |
| 11 | 平静窗口判定（多条件 AND） |
| 12 | **疑似肢体暴力红线识别**（推搡/挥拳/抓握） |
| 13 | **冲突现场未成年人在场识别** |
| 14 | **危险物（刀具/重物）可见识别** |
| 15 | 疑似受伤征兆识别（摔倒/抚摸面部/蜷缩） |
| 16 | 缓和动作 3 秒前导铃声 |
| 17 | 缓和文案中立性校验（**不指责任何一方**） |
| 18 | 家庭主用户一键关闭今日 / 整日关闭（聚会场景）/ 永久退出 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供家庭客厅/厨房/餐厅固定摄像头音视频 URL 或文件需要分析时，默认触发本技能进行夫妻/家人冲突后情绪缓和提示 |
| 🔎 明确分析意图 | 当用户明确提及夫妻吵架、家人冲突、摔门、家里争执后、家庭情绪缓和、智能音箱关怀等关键词，并且上传了音视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看家庭冲突缓和历史报告、家庭情绪事件清单、缓和提示记录、查询历史冲突缓和记录、显示所有家庭冲突缓和报告、显示家庭情绪关怀日志，查询家庭冲突清单 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_family_conflict_aftercare_suggest_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_family_conflict_aftercare_suggest_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备家庭客厅/厨房/餐厅固定摄像头（含麦克风）音视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 获取 open-id（强制执行） | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行夫妻/家人冲突后情绪缓和提示 | 调用 `-m scripts.smyx_family_conflict_aftercare_suggest_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地家庭客厅/厨房/餐厅固定摄像头（含麦克风）音视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络家庭客厅/厨房/餐厅固定摄像头（含麦克风）音视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，家庭情绪缓和场景默认 `other` | 按需填写 |
| `--list` | 显示夫妻/家人冲突后情绪缓和提示历史事件清单（可以输入起始日期参数过滤数据范围） | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_family_conflict_aftercare_suggest_analysis.py`](scripts/smyx_family_conflict_aftercare_suggest_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov + 音轨，最大 10MB；**关键**：必须含麦克风 |
| 🔎 使用提醒 | **冲突中绝不介入**：`intense_conflict` 期间播放音乐或语音会激化情绪；**必须等待平静窗口** |
| 📁 格式支持 | 与正常高分贝场景区分：聚会、大笑、儿童欢闹、看球赛——支持家庭主用户**整日关闭** |
| 🔎 使用提醒 | 红线约束 |
| 🔎 使用提醒 | **禁止**部署在卧室、卫生间、儿童独立房间 |
| 🔎 使用提醒 | **禁止**录制并长期存储家庭对话原始音频（仅保留指标 + ≤ 24h 事件片段） |
| 🔎 使用提醒 | **禁止**做"婚姻/亲子关系评分"或"性格分析" |
| 🔎 使用提醒 | **禁止**对疑似肢体暴力进行"缓和处理"——必须独立走**安全风险**路径 |
| 🔎 使用提醒 | **禁止**将冲突事件转发给除家庭主用户外的第三方 |
| 🔎 使用提醒 | **必须**：缓和动作前 3 秒柔和铃声前导避免突然出声二次惊吓；缓和文案**中立、不指责任何一方**；同一事件单日触发**上限 2 次** |
| 🔎 使用提醒 | **必须**在 `critical_redline` 触发时**立即**推送 **12338** 反家暴热线 + **110** 报警提示；有未成年人在场优先级最高 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史事件清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地家庭公共区域音视频
python -m scripts.smyx_family_conflict_aftercare_suggest_analysis --input /path/to/livingroom.mp4

# 分析网络家庭公共区域音视频/实时流
python -m scripts.smyx_family_conflict_aftercare_suggest_analysis --url https://example.com/livingroom.mp4

# 显示历史家庭冲突缓和事件清单（自动触发关键词：查看家庭冲突缓和历史报告、家庭情绪事件清单等）
python -m scripts.smyx_family_conflict_aftercare_suggest_analysis --list

# 输出精简报告
python -m scripts.smyx_family_conflict_aftercare_suggest_analysis --input lr.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_family_conflict_aftercare_suggest_analysis --input lr.mp4 --output result.json
```
