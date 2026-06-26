"""
Word to JPG Converter - OpenClaw Skill
将 Word 文档转换为高质量 JPG 图片

依赖：pip install comtypes pymupdf -q
"""

import os
import sys
import shutil
import comtypes.client
import fitz  # PyMuPDF

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')

# 配置
BASE_DIR = os.path.expanduser("~/.openclaw")
OUTPUT_DIR = os.path.join(BASE_DIR, "media/outbound/word-images")
TEMP_DIR = os.path.join(BASE_DIR, "workspace/temp")
INBOUND_DIR = os.path.join(BASE_DIR, "media/inbound")

def find_latest_docx(custom_path=None):
    """查找最新的 Word 文档"""
    if custom_path and os.path.exists(custom_path):
        if os.path.isfile(custom_path) and custom_path.lower().endswith(('.docx', '.doc')):
            return custom_path
        elif os.path.isdir(custom_path):
            # 查找目录中最新的 docx 文件
            docx_files = [f for f in os.listdir(custom_path) if f.lower().endswith(('.docx', '.doc'))]
            if docx_files:
                latest = max(docx_files, key=lambda f: os.path.getmtime(os.path.join(custom_path, f)))
                return os.path.join(custom_path, latest)
    
    # 默认从 inbound 目录查找
    if os.path.exists(INBOUND_DIR):
        docx_files = [f for f in os.listdir(INBOUND_DIR) if f.lower().endswith(('.docx', '.doc'))]
        if docx_files:
            latest = max(docx_files, key=lambda f: os.path.getmtime(os.path.join(INBOUND_DIR, f)))
            return os.path.join(INBOUND_DIR, latest)
    
    return None

def copy_to_temp(source_path):
    """复制文件到临时目录（避免中文路径问题）"""
    os.makedirs(TEMP_DIR, exist_ok=True)
    temp_path = os.path.join(TEMP_DIR, "source.docx")
    shutil.copy2(source_path, temp_path)
    return temp_path

def word_to_pdf(docx_path, pdf_path):
    """使用 Word COM 接口导出 PDF"""
    print(f"正在启动 Word...")
    word = comtypes.client.CreateObject("Word.Application")
    word.Visible = False
    
    try:
        print(f"正在打开文档：{os.path.basename(docx_path)}")
        doc = word.Documents.Open(docx_path, ReadOnly=True)
        
        print(f"正在导出 PDF...")
        doc.SaveAs2(pdf_path, 17)  # 17 = wdFormatPDF
        
        doc.Close(False)
        print(f"PDF 已保存：{pdf_path}")
        return True
        
    except Exception as e:
        print(f"错误：{e}")
        return False
        
    finally:
        word.Quit()

def pdf_to_jpg(pdf_path, output_dir):
    """使用 PyMuPDF 将 PDF 转为高质量 JPG"""
    print(f"\n正在打开 PDF...")
    doc = fitz.open(pdf_path)
    page_count = len(doc)
    print(f"总页数：{page_count}")
    
    # 清理旧的图片文件
    for f in os.listdir(output_dir):
        if f.endswith(('.jpg', '.png')):
            os.remove(os.path.join(output_dir, f))
    
    # 4 倍缩放 = 约 300 DPI
    zoom = 4.0
    mat = fitz.Matrix(zoom, zoom)
    
    for page_num in range(page_count):
        print(f"正在转换第 {page_num + 1} 页...")
        page = doc[page_num]
        pix = page.get_pixmap(matrix=mat)
        
        output_path = os.path.join(output_dir, f"page_{page_num + 1}.jpg")
        pix.save(output_path, output='jpeg', jpg_quality=95)
        print(f"已保存：{output_path} ({pix.width}×{pix.height})")
    
    doc.close()
    
    # 删除临时 PDF
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        print(f"临时 PDF 已清理")
    
    return page_count

def convert_word_to_jpg(custom_path=None):
    """主函数：Word → PDF → JPG"""
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 查找 Word 文档
    source_path = find_latest_docx(custom_path)
    if not source_path:
        print("错误：未找到 Word 文档")
        print("请确保已发送 Word 文档，或提供文件路径")
        return False
    
    print(f"找到文档：{os.path.basename(source_path)}")
    
    # 复制到临时目录（避免中文路径问题）
    temp_path = copy_to_temp(source_path)
    print(f"已复制到临时目录")
    
    # 转换为 PDF
    pdf_path = os.path.join(OUTPUT_DIR, "temp.pdf")
    if not word_to_pdf(temp_path, pdf_path):
        return False
    
    # 转换为 JPG
    page_count = pdf_to_jpg(pdf_path, OUTPUT_DIR)
    
    print(f"\n✅ 转换完成！")
    print(f"输出目录：{OUTPUT_DIR}")
    print(f"共生成 {page_count} 张图片")
    
    return True

# 命令行入口
if __name__ == "__main__":
    custom_path = sys.argv[1] if len(sys.argv) > 1 else None
    success = convert_word_to_jpg(custom_path)
    sys.exit(0 if success else 1)
