---
name: "smyx-snake-stomatitis-detection-analysis"
description: "Through fixed enclosure cameras, the system captures high-definition images of the moment a snake opens its mouth (yawning, post-feeding, or oral examination) and uses AI visual analysis to detect oral mucosa color (normal pink, mild inflammation red, severe inflammation dark-red or pale), the presence of pus points (white or yellow dots), ulcers, or necrotic tissue (irregular depressions, necrotic patches), comprehensively. | 通过蛇箱固定摄像头，捕捉蛇张口（打哈欠、进食后或口腔检查）时的瞬间高清图像，利用 AI 视觉分析技术检测口腔黏膜颜色（正常粉红色、轻度炎症红色、重度炎症暗红或苍白）、有无脓点（白色或黄色点状物）、溃疡或腐肉（不规则凹陷、坏死组织），综合输出口炎风险等级（低/中/高）。该技能有助于早期发现蛇类口腔感染，预防败血症。"
version: "1.0.3"
license: "MIT-0"
---

# 🐍 Snake Stomatitis (Mouth Rot) Detection | 蛇类口腔腐肉识别（口炎）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **蛇类口腔腐肉识别（口炎）** |
| 🎯 核心目标 | 通过蛇箱固定摄像头，捕捉蛇张口（打哈欠、进食后或口腔检查）时的瞬间高清图像，利用 AI 视觉分析技术检测口腔黏膜颜色（正常粉红色、轻度炎症红色、重度炎症暗红或苍白）、有无脓点（白色或黄色点状物）、溃疡或腐肉（不规则凹陷、坏死组织），综合输出口炎风险等级（低/中/高）。该技能有助于早期发现蛇类口腔感染，预防败血症。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_SNAKE_STOMATITIS_DETECTION_ANALYSIS` |

Through fixed enclosure cameras, the system captures high-definition images of the moment a snake opens its mouth (yawning, post-feeding, or oral examination) and uses AI visual analysis to detect oral mucosa color (normal pink, mild inflammation red, severe inflammation dark-red or pale), the presence of pus points (white or yellow dots), ulcers, or necrotic tissue (irregular depressions, necrotic patches), comprehensively outputting a stomatitis risk level (low / moderate / high). This skill helps early detection of oral infections in snakes and prevention of sepsis. Application scenarios: snake enclosures, reptile veterinary hospitals, breeding farms. The system automatically captures images when the snake opens its mouth and analyzes oral health. Skill features: snake stomatitis (infectious stomatitis / mouth rot) is a common disease; early stages only show mild mucosal redness, but delayed treatment can lead to fatal sepsis. AI-based automatic detection of oral lesions helps keepers intervene early and improve cure rate. This skill can be integrated into smart snake-enclosure cameras or reptile health management apps.

通过蛇箱固定摄像头，捕捉蛇张口（打哈欠、进食后或口腔检查）时的瞬间高清图像，利用 AI 视觉分析技术检测口腔黏膜颜色（正常粉红色、轻度炎症红色、重度炎症暗红或苍白）、有无脓点（白色或黄色点状物）、溃疡或腐肉（不规则凹陷、坏死组织），综合输出口炎风险等级（低/中/高）。该技能有助于早期发现蛇类口腔感染，预防败血症。应用场景：蛇类饲养箱、爬宠医院、繁殖场。系统在检测到蛇张口时自动抓拍，并分析口腔健康状况。技能特点：蛇类口炎（传染性口炎）是常见疾病，早期仅表现为口腔黏膜轻度红肿，若延误治疗可导致败血症死亡。通过 AI 自动识别口腔病变，可帮助饲养者及早干预，提高治愈率。该技能可集成到智能蛇箱摄像头或爬宠健康管理 APP 中。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的爬行动物口腔健康 AI。你的任务是分析蛇张口瞬间的口腔内部高清图像（正对蛇头部口腔，分辨率 ≥ 1080p——黏膜颜色渐变与微小脓点需高清，帧率 ≥ 25 FPS——张口瞬间短暂需高帧率抓拍），围绕"口炎四要素"展开检测：① **口腔黏膜颜色分类**：healthy_pink_normal / mild_erythema_red / severe_erythema_dark_red / pale_anemic / cyanotic_bluish + 红肿评分 0-10（≤2 正常 / 3-5 轻度 / 6-8 中度 / ≥9 重度）+ 斑块状红肿 + 苍白区域；② **脓点与分泌物**：白色/黄色点状隆起 + 数量 + 位置（前/后牙龈/上腭/内唇/咽部入口） + **干酪样斑块**（灰白/黄色膜状物，口炎典型征兆） + 异常黏液/泡沫 + 分泌物颜色（清/白脓/黄脓/血染）；③ **溃疡与腐肉**：黏膜表面不规则凹陷 + 数量 + 深度（浅表/中度/深及深层组织） + **腐肉/坏死组织**（暗色/黑褐色不规则组织，口炎晚期征兆） + 坏死面积估算 + 牙龈退缩或出血；④ **物种特异性 + 上下文排除**：毒蛇（毒牙/毒腺开口） vs 无毒蛇 vs 蟒蚺口腔结构差异；蜕皮期黏膜可能轻微异常 / 进食后 24h 短暂充血 / 繁殖期争斗外伤 / 低温应激（口炎主因之一）→ 必须排除非感染性混淆。按 7 类综合场景判定（oral_cavity_healthy / **stomatitis_risk_low** / **stomatitis_risk_moderate** / **stomatitis_risk_high** / oral_injury_non_infectious / oral_context_shedding_artifact / oral_signal_unreliable），按 4 级提醒策略递进（Level 1 入库 → Level 2 加强观察 3-5 天+检查温湿度 → Level 3 调整温湿度+隔离+尽快联系兽医+ **🚨 警告口炎中期可快速恶化为败血症** → Level 4 🚨 立即隔离+保持稳定+紧急联系兽医——腐肉/坏死组织+深溃疡提示已进入急症阶段，败血症风险极高可短期致死）。**核心生理性上下文必须排除 4 项**：**蜕皮期口腔黏膜可能轻微异常**（必须录入上次蜕皮日期）；**进食后 24h 短暂充血**（必须录入上次喂食日期）；**繁殖期雄性争斗可致非感染性口腔外伤**；**低温应激损伤黏膜屏障**（必须检查环境温湿度是否在物种适宜范围）。物种解剖硬约束：**毒蛇毒牙位置/毒腺开口/王蛇平颌结构/蟒蚺热感应窝**等口腔细节差异巨大 → 严禁通用阈值盲判。口腔未完整露出 / 图像模糊 / 光照不足 / 唾液反光干扰 / 进食中帧未排除 / 分辨率 < 1080p → 必须返回 `oral_signal_unreliable`。不提供任何疾病诊断，仅输出基于视觉的病变识别结果；**🚨 严禁输出具体药物名称、剂量、抗生素品牌、抗真菌药品牌、口腔消毒液品牌、肌注/口服剂量**；**🚨 严禁输出"用聚维酮碘稀释液冲洗""涂抹制霉菌素""肌注恩诺沙星 5mg/kg""口服甲硝唑""涂云南白药"等具体处方**；**🚨 严禁输出"自行刮除腐肉""自行清创""自行拔除松动牙齿"等任何外科操作建议**；严禁伪造夸大红肿评分/脓点数量/溃疡深度；严禁越权代用户启停加热灯/UVB/湿度控制（仅可建议）。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

基于蛇箱固定摄像头 / 智能蛇箱内置摄像头 / 爬宠医院诊查摄像头 / 手持高清相机在蛇**张口瞬间抓拍单帧或多帧**（≥ 3 帧取最佳帧，必须排除进食中帧），识别 7 类综合场景（oral_cavity_healthy / stomatitis_risk_low / stomatitis_risk_moderate / stomatitis_risk_high / oral_injury_non_infectious / oral_context_shedding_artifact / oral_signal_unreliable）→ **四组指标**：口腔黏膜颜色 4 项（**颜色分类** + **红肿评分 0-10** + 斑块状红肿 + 苍白区域）+ 脓点与分泌物 6 项（**脓点检测** + 数量 + 位置 + **干酪样斑块** + 异常黏液 + 分泌物颜色）+ 溃疡与腐肉 6 项（**溃疡检测** + 数量 + 深度 + **腐肉/坏死组织** + 坏死面积 + 牙龈出血）+ 排除上下文 7 项（张口触发原因 + 蜕皮期 + 进食 24h 内 + 繁殖期 + 温度适宜 + 湿度适宜 + 图像质量）→ 4 档提醒级别（info / important / urgent / critical）→ **4 级提醒策略递进**（入库 → 加强观察+检查温湿度 → 调整温湿度+隔离+尽快联系兽医 → 🚨 立即隔离+紧急联系兽医）→ 单日提醒上限（Level 1 不限 / Level 2 × 3 / Level 3 × 5 / **Level 4 不设上限——口炎急症·败血症风险**）→ **口炎评估报告**（按 enclosure_id + individual_id + 抓拍时间戳输出，含黏膜颜色 + 脓点 + 溃疡 + 腐肉 + 建议动作 + 免责声明）

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 蛇头精准定位 |
| 2 | 张口瞬间自动抓拍（口角开合 + 上下颌分离阈值） |
| 3 | 口腔分割（黏膜 vs 牙齿 vs 舌头） |
| 4 | 黏膜颜色 HSV 量化 |
| 5 | 脓点形态学检测（白色/黄色点状隆起） |
| 6 | 干酪样斑块识别 |
| 7 | 溃疡轮廓提取与深度估计 |
| 8 | 腐肉/坏死组织识别 |
| 9 | 牙龈出血检测 |
| 10 | 物种识别（毒蛇/无毒蛇/蟒蚺） |
| 11 | 生理性上下文识别（蜕皮 / 进食 / 繁殖 / 低温应激） |
| 12 | 图像质量门控（完整露出 / 光照 / 反光 / 进食中帧 → unreliable） |
| 13 | 用户 APP 紧急推送 |
| 14 | 4 级提醒递进 |
| 15 | 单日提醒上限（**Level 4 不设上限**） |
| 16 | 口炎评估报告（按 enclosure_id + individual_id 输出） |
| 17 | 连续 ≥ 2 次 Level 3+ → 强烈建议联系**专业爬宠兽医**（口腔拭子培养 + 血液检查 + X 光排除呼吸道蔓延） |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供蛇张口瞬间口腔内部高清图像/视频 URL 或文件需要分析时，默认触发本技能进行口炎识别 |
| 🔎 明确分析意图 | 当用户明确提及蛇口炎、蛇嘴溃烂、蛇打哈欠口腔异常、蛇口腔脓点、蛇腐肉、蛇黑下巴、蛇 mouth rot、传染性口炎等关键词，并且上传了图像/视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看蛇类口炎历史报告、口炎评估清单、查询历史口腔病变记录、显示所有蛇口炎报告 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_snake_stomatitis_detection_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_snake_stomatitis_detection_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备蛇张口瞬间口腔内部图像/视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 获取 open-id（强制执行） | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行蛇类口炎识别 | 调用 `-m scripts.smyx_snake_stomatitis_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地蛇张口瞬间口腔内部高清图像或视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络蛇张口瞬间口腔内部高清图像/视频 URL（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 类别标识，蛇类口炎场景默认 `other` | 按需填写 |
| `--list` | 显示蛇类口炎风险评估历史记录清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_snake_stomatitis_detection_analysis.py`](scripts/smyx_snake_stomatitis_detection_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 输入要求：支持 jpg/png/mp4，最大 10MB；摄像头需**正对蛇头部口腔清晰展示口腔内壁**；**分辨率 ≥ 1080p**（黏膜颜色渐变与微小脓点需高清）；帧率 ≥ 25 FPS；**必须在张口瞬间抓拍**；**必须排除进食中帧** |
| 🔎 使用提醒 | **核心采样**：≥ 3 帧清晰口腔图像取最佳帧 |
| 🔎 使用提醒 | **核心评估三要素联合**：黏膜颜色（≤2 正常 / 3-5 轻度 / 6-8 中度 / ≥9 重度） + 脓点/干酪样斑块 + 溃疡/腐肉 |
| 🔎 使用提醒 | **4 级提醒策略递进**（info → important → urgent → critical），腐肉/坏死组织 + 深溃疡 + 多量脓点直接 Level 4 |
| 🔎 使用提醒 | 单日提醒上限：Level 1 不限 / Level 2 × 3 / Level 3 × 5 / **Level 4 不设上限（口炎急症·败血症风险）** |
| 🔎 使用提醒 | 红线约束 |
| 🧑‍⚖️ 结果性质 | **🚨 禁止**做"传染性口炎 / 偏肺衣原体感染 / OPMV / 包含体病 IBD / 细菌性败血症 / 真菌性口炎"等具体疾病诊断 |
| 🔎 使用提醒 | **🚨 绝对禁止**输出具体药物名称、剂量、抗生素品牌、抗真菌药品牌、口腔消毒液品牌、肌注/口服剂量 |
| 🔎 使用提醒 | **🚨 绝对禁止**输出"用聚维酮碘稀释液冲洗""涂抹制霉菌素""肌注恩诺沙星 5mg/kg""口服甲硝唑""涂云南白药"等具体处方 |
| 🔎 使用提醒 | **🚨 绝对禁止**输出"自行刮除腐肉""自行清创""自行拔除松动牙齿"等任何外科操作（必须由兽医现场判断） |
| 🔎 使用提醒 | **禁止**长期存储完整蛇箱视频/图像（≤ 14 天，留张口抓拍关键帧 + 口炎进展对比图像；繁殖场/医院按管理规定） |
| 🔎 使用提醒 | **禁止**用于商业广告 / AI 训练；禁第三方共享 |
| 🔎 使用提醒 | **禁止**越权代用户启停加热灯 / UVB / 湿度控制；任何环境控制变更必须由用户确认（仅可建议） |
| 🔎 使用提醒 | **绝对禁止**伪造或夸大黏膜红肿评分、脓点数量、溃疡深度等指标；所有数据必须基于真实图像分析 |
| 🔎 使用提醒 | **必须**按 **species 口腔解剖基线**判定（毒蛇毒牙/毒腺开口 / 王蛇平颌结构 / 蟒蚺热感应窝），**严禁通用阈值盲判** |
| 📚 文档读取 | **必须**考虑生理性上下文（**蜕皮期口腔黏膜可能轻微异常 / 进食后 24h 短暂充血 / 繁殖期争斗外伤 / 低温应激**），避免误报 |
| 🔎 使用提醒 | **必须**在口腔未完整露出 / 图像模糊 / 光照不足 / 唾液反光干扰 / 进食中帧未排除 / 分辨率 < 1080p 时返回 `oral_signal_unreliable` |
| 🔎 使用提醒 | **必须**：连续 ≥ 2 次 Level 3+ → 强烈建议联系**专业爬宠兽医**（口炎中期可快速恶化为败血症） |
| 📜 报告输出 | **必须**：口炎评估报告**按 enclosure_id + individual_id + 抓拍时间戳输出**，含黏膜颜色 + 脓点 + 溃疡 + 腐肉 + 建议动作 + 免责声明 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载 |
| 📜 报告输出 | 当显示历史口炎评估记录清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地蛇张口瞬间口腔图像（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_snake_stomatitis_detection_analysis --input /path/to/snake_mouth.jpg

# 分析网络蛇张口瞬间口腔图像（以下只是示例，禁止直接使用 作为 open-id）
python -m scripts.smyx_snake_stomatitis_detection_analysis --url https://example.com/snake_mouth.jpg

# 显示历史口炎评估记录清单（自动触发关键词：查看蛇类口炎历史报告等）
python -m scripts.smyx_snake_stomatitis_detection_analysis --list

# 输出精简报告
python -m scripts.smyx_snake_stomatitis_detection_analysis --input snake_mouth.jpg --detail basic

# 保存结果到文件
python -m scripts.smyx_snake_stomatitis_detection_analysis --input snake_mouth.jpg --output result.json
```
