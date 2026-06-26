---
name: xiaohongshu-ai
version: 1.0.5
description: 小红书 AI 宣传图和图文笔记技能 - 根据用户提示词判断生成单张或多张宣传图，调用 gpt-image-2 或火山引擎 Ark 文生图模型生成视觉素材并合成小红书图片；仅在用户明确要求发布到小红书时才执行发布。
homepage: https://www.xiaohongshu.com
author: OpenClaw Community
metadata: {"openclaw":{"emoji":"📕","primaryEnv":"XHS_COOKIE","category":"social-media"}}
---

# 小红书 AI 宣传图和图文笔记技能

> 一体化工作流：理解用户意图 → 主题和文案生成 → AI 图片模型直接生成单张或多张宣传图 → 按需发布

## 🎯 使用场景

- 用户需要创建小红书宣传图、封面图、产品推广图或图文笔记时
- 用户只提供一段产品、服务、活动、知识点或个人经历描述，需要自动转成小红书图文内容
- 需要 AI 直接生成贴合主题的单张海报或多张组图
- 批量创作多条笔记素材

## 🧭 意图判定与执行规则

先根据用户提示词判断目标，再选择生成和发布动作：

- **只生成不发布是默认行为**。用户没有明确说“发布到小红书”“帮我发小红书”“生成并发布”“发到小红书账号”等发布意图时，只生成图片和文案，不运行 `scripts/publish_xhs.py`。
- **只有明确要求发布到小红书才发布**。即使生成了标题、描述和 Tags，也不能自动发布；发布前必须能从用户原话中判断出发布意图。
- **单张宣传图**：用户说“一张”“单张”“封面”“海报”“主图”“宣传图”且没有要求组图时，生成一张主宣传图/封面图。
- **多张宣传图**：用户说“多张”“组图”“轮播”“N 张”“一套”“系列图”时，按用户指定数量生成；未指定数量时生成封面 + 3-5 张正文卡片，总数不超过 9 张。
- **图文笔记**：用户要求“小红书笔记”“种草文”“发布文案”“带正文分页”时，生成封面、正文卡片、发布描述和 Tags。
- **发布内容来源**：发布时使用生成目录里的 `manifest.json` 读取标题和 `publish_desc`，图片按 `cover.png`、`card_*.png` 顺序上传，最多 9 张。

执行顺序：

1. 理解用户提示词，确定主题、受众、卖点、语气、是否单张/多张、是否发布。
2. 调用 `gpt-image-2` 或火山引擎 Ark 文生图模型直接生成贴合主题的小红书规格宣传图。
3. 保存 `cover.png` / `card_*.png` 和 `manifest.json`。
4. 仅当用户明确要求发布到小红书时，再运行发布脚本。

## ✨ 核心功能

### 1️⃣ 智能内容创作
根据用户输入自动生成：
- **标题**：不超过 20 字，吸引眼球，制造好奇心
- **主题**：自动选择适合的视觉主题
- **正文分页**：多图时按卡片天然拆页，短句、强重点、适量 Emoji
- **发布文案**：生成描述和 SEO Tags

### 2️⃣ AI 宣传图生成
- 默认根据可用 Key 自动选择图片提供方：`OPENAI_API_KEY` 走 OpenAI，`ARK_API_KEY` 走火山引擎 Ark
- OpenAI 图片默认调用 `gpt-image-2`
- 火山图片默认调用 `doubao-seedream-4-5-251128`
- 火山文案默认调用 `doubao-seed-2-0-pro-260215`，可用 `--text-model` 切换
- 直接生成竖版、无 Logo、无水印的最终宣传图
- 单张输出 `cover.png`，多张输出 `cover.png` + `card_*.png`

### 3️⃣ 图片输出
- **封面图**：3:4 比例，默认 1024×1536px
- **正文图**：多张宣传图自动拆页，最多 9 张

### 4️⃣ 明确授权后发布
- 自动登录（使用 Cookie）
- 上传图片（最多 9 张）
- 设置标题、描述、Tags
- 发布后返回笔记链接
- 不允许在用户未明确要求发布时自动发布

## 🚀 快速开始

