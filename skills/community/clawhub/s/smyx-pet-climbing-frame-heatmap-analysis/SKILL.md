---
name: "smyx-pet-climbing-frame-heatmap-analysis"
description: "Triggers when a user provides a cat climbing frame / cat tree area video URL or file for analysis; supports local video uploads or network URLs to call server-side APIs for multi-region activity recognition, analyzing dwell time on each layer, jump/transition counts, and generating a 2D activity heatmap to evaluate exercise volume and mental wellbeing (without diagnosing diseases). Application scenarios: cat climbing frame + camera, pet behavior monitoring, cat health management. Development reason: quantify cat activity distribution and enrichment usage. | 当用户提供猫爬架/猫树区域的视频URL或文件时，触发本技能进行活动热力图分析；支持通过上传本地视频或网络视频URL，调用服务端API进行多区域活动识别，分析各层停留时长、跳跃/转移次数，生成2D活动热力图，用于评估运动量与心理健康（不诊断疾病）。应用场景：猫爬架+摄像头、宠物行为监测、猫咪健康管理。"
version: "1.0.2"
license: "MIT-0"
---

# Pet Climbing Frame / Cat Tree Activity Heatmap | 宠物爬架/猫树活动热力图

Triggers when a user provides a cat climbing frame / cat tree area video URL or file for analysis; supports local video
uploads or network URLs to call server-side APIs for multi-region activity recognition, analyzing dwell time on each
layer, jump/transition counts, and generating a 2D activity heatmap to evaluate exercise volume and mental wellbeing (
without diagnosing diseases). Application scenarios: cat climbing frame + camera, pet behavior monitoring, cat health
management. Development reason: quantify cat activity distribution and enrichment usage.

当用户提供猫爬架/猫树区域的视频URL或文件时，触发本技能进行活动热力图分析；支持通过上传本地视频或网络视频URL，调用服务端API进行多区域活动识别，分析各层停留时长、跳跃/转移次数，生成2D活动热力图，用于评估运动量与心理健康（不诊断疾病）。应用场景：猫爬架+摄像头、宠物行为监测、猫咪健康管理。

## 🎯 AI 角色

**假设你是一个专业的宠物行为分析AI。你的任务是基于猫爬架（猫树）多区域的连续视频，检测猫咪在不同层级和位置的停留时长、跳跃或转移次数，生成标准化的活动热力图数据。不要提供健康诊断，仅客观描述活动分布指标。
**

## 任务目标

- 本 Skill 用于：通过猫爬架/猫树区域视频生成猫咪 2D 活动热力图，获取标准化的运动量与活动分布观察结果
- 能力包含：视频分析、各层停留时长统计、跳跃/转移次数计数、活动密度分布、2D 热力图生成、运动量与心理健康趋势提示
- 触发条件:
    1. **默认触发**：当用户提供猫爬架/猫树区域视频 URL 或文件需要分析时，默认触发本技能进行活动热力图分析
    2. 当用户明确需要进行猫咪活动监测时，提及猫爬架、猫树、活动热力图、停留时长、跳跃次数、运动量评估、猫咪心理健康、行为丰富度等关键词，并且上传了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**：查看历史活动热力图报告、历史猫爬架报告、活动热力图报告清单、查询活动热力图报告、显示所有猫爬架报告、显示猫咪运动量报告
- 自动行为：
    1. 如果用户上传了附件或者视频/图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有猫爬架报告"、"
       显示所有活动热力图报告"、"查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.smyx_pet_climbing_frame_heatmap_analysis --list` 调用 API
          查询云端的历史报告数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的报告、严格禁止从长期记忆中提取报告
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔐 用户身份处理（内部自动完成）

用户身份参数由系统内部自动处理，**不得向用户展示、询问或要求输入任何身份标识**。

执行本技能分析或历史报告查询时，脚本会自动完成身份初始化：

- 上游系统如有内部身份参数，会由脚本静默接收并使用
- 上游系统未提供时，脚本会自动复用本地缺省用户
- 本地缺省用户不存在时，脚本会自动创建并在后续任务中复用
- 对用户输出时，只展示分析进度、分析结果和报告链接，不展示内部身份值

**关键约束：**

- 不得提示用户输入用户名、手机号或任何内部身份参数
- 不得在回复、报告、示例、错误提示中暴露内部身份值
- 不得把内部身份参数列为用户需要理解或传入的参数
- 历史报告查询同样由系统内部身份自动关联，用户只需表达“查看历史报告/报告清单”等意图

---

- 标准流程:
    1. **准备视频输入**
        - 提供本地视频文件路径或网络视频 URL
        - 确保视频能完整覆盖猫爬架/猫树各层级与平台区域，光线充足，无遮挡，机位稳定（建议固定机位以获得稳定热力图）
    2. **系统自动完成身份关联**
        - 无需用户输入任何身份参数
        - 不在回复中展示内部身份值
    3. **执行活动热力图分析**
        - 调用 `-m scripts.smyx_pet_climbing_frame_heatmap_analysis` 处理视频文件（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--pet-type`: 宠物类型，可选值：cat/dog/other，默认 cat
            - `--list`: 显示猫爬架/猫树活动热力图视频历史分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的活动热力图观察报告
        - 包含：各层级/区域停留时长（秒/分钟）、跳跃与转移次数、最常停留区域、最少使用区域、活动总时长占比、2D
          活动热力图（区域热度分布）、运动量与心理健康参考提示
        - **重要提示**：仅客观描述观察到的活动分布指标，不提供疾病诊断或治疗建议

## 资源索引

-
必要脚本：见 [scripts/smyx_pet_climbing_frame_heatmap_analysis.py](scripts/smyx_pet_climbing_frame_heatmap_analysis.py)(
用途：调用 API 进行猫爬架/猫树活动热力图分析，本地文件上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 视频要求：支持 mp4/avi/mov 格式，最大 10MB
- 建议使用固定机位、能覆盖整座爬架/猫树全部层级的视角，连续记录时长不少于若干分钟，便于生成有意义的热力分布
- 分析结果仅供运动量与丰富度参考，不提供疾病诊断或治疗建议
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"报告名称"、"宠物类型"、"分析时间"、"点击查看"四列，其中"报告名称"列使用`猫爬架活动热力图报告-{记录id}`
  形式拼接, "点击查看"列使用 `[🔗 查看报告](reportImageUrl)` 格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 宠物类型 | 分析时间 | 点击查看 |
  |----------|----------|----------|----------|
  | 猫爬架活动热力图报告-20260312172200001 | 猫 | 2026-03-12 17:22:
  00 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 分析本地猫爬架视频
python -m scripts.smyx_pet_climbing_frame_heatmap_analysis --input /path/to/cat_tree_video.mp4 --pet-type cat

# 分析网络猫爬架视频
python -m scripts.smyx_pet_climbing_frame_heatmap_analysis --url https://example.com/cat_tree_video.mp4 --pet-type cat

# 显示历史分析报告/显示分析报告清单列表/显示历史活动热力图报告（自动触发关键词：查看历史活动热力图报告、历史报告、猫爬架报告清单等）
python -m scripts.smyx_pet_climbing_frame_heatmap_analysis --list

# 输出精简报告
python -m scripts.smyx_pet_climbing_frame_heatmap_analysis --input video.mp4 --pet-type cat --detail basic

# 保存结果到文件
python -m scripts.smyx_pet_climbing_frame_heatmap_analysis --input video.mp4 --pet-type cat --output result.json
```
