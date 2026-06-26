---
name: url-images-to-pdf
version: 1.0.2
description: 从URL提取图片并生成PDF（保持原文顺序，不排序）
author: OpenClaw
tags: [pdf, images, extraction]
---

# URL图片转PDF技能

## 功能
从网页URL提取图片并生成PDF文件

## 前置要求
1. Node.js 已安装
2. pdfkit 已安装: `npm install -g pdfkit`



### 方式## 使用方法1: 命令行
```bash
# 安装依赖
npm install -g pdfkit

# 运行脚本
node ~/.openclaw/workspace/skills/url-images-to-pdf/extract.js <URL> [输出文件名]
```

### 方式2: 在OpenClaw中调用

直接运行:
```bash
node ~/.openclaw/workspace/skills/url-images-to-pdf/extract.js "https://example.com/article"
```

## 输出
- PDF文件保存在当前目录或指定目录
- 自动从网页提取PNG/JPG图片

## 依赖安装
```bash
npm install -g pdfkit
```

## 示例
提取微信文章图片并生成PDF:
```bash
node ~/.openclaw/workspace/skills/url-images-to-pdf/extract.js "https://mp.weixin.qq.com/s/XXXX"
```

## 注意事项
- 需要网络访问权限
- 某些网站可能有反爬措施
- 建议先提取图片，确认数量后再生成PDF
