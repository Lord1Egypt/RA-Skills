---
name: "smyx-pet-body-condition-score-3d-analysis"
description: "Triggers when a user provides multi-angle pet videos (standing/side/top-down view) URL or files for analysis; supports local video uploads or network URLs to call server-side APIs for 3D body shape reconstruction and Body Condition Score (BCS, 1-9) evaluation, classifying body type as underweight, ideal, or overweight/obese, outputting standardized observation data (without diagnosing diseases or prescribing treatment). Application scenarios: smart feeders, pet cameras, pet health management platforms. Development reason: early warning for obesity-related diseases, scientific weight management. | 当用户提供宠物多角度视频（站立、侧身、俯视）的URL或文件时，触发本技能进行3D体型构建与BCS体况评分；支持通过上传本地视频或网络视频URL，调用服务端API进行体态分析，自动评估体况评分（1-9分），判断偏瘦、正常或肥胖，输出标准化体态观察结果（不诊断疾病、不提供治疗建议）。应用场景：智能喂食器、宠物摄像头、宠物健康管理平台。"
version: "1.0.0"
---

# Pet Body Condition Score 3D Analysis | 宠物体态3D评分（BCS）分析

Triggers when a user provides multi-angle pet videos (standing/side/top-down view) URL or files for analysis; supports
local video uploads or network URLs to call server-side APIs for 3D body shape reconstruction and Body Condition Score (
BCS, 1-9) evaluation, classifying body type as underweight, ideal, or overweight/obese, outputting standardized
observation data (without diagnosing diseases or prescribing treatment). Application scenarios: smart feeders, pet
cameras, pet health management platforms. Development reason: early warning for obesity-related diseases, scientific
weight management.

当用户提供宠物多角度视频（站立、侧身、俯视）的URL或文件时，触发本技能进行3D体型构建与BCS体况评分；支持通过上传本地视频或网络视频URL，调用服务端API进行体态分析，自动评估体况评分（1-9分），判断偏瘦、正常或肥胖，输出标准化体态观察结果（不诊断疾病、不提供治疗建议）。应用场景：智能喂食器、宠物摄像头、宠物健康管理平台。

## 🎯 AI 角色

**假设你是一个专业的宠物健康评估AI。你的任务是基于多角度视频（站立、侧身、俯视），分析宠物的体态特征，输出标准化的体况评分（BCS，1-9分），并给出体型分类。不要提供疾病诊断或治疗建议，仅客观描述体态观察结果。
**

smyx_pet_scratch_frequency_intensity_analysis
**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过宠物多角度视频（站立、侧身、俯视）进行 3D 体型构建与体况评分，获取标准化的 BCS（Body Condition Score，1-9
  分）观察结果与体型分类
- 能力包含：多角度视频分析、3D 体型重建、腰线/腹部轮廓识别、肋骨触感等价视觉判断、脂肪覆盖度估算、BCS 1-9
  分评分、体型分类（偏瘦 / 正常 / 偏胖 / 肥胖）、体态趋势监测
- 触发条件:
    1. **默认触发**：当用户提供宠物多角度视频 URL 或文件需要分析时，默认触发本技能进行体态 3D 评分
    2. 当用户明确需要进行体态/体重评估时，提及 BCS、体况评分、宠物体型、偏瘦、肥胖、体重管理、3D 体态、腰线评估等关键词，并且上传了视频文件或者图片文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史体态评分报告、历史 BCS 报告、体况评分报告清单、BCS 报告清单、查询历史体型分析报告、显示所有体态评分报告、显示宠物体重管理报告，查询肥胖风险提示报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有 BCS 报告"、"
       显示所有体态评分报告"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_pet_body_condition_score_3d_analysis --list --open-id` 参数调用 API
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

**在执行体态3D评分（BCS）分析前，必须按以下优先级顺序获取 open-id：**

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
        - **强烈建议**视频包含宠物的多角度画面：**站立位、侧身位、俯视位**，确保宠物身体完整入画、光线充足、无遮挡
        - 视频时长建议 ≥ 10 秒，便于 3D 体型重建
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行体态3D评分分析**
        - 调用 `-m scripts.smyx_pet_body_condition_score_3d_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 cat
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示宠物体态3D评分历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的体态3D评分观察报告
        - 包含：BCS 体况评分（1-9 分）、体型分类（极瘦 1-2 / 偏瘦 3 / 理想 4-5 / 偏胖 6-7 / 肥胖
          8-9）、腰线轮廓观察、腹部轮廓观察、脂肪覆盖度估算、3D 体型特征描述、健康风险提示
        - **BCS 评分参考标准**：
            - 1-3 分：偏瘦（肋骨明显可见、腰部内收明显、腹部上收）
            - 4-5 分：理想（肋骨易触及、腰线清晰、腹部适度上收）
            - 6-7 分：偏胖（肋骨需用力触及、腰线模糊、腹部下垂轻微）
            - 8-9 分：肥胖（肋骨难触及、无腰线、腹部明显下垂）
        - **重要提示**：仅客观描述观察到的体态特征与评分，不提供疾病诊断或治疗建议

## 资源索引

-

必要脚本：见 [scripts/smyx_pet_body_condition_score_3d_analysis.py](scripts/smyx_pet_body_condition_score_3d_analysis.py)(
用途：调用 API 进行宠物体态3D评分（BCS）分析，本地文件上传，网络 URL 由 API 服务自动下载)

- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB
- **多角度建议**：理想输入应包含站立、侧身、俯视三个角度，单一角度可能影响 3D 重建精度与 BCS 准确度
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供体重管理参考，不提供疾病诊断或治疗建议
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- BCS 评分基于视觉特征估算，可能与触诊评分存在偏差，建议结合兽医实际触诊作为最终参考
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`宠物体态3D评分报告-{记录id}`形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 宠物体态3D评分报告-20260312172200001 | 猫 | 2026-03-12 17:22:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地宠物多角度视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_pet_body_condition_score_3d_analysis --input /path/to/pet_multi_angle_video.mp4 --pet-type cat --open-id your-open-id

# 分析网络宠物多角度视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_pet_body_condition_score_3d_analysis --url https://example.com/pet_multi_angle_video.mp4 --pet-type cat --open-id your-open-id

# 显示历史分析报告/显示分析报告清单列表/显示历史BCS报告（自动触发关键词：查看历史BCS报告、历史报告、体态评分报告清单等）
python -m scripts.smyx_pet_body_condition_score_3d_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_pet_body_condition_score_3d_analysis --input video.mp4 --pet-type cat --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_pet_body_condition_score_3d_analysis --input video.mp4 --pet-type cat --open-id your-open-id --output result.json
```
