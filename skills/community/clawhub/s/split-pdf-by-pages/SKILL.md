---
name: split-pdf-by-pages
description: 将PDF中包含 显示日期 的页面切割成单独的文件，新文件以原文件名_页数命名。当用户需要从PDF中提取包含特定日期标识的页面时使用。
---

# PDF按页切割（含 显示日期 的页面）

扫描PDF每一页，只将包含 显示日期 文本的页面切割成独立的PDF文件，新文件命名格式为：`原文件名_p页码.pdf`

## 功能说明

- 扫描PDF每一页的内容
- 只提取包含 显示日期 的页面
- 文件名格式：`原文件名_p页码.pdf`
- 保留原PDF的所有格式和内容
- 支持批量处理多个PDF文件

## 使用方法

### Python脚本方式

```python
from pypdf import PdfReader, PdfWriter
from pdf2image import convert_from_path
import pytesseract
import os

def extract_text_with_ocr(pdf_path, page_num):
    """
    使用OCR从PDF页面提取文字（用于扫描件）
    
    Args:
        pdf_path: PDF文件路径
        page_num: 页码（从0开始）
    
    Returns:
        str: 提取的文字
    """
    try:
        # 将PDF页面转为图片
        images = convert_from_path(pdf_path, first_page=page_num+1, last_page=page_num+1)
        if images:
            # 使用OCR识别文字
            text = pytesseract.image_to_string(images[0], lang='chi_sim')
            return text
    except Exception as e:
        print(f"  OCR识别第 {page_num+1} 页时出错: {e}")
    return ""


def split_pdf_by_pages(input_path, output_dir=None, keyword="显示日期", use_ocr=False):
    """
    将PDF中包含指定关键词的页面切割成多个文件
    
    Args:
        input_path: 输入PDF文件路径
        output_dir: 输出目录（默认为原文件所在目录）
        keyword: 要搜索的关键词，默认为 显示日期
        use_ocr: 是否使用OCR识别扫描件，默认为False
    
    Returns:
        list: 生成的文件路径列表
    """
    # 获取文件信息
    input_path = os.path.abspath(input_path)
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    
    if output_dir is None:
        output_dir = os.path.dirname(input_path)
    else:
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)
    
    # 读取PDF
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    output_files = []
    matched_pages = []
    
    print(f"正在处理: {os.path.basename(input_path)}")
    print(f"总页数: {total_pages}")
    print(f"搜索关键词: 显示日期")
    if use_ocr:
        print("已启用OCR识别（用于扫描件）")
    
    # 先扫描所有页面，找出包含关键词的页面
    for page_num in range(total_pages):
        page = reader.pages[page_num]
        text = page.extract_text() or ""
        
        # 如果文本为空且启用OCR，则使用OCR识别
        if not text and use_ocr:
            print(f"  第 {page_num + 1} 页无文本，尝试OCR识别...")
            text = extract_text_with_ocr(input_path, page_num)
        
        if "显示日期" in text:
            matched_pages.append(page_num)
            print(f"  第 {page_num + 1} 页包含关键词")
    
    if not matched_pages:
        print(f"未找到包含 显示日期 的页面")
        return []
    
    print(f"共找到 {len(matched_pages)} 个包含 显示日期 的页面")
    
    # 只切割包含关键词的页面
    for page_num in matched_pages:
        writer = PdfWriter()
        writer.add_page(reader.pages[page_num])
        
        # 生成输出文件名: 原文件名_页码.pdf
        output_filename = f"{base_name}_p{page_num + 1}.pdf"
        output_path = os.path.join(output_dir, output_filename)
        
        # 写入文件
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        output_files.append(output_path)
        print(f"  已生成: {output_filename}")
    
    print(f"完成！共生成 {len(output_files)} 个文件")
    print(f"输出目录: {output_dir}")
    
    return output_files


def split_pdfs_in_directory(input_dir, output_dir=None, use_ocr=False):
    """
    批量处理目录中的所有PDF文件
    
    Args:
        input_dir: 输入目录路径
        output_dir: 输出目录路径（默认为输入目录下的split子目录）
        use_ocr: 是否使用OCR识别扫描件
    """
    input_dir = os.path.abspath(input_dir)
    
    if output_dir is None:
        output_dir = os.path.join(input_dir, 'split')
    else:
        output_dir = os.path.abspath(output_dir)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 查找所有PDF文件
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"在 {input_dir} 中未找到PDF文件")
        return
    
    print(f"找到 {len(pdf_files)} 个PDF文件")
    if use_ocr:
        print("已启用OCR识别（用于扫描件）")
    print("=" * 50)
    
    all_outputs = []
    for pdf_file in pdf_files:
        input_path = os.path.join(input_dir, pdf_file)
        # 为每个PDF创建子目录
        file_output_dir = os.path.join(output_dir, os.path.splitext(pdf_file)[0])
        outputs = split_pdf_by_pages(input_path, file_output_dir, use_ocr=use_ocr)
        all_outputs.extend(outputs)
        print("-" * 50)
    
    print(f"\n全部完成！共生成 {len(all_outputs)} 个文件")
    print(f"所有文件保存在: {output_dir}")
    
    return all_outputs


# 使用示例
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python split_pdf.py <PDF文件路径> [输出目录] [--ocr]")
        print("  python split_pdf.py --dir <目录路径> [输出目录]")
        print()
        print("示例:")
        print("  python split_pdf.py document.pdf")
        print("  python split_pdf.py document.pdf ./output")
        print("  python split_pdf.py document.pdf ./output --ocr")
        print("  python split_pdf.py --dir ./pdfs")
        sys.exit(1)
    
    # 检查是否启用OCR
    use_ocr = '--ocr' in sys.argv
    if use_ocr:
        sys.argv.remove('--ocr')
    
    if sys.argv[1] == '--dir':
        # 批量处理目录
        input_dir = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else None
        split_pdfs_in_directory(input_dir, output_dir, use_ocr=use_ocr)
    else:
        # 处理单个文件
        input_path = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
        split_pdf_by_pages(input_path, output_dir, use_ocr=use_ocr)
```

