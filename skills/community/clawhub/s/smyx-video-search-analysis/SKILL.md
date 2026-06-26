---
name: "video-search-analysis"
description: "Conducts intelligent video search based on target and semantic descriptions; supports conventional target retrieval, natural language description retrieval, and vectorized model matching. | 视频搜索/视频检索智能分析技能，基于目标、语义描述进行智能视频搜索，支持常规目标检索、自然语言描述检索、向量化模型匹配"
version: "1.0.0"
---

# Intelligent Video Search & Retrieval Analysis Skill | 视频搜索检索智能分析技能

Based on multimodal large models and deep learning algorithms, this feature constructs a next-generation intelligent
video retrieval system, supporting three core modes: conventional object retrieval, natural language description
retrieval, and vectorized model matching. Through computer vision technology, the system automatically identifies and
indexes conventional targets such as people, vehicles, and objects. Simultaneously, it leverages image-text multimodal
large models to achieve cross-modal alignment between semantics and video content, enabling open-ended retrieval via
natural language descriptions like "person wearing red clothes" or "talking on the phone." Furthermore, employing a
full-modal vectorization model, the system transforms video content into high-dimensional vectors, realizing fused
retrieval across mixed modalities of text, image, and video. Supporting multi-condition combination and fuzzy semantic
matching, it rapidly locates target footage, meeting the precise retrieval demands of complex scenarios such as security
surveillance and video asset management.

本功能基于多模态大模型与深度学习算法，构建了新一代智能视频检索系统，支持常规目标检索、自然语言描述检索及向量化模型匹配三种核心模式。系统通过计算机视觉技术自动识别并索引人、车、物等常规目标，同时利用图文多模态大模型实现语义与视频内容的跨模态对齐，支持用户通过“穿红色衣服的人”、“打电话”等自然语言描述进行开放式检索。此外，系统采用全模态向量化模型，将视频内容转化为高维向量，实现文本、图像、视频混合模态的融合检索，支持多条件组合与模糊语义匹配，快速定位目标画面，满足安防监控、视频资产管理等复杂场景下的精准检索需求

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：在长视频中根据用户提供的目标描述或关键词智能搜索，定位包含特定目标的片段
- 能力包含：**常规目标检索**（检测特定物体/人物出现）、**自然语言智述检索**（用自然语言描述要找的内容）、**向量化模型匹配**
  （基于视频特征向量相似度匹配）
- 支持从长视频中快速定位感兴趣内容，节省观看时间
- 触发条件:
    1. **默认触发**：当用户需要在视频中搜索特定内容/目标时，默认触发本技能进行视频检索分析
    2. 当用户明确需要视频搜索、视频检索时，提及视频搜索、视频检索、找片段、定位目标、智能搜视频等关键词，并且提供了视频文件和搜索描述
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史搜索报告、视频搜索报告清单、搜索报告列表、查询历史搜索报告、显示所有搜索报告、视频检索分析报告，查询视频搜索分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存到技能目录下 attachments
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有搜索报告"、"显示所有检索结果"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.video_search_analysis --list --open-id` 参数调用 API
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

**在执行视频搜索分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、search123、video456 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询搜索报告记录），并询问是否继续

---

- 标准流程:
    1. **准备视频输入**
        - 提供本地视频文件路径或网络视频 URL
        - 需要明确告知要搜索的目标/描述，可以是物体名称或自然语言描述
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行视频搜索智能分析**
        - 调用 `-m scripts.video_search_analysis` 处理视频（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径（使用 multipart/form-data 方式上传）
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--text`: 搜索目标/自然语言描述（说明要找什么内容）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示历史视频搜索分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的视频搜索分析报告
        - 包含：视频基本信息、搜索关键词、匹配到的片段数量、每个片段的起始时间/结束时间、置信度、视频片段预览链接

## 资源索引

- 必要脚本：见 [scripts/video_search_analysis.py](scripts/video_search_analysis.py)(用途：调用 API 进行视频搜索分析，本地文件使用
  multipart/form-data 方式上传，网络 URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：mp4/avi/mov，最大 1GB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 搜索结果仅供参考，请以实际视频内容为准
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从数据 json 中提取字段 reportImageUrl 作为超链接地址，使用 Markdown 表格格式输出，包含"
  报告名称"、"搜索关键词"、"分析时间"、"匹配片段数"、"点击查看"五列，其中"报告名称"列使用`视频搜索分析报告-{记录id}`
  形式拼接, "点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 搜索关键词 | 分析时间 | 匹配片段数 | 点击查看 |
  |----------|------------|----------|------------|----------|
  | 视频搜索分析报告 -20260328221000001 | 穿蓝色衣服的人出现 | 2026-03-28 22:10:00 |
  3段 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 在本地视频中搜索特定目标（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.video_search_analysis --input /path/to/life.mp4 --text "狗狗出现的片段" --open-id openclaw-control-ui

# 在网络视频中用自然语言搜索（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.video_search_analysis --url https://example.com/event.mp4 --text "有人发言的片段" --open-id openclaw-control-ui

# 显示历史搜索报告/显示搜索报告清单列表/显示历史视频搜索（自动触发关键词：查看历史搜索报告、历史报告、搜索报告清单等）
python -m scripts.video_search_analysis --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.video_search_analysis --input video.mp4 --text "汽车" --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.video_search_analysis --input video.mp4 --text "人物出现" --open-id your-open-id --output result.json
```
