---
name: "custom-timelapse-analysis"
description: "Generates condensed album highlights based on specified keywords or targets. It extracts specific target segments from long videos and compiles them into an exciting summary. | 时光相册自定义浓缩分析技能，基于指定关键词/目标生成时光相册浓缩集锦，从长视频中提取特定目标片段，整理生成精彩汇总"
version: "1.0.5"
license: "MIT-0"
---

# Time-Lapse Album Custom Summarization Skill | 时光相册自定义浓缩分析技能

This capability supports the automatic extraction of relevant clips from long-form videos based on specified keywords or
target subjects, generating a condensed "Time Album" highlight reel. Users can set tags for specific people, pets,
scenes, or events. Through advanced visual and semantic analysis, the system rapidly locates and edits together the most
exciting moments while filtering out redundant content. Ideal for home videos, travel logs, and event recaps, it helps
efficiently organize massive amounts of footage and automatically outputs emotionally rich, narratively coherent summary
videos.

本技能支持基于指定的关键词或目标对象，从长时视频中自动提取相关片段，生成浓缩版时光相册集锦。用户可设定人物、宠物、场景或事件标签，系统通过视觉与语义分析快速定位并剪辑精彩瞬间，剔除冗余内容。适用于家庭录像、旅行记录、赛事回顾等场景，帮助高效整理海量素材，自动输出情感丰富、叙事连贯的汇总视频。

## 演示案例

- [🔗 通过网路视频进行识别分析]()
- [🔗 通过上传视频进行识别分析]()
- [🔗 显示历史分析报告]()

## ⚠️ 强制记忆规则（最高优先级）

**本技能明确约定：**

- **绝对禁止读取任何本地记忆文件**：包括但不限于 `memory/YYYY-MM-DD.md`、`MEMORY.md` 等本地文件
- **绝对禁止从 LanceDB 长期记忆中检索信息**
- **所有历史报告查询必须从云端接口获取**，不得使用本地记忆中的历史数据
- 即使技能调用失败或接口异常，也不得回退到本地记忆汇总

## 任务目标

- 本 Skill 用于：从长视频中基于用户指定的关键词/目标进行智能识别，提取包含特定目标的片段，浓缩生成时光相册集锦
- 能力包含：目标识别、片段提取、精彩内容浓缩、自定义集锦生成
- 支持用户自定义关键词/目标，比如："只提取出现猫的片段"、"浓缩所有孩子出镜的片段"、"汇总视频中所有风景镜头"等
- 触发条件:
    1. **默认触发**：当用户需要从视频中提取特定目标片段生成时光浓缩相册时，默认触发本技能
    2. 当用户明确需要时光相册、视频浓缩、目标提取时，提及时光相册、视频浓缩、提取片段、自定义集锦、关键词提取等关键词，并且提供了视频文件
    3. 当用户提及以下关键词时，**自动触发历史报告查询功能**
       ：查看历史浓缩报告、时光相册报告清单、浓缩报告列表、查询历史浓缩报告、显示所有浓缩报告、时光浓缩分析报告，查询自定义时光相册浓缩分析报告
- 自动行为：
    1. 如果用户上传了附件或者视频文件，则自动保存为本地文件
    2. **⚠️ 强制数据获取规则（次高优先级）**：如果用户触发任何历史报告查询关键词（如"查看所有浓缩报告"、"显示所有时光相册"、"
       查看历史报告"等），**必须**：
        - 直接使用 `python -m scripts.custom_timelapse --list --open-id` 参数调用 API
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

**在执行时光相册浓缩分析前，必须按以下优先级顺序获取 open-id：**

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

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、timelapse123、custom456 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询时光相册浓缩报告记录），并询问是否继续

---