> ⚠️ **数据传输提示**：您输入的描述及生成的提示词等内容将发送至第三方 AI 服务（OpenAI 或火山引擎）进行处理。请勿在描述中包含商业机密、个人隐私或未公开的敏感信息。详见下方安全注意事项章节。

### 方式一：一句话自动生成（推荐）

```bash
# 只需要配置一种 API Key
export OPENAI_API_KEY="your_api_key"
# 或
export ARK_API_KEY="your_ark_api_key"

python3 scripts/generate_xhs.py \
  "给 蒙语 AI 翻译 API 写一篇小红书推广笔记，突出一个 API Key 搞定翻译、OCR 和语音识别" \
  -o ./output
```

生成结果：

```text
output/
├── manifest.json              # 结构化标题、主题、发布文案、Tags 和图片路径
├── cover.png
└── card_*.png
```

### 方式二：跳过图片生成，只生成结构化内容

```bash
python3 scripts/generate_xhs.py "你的描述" -o ./output --skip-image
```

### 方式三：指定单张或多张宣传图

```bash
# 单张宣传图，只输出 cover.png
python3 scripts/generate_xhs.py "你的描述" -o ./output --image-count 1

# 多张组图，总数包含封面，最多 9 张
python3 scripts/generate_xhs.py "你的描述" -o ./output --image-count 5
```

## 📁 文件结构

```
xiaohongshu-ai/
├── SKILL.md                 # 技能文档
├── scripts/
│   ├── generate_xhs.py      # 自动内容 + AI 宣传图生成脚本
│   ├── ai_services/         # 可扩展 AI 模型服务实现
│   │   ├── chatgpt_service.py
│   │   └── volcengine_service.py
│   └── publish_xhs.py       # 明确要求发布时使用的发布脚本
```

## 🤖 自动生成参数

### Python 脚本参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `description` | 用户输入的文字描述 | 必填或使用 `--input-file` |
| `--input-file` | 从文件读取描述 | 无 |
| `--output-dir`, `-o` | 输出目录 | `./output` |
| `--provider` | 服务提供方 | `openai`/`chatgpt` 或 `volcengine`/`ark`，默认根据可用 Key 自动选择 |
| `--text-model` | 主题和正文生成模型 | OpenAI 默认 `gpt-5-mini`，Ark 默认 `doubao-seed-2-0-pro-260215` |
| `--image-size` | 宣传图尺寸 | OpenAI 默认 `1024x1536`，火山默认 `2K` |
| `--image-quality` | OpenAI 宣传图质量 | `high` |
| `--ark-base-url` | 火山引擎 Ark OpenAI 兼容接口地址 | `https://ark.cn-beijing.volces.com/api/v3` |
| `--volcengine-watermark` | 火山图片生成时添加水印 | 关闭 |
| `--skip-image` | 不调用图片模型，只生成 `manifest.json` | 关闭 |
| `--image-count` | 目标输出图片总数，包含封面；单张宣传图使用 `1` | 不限制，按内容自动生成 |

### 常用命令

```bash
# 自动生成宣传图
python3 scripts/generate_xhs.py "你的描述" -o ./output

# 生成单张宣传图
python3 scripts/generate_xhs.py "你的描述" -o ./output --image-count 1

# 生成 5 张组图
python3 scripts/generate_xhs.py "你的描述" -o ./output --image-count 5

# 从文件读取需求描述
python3 scripts/generate_xhs.py --input-file brief.txt -o ./output

# 指定文案模型
python3 scripts/generate_xhs.py "你的描述" --text-model gpt-5-mini

# 使用火山引擎 Ark 文生图
python3 scripts/generate_xhs.py "你的描述" \
  --provider volcengine \
  --image-size 2K
```

## 📤 发布参数

发布是独立步骤，只能在用户明确要求”发布到小红书”时执行。

