---
name: "infant-sleep-monitoring-analysis"
description: "Identifies sleep states like deep sleep, light sleep, waking, and restlessness. Generates daily sleep reports and schedule analysis to help parents understand their baby's sleep patterns. | 婴儿睡眠状态监测技能，识别熟睡、浅睡、苏醒、躁动不同睡眠状态，生成每日睡眠报告和作息分析，帮助家长掌握宝宝睡眠规律"
version: "1.0.1"
---

# Baby Sleep State Monitoring Skill | 婴儿睡眠状态监测技能

Utilizing high-sensitivity sensing technology, this feature conducts refined monitoring of infant sleep cycles,
precisely distinguishing between different states such as deep sleep, light sleep, awakening, and restlessness. The
system automatically records full-night sleep data and, through intelligent algorithms, generates visualized daily sleep
reports and in-depth routine analysis. This not only helps parents intuitively understand their baby's sleep quality but
also assists them in mastering the baby's circadian rhythms, thereby scientifically adjusting schedules and cultivating
healthy sleep habits.

本功能利用高灵敏度传感技术，对婴儿的睡眠周期进行精细化监测，能够精准区分熟睡、浅睡、苏醒及躁动等不同状态。系统会自动记录全晚的睡眠数据，通过智能算法生成可视化的每日睡眠报告与深度作息分析。这不仅能帮助家长直观了解宝宝的睡眠质量，更能辅助其掌握宝宝的生物钟规律，从而科学地调整作息安排，培养宝宝良好的睡眠习惯

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过婴儿房夜间监控视频分析，识别宝宝不同睡眠状态：熟睡、浅睡、苏醒、躁动
- 能力包含：睡眠状态分类、睡眠时间统计、觉醒次数统计、生成睡眠报告、作息规律分析
- **适用场景**：婴儿房睡眠监测、宝宝睡眠习惯分析、家长科学育儿参考
- 输出：每日睡眠时长分布、状态变化曲线、作息规律总结、哄睡建议
- 触发条件:
    1. **默认触发**：当用户提供婴儿睡眠监控视频需要分析睡眠状态时，默认触发本技能
    2. 当用户明确需要婴儿睡眠监测、睡眠状态分析时，提及睡眠监测、宝宝睡眠、睡眠报告、作息分析等关键词，并且上传了监控视频
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史睡眠报告、睡眠监测报告清单、监测报告列表、查询历史监测报告、显示所有监测报告、睡眠分析报告，查询婴儿睡眠监测分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有睡眠报告"、"显示历史睡眠监测"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.infant_sleep_monitoring_analysis --list --open-id` 参数调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 监测要求（获得准确结果的前提）

为了获得准确的睡眠状态分析，请确保：

1. **摄像头固定位置**，覆盖婴儿床整体区域
2. **夜视/红外功能正常**，关灯后宝宝轮廓清晰可见
3. **婴儿床无过多杂物遮挡**，保证宝宝身体姿态完整可见

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行婴儿睡眠监测分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、babysleep123、sleeppattern456 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询监测报告记录），并询问是否继续

---

- 标准流程:
    1. **准备婴儿床监控视频输入**
        - 提供本地视频文件路径或网络视频 URL
        - 建议至少覆盖数小时睡眠周期
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行婴儿睡眠状态监测分析**
        - 调用 `-m scripts.infant_sleep_monitoring_analysis` 处理视频（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示历史婴儿睡眠监测分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的婴儿睡眠监测分析报告
        - 包含：监测时长、各睡眠状态时长统计、觉醒次数、睡眠规律评分、育儿建议

## 资源索引

- 必要脚本：见 [scripts/infant_sleep_monitoring_analysis.py](scripts/infant_sleep_monitoring_analysis.py)(用途：调用 API
  进行婴儿睡眠监测分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：mp4/avi/mov，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **⚠️ 重要提示**：本分析结果仅供育儿参考，不能替代专业医护建议，宝宝睡眠异常请咨询儿科医生
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"监测时长"、"熟睡时长"、"监测日期"、"点击查看"五列，其中"报告名称"列使用`婴儿睡眠监测报告-{记录id}`形式拼接, "
  点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 监测时长 | 熟睡时长 | 监测日期 | 点击查看 |
  |----------|----------|----------|----------|----------|
  | 婴儿睡眠监测报告 -20260329002800001 | 8小时 | 5.5小时 |
  2026-03-29 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地婴儿房监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.infant_sleep_monitoring_analysis --input /path/to/night_monitor.mp4 --open-id openclaw-control-ui

# 分析网络监控视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.infant_sleep_monitoring_analysis --url https://example.com/night.mp4 --open-id openclaw-control-ui

# 显示历史监测报告/显示监测报告清单列表/显示历史睡眠监测（自动触发关键词：查看历史监测报告、历史报告、监测报告清单等）
python -m scripts.infant_sleep_monitoring_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.infant_sleep_monitoring_analysis --input night_monitor.mp4 --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.infant_sleep_monitoring_analysis --input night_monitor.mp4 --open-id your-open-id --output result.json
```