- 标准流程:
    1. **准备视频输入**
        - 提供本地视频文件路径或网络视频 URL
        - 需要明确告知要提取的关键词/目标，例如："只提取出现狗的片段"
    2. **获取 open-id（强制执行）**
        - 按上述流程控制获取 open-id
        - 如无法获取，必须提示用户提供用户名或手机号
    3. **执行时光相册自定义浓缩分析**
        - 调用 `-m scripts.custom_timelapse` 处理视频（**必须在技能根目录下运行脚本**）
        - 参数说明:
            - `--input`: 本地视频文件路径
            - `--url`: 网络视频 URL 地址（API 服务自动下载）
            - `--text`: 自定义提取目标/关键词描述
            - `--open-id`: 当前用户的 open-id（必填，按上述流程获取）
            - `--list`: 显示历史时光相册浓缩分析报告列表清单（可以输入起始日期参数过滤数据范围）
            - `--api-key`: API 访问密钥（可选）
            - `--api-url`: API 服务地址（可选，使用默认值）
            - `--detail`: 输出详细程度（basic/standard/json，默认 json）
            - `--output`: 结果输出文件路径（可选）
    4. **查看分析结果**
        - 接收结构化的时光相册自定义浓缩分析报告
        - 包含：视频基本信息、自定义提取目标、提取到的片段数量、时长统计、浓缩集锦链接、总结说明

## 资源索引

- 必要脚本：见 [scripts/custom_timelapse.py](scripts/custom_timelapse.py)(用途：调用 API 进行时光相册自定义浓缩分析，本地文件上传，网络
  URL 由 API 服务自动下载)
- 配置文件：见 [scripts/config.py](scripts/config.py)(用途：配置 API 地址、默认参数和视频格式限制)
- 领域参考：见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解 API 接口详细规范和错误码时)

## 注意事项

- 仅在需要时读取参考文档，保持上下文简洁
- 支持格式：mp4/avi/mov，最大 500MB
- API 密钥可选，如果通过参数传入则必须确保调用鉴权成功，否则忽略鉴权
- 分析结果仅供整理使用，请注意保护个人隐私
- 禁止临时生成脚本，只能用技能本身的脚本
- 传入的网路地址参数，不需要下载本地，默认地址都是公网地址，api 服务会自动下载
- 当显示历史分析报告清单的时候，从接口返回 json 数据中提取字段 reportImageUrl 作为超链接地址，且自动转化为如下 Markdown
  表格格式输出，包含"
  报告名称"、"自定义目标"、"分析时间"、"提取片段数"、"点击查看"五列，其中"报告名称"列使用`时光相册浓缩分析报告-{记录id}`
  形式拼接, "点击查看"列使用
  `[🔗 查看报告](reportImageUrl)`
  格式的超链接，用户点击即可直接跳转到对应的完整报告页面。
- 表格输出示例：
  | 报告名称 | 自定义目标 | 分析时间 | 提取片段数 | 点击查看 |
  |----------|------------|----------|------------|----------|
  | 时光相册浓缩分析报告 -20260328221000001 | 所有出现猫的镜头 | 2026-03-28 22:10:00 |
  8段 | [🔗 查看报告](https://example.com/report?id=xxx) |

## 使用示例

```bash
# 浓缩本地视频，提取特定目标（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.custom_timelapse --input /path/to/vacation.mp4 --text "提取所有孩子出镜的片段" --open-id openclaw-control-ui

# 浓缩网络视频，自定义提取目标（以下只是示例，禁止直接使用openclaw-control-ui 作为 open-id）
python -m scripts.custom_timelapse --url https://example.com/family.mp4 --text "只提取风景镜头" --open-id openclaw-control-ui

# 显示历史浓缩报告/显示浓缩报告清单列表/显示历史时光相册（自动触发关键词：查看历史浓缩报告、历史报告、浓缩报告清单等）
python -m scripts.custom_timelapse --list --open-id openclaw-control-ui

# 输出精简报告
python -m scripts.custom_timelapse --input video.mp4 --text "提取车的片段" --open-id your-open-id --detail basic

# 保存结果到文件
python -m scripts.custom_timelapse --input video.mp4 --text "提取狗的片段" --open-id your-open-id --output result.json
```
