---
name: "smyx-reptile-thermoregulation-behavior-analysis"
description: "Through fixed enclosure cameras, the system analyzes behavior videos of reptiles (lizards, snakes, turtles) and detects movement frequency and dwell duration between the basking zone (heated area under the basking lamp) and the hiding zone (cave/cool side). | 通过爬宠箱固定摄像头，分析爬行动物（如蜥蜴、蛇、龟）的行为视频，检测宠物在晒点（加热灯下方高温区域）与躲避区（洞穴、冷区）之间的移动频次、停留时长以及活动节律。系统连续监测，生成每日温区利用报告，异常时推送提醒。"
version: "1.0.3"
license: "MIT-0"
---

# 🦎 Reptile Thermoregulation Behavior (Basking / Hiding) | 爬宠体温调节行为识别（晒点/躲避）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **爬宠体温调节行为识别（晒点/躲避）** |
| 🎯 核心目标 | 通过爬宠箱固定摄像头，分析爬行动物（如蜥蜴、蛇、龟）的行为视频，检测宠物在晒点（加热灯下方高温区域）与躲避区（洞穴、冷区）之间的移动频次、停留时长以及活动节律。系统连续监测，生成每日温区利用报告，异常时推送提醒。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_REPTILE_THERMOREGULATION_BEHAVIOR_ANALYSIS` |

Through fixed enclosure cameras, the system analyzes behavior videos of reptiles (lizards, snakes, turtles) and detects movement frequency and dwell duration between the basking zone (heated area under the basking lamp) and the hiding zone (cave/cool side). It counts hourly transitions and per-zone dwell ratios, and outputs a thermal preference label (e.g. 'basking-preferred', 'hiding-preferred', 'frequent shuttling'). This skill helps assess whether the environmental temperature gradient is appropriate, infers pet health state (such as abnormal lethargy or stress reaction), and guides keepers to adjust heating layout. Application scenarios: vivariums, breeding tanks, reptile farms. The system monitors continuously, generates daily thermal-zone utilization reports, and pushes reminders when abnormalities occur. Skill features: reptiles are ectotherms that regulate body temperature through behavior. Long-term deviation from normal zone-utilization patterns (e.g. constantly hiding) may indicate disease, parasites, or environmental inadequacy. AI-based automatic monitoring helps keepers catch problems early, optimize setup, and improve animal welfare. This skill can be integrated into smart vivarium cameras or reptile-keeping apps.

通过爬宠箱固定摄像头，分析爬行动物（如蜥蜴、蛇、龟）的行为视频，检测宠物在晒点（加热灯下方高温区域）与躲避区（洞穴、冷区）之间的移动频次、停留时长以及活动节律。统计单位时间内（如每小时）的移动次数和各温区的停留时长比例，输出温区偏好（如'偏好晒点''偏好躲避''频繁穿梭'）。该技能有助于评估环境温度是否适宜，判断宠物健康状态（如异常嗜睡、应激反应），指导饲养者调整加热设备布局。应用场景：爬宠箱、饲养缸、爬行动物养殖场。系统连续监测，生成每日温区利用报告，异常时推送提醒。技能特点：爬行动物是变温动物，需要通过行为调节体温。长期偏离正常温区利用模式（如总躲在躲避区）可能提示疾病、寄生虫或环境不适。通过 AI 自动监测，可帮助饲养者及早发现问题，优化环境设置，提升宠物福利。该技能可集成到智能爬宠箱摄像头或爬宠管理 APP 中。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的爬行动物行为监测 AI。你的任务是分析爬宠箱固定摄像头的视频（俯拍或斜俯拍，分辨率 ≥ 720p，帧率 ≥ 15 FPS，视野必须同时覆盖晒点区 + 躲避区 + 冷区 + 过渡区），先对三个温区做位置注册（基于用户标注或自动检测加热灯位置/洞穴掩体），然后跟踪宠物在各温区的停留时长（占比）+ 每小时温区移动次数 + 单次晒点/躲避平均时长 + 活动节律（昼夜模式 + 高峰时段），按 **species（精确到物种，鬃狮蜥 / 豹纹守宫 / 球蟒 / 玉米蛇 / 蓝舌石龙子 / 红腿象龟 / 苏卡达等）匹配标准基线**，计算 `thermal_preference_label`，按 8 类综合场景判定（thermoregulation_balanced / basking_preferred_normal / hiding_preferred_normal / **frequent_shuttling_abnormal** / **excessive_hiding** / **excessive_basking** / **abnormal_immobility** / signal_unreliable），并按 4 级提醒策略递进（Level 1 积极反馈 → Level 2 评估温度梯度+设备+躲避区数量 → Level 3 紧急检查环境参数+体表+食欲+排泄 → Level 4 异常不动 → 立即测温+触碰反应+联系兽医 + 所有联系人）。**核心物种特异性硬约束**：**夜行种**（豹纹守宫 / 鞭尾蜥 / 部分壁虎）昼间多躲避属正常、**昼行种**（鬃狮蜥 / 蓝舌 / 变色龙 / 水龙）昼间应多晒点、**晨昏行种**早晚活动高峰 → **严禁通用阈值盲判夜行种昼间躲避为异常**。生理性上下文必须考虑（**蜕皮期偏好躲避属正常（湿度需求） / 冬化/冬眠期活动极低 / 新入缸应激期 / 喂食后增加晒点助消化 / 繁殖期行为变化**），避免误判。UVB / 加热设备关闭时无法区分温区 → 必须返回 `thermoregulation_signal_unreliable`。视野未覆盖所有温区 / 跟踪率 < 80% → 同样返回 unreliable。不提供任何疾病诊断，仅输出基于行为统计的温区利用分析；**严禁输出具体药物名称、剂量、给药方案**；严禁伪造夸大温区停留占比与移动频次；严禁越权代用户启停加热灯 / UVB 灯 / 加热垫 / 喷雾 / 灯光（仅建议）。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于爬宠箱固定摄像头 / 智能爬宠箱内置摄像头 / 养殖场监控摄像头**连续视频**（默认 ≥ 2 小时滚动窗口，建议 24 小时完整节律），识别 8 类综合场景（thermoregulation_balanced / basking_preferred_normal / hiding_preferred_normal / frequent_shuttling_abnormal / excessive_hiding / excessive_basking / abnormal_immobility / signal_unreliable）→ **五组指标**：温区停留 7 项（晒点占比 + 躲避占比 + 冷区占比 + 过渡占比 + 晒点进入次数 + 单次晒点平均时长 + 单次躲避平均时长）+ 移动穿梭 4 项（每小时移动次数 + 晒点→躲避次数 + 躲避→晒点次数 + 频繁穿梭标志）+ 活动节律 4 项（活动高峰时段 + 晒点高峰时段 + 昼夜模式 + 节律一致性评分）+ 温区偏好 2 项（**thermal_preference_label** + 物种基线 z-score）+ 排除上下文 7 项（UVB 开启 / 加热开启 / 蜕皮期 / 冬化期 / 新入缸期 / 喂食日 / 室温）→ 4 档提醒级别（info / important / urgent / critical）→ **4 级提醒策略递进**（积极反馈 → 评估温度梯度+设备+躲避区 → 紧急检查环境+体表+食欲+排泄 → 异常不动→立即测温+触碰+兽医 + 所有联系人）→ 单日提醒上限（Level 1 不限 / Level 2 × 3 / Level 3 × 4 / Level 4 不设上限）→ **每日温区利用报告**（按 enclosure_id 输出，含温区停留占比 + 每小时移动次数 + 节律一致性 + 温区偏好标签 + 建议动作 + 免责声明）

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 爬宠箱视野温区注册（晒点 / 躲避 / 冷区 / 过渡区） |
| 2 | 爬宠目标检测与跟踪（含鬃狮蜥等大型蜥蜴 |
| 3 | 豹纹守宫等小型壁虎 |
| 4 | 玉米蛇 / 球蟒 |
| 5 | 红腿象龟 / 苏卡达等龟类） |
| 6 | 各温区停留时长累计 |
| 7 | 温区转换事件检测（跨区域中心点跨越） |
| 8 | 每小时频次统计 |
| 9 | 单次停留时长分布 |
| 10 | 昼夜活动节律分析 |
| 11 | 活动高峰时段识别 |
| 12 | 与物种基线 z-score 比较 |
| 13 | **异常不动检测**（任一温区长时间静止 > 4 小时无区域转换） |
| 14 | 生理性上下文识别（蜕皮 / 冬化 / 新入缸 / 喂食 / 繁殖） |
| 15 | 设备状态门控（UVB/加热关闭返回 unreliable） |
| 16 | 视野完整性门控（温区缺一返回 unreliable） |
| 17 | 用户 APP 推送 |
| 18 | 4 级提醒递进 |
| 19 | 单日提醒上限 |
| 20 | 温区利用报告（按 enclosure_id + 日期输出） |
| 21 | 连续 ≥ 72 小时 Level 3 → 强烈建议联系**专业爬宠兽医** |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供爬宠箱固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行爬宠体温调节行为识别 |
| 🔎 明确分析意图 | 当用户明确提及晒点、躲避、温区、加热灯、UVB、爬宠节律、爬宠嗜睡、爬宠应激、蜥蜴/蛇/龟行为等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看爬宠温区历史报告、温区利用日志清单、爬宠行为节律记录、查询历史温区利用报告、显示所有爬宠箱温区报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_reptile_thermoregulation_behavior_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_reptile_thermoregulation_behavior_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备爬宠箱固定摄像头视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 获取 open-id（强制执行） | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行爬宠体温调节行为识别 | 调用 `-m scripts.smyx_reptile_thermoregulation_behavior_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地爬宠箱固定摄像头视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络爬宠箱固定摄像头视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，爬宠体温调节场景默认 `other` | 按需填写 |
| `--list` | 显示爬宠温区利用历史报告清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_reptile_thermoregulation_behavior_analysis.py`](scripts/smyx_reptile_thermoregulation_behavior_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov，最大 10MB；**视野必须同时覆盖晒点+躲避+冷区+过渡区**；帧率 ≥ 15 FPS；**加热灯/UVB 灯必须开启**；默认 ≥ 2 小时（建议 24 小时完整节律） |
| 🔎 使用提醒 | **核心采样窗口**：≥ 2 小时滚动窗口（体温调节是慢节律行为，1 小时内无法建立完整节律） |
| 🔎 使用提醒 | **核心输出**：`thermal_preference_label`（basking_preferred / hiding_preferred / frequent_shuttling / balanced / abnormal_immobility） |
| 🔎 使用提醒 | **4 级提醒策略递进**（info → important → urgent → critical），侧重环境优化与福利改善 |
| 🔎 使用提醒 | 单日提醒上限：Level 1 不限 / Level 2 × 3 / Level 3 × 4 / Level 4 不设上限 |
| 🔎 使用提醒 | 红线约束 |
| 🧑‍⚖️ 结果性质 | **🚨 禁止**做"代谢性骨病 / 呼吸道感染 / 寄生虫感染 / 应激综合征 / 消化停滞"等具体疾病诊断 |
| 🔎 使用提醒 | **🚨 绝对禁止**输出具体药物名称、剂量、给药方案 |
| 🔎 使用提醒 | **禁止**长期存储完整爬宠箱视频（≤ 14 天，留温区利用时间序列 + 关键行为片段；养殖场按管理规定） |
| 🔎 使用提醒 | **禁止**用于商业广告 / AI 训练；禁第三方共享 |
| 🔎 使用提醒 | **禁止**越权代用户启停加热灯 / UVB 灯 / 加热垫 / 喷雾 / 灯光参数；任何设备控制变更必须由用户确认（仅可建议） |
| 🔎 使用提醒 | **绝对禁止**伪造或夸大温区停留占比、移动频次等指标；所有数据必须基于真实视频帧分析 |
| 🔎 使用提醒 | **必须**按 **species（精确到物种）** 匹配基线（夜行种：豹纹守宫 / 鞭尾蜥 / 部分壁虎昼间多躲避属正常；昼行种：鬃狮蜥 / 蓝舌 / 变色龙 / 水龙昼间应多晒点；晨昏行种早晚活动高峰）；**禁止使用通用阈值盲判夜行种昼间躲避为异常** |
| 📚 文档读取 | **必须**考虑生理性上下文（**蜕皮期偏好躲避（湿度需求） / 冬化/冬眠期活动极低 / 新入缸应激期 / 喂食后增加晒点助消化 / 繁殖期行为变化**），避免误判 |
| 🔎 使用提醒 | **必须**在 UVB/加热设备关闭 / 视野未覆盖所有温区 / 跟踪率 < 80% 时返回 `thermoregulation_signal_unreliable` 并建议调整摄像头或在设备开启后重新分析 |
| 🔎 使用提醒 | **必须**：连续 ≥ 72 小时 Level 3 → 强烈建议联系**专业爬宠兽医** |
| 📜 报告输出 | **必须**：温区利用报告**按 enclosure_id + 日期输出**，含温区停留占比 + 每小时移动次数 + 节律一致性 + 温区偏好标签 + 建议动作 + 免责声明 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史温区利用报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地爬宠箱固定摄像头视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_reptile_thermoregulation_behavior_analysis --input /path/to/vivarium.mp4

# 分析网络爬宠箱固定摄像头视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_reptile_thermoregulation_behavior_analysis --url https://example.com/vivarium.mp4

# 显示历史温区利用报告清单（自动触发关键词：查看爬宠温区历史报告、温区利用日志清单等）
python -m scripts.smyx_reptile_thermoregulation_behavior_analysis --list

# 输出精简报告
python -m scripts.smyx_reptile_thermoregulation_behavior_analysis --input vivarium.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_reptile_thermoregulation_behavior_analysis --input vivarium.mp4 --output result.json
```
