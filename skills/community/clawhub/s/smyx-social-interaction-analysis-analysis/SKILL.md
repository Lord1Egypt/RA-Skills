---
name: "smyx-social-interaction-analysis-analysis"
description: "AI-powered pet social interaction analysis for multi-pet households. Uses pose recognition and behavior classification to detect cat-cat, dog-dog, and cat-dog interactions—sniffing, chasing, biting, fleeing, hiding, playing—then records duration, frequency, initiator and receiver to generate a social-behavior report. Helps owners understand pet relationships, spot aggression or stress sources, and promote harmonious cohabitation. Scenarios: multi-pet homes, pet boarding centers, pet daycare, animal behavior clinics. | 通过多宠家庭固定摄像头，分析宠物之间（猫-猫、狗-狗、猫-狗等）的互动视频，利用姿态识别和行为分类模型检测嗅闻、追逐、撕咬、逃跑、躲避、玩耍等行为类型，记录每种行为的持续时间、频次以及发起者，生成社交行为报告。帮助主人了解宠物间的社交关系，识别潜在的攻击行为或压力源，促进多宠和谐共处。应用场景：多宠家庭（多猫/多狗/猫狗混养）、宠物寄养中心、宠物日托班、宠物行为诊所。"
version: "1.0.0"
---

# Pet Social Interaction Analysis | 宠物社交行为分析（与其他宠物互动）

AI-powered pet social interaction analysis for multi-pet households. Uses pose recognition and behavior classification to detect cat-cat, dog-dog, and cat-dog interactions—sniffing, chasing, biting, fleeing, hiding, playing—then records duration, frequency, initiator and receiver to generate a social-behavior report. Helps owners understand pet relationships, spot aggression or stress sources, and promote harmonious cohabitation. Scenarios: multi-pet homes, pet boarding centers, pet daycare, animal behavior clinics.

通过多宠家庭固定摄像头，分析宠物之间（猫-猫、狗-狗、猫-狗等）的互动视频，利用姿态识别和行为分类模型检测嗅闻、追逐、撕咬、逃跑、躲避、玩耍等行为类型，记录每种行为的持续时间、频次以及发起者，生成社交行为报告。帮助主人了解宠物间的社交关系，识别潜在的攻击行为或压力源，促进多宠和谐共处。应用场景：多宠家庭（多猫/多狗/猫狗混养）、宠物寄养中心、宠物日托班、宠物行为诊所。

## 🎯 AI 角色

**假设你是一个专业的宠物行为学AI。你的任务是分析多宠家庭固定摄像头的视频，识别宠物之间的互动行为类型（嗅闻、追逐、撕咬、逃跑、躲避、玩耍等），记录每种行为的持续时间、频次、发起者和接收者，输出社交行为报告。不要提供医疗或训练建议，仅输出基于视觉的行为观察结果。**

## 任务目标

- 本 Skill 用于：通过多宠互动视频进行社交行为识别与量化，记录互动类型、参与者、持续时间和频次，输出社交关系报告
- 能力包含：多宠个体识别与追踪、姿态识别、社交行为分类（友好/中性/对抗）、发起者-接收者关系标注、互动时长与频次统计、社交关系评估、潜在冲突预警
- 触发条件:
    1. **默认触发**：当用户提供多宠互动视频需要分析时，默认触发本技能进行社交行为分析
    2. 当用户明确需要多宠社交评估时，提及多猫、多狗、猫狗混养、宠物打架、追逐、霸凌、互动等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史社交报告、历史互动报告、社交行为报告清单、显示所有社交报告、查询互动记录
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有社交报告"、"显示互动记录"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_social_interaction_analysis_analysis --list --open-id` 参数调用 API
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

