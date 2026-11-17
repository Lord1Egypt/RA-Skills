# xiaohongshu-ai

小红书 AI 宣传图、图文笔记和视频发布 skill。根据用户提示词判断生成单张或多张宣传图，支持使用 `gpt-image-2` 或火山引擎 Ark 文生图模型直接生成图片，也支持将用户提供的本地 MP4 发布为视频笔记；只有用户明确要求发布到小红书时才发布。

## 如何使用这个 skill

把这个目录安装到支持 skill 的工具或智能体环境后，在对话里直接描述你要做的小红书内容即可触发使用，例如：

```text
帮我给一个蒙语 AI 翻译 API 生成一套小红书推广图，突出一个 API Key 搞定翻译、OCR 和语音识别
```

常见说法：

- `生成一张小红书宣传图`：只生成单张封面图。
- `生成一套小红书组图` / `生成 5 张轮播图`：生成封面和多张正文图。
- `写一篇小红书图文笔记`：生成图片、标题、正文分页、发布文案和 Tags。
- `生成并发布到小红书`：在生成后继续发布；只有明确说要发布时才会发布。
- `把这个 MP4 发布到小红书`：发布用户提供的本地视频，可选自定义封面；不生成或编辑视频。

## 文件结构

```text
xiaohongshu-ai/
├── SKILL.md
└── scripts/
    ├── ai_services/
    │   ├── chatgpt_service.py
    │   └── volcengine_service.py
    ├── generate_xhs.py
    └── publish_xhs.py
```

## 依赖

```bash
pip install openai
pip install "xhs>=0.2.13"
```

生成内容和图片只需要配置一种 API Key：

```bash
# 使用 OpenAI 文案和图片模型
export OPENAI_API_KEY="your_api_key"

# 或使用火山引擎 Ark 文案和文生图模型
export ARK_API_KEY="your_ark_api_key"
```

发布到小红书才需要：

```bash
export XHS_COOKIE="your_cookie_string"
```

使用 `--dry-run` 只验证文件和参数时不需要 Cookie。

## 生成宣传图

```bash
python3 scripts/generate_xhs.py "给某个产品生成一张小红书宣传图" -o ./output --image-count 1
```

生成多张组图：

```bash
python3 scripts/generate_xhs.py "给某个产品生成一套小红书组图" -o ./output --image-count 5
```

输出示例：

```text
output/
├── manifest.json
├── cover.png
├── card_1.png
└── card_2.png
```

只生成结构化文案，不生成图片：

```bash
python3 scripts/generate_xhs.py "你的描述" -o ./output --skip-image
```

使用火山引擎 Ark 文生图：

```bash
export ARK_API_KEY="your_ark_api_key"

python3 scripts/generate_xhs.py "给某个产品生成一张小红书宣传图" \
  -o ./output \
  --provider volcengine \
  --image-size 2K \
  --image-count 1
```

火山引擎文案模型默认使用 `doubao-seed-2-0-pro-260215`，可通过 `--text-model` 切换；火山图片模型固定使用 `doubao-seedream-4-5-251128`，不提供命令行切换参数。

## 发布规则

默认不发布。只有用户明确说“发布到小红书”“生成并发布”“帮我发小红书”等发布意图时，才运行发布脚本。

```bash
python3 scripts/publish_xhs.py \
  --title "笔记标题" \
  --desc "笔记描述 #标签" \
  --images ./output/cover.png ./output/card_*.png

# 使用 glob 匹配所有图片（自然排序）
python3 scripts/publish_xhs.py \
  --title "笔记标题" \
  --desc "笔记描述" \
  --images-glob "./output/*.png"

# 验证模式（不实际发布）
python3 scripts/publish_xhs.py \
  --title "笔记标题" \
  --desc "笔记描述" \
  --images cover.png \
  --dry-run

# 发布本地 MP4 视频（未指定封面时自动使用视频第一帧）
python3 scripts/publish_xhs.py \
  --title "视频标题" \
  --desc "视频描述 #标签" \
  --video ./video.mp4

# 发布视频并指定封面
python3 scripts/publish_xhs.py \
  --title "视频标题" \
  --desc "视频描述 #标签" \
  --video ./video.mp4 \
  --cover ./cover.png

# 验证视频文件和参数，不实际发布
python3 scripts/publish_xhs.py \
  --title "视频标题" \
  --video ./video.mp4 \
  --dry-run
```

视频发布只接受一个本地 `.mp4` 文件；`--video` 与 `--images` / `--images-glob` 互斥。Skill 不负责视频生成、下载、转码或剪辑。

## 常用参数

**生成参数（generate_xhs.py）：**

| 参数 | 说明 |
| --- | --- |
| `--image-count 1-9` | 目标输出图片总数，包含封面 |
| `--provider` | 服务提供方，`openai`/`chatgpt` 或 `volcengine`/`ark`；默认根据可用 Key 自动选择 |
| `--image-size` | 图片尺寸，OpenAI 默认 `1024x1536`，火山默认 `2K` |
| `--image-quality` | OpenAI 图片质量，默认 `high` |
| `--ark-base-url` | 火山引擎 Ark OpenAI 兼容接口地址 |
| `--volcengine-watermark` | 火山图片生成时添加水印，默认关闭 |
| `--text-model` | 文案模型，OpenAI 默认 `gpt-5-mini`，Ark 默认 `doubao-seed-2-0-pro-260215` |
| `--skip-image` | 只生成 `manifest.json` |

**发布参数（publish_xhs.py）：**

| 参数 | 说明 |
| --- | --- |
| `--images-glob` | 使用 glob 匹配图片，按自然序排序 |
| `--video`, `-v` | 本地 MP4 视频路径；与图片参数互斥 |
| `--cover` | 可选的视频封面图片；未指定时自动使用视频第一帧 |
| `--video-wait-time` | 自动获取视频第一帧时的轮询间隔秒数，默认 `3` |
| `--desc-file` | 从 UTF-8 文件读取笔记描述 |
| `--require-image-count` | 要求图片数量必须等于该值 |
| `--public` / `--private` | 公开/私密笔记（默认私密） |
| `--post-time` | 定时发布（格式：`2024-01-01 12:00:00`） |
| `--dry-run` | 仅验证，不实际发布 |
| `--verbose` | 显示底层库输出 |
| `--debug-json` | 将发布结果写入 JSON 文件 |
