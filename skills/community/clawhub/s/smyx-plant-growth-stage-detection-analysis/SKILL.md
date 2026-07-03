---
name: "smyx-plant-growth-stage-detection-analysis"
description: "AI-powered plant growth stage auto-detection from periodic full-plant images via smart pot / greenhouse fixed cameras. Recognizes key phenological features—cotyledon emergence, true-leaf count, flower bud differentiation, blooming, fruit setting, fruit ripening—and identifies the current developmental stage (germination, seedling, vegetative, flowering, fruiting, ripening), enabling precision irrigation/fertilization/lighting control and personalized growing guidance. Scenarios: smart pots, home grow boxes, greenhouses, plant factories. | 通过智能花盆或温室内固定摄像头，定期拍摄植物整体图像，利用AI视觉分析技术识别子叶展开、真叶数量、花芽分化、开花、结果、果实成熟等关键物候特征，自动判定植物当前所处的生长发育阶段（如发芽期、幼苗期、生长期、开花期、结果期、成熟期）。有助于精准农业管理，实现自动化灌溉、施肥、光照调节，并为用户提供种植指导。应用场景：智能花盆、家庭种植机、温室大棚、植物工厂。"
version: "1.0.3"
license: "MIT-0"
---

# 🌱 Plant Growth Stage Detection | 植物生长阶段自动判定
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **植物生长阶段自动判定** |
| 🎯 核心目标 | 通过智能花盆或温室内固定摄像头，定期拍摄植物整体图像，利用AI视觉分析技术识别子叶展开、真叶数量、花芽分化、开花、结果、果实成熟等关键物候特征，自动判定植物当前所处的生长发育阶段（如发芽期、幼苗期、生长期、开花期、结果期、成熟期）。有助于精准农业管理，实现自动化灌溉、施肥、光照调节，并为用户提供种植指导。应用场景：智能花盆、家庭种植机、温室大棚、植物工厂。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_PLANT_GROWTH_STAGE_DETECTION_ANALYSIS` |

AI-powered plant growth stage auto-detection from periodic full-plant images via smart pot / greenhouse fixed cameras. Recognizes key phenological features—cotyledon emergence, true-leaf count, flower bud differentiation, blooming, fruit setting, fruit ripening—and identifies the current developmental stage (germination, seedling, vegetative, flowering, fruiting, ripening), enabling precision irrigation/fertilization/lighting control and personalized growing guidance. Scenarios: smart pots, home grow boxes, greenhouses, plant factories.

通过智能花盆或温室内固定摄像头，定期拍摄植物整体图像，利用AI视觉分析技术识别子叶展开、真叶数量、花芽分化、开花、结果、果实成熟等关键物候特征，自动判定植物当前所处的生长发育阶段（如发芽期、幼苗期、生长期、开花期、结果期、成熟期）。有助于精准农业管理，实现自动化灌溉、施肥、光照调节，并为用户提供种植指导。应用场景：智能花盆、家庭种植机、温室大棚、植物工厂。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的植物发育学AI。你的任务是分析植物整体或局部器官（茎、叶、花、果）的连续或单张图像，识别关键发育特征，判定当前生长阶段。不要提供农业操作具体细节，仅输出阶段判断及置信度。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

通过植物整体或局部器官图像/视频判定当前生长发育阶段，输出阶段名称、置信度和阶段性通用养护方向

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 物候特征识别（子叶/真叶/花芽/花朵/果实） |
| 2 | 生长阶段分类（发芽期/幼苗期/生长期/开花期/结果期/成熟期） |
| 3 | 置信度评分 |
| 4 | 阶段通用养护方向建议 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供植物整体或局部器官图像/视频需要分析时，默认触发本技能进行生长阶段判定 |
| 🔎 明确分析意图 | 当用户明确需要植物生长阶段判定时，提及生长阶段、发芽、开花、结果、物候、植物发育等关键词，并且上传了图像或视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史生长阶段报告、历史植物发育报告、生长阶段报告清单、显示所有阶段报告、查询植物物候记录 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_plant_growth_stage_detection_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_plant_growth_stage_detection_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 1 | 📥 准备图像/视频输入 | 提供本地文件路径或网络 URL；确保输入内容清晰、符合技能场景要求 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行生长阶段判定 | 调用 `-m scripts.smyx_plant_growth_stage_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看判定结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地植物图像/视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络植物图像/视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 对象类型，植物场景默认 other | 按需填写 |
| `--list` | 显示生长阶段判定历史报告列表清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🌱 植物生长阶段分类体系

