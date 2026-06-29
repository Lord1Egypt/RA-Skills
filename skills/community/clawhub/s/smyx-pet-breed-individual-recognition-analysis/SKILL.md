---
name: "pet-breed-individual-recognition-analysis"
description: "Accurately identifies cat and dog breeds and supports distinguishing between different individuals in multi-pet households; an essential assistant for intelligent pet butlers. | 宠物品种个体识别技能，精准识别猫狗宠物品种，支持多宠家庭区分不同独立个体，智能宠物管家好帮手"
version: "1.0.5"
license: "MIT-0"
---

# 🐾 Pet Breed & Individual Identification Skill | 宠物品种个体识别技能

> **智能宠物管家中枢** · 猫狗品种识别 · 多宠个体区分 · 家庭宠物智能管理

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **Pet Breed & Individual Identification Skill / 宠物品种个体识别技能** |
| 🎯 核心目标 | 识别图片/视频中的宠物，准确判断猫狗品种，并支持多宠家庭区分不同独立个体 |
| 🖼️ 输入类型 | 宠物图片、视频、本地文件、网络图片/视频 URL |
| 🧠 技术能力 | 基于深度卷积神经网络（DCNN）的宠物检测、品种分类、个体识别、多目标区分 |
| 📝 输出能力 | 宠物数量、品种判定、个体区分结果、置信度、趣味备注、报告链接 |
| 🏡 适用场景 | 多宠家庭、智能宠物管家、家庭监控、宠物活动记录、宠物身份档案管理 |

Equipped with high-precision breed recognition algorithms based on Deep Convolutional Neural Networks (DCNN), this feature delivers millisecond-level accurate identification of breed characteristics for common pets like cats and dogs. The system not only encompasses a database of hundreds of mainstream and rare breeds globally but is also deeply optimized for multi-pet household scenarios. It supports simultaneous recognition and differentiation of distinct pet individuals within the same frame. By establishing independent pet identity profiles, the system accurately records the activity trajectories and behavioral habits of each pet, effectively resolving identity confusion in multi-pet environments. It provides personalized intelligent management services for pet owners, serving as an indispensable smart butler assistant for modern multi-pet families.

本功能搭载了基于深度卷积神经网络的高精度品种识别算法，能够对猫、狗等常见宠物的品种特征进行毫秒级精准判定。系统不仅涵盖了全球数百种主流及稀有品种的数据库，更针对多宠家庭场景进行了深度优化，支持在同一画面中同时识别并区分不同的宠物个体。通过建立独立的宠物身份档案，系统能够准确记录每只宠物的活动轨迹与行为习惯，有效解决多宠环境下的身份混淆问题，为宠物主人提供个性化的智能管理服务，是现代化多宠家庭不可或缺的智能管家助手。

---

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals

### 1. 🧩 技能用途

本 Skill 用于：识别图片/视频中的宠物，准确判断猫狗品种，支持多宠家庭区分不同独立个体。

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 检测图片/视频中的猫、狗等常见宠物 |
| 2 | 判断猫狗宠物品种，支持主流和稀有品种识别 |
| 3 | 多宠家庭中区分不同独立个体 |
| 4 | 支持同一画面中多个宠物的同时识别与区分 |
| 5 | 配合家庭监控自动记录宠物活动与行为习惯 |
| 6 | 查询历史宠物品种个体识别分析报告清单 |

### 3. 🏡 支持场景

| 场景 | 说明 |
|---|---|
| 🧬 品种识别 | 精准识别上百种猫狗品种 |
| 🐾 个体区分 | 多宠家庭能分辨出“这只是谁”“那只是谁” |
| 🏠 智能管家 | 配合家庭监控自动记录宠物活动 |

### 4. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | 当用户提供宠物图片/视频需要识别品种/个体时，默认触发本技能 |
| 🔎 明确识别意图 | 当用户明确需要宠物识别、品种鉴定时，提及宠物品种识别、猫咪品种、狗狗品种、区分宠物、个体识别等关键词，并且上传了图片/视频 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史识别报告、宠物识别报告清单、识别报告列表、查询历史识别报告、显示所有识别报告、宠物品种分析报告，查询宠物品种个体识别分析报告 |

### 5. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者图片/视频文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发任何历史报告查询关键词（如“查看所有识别报告”、“显示所有宠物识别”、“查看历史报告”等），必须直接调用云端 API 查询 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.pet_breed_individual_recognition_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.pet_breed_individual_recognition_analysis --list` 调用 API 查询云端的历史报告数据 |
| 🚫 严格禁止 | 从本地 `memory` 目录读取历史会话信息 |
| 🚫 严格禁止 | 手动汇总本地记录中的报告 |
| 🚫 严格禁止 | 从长期记忆中提取报告 |
| ✅ 输出格式 | 必须统一从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果 |

---

## 📦 前置准备 | Requirements

### 依赖说明

`scripts` 脚本所需的依赖包及版本：

```txt
requests>=2.28.0
```

---

## 📸 识别要求 | Recognition Requirements

