---
name: "smyx-plant-wilting-quantification-analysis"
description: "AI-powered plant wilting quantification from full-plant images via smart pots or fixed cameras. Detects leaf-stem angle (leaf droop), stem straightness, and leaf turgidity to quantify wilting severity (0-100%). Optionally fuses soil-moisture sensor data to discriminate dehydration (underwatering) vs. waterlogging (root hypoxia), and auto-triggers watering or drainage prompts for precision irrigation. Scenarios: smart pots, home gardening, greenhouses, plant factories. | 通过智能花盆或固定摄像头拍摄植物整体图像，利用AI视觉分析技术检测叶片与茎秆的夹角（叶片下垂角度）、茎秆挺直程度以及叶片舒展度，量化萎蔫程度（0-100%）。可选结合土壤湿度传感器数据，综合判断萎蔫原因是缺水还是水涝（根部缺氧导致）。可自动触发灌溉或排水提示，帮助用户精准浇水。应用场景：智能花盆、家庭园艺、温室大棚、植物工厂。"
version: "1.0.2"
license: "MIT-0"
---

# 🥀 Plant Wilting Quantification (Underwatering / Overwatering) | 植物萎蔫程度量化（缺水/水多）
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **植物萎蔫程度量化（缺水/水多）** |
| 🎯 核心目标 | 通过智能花盆或固定摄像头拍摄植物整体图像，利用AI视觉分析技术检测叶片与茎秆的夹角（叶片下垂角度）、茎秆挺直程度以及叶片舒展度，量化萎蔫程度（0-100%）。可选结合土壤湿度传感器数据，综合判断萎蔫原因是缺水还是水涝（根部缺氧导致）。可自动触发灌溉或排水提示，帮助用户精准浇水。应用场景：智能花盆、家庭园艺、温室大棚、植物工厂。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_PLANT_WILTING_QUANTIFICATION_ANALYSIS` |

AI-powered plant wilting quantification from full-plant images via smart pots or fixed cameras. Detects leaf-stem angle (leaf droop), stem straightness, and leaf turgidity to quantify wilting severity (0-100%). Optionally fuses soil-moisture sensor data to discriminate dehydration (underwatering) vs. waterlogging (root hypoxia), and auto-triggers watering or drainage prompts for precision irrigation. Scenarios: smart pots, home gardening, greenhouses, plant factories.

通过智能花盆或固定摄像头拍摄植物整体图像，利用AI视觉分析技术检测叶片与茎秆的夹角（叶片下垂角度）、茎秆挺直程度以及叶片舒展度，量化萎蔫程度（0-100%）。可选结合土壤湿度传感器数据，综合判断萎蔫原因是缺水还是水涝（根部缺氧导致）。可自动触发灌溉或排水提示，帮助用户精准浇水。应用场景：智能花盆、家庭园艺、温室大棚、植物工厂。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的植物生理健康AI。你的任务是分析植物的整体图像（侧视图最佳），计算萎蔫指数（基于叶片与茎秆夹角、茎秆弯曲度等），并可结合土壤湿度数据（若提供）判断萎蔫原因（缺水或水涝）。不要提供具体浇水量，仅输出萎蔫程度和可能原因。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

通过植物整体图像量化萎蔫程度，并结合可选土壤湿度数据判断萎蔫原因，输出干预方向建议

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 叶片下垂角度检测 |
| 2 | 茎秆挺直程度评估 |
| 3 | 叶片舒展度分析 |
| 4 | 萎蔫指数综合评分（0-100%） |
| 5 | 缺水/水涝原因判别（结合可选土壤湿度） |
| 6 | 灌溉/排水方向建议 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供植物整体图像或视频需要分析时，默认触发本技能进行萎蔫量化 |
| 🔎 明确分析意图 | 当用户明确需要萎蔫监测时，提及植物萎蔫、叶子耷拉、茎秆下垂、缺水、水涝、浇水判断等关键词，并且上传了图像或视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史萎蔫报告、历史萎蔫量化报告、萎蔫报告清单、显示所有萎蔫报告、查询浇水建议记录 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_plant_wilting_quantification_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_plant_wilting_quantification_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 3 | ⚙️ 执行萎蔫量化 | 调用 `-m scripts.smyx_plant_wilting_quantification_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看量化结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地植物图像/视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络植物图像/视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 对象类型，植物场景默认 other | 按需填写 |
| `--list` | 显示萎蔫量化历史报告列表清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 📐 萎蔫指数量化指标

