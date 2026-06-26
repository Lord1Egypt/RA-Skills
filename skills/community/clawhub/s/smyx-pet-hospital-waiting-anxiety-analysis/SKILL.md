---
name: "smyx-pet-hospital-waiting-anxiety-analysis"
description: "Triggers when a user provides a pet hospital waiting area video URL or file for analysis; supports local video uploads or network URLs to call server-side APIs for anxiety-related behavior recognition, detecting open-mouth panting intensity, limb/torso trembling amplitude, ear-flattening degree and other stress signals, outputting a standardized anxiety level (1-5) to help medical staff identify high-stress pets and prioritize care or comfort (without diagnosing diseases or prescribing treatment). Application scenarios: pet hospital waiting areas, veterinary clinics, pet care institutions. Development reason: optimize visit workflow and reduce stress-related harm. | 当用户提供候诊区宠物视频的URL或文件时，触发本技能进行焦虑行为信号分析；支持通过上传本地视频或网络视频URL，调用服务端API检测张口喘气强度、四肢/躯干颤抖幅度、耳朵后贴程度等应激信号，综合输出标准化焦虑等级（1-5级），帮助医护人员识别高应激宠物并优先安排就诊或安抚（不诊断疾病、不提供治疗方案）。应用场景：宠物医院候诊区、动物诊所、宠物护理机构。"
license: "MIT-0"
---

# Pet Hospital Waiting Anxiety Level Analysis | 宠物医院候诊焦虑等级评估

Triggers when a user provides a pet hospital waiting area video URL or file for analysis; supports local video uploads
or network URLs to call server-side APIs for anxiety-related behavior recognition, detecting open-mouth panting
intensity, limb/torso trembling amplitude, ear-flattening degree and other stress signals, outputting a standardized
anxiety level (1-5) to help medical staff identify high-stress pets and prioritize care or comfort (without diagnosing
diseases or prescribing treatment). Application scenarios: pet hospital waiting areas, veterinary clinics, pet care
institutions. Development reason: optimize visit workflow and reduce stress-related harm.

当用户提供候诊区宠物视频的URL或文件时，触发本技能进行焦虑行为信号分析；支持通过上传本地视频或网络视频URL，调用服务端API检测张口喘气强度、四肢/躯干颤抖幅度、耳朵后贴程度等应激信号，综合输出标准化焦虑等级（1-5级），帮助医护人员识别高应激宠物并优先安排就诊或安抚（不诊断疾病、不提供治疗方案）。应用场景：宠物医院候诊区、动物诊所、宠物护理机构。

## 🎯 AI 角色

**
假设你是一个专业的宠物行为与应激分析AI。你的任务是基于候诊区宠物的连续视频，检测宠物的焦虑相关行为信号，包括张口喘气强度、四肢/躯干颤抖幅度、耳朵后贴程度等，综合评估焦虑等级（1-5级）。不要提供疾病诊断或治疗方案，仅客观描述观察到的行为并输出等级。
**

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过宠物医院候诊区的连续视频识别宠物的应激/焦虑行为信号，输出标准化焦虑等级（1-5
  级）与行为观察清单，辅助医护人员优化就诊优先级与安抚干预
- 能力包含：候诊区视频分析、张口喘气检测、颤抖幅度估算（四肢/躯干）、耳朵姿态识别（直立/侧贴/后贴）、躲藏/僵直行为识别、瞳孔放大与频繁舔鼻等微表情捕捉、综合焦虑等级评分（1-5）、高应激宠物预警
- 触发条件:
    1. **默认触发**：当用户提供宠物医院候诊区视频 URL 或文件需要分析时，默认触发本技能进行焦虑等级评估
    2. 当用户明确需要评估宠物应激/焦虑状态时，提及候诊焦虑、应激评估、焦虑等级、宠物紧张、医院应激、喘气、颤抖、耳朵后贴等关键词，并且上传了视频文件或者图片文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史焦虑评估报告、历史候诊焦虑报告、焦虑等级报告清单、应激报告清单、查询历史焦虑评估、显示所有候诊焦虑报告、显示焦虑诊断报告，查询高应激宠物报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有候诊焦虑报告"、"
       显示所有焦虑评估报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_pet_hospital_waiting_anxiety_analysis --list --open-id` 参数调用 API
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

**在执行候诊焦虑等级评估前，必须按以下优先级顺序获取 open-id：**

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
        - 确保视频清晰拍摄候诊区宠物全身或上半身，能看到头部、耳朵、口鼻与四肢/躯干，光线充足、无遮挡
        - 建议时长 ≥ 15 秒，便于捕捉持续性应激信号（颤抖、喘气节律等）
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行候诊焦虑等级评估**
        - 调用 `-m scripts.smyx_pet_hospital_waiting_anxiety_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 cat
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示候诊焦虑历史评估报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的候诊焦虑等级评估报告
        - 包含：综合焦虑等级（1-5
          级）、张口喘气强度（无/轻/中/重）、颤抖幅度（无/轻微/明显/剧烈）、耳朵姿态（直立/侧贴/完全后贴）、躲藏或僵直行为标记、舔鼻/打哈欠等替代性行为统计、优先就诊建议（仅作为流程参考）
        - **焦虑等级参考标准**：
            - **1 级 平静**：耳朵直立、无喘气、无颤抖，正常张望或趴卧
            - **2 级 轻度紧张**：偶有舔鼻/打哈欠，耳朵略侧，环境警觉
            - **3 级 中度焦虑**：持续轻喘、轻微颤抖、耳朵明显侧贴或半后贴
            - **4 级 高度焦虑**：明显张口喘气、肢体颤抖、耳朵完全后贴、寻找躲藏
            - **5 级 极度应激**：剧烈喘气/嚎叫、全身颤抖、僵直或攻击性姿态，建议立即优先处理
        - **重要提示**：仅客观描述观察到的行为信号与等级，不提供疾病诊断或治疗方案，最终就诊优先级由兽医人员决定

## 资源索引

-

必要脚本：见 [scripts/smyx_pet_hospital_waiting_anxiety_analysis.py](scripts/smyx_pet_hospital_waiting_anxiety_analysis.py)(
用途：调用 API 进行候诊焦虑等级评估，本地文件上传，网络 URL 由 API 服务自动下载)

- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB
- 拍摄角度建议正面或侧前方，覆盖头部与躯干；避免逆光、剧烈晃动或宠物完全被笼具遮挡
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供候诊流程参考，不提供疾病诊断或治疗方案
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 焦虑等级综合多种行为信号估算，宠物个体差异、品种特性（如短鼻犬天然喘气重）可能影响判断，临床决策请结合现场观察
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`候诊焦虑等级评估报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 候诊焦虑等级评估报告-20260312172200001 | 猫 | 2026-03-12 17:22:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地候诊区宠物视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_pet_hospital_waiting_anxiety_analysis --input /path/to/waiting_area_video.mp4 --pet-type cat --open-id your-open-id

# 分析网络候诊区宠物视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_pet_hospital_waiting_anxiety_analysis --url https://example.com/waiting_area_video.mp4 --pet-type cat --open-id your-open-id

# 显示历史分析报告/显示分析报告清单列表/显示历史焦虑评估报告（自动触发关键词：查看历史焦虑评估报告、历史报告、候诊焦虑报告清单等）
python -m scripts.smyx_pet_hospital_waiting_anxiety_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_pet_hospital_waiting_anxiety_analysis --input video.mp4 --pet-type cat --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_pet_hospital_waiting_anxiety_analysis --input video.mp4 --pet-type cat --open-id your-open-id --output result.json
```
