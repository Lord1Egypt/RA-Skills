import PyPDF2
import os
import sys

pdf_path = r'C:\Users\Andapeng\.openclaw\workspace\skills\volcengine\references\volcengine-api-reference.pdf'
output_dir = r'C:\Users\Andapeng\.openclaw\workspace\skills\volcengine\references\extracted_pages'
os.makedirs(output_dir, exist_ok=True)

# 所有需要提取的页面
all_pages = [7, 10, 11, 12, 13, 14, 15, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470]

# 检查已经提取的页面
extracted_pages = []
for page_num in all_pages:
    output_file = os.path.join(output_dir, f'page_{page_num:03d}.txt')
    if os.path.exists(output_file):
        extracted_pages.append(page_num)

# 计算还需要提取的页面
remaining_pages = [p for p in all_pages if p not in extracted_pages]

print(f"已提取的页面: {extracted_pages}")
print(f"需要提取的剩余页面: {remaining_pages}")

if not remaining_pages:
    print("所有页面已提取完成！")
    sys.exit(0)

print(f"\n开始提取剩余页面...")
with open(pdf_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    total_pages = len(pdf_reader.pages)
    print(f"PDF总页数: {total_pages}")
    
    for page_num in remaining_pages:
        if page_num <= total_pages:
            try:
                page = pdf_reader.pages[page_num - 1]
                text = page.extract_text()
                
                # 保存为单独的txt文件
                output_file = os.path.join(output_dir, f'page_{page_num:03d}.txt')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                # 打印简单的日志信息，避免编码问题
                print(f"已提取第 {page_num} 页，保存到: {output_file}")
                
            except Exception as e:
                print(f"提取第 {page_num} 页时出错: {e}")
        else:
            print(f"警告: 第 {page_num} 页超出PDF总页数 ({total_pages})")

print("\n剩余页面提取完成！")