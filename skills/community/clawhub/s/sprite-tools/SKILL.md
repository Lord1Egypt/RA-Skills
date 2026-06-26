---
name: sprite-tools
version: 1.0.0
description: "游戏素材切图+抠图工具集。提供：1) Codex CLI 生图后批量裁剪（2x3/3x2网格拆分为独立图标）；2) 基于 Alpha 通道的背景抠图；3) 基于边缘色的边界裁剪；4) PIL-based 无外部依赖抠图（备选）。支持 PNG/JPG/WebP。所有脚本输出到指定目录或 /tmp/sprite_out/。"
metadata: {"openclaw":{"emoji":"✂️","requires":{"anyBins":["ffmpeg"],"pythonPkgs":["Pillow","numpy"]}}}
---

# Sprite Tools — 切图 + 抠图工具集

## 工具概览

| 工具 | 用途 | 依赖 |
|------|------|------|
| `batch_split.py` | **完整流程**：背景透明化 + 网格拆分 + alpha 抠图（推荐） | PIL + numpy |
| `grid_splitter.py` | 批量裁剪（按固定网格拆分，不做抠图） | PIL |
| `alpha_trim.py` | Alpha 通道抠图（去透明背景） | PIL |
| `color_trim.py` | 边缘色裁剪（去纯色背景如白/灰/黑边） | PIL + numpy |
| `rembg_simple.py` | 轻量级背景移除（色差检测） | PIL + numpy |

## 环境要求

```bash
pip install --break-system-packages Pillow numpy
# 可选（更精准的抠图）：
pip install --break-system-packages rembg
# 可选（ImageMagick，备选）：
sudo apt install imagemagick
```

## 快速参考

```bash
# ✅ 推荐：完整流程（背景透明 → 拆分 → 抠图，一气呵成）
python3 ~/.openclaw/skills/sprite-tools/scripts/batch_split.sh \
  /tmp/codex_batch.png 2x3 /tmp/icons/

# layout 格式：rows x cols
# "2x3" = 2行3列 → 每格 = image_width/3 x image_height/2
# "3x2" = 3行2列 → 每格 = image_width/2 x image_height/3
```

```bash
# 旧流程（分步）：
bash ~/.openclaw/skills/sprite-tools/scripts/grid_splitter.sh \
  /tmp/codex_batch.png 2x3 /tmp/icons/
```

## 1. 网格拆分 (grid_splitter)

### 用途
Codex CLI 的 `batch_generate.sh` 输出是一张大图内含多个元素（2x3 或 3x2 网格），用此脚本拆成独立文件。

### 原理
根据已知网格布局 (`rowsxcols`) 和**图片实际尺寸**自动计算每个格子的大小，然后 crop + 编号输出。

### 使用方式
```bash
python3 ~/.openclaw/skills/sprite-tools/scripts/grid_splitter.py \
  <input_image> <layout> [output_dir]

# layout 格式：2x3 / 3x2 / 2x2 / 4x3 等
# output_dir 默认为 /tmp/sprite_out/
```

### 示例
```bash
# Codex 输出 1024x1536 的 3x2 网格（2列3行，RPG 图标）
python3 ~/.openclaw/skills/sprite-tools/scripts/batch_split.sh \
  /tmp/rpg_batch.png 3x2 /tmp/rpg_icons/

# Codex 输出 1536x1024 的 2x3 网格（3列2行，像素风格）
python3 ~/.openclaw/skills/sprite-tools/scripts/batch_split.sh \
  /tmp/pixel_batch.png 2x3 /tmp/pixel_items/
```

### 输出
- `sprite_00.png`, `sprite_01.png`, ... 按行优先顺序（先左到右，再上行到下行）

---

## 2. Alpha 抠图 (alpha_trim)

### 用途
素材本身背景是透明的（Alpha=0），裁掉全透明的边，保留实际内容。

### 原理
遍历所有像素，找出 Alpha>0 的边界框（Bounding Box），crop 到此框。

### 使用方式
```bash
python3 ~/.openclaw/skills/sprite-tools/scripts/alpha_trim.py \
  <input.png> <output.png> [--batch] [--pad N]

# --batch: input 是目录，批量处理目录下所有 .png/.jpg
# --pad N: 裁剪后加 N 像素padding（默认 0）
```

### 示例
```bash
# 单个文件
python3 ~/.openclaw/skills/sprite-tools/scripts/alpha_trim.py \
  /tmp/icon.png /tmp/icon_nobg.png

# 批量（目录下所有 PNG）
python3 ~/.openclaw/skills/sprite-tools/scripts/alpha_trim.py \
  /tmp/icons/ /tmp/icons_nobg/ --batch --pad 4
```

---

## 3. 边缘色抠图 (color_trim)

### 用途
素材背景不是透明，而是固定颜色（白色、灰色、黑色或已知颜色），裁掉边框。

### 原理
以左上角 (0,0) 像素颜色为基准边缘色，向内扩展裁剪（允许颜色容差 `atol`）。