为了获得准确的品种/个体识别，请确保：

| 要求 | 说明 |
|---|---|
| 🐾 宠物完整出镜 | 避免身体、脸部或关键特征被过度遮挡 |
| 💡 光线充足清晰 | 避免过度模糊、暗角、逆光或强烈噪点 |
| 🐕 多宠间距适中 | 多宠同框时尽量保持宠物之间有一定间距，便于分别识别个体 |

---

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

## 🧪 标准流程 | Standard Flow

| 步骤 | 阶段 | 执行动作 |
|---:|---|---|
| 1 | 📥 准备宠物图片/视频输入 | 提供本地图片/视频文件路径或网络 URL；确保宠物完整出镜、光线充足 |
| 2 | 🔐 系统自动完成身份关联 | 无需用户输入任何身份参数；不在回复中展示内部身份值 |
| 3 | ⚙️ 执行宠物品种个体识别分析 | 调用 `-m scripts.pet_breed_individual_recognition_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看分析结果 | 接收结构化的宠物品种个体识别分析报告，包含输入基本信息、检测到的宠物数量、每个宠物的品种判定、个体区分结果、置信度、趣味备注 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地图片/视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络图片/视频 URL 地址 | API 服务自动下载 |
| `--list` | 显示历史宠物品种个体识别分析报告列表清单 | 可以输入起始日期参数过滤数据范围 |
| `--api-url` | API 服务地址 | 可选，使用默认值 |
| `--detail` | 输出详细程度 | `basic` / `standard` / `json`，默认 `json` |
| `--output` | 结果输出文件路径 | 可选 |

---

## 🗂️ 资源索引 | Resource Index

| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/pet_breed_individual_recognition_analysis.py`](scripts/pet_breed_individual_recognition_analysis.py) | 调用 API 进行宠物品种个体识别分析、本地文件上传、网络 URL 由 API 服务自动下载 | 执行分析或查询时使用 |
| ⚙️ 配置文件 | [`scripts/config.py`](scripts/config.py) | 配置 API 地址、默认参数和格式限制 | 需要确认默认配置时读取 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口详细规范和错误码 | 仅在需要了解 API 接口详细规范和错误码时读取 |

---

## ⚠️ 注意事项 | Notes

| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持 `jpg` / `jpeg` / `png` / `mp4` / `avi` / `mov`，最大 `10MB` |
| 🧾 结果性质 | 分析结果仅供宠物爱好参考，纯种鉴定请以专业机构结果为准 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载 |

---

## 📜 历史报告清单输出规范 | Report List Format

当显示历史分析报告清单的时候，从接口返回 JSON 数据中提取字段 `` 作为超链接地址，且自动转化为如下 Markdown 表格格式输出。

### 📌 固定输出列

| 列名 | 生成规则 |
|---|---|
| 报告名称 | 使用 `宠物品种个体识别报告-{记录id}` 形式拼接 |
| 宠物数量 | 从接口返回数据中提取 |
| 分析时间 | 从接口返回数据中提取 |
| 点击查看 | 使用 `[🔗 查看报告]()` 格式的超链接 |

### 🧾 表格输出示例

| 报告名称 | 宠物数量 | 分析时间 | 点击查看 |
|----------|----------|----------|----------|
| 宠物品种个体识别报告 -20260328221000001 | 2只 | 2026-03-28 22:10:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

---

## 📝 隐私与数据安全声明 | Privacy & Data Security

本技能在处理用户上传的视频时，严格遵守数据安全规范：

| 序号 | 说明 |
|---:|---|
| 1 | 🔐 **数据保密处理**：系统基于用户名/手机号生成的标识仅作为用户关联信息，**不保存任何可直接识别个人身份的明文信息** |
| 2 | 🛡️ **安全传输**：所有数据（包括视频文件及关联标识）均通过 **HTTPS/TLS 加密通道** 发送至云端 API 进行分析，防止数据在传输过程中被窃取或篡改 |
| 3 | 🧹 **数据留存策略**：云端服务器遵循“最小必要原则”，**分析任务完成后即刻删除原始视频数据，不进行持久化存储**，确保用户隐私数据不被留存或滥用 |

---

## 🧰 使用示例 | Examples

### 🖼️ 识别本地图片中的宠物

```bash
python -m scripts.pet_breed_individual_recognition_analysis --input /path/to/pets.jpg
```

### 🌐 识别网络图片

```bash
python -m scripts.pet_breed_individual_recognition_analysis --url https://example.com/dogs.jpg
```

### 📚 显示历史识别报告 / 显示识别报告清单列表 / 显示历史宠物识别

> 自动触发关键词：查看历史识别报告、历史报告、识别报告清单等。

```bash
python -m scripts.pet_breed_individual_recognition_analysis --list
```

### 🪶 输出精简报告

```bash
python -m scripts.pet_breed_individual_recognition_analysis --input pets.jpg --detail basic
```

### 💾 保存结果到文件

```bash
python -m scripts.pet_breed_individual_recognition_analysis --input pets.jpg --output result.json
```
