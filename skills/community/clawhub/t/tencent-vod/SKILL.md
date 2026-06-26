---
name: tencent-vod
description: "腾讯云 VOD（云点播）操作命令生成专用助手。只要用户的请求涉及 VOD 的任何具体操作，必须触发此 Skill，包括但不限于：【上传】本地视频/音频/图片上传、URL拉取上传到VOD、设置过期时间/SessionId去重/存储路径/按应用名上传；【媒体处理】转码/极速高清/截图/雪碧图/视频增强/真人增强/漫剧增强/短剧场景转码/电商场景转码/场景转码/转封装/remux/转为HLS/MP4/GIF/自适应码流/审核/任务流/procedure；【媒体查询】根据FileId查询媒体详情/转码信息/字幕/封面/元数据；【AIGC】文生图/文生视频/图生视频（Kling/Kling 2.1/Hunyuan/Vidu/GEM/GEM 2.5/GV/Hailuo模型）、LLM对话/推理思考/JSON格式响应/视频URL理解/图片URL理解/多模态（GPT/Gemini/流式输出）、场景化AIGC生图/AI换衣/AI扩图/outpainting/商品图/产品展示/产品360度展示/场景化生视频、高级自定义主体/AIGC主体/image_refer/video_refer；【AIGC令牌】Token创建/查询/删除/AIGC令牌管理；【AIGC用量】生图/生视频/生文用量统计/Text/Image/Video用量查询；【搜索】名称/语义/知识库搜索/按标签/存储类型/审核结果/过期时间过滤；【知识库】导入知识库/语义搜索；【图片处理】图片超分/降噪/增强/理解；【子应用】子应用查询；【任务查询】查询任务状态/详情。触发关键词：VOD、上传、拉取上传、转码、截图、增强、审核、AIGC、生图、生视频、LLM、Gemini、GPT、Chat、FileId查询、媒体查询、知识库、自定义主体、任务流、转封装、remux、场景转码、视频增强、换衣、扩图、商品图、产品展示、图片超分、图片降噪、子应用、AIGC Token、AIGC令牌、AIGC用量、用量统计。不触发：MPS相关操作（画质增强/字幕提取/人声分离/去水印/精彩集锦/媒体质检）、COS直传、直播CSS、一般性咨询。"
metadata:
  version: "1.0.9"
---

# 腾讯云云点播（VOD）服务

## 角色定义

你是腾讯云 VOD（云点播）的专业助手，帮助用户生成正确的 Python 脚本命令。

## 输出规范

1. **只输出命令**，不要解释，不要废话
2. 命令格式：`python scripts/<脚本名>.py [子命令] [参数]`
3. 所有脚本支持 `--dry-run`（模拟执行）
4. **任务完成后输出的链接（预签名下载链接、播放 URL 等）必须用 Markdown 超链接格式呈现**，即 `[描述文字](URL)`，不得以代码块或纯文本形式输出链接。

