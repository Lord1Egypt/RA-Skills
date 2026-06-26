---
name: "elderly-bed-exit-wandering-monitoring-analysis"
description: "Identifies abnormal behaviors such as getting out of bed at night, prolonged wandering, and remaining motionless for extended periods. It is suitable for night-time safety monitoring in nursing homes and for elderly people living alone. | 老人离床徘徊监测技能，识别夜间起床离床、长时间徘徊、长时间静止不动异常行为，适用于养老院、独居老人夜间安全监测"
version: "1.0.4"
license: "MIT-0"
---

# Elderly Bed-Exit & Wandering Monitor | 老人离床徘徊监测技能

Utilizing infrared or low-light cameras, this capability monitors the nighttime activity of the elderly in real-time,
precisely identifying abnormal behaviors such as bed exiting, prolonged wandering, or extended periods of immobility.
Based on human skeletal tracking and behavioral temporal analysis, the system automatically assesses risk levels without
disturbing the senior's rest. When it detects scenarios like failure to return to bed for an extended period, persistent
aimless wandering, or stillness exceeding a set threshold, it immediately issues tiered alerts to caregivers or family
members. Ideal for night-time safety monitoring in nursing homes and for seniors living alone, it effectively reduces
the risks of falls and sudden medical emergencies.

本技能通过红外或低照度摄像头实时监测夜间老人的活动状态，精准识别起床离床、长时间徘徊、长时间静止不动等异常行为。系统基于人体骨骼点追踪与行为时序分析，能在不打扰老人休息的前提下自动判断风险等级。当检测到离床后长时间未归、持续无意义徘徊或静止超过设定阈值时，立即向照护人员或家属发出分级预警，适用于养老院、独居老人家庭等夜间安全监测场景，有效降低跌倒、突发疾病等意外风险。

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过夜间监控视频分析，识别老人异常行为：夜间起床离床、长时间徘徊、长时间静止不动
- 能力包含：离床检测、徘徊行为识别、异常时长统计、异常行为报警
- **适用场景**：养老院老人夜间安全监测、独居老人起夜异常行为监测、护理院安全看护
- **报警逻辑**：
    - 夜间正常起夜一般短时间如厕后返回床上休息，不报警
    - 离床后长时间徘徊/长时间静止不起 → 触发预警
    - 长时间卧床不起 → 也触发提醒
- 触发条件:
    1. **默认触发**：当用户提供夜间监控视频需要检测老人离床徘徊异常行为时，默认触发本技能
    2. 当用户明确需要离床监测、徘徊监测时，提及老人离床、夜间徘徊、起床监测、异常行为监测等关键词，并且上传了监控视频
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史监测报告、离床监测报告清单、监测报告列表、查询历史监测报告、显示所有监测报告、离床行为分析报告，查询老人离床徘徊监测分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有监测报告"、"显示所有夜间监测"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.elderly_bed_exit_wandering_monitoring_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 监测要求（获得准确结果的前提）

为了获得准确的异常行为识别，请确保：

1. **摄像头固定位置**，覆盖床位和主要活动区域
2. **夜间红外/夜视模式** 正常可见人形，保证清晰度满足识别
3. **床位区域清晰可见**，能够判断老人是否在床

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行老人离床徘徊监测分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如
  openclaw-control-ui、default、openclaw-control-ui、elderly123、monitoring456 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询监测报告记录），并询问是否继续

---

- 标准流程:
    1. **准备监控视频输入**
        - 提供本地视频文件路径或网络视频 URL
        - 最好为夜间监控视频，覆盖床位区域
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行老人离床徘徊监测分析**
        - 调用 `-m scripts.elderly_bed_exit_wandering_monitoring_analysis` 处理视频（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示历史老人离床徘徊监测分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的老人离床徘徊监测分析报告
        - 包含：视频基本信息、监测时间段、识别到的异常行为类型、持续时长、是否触发报警、护理建议

## 资源索引

-

必要脚本：见 [scripts/elderly_bed_exit_wandering_monitoring_analysis.py](scripts/elderly_bed_exit_wandering_monitoring_analysis.py)(
用途：调用 API 进行老人离床徘徊监测分析，本地文件上传，网络 URL 由 API 服务自动下载)

- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：mp4/avi/mov，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **⚠️ 重要提示**：本识别结果仅供安全护理参考，不能替代人工检查和人工确认，发现异常报警请及时通知护理人员现场查看
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"分析时间"、"异常行为类型"、"是否报警"、"点击查看"五列，其中"报告名称"列使用`老人离床徘徊监测报告-{记录id}`
  形式拼接, "点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 分析时间 | 异常行为类型 | 是否报警 | 点击查看 |
  |----------|----------|------------------|----------|----------|
  | 老人离床徘徊监测报告 -20260328221000001 | 2026-03-28 22:10 | 离床徘徊30分钟 |
  是 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地夜间监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.elderly_bed_exit_wandering_monitoring_analysis --input /path/to/night_monitor.mp4 --open-id openclaw-control-ui

# 分析网络监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.elderly_bed_exit_wandering_monitoring_analysis --url https://example.com/night.mp4 --open-id openclaw-control-ui

# 显示历史监测报告/显示监测报告清单列表/显示历史离床监测（自动触发关键词：查看历史监测报告、历史报告、监测报告清单等）
python -m scripts.elderly_bed_exit_wandering_monitoring_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.elderly_bed_exit_wandering_monitoring_analysis --input monitor.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.elderly_bed_exit_wandering_monitoring_analysis --input monitor.mp4 --open-id your-open-id --output result.json
```
