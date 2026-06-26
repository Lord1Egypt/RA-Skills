---
name: "smyx-pet-carrier-respiratory-rate-analysis"
description: "Triggers when a user provides a video of a pet inside an airline carrier/crate for analysis; supports local uploads or network URLs to call server-side APIs for respiratory rate monitoring, detecting chest/abdomen rise-fall cycles to calculate resting breathing frequency (breaths/min), and outputting an alert when the rate exceeds the safety threshold (>40 bpm), helping early detection of hypoxia, anxiety, or health abnormalities during pet air transport to reduce transport risks (without diagnosing diseases). Application scenarios: pet airline carriers, pet cargo transport, long-distance pet transport. | 当用户提供航空箱内宠物视频时，触发本技能进行呼吸频率监测分析；支持通过上传本地视频或网络视频URL，调用服务端API检测胸腹起伏运动，计算静息呼吸频率（次/分），超过安全阈值（>40次/分）时输出预警，帮助托运过程中早期发现缺氧、焦虑或健康异常，降低托运风险（不诊断疾病）。应用场景：宠物航空箱、宠物托运、宠物长途运输。"
version: "1.0.0"
license: "MIT-0"
---

# Pet Carrier Respiratory Rate Analysis | 宠物航空箱内呼吸频率监测

Triggers when a user provides a video of a pet inside an airline carrier/crate for analysis; supports local uploads or
network URLs to call server-side APIs for respiratory rate monitoring, detecting chest/abdomen rise-fall cycles to
calculate resting breathing frequency (breaths/min), and outputting an alert when the rate exceeds the safety
threshold (>40 bpm), helping early detection of hypoxia, anxiety, or health abnormalities during pet air transport to
reduce transport risks (without diagnosing diseases). Application scenarios: pet airline carriers, pet cargo transport,
long-distance pet transport.

当用户提供航空箱内宠物视频时，触发本技能进行呼吸频率监测分析；支持通过上传本地视频或网络视频URL，调用服务端API检测胸腹起伏运动，计算静息呼吸频率（次/分），超过安全阈值（>
40次/分）时输出预警，帮助托运过程中早期发现缺氧、焦虑或健康异常，降低托运风险（不诊断疾病）。应用场景：宠物航空箱、宠物托运、宠物长途运输。

## 🎯 AI 角色

**你是一个专业的宠物健康监测AI。你的任务是基于航空箱内宠物的连续视频，检测宠物的胸腹起伏运动，计算静息呼吸频率，并与安全阈值对比，输出标准化呼吸监测结果。不要提供疾病诊断或治疗建议，仅客观描述呼吸频率数据及异常提醒。
**

## 任务目标

- 本 Skill 用于：通过航空箱内宠物视频进行呼吸频率监测分析，获取标准化的呼吸频率数据和异常预警，帮助托运过程中早期发现缺氧、焦虑或健康异常
- 能力包含：视频分析、胸腹起伏周期检测、静息呼吸频率计算（次/分）、安全阈值对比（>40次/分预警）、呼吸节律异常检测、缺氧/焦虑风险提示
- 触发条件:
    1. **默认触发**：当用户提供航空箱内宠物视频 URL 或文件需要分析时，默认触发本技能进行呼吸频率监测
    2. 当用户明确需要进行宠物呼吸监测时，提及航空箱、托运、呼吸频率、喘息、缺氧、呼吸急促、胸腹起伏、宠物运输等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史呼吸报告、历史航空箱监测报告、呼吸频率报告清单、查询呼吸监测记录、显示所有托运监测报告、显示呼吸频率监测报告，查询宠物运输健康风险报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有呼吸报告"、"
       显示所有航空箱监测报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_pet_carrier_respiratory_rate_analysis --list --open-id` 参数调用 API
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

**在执行呼吸频率监测分析前，必须按以下优先级顺序获取 open-id：**

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
        - 确保视频清晰展示航空箱内宠物的胸腹区域，光线充足（建议箱内补光），宠物身体可见且无明显遮挡
        - 建议视频时长 ≥ 30 秒，以确保呼吸周期采样充分
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行呼吸频率监测分析**
        - 调用 `-m scripts.smyx_pet_carrier_respiratory_rate_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 dog
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示航空箱呼吸频率历史分析报告列表清单（可输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的呼吸频率监测报告
        - 包含：静息呼吸频率（次/分）、呼吸节律分析（规律/不规律/浅快/深慢）、安全阈值对比（正常范围 ≤ 40次/分、偏快 41~
          60次/分、急促 > 60次/分）、异常特征标记（呼吸暂停、喘息、张口呼吸）、缺氧/焦虑风险提示
        - **重要提示**：仅客观描述观察到的呼吸频率数据和异常提醒，不提供疾病诊断或治疗建议

## 呼吸频率安全参考阈值

| 状态      | 狗（次/分） | 猫（次/分） | 说明             |
|---------|--------|--------|----------------|
| 正常静息    | 10~30  | 20~30  | 安静放松状态         |
| 偏快（关注）  | 31~40  | 31~40  | 可能紧张/环境温度高     |
| ⚠️ 异常预警 | >40    | >40    | 缺氧/焦虑/疼痛风险，需关注 |
| 🚨 急促危险 | >60    | >60    | 高度危险，建议紧急处理    |

> 注：以上阈值仅供参考，幼宠/老龄宠/短鼻犬种（法斗、巴哥等）呼吸频率天然偏高，需结合品种特征综合判断。

## 资源索引

-
必要脚本：见 [scripts/smyx_pet_carrier_respiratory_rate_analysis.py](scripts/smyx_pet_carrier_respiratory_rate_analysis.py)(
用途：调用 API 进行呼吸频率监测分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景代码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB，建议时长 ≥ 30 秒
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供健康参考，不提供疾病诊断或治疗建议
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 短鼻犬种（法斗、巴哥、英斗等）静息呼吸频率天然偏高，AI 角色在输出结果时需提醒用户结合品种特征判断
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 `reportImageUrl` 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`航空箱呼吸频率监测报告-{记录id}`形式拼接, "
  点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 航空箱呼吸频率监测报告-20260522000800001 | 狗 | 2026-05-22 00:08:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地航空箱内宠物视频（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_pet_carrier_respiratory_rate_analysis --input /path/to/carrier_video.mp4 --pet-type dog --open-id your-open-id

# 分析网络航空箱内宠物视频（以下只是示例，禁止直接使用 openclaw-control-ui 作为 open-id）
python -m scripts.smyx_pet_carrier_respiratory_rate_analysis --url https://example.com/carrier_video.mp4 --pet-type dog --open-id your-open-id

# 显示历史分析报告清单（自动触发关键词：查看历史呼吸报告、航空箱监测报告清单等）
python -m scripts.smyx_pet_carrier_respiratory_rate_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_pet_carrier_respiratory_rate_analysis --input carrier_video.mp4 --pet-type dog --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_pet_carrier_respiratory_rate_analysis --input carrier_video.mp4 --pet-type dog --open-id your-open-id --output result.json
```
