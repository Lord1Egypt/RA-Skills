---
name: tiff-merge
version: 1.0.1
description: 合并图片为 TIFF 或拆分 TIFF 为单张图片（本地处理，隐私安全）
metadata:
  openclaw:
    emoji: 🖼️
    requires:
      bins:
        - node
    install:
      - kind: npm
        package: utif
---

# TIFF Merge & Split Skill

将多张图片合并为多页 TIFF 文件，或将 TIFF 拆分为单张图片，完全本地处理，隐私安全。

## 使用方法

### 合并模式

```bash
# 合并多张图片为 TIFF
node index.js merge image1.jpg image2.jpg image3.jpg -o output.tiff
```

### 拆分模式

```bash
# 拆分 TIFF 为单张图片
node index.js split input.tiff -o output_folder/
```

## 功能特点

- ✅ 本地处理，文件不上传
- ✅ 支持 JPG/PNG/TIFF 格式
- ✅ 多张图片合并为多页 TIFF
- ✅ TIFF 拆分为单张图片
- ✅ 隐私安全

## 示例

### 合并图片

```bash
# 合并旅游照片
node index.js merge photo1.jpg photo2.jpg photo3.jpg -o travel.tiff

# 合并文档扫描件
node index.js merge scan_001.png scan_002.png scan_003.png -o document.tiff
```

### 拆分 TIFF

```bash
# 拆分为 PNG 图片
node index.js split document.tiff -o ./output/ --format png

# 拆分为 JPG 图片
node index.js split document.tiff -o ./output/ --format jpg
```

## 许可证

MIT

## 作者

fly3094
