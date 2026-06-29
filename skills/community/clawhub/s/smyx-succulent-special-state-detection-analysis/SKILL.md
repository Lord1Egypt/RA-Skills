---
name: "smyx-succulent-special-state-detection-analysis"
description: "AI-powered succulent special-state detection from HD images via plant cameras or smartphones. Identifies three critical conditions—black rot (stem base or leaves turning black and mushy), etiolation/melting (leaves becoming translucent and water-soaked), and stretching (elongated internodes, widened leaf spacing, loose rosette)—and outputs the anomaly type with severity grading, enabling early intervention such as beheading, water restriction, or increased light. Scenarios: home succulent care, succulent greenhouses, flower shops. | 通过多肉种植摄像头或手机拍摄的高清图像，利用AI视觉分析技术识别多肉植物的三种常见异常状态：黑腐病（茎基部或叶片变黑、腐烂）、化水（叶片透明化、水渍状）、徒长（茎节拉长、叶片间距增大、形态松散）。输出对应的异常状态类型及严重程度，帮助种植者及时采取处理措施（如砍头、控水、增加光照）。应用场景：多肉植物家庭养护、多肉大棚、花店。"
version: "1.0.3"
license: "MIT-0"
---

# 🌵 Succulent Special State Detection | 多肉植物特殊状态识别
> **智能分析中枢** · 图片/视频智能分析 · 结构化报告 · 历史报告云端查询

---

## 🧭 技能概览 | Overview

| 模块 | 内容 |
|---|---|
| 🏷️ 技能名称 | **多肉植物特殊状态识别** |
| 🎯 核心目标 | 通过多肉种植摄像头或手机拍摄的高清图像，利用AI视觉分析技术识别多肉植物的三种常见异常状态：黑腐病（茎基部或叶片变黑、腐烂）、化水（叶片透明化、水渍状）、徒长（茎节拉长、叶片间距增大、形态松散）。输出对应的异常状态类型及严重程度，帮助种植者及时采取处理措施（如砍头、控水、增加光照）。应用场景：多肉植物家庭养护、多肉大棚、花店。 |
| 🖼️ 输入类型 | 图片、视频、本地文件、网络 URL |
| 📝 输出能力 | 结构化分析报告、识别/监测结果、建议与报告链接 |
| 🧩 场景码 | `SMYX_SUCCULENT_SPECIAL_STATE_DETECTION_ANALYSIS` |

AI-powered succulent special-state detection from HD images via plant cameras or smartphones. Identifies three critical conditions—black rot (stem base or leaves turning black and mushy), etiolation/melting (leaves becoming translucent and water-soaked), and stretching (elongated internodes, widened leaf spacing, loose rosette)—and outputs the anomaly type with severity grading, enabling early intervention such as beheading, water restriction, or increased light. Scenarios: home succulent care, succulent greenhouses, flower shops.

通过多肉种植摄像头或手机拍摄的高清图像，利用AI视觉分析技术识别多肉植物的三种常见异常状态：黑腐病（茎基部或叶片变黑、腐烂）、化水（叶片透明化、水渍状）、徒长（茎节拉长、叶片间距增大、形态松散）。输出对应的异常状态类型及严重程度，帮助种植者及时采取处理措施（如砍头、控水、增加光照）。应用场景：多肉植物家庭养护、多肉大棚、花店。

## 🤖 AI 角色 | AI Role
| 角色要点 | 说明 |
|---|---|
| 说明 1 | **假设你是一个专业的多肉植物健康AI。你的任务是分析多肉植物的高清图像，检测是否存在黑腐、化水、徒长等特殊异常状态，评估严重程度。不要提供具体的救治步骤，仅输出识别到的状态类型及置信度。** |

## 🎬 技能演示 | Skill Demo

