---
name: pdf-toolkit
description: PDF 工具箱技能。支持 PDF 合并、拆分、旋转、压缩、格式转换、文字提取、水印添加等常用操作。使用场景：(1) 合并多个 PDF，(2) 拆分 PDF 页面，(3) 旋转/调整方向，(4) 压缩 PDF 大小，(5) PDF 转图片/Word，(6) 提取 PDF 文字，(7) 添加/移除水印。
---

# PDF 工具箱

## 核心功能

提供一站式 PDF 处理解决方案，满足日常办公、学习中的各种 PDF 处理需求。

### 支持的操作
- 📎 **合并** - 多个 PDF 合并成一个
- ✂️ **拆分** - 按页码拆分 PDF
- 🔄 **旋转** - 调整页面方向
- 📦 **压缩** - 减小 PDF 文件大小
- 📝 **转换** - PDF 转 Word/图片/文本
- 📄 **提取** - 提取 PDF 中的文字/图片
- 💧 **水印** - 添加或移除水印
- 🔒 **加密** - 设置密码保护

---

## 使用方式

### 1. 合并 PDF

用户请求示例：
- "把这几个 PDF 合并成一个"
- "合并 report1.pdf, report2.pdf, report3.pdf"

**命令：**
```bash
python scripts/merge_pdf.py --output merged.pdf file1.pdf file2.pdf file3.pdf
```

### 2. 拆分 PDF

用户请求示例：
- "把这个 PDF 拆分成单独页面"
- "提取第 1-5 页"

**命令：**
```bash
python scripts/split_pdf.py --input input.pdf --pages 1-5 --output output.pdf
```

### 3. 旋转 PDF

用户请求示例：
- "把这个 PDF 顺时针旋转 90 度"
- "所有页面旋转 180 度"

**命令：**
```bash
python scripts/rotate_pdf.py --input input.pdf --angle 90 --output output.pdf
```

### 4. 压缩 PDF

用户请求示例：
- "压缩这个 PDF，太大了"
- "把 PDF 压缩到 5MB 以内"

**命令：**
```bash
python scripts/compress_pdf.py --input input.pdf --output output.pdf --quality medium
```

### 5. PDF 转换

用户请求示例：
- "把 PDF 转成 Word"
- "PDF 转图片"

**命令：**
```bash
python scripts/convert_pdf.py --input input.pdf --format word --output output.docx
python scripts/convert_pdf.py --input input.pdf --format image --output-dir images/
```

### 6. 提取文字

用户请求示例：
- "提取这个 PDF 的文字内容"
- "把 PDF 转成文本"

**命令：**
```bash
python scripts/extract_text.py --input input.pdf --output output.txt
```

### 7. 添加水印

用户请求示例：
- "给 PDF 添加水印"
- "加上'机密'两个字"

**命令：**
```bash
python scripts/watermark.py --input input.pdf --text "机密" --output output.pdf
```

---

## 质量选项

### 压缩质量
| 选项 | 说明 | 适用场景 |
|------|------|---------|
| low | 高压缩，质量较低 | 邮件发送、网页展示 |
| medium | 平衡压缩和质量 | 日常使用 |
| high | 低压缩，保持质量 | 打印、存档 |

### 转换格式
| 格式 | 说明 | 保留内容 |
|------|------|---------|
| word | 转 Word 文档 | 文字、格式、图片 |
| image | 转图片（PNG） | 每页一张图片 |
| text | 纯文本 | 仅文字内容 |
| html | 网页格式 | 文字、基本格式 |

---

## 常见问题

### Q: 合并后顺序不对怎么办？
A: 按文件名排序，确保文件名有序（如 01.pdf, 02.pdf）

### Q: 压缩后文字模糊？
A: 使用 high 质量选项，或降低压缩比例

### Q: 提取的文字乱码？
A: 可能是扫描版 PDF，需要 OCR 功能（需额外安装）

### Q: 加密的 PDF 怎么处理？
A: 先提供密码解密，处理后再加密

---

## 批量处理

支持批量操作多个文件：

```bash
# 批量旋转当前目录所有 PDF
for f in *.pdf; do
  python scripts/rotate_pdf.py --input "$f" --angle 90 --output "rotated_$f"
done

# 批量压缩
for f in *.pdf; do
  python scripts/compress_pdf.py --input "$f" --output "compressed_$f" --quality medium
done
```

---

## 参考资源

- 脚本使用说明：见 `references/scripts.md`
- 常见问题解答：见 `references/faq.md`
- 批量处理示例：见 `references/batch-examples.md`
