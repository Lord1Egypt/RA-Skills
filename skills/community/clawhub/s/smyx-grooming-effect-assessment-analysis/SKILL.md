---
name: "smyx-grooming-effect-assessment-analysis"
description: "AI-powered pet grooming effect assessment: detects mat residue area, dandruff coverage, and coat smoothness from post-grooming images, outputs a 0-100 grooming score with targeted re-grooming suggestions. Scenarios: daily home grooming, pet salon quality check, long-hair cat/dog shedding season management. | 通过智能梳毛器或普通摄像头拍摄梳毛后的宠物皮肤和毛发高清图像，利用AI图像识别技术检测毛结团块残留面积、皮屑覆盖率以及毛发顺滑度，自动评估本次梳毛效果，并提示是否需要进行二次梳理或进一步护理。有助于宠物主人判断梳毛是否彻底，预防毛球症和皮肤问题。应用场景：宠物家庭日常梳理、宠物美容店服务质检、长毛猫/犬换毛期管理。"
version: "1.0.0"
---

# Pet Grooming Effect Assessment (Mats/Dandruff) | 宠物梳毛效果评估（毛结/皮屑）

AI-powered pet grooming effect assessment: detects mat residue area, dandruff coverage, and coat smoothness from
post-grooming images, outputs a 0-100 grooming score with targeted re-grooming suggestions. Scenarios: daily home
grooming, pet salon quality check, long-hair cat/dog shedding season management.

通过智能梳毛器或普通摄像头拍摄梳毛后的宠物皮肤和毛发高清图像，利用AI图像识别技术检测毛结团块残留面积、皮屑覆盖率以及毛发顺滑度，自动评估本次梳毛效果，并提示是否需要进行二次梳理或进一步护理。有助于宠物主人判断梳毛是否彻底，预防毛球症和皮肤问题。应用场景：宠物家庭日常梳理、宠物美容店服务质检、长毛猫/犬换毛期管理。

## 🎯 AI 角色

**假设你是一个专业的宠物护理AI。你的任务是分析梳毛后宠物的高清图像（局部或全身），检测皮肤表面的皮屑覆盖情况以及毛发中残留的毛结团块，评估梳毛效果，并输出梳理质量评分。不要提供医疗建议，仅输出基于视觉的评估结果。
**

## 任务目标

- 本 Skill 用于：通过梳毛后的宠物图像/视频进行梳毛效果评估，检测毛结残留与皮屑覆盖情况，输出标准化评估结果和护理建议
- 能力包含：图像分析、毛结团块残留检测、皮屑覆盖率评估、毛发顺滑度评分、梳理效果综合评分、二次梳理建议
- 触发条件:
    1. **默认触发**：当用户提供梳毛后宠物皮肤/毛发图像或视频需要分析时，默认触发本技能进行梳毛效果评估
    2. 当用户明确需要梳毛效果评估时，提及梳毛效果、毛结检测、皮屑评估、毛发顺滑度、梳理评分等关键词，并且上传了图像或视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史梳毛评估报告、历史梳理效果报告、梳毛评估报告清单、显示所有梳毛报告、查询梳理评估结果
- 自动行为：
    1. 如果用户上传了附件或者图像/视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有梳毛评估报告"、"
       显示梳理效果报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_grooming_effect_assessment_analysis --list --open-id` 参数调用 API
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

**在执行梳毛效果评估前，必须按以下优先级顺序获取 open-id：**

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
    1. **准备图像/视频输入**
        - 提供本地图像/视频文件路径或网络图像/视频 URL
        - 确保图像/视频清晰展示梳毛后宠物皮肤和毛发状态，光线充足，尽量拍摄背部、腹部、四肢等典型部位
        - 支持图像（jpg/png）和视频（mp4/avi/mov）格式
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行梳毛效果评估**
        - 调用 `-m scripts.smyx_grooming_effect_assessment_analysis` 处理图像/视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地图像/视频文件路径
            - `--url`: 网络图像/视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 cat
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示梳毛效果评估历史报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看评估结果**
        - 接收结构化的梳毛效果评估报告
        - 包含：**梳理效果评分**（0-100分，综合毛结残留、皮屑覆盖、毛发顺滑度）、**毛结残留检测**（位置、面积占比、严重程度）、*
          *皮屑覆盖评估**（覆盖率、分布区域、严重程度）、**毛发顺滑度**（等级评价）、**护理建议**（如"
          右后腿根部仍有毛结，建议重点梳理"）
        - **重要提示**：仅客观描述视觉评估结果，不提供医疗诊断或治疗建议

## 📊 评分体系说明

| 评分区间   | 梳理效果  | 说明                     |
|--------|-------|------------------------|
| 90-100 | ⭐ 优秀  | 毛发顺滑无结，皮屑极少，梳理非常彻底     |
| 70-89  | ✅ 良好  | 偶有微小毛结或轻微皮屑，整体梳理效果不错   |
| 50-69  | ⚠️ 一般 | 存在明显毛结或皮屑较多，建议二次梳理     |
| 0-49   | ❌ 较差  | 毛结残留较多或皮屑严重，需重点补梳或就医检查 |

## 资源索引

-
必要脚本：见 [scripts/smyx_grooming_effect_assessment_analysis.py](scripts/smyx_grooming_effect_assessment_analysis.py)(
用途：调用 API 进行梳毛效果评估分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和场景代码)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持 jpg/png/mp4/avi/mov 格式，最大 10MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 评估结果仅供梳毛效果参考，不提供医疗诊断或治疗建议
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，API 服务会自动下载
- 当显示历史评估报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`梳毛效果评估报告-{记录id}`
  形式拼接, "点击查看"
  列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 梳毛效果评估报告-20260312172200001 | 猫 | 2026-03-12 17:22:00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地梳毛后宠物图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_grooming_effect_assessment_analysis --input /path/to/grooming_photo.jpg --pet-type cat --open-id your-open-id

# 分析网络梳毛后宠物图像/视频（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.smyx_grooming_effect_assessment_analysis --url https://example.com/grooming_video.mp4 --pet-type cat --open-id your-open-id

# 显示历史评估报告/显示评估报告清单列表（自动触发关键词：查看历史梳毛评估报告、历史报告、梳理效果报告清单等）
python -m scripts.smyx_grooming_effect_assessment_analysis --list --open-id your-open-id

# 输出精简报告
python -m scripts.smyx_grooming_effect_assessment_analysis --input photo.jpg --pet-type cat --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.smyx_grooming_effect_assessment_analysis --input photo.jpg --pet-type cat --open-id your-open-id --output result.json
```
