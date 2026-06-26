---
name: "smyx-plant-wilting-quantification-analysis"
description: "AI-powered plant wilting quantification from full-plant images via smart pots or fixed cameras. Detects leaf-stem angle (leaf droop), stem straightness, and leaf turgidity to quantify wilting severity (0-100%). Optionally fuses soil-moisture sensor data to discriminate dehydration (underwatering) vs. waterlogging (root hypoxia), and auto-triggers watering or drainage prompts for precision irrigation. Scenarios: smart pots, home gardening, greenhouses, plant factories. | 通过智能花盆或固定摄像头拍摄植物整体图像，利用AI视觉分析技术检测叶片与茎秆的夹角（叶片下垂角度）、茎秆挺直程度以及叶片舒展度，量化萎蔫程度（0-100%）。可选结合土壤湿度传感器数据，综合判断萎蔫原因是缺水还是水涝（根部缺氧导致）。可自动触发灌溉或排水提示，帮助用户精准浇水。应用场景：智能花盆、家庭园艺、温室大棚、植物工厂。"
version: "1.0.1"
license: "MIT-0"
---

# Plant Wilting Quantification (Underwatering / Overwatering) | 植物萎蔫程度量化（缺水/水多）

AI-powered plant wilting quantification from full-plant images via smart pots or fixed cameras. Detects leaf-stem angle (leaf droop), stem straightness, and leaf turgidity to quantify wilting severity (0-100%). Optionally fuses soil-moisture sensor data to discriminate dehydration (underwatering) vs. waterlogging (root hypoxia), and auto-triggers watering or drainage prompts for precision irrigation. Scenarios: smart pots, home gardening, greenhouses, plant factories.

通过智能花盆或固定摄像头拍摄植物整体图像，利用AI视觉分析技术检测叶片与茎秆的夹角（叶片下垂角度）、茎秆挺直程度以及叶片舒展度，量化萎蔫程度（0-100%）。可选结合土壤湿度传感器数据，综合判断萎蔫原因是缺水还是水涝（根部缺氧导致）。可自动触发灌溉或排水提示，帮助用户精准浇水。应用场景：智能花盆、家庭园艺、温室大棚、植物工厂。

## 🎯 AI 角色

**假设你是一个专业的植物生理健康AI。你的任务是分析植物的整体图像（侧视图最佳），计算萎蔫指数（基于叶片与茎秆夹角、茎秆弯曲度等），并可结合土壤湿度数据（若提供）判断萎蔫原因（缺水或水涝）。不要提供具体浇水量，仅输出萎蔫程度和可能原因。**

## 任务目标

- 本 Skill 用于：通过植物整体图像量化萎蔫程度，并结合可选土壤湿度数据判断萎蔫原因，输出干预方向建议
- 能力包含：叶片下垂角度检测、茎秆挺直程度评估、叶片舒展度分析、萎蔫指数综合评分（0-100%）、缺水/水涝原因判别（结合可选土壤湿度）、灌溉/排水方向建议
- 触发条件:
    1. **默认触发**：当用户提供植物整体图像或视频需要分析时，默认触发本技能进行萎蔫量化
    2. 当用户明确需要萎蔫监测时，提及植物萎蔫、叶子耷拉、茎秆下垂、缺水、水涝、浇水判断等关键词，并且上传了图像或视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史萎蔫报告、历史萎蔫量化报告、萎蔫报告清单、显示所有萎蔫报告、查询浇水建议记录
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有萎蔫报告"、"显示萎蔫量化报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_plant_wilting_quantification_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行萎蔫量化前，必须按以下优先级顺序获取 open-id：**

```
第 1 步：【最高优先级】检查技能所在目录的配置文件（优先）
        路径：scripts/config.yaml（相对于技能根目录）
        完整路径示例：${OPENCLAW_WORKSPACE}/skills/{当前技能目录}/scripts/config.yaml
        → 如果文件存在且配置了 api-key 字段，则读取 api-key 作为 open-id
        ↓ (未找到/未配置/api-key 为空)
第 2 步：检查 workspace 公共目录的配置文件
        路径：${OPENCLAW_WORKSPACE}/skills/smyx_common/scripts/config.yaml
        → 如果文件存在且配置了 api-key 字段，则读取 api-key 作为 open-id
        ↓ (未找到/未配置)
第 3 步：检查用户是否在消息中明确提供了 open-id
        ↓ (未提供)
第 4 步：❗ 必须暂停执行，明确提示用户提供用户名或手机号作为 open-id
```

**⚠️ 关键约束：**

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、userC113、user123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询历史报告记录），并询问是否继续

---

- 标准流程:
    1. **准备图像/视频输入**
        - 提供本地植物整体图像/视频文件路径或网络 URL
        - 拍摄建议：
          - **侧视图最佳**，能清晰看到叶片与茎秆的夹角
          - 光线充足（自然光最佳），避免逆光
          - 固定角度定期拍摄便于对比萎蔫变化
        - 支持图像（jpg/png）和视频（mp4/avi/mov）格式
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行萎蔫量化**
        - 调用 `-m scripts.smyx_plant_wilting_quantification_analysis` 处理图像/视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地植物图像/视频文件路径
            - `--url`: 网络植物图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 对象类型，植物场景默认 other
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示萎蔫量化历史报告列表清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看量化结果**
        - 接收结构化的萎蔫量化报告
        - 包含：**萎蔫指数（0-100%）**、**叶片下垂角度**、**茎秆挺直度**、**叶片舒展度**、**萎蔫原因判断**（缺水/水涝/其他，结合可选土壤湿度）、**干预方向建议**（如"缺水，请浇水"或"水涝，请停止浇水并松土"）
        - **重要提示**：仅输出萎蔫程度和可能原因，**不提供具体浇水量**

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

## 资源索引

- 必要脚本：见 [scripts/smyx_plant_wilting_quantification_analysis.py](scripts/smyx_plant_wilting_quantification_analysis.py)(用途：调用 API 进行萎蔫量化分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景代码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持 jpg/png/mp4/avi/mov 格式，最大 10MB
- **拍摄要求**：侧视图最佳，需清晰看到叶片与茎秆关系；俯视图无法准确评估下垂角度
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **仅输出萎蔫程度和可能原因，不提供具体浇水量**
- 无土壤湿度数据时，缺水/水涝判断为推测，建议结合手动检查土壤确认
- 高温午间萎蔫为正常蒸腾萎蔫，傍晚可自行恢复，无需紧急浇水
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史量化报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"对象类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`植物萎蔫量化报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 对象类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 植物萎蔫量化报告-20260312172200001 | 植物 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地植物图像（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_plant_wilting_quantification_analysis --input /path/to/plant_side.jpg --open-id your-open-id

# 分析网络植物图像（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_plant_wilting_quantification_analysis --url https://example.com/plant.jpg --open-id your-open-id

# 显示历史量化报告/显示报告清单列表
python -m scripts.smyx_plant_wilting_quantification_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_plant_wilting_quantification_analysis --input plant.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_plant_wilting_quantification_analysis --input plant.jpg --open-id your-open-id --output result.json
```
