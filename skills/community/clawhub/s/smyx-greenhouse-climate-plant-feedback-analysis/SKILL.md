---
name: "smyx-greenhouse-climate-plant-feedback-analysis"
description: "Using fixed cameras in a smart greenhouse to analyze plant morphology in real time (e.g., leaf wilting angle, stem uprightness, leaf color changes) combined with environmental sensors (light intensity, temperature, humidity, soil moisture), an AI decision model outputs climate control commands including irrigation (pump/solenoid valve), shade-net opening, fan/wet-curtain on-off, heater on-off, etc. This skill implements closed-loop control driven by plant demand, improving resource efficiency and crop yield. Application scenarios: smart greenhouses, plant factories, multi-span greenhouses. The system continuously monitors plant state and environmental parameters: when plants wilt (water shortage) and soil moisture falls below a threshold it issues an irrigation command; when light is too strong and leaves curl it issues a shading command; when temperature/humidity exceed thresholds and plants show heat stress it issues fan/wet-curtain start commands. Skill features: precision energy saving. | 通过智能温室中的固定摄像头实时分析植物的形态（如叶片萎蔫角度、茎秆挺直度、叶色变化）以及结合环境传感器（光照强度、温度、湿度、土壤水分），利用AI决策模型输出环境调控指令，包括灌溉（水泵/电磁阀）、遮阳网开度、风机/湿帘启停、加热器开关等。该技能实现基于植物需求的闭环控制，提高资源利用效率和作物产量。应用场景：智能温室、植物工厂、连栋大棚。系统持续监测植物状态和环境参数，当检测到植物萎蔫（缺水）且土壤湿度低于阈值时输出灌溉指令；当光照过强导致叶片卷曲时输出遮阳指令；当温湿度超过设定阈值且植物表现出热胁迫时输出风机/湿帘启动指令。技能特点：精准节能。"
version: "1.0.0"
---

# Greenhouse Climate Plant Feedback Analysis | 温室环境与植物状态联动调控

Using fixed cameras in a smart greenhouse to analyze plant morphology in real time (e.g., leaf wilting angle, stem uprightness, leaf color changes) combined with environmental sensors (light intensity, temperature, humidity, soil moisture), an AI decision model outputs climate control commands including irrigation (pump/solenoid valve), shade-net opening, fan/wet-curtain on-off, heater on-off, etc. This skill implements closed-loop control driven by plant demand, improving resource efficiency and crop yield. Application scenarios: smart greenhouses, plant factories, multi-span greenhouses. The system continuously monitors plant state and environmental parameters: when plants wilt (water shortage) and soil moisture falls below a threshold it issues an irrigation command; when light is too strong and leaves curl it issues a shading command; when temperature/humidity exceed thresholds and plants show heat stress it issues fan/wet-curtain start commands. Skill features: precision energy saving.

通过智能温室中的固定摄像头实时分析植物的形态（如叶片萎蔫角度、茎秆挺直度、叶色变化）以及结合环境传感器（光照强度、温度、湿度、土壤水分），利用AI决策模型输出环境调控指令，包括灌溉（水泵/电磁阀）、遮阳网开度、风机/湿帘启停、加热器开关等。该技能实现基于植物需求的闭环控制，提高资源利用效率和作物产量。应用场景：智能温室、植物工厂、连栋大棚。系统持续监测植物状态和环境参数，当检测到植物萎蔫（缺水）且土壤湿度低于阈值时输出灌溉指令；当光照过强导致叶片卷曲时输出遮阳指令；当温湿度超过设定阈值且植物表现出热胁迫时输出风机/湿帘启动指令。技能特点：精准节能。

## 🎯 AI 角色

**假设你是一个专业的温室环境智能控制 AI。你的任务是分析植物的实时图像（叶片角度、茎秆弯曲度、叶色）以及接收环境传感器数据（光照强度 lux、空气温度 ℃、相对湿度 %、土壤湿度 %），综合判断植物当前的水分、光照、温度胁迫状态，并输出相应的环境调控指令（灌溉、遮阳、风机、加热等）。不要提供具体的控制参数（如 PID 值、阀门开度百分比），仅输出动作指令及优先级（HIGH / MEDIUM / LOW）。**

