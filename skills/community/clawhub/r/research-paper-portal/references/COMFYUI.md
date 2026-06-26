# ComfyUI Flux2 工作流说明

## 服务器配置

### 硬件要求

| 组件 | 最低配置 | 推荐配置 |
|------|----------|----------|
| GPU | RTX 3060 (12GB) | RTX 4090 (24GB) |
| 内存 | 16GB | 32GB |
| 存储 | 50GB SSD | 100GB NVMe |

### 软件要求

- Python 3.10+
- CUDA 11.8+
- ComfyUI 0.17+

## 模型文件

### Flux2 所需模型

| 模型类型 | 文件名 | 大小 | 存放路径 |
|----------|--------|------|----------|
| UNET | flux2_dev_fp8mixed.safetensors | ~16GB | models/diffusion_models/ |
| CLIP | mistral_3_small_flux2_bf16.safetensors | ~3GB | models/text_encoders/ |
| VAE | flux2-vae.safetensors | ~300MB | models/vae/ |

### 下载地址

从 Hugging Face 下载：

```bash
# 使用 huggingface-cli
huggingface-cli download black-forest-labs/FLUX.1-dev --local-dir ./models
```

## API 调用

### 提交任务

```python
import requests

url = "http://YOUR_SERVER:8188/prompt"
workflow = {
    # 工作流定义
}

response = requests.post(url, json={"prompt": workflow})
prompt_id = response.json()["prompt_id"]
```

### 查询状态

```python
status_url = f"http://YOUR_SERVER:8188/history/{prompt_id}"
response = requests.get(status_url)
data = response.json()

if prompt_id in data:
    if data[prompt_id]["status"]["completed"]:
        # 任务完成
        outputs = data[prompt_id]["outputs"]
```

### 下载图片

```python
img_url = f"http://YOUR_SERVER:8188/view?filename={filename}&type=output"
response = requests.get(img_url)
with open("output.png", "wb") as f:
    f.write(response.content)
```

## 工作流节点

### Flux2 基础工作流

```
UNETLoader → CLIPLoader → VAELoader
     ↓            ↓
CLIPTextEncode (positive)
     ↓
EmptyFlux2LatentImage → RandomNoise
     ↓                      ↓
     └──────→ SamplerCustomAdvanced ←──────┘
                      ↓
                 VAEDecode → SaveImage
```

### 关键参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| `steps` | 20 | 采样步数 |
| `cfg` | 1.0 | 引导强度 |
| `sampler` | euler | 采样器 |
| `scheduler` | simple | 调度器 |

## 提示词模板

### 学术风格

```
主题描述, 关键元素, 颜色配色, scientific illustration, 
abstract background, 4k, detailed, no text
```

### 示例提示词

**地热研究**:
```
Deep underground geothermal energy, borehole drilling, 
earth layers cross-section, magma glow, warm orange red 
brown colors, scientific illustration, abstract background, 
4k, detailed, no text
```

**热管研究**:
```
Heat pipe thermal management system, vapor condensation 
cycle, blue orange silver metallic colors, engineering 
diagram, abstract background, 4k, detailed, no text
```

**纳米材料**:
```
Nanoscale materials, molecular structure, crystal lattice, 
quantum dots, green blue silver colors, scientific 
illustration, abstract background, 4k, detailed, no text
```

## 性能优化

### 降低显存占用

1. 使用 fp8 模型（flux2_dev_fp8mixed）
2. 减小图片尺寸
3. 使用 `--lowvram` 参数启动

### 提高生成速度

1. 启用 xformers
2. 使用 CUDA Graph
3. 批量生成

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| CUDA out of memory | 使用 fp8 模型或减小图片尺寸 |
| 模型加载失败 | 检查模型路径和文件完整性 |
| 生成图片模糊 | 增加采样步数 |
| API 无响应 | 检查服务器状态和端口 |
