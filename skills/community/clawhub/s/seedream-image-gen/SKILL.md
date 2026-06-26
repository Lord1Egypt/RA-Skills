---
name: seedream
description: Seedream 图片生成 - 火山引擎方舟大模型服务平台图片生成 API。支持文生图、图生图、多图融合、组图生成等多种模式。
homepage: https://www.volcengine.com/docs/82379/1541523
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": ["python3"], "env": ["ARK_API_KEY"] },
        "primaryEnv": "ARK_API_KEY",
        "install":
          [
            {
              "id": "python-brew",
              "kind": "brew",
              "formula": "python",
              "bins": ["python3"],
              "label": "Install Python (brew)",
            },
          ],
      },
  }
---

# Seedream 图片生成

基于火山引擎方舟大模型服务平台的 Seedream 图片生成 API。

## 功能

- ✅ 文生图 (Text to Image)
- ✅ 图生图 (Image to Image) - 单图输入
- ✅ 多图融合 (Multi-image to Image) - 多图输入
- ✅ 组图生成 (Sequential Image Generation)
- ✅ 联网搜索 (Web Search) - 仅 5.0 lite

## 环境配置

使用前需要设置环境变量 `ARK_API_KEY`：

```bash
export ARK_API_KEY="your-api-key-here"
```

或在命令中传入：
```bash
python3 {baseDir}/scripts/seedream.py --api-key "your-api-key" ...
```

## 快速开始

### 文生图

```bash
python3 {baseDir}/scripts/seedream.py -p "一只可爱的橘猫坐在窗台上"
```

### 图生图

```bash
python3 {baseDir}/scripts/seedream.py -p "将图片转为水彩画风格" -i "https://example.com/input.png"
```

### 多图融合

```bash
python3 {baseDir}/scripts/seedream.py -p "将图1的服装换为图2的服装" -i "img1.png" -i "img2.png"
```

### 组图生成

```bash
python3 {baseDir}/scripts/seedream.py -p "生成4张连贯插画" --sequential --max-images 4
```

## 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| --api-key | -k | API Key | 环境变量 ARK_API_KEY |
| --prompt | -p | 提示词 | (必填) |
| --model | -m | 模型 (5.0-lite/4.5/4.0) | 5.0-lite |
| --image | -i | 输入图片 URL (可多次使用) | - |
| --size | -s | 图像尺寸 | 2K |
| --output-format | -f | 输出格式 (png/jpeg) | png |
| --watermark | -w | 添加水印 | False |
| --sequential | - | 启用组图模式 | False |
| --max-images | - | 最大图片数 | 4 |
| --web-search | - | 启用联网搜索 | False |
| --output | -o | 输出目录 | ~/Downloads |
| --proxy | -x | 代理地址 | - |

## 支持的模型

| 模型 | 别名 | 支持功能 |
|------|------|----------|
| Seedream 5.0 lite | 5.0-lite | 文生图、图生图、组图、联网搜索、png输出 |
| Seedream 4.5 | 4.5 | 文生图、图生图、组图、jpeg输出 |
| Seedream 4.0 | 4.0 | 文生图、图生图、组图、jpeg输出 |

## 图像尺寸

- 方式1: `2K`, `3K`, `4K` (5.0-lite/4.5), `1K`, `2K`, `4K` (4.0)
- 方式2: 像素值，如 `2048x2048`, `2848x1600`

## 示例

### 生成单张图片

```bash
# 文生图 - 5.0 lite
python3 {baseDir}/scripts/seedream.py -p "科技感的城市夜景" -o ./images

# 图生图
python3 {baseDir}/scripts/seedream.py -p "转为黑白风格" -i "input.png" -o ./images

# 使用 4.5 模型
python3 {baseDir}/scripts/seedream.py -p "可爱的柴犬" -m 4.5 -o ./images
```

### 生成组图

```bash
# 文生组图
python3 {baseDir}/scripts/seedream.py -p "生成4张连贯的四季风景" --sequential -o ./images

# 参考图生组图
python3 {baseDir}/scripts/seedream.py -p "参考logo生成品牌设计" -i "logo.png" --sequential --max-images 6 -o ./images
```

### 联网搜索

```bash
# 生成实时天气图
python3 {baseDir}/scripts/seedream.py -p "北京今日天气预报，现代扁平化风格" --web-search -o ./images
```

## 输出

- 生成的图片保存在指定输出目录 (默认 ~/Downloads)
- 文件名格式: `seedream_{timestamp}_{index}.{ext}`
