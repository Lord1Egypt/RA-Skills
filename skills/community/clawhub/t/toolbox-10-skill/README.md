# 实用工具匣 (Toolbox Skill)

> 集合四大高频实用图像工具 Skill：去水印 / OCR文字识别 / 图片压缩 / 标准证件照生成

## 工具列表

| 工具 | 脚本 | 能力 |
|------|------|------|
| 🔧 去水印 | `scripts/remove_watermark.py` | OpenCV inpainting 自动检测并修复水印 |
| 📝 OCR识别 | `scripts/ocr_recognize.py` | EasyOCR 中英文混合，输出文字+坐标 |
| 📦 图片压缩 | `scripts/compress_image.py` | Pillow 智能压缩，支持质量/尺寸/格式/大小上限 |
| 📸 证件照 | `scripts/id_photo.py` | rembg 去背景+Pillow 裁剪，一寸/二寸/护照等9种规格，红蓝白三底色 |

## 安装

```bash
pip install opencv-python-headless Pillow numpy rembg onnxruntime easyocr
```

> 首次使用 OCR 或证件照功能时，EasyOCR 和 rembg 会自动下载模型文件（约 100-300MB），请保持网络畅通。

## 快速示例

```bash
# 去水印
python scripts/remove_watermark.py photo.jpg -o clean.jpg

# OCR 识别
python scripts/ocr_recognize.py screenshot.png -o result.txt

# 图片压缩（限制 200KB 以内）
python scripts/compress_image.py large.png --max-size 200 --format jpg

# 蓝底一寸证件照
python scripts/id_photo.py portrait.jpg --spec 一寸 --bg blue -o id_photo.jpg
```

## 支持的证件照规格

一寸、小一寸、大一寸、二寸、小二寸、三寸、护照、美国签证、日本签证

## 作为 WorkBuddy Skill 安装

将本仓库克隆到 `~/.workbuddy/skills/toolbox-10-skill/` 即可。

## License

MIT
