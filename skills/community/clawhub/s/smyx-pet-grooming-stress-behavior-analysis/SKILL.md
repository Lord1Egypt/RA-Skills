---
name: "smyx-pet-grooming-stress-behavior-analysis"
description: "Triggers when a user provides a pet grooming session video URL or file for analysis; supports local video uploads or network URLs to call server-side APIs for stress behavior recognition, detecting struggling, panting, tail tucking and other stress signals during grooming, outputting stress level grading to help groomers intervene promptly. Application scenarios: pet grooming shop cameras, veterinary clinics, pet care services. | 当用户提供宠物美容过程视频URL或文件时，触发本技能进行应激行为分析；支持通过上传本地视频或网络视频URL，调用服务端API进行识别，检测挣扎、张口喘气、尾巴夹紧等应激行为信号，输出应激等级，帮助美容师及时干预，减少宠物应激伤害，提升服务体验。应用场景：宠物美容店摄像头、宠物医院、宠物护理服务。"
version: "1.0.2"
license: "MIT-0"
---

# Pet Grooming Stress Behavior Analysis | 宠物美容过程应激行为识别

Triggers when a user provides a pet grooming session video URL or file for analysis; supports local video uploads or
network URLs to call server-side APIs for stress behavior recognition, detecting struggling, panting, tail tucking and
other stress signals during grooming, outputting stress level grading to help groomers intervene promptly. Application
scenarios: pet grooming shop cameras, veterinary clinics, pet care services.

当用户提供宠物美容过程视频URL或文件时，触发本技能进行应激行为分析；支持通过上传本地视频或网络视频URL，调用服务端API进行识别，检测挣扎、张口喘气、尾巴夹紧等应激行为信号，输出应激等级，帮助美容师及时干预，减少宠物应激伤害，提升服务体验。应用场景：宠物美容店摄像头、宠物医院、宠物护理服务。

## 🎯 AI 角色

假设你是一个专业的宠物行为与应激分析AI。你的任务是基于美容过程的连续视频，检测宠物表现出的应激相关行为，包括身体挣扎幅度、张口喘气频次、尾巴姿态等，综合评估应激等级。不要提供疾病诊断或行为矫正方案，仅客观描述观察到的行为信号。

## 任务目标

- 本 Skill 用于：通过美容过程视频进行宠物应激行为识别分析，获取标准化的行为观察结果和应激等级评估
- 能力包含：视频分析、挣扎行为检测、喘气频次识别、尾巴姿态分析、耳朵/瞳孔状态观察、应激等级评估、美容阶段关联分析、历史趋势对比
- 触发条件:
    1. **默认触发**：当用户提供宠物美容过程视频 URL 或文件需要分析时，默认触发本技能进行应激行为识别
    2. 当用户明确需要进行应激/美容监测时，提及美容应激、宠物挣扎、张口喘气、夹尾巴、应激反应、美容恐惧、洗澡应激、剪毛应激、宠物焦虑等关键词，并且上传了视频文件或者图片文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史应激报告、历史美容应激报告、应激行为分析报告清单、美容应激报告清单、查询历史应激报告、显示所有美容报告、显示应激等级报告，查询健康风险提示报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有美容应激报告"、"
       显示所有应激报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_pet_grooming_stress_behavior_analysis --list --open-id` 参数调用 API
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

**在执行应激行为分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备视频输入**
        - 提供本地视频文件路径或网络视频 URL
        - 确保视频清晰展示宠物在美容过程中的全身状态，能看到身体、尾巴、面部表情，光线充足，无遮挡
        - 建议视频覆盖完整美容过程（洗澡、吹毛、剪毛、修甲等阶段），以获取分阶段应激评估
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行应激行为分析**
        - 调用 `-m scripts.smyx_pet_grooming_stress_behavior_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/bird/other，默认 cat
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示美容应激历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的应激行为观察报告
        -
       包含：挣扎行为检测（挣扎次数、幅度等级）、喘气行为分析（张口喘气频次、持续时段）、尾巴姿态评估（夹紧/低垂/正常摆动）、耳朵状态观察（贴头/竖立/频繁转动）、瞳孔状态（是否放大）、综合应激等级（1-5级）、美容阶段关联（各阶段的应激峰值时段）、历史趋势对比（与近期美容应激等级对比）
        - **重要提示**：仅客观描述观察到的行为信号，不提供疾病诊断或行为矫正方案

