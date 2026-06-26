---
name: tiff-merge
description: 将多张图片合并为多页 TIFF 文件（本地处理，隐私安全）
version: 1.0.0
metadata:
  openclaw:
    emoji: 🖼️
    requires:
      bins:
        - node
      env: []
    install:
      - kind: npm
        package: utif
        bins: []
---

# TIFF Merge Skill

将多张图片合并为多页 TIFF 文件，完全本地处理，隐私安全。

## 功能特点

- ✅ **本地处理** - 文件不上传，隐私安全
- ✅ **多格式支持** - 支持 JPG、PNG、TIFF 格式
- ✅ **多页合成** - 将多张图片合并为多页 TIFF
- ✅ **图片编辑** - 支持旋转、调整顺序
- ✅ **快速高效** - 基于 UTIF.js，处理速度快

## 使用方法

### 通过 OpenClaw 自然语言调用

```
帮我把这几张图片合并成 TIFF
将 image1.jpg, image2.jpg, image3.jpg 转换为多页 TIFF
帮我生成一个 TIFF 文件，包含这些图片
```

### 命令行使用

```bash
# 基本用法
node index.js image1.jpg image2.jpg image3.jpg output.tiff

# 自动命名输出文件
node index.js image1.jpg image2.jpg image3.jpg
# 输出：merged-1713088800000.tiff
```

## 示例

### 示例 1：合并旅游照片

```bash
node index.js photo1.jpg photo2.jpg photo3.jpg travel.tiff
```

### 示例 2：合并文档扫描件

```bash
node index.js scan_001.png scan_002.png scan_003.png document.tiff
```

## 技术实现

- **核心库**: [UTIF.js](https://github.com/photopea/UTIF.js)
- **运行环境**: Node.js 14+
- **处理模式**: 本地处理，无需服务器

## 隐私说明

- ✅ 所有处理在本地完成
- ✅ 文件不上传到任何服务器
- ✅ 不收集任何用户数据
- ✅ 开源代码，可审计

## 许可证

MIT License

## 作者

fly3094
