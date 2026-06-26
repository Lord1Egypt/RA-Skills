---
name: volc-image
description: 火山引擎图像生成 - 使用火山引擎方舟API生成图片并下载
metadata:
  openclaw:
    emoji: 🖼️
    requires:
      env:
        - ARK_API_KEY
    primaryEnv: ARK_API_KEY
---

# volc-image

火山引擎图像生成技能 - 使用火山引擎方舟(Doubao Seedream) API生成图片。

## 环境配置

需要设置环境变量 `ARK_API_KEY`：
- 在火山引擎控制台获取 API Key：https://console.volcengine.com/ark/endpoint

## 功能

1. **生成图片** - 根据提示词生成图片
2. **下载保存** - 自动将生成的图片保存到本地

## 使用方式

直接告诉我要生成什么样的图片，例如：
- "生成一张小说封面：顶流重生指南"
- "生成一张科技感海报"
- "生成一张可爱猫咪图片"

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| model | 模型 | doubao-seedream-5-0-260128 |
| size | 尺寸 | 2K (1664x2496) |
| prompt | 提示词 | 用户输入 |

## 示例提示词

### 小说封面
```
小说封面，顶流重生指南，标题金色大字，时尚美女坐在王座上，娱乐圈背景，霓虹灯光，紫色金色主题，精致画面，4K
```

### 科幻风格
```
星际穿越，黑洞，黑洞里冲出一辆支离破碎的复古列车，视觉冲击力，电影大片，末日既视感，动感，对比色，oc渲染，光线追踪，动态模糊，景深，超现实主义，深蓝
```

### 可爱风格
```
可爱的小猫咪，胖乎乎，大眼睛，萌萌的，粉色背景，卡通风格，精致可爱
```

## 技术实现

```python
import os
import requests

# API配置
url = 'https://ark.cn-beijing.volces.com/api/v3/images/generations'
api_key = os.environ.get('ARK_API_KEY')

# 请求数据
data = {
    'model': 'doubao-seedream-5-0-260128',
    'prompt': '<用户提示词>',
    'sequential_image_generation': 'disabled',
    'response_format': 'url',
    'size': '2K',
    'stream': False,
    'watermark': True
}

# 发送请求
response = requests.post(url, headers={
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}, json=data)

# 获取图片URL并下载
img_url = response.json()['data'][0]['url']
img_data = requests.get(img_url).content

# 保存图片
with open('output.jpg', 'wb') as f:
    f.write(img_data)
```

## 注意事项

- API Key 需要在火山引擎控制台获取
- 图片URL有效期约24小时
- 生成图片可能需要几秒钟时间

## 执行命令

设置API Key并生成图片：
```bash
# 设置API Key
set ARK_API_KEY=你的API密钥

# 生成图片
python volc_image.py "你的提示词"
```

或者在Python中直接调用：
```python
import os
os.environ['ARK_API_KEY'] = '你的API密钥'
exec(open('volc_image.py').read())
```
