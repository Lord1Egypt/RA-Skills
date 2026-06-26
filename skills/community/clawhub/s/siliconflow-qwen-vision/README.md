---
name: siliconflow-qwen-vision
description: 图片理解与分析。当用户需要分析图片内容、识别图片中的物体、描述图片场景、理解图片含义时使用此技能。支持图片问答、物体识别、场景描述等。
---

# 图片理解 (SiliconFlow Qwen2.5-VL)

使用 SiliconFlow 的 Qwen2.5-VL 模型进行图片分析理解。

## 环境配置

- 需要设置 `OPENAI_API_KEY` 环境变量 (SiliconFlow API Key)
- 或使用 `--api-key` 参数直接传入 API Key

## 使用方法

```bash
cd siliconflow-qwen-vision
python scripts/analyze_image.py -i /path/to/image.jpg -p "请描述这张图片"
```

## 参数说明

- `-i, --image`: 图片路径 (必需)
- `-p, --prompt`: 提示词，默认 "请描述这张图片"
- `-k, --api-key`: API Key (可选，默认从环境变量读取)
- `-o, --output`: 输出文件路径 (可选)

## 示例

```bash
# 描述图片内容
python scripts/analyze_image.py -i photo.jpg -p "这张图片里有什么?"

# 识别物体
python scripts/analyze_image.py -i photo.jpg -p "图片中有哪些物体?"

# 分析场景
python scripts/analyze_image.py -i photo.jpg -p "描述这个场景"

# 保存结果到文件
python scripts/analyze_image.py -i photo.jpg -p "详细描述图片" -o result.txt
```
