---
name: "stroke-risk-screening-analysis"
description: "Combines TCM facial feature recognition with physiological indicator information to provide early warnings of high-risk stroke conditions such as cerebral infarction and cerebral hemorrhage, and provides lifestyle intervention suggestions and medical guidance. | 脑卒中风险筛查技能，结合中医面部特征辨识结合生理指标信息，提前预警脑梗塞、脑出血等脑卒中高危状态，给出生活干预建议和就医指引"
version: "1.0.5"
license: "MIT-0"
---

# Stroke Risk Screening Analysis Skill | 脑卒中风险筛查分析技能

This feature innovatively integrates the wisdom of TCM "Wang Zhen" (Inspection) with modern physiological monitoring
technology to construct an early warning and intervention system for stroke. By utilizing high-precision cameras to
capture subtle facial characteristics—such as greenish-yellow or purplish-red complexion, swollen tongue body, and mouth
deviation—alongside real-time physiological indicators like blood pressure and Heart Rate Variability (HRV), the system
employs multimodal AI algorithms for comprehensive analysis. It accurately identifies high-risk constitutions, such as
Qi deficiency with phlegm-dampness or Qi and blood stasis, issuing graded warnings prior to a stroke event. Furthermore,
grounded in the theory of TCM syndrome differentiation and treatment, it provides users with personalized lifestyle
interventions (including dietary regulation and cold avoidance) and scientific medical guidance, truly realizing the
leap in health management from "treating existing diseases" to "treating potential diseases" (preventive medicine).

本功能创新性地将中医“望诊”智慧与现代生理监测技术深度融合，旨在构建一套脑卒中早期预警与干预系统。系统通过高精度摄像头捕捉面部微细特征，如面色青黄或紫红、舌体胖大、口角歪斜等中医“面象”与“舌象”信息，结合实时采集的血压、心率变异性等生理指标，利用多模态AI算法进行综合分析。系统能够精准识别气虚痰湿、气血瘀滞等高危体质倾向，在脑卒中发生前发出分级预警，并基于中医辨证施治理论，为用户提供个性化的饮食调理、起居避寒等生活干预建议及科学的就医指引，真正实现从“治已病”到“治未病”的健康管理跨越

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史筛查报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过面部视频图片结合生理指标进行脑卒中风险筛查，获取结构化的脑卒中风险筛查报告
- 能力包含：面部特征辨识、中风高危面相识别、风险等级评估、高危状态预警、生活干预建议生成
- 触发条件:
    1. **默认触发**：当用户提供面部视频或图片需要进行脑卒中风险筛查时，默认触发本技能
    2. 当用户明确需要进行脑卒中风险筛查，提及脑梗、脑出血、中风筛查、脑卒中风险、脑血管风险等关键词，并且上传了面部视频或图片
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史筛查报告、脑卒中报告清单、筛查报告列表、查询历史报告、显示所有筛查报告、脑卒中筛查历史记录，查询脑卒中风险筛查分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有筛查报告"、"
       显示所有脑卒中报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.stroke_risk_screening_analysis --list --open-id` 参数调用 API
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

**在执行脑卒中风险筛查前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、stroke123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询脑卒中筛查报告记录），并询问是否继续

---

- 标准流程:
    1. **准备面部素材**
        - 提供面部视频或清晰正面照片文件路径或网络 URL
        - 确保面部完整露出，光线充足，无遮挡
        - 可选提供血压、血糖、血脂等生理指标辅助提高筛查准确性
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行脑卒中风险筛查**
        - 调用 `-m scripts.stroke_risk_screening_analysis` 处理素材（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频/图片文件路径
            - `--url`: 网络视频/图片 URL 地址（API 服务自动下载）
            - `--media-type`: 媒体类型，可选值：video/image，默认 video
            - `--blood-pressure`: 血压值，格式：收缩压/舒张压，如 140/90（可选）
            - `--blood-sugar`: 空腹血糖值 mmol/L（可选）
            - `--blood-lipid`: 总胆固醇值 mmol/L（可选）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示脑卒中风险筛查历史报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的脑卒中风险筛查报告
        - 包含：基本信息、面部特征辨识、风险等级评估、高危预警、生活干预建议、就医指引

## 资源索引

- 必要脚本：见 [scripts/stroke_risk_screening_analysis.py](scripts/stroke_risk_screening_analysis.py)(用途：调用 API
  进行脑卒中风险筛查，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和媒体格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：视频支持 mp4/avi/mov 格式，图片支持 jpg/png/jpeg 格式，最大 10MB
- 本技能仅作健康风险筛查提示，不能替代专业医学检查和医生诊断，发现高危请及时就医
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史筛查报告清单的时候，从数据 json 中提取字段 reportImageUrl 作为超链接地址，使用 Markdown 表格格式输出，包含"
  报告名称"、"筛查时间"、"风险等级"、"点击查看"四列，其中"报告名称"列使用`脑卒中风险筛查报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 筛查时间 | 风险等级 | 点击查看 |
  |----------|----------|----------|----------|
  | 脑卒中风险筛查报告-20260312172200001 | 2026-03-12 17:22:00 |
  高危 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地面部视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.stroke_risk_screening_analysis --input /path/to/face_video.mp4 --media-type video --open-id openclaw-control-ui

# 分析本地面部照片，附带生理指标（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.stroke_risk_screening_analysis --input /path/to/face.jpg --media-type image --blood-pressure 145/92 --blood-sugar 6.8 --open-id openclaw-control-ui

# 分析网络视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.stroke_risk_screening_analysis --url https://example.com/face_video.mp4 --media-type video --open-id openclaw-control-ui

# 显示历史筛查报告/显示筛查报告清单列表/显示历史脑卒中报告（自动触发关键词：查看历史筛查报告、历史报告、筛查报告清单等）
python -m scripts.stroke_risk_screening_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.stroke_risk_screening_analysis --input video.mp4 --media-type video --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.stroke_risk_screening_analysis --input video.mp4 --media-type video --open-id your-open-id --output result.json
```