### 使用方式
```bash
python3 ~/.openclaw/skills/sprite-tools/scripts/color_trim.py \
  <input.png> <output.png> [--atol N] [--batch] [--pad N]

# --atol N: 颜色容差（0-255，默认 10）
# --batch: 批量处理目录
# --pad N: 裁剪后加 N 像素 padding
```

### 示例
```bash
# 白色背景（容差 10）
python3 ~/.openclaw/skills/sprite-tools/scripts/color_trim.py \
  /tmp/icon_white_bg.png /tmp/icon_nobg.png --atol 10

# 灰色背景（容差 20）
python3 ~/.openclaw/skills/sprite-tools/scripts/color_trim.py \
  /tmp/icon_gray_bg.png /tmp/icon_nobg.png --atol 20

# 批量处理
python3 ~/.openclaw/skills/sprite-tools/scripts/color_trim.py \
  /tmp/icons/ /tmp/icons_nobg/ --batch --atol 10
```

---

## 4. 轻量级背景移除 (rembg_simple)

### 用途
在没有 rembg 模型的情况下，用简单色差检测做背景移除（适合背景与主体色差大的情况）。

### 原理
基于超像素（superpixel）分割的思想：用 SLIC/SLICO 算法将图像分成小块，计算每块与边缘色的相似度，保留与主体更相似的块。

### 使用方式
```bash
python3 ~/.openclaw/skills/sprite-tools/scripts/rembg_simple.py \
  <input.png> <output.png> [--strength 0.5] [--batch]

# --strength: 0.0-1.0，背景检测激进程度（默认 0.5）
# --batch: 批量处理目录
```

### 示例
```bash
# 单个文件
python3 ~/.openclaw/skills/sprite-tools/scripts/rembg_simple.py \
  /tmp/complex_bg.png /tmp/complex_nobg.png --strength 0.6

# 批量
python3 ~/.openclaw/skills/sprite-tools/scripts/rembg_simple.py \
  /tmp/batch/ /tmp/batch_nobg/ --batch --strength 0.5
```

### 限制
- 简单色差检测，复杂背景效果有限
- 复杂抠图建议安装 `rembg`（需模型下载，首次运行自动下载 isnet models）

---

## rembg 安装与使用（可选，精准抠图）

### 安装
```bash
pip install --break-system-packages rembg
```

### 首次运行
rembg 首次使用会自动下载 ONNX 模型（isnet），约 170MB，存到 `~/.u2net/` 或 `~/.rembg/`。

```bash
# 首次运行（会自动下载模型）
python3 -c "
from rembg import remove
from PIL import Image
img = Image.open('/tmp/test.png')
out = remove(img)
out.save('/tmp/test_nobg.png')
print('Done')
"
```

### 快速抠图
```python
from rembg import remove
from PIL import Image

def rembg(input_path, output_path):
    img = Image.open(input_path)
    out = remove(img)
    out.save(output_path)
    return out.size

# 批量
import os
for f in os.listdir('/tmp/icons/'):
    if f.endswith('.png'):
        rembg(f'/tmp/icons/{f}', f'/tmp/icons_nobg/{f}')
```

### Web 抠图 API（无需本地模型）
```python
# 使用 remove.bg API（需要 API key）
import requests

def removebg_api(input_path, output_path, api_key):
    with open(input_path, 'rb') as f:
        r = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': f},
            data={'size': 'auto'},
            headers={'X-Api-Key': api_key}
        )
    if r.status_code == 200:
        with open(output_path, 'wb') as out:
            out.write(r.content)
        return True
    return False
```

---

## 工作流建议

```
Codex 生图（batch_generate.sh）
    ↓
网格拆分（grid_splitter）
    ↓
抠图（alpha_trim / color_trim / rembg_simple）
    ↓
输出独立素材 → 交给 Unity / 美术流程
```

### 完整示例
```bash
# 1. Codex 生成 RPG 图标集（白色背景）
bash ~/.openclaw/skills/codex-imggen/scripts/batch_generate.sh \
  "flat vector art style, white background (#ffffff), each icon approximately 256x256 pixels, consistent 2px gold (#d4af37) border, same lighting angle, centered subjects" \
  6 \
  /tmp/rpg_batch/

# 2. 找到生成的大图
BATCH_FILE=$(ls /tmp/rpg_batch/*.png | head -1)
echo "Batch file: $BATCH_FILE"

# 3. 拆分为独立图标 + 抠图（一键完成）
# 1024x1536 → 3x2 layout（2列3行）
python3 ~/.openclaw/skills/sprite-tools/scripts/batch_split.sh \
  "$BATCH_FILE" 3x2 /tmp/rpg_icons/

# 4. 验证
ls /tmp/rpg_icons/
```

---

## 依赖状态

| 依赖 | 状态 |
|------|------|
| PIL (Pillow) | ✅ 已安装 |
| numpy | ✅ 已安装 |
| rembg | ✅ 已安装（需要模型下载） |
| ffmpeg | ✅ 已安装（视频帧提取时用） |
| ImageMagick | ❌ 未安装（可选备选） |