# rembg 详细指南

## 模型选项

| 模型 | 命令 | 描述 | 大小 |
|------|------|------|------|
| u2net | `-m u2net` | 通用模型（默认） | ~176MB |
| u2netp | `-m u2netp` | 轻量版 u2net | ~45MB |
| u2net_human_seg | `-m u2net_human_seg` | 人像分割 | ~176MB |
| u2net_cloth_seg | `-m u2net_cloth_seg` | 衣物分割 | ~176MB |
| isnet | `-m isnet` | 高精度通用 | ~176MB |
| birefnet-general | `-m birefnet-general` | BiRefNet 通用 | ~973MB |

## 使用示例

### 使用特定模型

```python
from rembg import remove, new_session

# 使用人像分割模型
session = new_session("u2net_human_seg")
result = remove(input_image, session=session)
```

### 调整参数

```python
from rembg import remove
from PIL import Image

input_image = Image.open("input.png")

# 基础去背景
output = remove(input_image)

# 开启 alpha matting（更好的边缘）
output = remove(input_image, alpha_matting=True, alpha_matting_foreground_threshold=240)

# 仅返回 mask
output = remove(input_image, only_mask=True)
```

## 首次运行

首次运行时会自动下载默认模型（u2net），约 176MB：

```
Downloading model: u2net
Downloading data from 'https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx' to file '/Users/xxx/.u2net/u2net.onnx'.
```

模型保存在：`~/.u2net/`

## 常见问题

### Q: 处理速度慢？

A: 可以使用轻量模型 `u2netp`，速度更快但精度略低

### Q: 内存不足？

A: 减少批量处理数量，或使用 `u2netp` 模型

### Q: 模型下载失败？

A: 手动下载：
```bash
python3 -c "from rembg import new_session; new_session('u2net')"
```

## API 参考

### Python API

```python
from rembg import remove

# 基本用法
output = remove(input)  # input 可以是 PIL Image 或 bytes

# 高级用法
output = remove(
    input,
    model='u2net',           # 模型选择
    alpha_matting=False,      # 开启 alpha matting
    alpha_matting_foreground_threshold=240,
    alpha_matting_background_threshold=10,
    alpha_matting_erode_size=10,
    only_mask=False,          # 仅返回 mask
    session=None,             # 复用 session
)
```

### CLI 用法

```bash
# 基本用法
rembg i input.png output.png

# 指定模型
rembg i -m u2net_human_seg input.png output.png

# 开启 alpha matting
rembg i -a input.png output.png

# 仅返回 mask
rembg i -om input.png output.png

# 批量处理
rembg p input_folder/ output_folder/

# 批量处理 + 监视模式
rembg p -w input_folder/ output_folder/
```
