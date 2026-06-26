---
name: seedream-img-gen
description: "This skill should be used when the user wants to generate images using Seedream, the image generation model from ByteDance on Volcengine platform. Triggers include requests like 用Seedream生成图片, seedream画图, generate image with seedream, 调用seedream, 用豆包画图, or any request to create, draw, or generate images via the Seedream API."
---

# Seedream 图片生成 Skill

## 概述

本 Skill 帮助通过火山引擎方舟平台（Volcengine Ark）的 Seedream 系列模型生成图片，支持文生图（text-to-image）和图生图（image-to-image，Seedream 4.0+）。

---

## 前置条件

1. **获取 API Key**：前往 https://console.volcengine.com/ark 注册并获取 `ARK_API_KEY`
2. **开通模型**：在方舟平台「开通管理」页面开通所需模型
3. **安装依赖**（二选一）：
   - 官方 SDK：`pip install 'volcengine-python-sdk[ark]'`
   - OpenAI 兼容：`pip install openai`

---

## 核心工作流

### 1. 收集必要信息

在生成图片前，需要明确：
- **提示词**（prompt）：图片内容描述，支持中英文
- **模型选择**：默认使用 `doubao-seedream-3-0-t2i-250415`（详细模型列表见 `references/api_reference.md`）
- **图片尺寸**（可选）：如 `1024x1024`、`1792x1024`
- **输出路径**（可选）：保存图片的本地路径

如果用户未明确提到模型，默认使用 Seedream 4.0（`doubao-seedream-4-0-250828`）。

### 2. 检查环境

To verify the environment is ready, run:
```bash
echo $ARK_API_KEY
```

If the API key is missing, instruct the user to set it:
```bash
export ARK_API_KEY="your_api_key_here"
```

### 3. 调用生成脚本

Use the bundled script at `scripts/generate_image.py`:

```bash
# 基本用法（文生图）
python3 ~/.workbuddy/skills/seedream-image-gen/scripts/generate_image.py \
  --prompt "一只可爱的橘猫坐在窗边看夕阳，写实摄影风格" \
  --output output.png

# 指定模型
python3 ~/.workbuddy/skills/seedream-image-gen/scripts/generate_image.py \
  --prompt "a cyberpunk city at night" \
  --model doubao-seedream-4-0-250828 \
  --output output.png

# 指定尺寸
python3 ~/.workbuddy/skills/seedream-image-gen/scripts/generate_image.py \
  --prompt "横版风景画，超宽屏" \
  --size 1792x1024 \
  --output landscape.png

# 生成多张
python3 ~/.workbuddy/skills/seedream-image-gen/scripts/generate_image.py \
  --prompt "卡通风格的小动物" \
  --n 4 \
  --output animals.png

# 使用 OpenAI 兼容模式
python3 ~/.workbuddy/skills/seedream-image-gen/scripts/generate_image.py \
  --prompt "描述内容" \
  --sdk openai \
  --output result.png
```

### 4. 处理结果

- 脚本成功执行后会输出图片保存路径
- 生成的图片默认保存到当前工作目录，也可通过 `--output` 指定
- 使用 `url` 格式时，脚本会自动下载图片到本地

---

## 快速内联调用（不使用脚本）

如果希望直接生成代码调用，可用以下模板：

```python
import os
from volcenginesdkarkruntime import Ark

client = Ark(api_key=os.environ.get("ARK_API_KEY"))
resp = client.images.generate(
    model="doubao-seedream-3-0-t2i-250415",
    prompt="YOUR_PROMPT_HERE",
    response_format="url",
)

url = resp.data[0].url
print("图片 URL:", url)

# 下载图片
import urllib.request
urllib.request.urlretrieve(url, "output.png")
print("已保存至 output.png")
```

---

## 模型选择建议

| 场景 | 推荐模型 |
|------|---------|
| 通用文生图，快速稳定 | `doubao-seedream-3-0-t2i-250415` |
| 高质量图片，支持参考图 | `doubao-seedream-4-0-250828` |
| 最新最强效果 | `doubao-seedream-4-5-251128` |
| 极速轻量 | `doubao-seedream-5-0-lite` |

---

## 参考资源

- 详细 API 参数和代码示例：`references/api_reference.md`
- 生成脚本（支持命令行调用）：`scripts/generate_image.py`
- 官方文档：https://www.volcengine.com/docs/82379
