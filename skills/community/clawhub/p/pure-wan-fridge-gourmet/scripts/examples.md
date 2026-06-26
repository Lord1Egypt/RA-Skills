# 纯血万相冰箱盲盒 - 示例配置

## 环境变量设置

```bash
# Linux/macOS
export WAN_API_KEY="your-wan-api-key-here"
export WAN_API_URL="https://api.wan.xxx/v1/images/generate"

# Windows (PowerShell)
$env:WAN_API_KEY="your-wan-api-key-here"
$env:WAN_API_URL="https://api.wan.xxx/v1/images/generate"
```

## 快速测试

```bash
# 1. 设置环境变量
export WAN_API_KEY="your-key"

# 2. 运行生成
python3 scripts/generate_gourmet.py path/to/your/fridge.jpg --style michelin

# 3. 尝试不同风格
python3 scripts/generate_gourmet.py path/to/your/fridge.jpg --style japanese
python3 scripts/generate_gourmet.py path/to/your/fridge.jpg --style italian
```

## Python 调用示例

```python
from scripts.generate_gourmet import WanFridgeGourmet

# 初始化
gourmet = WanFridgeGourmet()

# 生成米其林风格
result = gourmet.generate(
    image_path="my_fridge.jpg",
    style="michelin",
    denoising_strength=0.85
)

# 生成日式风格
result = gourmet.generate(
    image_path="my_fridge.jpg", 
    style="japanese",
    denoising_strength=0.8
)

# 自定义提示词
result = gourmet.generate(
    image_path="my_fridge.jpg",
    custom_prompt="基于照片中的食材，创造一道精致的中式私房菜..."
)
```

## 参数调优指南

| 场景 | denoising_strength | semantic_consistency_strength |
|------|-------------------|------------------------------|
| 想要更大创意 | 0.90-0.95 | 0.7-0.8 |
| 平衡创意与真实 | 0.85 | 0.9 |
| 更忠实原食材 | 0.75-0.80 | 0.95 |
