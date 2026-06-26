# 数科文印格式自动化工具包

## 简介

本工具包提供了一套完整的自动化解决方案，用于按照数科公司的严格文印格式要求处理文档。

## 核心功能

- **智能文档格式化**：自动识别文档结构，应用正确的字体、字号、对齐方式
- **精确PDF生成**：使用指定字体生成完全符合格式要求的PDF
- **字体安装与管理**：一键安装所需字体，验证安装结果
- **批量处理**：支持批量转换文件夹中的所有文档
- **格式验证**：检查PDF使用的字体是否符合要求

## 快速开始

### 1. 安装依赖

```bash
pip install python-docx
```

### 2. 安装字体

```bash
python install_shuke_fonts.py
python verify_shuke_fonts.py
```

### 3. 格式化文档

```bash
python smart_format_v3.py input.docx formatted.docx
```

### 4. 生成PDF

```bash
python convert_to_pdf_shuke_final.py formatted.docx output.pdf
```

## 工具列表

- `smart_format_v3.py` - 智能文档格式化工具
- `convert_to_pdf_shuke_final.py` - PDF生成工具
- `install_shuke_fonts.py` - 字体安装工具
- `verify_shuke_fonts.py` - 字体验证工具
- `batch_convert_shuke_pdf.py` - 批量转换工具
- `check_pdf_fonts.py` - PDF字体检查工具
- `doc_generator.py` - 文档生成器
- `generate_proper_example.py` - 示例生成器

## 格式要求

本工具包严格按照数科公司文印格式要求实现：

- **标题**：方正小标宋简体，二号，居中
- **一级标题**：黑体，三号，左对齐
- **二级标题**：楷体GB2312，三号，加粗，左对齐
- **三级标题**：仿宋GB2312，三号，左对齐
- **正文**：仿宋GB2312，三号，首行缩进2字符
- **页面设置**：上3.5cm，下3.5cm，左2.8cm，右2.8cm
- **网格要求**：28字/行，22行/页
- **行距**：固定值28磅

## 许可证

MIT-0 License