# qwen-vision

👁️ 使用阿里云通义千问视觉模型（Qwen Vision API）分析图片和视频。

## 功能

- 🖼️ **图片理解** - 描述图片内容、识别物体、场景
- 📝 **OCR 文字识别** - 提取图片中的文字
- 📊 **图表分析** - 解读数据图表、趋势分析
- 🔍 **视觉问答** - 回答关于图片的问题
- 🎥 **视频理解** - 分析视频内容（需传入视频帧）

## 安装方法

### 方式 1：通过 clawhub 安装（推荐）

```bash
openclaw skill install qwen-vision
```

或

```bash
openclaw clawhub install qwen-vision
```

### 方式 2：手动安装

1. 克隆或复制 skill 到技能目录：
```bash
git clone <repo-url> ~/.openclaw/workspace/skills/qwen-vision
```

或直接复制本目录：
```bash
cp -r /path/to/qwen-vision ~/.openclaw/workspace/skills/
```

2. 验证安装：
```bash
openclaw skill list | grep qwen-vision
```

### 方式 3：通过 skillhub

```bash
openclaw skillhub install qwen-vision
```

## 配置 API Key

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "models": {
    "providers": {
      "bailian": {
        "apiKey": "sk-your-api-key-here"
      }
    }
  }
}
```

或设置环境变量：
```bash
export DASHSCOPE_API_KEY="sk-your-api-key-here"
```

获取 API Key：https://dashscope.console.aliyun.com/

## 使用方法

### 基础用法

```bash
# 分析图片
uv run ~/.openclaw/workspace/skills/qwen-vision/scripts/analyze_image.py \
  --image "/path/to/image.jpg" \
  --prompt "请描述这张图片"
```

### 指定模型

```bash
uv run ~/.openclaw/workspace/skills/qwen-vision/scripts/analyze_image.py \
  --image "/path/to/image.jpg" \
  --model "qwen-vl-max-latest" \
  --prompt "分析这张图表的数据"
```

### 常用提示词示例

| 任务 | 提示词 |
|------|--------|
| 描述图片 | "请详细描述这张图片的内容" |
| OCR | "提取图片中的所有文字" |
| 数数 | "数一下图中有多少个物体" |
| 图表分析 | "分析这张图表的数据趋势" |
| 识别 | "这是什么地方/物品？" |
| 情感分析 | "这张图片传达了什么情绪？" |

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--image`, `-i` | 图片路径（必填） | - |
| `--prompt`, `-p` | 分析提示词 | "请详细描述这张图片的内容。" |
| `--model`, `-m` | 模型选择 | `qwen-vl-max-latest` |
| `--api-key`, `-k` | API Key（可选，可从配置读取） | - |

## 可用模型

| 模型 | 描述 | 适用场景 |
|------|------|----------|
| `qwen-vl-max-latest` | 最强视觉模型 | 复杂分析、高精度需求 |
| `qwen-vl-plus-latest` | 性价比模型 | 快速响应、简单任务 |

## 支持格式

- **图片格式**：JPG, JPEG, PNG, GIF, WebP, BMP
- **最大尺寸**：建议不超过 4096x4096
- **文件大小**：建议不超过 10MB

## 示例

### 示例 1：描述图片
```bash
uv run ~/.openclaw/workspace/skills/qwen-vision/scripts/analyze_image.py \
  -i "photo.jpg" \
  -p "这张照片里有什么？"
```

### 示例 2：OCR 文字识别
```bash
uv run ~/.openclaw/workspace/skills/qwen-vision/scripts/analyze_image.py \
  -i "document.png" \
  -p "提取图片中的所有文字，保持原有格式"
```

### 示例 3：图表分析
```bash
uv run ~/.openclaw/workspace/skills/qwen-vision/scripts/analyze_image.py \
  -i "chart.png" \
  -p "分析这张图表的数据趋势，总结关键发现"
```

## 故障排除

### 401 Unauthorized
- 检查 API Key 是否正确
- 确认 Key 未过期

### 429 Too Many Requests
- API 调用频率超限，稍后重试
- 考虑升级套餐或降低调用频率

### 400 Invalid Request
- 检查图片格式是否支持
- 确认图片文件未损坏

## 相关技能

- **qwen-image** - 图片生成（文生图）
- **agent-browser** - 浏览器自动化（网页截图）
- **summarize** - 内容总结（支持图片分析）

## 许可证

MIT License

## 反馈

遇到问题或有建议？欢迎提交 issue 或联系维护者。