**在执行社交行为分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备视频输入**
        - 提供本地多宠互动视频文件路径或网络视频 URL
        - 拍摄建议：固定摄像头，视角覆盖宠物主要活动区域，确保画面中可同时看到多只宠物；光线充足，避免遮挡
        - 视频时长：建议 ≥ 1 分钟，较长视频可覆盖更完整的互动模式
        - 支持视频格式：mp4/avi/mov
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行社交行为分析**
        - 调用 `-m scripts.smyx_social_interaction_analysis_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地多宠互动视频文件路径
            - `--url`: 网络多宠互动视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 cat
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示社交行为分析历史报告列表清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的社交行为分析报告
        - 包含：**互动行为清单**（类型、发起者、接收者、持续时间、频次）、**行为分类统计**（友好/中性/对抗占比）、**社交关系评估**（配对关系热力图）、**潜在冲突预警**（如"猫咪A持续追逐猫咪B，可能引发应激，建议增加垂直空间或隔离"）
        - **重要提示**：仅输出基于视觉的行为观察结果，**不提供医疗或训练建议**

## 🐾 互动行为分类体系

### 友好行为 🟢

| 行为 | 特征描述 | 社交含义 |
|------|----------|----------|
| 嗅闻 | 互相嗅闻头部/尾部/身体 | 正常社交问候、信息交换 |
| 蹭头/摩擦 | 头部或身体主动蹭对方 | 亲昵标记、信任表达 |
| 依偎/靠拢 | 身体贴近躺卧或坐在一起 | 亲密关系、安全感 |
| 互相舔毛 | 一方主动舔舐另一方 | 社交联结、等级关系 |
| 玩耍互动 | 交替追逐、扑咬（无攻击性） | 友好社交、精力释放 |

### 中性行为 🟡

| 行为 | 特征描述 | 社交含义 |
|------|----------|----------|
| 平行活动 | 同空间各自活动，无直接互动 | 共存但不亲密 |
| 旁观 | 一方注视另一方但未参与 | 好奇或评估 |
| 绕行 | 一方绕开另一方行走 | 避免冲突的礼貌行为 |
| 资源共享 | 同时使用食盆/猫砂盆但无争抢 | 关系可接受 |

### 对抗行为 🔴

| 行为 | 特征描述 | 社交含义 |
|------|----------|----------|
| 追逐 | 一方持续追赶另一方（非玩耍） | 霸凌、领地驱赶 |
| 撕咬/攻击 | 带攻击意图的扑咬、拍打 | 直接攻击，需干预 |
| 威胁姿态 | 哈气、弓背、低吼、露齿 | 警告、防御 |
| 逃跑 | 一方快速逃离另一方 | 恐惧、被霸凌 |
| 躲避 | 一方长期躲在角落/高处 | 持续受压、缺乏安全感 |

## 🚨 冲突预警分级

| 等级 | 触发条件 | 建议 |
|------|----------|------|
| 🟢 和谐 | 友好行为 > 70%，对抗 < 10% | 社交关系良好，维持现状 |
| 🟡 轻度紧张 | 对抗 10%-25%，偶有追逐 | 增加资源（食盆/猫砂盆/休息区），观察趋势 |
| 🟠 明显冲突 | 对抗 25%-50%，某方持续被追 | 建议增加垂直空间/隔离区，考虑行为咨询 |
| 🔴 严重霸凌 | 对抗 > 50%，某方长期躲避 | ⚠️ 建议立即隔离，寻求专业行为矫正 |

## 💡 多宠家庭环境优化建议参考

| 问题 | 可能原因 | 环境调整方向 |
|------|----------|--------------|
| 食盆争抢 | 资源不足 | 增加食盆数量，分散放置 |
| 猫砂盆冲突 | 猫砂盆太少 | N+1 原则（猫数量+1个砂盆） |
| 追逐/驱赶 | 领地不足 | 增加垂直空间（猫爬架/高架） |
| 躲避不出 | 缺乏安全区 | 设置专属躲避窝/高台 |
| 狗追猫 | 狩猎本能 | 猫狗分离活动区，设置猫专属通道 |

## 资源索引

- 必要脚本：见 [scripts/smyx_social_interaction_analysis_analysis.py](scripts/smyx_social_interaction_analysis_analysis.py)(用途：调用 API 进行社交行为分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景代码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB；建议时长 ≥ 1 分钟
- **画面中需同时包含多只宠物**，单只宠物视频无法进行互动分析
- 摄像头需固定，视角覆盖宠物主要活动区域；移动拍摄可能影响个体追踪与行为识别
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- **分析结果仅供行为观察参考，不提供医疗或训练建议**；严重冲突建议咨询专业行为师
- 玩耍与攻击行为在视觉上存在一定重叠（如玩耍中的扑咬），需结合频次、持续时间和双方反应综合判断
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`社交行为分析报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 社交行为分析报告-20260312172200001 | 猫 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地多宠互动视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_social_interaction_analysis_analysis --input /path/to/multi_pet.mp4 --pet-type cat --open-id your-open-id

# 分析网络多宠互动视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_social_interaction_analysis_analysis --url https://example.com/multi_pet.mp4 --pet-type dog --open-id your-open-id

# 显示历史分析报告/显示报告清单列表（自动触发关键词：查看历史社交报告、互动报告清单等）
python -m scripts.smyx_social_interaction_analysis_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_social_interaction_analysis_analysis --input video.mp4 --pet-type cat --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_social_interaction_analysis_analysis --input video.mp4 --pet-type cat --open-id your-open-id --output result.json
```