[▶️ 点击查看技能使用介绍](https://lifeemergence.com/sample.html)

---

## 🎯 任务目标 | Goals
### 1. 🧩 技能用途

通过多肉植物高清图像检测黑腐病、化水、徒长三种特殊异常状态，输出状态类型、严重程度和置信度

### 2. 🛠️ 能力范围

| 序号 | 具体能力 |
|---:|---|
| 1 | 黑腐病识别（茎基/叶片变黑腐烂） |
| 2 | 化水识别（叶片透明水渍状） |
| 3 | 徒长识别（茎节拉长/叶片松散） |
| 4 | 严重程度分级（轻度/中度/重度） |
| 5 | 置信度评分 |
| 6 | 异常部位定位 |

### 3. ⚡ 触发条件

| 触发类型 | 触发规则 |
|---|---|
| ✅ 默认触发 | **默认触发**：当用户提供多肉植物图像或视频需要分析时，默认触发本技能进行特殊状态识别 |
| 🔎 明确分析意图 | 当用户明确需要多肉状态检测时，提及黑腐、化水、徒长、多肉变黑、多肉透明、多肉长歪等关键词，并且上传了图像或视频文件 |
| 📚 历史报告查询 | 当用户提及以下关键词时，**自动触发历史报告查询功能** ：查看历史多肉状态报告、历史黑腐检测报告、多肉报告清单、显示所有状态报告、查询多肉健康记录 |

### 4. 🤖 自动行为

| 自动行为 | 执行要求 |
|---|---|
| 📎 附件处理 | 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件 |
| ☁️ 历史报告查询 | 如果用户触发历史报告查询关键词，必须直接调用云端 API 查询，不得从本地记忆或人工汇总中获取 |

#### ⚠️ 强制数据获取规则（次高优先级）

> **橙色强约束：** 历史报告清单只允许从云端接口读取，不允许从本地记录、长期记忆或人工汇总中提取。

必须执行：

```bash
python -m scripts.smyx_succulent_special_state_detection_analysis --list
```

| 类型 | 要求 |
|---|---|
| ✅ 必须 | 使用 `python -m scripts.smyx_succulent_special_state_detection_analysis --list` 调用 API 查询云端的历史报告数据 |
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
| 3 | ⚙️ 执行特殊状态识别 | 调用 `-m scripts.smyx_succulent_special_state_detection_analysis` 处理输入（**必须在技能根目录下运行脚本**） |
| 4 | 📊 查看识别结果 | 接收结构化分析报告，查看识别/监测结果、风险提示、建议与报告链接 |

### ⚙️ 脚本参数说明

| 参数 | 含义 | 备注 |
|---|---|---|
| `--input` | 本地多肉植物图像/视频文件路径 | 适用于本地文件分析 |
| `--url` | 网络多肉植物图像/视频 URL 地址（API 服务自动下载） | API 服务自动下载网络资源 |
| `--pet-type` | 对象类型，植物场景默认 other | 按需填写 |
| `--list` | 显示多肉特殊状态识别历史报告列表清单 | 用于云端历史报告查询 |
| `--api-url` | API 服务地址（可选，使用默认值） | 按需填写 |
| `--detail` | 输出详细程度（basic/standard/json，默认 json） | 输出详细程度 |
| `--output` | 结果输出文件路径（可选） | 可选 |

## 🖤 黑腐病（Black Rot）

| 项目 | 说明 |
|------|------|
| 识别特征 | 茎基部或叶片出现黑色/深褐色腐烂区域，组织变软流液 |
| 常见诱因 | 高温高湿 + 伤口感染真菌（镰刀菌等）；浇水后积水未排 |
| 死亡风险 | ⚠️ **极高** — 从感染到整株死亡可能仅需 3-7 天 |
| 早期信号 | 茎基部轻微发黑、底部叶片异常脱落、轻压有软感 |
| 进展速度 | 极快，尤其在夏季闷热环境 |

### 黑腐严重程度分级

| 级别 | 视觉表现 | 危险程度 |
|------|----------|----------|
| 🟡 轻度 | 局部叶片发黑，茎部尚未变软 | 及时处理可救回 |
| 🟠 中度 | 茎基部发黑变软，多片叶片受影响 | 需紧急砍头抢救 |
| 🔴 重度 | 大面积腐烂，整株发黑流液 | 通常不可逆，建议取健康叶片叶插 |

## 💧 化水（Etiolation / Melting）

| 项目 | 说明 |
|------|------|
| 识别特征 | 叶片变为半透明/水渍状，质地变软呈果冻感，轻触即破 |
| 常见诱因 | 浇水过多 + 通风不良；低温高湿环境下更易发生 |
| 死亡风险 | ⚠️ **高** — 化水叶片不可恢复，且易蔓延至全株 |
| 早期信号 | 底部叶片微微发黄变透明，触感变软 |
| 与黑腐区别 | 化水为透明水渍状，黑腐为黑色腐烂；化水常是黑腐的前兆 |

### 化水严重程度分级

| 级别 | 视觉表现 | 处理紧迫性 |
|------|----------|------------|
| 🟡 轻度 | 1-2片底部叶片微透明 | 摘除化水叶，控水通风 |
| 🟠 中度 | 多片叶片透明软化 | 需摘除所有化水叶，检查茎部是否健康 |
| 🔴 重度 | 大面积化水，茎部也开始软化 | 紧急砍头至健康组织，晾干后重新发根 |

## 🌿 徒长（Stretching / Etiolation）

| 项目 | 说明 |
|------|------|
| 识别特征 | 茎节明显拉长、叶片间距增大、莲座形态松散、植株向光弯曲 |
| 常见诱因 | 光照不足 + 浇水偏多；室内养护最常见问题 |
| 死亡风险 | 低（不影响存活，但严重影响观赏性） |
| 早期信号 | 叶片开始变绿变薄、茎部微微拉长、植株不再紧凑 |
| 可逆性 | 已徒长部分不可逆，但可通过增加光照防止继续徒长 |

### 徒长严重程度分级

| 级别 | 视觉表现 | 紧凑度 |
|------|----------|--------|
| 🟡 轻度 | 叶片微微变绿拉长，莲座略松散 | 尚可接受，增加光照即可 |
| 🟠 中度 | 茎节明显拉长，叶片间距显著增大 | 影响美观，建议砍头重新发根 |
| 🔴 重度 | 严重"长脖子"，茎干细长弯曲，叶片稀疏 | 需砍头/叶插重新培育 |

## 🔍 三种状态快速对比

| 特征 | 🖤 黑腐 | 💧 化水 | 🌿 徒长 |
|------|---------|---------|---------|
| 颜色变化 | 黑色/深褐色 | 透明/水渍状 | 变绿/褪色 |
| 质地 | 软烂流液 | 果冻感易破 | 茎细长偏软 |
| 紧迫性 | ⚠️ 最紧急 | 紧急 | 非紧急 |
| 可逆性 | 不可逆（需砍头） | 不可逆（需摘叶） | 不可逆（需砍头重发） |
| 主要诱因 | 真菌感染 | 水多+不通风 | 光照不足 |
| 季节高发 | 夏季闷热 | 梅雨/冬季闷湿 | 冬季室内 |

## 📊 置信度说明

| 置信度区间 | 可靠性 | 说明 |
|------------|--------|------|
| 80%-100% | 🟢 高 | 特征明确，状态判定可靠 |
| 60%-79% | 🟡 中 | 部分特征可见，建议补充特写图像 |
| <60% | 🟠 低 | 特征不典型，可能处于早期，建议持续观察 |

## ⚠️ 多肉养护高危季节提醒

| 季节 | 高危状态 | 原因 | 预防要点 |
|------|----------|------|----------|
| 🌞 夏季（6-9月） | 黑腐 | 高温高湿，真菌活跃 | 遮阴通风，严格控水，避免叶心积水 |
| 🌧️ 梅雨季 | 化水 | 持续阴雨，空气湿度大 | 停水，移至室内，加强通风 |
| ❄️ 冬季 | 徒长 | 室内光照不足 | 补光灯辅助，减少浇水频率 |
| 🍂 春秋 | 相对安全 | 温度适宜，光照充足 | 正常养护，是换盆叶插的好时机 |

## 🗂️ 资源索引 | Resource Index
| 资源类型 | 路径 | 用途 | 何时读取 |
|---|---|---|---|
| 🐍 必要脚本 | [`scripts/smyx_succulent_special_state_detection_analysis.py`](scripts/smyx_succulent_special_state_detection_analysis.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 🐍 必要脚本 | [`scripts/config.py`](scripts/config.py) | 调用 API、执行分析或查询历史报告 | 执行分析或查询时使用 |
| 📘 领域参考 | [`references/api_doc.md`](references/api_doc.md) | 了解 API 接口规范、字段说明和错误码 | 仅在需要了解接口规范或错误码时读取 |

## ⚠️ 注意事项 | Notes
| 分类 | 注意事项 |
|---|---|
| 📚 文档读取 | 仅在需要时读取参考文档，保持上下文简洁 |
| 📁 格式支持 | 支持 jpg/png/mp4/avi/mov 格式，最大 10MB |
| 🔎 使用提醒 | **拍摄要求**：高清近景为主，需看清叶片和茎基细节；整体+特写各一张效果更佳 |
| 🔎 使用提醒 | **仅输出状态类型及置信度，不提供具体救治步骤** |
| 🔎 使用提醒 | 黑腐和化水早期症状相似，置信度可能偏低，建议持续观察 |
| 🔎 使用提醒 | 多肉品种繁多（景天科、百合科、仙人掌科等），不同品种表现有差异 |
| 🔎 使用提醒 | 夏季黑腐发展极快，发现疑似症状应尽早处理 |
| 🚫 脚本限制 | 禁止临时生成脚本，只能用技能本身的脚本 |
| 🌐 网络地址 | 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载 |
| 📜 报告输出 | 当显示历史识别报告清单的时候，从接口返回 json 数据中提取字段  作为超链接地址，且自动转化为如下 Markdown |
| 📜 报告输出 | 表格输出示例 |

## 🧰 使用示例 | Examples
```bash
# 分析本地多肉图像
python -m scripts.smyx_succulent_special_state_detection_analysis --input /path/to/succulent.jpg

# 分析网络多肉图像
python -m scripts.smyx_succulent_special_state_detection_analysis --url https://example.com/succulent.jpg

# 显示历史识别报告/显示报告清单列表
python -m scripts.smyx_succulent_special_state_detection_analysis --list

# 输出精简报告
python -m scripts.smyx_succulent_special_state_detection_analysis --input succulent.jpg --detail basic

# 保存结果到文件
python -m scripts.smyx_succulent_special_state_detection_analysis --input succulent.jpg --output result.json
```
