---
name: "smyx-vaccination-reminder-analysis"
description: "Triggers when a user provides a pet facial image or video URL/file for vaccination reminder analysis; uses AI facial recognition to confirm pet identity, automatically queries the linked vaccination records (last dose date, vaccine type) from the hospital management database, and compares with current date. When the gap since last vaccination exceeds 11 months (or the preset reminder cycle), outputs a due/overdue reminder and suggests re-vaccination. Helps pet hospitals automate client management, raise vaccination coverage and avoid missed doses. Application: hospital front-desk registration, boarding center check-in, pet insurance underwriting. Does NOT provide medical advice — only returns database-comparison results. | 当用户提供宠物面部图像或视频URL/文件时，触发本技能进行疫苗到期提醒分析；利用AI面部识别确认宠物个体身份，自动关联数据库中该宠物的疫苗接种记录（上次接种日期、疫苗类型）并与当前日期比对；若距离上次接种超过11个月（或预设的提醒周期），输出到期/逾期提醒，并建议尽快补种。该技能可帮助宠物医院实现自动化客户管理、提升疫苗接种率、防止漏种。应用场景：宠物医院前台登记、宠物寄养中心入住检查、宠物保险核保。仅输出基于数据库比对的结果，不提供医疗建议。"
version: "1.0.0"
---

# Pet Vaccination Reminder (Facial Recognition) | 宠物疫苗接种到期提醒（面部识别）

Triggers when a user provides a pet facial image or video URL/file for vaccination reminder analysis; uses AI facial recognition to confirm pet identity, automatically queries the linked vaccination records (last dose date, vaccine type) from the hospital management database, and compares with current date. When the gap since last vaccination exceeds 11 months (or the preset reminder cycle), outputs a due/overdue reminder and suggests re-vaccination. Helps pet hospitals automate client management, raise vaccination coverage and avoid missed doses. Application: hospital front-desk registration, boarding center check-in, pet insurance underwriting. Does NOT provide medical advice — only returns database-comparison results.

当用户提供宠物面部图像或视频URL/文件时，触发本技能进行疫苗到期提醒分析；利用AI面部识别确认宠物个体身份，自动关联数据库中该宠物的疫苗接种记录（上次接种日期、疫苗类型）并与当前日期比对；若距离上次接种超过11个月（或预设的提醒周期），输出到期/逾期提醒，并建议尽快补种。该技能可帮助宠物医院实现自动化客户管理、提升疫苗接种率、防止漏种。应用场景：宠物医院前台登记、宠物寄养中心入住检查、宠物保险核保。仅输出基于数据库比对的结果，不提供医疗建议。


## 🎯 AI 角色

**你是一个专业的宠物医疗管理AI。你的任务是接收一张宠物面部图像或视频，通过面部特征匹配识别宠物身份（个体ID），然后查询本地或云端数据库获取该宠物的最近一次疫苗接种记录（疫苗类型、接种日期、有效期类型/周期），并与当前日期进行比较。若距离上次接种超过建议的间隔周期（默认犬猫核心疫苗为11个月），则输出到期提醒。不要提供医疗建议，仅输出基于数据库比对的结果。**

## 任务目标

- 本 Skill 用于：通过宠物面部图像识别个体身份，关联其疫苗接种档案，自动判断是否到期/逾期，输出标准化的到期提醒结果
- 能力包含：宠物面部检测与特征匹配、个体身份识别、疫苗档案查询、上次接种日期与当前日期比对、到期/逾期状态判定、补种建议输出
- 触发条件:
    1. **默认触发**：当用户提供宠物面部图像/视频 URL 或文件需要核对疫苗到期情况时，默认触发本技能进行疫苗到期提醒分析
    2. 当用户明确需要核对疫苗接种时，提及疫苗到期、补种、疫苗提醒、漏种、核心疫苗、狂犬疫苗、年度疫苗等关键词，并且上传了宠物面部图像或视频
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史疫苗提醒报告、历史疫苗记录、疫苗提醒清单、查询疫苗到期记录、显示所有疫苗提醒报告、显示疫苗到期诊断报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有疫苗报告"、"显示历史疫苗提醒"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_vaccination_reminder_analysis --list --open-id` 参数调用 API 查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行疫苗到期提醒分析前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备宠物面部输入**
        - 提供本地宠物面部图像/视频文件路径或网络 URL
        - 确保画面清晰展示宠物正面面部，光线充足，无大幅遮挡
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行疫苗到期提醒分析**
        - 调用 `-m scripts.smyx_vaccination_reminder_analysis` 处理面部输入（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地宠物面部图像/视频文件路径
            - `--url`: 网络面部图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 dog
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示疫苗到期提醒历史报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的疫苗到期提醒报告
        - 包含：宠物个体识别结果（宠物ID、姓名、品种）、最近接种记录（疫苗类型、接种日期）、当前日期、距上次接种天数、状态（在有效期内/即将到期/已过期）、补种建议
        - **重要提示**：仅输出基于数据库比对的客观结果，不提供具体医疗建议

## 资源索引

- 必要脚本：见 [scripts/smyx_vaccination_reminder_analysis.py](scripts/smyx_vaccination_reminder_analysis.py)（用途：调用 API 进行面部识别 + 疫苗记录比对分析，本地文件上传，网络 URL 由 API 服务自动下载）
- 配置文件：见 [scripts/config.py](scripts/config.py)（用途：配置 API 地址、默认参数和文件格式限制）
- 领域参考：见 [references/api_doc.md](references/api_doc.md)（何时读取：需要了解 API 接口详细规范和错误码时）

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 输入要求：支持 jpg/png 图像或 mp4/avi/mov 视频格式，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 默认核心疫苗提醒周期为 11 个月，可后续在 API 端按疫苗类型自定义
- 若面部识别未能匹配到已登记的宠物个体，输出"未识别到已登记宠物，请先建档"
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown 表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`宠物疫苗到期提醒报告-{记录id}`形式拼接, "点击查看"列使用 `[🔗 查看报告](reportImageUrl)` 格式的超链接，用户点击即可直接跳转到对应的完整报告页面
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 宠物疫苗到期提醒报告-20260312172200001 | 狗 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地宠物面部图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_vaccination_reminder_analysis --input /path/to/pet_face.jpg --pet-type dog --open-id your-open-id

# 分析网络宠物面部图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_vaccination_reminder_analysis --url https://example.com/pet_face.mp4 --pet-type dog --open-id your-open-id

# 显示历史分析报告/疫苗提醒历史清单（自动触发关键词：查看历史疫苗报告、疫苗提醒清单等）
python -m scripts.smyx_vaccination_reminder_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_vaccination_reminder_analysis --input pet_face.jpg --pet-type dog --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_vaccination_reminder_analysis --input pet_face.jpg --pet-type dog --open-id your-open-id --output result.json
```
