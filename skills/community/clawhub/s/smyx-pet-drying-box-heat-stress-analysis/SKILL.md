---
name: "smyx-pet-drying-box-heat-stress-analysis"
description: "Triggers when a user provides a pet drying box area video URL or file for analysis; supports local video uploads or network URLs to call server-side APIs for pet heat stress signal detection, analyzing open-mouth panting intensity, tongue color (pink/cyanotic), and body movement frequency to identify early heat stress signals, outputting risk levels and supporting auto-cooling or stopping drying. Application scenarios: pet drying boxes, pet grooming stores, pet hospitals. Development reason: prevent heatstroke and improve safety. | 当用户提供宠物烘干箱区域的视频URL或文件时，触发本技能进行烘干箱内热应激预警分析；支持通过上传本地视频或网络视频URL，调用服务端API进行热应激信号识别，分析张口喘气强度、舌体颜色（粉红/紫绀）、身体移动频率，识别热应激早期信号，输出风险等级，支持自动降温或停止烘干。应用场景：宠物烘干箱、宠物美容店、宠物医院。"
version: "1.0.2"
license: "MIT-0"
---

# Pet Drying Box Heat Stress Analysis | 宠物烘干箱内热应激预警

Triggers when a user provides a pet drying box area video URL or file for analysis; supports local video uploads or
network URLs to call server-side APIs for pet heat stress signal detection, analyzing open-mouth panting intensity,
tongue color (pink/cyanotic), and body movement frequency to identify early heat stress signals, outputting risk levels
and supporting auto-cooling or stopping drying. Application scenarios: pet drying boxes, pet grooming stores, pet
hospitals. Development reason: prevent heatstroke and improve safety.

当用户提供宠物烘干箱区域的视频URL或文件时，触发本技能进行烘干箱内热应激预警分析；支持通过上传本地视频或网络视频URL，调用服务端API进行热应激信号识别，分析张口喘气强度、舌体颜色（粉红/紫绀）、身体移动频率，识别热应激早期信号，输出风险等级，支持自动降温或停止烘干。应用场景：宠物烘干箱、宠物美容店、宠物医院。

## 🎯 AI 角色

*
*假设你是一个专业的宠物热应激监测AI。你的任务是基于宠物烘干箱内的连续视频，检测宠物的热应激相关行为信号，包括张口喘气强度、舌体颜色（粉红/紫绀）、身体移动频率等，综合评估热应激风险等级，并给出干预建议（如自动降温、停止烘干）。不要提供疾病诊断，仅客观描述观察到的生理和行为迹象。
**

## 任务目标

- 本 Skill 用于：通过烘干箱内的视频监测宠物热应激信号，获取标准化的观察结果和风险等级预警
- 能力包含：视频分析、张口喘气强度识别、舌体颜色（粉红/紫绀）分析、身体移动频率监测、综合风险等级评估、降温/停止烘干干预建议
- 触发条件:
    1. **默认触发**：当用户提供宠物烘干箱内视频 URL 或文件需要分析时，默认触发本技能进行热应激预警分析
    2. 当用户明确需要进行烘干箱内宠物监测时，提及烘干箱、宠物烘干、热应激、张口喘气、舌体紫绀、宠物中暑、烘干安全等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史热应激报告、历史烘干箱报告、热应激预警报告清单、查询热应激报告、显示所有烘干箱报告、显示宠物热应激报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有烘干箱报告"、"
       显示所有热应激报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_pet_drying_box_heat_stress_analysis --list --open-id` 参数调用 API
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

**在执行热应激预警分析前，必须按以下优先级顺序获取 open-id：**

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
        - 确保视频清晰展示烘干箱内宠物头部、口腔/舌部和整体身体姿态，光线充足，无遮挡
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行热应激预警分析**
        - 调用 `-m scripts.smyx_pet_drying_box_heat_stress_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 cat
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示烘干箱热应激预警视频历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的热应激信号观察报告
        - 包含：张口喘气强度（无/轻度/中度/重度）、舌体颜色评估（粉红/淡白/紫绀）、身体移动频率（静止/正常/烦躁/挣扎）、综合热应激风险等级（低/中/高/紧急）、干预建议（自动降温、停止烘干、人工干预）
        - **重要提示**：仅客观描述观察到的现象，不提供疾病诊断或治疗建议

## 资源索引

-
必要脚本：见 [scripts/smyx_pet_drying_box_heat_stress_analysis.py](scripts/smyx_pet_drying_box_heat_stress_analysis.py)(
用途：调用 API 进行烘干箱内热应激信号分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供烘干安全参考，不提供疾病诊断或治疗建议
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 检测到高风险或紧急级别热应激信号时，应提示用户立即停止烘干、降低温度、开盖通风并观察宠物状态
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`烘干箱热应激预警报告-{记录id}`
  形式拼接, "点击查看"列使用 `[🔗 查看报告](reportImageUrl)` 格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 烘干箱热应激预警报告-20260312172200001 | 猫 | 2026-03-12 17:22:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地烘干箱视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_pet_drying_box_heat_stress_analysis --input /path/to/drying_box_video.mp4 --pet-type cat --open-id your-open-id

# 分析网络烘干箱视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_pet_drying_box_heat_stress_analysis --url https://example.com/drying_box_video.mp4 --pet-type cat --open-id your-open-id

# 显示历史分析报告/显示分析报告清单列表/显示历史热应激报告（自动触发关键词：查看历史热应激报告、历史报告、烘干箱报告清单等）
python -m scripts.smyx_pet_drying_box_heat_stress_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_pet_drying_box_heat_stress_analysis --input video.mp4 --pet-type cat --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_pet_drying_box_heat_stress_analysis --input video.mp4 --pet-type cat --open-id your-open-id --output result.json
```
