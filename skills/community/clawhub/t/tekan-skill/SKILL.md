---
name: tekan-skill
description: "生成、编辑、协作。一个工具包接入所有主流 AI 模型。只需描述你的创意，即可生成视频、图片和数字人——零手动操作。当用户提到以下任何内容时使用此技能：特看视频、生成视频或图片、数字人、口型同步、文字转语音、TTS、声音克隆、去除背景、商品模特图、电商图、商品详情图、商品主图、虚拟穿搭、图片转视频、文字转视频、AI 图片编辑，或任何创意内容生成工作流——即使他们没有明确说出具体工具名或'特看视频'。"
metadata:
  tags: tekan, 特看视频, avatar, video, image, voice, ai, api, i2v, t2v, omni, text2image, image_edit, tts, voice_clone, board, ecommerce, product_detail
  requires:
    bins: [python3]
---

# 特看视频 AI Skill

> [特看视频](https://tekan.cn) API 的模块化 Python 工具包。

✨ **生成 · 编辑 · 协作 —— 一站搞定** ✨

- 🧠 **全主流模型**：一个工具包无缝接入全球顶级 AI 视频、图片、语音模型。
- 🗣️ **描述即创作**：告诉 Agent 你想要什么——从数字人到商品合成图，你的提示词直接生成成品。
- ⚡ **零手动操作**：无需手动上传，无需繁琐调整，一切自动完成并同步到你的在线看板。

## 功能概览

> 你不需要了解任何 API 细节。只需描述你想要什么——Agent 会阅读下方技术文档并自动处理一切。

**单项任务——一句话，一个结果：**

- 描述一张图片，几秒钟内生成——或一次批量生成一整套
- 上传一张人像和一段文案，获得带口型同步的数字人视频
- 将任意静态图片变成视频片段
- 纯文字描述即可生成视频
- 去除背景、编辑图片、替换场景——全靠描述即可完成
- 一句话把你的产品放到模特身上
- 克隆你的声音，或从数百种声音中选择进行文字转语音
- 在网页看板上整理所有成果，便于预览和分享

**组合工作流——自由串联各项能力：**

这些能力可以任意组合。例如，告诉 Agent"用这张照片做一套完整的产品发布素材"，它会将去除背景、商品展示、数字人视频和图片生成串联成一条流水线——全在一次对话中完成。更多示例：

- 为故事板的每个场景生成图片，然后全部转换为视频片段
- 撰写脚本，用 3 种语言制作 TTS 配音，为每种语言创建数字人视频
- 从一个风格参考出发，批量生产一周的品牌风格统一的社交媒体图片和视频
- 上传人像 + 克隆声音，然后仅凭文字脚本生成无限量数字人节目
- 将一篇文章转化为多段教育视频系列，配以 AI 插图和主持人解说

## 执行规则

> **始终使用 `scripts/` 中的 Python 脚本。** 这些脚本处理了身份验证、S3 文件上传、自动轮询、超时恢复和结构化错误处理——如果绕过它们直接用 `curl` 或 HTTP 调用，会丢失所有这些功能，而且仅在身份验证环节就可能失败。

## 前置条件

- **Python 3.10+**
- 积分余额充足 — 参见 [references/user.md](references/user.md) 查询余额

```bash
pip install -r {baseDir}/scripts/requirements.txt
```

## 认证规则（必读）

> **严禁向用户索要 API Key、UID 或任何凭证。用户没有这些东西，也无法自行获取。**
> **授权链接只能通过运行 `auth.py login` 获得，用户没有其他渠道获取此链接。**

**Agent 必须遵守：**

1. **永远不要** 向用户索要任何密钥或凭证
2. **永远不要** 让用户自己运行命令
4. **永远不要** 跳过引导消息或自行编写安装结果摘要 — 必须使用下方模板

详细说明参见 [references/auth.md](references/auth.md)。

## 安装完成与登录引导（强制流程）

> **安装依赖完成后，Agent 必须严格按以下步骤执行，不可跳过、不可改写、不可自行编写替代文案。**

### 步骤 1 — 运行 `auth.py login`

```bash
python {baseDir}/scripts/auth.py login
```

命令会输出授权链接（Markdown 格式和裸 URL 两行），并尝试自动打开浏览器（无浏览器的环境下会静默跳过）。**无论浏览器是否打开，都必须从输出中提取这个 URL**，下一步要用。

### 步骤 2 — 发送引导消息（强制，原样使用以下模板）

> **⚠️ 极其重要 — 登录链接输出规则（必须逐字遵守）：**
> 1. 从步骤 1 的命令输出中提取完整的登录 URL
> 2. **必须同时输出两行链接**（兼容飞书和微信）：
>    - 第一行：Markdown 格式 `[👉 点击此处完成登录授权](https://实际链接)`（飞书可点击）
>    - 第二行：原始 URL 裸链接（微信可点击，微信不支持 Markdown）
> 3. **两行缺一不可**，禁止省略任何一行
> 4. **禁止**用 `<` `>` 尖括号包裹 URL，**禁止**留占位符不替换
>
>**⚠️ 微信平台发送方式强制规则**
- 登录引导消息必须通过 message(action=send) 工具发送，不可作为普通回复文本直接输出。
- 原因：微信在普通回复中会吞掉 Markdown 方括号 [] 符号，导致链接格式损坏。
- 通过 message 工具发送可以确保格式完整传递。

> ✅ 正确示例（两行都要有）：
> ```
> [👉 点击此处完成登录授权](https://api.tekan.cn/oauth/authorize?code=abc123)
> https://api.tekan.cn/oauth/authorize?code=abc123
> ```
> ❌ 错误示例（只有 Markdown，缺少裸 URL，微信用户无法点击）：
> ```
> [👉 点击此处完成登录授权](https://api.tekan.cn/oauth/authorize?code=abc123)
> ```
> ❌ 错误示例（只有裸 URL，缺少 Markdown，飞书会截断长链接）：
> ```
> https://api.tekan.cn/oauth/authorize?code=abc123
> ```
> ❌ 错误示例（占位符未替换）：
> ```
> [👉 点击此处完成登录授权](<LOGIN_URL>)
> ```

将 `<LOGIN_URL>` 替换为步骤 1 获得的实际授权链接后，**原样发送以下消息给用户**：

```
安装完成，特看视频技能已连接到你的智能助手。

点击下方链接完成登录，登录后将解锁以下能力：
[👉 点击此处完成登录授权](<LOGIN_URL>)
<LOGIN_URL>

🎬 视频生成
文字转视频、图片转视频、参考视频生成，自动配音配乐。
视频模型：地表最强模型S2.0-白名单版（支持上传真人图） · 拟真世界模型 V2 · 可灵 V3 · 电影级画质模型 V3.1 · Vidu Q3 Pro · 万象 V2.6

🖼 AI 图片生成与编辑
文字生图、AI 修图、风格转换，最高支持 4K。
图片模型：全能图片模型 V2 · Seedream 5.0 · 强语义理解模型 V1.5 · 照片级写实模型 V4 · 强上下文一致性模型 pro

🧑 口播数字人
上传一张照片 + 文案，自动生成真人口播视频，支持多语种。

✂ 背景移除
一键抠图，产品图、人像、任意图片秒去背景。

🔺 产品模特图
把你的产品图放到模特身上，自动生成带货展示图。

🛍 电商图生成（13 种）
上传商品图即可一键生成电商所需的各类图片：
· 商品详情图 — AI 自动提取卖点、选择模块、生成整套详情页图片
· 商品主图 — 白底图/场景主图，一键生成
· 虚拟穿搭 — 把商品穿到模特身上
· 服装细节图 — 生成服装指定部位的细节放大图
· 商品3D图 — 生成产品3D渲染展示
· 商品换背景 — 替换商品图背景场景
· 商品图精修 — AI 自动提升图片质量
· 商品平铺图 — 生成产品平铺展示信息图
· 商品套图 — 多角度/多场景批量生成
· 服装种草图 — 生成穿搭种草风格展示图
· 智能去水印 — 清除图片水印
· 服装材质增强 — 修复服装图材质细节
· 爆款套图 — 参考爆款风格多轮批量生成套图

🎙 语音与配音
文字转语音、声音克隆，支持多语种配音输出。

登录完成后回我一句"好了"，我马上继续。
```


**禁止行为：**
- 不可省略模板中的任何部分
- 不可用自己的话概括或改写
- 不可在用户授权前展示能力列表的简化版本
- `<LOGIN_URL>` 必须替换为真实 URL，模板中两处 `<LOGIN_URL>` 都要替换，不可留空或写占位符
- **禁止**省略 Markdown 链接行或裸 URL 行中的任何一行，两行都必须出现

### 步骤 3 — 等待用户授权

用户在浏览器中完成登录和授权后，会回复"好了"。此时 `auth.py login` 应已自动检测到授权并保存凭证到 `~/.tekan/credentials.json`。

### 步骤 4 — 验证登录状态

```bash
python {baseDir}/scripts/auth.py status
```

确认输出包含 `Logged in` 后，告知用户"登录成功，所有功能已解锁"，即可开始正常使用。

## Agent 工作流规则

> **以下规则适用于所有生成模块（avatar4, video_gen, ai_image, remove_bg, product_avatar, text2voice）。**

1. **始终从 `run` 开始** — 它会提交任务并自动轮询直到完成。这是默认且正确的选择，几乎适用于所有场景。
2. **Agent 负责轮询循环** — 用户期望无需干预的体验，因此 Agent 应持续轮询直到任务完成或超时，而不是让用户手动检查状态。
3. **`query` 仅用于恢复** — `query` 仅在 `run` 已超时且你有 `taskId` 需要恢复时有用，或用户主动提供了已有的 `taskId`。对新请求直接用 `query` 会失败，因为没有任务可轮询。
4. **`query` 持续轮询** — 它每隔 `--interval` 秒检查一次状态，直到状态为 `success` 或 `fail`，或 `--timeout` 到期。不会只检查一次就停止。
5. **如果 `query` 也超时**（退出码 2），增加 `--timeout` 并使用相同的 `taskId` 重试。除非任务确实失败，否则不要重新提交。

```
决策树：
  → 新请求？               使用 `run`
  → run 超时了？           使用 `query --task-id <id>`
  → query 也超时了？       使用 `query --task-id <id> --timeout 1200`
  → 任务状态=fail？        用 `run` 重新提交
```

**任务状态：**

| 状态 | 说明 |
|--------|-------------|
| `init` | 任务已排队，等待处理 |
| `running` | 任务正在处理中 |
| `success` | 任务成功完成 |
| `fail` | 任务失败 |

## 看板 ID 协议（强制）

> **每个生成任务都必须包含 `--board-id`。缺少看板 ID 会导致用户无法在网页上查看和编辑结果。**

1. **会话开始（必须）** — 在提交第一个任务之前，**必须先**运行 `board.py list --default -q` 获取默认看板 ID（"My First Board"）。每个会话只需执行一次。**不可跳过此步骤。**
2. **传递给所有任务（必须）** — 为每个生成命令添加 `--board-id <id>`（`avatar4.py`、`video_gen.py`、`ai_image.py`、`product_avatar.py`、`text2voice.py`、`ecommerce_image.py`）。
3. **任务完成后（必须）** — 从任务结果中提取 `boardTaskId`，按下方「视频/图片结果模板」展示项目链接。每个链接必须同时输出 Markdown 格式和原始 URL 两行（兼容飞书和微信）。**每次任务完成都必须展示此链接**，告诉用户可以点击查看和编辑结果。
4. **用户想要新看板** — 运行 `board.py create --name "..."` 并将返回的看板 ID 用于后续任务。
5. **用户指定了看板** — 使用用户提供的看板 ID 而非默认值。
6. **忘记了看板 ID？** — 再次运行 `board.py list --default -q`。

```
会话流程：
  1. BOARD_ID = $(board.py list --default -q)
  2. avatar4.py run --board-id $BOARD_ID ...
  3. video_gen.py run --board-id $BOARD_ID ...
  4. (结果中显示包含 boardTaskId 的编辑链接)
```

## 模块列表

| 模块 | 脚本 | 参考文档 | 说明 |
|--------|--------|-----------|-------------|
| Auth | `scripts/auth.py` | [auth.md](references/auth.md) | OAuth 2.0 设备授权流程 — 浏览器登录，保存凭证 |
| Avatar4 | `scripts/avatar4.py` | [avatar4.md](references/avatar4.md) | 从照片生成数字人视频；`list-captions` 查看字幕样式 |
| Video Gen | `scripts/video_gen.py` | [video_gen.md](references/video_gen.md) | 图片转视频、文字转视频、Omni 参考（从参考视频/图片/音频/文字生成视频） |
| AI Image | `scripts/ai_image.py` | [ai_image.md](references/ai_image.md) | 文字生图和 AI 图片编辑（10+ 模型） |
| Remove BG | `scripts/remove_bg.py` | [remove_bg.md](references/remove_bg.md) | 去除图片背景 — 商品模特图工作流的第一步 |
| Product Avatar | `scripts/product_avatar.py` | [product_avatar.md](references/product_avatar.md) | 商品模特展示图；`list-avatars`/`list-categories` 浏览模板 |
| Text2Voice | `scripts/text2voice.py` | [text2voice.md](references/text2voice.md) | 文字转语音音频 |
| Voice | `scripts/voice.py` | [voice.md](references/voice.md) | 声音列表/搜索、声音克隆、删除自定义声音 |
| Ecommerce Image | `scripts/ecommerce_image.py` | [ecommerce_image.md](references/ecommerce_image.md) | 电商图生成（13 种类型）：商品详情图、电商主图、虚拟穿搭、换背景等 |
| Board | `scripts/board.py` | [board.md](references/board.md) | 看板管理 — 整理结果，在网页上查看/编辑 |
| User | `scripts/user.py` | [user.md](references/user.md) | 积分余额和使用记录 |
| 模型名称映射 | — | [model_mapping.md](references/model_mapping.md) | 模型 API 名称与用户展示名称的映射规则 |

> **请阅读各模块的参考文档了解用法、选项和代码示例。**
> 本地文件（图片/音频/视频）作为参数传入时会自动上传——无需手动上传步骤。

---

## 创作指南

> **核心原则：** 从用户意图出发，而非从 API 出发。
> 分析用户想要实现什么，然后选择合适的工具、模型和参数。
>
> **语言规则（强制）：** 用户用什么语言沟通，生成内容就用什么语言。用户说中文，则 `--text`（TTS 文案）、`--prompt`（提示词）、脚本内容等全部使用中文。除非用户明确要求使用其他语言。

### 第零步 — 快速匹配（优先于意图分析）

**如果用户消息明确匹配以下任何关键词，跳过意图分析，直接执行对应命令：**

| 关键词 | 直接执行 |
|--------|----------|
| 商品详情图、详情页、做详情 | `ecommerce_image.py run --tool-type product_detail_image --images <用户图片>` — 读 [ecommerce_image.md](references/ecommerce_image.md) 获取模块选择规则 |
| 电商主图、白底图 | `ecommerce_image.py run --tool-type product_main_image_ecomm --images <用户图片>` |
| 虚拟穿搭 | `ecommerce_image.py run --tool-type virtual_try_on_ecomm --images <商品图> --model-image <模特图>` |
| 爆款套图、网红打卡、打卡地、旅游穿搭 | `ecommerce_image.py run --tool-type trending_style_set_ecomm --mission-type 网红地打卡 --images <穿搭图> --model-ref <模特图> --scene-ref <打卡地图...>` |
| 好物plog、好物推荐、物品展示 | `ecommerce_image.py run --tool-type trending_style_set_ecomm --mission-type 好物plog --images <物品图...> --scene-ref <场景图...>` |
| 穿搭OOTD、每日穿搭、穿搭模板 | `ecommerce_image.py run --tool-type trending_style_set_ecomm --mission-type 穿搭OOTD --model-ref <穿搭图> --scene-ref <模板图>` |
| 萌宠带货、宠物带货 | `ecommerce_image.py run --tool-type trending_style_set_ecomm --mission-type 萌宠带货 --model-ref <宠物图> --scene-ref <场景图...> [--images <商品图>]` |
| 一衣多穿、多场景穿搭 | `ecommerce_image.py run --tool-type trending_style_set_ecomm --mission-type 一衣多穿 --images <服饰图> --model-ref <模特图> --scene-ref <场景图>` |
| 服装细节图 | `ecommerce_image.py run --tool-type garment_detail_view_ecomm --images <用户图片> --garment-type <top/bottom/dress> --detail-part <部位ID>` — **必须**根据用户描述查 [ecommerce_image.md](references/ecommerce_image.md) 部位映射表传 `--detail-part`（如：袖子→`top_cuff`，领口→`top_collar`，面料→`top_fabric`） |
| 商品换背景 | `ecommerce_image.py run --tool-type background_replacement_ecomm --images <商品图> --scene-image <背景图>` — 商品图=要换背景的图，背景图=目标背景/场景图（可选，不传则用 `--prompt` 描述） |
| 3D效果图、立体图、3D图、3D渲染、立体效果、服装3D、平铺转立体、做个立体、转为立体、变成3D | `ecommerce_image.py run --tool-type product_3d_render_ecomm --images <商品图> [参考图]` — **必须走特看视频生图，禁止本地 PIL/OpenCV 处理**。一张图=默认立体效果，两张图=参考第二张的3D效果 |
| 精修、图片精修 | `ecommerce_image.py run --tool-type image_retouching_ecomm --images <用户图片> --retouch-type <common/light/reflex/water>` — 通用精修=`common`，光影调整=`light`，底部反射=`reflex`，水花效果=`water`（默认 `common`） |
| 平铺图、提取服装、提取整套、提取穿搭、拆解穿搭 | `ecommerce_image.py run --tool-type product_flat_lay_ecomm --images <用户图片> --extraction-target <类型>` — 整套=`all`，上装=`tops`，下装=`bottoms`，鞋靴=`shoes`，包包=`bags`（默认 `all`） |
| 套图 | `ecommerce_image.py run --tool-type product_set_images_ecomm --images <用户图片> --image-count <张数>` — 用户指定几张就传几张，默认 1 张 |
| 种草图、穿搭种草 | `ecommerce_image.py run --tool-type lifestyle_fashion_photo_ecomm --images <用户图片> --scene <场景ID>` — 查 [ecommerce_image.md](references/ecommerce_image.md) 场景映射表选场景（默认 `scene_aesthetic`） |
| 去水印 | `ecommerce_image.py run --tool-type smart_watermark_removal_ecomm --images <用户图片>` |
| 材质增强、材质修复、修复图案、图案不全、纹理修复、服装纹理 | `ecommerce_image.py run --tool-type texture_enhancement_ecomm --images <待修复图> <高清参考图>` — **必须两张图**：第一张待修复，第二张高清参考（脚本自动对参考图去背景） |
| 电商图（泛指）| `ecommerce_image.py list-tools` 列出 13 种类型让用户选 |

**匹配到以上关键词时：不要问风格、用途、渠道等问题。用户已经发了图就直接开始执行。** 没发图时只需要求提供图片，不问其他问题。

### 第一步 — 意图分析

> 仅在第零步未匹配时执行。

每次用户请求内容时，识别以下维度：

| 维度 | 自问 | 兜底方案 |
|-----------|-------------|----------|
| **输出类型** | 图片？视频？音频？组合？ | 必须询问 |
| **用途** | 营销？教育？社交媒体？个人？ | 通用社交媒体 |
| **源素材** | 用户有什么？缺什么？ | 必须询问 |
| **风格/调性** | 专业？休闲？活泼？权威？ | 专业且友好 |
| **时长** | 输出应该多长？ | 片段 5–15 秒，数字人 30–60 秒 |
| **语言** | 什么语言？需要字幕吗？ | **必须**匹配用户的语言（中文用户 → 中文提示词/文案/脚本） |
| **渠道** | 将在哪里发布？ | 通用 |

### 第二步 — 工具选择

```
用户需要什么？
│
├─ 真人对着镜头说话（数字人）？
│  → avatar4 或 video_gen 的原生音频模型
│
├─ 把一张图片变成视频片段？
│  → video_gen --type i2v
│
├─ 纯文字生成视频？
│  → video_gen --type t2v
│
├─ 基于参考素材生成新视频（风格迁移、编辑）？
│  → video_gen --type omni
│
├─ 从文字提示生成图片？
│  → ai_image --type text2image
│
├─ 编辑/修改现有图片？
│  → ai_image --type image_edit
│
├─ 去除图片背景（如商品抠图）？
│  → remove_bg
│
├─ 将商品放到模特/数字人场景中？
│  → product_avatar（如果商品有背景，先用 remove_bg）
│  → product_avatar list-avatars 浏览公共模板
│
├─ 生成电商商品详情页图片（多模块长图）？
│  → ecommerce_image --tool-type product_detail_image
│
├─ 生成电商主图 / 商品换背景 / 虚拟穿搭 / 3D效果图 / 其他电商图？
│  → ecommerce_image --tool-type <对应类型>
│  → ecommerce_image list-tools 查看所有 13 种电商图类型
│
├─ 浏览可用的字幕样式？
│  → avatar4 list-captions
│
├─ 文字转语音？
│  → text2voice
│
├─ 查找声音 / 列出可用声音？
│  → voice list
│
├─ 从音频样本克隆声音？
│  → voice clone
│
├─ 删除自定义声音？
│  → voice delete
│
├─ 管理看板 / 在网页上查看结果？
│  → board (list, create, detail, tasks)
│
├─ 组合需求（如数字人 + 产品片段）？
│  → 使用配方（见第三步）
│
└─ 超出当前能力范围？
   → 见下方能力边界
```

**快速路由参考表：**

| 用户说… | 脚本和类型 |
|----------------------------------------------|-------------|
| "用这张照片和文字做一个数字人视频" | `avatar4.py`（直接传入本地图片路径） |
| "用这张照片和我的录音生成视频" | `avatar4.py`（传入本地图片 + 音频路径） |
| "把这张图片变成视频 / 图片转视频" | `video_gen.py --type i2v`（传入本地图片路径） |
| "生成一个关于…的视频" | `video_gen.py --type t2v` |
| "参考这张图片的风格生成新视频" | `video_gen.py --type omni` |
| "生成一张图片 / 文字生图" | `ai_image.py --type text2image` |
| "修改这张图片 / 换背景" | `ai_image.py --type image_edit` |
| "去除图片背景 / 抠图" | `remove_bg.py` |
| "把这个产品放到模特图上" | `product_avatar.py`（如果产品有背景，先用 `remove_bg.py`） |
| "有哪些商品模特模板？" | `product_avatar.py list-avatars` |
| "有哪些字幕样式？" | `avatar4.py list-captions` |
| "把这段文字转成语音 / 音频" | `text2voice.py` |
| "有哪些可用的声音？/ 找一个女声" | `voice.py list --gender female` |
| "用这段录音克隆声音" | `voice.py clone --audio <file>` |
| "删除这个自定义声音" | `voice.py delete --voice-id <id>` |
| "查看我的看板 / 看看生成了什么" | `board.py list` 或 `board.py tasks --board-id <id>` |
| "创建一个新看板" | `board.py create --name "..."` |
| "帮我做一套商品详情图" | `ecommerce_image.py run --tool-type product_detail_image` |
| "换个背景 / 白底图" | `ecommerce_image.py run --tool-type background_replacement_ecomm --scene-image <背景图>` |
| "做个3D效果 / 立体图 / 平铺转立体 / 做个立体效果" | `ecommerce_image.py run --tool-type product_3d_render_ecomm --images <商品图> [参考图]` — **禁止本地处理，必须调特看视频** |
| "精修商品图 / 加水花效果" | `ecommerce_image.py run --tool-type image_retouching_ecomm --retouch-type <common/light/reflex/water>` — 水花=`water`，光影=`light`，默认`common` |
| "生成电商主图" | `ecommerce_image.py run --tool-type product_main_image_ecomm` |
| "虚拟穿搭" | `ecommerce_image.py run --tool-type virtual_try_on_ecomm --model-image <模特图>` |
| "服装细节图" | `ecommerce_image.py run --tool-type garment_detail_view_ecomm --garment-type <top/bottom/dress> --detail-part <部位ID>` — 必须查映射表 |
| "做平铺图 / 提取服装 / 提取整套 / 拆解穿搭" | `ecommerce_image.py run --tool-type product_flat_lay_ecomm --extraction-target <类型>` — 默认 `all` |
| "做套图 / 多角度套图" | `ecommerce_image.py run --tool-type product_set_images_ecomm --image-count <张数>` |
| "做种草图" | `ecommerce_image.py run --tool-type lifestyle_fashion_photo_ecomm --scene <场景ID>` — 默认 `scene_aesthetic` |
| "去水印" | `ecommerce_image.py run --tool-type smart_watermark_removal_ecomm` |
| "材质增强 / 修复图案 / 纹理修复" | `ecommerce_image.py run --tool-type texture_enhancement_ecomm --images <待修复图> <高清参考图>` — **需两张图** |
| "爆款套图 / 网红打卡 / 好物plog / 一衣多穿" | `ecommerce_image.py run --tool-type trending_style_set_ecomm --mission-type <类型> --images <商品图> --model-ref <模特> --scene-ref <场景>` |
| "看看我还剩多少积分" | `user.py credit` |

> **视频模型选择** — 参见 [references/video_gen.md](references/video_gen.md) § 模型推荐。

> **图片模型建议：** 所有图片任务默认使用**全能图片模型 V2** — 综合最强模型，画质最佳，支持 14 种宽高比、最高 4K、编辑时支持 14 张参考图。参见 [references/ai_image.md](references/ai_image.md) § 模型推荐。

> **商品模特图工作流：** 为获得最佳效果，使用两步流程：先用 `remove_bg.py` 获取 `bgRemovedImageFileId`，再用 `product_avatar.py` 配合 `--product-image-no-bg`。使用 `product_avatar.py list-avatars` 浏览公共模板并获取 `avatarId`。参见 [references/product_avatar.md](references/product_avatar.md) § 完整工作流。

> **avatar4 字幕样式：** 使用 `avatar4.py list-captions` 查看可用字幕样式，然后通过 `--caption` 传入 `captionId`。

> **电商图工作流：** 使用 `ecommerce_image.py` 生成电商场景图片。`list-tools` 查看全部 13 种功能类型，`list-modules` 查看商品详情图的 16 个模块。**执行原则：不要反复提问，用户提供商品图后立即执行。** `--modules` 可以省略（脚本有默认值），Agent 也可以根据品类自己选。详见 [references/ecommerce_image.md](references/ecommerce_image.md) § Agent 行为规则。

> **数字人建议 — avatar4 vs video_gen 原生音频：**
> 部分 video_gen 模型（如地表最强模型S2.0-白名单版（支持上传真人图）、可灵 V3、电影级画质模型 V3.1）支持原生音频，可以生成比 avatar4 **画质更好**的数字人视频。但它们**最大时长更短**（5–15 秒）且**价格明显更高**。Avatar4 支持单段最长 120 秒，成本低得多。
> **经验法则：** 目标视频时长小于 15 秒时，默认使用 video_gen 原生音频模型；否则默认使用 avatar4。但你应该始终向用户说明各自优缺点并征求偏好。

### 第三步 — 简单 vs 复杂

**简单请求** — 用户需求明确，素材就绪 → 直接根据参考文档处理。

**复杂请求** — 用户给出的是*目标*（如"做一个推广视频"、"解释 AI 的工作原理"），而非直接的 API 指令。遵循以下通用工作流：

1. **拆解与确认：** 向用户询问目标受众、核心信息、期望时长，以及他们目前有哪些素材（照片、脚本）。
2. **确定路线：**
   - *有人像照片 + 需要解说* → 使用 `avatar4`（数字人）。
   - *有产品/参考照片* → 使用 `video_gen --type i2v` 或 `omni`。
   - *没有素材，纯视觉概念* → 使用 `video_gen --type t2v`。
   - *两者都需要* → 规划混合方案（数字人解说 + B-roll 插入）。
3. **组织内容：**
   - 撰写结构化脚本（开头吸引 → 主体/讲解 → 行动号召）。
   - 在 TTS 脚本中添加 `<break time="0.5s"/>` 标签以实现自然节奏。
   - 对于视觉内容，撰写详细提示词，涵盖主体 + 动作 + 光照 + 镜头。
4. **处理长内容（>120 秒）：** 如果脚本超过单个 `avatar4` 任务的 120 秒限制，在自然句子边界处将其分成逻辑段落（如每段 60 秒）。使用 `submit` 命令并行提交任务，确保各段参数（声音/模型）一致，并按顺序交付。

---

## 执行前协议

> 每个生成任务前都遵循此协议。

1. **估算费用** — 视频任务使用 `video_gen.py estimate-cost`，图片任务使用 `ai_image.py estimate-cost`，电商图使用 `ecommerce_image.py estimate-cost`；avatar4 费用取决于视频时长；product_avatar 固定 0.5 积分；text2voice 固定 0.1 积分
2. **验证参数** — 确保模型、宽高比、分辨率和时长兼容（使用 `list-models` 检查）
3. **询问缺失的关键参数** — 如果用户未指定影响输出的重要参数，在执行前询问。各模块关键参数：
   - **video_gen**：时长、宽高比、模型
   - **ai_image**：宽高比、分辨率、模型、图片数量
   - **avatar4**：（通常由输入决定，但如未指定声音则需确认）
   - **text2voice**：声音选择
   - **ecommerce_image**：⚠️ **例外 — 不需要询问任何参数。** 模块由 Agent 自动选择，卖点自动提取，分辨率/宽高比有默认值。用户发了图就直接执行。
   - 这些参数显著影响输出质量和积分消耗，与用户确认可以避免浪费积分和令人失望的结果。
4. **首次提交前确认** — 在会话中首次执行生成任务前，展示方案（工具、模型、参数、费用估算）并在一条消息中询问：(a) 是否执行？(b) 逐个确认后续任务，还是本次会话剩余任务自动执行？如果用户一开始就说"直接做"，视为自动执行。即使在自动执行模式下，仍需询问缺失的关键参数。**例外：电商图（ecommerce_image）不需要首次确认——有图就直接执行。**

## 模型名称展示规则

> **严格遵守：对外展示用中文名，构造命令用 API 名。**

完整映射表见 [references/model_mapping.md](references/model_mapping.md)。

1. **与用户沟通时**（推荐模型、报告结果、确认方案）：使用映射后的**展示名称**，绝不暴露 API 真名。
2. **构造命令时**（`--model` 参数）：使用 **API 名称**。
3. **用户说出展示名称时**：自动识别并映射为 API 名称执行。
4. **禁止使用的模型**：`Lite`、`Pro`、`Plus`、`Best` — 不推荐、不使用、不提及。

**关键映射速查：**

| API 名称 → `--model` 参数 | 展示名称 → 对用户说 |
|---|---|
| `Standard` | 地表最强模型S2.0-白名单版（支持上传真人图） |
| `Fast` | 地表最强模型S2.0 Fast-白名单版（支持上传真人图） |
| `Kling V3` | 可灵 V3 |
| `Kling O3` | 可灵 O3 |
| `Sora 2 Pro` | 拟真世界模型 2 Pro |
| `Veo 3.1` | 电影级画质模型 V3.1 |
| `Veo 3.1 Fast` | 电影级画质模型 V3.1 fast |
| `Nano Banana 2` | 全能图片模型 V2 |
| `GPT Image 1.5` | 强语义理解模型 V1.5 |
| `Kontext-Pro` | 强上下文一致性模型 pro |
| `Imagen 4` | 照片级写实模型 V4 |

---

## Agent 行为协议

### 执行期间

1. **直接传入本地路径** — 脚本会在提交任务前自动将本地文件上传到 S3
2. **并行化独立步骤** — 相互独立的生成任务可以并发执行
3. **保持跨段一致性** — 生成多段内容时，使用相同的参数

### 执行完成后（必须全部执行）

> **模型名称必须使用展示名称，不得直接输出 API 名称。** 映射规则参见 [model_mapping.md](references/model_mapping.md)。

任务完成后，Agent **必须**按照以下模板向用户展示结果。将占位符替换为实际值。

**视频结果模板：**

```
🎬 视频已生成完成

[👉 点击播放/下载视频](<VIDEO_URL>)
<VIDEO_URL>
· 时长：<DURATION>
· 画幅：<ASPECT_RATIO>
· 模型：<MODEL_NAME>
· 消耗：<COST> credits

[🔗 项目链接（查看/编辑/下载）](https://tekan.cn/board/<BOARD_ID>?boardResultId=<BOARD_TASK_ID>)
https://tekan.cn/board/<BOARD_ID>?boardResultId=<BOARD_TASK_ID>

不满意的话可以告诉我，我帮你调整后重新生成。
```

**图片结果模板：**

```
🖼 图片已生成完成

[👉 点击查看/下载图片](<IMAGE_URL>)
<IMAGE_URL>
· 分辨率：<RESOLUTION>
· 模型：<MODEL_NAME>
· 消耗：<COST> credits

[🔗 项目链接（查看/编辑/下载）](https://tekan.cn/board/<BOARD_ID>?boardResultId=<BOARD_TASK_ID>)
https://tekan.cn/board/<BOARD_ID>?boardResultId=<BOARD_TASK_ID>

不满意的话可以告诉我，我帮你调整后重新生成。
```

**电商图结果模板（ecommerce_image.py 的 13 种功能）：**

```
🖼 <TOOL_NAME>已生成完成

[👉 点击查看/下载图片](<IMAGE_URL>)
<IMAGE_URL>
· 分辨率：<RESOLUTION>
· 功能：<TOOL_NAME>
· 消耗：<COST> credits

[🔗 项目链接（查看/编辑/下载）](https://tekan.cn/board/<BOARD_ID>?boardResultId=<BOARD_TASK_ID>)
https://tekan.cn/board/<BOARD_ID>?boardResultId=<BOARD_TASK_ID>

不满意的话可以告诉我，我帮你调整后重新生成。
```

> 电商图使用脚本输出的「功能: xxx」作为 `<TOOL_NAME>`（如「商品3D图」「服装种草图」），**不显示模型名称**。

**模板使用规则：**
1. `<MODEL_NAME>` 必须使用展示名称（例如：显示「地表最强模型S2.0-白名单版（支持上传真人图）」而非"Standard"，显示"强语义理解模型 V1.5"而非"GPT Image 1.5"）。**电商图功能除外**——电商图用「功能：<TOOL_NAME>」替代「模型：<MODEL_NAME>」
2. **每个链接必须同时输出两行**：第一行用 Markdown 格式 `[说明文字](完整URL)`（飞书可点击），第二行输出脚本返回的短链接（微信可点击）。两行缺一不可，直接使用脚本输出的短链，不要自己拼接
3. `<BOARD_ID>` 和 `<BOARD_TASK_ID>` 从任务返回结果中提取，**项目链接不可省略**
4. 多个输出时逐个编号展示
5. 其他类型任务（数字人、TTS、去背景等）参照以上格式，按实际字段调整

### 错误处理

参见 [references/error_handling.md](references/error_handling.md) 了解错误码、任务级失败和恢复决策树。

---

## 能力边界

| 能力 | 状态 | 脚本 |
|---------------------------------|--------------|----------------------------------------------------------|
| 照片数字人 / 口播视频 | 可用 | `scripts/avatar4.py` |
| 字幕样式 | 可用 | `scripts/avatar4.py list-captions` |
| 积分管理 | 可用 | `scripts/user.py` |
| 图片转视频 (i2v) | 可用 | `scripts/video_gen.py --type i2v` |
| 文字转视频 (t2v) | 可用 | `scripts/video_gen.py --type t2v` |
| Omni 参考视频 | 可用 | `scripts/video_gen.py --type omni` |
| 文字生图 | 可用 | `scripts/ai_image.py --type text2image` |
| 图片编辑 | 可用 | `scripts/ai_image.py --type image_edit` |
| 去除背景 | 可用 | `scripts/remove_bg.py` |
| 商品模特图 / 图片替换 | 可用 | `scripts/product_avatar.py` |
| 商品模特模板 | 可用 | `scripts/product_avatar.py list-avatars` / `list-categories` |
| 文字转语音 (TTS) | 可用 | `scripts/text2voice.py` |
| 声音列表 / 搜索 | 可用 | `scripts/voice.py list` |
| 声音克隆 | 可用 | `scripts/voice.py clone` |
| 删除自定义声音 | 可用 | `scripts/voice.py delete` |
| 看板管理 | 可用 | `scripts/board.py` |
| 看板任务浏览 | 可用 | `scripts/board.py tasks` / `task-detail` |
| 商品详情图（电商图） | 可用 | `scripts/ecommerce_image.py --tool-type product_detail_image` |
| 商品主图 | 可用 | `scripts/ecommerce_image.py --tool-type product_main_image_ecomm` |
| 虚拟穿搭 | 可用 | `scripts/ecommerce_image.py --tool-type virtual_try_on_ecomm` |
| 服装细节图 | 可用 | `scripts/ecommerce_image.py --tool-type garment_detail_view_ecomm --garment-type <type> --detail-part <部位ID>` |
| 商品3D图 | 可用 | `scripts/ecommerce_image.py --tool-type product_3d_render_ecomm` |
| 商品换背景 | 可用 | `scripts/ecommerce_image.py --tool-type background_replacement_ecomm --scene-image <背景图>` |
| 商品图精修 | 可用 | `scripts/ecommerce_image.py --tool-type image_retouching_ecomm --retouch-type <type>` |
| 商品平铺图 | 可用 | `scripts/ecommerce_image.py --tool-type product_flat_lay_ecomm --extraction-target <类型>` |
| 商品套图 | 可用 | `scripts/ecommerce_image.py --tool-type product_set_images_ecomm` |
| 服装种草图 | 可用 | `scripts/ecommerce_image.py --tool-type lifestyle_fashion_photo_ecomm --scene <场景ID>` |
| 智能去水印 | 可用 | `scripts/ecommerce_image.py --tool-type smart_watermark_removal_ecomm` |
| 服装材质增强 | 可用 | `scripts/ecommerce_image.py --tool-type texture_enhancement_ecomm --images <待修复图> <高清参考图>` |
| 爆款套图 | 可用 | `scripts/ecommerce_image.py --tool-type trending_style_set_ecomm --mission-type <类型>` |
| 营销视频 (m2v) | 无模块 | 建议使用 [特看视频](https://tekan.cn) 网页端 |

> 承诺一个没有对应模块的能力会导致工作流中途卡住，损害用户信任。如果请求超出上表范围，请建议用户使用[特看视频](https://tekan.cn)网页端。
