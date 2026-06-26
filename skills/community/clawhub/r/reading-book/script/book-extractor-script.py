"""
书籍章节提取脚本
从Word或PDF文档中提取章节结构并分割内容
"""

import os
import re
from docx import Document
import PyPDF2


def read_book(book_path):
    """
    读取Word或PDF文档
    Args:
        book_path: 书籍完整路径
    Returns:
        Document对象 (Word) 或 文本列表 (PDF), 文件类型
    """
    file_ext = os.path.splitext(book_path)[1].lower()

    if file_ext == '.docx':
        doc = Document(book_path)
        return doc, 'docx'
    elif file_ext == '.pdf':
        text_blocks = extract_pdf_text(book_path)
        return text_blocks, 'pdf'
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")


def extract_pdf_text(book_path):
    """
    从PDF提取文本，按段落分割
    Returns:
        list: 段落文本列表
    """
    text_blocks = []
    
    try:
        with open(book_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                # 按段落分割文本
                paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
                text_blocks.extend(paragraphs)
    except Exception as e:
        raise Exception(f"PDF提取失败: {str(e)}")
    
    return text_blocks


def detect_chapter_title(text):
    """
    检测是否为章节标题
    Args:
        text: 文本内容
    Returns:
        bool: 是否为章节标题
    """
    if not text or len(text.strip()) == 0:
        return False
    
    text = text.strip()
    
    # 规则1: CHAPTER开头
    if 'CHAPTER' in text.upper()[:20]:
        return True
    
    # 规则2: Chapter X格式
    if text.startswith('Chapter ') and len(text) > 9 and text[8:9].isdigit():
        return True
    
    # 规则3: 第X章格式
    if text.startswith('第') and '章' in text[:10]:
        return True
    
    # 规则4: 全大写且较短（可能为标题）
    if len(text) < 100 and text.isupper() and any(char.isdigit() for char in text):
        return True
    
    return False


def clean_pdf_text(text):
    """
    清理PDF提取的文本噪音
    Args:
        text: 原始文本
    Returns:
        str: 清理后的文本 或 None（如果是噪音）
    """
    # 移除页码
    text = re.sub(r'^\d+\s*$', '', text)
    
    # 移除过短的行（可能是页眉页脚）
    if len(text) < 5:
        return None
    
    return text.strip()


def extract_chapters(doc, file_type):
    """
    提取章节列表
    Args:
        doc: Document对象 (docx) 或 文本列表 (pdf)
        file_type: 'docx' 或 'pdf'
    Returns:
        list: 章节列表
    """
    chapters = []
    current_chapter = None
    chapter_counter = 0

    if file_type == 'docx':
        # Word文档处理
        for idx, para in enumerate(doc.paragraphs):
            text = para.text.strip()
            if not text:
                continue

            # 检测章节标题
            is_chapter = detect_chapter_title(text)
            
            if is_chapter:
                chapter_counter += 1
                current_chapter = {
                    "chapter": chapter_counter,
                    "title": text,
                    "start_paragraph": idx,
                    "paragraphs": []
                }
                chapters.append(current_chapter)
            elif current_chapter:
                current_chapter["paragraphs"].append(text)
    
    elif file_type == 'pdf':
        # PDF文档处理
        for idx, text in enumerate(doc):
            # 清理文本
            cleaned = clean_pdf_text(text)
            if not cleaned:
                continue

            # 检测章节标题
            is_chapter = detect_chapter_title(cleaned)
            
            if is_chapter:
                chapter_counter += 1
                current_chapter = {
                    "chapter": chapter_counter,
                    "title": cleaned,
                    "start_paragraph": idx,
                    "paragraphs": []
                }
                chapters.append(current_chapter)
            elif current_chapter:
                current_chapter["paragraphs"].append(cleaned)

    return chapters


def validate_book_path(book_path):
    """
    验证书籍路径
    Args:
        book_path: 书籍路径
    Returns:
        dict: 验证结果和文件信息
    """
    if not os.path.exists(book_path):
        return {
            "success": False,
            "error": f"文件不存在: {book_path}"
        }
    
    file_ext = os.path.splitext(book_path)[1].lower()
    if file_ext not in ['.docx', '.pdf']:
        return {
            "success": False,
            "error": f"不支持的文件格式: {file_ext}，仅支持.docx和.pdf"
        }
    
    file_size = os.path.getsize(book_path)
    
    return {
        "success": True,
        "file_type": file_ext,
        "file_size": file_size,
        "file_size_mb": round(file_size / (1024 * 1024), 2)
    }


def generate_chapter_summary(chapters):
    """
    生成章节统计
    Args:
        chapters: 章节列表
    Returns:
        list: 章节统计信息
    """
    summary = []
    for chapter in chapters:
        para_count = len(chapter.get('paragraphs', []))
        estimated_chars = sum(len(p) for p in chapter.get('paragraphs', []))
        
        summary.append({
            "chapter": chapter['chapter'],
            "title": chapter['title'],
            "paragraph_count": para_count,
            "estimated_chars": estimated_chars,
            "estimated_kb": round(estimated_chars / 1024, 2)
        })
    
    return summary


def process_book(book_path, book_title=None):
    """
    处理书籍的主函数
    Args:
        book_path: 书籍路径
        book_title: 书名（可选，默认从路径提取）
    Returns:
        dict: 处理结果
    """
    # 验证路径
    validation = validate_book_path(book_path)
    if not validation['success']:
        return {
            "success": False,
            "error": validation['error']
        }
    
    # 提取书名
    if book_title is None:
        book_title = os.path.basename(os.path.dirname(book_path))
    
    try:
        # 读取文档
        doc, file_type = read_book(book_path)
        
        # 提取章节
        chapters = extract_chapters(doc, file_type)
        
        if len(chapters) == 0:
            return {
                "success": False,
                "error": "无法识别章节，请检查文档格式或章节标题格式"
            }
        
        # 生成统计
        summary = generate_chapter_summary(chapters)
        
        return {
            "success": True,
            "book_info": {
                "title": book_title,
                "path": book_path,
                "file_type": file_type,
                "total_chapters": len(chapters),
                "file_size_mb": validation['file_size_mb']
            },
            "chapters": chapters,
            "summary": summary
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"处理失败: {str(e)}"
        }


# 使用示例
if __name__ == "__main__":
    # 示例: 处理Word文档
    result = process_book(r"F:\book\Security Analysis\Security Analysis.docx")
    if result['success']:
        print(f"成功提取 {result['book_info']['total_chapters']} 个章节")
        for ch in result['summary'][:3]:
            print(f"  Chapter {ch['chapter']}: {ch['paragraph_count']} 段落")
    else:
        print(f"错误: {result['error']}")
