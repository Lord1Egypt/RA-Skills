---
name: "smyx-respiratory-rate-abnormal-detect-analysis"
description: "AI-powered non-contact pet respiratory rate monitoring at rest. Detects thoracic-abdominal motion via a fixed camera, calculates breaths-per-minute, and compares against species/body-size resting norms; triggers early-warning when abnormal (e.g. dog >30 bpm, cat >40 bpm, or <8 bpm). Helps detect cardiopulmonary, respiratory or heat-stress risks early. Scenarios: home night monitoring, animal hospital wards, pet boarding centers. | 通过宠物窝或休息区固定摄像头，在宠物静息状态下分析其胸腹部起伏运动，自动计算呼吸频率（次/分钟），并与该物种/体型的正常静息呼吸范围进行对比；若检测到呼吸过快（如犬>30次/分钟，猫>40次/分钟）或过慢（<8次/分钟），则输出健康预警，建议主人观察或就医。有助于早期发现呼吸系统、心脏或热应激等潜在问题。应用场景：宠物家庭夜间监护、宠物医院住院部、宠物寄养中心。"
version: "1.0.0"
---

# Pet Respiratory Rate Abnormal Detection (Resting) | 宠物呼吸频率异常监测（静息）

AI-powered non-contact pet respiratory rate monitoring at rest. Detects thoracic-abdominal motion via a fixed camera,
calculates breaths-per-minute, and compares against species/body-size resting norms; triggers early-warning when
abnormal (e.g. dog >30 bpm, cat >40 bpm, or <8 bpm). Helps detect cardiopulmonary, respiratory or heat-stress risks
early. Scenarios: home night monitoring, animal hospital wards, pet boarding centers.

通过宠物窝或休息区固定摄像头，在宠物静息状态下分析其胸腹部起伏运动，自动计算呼吸频率（次/分钟），并与该物种/体型的正常静息呼吸范围进行对比；若检测到呼吸过快（如犬>
30次/分钟，猫>40次/分钟）或过慢（<8次/分钟），则输出健康预警，建议主人观察或就医。有助于早期发现呼吸系统、心脏或热应激等潜在问题。应用场景：宠物家庭夜间监护、宠物医院住院部、宠物寄养中心。

## 🎯 AI 角色

**假设你是一个专业的宠物呼吸健康监测AI。你的任务是分析宠物静息状态下的胸腹部视频，检测呼吸周期，计算呼吸频率，并与种属、体型的正常静息呼吸范围进行比对，输出异常预警。不要提供医疗诊断，仅输出呼吸频率数值及超出正常范围的提示。
**

## 任务目标

- 本 Skill 用于：通过宠物静息状态视频进行胸腹部起伏分析，计算静息呼吸频率（次/分钟），与种属/体型正常范围对比，输出异常预警和呼吸波形记录
- 能力包含：胸腹部运动检测、呼吸周期识别、静息呼吸频率计算（RR/min）、种属/体型范围比对、异常预警分级、持续监测与趋势分析
- 触发条件:
    1. **默认触发**：当用户提供宠物静息（睡眠/静卧）状态视频需要分析时，默认触发本技能进行呼吸频率监测
    2. 当用户明确需要呼吸频率监测时，提及呼吸频率、呼吸次数、呼吸异常、静息呼吸、胸腹起伏、夜间监护等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史呼吸监测报告、历史呼吸报告、呼吸频率报告清单、显示所有呼吸报告、查询呼吸异常记录
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有呼吸监测报告"、"
       显示呼吸频率报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_respiratory_rate_abnormal_detect_analysis --list --open-id` 参数调用 API
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

**在执行呼吸频率监测前，必须按以下优先级顺序获取 open-id：**

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
        - 提供本地静息状态视频文件路径或网络视频 URL
        - 拍摄建议：宠物处于**真正的静息状态**（睡眠/静卧 ≥ 1 分钟）；摄像头固定，清晰拍摄胸腹部区域；建议视频时长 ≥ 60
          秒以保证频率统计稳定
        - 避免：宠物正在移动、玩耍、喘气、进食后立即检测
        - 支持视频格式：mp4/avi/mov
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行呼吸频率监测**
        - 调用 `-m scripts.smyx_respiratory_rate_abnormal_detect_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地静息状态视频文件路径
            - `--url`: 网络静息状态视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 cat
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示呼吸频率监测历史报告列表清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看监测结果**
        - 接收结构化的呼吸频率监测报告
        - 包含：**静息呼吸频率（次/分钟）**、**呼吸节律评价**（规律/不规律）、**正常范围对比**（种属/体型）、**异常等级**
          （正常/偏快/偏慢/严重异常）、**呼吸波形数据**（异常时段记录）、**健康建议**（如"呼吸 48 次/分钟，超出成猫静息上限
          40，建议观察并联系兽医"）
        - **重要提示**：仅输出呼吸频率数值与范围比对，不提供医疗诊断或治疗建议

