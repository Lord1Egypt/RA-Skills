---
name: doubao-image-gen
description: "使用豆包 Seedream 模型文生图，支持并发批量生成，输出图库预览页"
description_en: "Text-to-image generation using Doubao Seedream model, supports concurrent batch generation with gallery output"
allowed-tools: Read,Write,Bash
---

# 豆包文生图 (Doubao Image Gen)

使用火山引擎豆包 `doubao-seedream-5-0-260128` 模型，根据文字描述生成高质量图像，支持并发批量生成多张图片，并输出图库预览页面。

## 环境要求

- Python 3.8+
- openai 库：`pip install "openai>=1.0"`

## Setup — API Key 配置

API Key 读取优先级（从高到低）：
1. `--api-key` 命令行参数
2. 环境变量 `ARK_API_KEY`
3. 用户目录 `~/.doubao-image-gen/.env` 文件中的 `ARK_API_KEY=xxx`

获取 API Key：登录 [火山方舟控制台](https://console.volcengine.com/ark) → API Key 管理

## Run

```bash
# 生成单张图片
python {baseDir}/scripts/gen.py --prompt "赛博朋克风格的上海夜景" --api-key YOUR_KEY

# 并发生成4张（默认并发数=4）
python {baseDir}/scripts/gen.py --prompt "水墨风格的山水画" --count 4 --api-key YOUR_KEY

# 指定尺寸（支持 1024x1024 / 2K / 1280x720 / 720x1280 / 2048x2048）
python {baseDir}/scripts/gen.py --prompt "星空下的草原" --size 2K --api-key YOUR_KEY

# 指定输出目录
python {baseDir}/scripts/gen.py --prompt "古风仙侠" --out-dir ./output --api-key YOUR_KEY

# 从环境变量读取 Key（推荐）
python {baseDir}/scripts/gen.py --prompt "未来城市" --count 2
```

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--prompt` | 必填 | 图像描述提示词 |
| `--count` | 1 | 生成数量（并发执行） |
| `--size` | `2K` | 图像尺寸 |
| `--model` | `doubao-seedream-5-0-260128` | 模型名称 |
| `--out-dir` | `./doubao-output-{时间戳}` | 输出目录 |
| `--api-key` | 环境变量 | ARK API Key |
| `--workers` | 4 | 并发线程数 |
| `--watermark` | False | 是否添加水印 |
| `--dry-run` | False | 仅打印参数不调用 API |

## Output

- `*.jpeg` 图像文件（按序号命名）
- `prompts.json` 提示词与文件的映射记录
- `index.html` 图库预览页面（可直接在浏览器打开）

## AI 使用指引

当用户说以下内容时，加载本技能并调用脚本：

- "帮我画一张..." / "生成一张..." / "画个图..." 
- "批量生成 N 张图片"
- "用豆包生成图片"

**标准流程：**
1. 提取或优化用户的提示词（必要时翻译为英文以提升质量）
2. 调用 `python {baseDir}/scripts/gen.py` 生成图片
3. 生成完成后，**直接在聊天中以 Markdown 图片形式发送给用户**：`![描述](图片路径或URL)`
4. 同时提供 `index.html` 预览链接供浏览

**示例 Prompt 优化：**
用户说"画一只猫"→ 优化为 "A cute cat sitting gracefully, soft studio lighting, photorealistic, 8K detail"
