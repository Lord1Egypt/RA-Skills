---
name: "smyx-picky-eater-detection-analysis"
description: "Triggers when a user provides a video of a pet feeding bowl area for analysis; supports local video uploads or network URLs to call server-side APIs for picky-eater behavior detection, identifying behaviors such as pushing kibble out of the bowl, picking only treats/freeze-dried bites, or sniffing then leaving without eating; records frequency and outputs feeding-adjustment suggestions to prevent malnutrition. Application scenarios: smart pet feeders, pet boarding centers, pet hospital inpatient wards. | 当用户提供宠物食盆区域视频时，触发本技能进行选择性拒食行为识别；支持通过上传本地视频或网络视频URL，调用服务端API识别宠物把主粮拨出食盆、只挑拣零食/冻干、嗅闻后离开等挑食行为，记录发生频率，连续异常时输出喂养调整建议，预防营养不均衡（不诊断疾病）。应用场景：智能喂食器、宠物寄养中心、宠物医院住院部。"
version: "1.0.0"
---

# Pet Picky Eater Detection | 宠物选择性拒食识别

Triggers when a user provides a video of a pet feeding bowl area for analysis; supports local video uploads or network URLs to call server-side APIs for picky-eater behavior detection, identifying behaviors such as pushing kibble out of the bowl, picking only treats/freeze-dried bites, or sniffing then leaving without eating; records frequency and outputs feeding-adjustment suggestions to prevent malnutrition. Application scenarios: smart pet feeders, pet boarding centers, pet hospital inpatient wards.

当用户提供宠物食盆区域视频时，触发本技能进行选择性拒食行为识别；支持通过上传本地视频或网络视频URL，调用服务端API识别宠物把主粮拨出食盆、只挑拣零食/冻干、嗅闻后离开等挑食行为，记录发生频率，连续异常时输出喂养调整建议，预防营养不均衡（不诊断疾病）。应用场景：智能喂食器、宠物寄养中心、宠物医院住院部。

## 🎯 AI 角色

**你是一个专业的宠物行为与营养管理AI。你的任务是分析智能喂食器拍摄的食盆区域视频（从投食开始至宠物离开），检测宠物是否存在"选择性拒食"行为，即主动将主粮颗粒拨出食盆、只挑拣其中的零食/冻干食用、或者嗅闻后拒绝进食。不要提供医疗建议，仅输出基于视觉的行为分析结果。**

## 任务目标

- 本 Skill 用于：通过食盆区域视频识别宠物选择性拒食行为，记录挑食频率、主粮/零食摄入比例，连续异常时输出喂养调整建议，帮助主人及早发现挑食问题，避免营养不均衡
- 能力包含：视频分析、宠物嘴部/爪部动作识别、主粮与零食颗粒区分、拨食/挑食/嗅闻离开行为检测、进食时长统计、行为发生频率统计、连续异常判定、喂养调整建议输出
- 触发条件:
    1. **默认触发**：当用户提供食盆区域视频 URL 或文件需要分析时，默认触发本技能进行选择性拒食识别
    2. 当用户明确需要进行宠物挑食监测时，提及挑食、拒食、不吃主粮、只吃零食、拨食、嗅闻离开、宠物喂食器、营养不均衡等关键词，并且上传了视频文件或者图片文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史挑食报告、历史拒食识别报告、挑食行为报告清单、拒食识别报告清单、查询历史挑食报告、显示所有拒食识别报告、查询喂养行为报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有挑食报告"、"显示拒食识别报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_picky_eater_detection_analysis --list --open-id` 参数调用 API
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

**在执行选择性拒食识别前，必须按以下优先级顺序获取 open-id：**

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
        - 提供本地视频文件路径或网络视频 URL
        - 确保视频清晰展示食盆区域，从投食开始拍摄至宠物离开，光线充足，主粮与零食颗粒可视觉区分
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行选择性拒食识别**
        - 调用 `-m scripts.smyx_picky_eater_detection_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/bird/other，默认 cat
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示选择性拒食识别历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的选择性拒食行为报告
        - 包含：进食时长、嗅闻次数、拨食次数（将主粮拨出食盆）、挑食行为（只挑零食/冻干）、嗅闻后离开判定、主粮/零食摄入比例估计、挑食程度分级（轻度/中度/重度）、喂养调整建议（更换主粮品牌、减少零食投喂量、尝试拌食诱食等）
        - **重要提示**：仅客观描述观察到的进食行为，不提供疾病诊断或治疗建议

## 资源索引

- 必要脚本：见 [scripts/smyx_picky_eater_detection_analysis.py](scripts/smyx_picky_eater_detection_analysis.py)(用途：调用 API 进行选择性拒食识别分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制，场景码 SMYX_PICKY_EATER_DETECTION_ANALYSIS)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供喂养行为参考，不提供疾病诊断或治疗建议
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`选择性拒食识别报告-{记录id}`形式拼接, "点击查看"
  列使用 `[🔗 查看报告](reportImageUrl)` 格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 选择性拒食识别报告-20260312172200001 | 猫 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地食盆区域视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_picky_eater_detection_analysis --input /path/to/feeder_video.mp4 --pet-type cat --open-id your-open-id

# 分析网络食盆区域视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_picky_eater_detection_analysis --url https://example.com/feeder_video.mp4 --pet-type cat --open-id your-open-id

# 显示历史分析报告/显示分析报告清单列表/显示历史挑食识别报告（自动触发关键词：查看历史挑食报告、历史报告、拒食识别报告清单等）
python -m scripts.smyx_picky_eater_detection_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_picky_eater_detection_analysis --input video.mp4 --pet-type cat --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_picky_eater_detection_analysis --input video.mp4 --pet-type cat --open-id your-open-id --output result.json
```