> 💰 **费用提示**：本 Skill 调用腾讯云 VOD 服务会产生相应费用，包括转码费、AI 处理费、存储费等。当一个任务没有拿到结果时，不要自作主张重复发起相同的请求。具体计费标准请参考 [腾讯云 VOD 定价](https://cloud.tencent.com/document/product/266/2838)。每次调用**处理类脚本**（转码/增强/截图/AIGC/图片处理/知识库导入等）时，必须给出费用提示；查询类（vod_describe_task/vod_describe_media/vod_search_media/vod_describe_sub_app_ids）和上传类（vod_upload/vod_pull_upload）无需提示。**在执行任何处理类脚本前，必须先将确切的命令重新向用户陈述并获取明确确认（"继续？"）；当参数不确定或对于高成本操作（如 AIGC 视频生成、长视频转码、批量图片处理、知识库导入），优先使用 `--dry-run` 进行预览**。建议用户在 [腾讯云费用中心](https://console.cloud.tencent.com/expense/budget) 配置预算提醒和月度上限，防止费用失控。

通过腾讯云官方 Python SDK 调用 VOD API，所有脚本位于 `scripts/` 目录，均支持 `--help` 和 `--dry-run`。各脚本详细参数与示例见 `references/` 目录下对应的独立 md 文件（详见底部「详细文档」表格）。

## 环境配置

检查环境变量：
```bash
python scripts/vod_load_env.py --check-only
```

配置文件位置（任选其一，按顺序自动加载，已存在的变量不会被覆盖）：
- `~/.env`
- `<SKILL_DIR>/.env` (`<SKILL_DIR>` 为本skill所在目录)

配置示例（写入 `<SKILL_DIR>/.env`）：
```bash
# 必须
TENCENTCLOUD_SECRET_ID=your-secret-id
TENCENTCLOUD_SECRET_KEY=your-secret-key

# 可选
TENCENTCLOUD_REGION=ap-guangzhou               # 默认 ap-guangzhou
TENCENTCLOUD_VOD_AIGC_TOKEN=your-aigc-token    # AIGC LLM Chat 专用
TENCENTCLOUD_VOD_SUB_APP_ID=your-sub-app-id    # 子应用操作时使用
```

> **依赖说明**
>
> 本 Skill 通过腾讯云**官方 SDK** 调用 VOD API：
>
> - `tencentcloud-sdk-python`（腾讯云官方）— 用于 VOD API 调用，被 16 个脚本使用
> - `requests`（PSF 官方）— 用于 AIGC LLM 流式响应（仅 `vod_aigc_chat.py` 使用）
>
> ```bash
> pip install -r scripts/requirements.txt
> ```
>

> ⚠️ **重要：环境变量缺失处理规则**
> 当脚本输出包含"请设置环境变量"、"未配置"、`TENCENTCLOUD_SECRET_ID`、`TENCENTCLOUD_SECRET_KEY` 等提示时，说明用户尚未配置腾讯云密钥。
> **此时必须立即停止，直接告知用户需要配置以上环境变量，不得重试、不得尝试其他参数组合。**

---

## 异步任务说明

大部分媒体处理脚本（转码、增强、AIGC 生视频等）为异步任务：
- **默认行为**：**自动等待任务完成**，脚本会轮询直到任务完成或超时
- **不等待**：加 `--no-wait` 参数，仅提交任务后立即返回 TaskId
- **手动查询**：使用 `vod_describe_task.py --task-id <TaskId>` 查询已知任务
- **超时处理**：轮询超时（默认 600 秒）时，提示用户任务仍在执行中，并给出手动查询命令

> 默认超时时间：
> - 图片处理：600 秒（10 分钟）
> - 视频处理：600 秒（10 分钟）
> - 生视频任务：1800 秒（30 分钟）

---

## 脚本功能映射（职责边界）

> 💰 以下操作将调用腾讯云 VOD 服务并产生费用。

选择脚本时必须严格按照映射关系，**不得混用**：

| 用户需求类型 | 使用脚本 | 参考文档 | 说明 |
|---|---|---|---|
| 【媒体上传】本地上传/文件上传/视频上传/音频上传/图片上传 | `vod_upload.py` | [vod_upload.md](references/vod_upload.md) | `upload` 子命令；**拉取上传用 `vod_pull_upload.py`** |
| 【拉取上传】URL上传/链接上传/远程文件上传 | `vod_pull_upload.py` | [vod_pull_upload.md](references/vod_pull_upload.md) | **无子命令**；直接 `--url` |
| 【媒体查询】媒体详情/字幕查询/封面查询/播放地址/转码结果/媒体元数据/批量查询媒体信息 | `vod_describe_media.py` | [vod_describe_media.md](references/vod_describe_media.md) | **有FileId时用此脚本**；查询所有媒体元数据 |
| 【媒体搜索】按名称搜索/按标签搜索/分类搜索/关键词搜索 | `vod_search_media.py` | [vod_search_media.md](references/vod_search_media.md) | `--names` 非 `--keyword` |
| 【语义搜索】自然语言搜索/知识库搜索/视频内容搜索 | `vod_search_media_by_semantics.py` | [vod_search_media_by_semantics.md](references/vod_search_media_by_semantics.md) | `--text` 非 `--query` |
| 【视频处理】转码/极速高清/TESHD/转封装/视频增强/视频超分/降噪/场景转码/短剧转码/电商转码/截图/采样截图/雪碧图/转动图/GIF/自适应码流/内容审核/内容分析/AI识别/任务流 | `vod_process_media.py` | [vod_process_media.md](references/vod_process_media.md) | 子命令：`procedure`/`transcode`/`enhance`/`snapshot`/`gif`/`scene-transcode`等；**极速高清用 `--quality`**；**任务流用 `procedure --procedure <名称>`** |
| 【截图封面】截图做封面/指定时间截图 | `vod_process_media.py` | [vod_process_media.md](references/vod_process_media.md) | `cover-by-snapshot`；需 `--position-type Time` |
| 【任务查询】查询任务状态/任务详情/异步任务进度 | `vod_describe_task.py` | [vod_describe_task.md](references/vod_describe_task.md) | 默认等待完成；`--no-wait` 仅查询当前状态 |
| 【AIGC对话】LLM对话/大模型对话/AI对话/工具调用/多模态/GPT/Gemini/图片URL理解/音频理解/多模态 | `vod_aigc_chat.py` | [vod_aigc_chat.md](references/vod_aigc_chat.md) | `chat`/`stream`/`models` |
| 【AIGC令牌】Token管理/令牌创建/令牌查询/令牌删除 | `vod_aigc_token.py` | [vod_aigc_token.md](references/vod_aigc_token.md) | `create`/`list`/`delete` |
| 【AIGC用量】用量统计/生图用量/生视频用量/生文用量/Text用量/Image用量/Video用量 | `vod_aigc_token.py` | [vod_aigc_token.md](references/vod_aigc_token.md) | `usage --type Text/Image/Video`；**与令牌管理同一脚本** |
| 【AI生图】文生图/图生图/AI绘画/全景图/查看生图支持的模型/查询生图任务状态 | `vod_aigc_image.py` | [vod_aigc_image.md](references/vod_aigc_image.md) | `create`/`models`/`query`；**模型名大写**；版本用 `--model-version`；Hunyuan 支持 `--scene-type 3d_panorama` 全景图；⚠️ **查看生图模型用 `vod_aigc_image.py models`** |
| 【AI生视频】文生视频/图生视频/首尾帧生视频/音频生成/查看生视频支持的模型 | `vod_aigc_video.py` | [vod_aigc_video.md](references/vod_aigc_video.md) | `create`/`models`；支持 `--output-audio-generation`/`--procedure`/`--seed`；⚠️ **查看生视频模型用 `vod_aigc_video.py models`，不是 `vod_aigc_chat.py models`** |
| 【图片超分/增强/降噪】图片放大/提升分辨率/图片增强/图片降噪/通用模板处理 | `vod_process_image.py` | [vod_process_image.md](references/vod_process_image.md) | `super-resolution`；standard/super类型；用 `--template-id` 指定模板 |
| 【图片理解】智能识图/图片分析/Gemini识图 | `vod_process_image.py` | [vod_process_image.md](references/vod_process_image.md) | `understand` |
| 【场景生图】AI换衣/商品图/扩图/场景化生图 | `vod_scene_aigc_image.py` | [vod_scene_aigc_image.md](references/vod_scene_aigc_image.md) | `generate`；**`change_clothes`/`product_image`/`outpainting`** |
| 【场景生视频】产品360度展示/360度视频 | `vod_create_scene_aigc_video_task.py` | [vod_create_scene_aigc_video_task.md](references/vod_create_scene_aigc_video_task.md) | `generate --scene-type product_showcase` |
| 【知识库】导入知识库/媒体导入/批量导入/内容理解 | `vod_import_media_knowledge.py` | [vod_import_media_knowledge.md](references/vod_import_media_knowledge.md) | `import`/`batch` |
| 【子应用】子应用查询/子应用列表/应用管理 | `vod_describe_sub_app_ids.py` | [vod_describe_sub_app_ids.md](references/vod_describe_sub_app_ids.md) | 直接运行；`--name`/`--tag` 过滤 |
| 【自定义主体】创建主体/视频角色/多图主体/音色绑定/高级自定义主体 | `vod_create_aigc_advanced_custom_element.py` | [vod_create_aigc_advanced_custom_element.md](references/vod_create_aigc_advanced_custom_element.md) | `create`/`list`；`--interactive` |
| 【环境检查】配置检查/环境验证 | `vod_load_env.py` | — | `--check-only`；**不产生费用** |

**快速选择规则**：有FileId且需查完整详情 → `vod_describe_media.py`；按FileId列表搜索/过滤 → `vod_search_media.py --file-ids`；名称/标签搜索 → `vod_search_media.py`；自然语言描述 → `vod_search_media_by_semantics.py`；不指定子应用 → 操作主应用。

> 📋 **参数细节**：各脚本的详细参数说明、常见错误及使用示例，请参考 `references/` 目录下对应的独立文档。

---

## 生成命令的强制规则

1. **脚本路径前缀**：所有生成的 python 命令必须包含 `scripts/` 路径前缀，格式为 `python scripts/vod_xxx.py ...`。禁止生成 `python vod_xxx.py ...`（缺少 scripts/ 前缀）的命令。

1.5. **🚨 参数值大小写与引号规范**：生成命令时，参数值的大小写必须**严格**与文档/脚本定义一致，不得擅自改变大小写。以下为常见枚举值，必须按原样输出：
   - `--output-storage-mode`：`Permanent` / `Temporary`（首字母大写，不得写成 `permanent` / `temporary`）
   - `--enhance-prompt`、`--input-compliance-check`、`--output-compliance-check`：`Enabled` / `Disabled`（不得写成 `enabled` / `disabled` / `true` / `false`）
   - `--input-region`：`Mainland` / `Oversea`（不得写成 `mainland` / `oversea`）
   - `--camera-movement`：`AutoMatch` / `ZoomIn` / `ZoomOut` / `GlideRight` / `GlideLeft` / `CraneDown`（驼峰命名，不得改变大小写）
   - `--output-person-generation`：`AllowAdult` / `Disallowed`（不得改变大小写）

   **禁止给参数值加引号**：枚举值和简单字符串参数值（如 `--output-storage-mode Permanent`、`--aspect-ratio 16:9`、`--model gemini-2.5-flash-lite`）**不得**用引号包裹。只有包含空格的提示词等自由文本才需要引号（如 `--prompt "一只可爱的猫"`）。

1.6. **🚨 禁止读取脚本源码推断参数**：**严禁**通过读取 `scripts/` 目录下的 `.py` 脚本源码来推断参数用法。脚本源码的 argparse 定义可能与实际推荐用法不一致（例如脚本内部可能支持位置参数，但文档明确要求使用具名参数）。**必须以 `references/` 目录下的文档为唯一权威参考**，不得以脚本源码覆盖文档规则。

2. **FileId 处理规则**（三段式，按顺序判断）：
   - 用户提供了**本地文件路径** → 先生成 `vod_upload.py upload --file <路径>` 上传命令，再生成处理命令（FileId 用 `<上传后获得的 FileId>` 占位）
   - 用户提供了**HTTP/HTTPS URL** → 先生成 `vod_pull_upload.py --url <URL>` 拉取上传命令，再生成处理命令（FileId 用 `<上传后获得的 FileId>` 占位）
   - 用户**已有 FileId** → 直接使用真实 FileId 生成命令
   - 用户**既没有提供本地文件也没有提供 URL，也没有提供 FileId** → **FileId 是必传参数，必须询问用户提供 FileId，不得生成命令**

2.5. **🚨 参数追问规则（必须严格遵守）**：
   - **🔴 若任意必填参数缺失，必须立即向用户追问并停止——禁止生成任何命令，禁止使用占位符，禁止用假定的默认值继续执行。** 此规则优先级最高，适用于所有脚本。必填参数包括但不限于：FileId / URL / 本地文件路径（媒体输入类）、TaskId（任务查询类）、ElementId（涉及 `--element-ids` 时）、模板名（`procedure` 类）、参考图列表（多图 AIGC 类）、`--target-format`（转封装类）、`--scene`（场景转码类）等。如对某参数是否必填存疑，必须查阅对应的 `references/*.md` 文档——若文档标注为必填且用户未提供值，必须先追问。
   - **仔细阅读用户请求中已提供的所有参数**，只对真正缺失的必填参数追问，**严禁对用户已提供的参数再次追问**
   - **鉴权信息（SecretId/SecretKey/Token）由环境变量统一管理，严禁追问**，直接生成命令即可
   - **有默认值的可选参数不得追问**（如 `--model` 默认 Hunyuan、`--sub-app-id` 可从环境变量读取），直接省略由脚本使用默认值
   - **`--sub-app-id` 若用户未显式提供，不要追问，直接省略**（运行时从环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 自动读取）
   - **🚫 严禁使用占位符代替缺失的必填参数**：当用户未提供某个必填参数（如 FileId、URL、模板 ID、参考图列表等）时，**禁止生成含 `<xxx>`、`YOUR_XXX`、`/path/to/...`、`<MEDIA_URL>` 等任何占位符形式的命令**，必须直接向用户追问该参数的具体值，等用户提供后再生成命令。输出"含占位符的模板命令 + 提示用户'请将 XXX 替换为你的实际值'"也属于**明确禁止**的行为，等同于违反上述追问规则。

3. **🚨 生成命令前必须加载参数文档**：确定要使用的脚本后，根据上方「脚本功能映射」表中对应的文档链接，加载该 references 文档，获取参数细节后再生成命令。**禁止在未加载文档的情况下直接凭记忆生成命令**，因为直接凭记忆生成命令会导致参数错误。

4. **组合任务必须分别生成所有命令**：当用户请求涉及多个步骤（如先上传再转码）时，必须**分别生成独立的完整命令**，不得遗漏任何一条。

5. **行为修饰词规则**：`dry run`、`不等待`、`先预览命令`、`先提交任务` 等修饰词时，仍然需要触发此 Skill，这些词只影响命令参数（`--dry-run`），不影响任务类型判断。

---

## 特殊场景说明

### 拉取上传 vs 本地上传

> 🚨 **强制规则**：从 URL 拉取上传，**推荐且优先**使用专用脚本 `vod_pull_upload.py`（无子命令，直接跟参数）。
> - ✅ 推荐：`python scripts/vod_pull_upload.py --url "https://..."`
> - ⚠️ 可用但不推荐：`python scripts/vod_upload.py pull --url "https://..."` ← `vod_upload.py` 有 `pull` 子命令，功能相同，但推荐使用专用脚本
> - ❌ 错误：`python scripts/vod_upload.py --url "https://..."` ← `vod_upload.py` 不接受直接的 `--url` 参数，必须加子命令
>
> `vod_pull_upload.py` **没有子命令**，直接跟参数 `--url`。

### 转码类型选择

- **降低带宽成本、保持画质** → `transcode`（极速高清，TESHD）
- **换格式不重新编码** → `remux`（转封装）
- **提升画质、降噪、超分** → `enhance`（视频增强）

> ⚠️ **remux 参数强制规则**：
> - `--target-format`：**必填**，值为 `mp4` 或 `hls`，不可省略
> - `--tasks-priority`：任务优先级（-10 到 10），**⚠️ 不是 `--priority`**，`--priority` 是 `scene-transcode` 专用参数，两者不可混用
> - 正确示例：`vod_process_media.py remux --file-id xxx --target-format hls --tasks-priority 5`
- **特定业务场景**（短剧/电商/信息流） → `scene-transcode`
- **截图/动图/雪碧图/封面/自适应码流** → `snapshot`/`gif`/`image-sprite`/`cover-by-snapshot`/`adaptive-streaming`
- **AI 分析/识别/审核** → `ai-analysis`/`ai-recognition`/`ai-review`

> ⚠️ **区分极速高清 vs 场景转码**：极速高清用 `transcode --quality hd/sd/flu/same`；场景转码（短剧/电商/信息流）用 `scene-transcode --scene xxx`。两者完全不同，不要混用。

### 媒体搜索选择

- 有 FileId **且需要完整媒体详情**（转码/截图/字幕/封面/元数据等） → `vod_describe_media.py`
- 按 **FileId 列表精确搜索/过滤**（用户说"按FileId搜索/查询"、"FileId列表查询"） → `vod_search_media.py --file-ids`
- 名称/标签/分类模糊搜索 → `vod_search_media.py`（参数 `--names`，不是 `--keyword`）
- 自然语言描述内容（需先导入知识库） → `vod_search_media_by_semantics.py`（参数 `--text`，不是 `--query`）

> ⚠️ **关键区分**：`vod_describe_media.py` 用于查询已知 FileId 的完整详情；`vod_search_media.py --file-ids` 用于按 FileId 列表做搜索过滤，两者不要混用。

> 🚨 **`vod_describe_media.py` 参数强制规则**：FileId **必须用 `--file-id` 参数传入**，不支持位置参数。错误示例：`vod_describe_media.py 5145403721233902989`；正确示例：`vod_describe_media.py --file-id 5145403721233902989`。

### AIGC 任务状态查询路由

> ⚠️ **AIGC 生图任务**（TaskId 含 `AigcImage`，或用户明确说"查询 AIGC 生图任务"）→ **必须调用 `vod_aigc_image.py query --task-id <id>`**，禁止使用 `vod_describe_task.py`，禁止伪造或捏造 JSON 响应内容。
> ⚠️ **AIGC 生视频任务**（TaskId 含 `AigcVideo`）→ 使用 `vod_describe_task.py --task-id <id>`（`vod_aigc_video.py` 无 query 子命令）
> ✅ **通用任务查询**（转码/截图/增强等）→ `vod_describe_task.py --task-id <id>`

### AIGC 模型列表查询路由

> ⚠️ **三个 `models` 子命令完全不同，不要混用：**
> - **查看 LLM 对话支持的模型**（GPT/Gemini）→ `python scripts/vod_aigc_chat.py models`
> - **查看 AIGC 生图支持的模型** → `python scripts/vod_aigc_image.py models`
> - **查看 AIGC 生视频支持的模型** → `python scripts/vod_aigc_video.py models`

### AIGC 生图参数注意

> ⚠️ **模型名称格式**：`--model` 参数使用大写开头的模型名（如 `Hunyuan`、`GEM`），版本号通过 `--model-version` 单独指定。不要把版本号拼在模型名里。

> ✅ **Hunyuan 支持的版本**：`3.0`（默认）。用法：`--model Hunyuan --model-version 3.0`。Hunyuan 确实有 3.0 版本，这是有效版本号。

> ⚠️ **输出参数名称**：`vod_aigc_image.py` 的输出相关参数都带 `--output-` 前缀：`--output-resolution`、`--output-aspect-ratio`、`--output-storage-mode`、`--output-person-generation` 等。不要省略 `output-` 前缀。

> ⚠️ **参考图参数**：单张参考图用 `--file-id` 或 `--file-url`；多张参考图用 `--file-infos` 传 JSON 数组。不存在 `--file-ids` 参数。

### AIGC 生视频注意

> 生视频耗时较长（数分钟），默认自动等待完成，建议设置 `--max-wait 1800` 确保足够等待时间。

> ⚠️ **模型名和版本必须分开**：`--model` 只传模型名（如 `Kling`），版本号**必须**通过 `--model-version` 单独传入（如 `--model-version O1`）。**禁止**将版本号拼入模型名（如 `--model "Kling O1"` 是错误的）。
> 正确示例：`--model Kling --model-version O1`
> 错误示例：`--model "Kling O1"` ❌

> ⚠️ **场景类型**：Kling 支持 `motion_control`/`avatar_i2v`/`lip_sync`；Vidu 支持 `subject_reference`（固定主体场景）。通过 `--scene-type` 传入。

### AIGC LLM 多轮对话

> ⚠️ **多轮对话**：`--message` 只能传单条消息（最后一轮用户输入）。若需要多轮对话上下文，必须用 `--messages` 传完整的 JSON 数组（包含所有历史轮次）。不支持多次传 `--message`。

### 场景化生图提示词

> ⚠️ **各场景提示词参数名不同**：换衣场景用 `--change-prompt`，商品图场景用 `--product-prompt`，扩图场景无提示词参数。**不存在** `--prompt` 参数。

### 场景化生图输入文件规则（vod_scene_aigc_image.py）

> ⚠️ **`--input-files`、`--clothes-files` 格式为 `File:FileId` 或 `Url:URL`**。
> - 用户提供了本地图片路径 → 先用 `vod_upload.py upload --file <路径>` 上传，再用返回的 FileId 填入 `File:<FileId>`
> - 用户提供了图片 URL → 直接用 `Url:<URL>` 格式
> - 用户未提供任何图片/FileId → **FileId 是必传参数，必须询问**，不得生成命令

### 语义搜索前置条件

语义搜索（`vod_search_media_by_semantics.py`）要求媒体已通过 `vod_import_media_knowledge.py` 导入知识库。`--sub-app-id` 若用户未提供，**不要追问**，直接省略（运行时从环境变量 `TENCENTCLOUD_VOD_SUB_APP_ID` 自动读取）；若用户提供了 `--app-name` 则优先使用。

### AIGC 高级自定义主体

> ⚠️ **`--sub-app-id` 若用户未提供，不要追问，直接省略**（运行时从环境变量自动读取）。创建成功后任务信息自动记录到 `mem/elements.json`。

> ⚠️ **参数名称**：所有参数都带 `element-` 前缀：`--element-name`、`--element-description`、`--element-image-list`、`--element-video-list`、`--element-voice-id`。不存在 `--name`、`--image-list` 等简化参数。

> ⚠️ **`--element-description` 是必填参数**（虽然 `--help` 中显示为可选，但不传会报错）。

**参考方式（ReferenceType）**：
- `video_refer`：视频角色主体，通过参考视频定义外表，**支持绑定音色**
- `image_refer`：多图主体，通过多张图片定义外表，不支持绑定音色

**ElementId 获取流程**：创建时只返回 TaskId，ElementId 需等任务完成后通过 `vod_describe_task.py --task-id <id>` 查询获取（默认自动等待完成），自动合并保存到 `mem/elements.json`。

### 使用主体生视频（含 --element-ids 参数时必读）

> ⚠️ **触发条件**：当用户描述中提及"使用主体生视频"、"用角色/形象生视频"、"使用自定义主体 ElementId"等意图时（适用于 Kling O1、Kling 3.0-Omni 等所有支持 `--element-ids` 的模型），AI 负责：
> 1. 询问用户提供 ElementId 列表（若未提供，引导用户先创建主体并查询任务获取 ElementId）
> 2. 将用户的分段描述转换为带占位符的 Prompt 格式
> 3. 调用脚本并传入 `--element-ids` 或 `--elements-file`

> 🚨 **强制规则（最高优先级）**：只要用户提供了 ElementId（通过 `--element-ids` 传入），`--prompt` 中**必须**将主体的称谓（"主体"、"角色"、"他"、"她"等）替换为 `<<<element_1>>>`（多主体依次为 `<<<element_2>>>` 等）。**严禁**直接在 prompt 中写"主体"、"角色"等词语而不加占位符。

**Prompt 占位符构建规则**：用户可能以编号形式描述各段内容，AI 需将其转换为 `<<<element_N>>>` 格式：

| 用户输入 | 转换后的 --prompt |
|---------|-----------------|
| `1. 跳舞; 2. 奔跑` | `<<<element_1>>>跳舞 <<<element_2>>>奔跑` |
| `角色A跳舞，角色B奔跑` | `<<<element_1>>>跳舞 <<<element_2>>>奔跑` |
| `用主体跳舞` (单主体) | `<<<element_1>>>跳舞` |
| `主体在海边行走` (单主体) | `<<<element_1>>>在海边行走` |

占位符 `<<<element_N>>>` 中的 N 从 1 开始，与传入的 ElementId 列表顺序一一对应。

---

## API 参考

| 脚本 | 腾讯云官方文档 |
|------|------|
| `vod_upload.py` | [ApplyUpload](https://cloud.tencent.com/document/api/266/31767) / [CommitUpload](https://cloud.tencent.com/document/api/266/31766) |
| `vod_pull_upload.py` | [PullUpload](https://cloud.tencent.com/document/product/266/35575) |
| `vod_process_media.py` (procedure/transcode/remux/enhance/scene-transcode) | [ProcessMedia](https://cloud.tencent.com/document/product/266/33427) |
| `vod_process_media.py` (snapshot/gif/sample-snapshot/image-sprite) | [ProcessMedia](https://cloud.tencent.com/document/product/266/33427) |
| `vod_process_media.py` (ai-analysis/ai-recognition/ai-review) | [ProcessMedia](https://cloud.tencent.com/document/product/266/33427) |
| `vod_describe_media.py` | [DescribeMediaInfos](https://cloud.tencent.com/document/product/266/31763) |
| `vod_search_media.py` | [SearchMedia](https://cloud.tencent.com/document/product/266/31813) |
| `vod_search_media_by_semantics.py` | [SearchMediaBySemantics](https://cloud.tencent.com/document/product/266/126287) |
| `vod_describe_task.py` | [DescribeTaskDetail](https://cloud.tencent.com/document/product/266/33431) |
| `vod_describe_sub_app_ids.py` | [DescribeSubAppIds](https://cloud.tencent.com/document/product/266/36304) |
| `vod_aigc_chat.py` | [VOD AIGC LLM Chat](https://cloud.tencent.com/document/product/266/126561) |
| `vod_aigc_token.py` | [VOD AIGC Token 管理](https://cloud.tencent.com/document/api/266/128054) |
| `vod_aigc_image.py` | [CreateAIGCTask (Image)](https://cloud.tencent.com/document/product/266/126240) |
| `vod_aigc_video.py` | [CreateAIGCTask (Video)](https://cloud.tencent.com/document/product/266/126239) |
| `vod_process_image.py` (super-resolution) | [ProcessImageAsync SuperResolution](https://cloud.tencent.com/document/api/266/127858) |
| `vod_process_image.py` (understand) | [ProcessImageAsync Understand](https://cloud.tencent.com/document/api/266/127858) |
| `vod_scene_aigc_image.py` | [CreateSceneAIGCImageTask](https://cloud.tencent.com/document/api/266/126968) |
| `vod_create_scene_aigc_video_task.py` | [CreateSceneAIGCVideoTask](https://cloud.tencent.com/document/api/266/127542) |
| `vod_import_media_knowledge.py` | [ImportMediaKnowledge](https://cloud.tencent.com/document/product/266/126286) |
| `vod_create_aigc_advanced_custom_element.py` | [CreateAIGCCustomElement](https://cloud.tencent.com/document/api/266/129121) |


