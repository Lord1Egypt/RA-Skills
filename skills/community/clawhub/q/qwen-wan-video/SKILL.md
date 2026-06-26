---
name: qwen-wan-video
description: 直接调用通义万相2.6视频生成模型（Qwen Wan 2.6），支持文生视频和图生视频，无需中间API代理。适用于需要直接对接阿里云大模型的视频创作场景。
---

# 通义万相视频生成技能

直接集成阿里云通义万相2.6（Qwen Wan 2.6）视频生成模型，通过DashScope API实现高质量视频生成。

## 功能特性
- ✅ **文生视频**（Text-to-Video）：根据文本描述生成5秒短视频
- ✅ **图生视频**（Image-to-Video）：基于参考图像生成动态视频
- ✅ **电影级参数**：支持景深、镜头运动、分辨率等专业控制
- ✅ **异步任务**：自动处理长时任务轮询和结果获取

## 环境配置
```bash
# 设置阿里云API密钥（需在阿里云控制台申请）
export DASHSCOPE_API_KEY="your-dashscope-api-key"
```

## 使用示例

### 1. 文生视频
```python
from scripts.qwen_wan_client import generate_video_t2v

video_url = generate_video_t2v(
    prompt="电影感特写镜头，缓慢推进，浅景深，风吹动头发",
    duration=5,
    resolution="720P"
)
```

### 2. 图生视频
```python
from scripts.qwen_wan_client import generate_video_i2v

video_url = generate_video_i2v(
    prompt="镜头缓慢旋转，展示产品细节",
    image_url="https://example.com/product.jpg",
    duration=4
)
```

## 技术细节
- **模型版本**：wan2.6-t2v
- **最大时长**：5秒
- **支持分辨率**：720P/1080P
- **异步处理**：自动轮询任务状态（最多10分钟超时）