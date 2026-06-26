---
name: "smyx-fish-gasping-ammonia-warning-analysis"
description: "Through fixed aquarium cameras, the system analyzes fish behavior near the water surface, detecting repeated mouth-out-of-water (gasping), rapid mouth opening/closing (fast respiration) and exaggerated operculum (gill cover) movement — classic symptoms of hypoxia or poisoning. | 通过鱼缸固定摄像头，分析鱼类在水面附近的行为，检测鱼嘴反复探出水面（浮头）、张口快速开合（类似喘气）、鳃盖运动加剧等缺氧或中毒典型症状。当多条鱼同时出现上述行为且持续时间超过设定阈值（默认 60 秒）时，输出'氨氮中毒或缺氧风险预警'，提醒用户立即检测水质、换水或增氧。"
version: "1.0.2"
license: "MIT-0"
---

# ⚠️ Fish Gasping & Ammonia Poisoning Visual Warning | 水族箱内氨氮中毒视觉预兆（鱼浮头）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **水族箱内氨氮中毒视觉预兆（鱼浮头）** |
| 🎯 核心目标 | 通过鱼缸固定摄像头，分析鱼类在水面附近的行为，检测鱼嘴反复探出水面（浮头）、张口快速开合（类似喘气）、鳃盖运动加剧等缺氧或中毒典型症状。当多条鱼同时出现上述行为且持续时间超过设定阈值（默认 60 秒）时，输出'氨氮中毒或缺氧风险预警'，提醒用户立即检测水质、换水或增氧。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_FISH_GASPING_AMMONIA_WARNING_ANALYSIS` |

Through fixed aquarium cameras, the system analyzes fish behavior near the water surface, detecting repeated mouth-out-of-water (gasping), rapid mouth opening/closing (fast respiration) and exaggerated operculum (gill cover) movement — classic symptoms of hypoxia or poisoning. When multiple fish exhibit the above behavior simultaneously and the duration exceeds a configurable threshold (default 60 seconds), the system outputs an 'ammonia poisoning or hypoxia risk warning', prompting the user to immediately test water quality, perform water change, or increase aeration. This skill helps take emergency action BEFORE fish die. Application scenarios: home aquariums, public aquariums, aquaculture ponds. The system monitors in real time and pushes alerts the moment fish gasping is detected. Skill features: ammonia poisoning is a common acute emergency in aquariums — by the time it is noticed, fish deaths may have already occurred. AI-based automatic recognition of gasping and abnormal respiration provides emergency warning at the earliest stage, buying time to handle the situation and reduce losses. This skill can be integrated into smart aquarium cameras or aquatic safety monitoring systems.

通过鱼缸固定摄像头，分析鱼类在水面附近的行为，检测鱼嘴反复探出水面（浮头）、张口快速开合（类似喘气）、鳃盖运动加剧等缺氧或中毒典型症状。当多条鱼同时出现上述行为且持续时间超过设定阈值（默认 60 秒）时，输出'氨氮中毒或缺氧风险预警'，提醒用户立即检测水质、换水或增氧。该技能有助于在鱼只死亡前采取紧急措施。应用场景：家庭鱼缸、水族馆、养殖池。系统实时监测，一旦发现鱼浮头立即推送警报。技能特点：氨氮中毒是鱼缸常见急症，往往在检测到前已造成鱼只死亡。通过 AI 自动识别鱼浮头和异常呼吸，可在事发初期紧急提醒，为处理争取时间，减少损失。该技能可集成到智能鱼缸摄像头或水族安防系统中。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的水族水质安全 AI。你的任务是分析鱼缸固定摄像头的视频（覆盖水面带 + 水中段，分辨率 ≥ 720p，帧率 ≥ 25 FPS），检测鱼类在水面附近的三大异常行为：① **鱼嘴反复探出水面**（头部冲出水面后缩回） ② **口部快速开合**（频率 > 2 次/秒） ③ **鳃盖开合幅度增大**（体长归一化）。当**多条鱼（至少 2 条）同时出现这些行为且持续时间超过 60 秒**（用户可配置 30-300 秒）时，输出**氨氮中毒或缺氧风险预警**。按 7 类综合场景判定（surface_behavior_normal / single_fish_surface_breathing_short / single_fish_gasping_persistent / multi_fish_gasping_moderate / multi_fish_gasping_severe / whole_tank_gasping_emergency / signal_unreliable），按 4 级告警策略递进（Level 1 不提示 → Level 2 单鱼观察评估隔离 → Level 3 紧急检测水质 NH3/NO2-/DO/pH + 增氧 + 准备换水 → Level 4 **🚨 最高紧急 + 所有联系人** + 立即增氧 + 换 1/3-1/2 水（**温度 pH 匹配，禁冷水直冲**）+ 立即测氨氮 + 检查滤材/硝化系统 + **联系兽医**）。鱼种特异性必须按基线判定：**气呼吸鱼种**（斗鱼 / 攀鲈 / 部分鳉鱼科 / 蛇头鱼）天然偶尔到水面换气、**水面摄食型**（孔雀鱼 / 鳉鱼科）天然偏好水面 → **严禁通用阈值盲判气呼吸鱼种为浮头**。必须考虑生理性上下文（投喂窗口聚拢水面抢食 / 强水流 / 水温过高 / 鱼苗自然集群水面），避免误报。水面波纹过大 / 水草浮于水面遮挡 / 跟踪率 < 80% 时必须返回 `gasping_signal_unreliable` 并建议调整摄像头，**严禁给出不可靠预警**。**🚨 严禁做"氨氮中毒确诊 / 亚硝酸盐中毒确诊 / 鳃病确诊"等具体疾病诊断**（仅可输出"视觉预兆/风险预警"语义）；**严禁输出具体药物名称、剂量、给药方案**（包括硝化菌液具体品牌、解氨剂、亚甲基蓝等任何药剂）；严禁伪造夸大浮头条数 / 口开合频率 / 鳃盖幅度；严禁越权代用户启停增氧泵/加热棒/换水/喂食器/灯光等（仅建议）。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于鱼缸固定摄像头 / 水族馆侧面观察摄像头 / 养殖池水面摄像头**实时视频**（默认 60 秒滚动窗口，用户可配置 30-300 秒），识别 7 类综合场景（surface_behavior_normal / single_fish_surface_breathing_short / single_fish_gasping_persistent / multi_fish_gasping_moderate / multi_fish_gasping_severe / whole_tank_gasping_emergency / gasping_signal_unreliable）→ **四组指标**：浮头行为 4 项（水面带鱼数 / 嘴穿出水面鱼数 / 浮头比例 / 每分钟浮头事件数）+ 呼吸异常 4 项（口开合 Hz / 口张幅度 / 鳃盖幅度 / 鳃盖呼吸 BPM）+ 群体异常 4 项（注册总鱼数 / 同时浮头鱼数 / 持续时长秒 / 氧气泵是否运行）+ 排除上下文 5 项（气呼吸鱼种 / 投喂期 / 水面摄食鱼种 / 水面扰动 / 水草浮面）→ 4 档告警级别（none → important → urgent → critical）→ **4 级告警策略递进**（不提示 → 单鱼观察评估隔离 → 紧急测水质+增氧+准备换水 → 🚨 最高紧急+所有联系人+立即换水（温度 pH 匹配）+测氨氮+检查滤材+联系兽医）→ 单日告警上限（Level 1 不限 / Level 2 × 4 / Level 3 × 6 / Level 4 **不设上限**）→ **预警报告**（按 tank_id 输出，含浮头鱼条数/持续时长/口开合频率/鳃盖幅度 + 建议动作 + 免责声明）

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 鱼缸水面带分割 |
| 2 | 鱼体目标检测 + 多目标跟踪 |
| 3 | **水面穿透事件检测**（鱼头穿出水面/缩回的关键事件帧） |
| 4 | 口部关键点检测 + 开合频率估计（FFT/峰值法） |
| 5 | 鳃盖开合幅度估计（体长归一化） |
| 6 | 多鱼并发计数与持续时长累计（跨帧累积） |
| 7 | 鱼种自适应基线（气呼吸 / 水面摄食 / 中下层 / 底栖） |
| 8 | 生理性上下文识别（投喂期 / 水流 / 水温 / 鱼苗） |
| 9 | 波纹/水草遮挡门控（跟踪率 < 80% 返回 unreliable） |
| 10 | 用户 APP 紧急推送 |
| 11 | 4 级告警递进 |
| 12 | 单日告警上限（**Level 4 不设上限**） |
| 13 | 预警报告（按 tank_id + 事件时间戳输出） |
| 14 | 连续 ≥ 2 次 Level 3+ → 强烈建议联系**当地观赏鱼兽医或水产技术员** |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供鱼缸固定摄像头视频 URL 或文件需要分析时，默认触发本技能进行水族箱氨氮中毒视觉预兆识别 |
| 🔎 明确分析意图 | 当用户明确提及鱼浮头、鱼喘气、鱼集体上水面、鱼缸氨氮、鱼缸缺氧、亚硝酸盐爆表、鱼鳃异常呼吸、硝化系统崩溃等关键词，并且上传了视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看鱼缸浮头历史报告、氨氮预警日志清单、缺氧事件清单、查询历史鱼缸预警记录、显示所有水族安防预警报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_fish_gasping_ammonia_warning_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_fish_gasping_ammonia_warning_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备鱼缸固定摄像头视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 获取 open-id（强制执行） | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行水族箱氨氮中毒视觉预兆识别 | 调用 `-m scripts.smyx_fish_gasping_ammonia_warning_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地鱼缸固定摄像头视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络鱼缸固定摄像头视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，水族箱氨氮中毒视觉预兆场景默认 `other` | 按需填写 |
| `--list` | 显示水族箱氨氮中毒视觉预兆历史记录清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_fish_gasping_ammonia_warning_analysis.py`](scripts/smyx_fish_gasping_ammonia_warning_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 mp4/avi/mov，最大 10MB；摄像头需**同时覆盖水面带和水中段**；**帧率 ≥ 25 FPS**；默认 60s 滚动窗口 |
| 🔎 使用提醒 | **核心采样窗口**：60 秒滚动窗口（用户可配置 30-300 秒） |
| 🔎 使用提醒 | **核心预警门槛**：**多鱼（≥ 2 条）同时浮头持续 ≥ 60 秒** 触发 Level 3+ 告警 |
| 🔎 使用提醒 | **4 级告警策略递进**（none → important → urgent → critical），多鱼/全缸/持续超长进入更高级别 |
| 🔎 使用提醒 | 单日告警上限：Level 1 不限 / Level 2 × 4 / Level 3 × 6 / Level 4 **不设上限**（生命安全优先） |
| 🔎 使用提醒 | 红线约束 |
| 🧑‍⚖️ 结果性质 | **🚨 禁止**做"氨氮中毒确诊 / 亚硝酸盐中毒确诊 / 鳃病确诊 / 寄生虫确诊"等具体疾病诊断（仅可输出"视觉预兆/风险预警"语义） |
| 🔎 使用提醒 | **🚨 绝对禁止**输出具体药物名称、剂量、给药方案（特别**严禁推荐硝化菌液具体品牌、解氨剂、亚甲基蓝等任何药剂**） |
| 🔎 使用提醒 | **禁止**长期存储完整鱼缸视频（≤ 7 天，仅入库浮头事件片段；公共水族馆/养殖场按管理规定） |
| 🔎 使用提醒 | **禁止**用于商业广告 / AI 训练；禁第三方共享 |
| 🔎 使用提醒 | **禁止**越权代用户启停增氧泵 / 加热棒 / 换水 / 投药 / 灯光参数；**任何水族设备控制变更必须由用户确认**（仅可建议） |
| 🔎 使用提醒 | **绝对禁止**伪造或夸大浮头条数、口开合频率、鳃盖幅度、持续时长等指标；所有数据必须基于真实视频帧分析 |
| 🔎 使用提醒 | **必须**按**鱼种基线**判定：**气呼吸鱼种（斗鱼 / 攀鲈 / 部分鳉鱼科 / 蛇头鱼）天然偶尔到水面换气** + **水面摄食型（孔雀鱼 / 鳉鱼科）天然偏好水面** → 严禁通用阈值盲判 |
| 📚 文档读取 | **必须**考虑生理性上下文（投喂窗口聚拢水面抢食 / 强水流冲到水面 / 水温过高 / 鱼苗自然集群水面），避免误报 |
| 🔎 使用提醒 | **必须**在水面波纹过大 / 水草浮于水面遮挡 / 跟踪率 < 80% 时返回 `gasping_signal_unreliable` 并建议调整摄像头/清理遮挡，**禁止给出不可靠的预警** |
| 🔎 使用提醒 | **必须**在 Level 4 紧急换水建议中明确：**温度 pH 匹配，禁冷水直冲** |
| 🔎 使用提醒 | **必须**：连续 ≥ 2 次 Level 3+ → 强烈建议联系**当地观赏鱼兽医或水产技术员** |
| 📜 报告输出 | **必须**：预警报告**按 tank_id + 事件时间戳输出**，含浮头鱼条数 + 持续时长 + 口开合频率 + 鳃盖幅度 + 建议动作 + 免责声明 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史浮头预警记录清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地鱼缸固定摄像头视频（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_fish_gasping_ammonia_warning_analysis --input /path/to/tank.mp4

# 分析网络鱼缸固定摄像头视频/实时流（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_fish_gasping_ammonia_warning_analysis --url https://example.com/tank.mp4

# 显示历史浮头预警记录清单（自动触发关键词：查看鱼缸浮头历史报告、氨氮预警日志清单等）
python -m scripts.smyx_fish_gasping_ammonia_warning_analysis --list

# 输出精简报告
python -m scripts.smyx_fish_gasping_ammonia_warning_analysis --input tank.mp4 --detail basic

# 保存结果到文件
python -m scripts.smyx_fish_gasping_ammonia_warning_analysis --input tank.mp4 --output result.json
```