## 📊 分析指标说明

| 指标     | 说明                  | 风险参考                                    |
|--------|---------------------|-----------------------------------------|
| 挣扎次数   | 美容过程中宠物身体明显挣脱/扭动的次数 | 0-2次 轻微；3-5次 中度；>5次 重度                  |
| 挣扎幅度   | 每次挣扎时身体扭动的激烈程度      | 轻微（局部挪动）/ 中度（全身扭动）/ 剧烈（猛烈挣脱）            |
| 张口喘气频次 | 非运动状态下的张口快速呼吸频率     | 猫：应激标志；狗：>60次/分钟为异常喘气                   |
| 尾巴姿态   | 尾巴的位置和运动状态          | 夹紧贴腹（高应激）/ 低垂不动（中度）/ 轻微颤抖（轻度）/ 正常摆动（放松） |
| 耳朵状态   | 耳朵的位置和运动            | 贴头紧压（恐惧）/ 频繁转动（警觉）/ 竖立正常（放松）            |
| 综合应激等级 | 基于多指标加权的综合评分        | 1级（放松）→ 5级（极度应激）                        |

## 🚨 应激等级定义

| 等级    | 状态   | 行为特征                 | 建议措施               |
|-------|------|----------------------|--------------------|
| 1级 🟢 | 放松   | 身体松弛，尾巴自然摆动，呼吸平稳     | 正常进行               |
| 2级 🟡 | 轻度紧张 | 偶尔轻微挪动，耳朵频繁转动，呼吸略快   | 安抚语气，放慢节奏          |
| 3级 🟠 | 中度应激 | 明显挣扎（2-3次），尾巴夹紧，张口喘气 | 暂停操作，给予休息和安抚       |
| 4级 🔴 | 重度应激 | 频繁挣扎（>5次），剧烈扭动，持续喘气  | 立即暂停，移至安静环境，评估是否继续 |
| 5级 ⚫  | 极度应激 | 试图逃跑/攻击，瞳孔放大，全身颤抖    | 停止美容操作，隔离冷静，必要时就医  |

## ✂️ 美容阶段关联分析

本技能支持按美容阶段分别评估应激水平，常见阶段包括：

| 阶段    | 常见应激源      | 关注重点      |
|-------|------------|-----------|
| 入笼等待  | 环境噪音、陌生气味  | 喘气、来回踱步   |
| 洗澡    | 水温、水流冲击    | 挣扎幅度、耳朵贴头 |
| 吹毛    | 吹风机噪音、热风   | 喘气频次、颤抖   |
| 剪毛/修型 | 剪刀/推子靠近    | 挣扎次数、尾巴夹紧 |
| 修甲    | 肢体被固定、剪甲触感 | 剧烈挣扎、试图咬人 |
| 全程    | 陌生人接触、束缚感  | 综合应激趋势变化  |

## 资源索引

-

必要脚本：见 [scripts/smyx_pet_grooming_stress_behavior_analysis.py](scripts/smyx_pet_grooming_stress_behavior_analysis.py)(
用途：调用 API 进行应激行为分析，本地文件上传，网络 URL 由 API 服务自动下载)

- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供行为观察参考，不提供疾病诊断或行为矫正方案
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 猫和狗的应激行为表现差异较大，分析时会结合宠物类型调整判定标准
- 短鼻犬种（法斗、巴哥等）张口喘气需区分正常呼吸和应激喘气
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`美容应激行为分析报告-{记录id}`
  形式拼接, "点击查看"列使用 `[🔗 查看报告](reportImageUrl)` 格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 美容应激行为分析报告-20260312172200001 | 猫 | 2026-03-12 17:22:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地美容过程视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_pet_grooming_stress_behavior_analysis --input /path/to/grooming_video.mp4 --pet-type cat --open-id your-open-id

# 分析网络美容过程视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_pet_grooming_stress_behavior_analysis --url https://example.com/grooming_video.mp4 --pet-type cat --open-id your-open-id

# 显示历史分析报告/显示分析报告清单列表/显示历史应激报告（自动触发关键词：查看历史应激报告、历史报告、美容应激报告清单等）
python -m scripts.smyx_pet_grooming_stress_behavior_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_pet_grooming_stress_behavior_analysis --input video.mp4 --pet-type cat --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_pet_grooming_stress_behavior_analysis --input video.mp4 --pet-type cat --open-id your-open-id --output result.json
```