## 任务目标

- 本 Skill 用于：基于温室固定摄像头的植物形态图像 + 可选环境传感器数据，输出闭环环境调控指令集，实现按需灌溉、遮阳、通风、加热
- 能力包含：叶片萎蔫角度估算、茎秆挺直度评估、叶色变化识别（黄化/卷曲/灼烧）、水分胁迫判断、光照胁迫判断、温度胁迫判断、调控指令生成（灌溉/遮阳/风机/湿帘/加热）、指令优先级排序、节能与资源利用建议
- 触发条件:
    1. **默认触发**：当用户提供温室植物图像/视频 URL 或文件需要分析时，默认触发本技能进行环境联动调控分析
    2. 当用户明确提及温室、连栋大棚、植物工厂、智能调控、灌溉、遮阳网、风机、湿帘、加热器、萎蔫、热胁迫、闭环控制等关键词，并且上传了植物图像/视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看温室调控历史、温室联动报告清单、调控指令历史、温室控制报告、查询历史调控记录、显示所有温室调控报告、显示植物联动调控诊断报告，查询温室调控建议清单
- 自动行为：
    1. 如果用户上传了附件或者植物图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有温室调控报告"、"
       显示所有联动调控报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_greenhouse_climate_plant_feedback_analysis --list --open-id` 参数调用 API
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

**在执行温室联动调控分析前，必须按以下优先级顺序获取 open-id：**

```
第 1 步：【最高优先级】检查技能所在目录的配置文件（优先）
        路径：skills/smyx_common/scripts/config.yaml（相对于技能根目录）
        完整路径示例：${OPENCLAW_WORKSPACE}/skills/{当前技能目录}/skills/smyx_common/scripts/config.yaml
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
    1. **准备植物图像/视频输入**
        - 提供本地植物图像/视频文件路径或网络 URL
        - 确保图像清晰展示植物冠层（叶片、茎秆、叶色），光照充足或夜间补光
        - 可选：附带同时段的环境传感器数据（光照 lux、气温 ℃、湿度 %、土壤湿度 %）
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行温室联动调控分析**
        - 调用 `-m scripts.smyx_greenhouse_climate_plant_feedback_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地温室植物图像/视频文件路径
            - `--url`: 网络温室植物图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，温室植物场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示温室联动调控历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的温室联动调控指令报告
        - 包含：植物形态评估（萎蔫角度、茎秆挺直度、叶色变化）、环境胁迫状态（水分/光照/温度）、调控指令列表（灌溉/遮阳/风机/湿帘/加热）、指令优先级（HIGH/MEDIUM/LOW）、节能与资源利用建议
        - **重要提示**：仅输出动作指令及优先级，不输出 PID/阀门开度等具体控制参数

## 资源索引

- 必要脚本：见 [scripts/smyx_greenhouse_climate_plant_feedback_analysis.py](scripts/smyx_greenhouse_climate_plant_feedback_analysis.py)(
  用途：调用 API 进行温室环境与植物状态联动调控分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范、调控指令枚举和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 jpg/png 图像或 mp4/avi/mov 视频，最大 10MB；建议覆盖完整植物冠层
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅作为温室控制决策参考，实际执行建议结合本地控制器安全策略
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"温室区域"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`温室联动调控分析报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 温室区域 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 温室联动调控分析报告-20260312172200001 | A区番茄棚 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地温室植物图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_greenhouse_climate_plant_feedback_analysis --input /path/to/greenhouse_video.mp4 --open-id your-open-id

# 分析网络温室视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_greenhouse_climate_plant_feedback_analysis --url https://example.com/greenhouse_video.mp4 --open-id your-open-id

# 显示历史调控报告/调控报告清单（自动触发关键词：查看温室调控历史、温室联动报告清单、调控指令历史等）
python -m scripts.smyx_greenhouse_climate_plant_feedback_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_greenhouse_climate_plant_feedback_analysis --input video.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_greenhouse_climate_plant_feedback_analysis --input video.mp4 --open-id your-open-id --output result.json
```