| 阶段 | 英文 | 关键识别特征 | 典型时长 |
|------|------|--------------|----------|
| 🌰 发芽期 | Germination | 种子萌发、子叶展开 | 3-14 天 |
| 🌿 幼苗期 | Seedling | 子叶→真叶转换、1-3片真叶 | 1-4 周 |
| 📈 生长期 | Vegetative | 真叶数量增加、茎干拔高、枝叶茂盛 | 数周-数月 |
| 🌸 开花期 | Flowering | 花芽分化、花苞形成、花朵开放 | 1-8 周 |
| 🍅 结果期 | Fruiting | 花后坐果、幼果膨大 | 数周-数月 |
| 🍎 成熟期 | Ripening | 果实转色、糖度上升、可采收 | 1-4 周 |

## 🔍 关键物候特征识别对照

| 物候特征 | 视觉表现 | 标志性阶段转换 |
|----------|----------|----------------|
| 子叶展开 | 两片对称小叶从种壳中展开 | 发芽期 → 幼苗期 |
| 第一真叶 | 子叶上方出现不同于子叶形态的真叶 | 进入幼苗期 |
| 叶片数量激增 | 真叶快速增长、茎节伸长 | 幼苗期 → 生长期 |
| 花芽分化 | 叶腋或顶端出现膨大的花芽 | 生长期 → 开花期 |
| 花朵开放 | 花苞绽放，花瓣可见 | 开花期标志 |
| 幼果坐果 | 花后子房膨大形成幼果 | 开花期 → 结果期 |
| 果实膨大 | 果实体积增大、形状渐趋完满 | 结果期进行中 |
| 果实转色 | 由绿转红/黄/橙等成熟色 | 结果期 → 成熟期 |

## 📊 置信度说明

| 置信度区间 | 可靠性 | 说明 |
|------------|--------|------|
| 80%-100% | 🟢 高 | 特征明确，阶段判定可靠 |
| 60%-79% | 🟡 中 | 部分特征可见，建议补充更多图像 |
| <60% | 🟠 低 | 特征模糊，可能处于阶段过渡期，建议隔天再次拍摄 |

## 💡 各阶段通用养护方向参考

| 阶段 | 水分 | 养分重点 | 光照 | 特殊提示 |
|------|------|----------|------|----------|
| 🌰 发芽期 | 保持湿润 | 无需施肥 | 弱光散射光 | 覆膜保湿 |
| 🌿 幼苗期 | 适度浇水 | 稀薄氮肥 | 逐步增加光照 | 防止徒长 |
| 📈 生长期 | 充足浇水 | 氮肥为主，适量磷钾 | 充足日照 | 番茄等需搭架 |
| 🌸 开花期 | 适度控水 | 磷钾肥为主 | 充足日照 | 建议人工辅助授粉 |
| 🍅 结果期 | 均匀浇水 | 钾肥为主 | 充足日照 | 避免水分剧烈波动 |
| 🍎 成熟期 | 减少浇水 | 停止施肥 | 保持光照 | 适时采收 |

> ⚠️ 以上仅为通用方向参考，**不构成具体农业操作方案**；具体施肥/灌溉需根据植物种类、环境条件调整。

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_plant_growth_stage_detection_analysis.py`](scripts/smyx_plant_growth_stage_detection_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持 jpg/png/mp4/avi/mov 格式，最大 10MB |
| 🔎 使用提醒 | **拍摄建议**：整体 + 关键器官近景；固定角度定期拍摄便于对比 |
| 🧑‍⚖️ 结果性质 | **判定结果仅供生长阶段参考，不提供农业操作具体细节** |
| 🔎 使用提醒 | 不同植物物候周期差异大，判定需结合植物种类信息 |
| 🔎 使用提醒 | 阶段过渡期（如开花初期）特征可能不明确，置信度会偏低 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载 |
| 📜 报告输出 | 当显示历史判定报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地植物图像
python -m scripts.smyx_plant_growth_stage_detection_analysis --input /path/to/plant.jpg

# 分析网络植物图像
python -m scripts.smyx_plant_growth_stage_detection_analysis --url https://example.com/plant.jpg

# 显示历史判定报告/显示报告清单列表
python -m scripts.smyx_plant_growth_stage_detection_analysis --list

# 输出精简报告
python -m scripts.smyx_plant_growth_stage_detection_analysis --input plant.jpg --detail basic

# 保存结果到文件
python -m scripts.smyx_plant_growth_stage_detection_analysis --input plant.jpg --output result.json
```