```bash
python3 scripts/publish_xhs.py \
  --title “笔记标题” \
  --desc “笔记描述 #标签 1 #标签 2” \
  --images cover.png card_1.png card_2.png

# 使用 glob 匹配所有图片（自然排序）
python3 scripts/publish_xhs.py \
  --title “笔记标题” \
  --desc “笔记描述” \
  --images-glob “./output/*.png”

# 从文件读取描述
python3 scripts/publish_xhs.py \
  --title “笔记标题” \
  --desc-file ./output/desc.txt \
  --images cover.png

# 验证模式（不实际发布）
python3 scripts/publish_xhs.py \
  --title “笔记标题” \
  --desc “笔记描述” \
  --images cover.png \
  --dry-run

# 设为公开笔记（默认为私密）
python3 scripts/publish_xhs.py \
  --title “笔记标题” \
  --desc “笔记描述” \
  --images cover.png \
  --public

# 定时发布
python3 scripts/publish_xhs.py \
  --title “笔记标题” \
  --desc “笔记描述” \
  --images cover.png \
  --post-time “2024-01-01 12:00:00”
```

### 发布参数一览

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--title`, `-t` | 笔记标题（不超过 20 字） | 必填 |
| `--desc`, `-d` | 笔记描述/正文内容 | `””` |
| `--desc-file` | 从 UTF-8 文件读取描述 | 无 |
| `--images`, `-i` | 图片文件路径（空格分隔） | 无 |
| `--images-glob` | 使用 glob 匹配图片，按自然序排序 | 无 |
| `--require-image-count` | 要求图片数量必须等于该值 | 不限制 |
| `--private` | 设为私密笔记（默认） | 默认开启 |
| `--public` | 设为公开笔记 | 关闭 |
| `--post-time` | 定时发布时间（`2024-01-01 12:00:00`） | 立即发布 |
| `--dry-run` | 仅验证，不实际发布 | 关闭 |
| `--verbose` | 显示底层库输出 | 关闭 |
| `--debug-json` | 将发布结果写入 JSON 文件 | 无 |
| `--yes`, `-y` | 兼容旧参数（当前脚本不再交互确认） | — |

### 前置条件

1. **配置 API Key（二选一即可）**：
   - `export OPENAI_API_KEY="your_api_key"`
   - `export ARK_API_KEY="your_ark_api_key"`

2. **配置 Cookie**（发布时必须使用环境变量）：
   - `export XHS_COOKIE="your_cookie_string"`

3. **获取 Cookie**：
   - 浏览器登录 https://www.xiaohongshu.com
   - F12 → Network → 查看请求头 Cookie
   - 复制完整 Cookie 字符串

## ⚠️ 安全注意事项（重要）

### Cookie 与账号安全

- **Cookie 相当于账号密码**：完整的小红书 Cookie 字符串是 Bearer Token，持有它的任何程序都能以您的身份操作账号（发布、编辑、删除内容等）。请像对待密码一样保护它。
- **不要提交到版本控制**：请勿将 Cookie 写入 git 仓库中的任何文件。
- **明文存储风险**：环境变量以明文保存 Cookie，请确保运行环境安全可控。
- **定期轮换**：建议定期重新获取 Cookie；不再使用时及时在浏览器中退出登录使其失效。
- **发布前无确认**：脚本不会在执行发布前要求用户确认，调用即发布。请确保在调用前已核对标题、描述和图片内容。如需验证而不实际发布，请使用 `--dry-run` 参数。

### 第三方 AI 服务数据传输

- **文案生成**：您输入的产品描述、品牌信息和营销内容会发送到 OpenAI 或火山引擎的服务器用于生成文案。请避免在描述中包含商业机密、个人隐私或未公开的产品信息。
- **图片生成**：生成的视觉提示词（visual_prompt）和卡片内容会发送到外部图片生成服务（gpt-image-2 或火山引擎 Ark）。这些服务提供方有各自的数据处理政策。
- **了解服务条款**：使用前请确认所用 AI 服务提供方的数据隐私政策，评估数据传输是否符合您的合规要求。

## ⚠️ 其他注意事项

1. **图片规格**：
   - 封面：1080×1440px（3:4）
   - 正文卡片：1080×1440px（可动态调整）
   - 最多 9 张图片

2. **Cookie 有效期**：
   - Cookie 有有效期，过期需重新获取
   - 建议定期更新 `XHS_COOKIE`

3. **发布限制**：
   - 标题不超过 20 字
   - 描述不超过 1000 字
   - Tags 不超过 10 个

4. **内容规范**：
   - 遵守小红书社区规范
   - 避免违规内容
   - 原创内容优先

## 🔧 依赖安装

```bash
pip install openai xhs
```