## 📊 静息呼吸频率正常范围参考

| 物种/体型           | 正常静息范围（次/分钟） | 偏快预警 | 严重异常      |
|-----------------|--------------|------|-----------|
| 🐱 成猫           | 16-40        | >40  | >60 或 <8  |
| 🐶 小型犬（<10kg）   | 18-34        | >35  | >50 或 <8  |
| 🐶 中型犬（10-25kg） | 15-30        | >30  | >45 或 <8  |
| 🐶 大型犬（>25kg）   | 10-28        | >30  | >40 或 <8  |
| 🐶/🐱 幼宠（<6月）   | 20-50        | >50  | >70 或 <10 |

> 数据仅供算法基线参考，具体应结合个体体重、年龄、品种（短鼻品种基线略高）和兽医建议判断。

## 🚨 异常预警分级

| 等级      | 触发条件                     | 建议                    |
|---------|--------------------------|-----------------------|
| 🟢 正常   | 在正常范围内，节律规律              | 持续监测                  |
| 🟡 轻度偏快 | 超出上限 10% 以内，节律规律         | 观察是否环境过热或刚结束运动        |
| 🟠 偏快   | 超出上限 10%-30%，持续 5 分钟     | 建议联系兽医评估              |
| 🔴 严重异常 | 超出上限 >30% 或低于下限，或节律明显不规律 | ⚠️ 立即就医检查，警惕心衰、肺炎、热射病 |

## 💡 高风险品种重点关注

| 品种类型               | 重点关注原因                |
|--------------------|-----------------------|
| 短鼻犬猫（英斗、波斯、加菲、巴哥等） | 上呼吸道阻塞，呼吸基线偏高，易出现热应激  |
| 老年宠物（>7岁）          | 心肺功能下降，呼吸异常常为早期心衰信号   |
| 既往心脏病史             | 静息呼吸频率持续 >30/分钟为肺水肿预警 |
| 肥胖宠物               | 胸廓压迫导致呼吸代偿性增快         |

## 资源索引

-

必要脚本：见 [scripts/smyx_respiratory_rate_abnormal_detect_analysis.py](scripts/smyx_respiratory_rate_abnormal_detect_analysis.py)(
用途：调用 API 进行静息呼吸频率监测分析，本地文件上传，网络 URL 由 API 服务自动下载)

- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景代码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB；**建议时长 ≥ 60 秒**以保证呼吸周期统计的稳定性
- **必须为静息状态**（睡眠/静卧 ≥ 1 分钟），活动状态下结果无参考意义
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 监测结果仅供健康参考，**不提供医疗诊断或治疗建议**；持续异常建议及时就医
- 短鼻品种基线呼吸频率偏高，请结合个体差异综合判断
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史监测报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`呼吸频率异常监测报告-{记录id}`
  形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 呼吸频率异常监测报告-20260312172200001 | 猫 | 2026-03-12 17:22:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地静息状态视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_respiratory_rate_abnormal_detect_analysis --input /path/to/sleeping_pet.mp4 --pet-type cat --open-id your-open-id

# 分析网络静息状态视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_respiratory_rate_abnormal_detect_analysis --url https://example.com/sleeping_pet.mp4 --pet-type dog --open-id your-open-id

# 显示历史监测报告/显示报告清单列表（自动触发关键词：查看历史呼吸监测报告、呼吸报告清单等）
python -m scripts.smyx_respiratory_rate_abnormal_detect_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_respiratory_rate_abnormal_detect_analysis --input rest.mp4 --pet-type cat --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_respiratory_rate_abnormal_detect_analysis --input rest.mp4 --pet-type cat --open-id your-open-id --output result.json
```