### 命令行方式

**安装依赖**:
```bash
# 基础依赖
pip install pypdf

# OCR依赖（用于扫描件PDF）
pip install pdf2image pytesseract

# 安装Tesseract-OCR引擎
# macOS:
brew install tesseract tesseract-lang

# Ubuntu/Debian:
# sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim

# Windows:
# 下载安装包: https://github.com/UB-Mannheim/tesseract/wiki
```

**切割单个PDF**（普通PDF）:
```bash
python split_pdf.py document.pdf
```

**切割扫描件PDF**（启用OCR）:
```bash
python split_pdf.py document.pdf --ocr
```

输出：`document_p1.pdf`, `document_p2.pdf`...（仅包含 显示日期 的页面）

**指定输出目录**:
```bash
python split_pdf.py document.pdf ./output
```

**批量处理目录**:
```bash
python split_pdf.py --dir ./pdfs
```

## 输出示例

输入文件：`report.pdf`（共5页，其中第2页和第4页包含 显示日期）

处理过程：
```
正在处理: report.pdf
总页数: 5
搜索关键词: 显示日期
  第 2 页包含关键词
  第 4 页包含关键词
共找到 2 个包含 显示日期 的页面
  已生成: report_p2.pdf
  已生成: report_p4.pdf
完成！共生成 2 个文件
```

输出文件：
```
report_p2.pdf  （原第2页，包含 显示日期）
report_p4.pdf  （原第4页，包含 显示日期）
```

## 注意事项

1. **依赖安装**: 需要安装 `pypdf` 库 (`pip install pypdf`)
2. **文件覆盖**: 如果输出文件已存在，将被覆盖
3. **命名冲突**: 同一目录下不要有不同扩展名的同名文件
4. **大文件处理**: 对于页数很多的PDF，处理时间可能较长

## 进阶用法

### 提取指定页面范围

```python
def split_pdf_range(input_path, start_page, end_page, output_path):
    """提取指定页面范围到新PDF"""
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for page_num in range(start_page - 1, end_page):
        writer.add_page(reader.pages[page_num])
    
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)
    
    print(f"已提取第 {start_page}-{end_page} 页到: {output_path}")

# 示例：提取第3-5页
split_pdf_range('document.pdf', 3, 5, 'document_pages_3_5.pdf')
```

### 按指定页数分组切割

```python
def split_pdf_by_group(input_path, pages_per_file, output_dir=None):
    """
    按指定页数分组切割PDF
    例如：每2页一个文件
    """
    input_path = os.path.abspath(input_path)
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    
    if output_dir is None:
        output_dir = os.path.dirname(input_path)
    else:
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)
    
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    
    file_count = 0
    for start in range(0, total_pages, pages_per_file):
        writer = PdfWriter()
        end = min(start + pages_per_file, total_pages)
        
        for page_num in range(start, end):
            writer.add_page(reader.pages[page_num])
        
        file_count += 1
        output_filename = f"{base_name}_part{file_count}.pdf"
        output_path = os.path.join(output_dir, output_filename)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        print(f"已生成: {output_filename} (第{start+1}-{end}页)")
    
    print(f"完成！共生成 {file_count} 个文件")

# 示例：每3页一个文件
split_pdf_by_group('document.pdf', 3)
```

## 常见问题

**Q: 切割后的PDF文件大小比原文件大？**
A: 这是正常现象，因为每个单页文件都包含完整的PDF结构信息。

**Q: 如何处理加密的PDF？**
A: 需要先解密PDF：
```python
reader = PdfReader('encrypted.pdf')
if reader.is_encrypted:
    reader.decrypt('password')
```

**Q: 能否保持原PDF的书签和元数据？**
A: 基础切割不包含书签，如需保留元数据，需要使用更高级的库如 `pikepdf`。
