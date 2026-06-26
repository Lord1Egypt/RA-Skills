# seedream-volcengine

直连火山引擎 Doubao-Seedream API 生成和编辑图片（无第三方中转）。

Generate and edit images using Volcengine Doubao-Seedream API (direct connection, no third-party proxy).

[![ClawHub](https://img.shields.io/badge/ClawHub-seedream--volcengine-blue)](https://clawhub.ai/CyberKurry/seedream-volcengine) [![GitHub](https://img.shields.io/badge/GitHub-CyberKurry%2Fseedream--volcengine-black)](https://github.com/CyberKurry/seedream-volcengine) [![License: MIT-0](https://img.shields.io/badge/License-MIT--0-green.svg)](LICENSE)

**Version:** 1.0.0 | **Owner:** [CyberKurry](https://github.com/CyberKurry)

---

## 功能 / Features

- **文生图** — 通过自然语言描述生成图片
- **图片编辑** — AI 驱动的图片修改（单图输入单图输出）
- **多图融合** — 合并多张参考图（最多 14 张）
- **组图生成** — 一次请求生成最多 15 张关联图片
- **PNG 输出** — 无损格式支持（5.0-lite 模型）
- **提示词优化** — 标准（所有模型）和极速（仅 4.0）两种模式
- **联网搜索** — 实时信息集成，如天气、新闻等（仅 5.0-lite）
- **流式输出** — 实时获取生成结果（所有模型）

- **Text-to-image** — Generate images from natural language descriptions
- **Image editing** — Modify existing images with AI-powered editing
- **Multi-reference fusion** — Combine multiple reference images into one (up to 14)
- **Sequential/group generation** — Generate up to 15 related images in one request
- **PNG output** — Lossless format support (5.0-lite only)
- **Prompt optimization** — Standard (all models) and fast (4.0 only) modes
- **Web search** — Real-time info integration, e.g. weather, news (5.0-lite only)
- **Streaming** — Get results as they're generated (all models)

## 支持模型 / Supported Models

| 模型 / Model | Model ID | 分辨率 / Resolution | 输出 / Output | 提示词优化 / Prompt Opt | 联网搜索 / Web Search |
|-------------|----------|---------------------|--------------|------------------------|---------------------|
| Seedream 5.0-lite | `doubao-seedream-5-0-260128` | 2K, 3K, 4K | png, jpeg | standard | ✅ |
| Seedream 4.5 | `doubao-seedream-4-5-251128` | 2K, 4K | jpeg | standard | ❌ |
| Seedream 4.0 | `doubao-seedream-4-0-250828` | 1K, 2K, 4K | jpeg | standard, fast | ❌ |

> **Note**: 5.0-lite also supports alias `doubao-seedream-5-0-lite-260128`.

## 安装 / Setup

1. 从 [火山方舟控制台](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey) 获取 API Key
   Get API key from [Volcengine Ark Console](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)

2. 设置环境变量 / Set environment variable:
   ```bash
   export VOLC_API_KEY="your-key"
   ```

3. 安装 uv（Python 包运行器）/ Install [uv](https://docs.astral.sh/uv/):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### OpenClaw 安装 / OpenClaw Installation

```bash
# Via ClawHub
openclaw skill install CyberKurry/seedream-volcengine

# Or clone from GitHub
git clone https://github.com/CyberKurry/seedream-volcengine.git
```

## 使用方法 / Usage

```bash
# 文生图 / Text to image
uv run scripts/generate_image.py --prompt "一只赛博朋克风格的猫"

# 图片编辑（带参考图）/ Image editing (with reference)
uv run scripts/generate_image.py --prompt "变为水墨画风格" --image "https://example.com/photo.jpg"

# 多图融合 / Multi-reference fusion
uv run scripts/generate_image.py --prompt "融合风格" --image "https://a.jpg" --image "https://b.jpg"

# 组图生成 / Group generation
uv run scripts/generate_image.py --prompt "四格漫画" --sequential --max-images 4

# 4K PNG 输出 / 4K PNG output
uv run scripts/generate_image.py --prompt "超高清风景" --size 4K --output-format png

# 联网搜索（仅 5.0-lite）/ Web search (5.0-lite only)
uv run scripts/generate_image.py --prompt "今天上海天气预报图" --web-search

# 提示词优化 / Prompt optimization
uv run scripts/generate_image.py --prompt "一只猫" --prompt-optimization standard

# 列出所有可用模型 / List all available models
uv run scripts/generate_image.py --list-models
```

## API Key 安全 / API Key Safety

切勿硬编码 API Key。请使用环境变量或 `--api-key` 参数。

Never hardcode API keys. Use environment variables or the `--api-key` flag.

## 许可证 / License

MIT No Attribution — 可自由使用、修改、分发，无需署名。详见 [LICENSE](LICENSE)。

MIT No Attribution — free to use, modify, and distribute without attribution. See [LICENSE](LICENSE) for details.

## 参考 / References

- **Volcengine Seedream API**: https://www.volcengine.com/docs/82379/1541523
- **Seedream Tutorial**: https://www.volcengine.com/docs/82379/1824121

## 链接 / Links

- **ClawHub**: https://clawhub.ai/CyberKurry/seedream-volcengine
- **GitHub**: https://github.com/CyberKurry/seedream-volcengine
