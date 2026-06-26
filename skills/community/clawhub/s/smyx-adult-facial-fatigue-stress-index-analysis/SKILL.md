---
name: "smyx-adult-facial-fatigue-stress-index-analysis"
description: "Using a smart mirror or fixed camera, the system analyzes high-resolution adult facial images or short videos to detect physiological features such as under-eye bag area (puffiness/shadow under the lower eyelid), dark-circle grayscale (darkness around the eyes), mouth-corner drop angle (angle between corner of mouth and horizontal), and glabellar frown lines (vertical lines between the brows), and computes a comprehensive fatigue/stress index (0-100). The skill supports workplace health management and personal state monitoring, helping users understand their energy level. Application scenarios: smart mirrors, office health displays, smartphone selfie apps, personal health management. The system auto-evaluates daily or per use, outputs the fatigue index, and suggests rest, hydration, or relaxation. Skill features: modern workers commonly face fatigue and stress that often go unnoticed. Non-contact facial analysis lets individuals and enterprises understand the state in time, adjust work rhythm, and prevent overwork. Can be integrated into smart mirrors, attendance terminals, or health management systems as a practical employee-care tool. | 通过智能镜子或固定摄像头，分析成人面部的高清图像或视频，检测眼袋面积（下眼睑区域的浮肿或阴影面积）、黑眼圈灰度（眼眶区域的暗沉程度）、嘴角下垂角度（口角与水平线的夹角）以及皱眉纹（眉间川字纹）等生理特征，综合计算疲劳/压力指数（0-100分）。该技能可用于职场健康管理、个人状态监测，辅助了解自身精力水平。应用场景：智能镜子、办公室健康屏、手机APP自拍、个人健康管理。系统每日或每次使用时自动评估，输出疲劳指数，并建议休息、补水或进行放松训练。技能特点：现代职场人普遍面临疲劳和压力问题，但常被忽视。通过非接触式面部分析，可帮助个人和企业及时了解状态，调整工作节奏，预防过劳。该技能可集成到智能镜子、考勤终端或健康管理系统中，成为员工关怀的实用工具。"
version: "1.0.0"
---

# Adult Facial Fatigue / Stress Index | 成人面部疲劳/压力指数分析

Using a smart mirror or fixed camera, the system analyzes high-resolution adult facial images or short videos to detect physiological features such as under-eye bag area (puffiness/shadow under the lower eyelid), dark-circle grayscale (darkness around the eyes), mouth-corner drop angle (angle between corner of mouth and horizontal), and glabellar frown lines (vertical lines between the brows), and computes a comprehensive fatigue/stress index (0-100). The skill supports workplace health management and personal state monitoring, helping users understand their energy level. Application scenarios: smart mirrors, office health displays, smartphone selfie apps, personal health management. The system auto-evaluates daily or per use, outputs the fatigue index, and suggests rest, hydration, or relaxation. Skill features: modern workers commonly face fatigue and stress that often go unnoticed. Non-contact facial analysis lets individuals and enterprises understand the state in time, adjust work rhythm, and prevent overwork. Can be integrated into smart mirrors, attendance terminals, or health management systems as a practical employee-care tool.

通过智能镜子或固定摄像头，分析成人面部的高清图像或视频，检测眼袋面积（下眼睑区域的浮肿或阴影面积）、黑眼圈灰度（眼眶区域的暗沉程度）、嘴角下垂角度（口角与水平线的夹角）以及皱眉纹（眉间川字纹）等生理特征，综合计算疲劳/压力指数（0-100分）。该技能可用于职场健康管理、个人状态监测，辅助了解自身精力水平。应用场景：智能镜子、办公室健康屏、手机APP自拍、个人健康管理。系统每日或每次使用时自动评估，输出疲劳指数，并建议休息、补水或进行放松训练。技能特点：现代职场人普遍面临疲劳和压力问题，但常被忽视。通过非接触式面部分析，可帮助个人和企业及时了解状态，调整工作节奏，预防过劳。该技能可集成到智能镜子、考勤终端或健康管理系统中，成为员工关怀的实用工具。

## 🎯 AI 角色

**假设你是一个专业的个人健康状态分析 AI。你的任务是分析成人面部图像或短视频，检测眼袋面积、黑眼圈灰度、嘴角下垂程度以及眉间皱纹等疲劳相关特征，综合输出疲劳/压力指数（0-100）。不要提供医疗诊断或临床压力评估，仅输出基于面部视觉的客观评分与方向性建议。**

## 任务目标