| 指标 | 测量方式 | 健康状态 | 轻度萎蔫 | 重度萎蔫 |
|------|----------|----------|----------|----------|
| 叶片-茎秆夹角 | 叶片与茎秆夹角 | 30°-60°（向上展开） | 60°-90°（水平） | >90°（下垂） |
| 茎秆挺直度 | 茎秆弯曲程度 | 笔直 | 轻微弯曲 | 明显弯曲/倒伏 |
| 叶片舒展度 | 叶片展开面积比 | 充分展开 | 边缘卷曲 | 严重卷缩/干枯 |

> 萎蔫指数 = f(叶片夹角, 茎秆挺直度, 叶片舒展度)，综合三项指标加权计算 0-100%。

## 📊 萎蔫程度分级

| 萎蔫指数 | 程度 | 视觉表现 | 建议 |
|----------|------|----------|------|
| 0%-15% | 🟢 健康 | 叶片挺拔舒展，茎秆笔直 | 无需干预 |
| 16%-35% | 🟡 轻度 | 叶片轻微下垂，边缘微卷 | 关注，观察 1-2 小时是否恢复 |
| 36%-60% | 🟠 中度 | 叶片明显下垂，茎秆微弯 | 需要干预，判断缺水/水涝后处理 |
| 61%-100% | 🔴 重度 | 叶片严重下垂/卷缩，茎秆弯曲倒伏 | ⚠️ 紧急处理，重度萎蔫可能不可逆 |

## 🚰 缺水 vs 水涝：关键区别

| 特征 | 缺水（干旱） | 水涝（过湿） |
|------|--------------|--------------|
| 叶片表现 | 从边缘开始干枯、卷曲、变脆 | 整体发黄、柔软、易脱落 |
| 茎秆 | 可能偏软但通常保持挺直 | 基部发软、发黑 |
| 土壤 | 干燥、开裂 | 湿润、积水、可能有异味 |
| 根系 | 根尖干枯 | 根部腐烂、发黑发臭 |
| 恢复速度 | 浇水后数小时内恢复 | 需排水+通风，恢复较慢 |
| 常见误区 | — | 看到萎蔫就浇水，可能加重水涝 |

> **关键**：水涝导致的萎蔫与缺水外观相似，但处理方式完全相反！错误浇水会加速植物死亡。

## 🔧 智能设备联动参考

| 联动设备 | 缺水场景 | 水涝场景 |
|----------|----------|----------|
| 💧 自动灌溉 | 启动浇水 | 停止浇水 |
| 🌡️ 土壤湿度传感器 | 确认土壤干燥 | 确认土壤过湿 |
| 💨 排风扇/通风 | — | 启动通风加速蒸发 |
| 🔦 补光灯 | — | 关闭（减少蒸腾） |
| 📱 APP 推送 | "缺水，请浇水" | "水涝，请停止浇水并松土" |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_plant_wilting_quantification_analysis.py`](scripts/smyx_plant_wilting_quantification_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持 jpg/png/mp4/avi/mov 格式，最大 10MB |
| 🔎 使用提醒 | **拍摄要求**：侧视图最佳，需清晰看到叶片与茎秆关系；俯视图无法准确评估下垂角度 |
| 🔎 使用提醒 | **仅输出萎蔫程度和可能原因，不提供具体浇水量** |
| 🔎 使用提醒 | 无土壤湿度数据时，缺水/水涝判断为推测，建议结合手动检查土壤确认 |
| 🔎 使用提醒 | 高温午间萎蔫为正常蒸腾萎蔫，傍晚可自行恢复，无需紧急浇水 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载 |
| 📜 报告输出 | 当显示历史量化报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地植物图像
python -m scripts.smyx_plant_wilting_quantification_analysis --input /path/to/plant_side.jpg

# 分析网络植物图像
python -m scripts.smyx_plant_wilting_quantification_analysis --url https://example.com/plant.jpg

# 显示历史量化报告/显示报告清单列表
python -m scripts.smyx_plant_wilting_quantification_analysis --list

# 输出精简报告
python -m scripts.smyx_plant_wilting_quantification_analysis --input plant.jpg --detail basic

# 保存结果到文件
python -m scripts.smyx_plant_wilting_quantification_analysis --input plant.jpg --output result.json
```
