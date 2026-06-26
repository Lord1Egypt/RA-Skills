---
name: textin-parse
version: "1.0.0"
description: |
  Textin 文档解析 API 封装，支持上传图片/pdf/word/html/excel/ppt/txt 等格式进行版面检测、文字识别、表格识别，生成 markdown 文档及结构化数据。
  用于：(1) 解析 PDF/图片/文档为 markdown；(2) 提取文档结构化数据；(3) 识别表格和公式；(4) 提取目录。
  触发方式：用户询问文档解析、PDF 转 markdown、提取文档内容等。
---

# Textin 文档解析

## 快速开始

### 第1步：注册获取 API 凭证

首次使用需要先注册 Textin 账号并获取 API 凭证：

1. 访问注册链接：https://www.textin.com/register/code/3EJS7P
2. 注册完成后，登录并进入"开发者与账户信息"页面
3. 获取 `x-ti-app-id` 和 `x-ti-secret-code`

获取凭证后，告诉我这两个值，我会帮你配置。

### 第2步：配置凭证

告诉我你的 `x-ti-app-id` 和 `x-ti-secret-code`，我会保存到配置文件中。

### 第3步：解析文档

配置好凭证后，你可以这样使用：

```
解析这个PDF文件
解析这张图片为markdown
提取这个文档的目录结构
```

## 支持的文件格式

- 图片：png, jpg, jpeg, bmp, tiff, webp
- 文档：pdf, doc, docx, html, mhtml, xls, xlsx, csv, ppt, pptx, txt, ofd, rtf
- 文件大小：最大 500MB

## 可选参数说明

### 解析模式 (parse_mode)

- `auto` - 由引擎自动选择，适用范围最广
- `scan` - 文档统一当成图片解析
- `lite` - 轻量版，只输出表格和文字结果
- `parse` - 仅电子档文字解析，速度最快
- `vlm` - 视觉语言模型解析模式

默认：`scan`

### 表格格式 (table_flavor)

- `html` - 按 HTML 语法输出表格
- `md` - 按 Markdown 语法输出表格
- `none` - 不进行表格识别

默认：`html`

### 获取图片 (get_image)

- `none` - 不返回任何图像
- `page` - 返回每一页的整页图像
- `objects` - 返回页面内的子图像
- `both` - 返回整页图像和图像对象

默认：`objects`

### 标题层级 (apply_document_tree)

- `1` - 生成标题层级
- `0` - 不生成标题

默认：`1`

### 公式识别 (formula_level)

- `0` - 全识别
- `1` - 仅识别行间公式
- `2` - 不识别

默认：`0`

### 去水印 (remove_watermark)

- `0` - 不去水印
- `1` - 去水印

默认：`0`

### 图表识别 (apply_chart)

- `0` - 不开启图表识别
- `1` - 开启图表识别，以表格形式输出

默认：`0`

### 其他常用参数

- `pdf_pwd` - PDF 密码（加密文档时使用）
- `page_start` - 从第几页开始解析（PDF 时有效）
- `page_count` - 解析的页数（默认 1000，最大 1000）
- `dpi` - 坐标基准（72/144/216，默认 144）
- `get_excel` - 是否返回 Excel（0 或 1）
- `crop_dewarp` - 是否切边矫正（0 或 1）
- `markdown_details` - 是否返回 detail 字段（0 或 1，默认 1）
- `page_details` - 是否返回 pages 字段（0 或 1，默认 1）

## 使用示例

### 基础用法

```
帮我解析这个PDF文件
```

### 指定参数

```
用 parse 模式解析这个PDF
用 lite 模式解析，输出 markdown 表格
解析这个文件并提取目录
```

## 错误码处理

常见错误：
- `40101` - App ID 或 Secret 为空
- `40102` - App ID 或 Secret 无效
- `40003` - 余额不足
- `40303` - 文件类型不支持

如遇错误，请检查凭证是否正确，或咨询用户。