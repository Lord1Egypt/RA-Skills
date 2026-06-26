---
name: "smyx-sleep-quality-analysis-analysis"
description: "AI-powered pet sleep quality analysis from a fixed bed/rest-area camera. Uses motion detection and pose recognition to distinguish sleeping vs. awake states, accumulates total sleep duration, counts roll-overs / position changes and startle-awakenings, and outputs a 0-100 sleep-quality score. Helps owners spot potential pain, anxiety, or disease early. Scenarios: home nighttime monitoring, senior pet health management, animal hospital wards, pet boarding centers. | 通过宠物窝或休息区固定摄像头，在夜间（或宠物主要睡眠时段）持续分析视频，利用运动检测和姿态识别技术判断宠物处于静止（睡眠）或活动（觉醒）状态，累计睡眠总时长，并统计翻身次数、惊醒频次，输出睡眠质量评分（0-100分），帮助主人了解宠物的睡眠健康，识别潜在的疼痛、焦虑或疾病。应用场景：宠物家庭夜间监护、老年宠物健康管理、宠物医院住院观察、寄养中心。"
version: "1.0.2"
license: "MIT-0"
---

# Pet Sleep Quality Analysis (Duration / Roll Count) | 宠物睡眠质量分析（时长/翻滚次数）

AI-powered pet sleep quality analysis from a fixed bed/rest-area camera. Uses motion detection and pose recognition to distinguish sleeping vs. awake states, accumulates total sleep duration, counts roll-overs / position changes and startle-awakenings, and outputs a 0-100 sleep-quality score. Helps owners spot potential pain, anxiety, or disease early. Scenarios: home nighttime monitoring, senior pet health management, animal hospital wards, pet boarding centers.

通过宠物窝或休息区固定摄像头，在夜间（或宠物主要睡眠时段）持续分析视频，利用运动检测和姿态识别技术判断宠物处于静止（睡眠）或活动（觉醒）状态，累计睡眠总时长，并统计翻身次数、惊醒频次，输出睡眠质量评分（0-100分），帮助主人了解宠物的睡眠健康，识别潜在的疼痛、焦虑或疾病。应用场景：宠物家庭夜间监护、老年宠物健康管理、宠物医院住院观察、寄养中心。

## 🎯 AI 角色

**假设你是一个专业的宠物睡眠健康AI。你的任务是分析宠物窝/休息区固定摄像头的夜间视频，检测宠物的活动状态，统计睡眠总时长、翻身次数、惊醒频次，并输出睡眠质量评分。不要提供医疗诊断，仅输出基于视觉的睡眠指标。**

## 任务目标

- 本 Skill 用于：通过夜间或主要睡眠时段视频进行宠物睡眠质量评估，输出睡眠总时长、翻身次数、惊醒频次和综合评分
- 能力包含：睡眠/觉醒状态识别、睡眠总时长累计、翻身/姿势变换次数统计、惊醒事件检测、深睡/浅睡时段划分、睡眠质量综合评分（0-100）
- 触发条件:
    1. **默认触发**：当用户提供宠物窝/休息区夜间视频需要分析时，默认触发本技能进行睡眠质量分析
    2. 当用户明确需要睡眠监测时，提及睡眠质量、翻身、惊醒、夜间监测、宠物失眠、老年宠物睡眠等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史睡眠报告、历史睡眠质量报告、睡眠报告清单、显示所有睡眠报告、查询睡眠记录
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有睡眠报告"、"显示睡眠质量报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_sleep_quality_analysis_analysis --list --open-id` 参数调用 API
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

**在执行睡眠质量分析前，必须按以下优先级顺序获取 open-id：**

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


### 📍 open-id 首次回复服务端签到（严格触发）

**当且仅当以下条件同时成立时，才允许调用服务端签到接口：**

1. 助手刚刚明确询问用户提供 open-id / 用户名 / 手机号；
2. 用户随后首次返回 open-id；
3. 本地首次签到状态中没有这个 open-id 的历史记录。

满足以上条件时，在调用任何分析脚本/API 前，先执行：

```bash
python3 /root/.openclaw/workspace/scripts/track_open_id_received.py --skill smyx_sleep_quality_analysis_analysis --open-id '<open-id>' --source user_reply_after_prompt
```

脚本会自动调用：`ApiEnum.BASE_URL_HEALTH + "/sys/phoneCheckIn"`。

**禁止调用签到接口的情况：**
- open-id 来自历史对话、记忆、已有上下文：不要调用；
- open-id 来自技能目录配置文件：不要调用；
- open-id 来自 workspace 公共配置：不要调用；
- open-id 来自环境变量：不要调用；
- 用户重复发送同一个 open-id，或本地状态已记录：不要调用；
- 不是刚刚询问 open-id 后收到的首次回复：不要调用。

约束：
- 这个签到只表示 **用户首次回复 open-id**，不是分析 API 已调用。
- 必须先完成首次判断；只有符合严格触发条件才签到。
- 签到成功后再执行 `python -m scripts... --open-id ...` 或任何分析服务调用。
- 禁止自行生成 open-id 后签到；只允许对真实首次用户回复的 open-id 签到。

**⚠️ 关键约束：**

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、userC113、user123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询历史报告记录），并询问是否继续

---

- 标准流程:
    1. **准备视频输入**
        - 提供本地宠物窝/休息区夜间视频文件路径或网络视频 URL
        - 拍摄建议：固定摄像头视角覆盖宠物休息区域；夜间需开启红外/夜视模式；建议录制完整睡眠时段（≥1小时，最佳为整夜）
        - 支持视频格式：mp4/avi/mov
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行睡眠质量分析**
        - 调用 `-m scripts.smyx_sleep_quality_analysis_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地宠物窝夜间视频文件路径
            - `--url`: 网络宠物窝夜间视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 cat
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示睡眠质量分析历史报告列表清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的睡眠质量分析报告
        - 包含：**睡眠总时长**（小时/分钟）、**翻身次数**、**惊醒频次**、**深睡/浅睡时段划分**、**睡眠效率百分比**、**睡眠质量综合评分（0-100）**、**异常提示**（如"猫咪昨晚翻身频繁，可能有关节不适或皮肤瘙痒"）
        - **重要提示**：仅输出基于视觉的睡眠指标，**不提供医疗诊断**；持续异常建议就医