- 本 Skill 用于：基于成人正面面部图像或短视频，量化眼袋 / 黑眼圈 / 嘴角下垂 / 眉间川字纹等疲劳特征，综合输出 0-100 疲劳/压力指数与等级
- 能力包含：正面面部检测与对齐、眼袋面积估算、黑眼圈灰度分析、嘴角下垂角度、眉间川字纹评分、整体肌肤暗沉度（参考）、综合疲劳/压力指数（0-100）、等级判定（good / mild_fatigue / moderate_stress / high_stress）、主要贡献特征排序、方向性建议提示
- 触发条件:
    1. **默认触发**：当用户提供成人正面面部图像或短视频 URL/文件需要分析时，默认触发本技能进行疲劳/压力指数评估
    2. 当用户明确提及面部疲劳、压力指数、眼袋、黑眼圈、嘴角下垂、皱眉纹、川字纹、智能镜子健康、过劳预防、面部状态评估等关键词，并且上传了图像/视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看疲劳压力历史报告、面部疲劳报告清单、疲劳指数报告清单、查询历史疲劳指数、显示所有疲劳压力报告、显示个人状态诊断报告，查询疲劳压力建议清单
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有疲劳压力报告"、"
       显示所有面部疲劳报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_adult_facial_fatigue_stress_index_analysis --list --open-id` 参数调用 API
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

**在执行成人面部疲劳/压力指数分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备成人正面面部图像/短视频输入**
        - 提供本地正面面部图像/短视频路径或网络 URL
        - 推荐正面、平视、清晰、光照均匀；单图或 3-10 秒短视频均可
        - 拍摄距离 30-80 cm，五官区域清晰，避免厚重妆容或重度滤镜
        - 可选附带：被检测人姓名、近期睡眠/工作时长、是否处于经期/感冒等可能影响面部特征的状况
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行成人面部疲劳/压力指数分析**
        - 调用 `-m scripts.smyx_adult_facial_fatigue_stress_index_analysis` 处理输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地成人正面面部图像/短视频文件路径
            - `--url`: 网络成人正面面部图像/短视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 类别标识，成人个人健康状态场景默认 `other`
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示成人面部疲劳/压力指数历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的面部疲劳/压力指数报告
        - 包含：是否检测到面部（face_detected）、各项面部特征数值（feature_metrics：eye_bag_area / dark_circle_grayscale / mouth_corner_drop_deg / glabellar_frown_lines_score / skin_dullness_score）、综合疲劳/压力指数（fatigue_stress_score，0-100）、等级（fatigue_stress_level：good / mild_fatigue / moderate_stress / high_stress）、主要贡献特征排序（top_contributing_features）、方向性建议（suggestion_hint：如"建议补水休息"、"今晚早睡"、"短暂深呼吸/放松训练"）、医疗复核提示
        - **重要提示**：仅输出基于面部视觉的客观评分与方向性建议，不提供医学诊断或临床压力评估；如长期高分伴明显躯体症状，请咨询专业医生

## 资源索引

- 必要脚本：见 [scripts/smyx_adult_facial_fatigue_stress_index_analysis.py](scripts/smyx_adult_facial_fatigue_stress_index_analysis.py)(
  用途：调用 API 进行成人面部疲劳/压力指数分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范、疲劳特征定义/分级和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 jpg/png 图像或 mp4/avi/mov 短视频，最大 10MB；建议正面、光照均匀、无重度滤镜
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 评分结果仅作为个人状态参考，单次评分受光照/妆容影响较大，建议结合连续趋势查看；不替代专业医生评估
- 隐私合规：面部数据涉及生物特征隐私，使用前需取得本人同意，并妥善保管/加密相关图像
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"疲劳指数"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`面部疲劳压力指数报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 疲劳指数 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 面部疲劳压力指数报告-20260312172200001 | 68 / moderate_stress（眼袋+黑眼圈） | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地正面面部图像（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_adult_facial_fatigue_stress_index_analysis --input /path/to/selfie.jpg --open-id your-open-id

# 分析网络面部图像/短视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_adult_facial_fatigue_stress_index_analysis --url https://example.com/selfie.jpg --open-id your-open-id

# 显示历史疲劳/压力指数报告（自动触发关键词：查看疲劳压力历史报告、面部疲劳报告清单等）
python -m scripts.smyx_adult_facial_fatigue_stress_index_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_adult_facial_fatigue_stress_index_analysis --input face.jpg --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_adult_facial_fatigue_stress_index_analysis --input face.jpg --open-id your-open-id --output result.json
```
