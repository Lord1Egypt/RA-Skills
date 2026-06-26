import PyPDF2
import os

pdf_path = r'C:\Users\Andapeng\.openclaw\workspace\skills\volcengine\references\volcengine-api-reference.pdf'

# 提取指定页面
pages_to_extract = [7, 10, 11, 12, 13, 14, 15, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470]

# 创建输出目录
output_dir = r'C:\Users\Andapeng\.openclaw\workspace\skills\volcengine\references\extracted_pages'
os.makedirs(output_dir, exist_ok=True)

print(f"开始提取PDF页面...")
print(f"PDF路径: {pdf_path}")
print(f"输出目录: {output_dir}")
print(f"要提取的页面: {pages_to_extract}")

with open(pdf_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    total_pages = len(pdf_reader.pages)
    print(f"PDF总页数: {total_pages}")
    
    for page_num in pages_to_extract:
        if page_num <= total_pages:
            page = pdf_reader.pages[page_num - 1]
            text = page.extract_text()
            
            # 保存为单独的txt文件
            output_file = os.path.join(output_dir, f'page_{page_num:03d}.txt')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            # 打印预览
            preview = text[:500] if text else "(无文本内容)"
            print(f"\n=== 第 {page_num} 页 ===")
            print(f"已保存到: {output_file}")
            print(f"预览: {preview}...")
        else:
            print(f"\n警告: 第 {page_num} 页超出PDF总页数 ({total_pages})")

print("\n页面提取完成！")