## 😴 睡眠指标参考范围

| 指标 | 成猫正常范围 | 成犬正常范围 | 异常预警 |
|------|--------------|--------------|----------|
| 总睡眠时长（24h） | 12-16 小时 | 12-14 小时 | <8 或 >20 小时 |
| 夜间睡眠时长（8h） | 5-7 小时 | 6-8 小时 | <4 小时 |
| 翻身次数（夜间） | 3-8 次 | 5-12 次 | >15 次（夜间） |
| 惊醒次数（夜间） | 0-3 次 | 0-3 次 | >5 次 |
| 深睡占比 | 25%-40% | 20%-35% | <15% |

> 数据仅供算法基线参考；幼宠和老年宠物睡眠时长更长（可达 18-20 小时），属正常。

## 📊 睡眠质量评分体系

| 评分区间 | 睡眠质量 | 说明 |
|----------|----------|------|
| 90-100 | 🌟 优秀 | 睡眠充足、深睡占比高、翻身惊醒少 |
| 75-89 | ✅ 良好 | 整体睡眠质量较好，偶有轻度翻身 |
| 60-74 | ⚠️ 一般 | 翻身或惊醒偏多，建议关注环境与健康 |
| 40-59 | 🟠 较差 | 睡眠片段化明显，可能有焦虑或不适 |
| 0-39 | 🔴 极差 | 睡眠严重异常，建议就医检查 |

## 🚨 异常翻身/惊醒可能提示

| 异常表现 | 可能原因 |
|----------|----------|
| 🦴 频繁翻身 + 关节部位活动 | 关节炎、髋关节发育不良、肌肉酸痛 |
| 🐛 频繁翻身 + 抓挠/舔毛 | 皮肤瘙痒、寄生虫、过敏 |
| 😰 频繁惊醒 + 起身张望 | 焦虑、噪音敏感、认知功能障碍 |
| 🌡️ 频繁变换睡姿 | 环境温度不适（过冷/过热） |
| 💤 睡眠时长骤减 | 疼痛、消化不良、应激事件 |
| 😴 睡眠时长骤增 | 嗜睡、代谢性疾病、低血糖 |

## 💡 高风险群体重点关注

| 类别 | 重点关注原因 |
|------|--------------|
| 老年宠物（>7岁） | 关节炎、认知功能障碍（CDS）高发，睡眠常异常 |
| 大型犬 | 髋关节发育不良易致翻身困难 |
| 短鼻品种 | 睡眠呼吸暂停风险，需观察呼吸节律 |
| 既往焦虑史 | 易频繁惊醒 |
| 术后/疾病恢复期 | 睡眠质量是康复重要指标 |

## 资源索引

- 必要脚本：见 [scripts/smyx_sleep_quality_analysis_analysis.py](scripts/smyx_sleep_quality_analysis_analysis.py)(用途：调用 API 进行宠物睡眠质量分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景代码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB；建议时长 ≥ 1 小时，最佳为整夜
- 夜间拍摄需开启**红外/夜视模式**，确保黑暗环境下可见宠物姿态
- 摄像头需固定，视角完整覆盖宠物休息区域
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **分析结果仅供睡眠健康参考，不提供医疗诊断**；持续异常建议及时就医
- 老年宠物和幼宠的正常睡眠时长普遍更长，请结合个体年龄判断
- 不建议使用宠物活动期作为分析时段，重点应在主要睡眠时段
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`睡眠质量分析报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 睡眠质量分析报告-20260312172200001 | 猫 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地夜间睡眠视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_sleep_quality_analysis_analysis --input /path/to/night_sleep.mp4 --pet-type cat --open-id your-open-id

# 分析网络夜间睡眠视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_sleep_quality_analysis_analysis --url https://example.com/night_sleep.mp4 --pet-type dog --open-id your-open-id

# 显示历史分析报告/显示报告清单列表
python -m scripts.smyx_sleep_quality_analysis_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_sleep_quality_analysis_analysis --input video.mp4 --pet-type cat --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_sleep_quality_analysis_analysis --input video.mp4 --pet-type cat --open-id your-open-id --output result.json
```
