---
name: "visual-qa-analysis"
description: "Conducts open-ended Q&A on image content based on computer vision and large language models, supporting any questions to receive natural language responses. | 大模型视觉问答（VQA）技能，基于计算机视觉和大语言模型对图片内容进行开放式问答，支持任意提问得到自然语言回答"
version: "1.0.4"
license: "MIT-0"
---

# Large Model Visual Question Answering Skill | 大模型视觉问答技能

Deeply integrating Computer Vision (CV) and Large Language Model (LLM) technologies, this feature constructs a
next-generation open-ended image question-answering system. Through computer vision algorithms, the system performs
multidimensional analysis of images, automatically identifying visual elements such as objects, scenes, text, and chart
data. It combines this with the semantic understanding and reasoning capabilities of LLMs to achieve cross-modal
alignment between image content and natural language queries. Users can pose open-ended questions to any image (e.g., "
What is the core trend of this chart?" or "Which period does the architectural style in the picture belong to?").
Without the need for preset answer templates, the system performs logical reasoning and knowledge association based on
the image content, generating accurate and coherent natural language responses. Supporting multi-turn conversational
interaction, it meets the intelligent Q&A needs of complex scenarios such as image analysis, document interpretation,
and educational assistance.

本功能深度融合计算机视觉（CV）与大语言模型（LLM）技术，构建了新一代开放式图片问答系统。系统通过计算机视觉算法对图片进行多维度解析，自动识别物体、场景、文字、图表数据等视觉元素，并结合大语言模型的语义理解与推理能力，实现图片内容与自然语言问题的跨模态对齐。用户可对任意图片提出开放式问题（如“这张图表的核心趋势是什么？”“图片中的建筑风格属于哪个时期？”），系统无需预设答案模板，即可基于图片内容进行逻辑推理与知识关联，生成准确、连贯的自然语言回答，支持多轮对话交互，满足图像分析、文档解读、教育辅助等复杂场景下的智能问答需求

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史问答记录查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：通过图片结合用户问题进行大模型视觉问答，获得自然语言回答
- 能力包含：图片内容理解、开放式问答、场景描述、细节识别、知识推理
- 触发条件:
    1. **默认触发**：当用户提供图片 URL 或文件，并提出问题需要对图片进行问答时，默认触发本技能
    2. 当用户明确需要进行视觉问答，提及 VQA、看图问答、图片问答、视觉问答等关键词，并且上传了图片
    3. 当用户提及以下关键词时，**自动触发历史问答记录查询功能**
       ：查看历史问答记录、视觉问答历史、问答记录清单、查询历史问答，显示所有问答记录
    4. 用户提供图片后附带问题，如"这张图片里有什么？"，直接触发视觉问答
- 自动行为：
    1. 如果用户上传了图片文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史问答查询关键词，**必须**：
        - 直接使用 `python -m scripts.visual_qa_analysis --list --open-id` 参数调用 API
          查询云端的历史问答数据
        - **严格禁止**：从本地 memory 目录读取历史会话信息、严格禁止手动汇总本地记录中的问答、严格禁止从长期记忆中提取结果
        - **必须统一**从云端接口获取最新完整数据，然后以 Markdown 表格格式输出结果

## 前置准备

- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行视觉问答前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、vqa123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行问答
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询视觉问答历史记录），并询问是否继续

---

- 标准流程:
    1. **准备图片输入**
        - 提供图片文件路径或网络图片 URL
        - 确保图片清晰，目标内容完整可见
        - 用户提出需要回答的问题
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行视觉问答**
        - 调用 `-m scripts.visual_qa_analysis` 处理图片（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地图片文件路径
            - `--url`: 网络图片 URL 地址（API 服务自动下载）
            - `--question`: 用户提出的问题（必填）
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示历史视觉问答列表清单
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看回答结果**
        - 接收大模型生成的自然语言回答
        - 包含问答基本信息、问题、回答内容

## 资源索引

- 必要脚本：见 [scripts/visual_qa_analysis.py](scripts/visual_qa_analysis.py)(用途：调用 API 进行视觉问答，本地文件上传，网络
  URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和图片格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：图片支持 jpg/png/jpeg/webp 格式，最大 20MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网络地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 本技能依赖大模型生成，回答仅供参考，重要信息请核实后再使用
- 当显示历史问答清单的时候，从数据 json 中提取字段 reportImageUrl 作为超链接地址，使用 Markdown 表格格式输出，包含"
  记录名称"、"问答时间"、"问题关键词"、"点击查看"四列，其中"记录名称"列使用`视觉问答记录-{记录id}`形式拼接, "点击查看"列使用
  `[🔗 查看回答](reportImageUrl)`格式的超链接，用户点击即可直接跳转到对应的完整问答页面。
- 表格输出示例：
  | 记录名称 | 问答时间 | 问题关键词 | 点击查看 |
  |----------|----------|----------|----------|
  | 视觉问答记录-20260312172200001 | 2026-03-12 17:22:00 |
  图片里有什么动物 | [🔗 查看回答](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 本地图片问答（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.visual_qa_analysis --input /path/to/image.jpg --question "这张图片里有什么内容？请描述一下" --open-id openclaw-control-ui

# 网络图片问答（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.visual_qa_analysis --url https://example.com/image.jpg --question "图片中有几个人，他们在做什么？" --open-id openclaw-control-ui

# 显示历史问答记录（自动触发关键词：查看历史问答、历史记录、问答清单等）
python -m scripts.visual_qa_analysis --list --open-id openclaw-control-ui

# 输出精简回答
python -m scripts.visual_qa_analysis --input image.jpg --question "描述一下这张图片" --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.visual_qa_analysis --input image.jpg --question "请识别图片中的文字内容" --open-id your-open-id --output result.json
```
