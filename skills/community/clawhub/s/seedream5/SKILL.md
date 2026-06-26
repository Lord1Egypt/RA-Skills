---
name: seedream5
description: 使用火山引擎豆包 Seedream 5.0 生成或编辑图片。支持文生图、单图/多图生图、组图、联网搜索。
homepage: https://www.volcengine.com/docs/82379/1541523
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": ["uv"], "env": ["VOLC_API_KEY"] },
        "primaryEnv": "VOLC_API_KEY",
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---

# Seedream5 (火山引擎豆包 Seedream 5.0)

使用火山引擎图片生成 API 生成或编辑图片。模型：`doubao-seedream-5-0-260128`。API 文档：<https://www.volcengine.com/docs/82379/1541523>

## 文生图

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "你的图片描述" --filename "output.png" --resolution 2K
```

## 单图生图

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "编辑指令" --filename "output.png" -i "/path/in.png" --resolution 2K
```

## 多图生图（2–14 张参考图）

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "将这几张图合成一个场景" --filename "output.png" -i img1.png -i img2.png -i img3.png
```

## API Key 配置

本技能需要火山引擎 API Key。任选以下一种方式配置即可。

### 方式一：环境变量（推荐用于本地开发）

```bash
export VOLC_API_KEY="你的API_KEY"
# 或
export ARK_API_KEY="你的API_KEY"
```

### 方式二：openclaw.json（推荐用于持久配置）

编辑 `~/.openclaw/openclaw.json`（或你的 `OPENCLAW_CONFIG_PATH` 指向的配置文件），在 `skills.entries` 下添加：

```json
{
  "skills": {
    "entries": {
      "seedream5": {
        "apiKey": "你的火山引擎API_KEY"
      }
    }
  }
}
```

OpenClaw 会将 `apiKey` 注入为 `VOLC_API_KEY` 环境变量，脚本会自动读取。

### 方式三：ClawPanel / Control UI

若使用 ClawPanel 或 OpenClaw Control UI，在 Skills 页面找到 seedream5，在凭证/API Key 字段中填写即可。

### 获取 API Key

前往 [火山引擎控制台](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey) 获取长效 API Key。

## 可选参数

指定宽高比

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "竖屏人像" --filename "output.png" --aspect-ratio 9:16
```

不添加水印

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "..." --filename "output.png" --no-watermark
```

组图模式（多张关联图片）

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "生成3张不同时段场景" --filename "out.png" -i ref.png --sequential auto --max-images 3
```

联网搜索（天气、实时信息等）

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "上海未来5日天气预报图" --filename "weather.png" --web-search
```

输入图支持 URL

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "换装" --filename "out.png" -i "https://example.com/ref.png"
```

## 分辨率与宽高比

- **分辨率**：`2K`、`3K`（doubao-seedream-5-0-260128 支持）
- **宽高比**：`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`
- 建议在文件名中使用时间戳：`yyyy-mm-dd-hh-mm-ss-name.png`
- 脚本会输出 `MEDIA:<path>` 供 OpenClaw 在支持的聊天渠道中自动附加
- 不要读取图片内容回传，仅报告保存路径即可
