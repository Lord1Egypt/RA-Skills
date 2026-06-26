"""
使用示例：PDF处理
"""

import asyncio
import base64
from main import execute


async def example_convert_pdf_to_word():
    """示例：PDF转Word"""
    with open("sample.pdf", "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode('utf-8')
    
    params = {
        "action": "PDF转Word",
        "action_type": "convert_pdf",
        "file_data": pdf_data,
        "target_format": "word",
        "preserve_formatting": True
    }
    
    result = await execute(params)
    
    if result["success"]:
        print(f"✓ {result['message']}")
        
        file_data = base64.b64decode(result["file_data"])
        with open("converted.docx", "wb") as f:
            f.write(file_data)
        print(f"✓ 文件已保存: {result['file_name']}")


async def example_convert_pdf_to_excel():
    """示例：PDF转Excel"""
    with open("tables.pdf", "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode('utf-8')
    
    params = {
        "action": "PDF转Excel",
        "action_type": "convert_pdf",
        "file_data": pdf_data,
        "target_format": "excel"
    }
    
    result = await execute(params)
    
    if result["success"]:
        file_data = base64.b64decode(result["file_data"])
        with open("tables.xlsx", "wb") as f:
            f.write(file_data)
        print(f"✓ PDF表格已转换为Excel")


async def example_extract_text():
    """示例：提取PDF文本"""
    with open("document.pdf", "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode('utf-8')
    
    params = {
        "action": "提取PDF文本",
        "action_type": "extract_pdf",
        "file_data": pdf_data,
        "extraction_type": "text",
        "page_range": "1-5"
    }
    
    result = await execute(params)
    
    if result["success"]:
        print(f"✓ {result['message']}")
        print(f"  总页数: {result['data']['page_count']}")
        print(f"  字数: {result['data']['word_count']}")
        print("\n提取内容:")
        print(result['data']['content'][:500] + "...")


async def example_extract_summary():
    """示例：提取PDF摘要"""
    with open("report.pdf", "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode('utf-8')
    
    params = {
        "action": "提取PDF摘要",
        "action_type": "extract_pdf",
        "file_data": pdf_data,
        "extraction_type": "summary"
    }
    
    result = await execute(params)
    
    if result["success"]:
        print(f"✓ 摘要提取成功")
        print("\n文档摘要:")
        print(result['data']['content'])


async def example_extract_key_points():
    """示例：提取PDF关键要点"""
    with open("paper.pdf", "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode('utf-8')
    
    params = {
        "action": "提取PDF关键要点",
        "action_type": "extract_pdf",
        "file_data": pdf_data,
        "extraction_type": "key_points"
    }
    
    result = await execute(params)
    
    if result["success"]:
        print(f"✓ 关键要点提取成功")
        print("\n关键要点:")
        print(result['data']['content'])


async def example_merge_pdfs():
    """示例：合并PDF"""
    files = []
    for filename in ["file1.pdf", "file2.pdf", "file3.pdf"]:
        with open(filename, "rb") as f:
            files.append(base64.b64encode(f.read()).decode('utf-8'))
    
    params = {
        "action": "合并PDF",
        "action_type": "merge_pdf",
        "files": files
    }
    
    result = await execute(params)
    
    if result["success"]:
        print(f"✓ {result['message']}")
        
        file_data = base64.b64decode(result["file_data"])
        with open("merged.pdf", "wb") as f:
            f.write(file_data)
        print(f"✓ 合并文件已保存")


async def example_split_pdf():
    """示例：拆分PDF"""
    with open("large_document.pdf", "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode('utf-8')
    
    params = {
        "action": "拆分PDF",
        "action_type": "split_pdf",
        "file_data": pdf_data,
        "split_mode": "range",
        "page_ranges": ["1-5", "6-10", "11-15"]
    }
    
    result = await execute(params)
    
    if result["success"]:
        print(f"✓ {result['message']}")
        
        for i, file_data_str in enumerate(result['data']['files'], 1):
            file_data = base64.b64decode(file_data_str)
            with open(f"part_{i}.pdf", "wb") as f:
                f.write(file_data)
        print(f"✓ 已拆分为 {len(result['data']['files'])} 个文件")


async def example_add_watermark():
    """示例：添加水印"""
    with open("document.pdf", "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode('utf-8')
    
    params = {
        "action": "添加水印",
        "action_type": "add_watermark",
        "file_data": pdf_data,
        "watermark_text": "机密文件",
        "opacity": 0.3
    }
    
    result = await execute(params)
    
    if result["success"]:
        file_data = base64.b64decode(result["file_data"])
        with open("watermarked.pdf", "wb") as f:
            f.write(file_data)
        print(f"✓ 水印添加成功")


async def main():
    """运行所有示例"""
    print("=" * 60)
    print("示例1: PDF转Word")
    print("=" * 60)
    await example_convert_pdf_to_word()
    
    print("\n" + "=" * 60)
    print("示例2: PDF转Excel")
    print("=" * 60)
    await example_convert_pdf_to_excel()
    
    print("\n" + "=" * 60)
    print("示例3: 提取PDF文本")
    print("=" * 60)
    await example_extract_text()
    
    print("\n" + "=" * 60)
    print("示例4: 提取PDF摘要")
    print("=" * 60)
    await example_extract_summary()
    
    print("\n" + "=" * 60)
    print("示例5: 提取关键要点")
    print("=" * 60)
    await example_extract_key_points()
    
    print("\n" + "=" * 60)
    print("示例6: 合并PDF")
    print("=" * 60)
    await example_merge_pdfs()
    
    print("\n" + "=" * 60)
    print("示例7: 拆分PDF")
    print("=" * 60)
    await example_split_pdf()
    
    print("\n" + "=" * 60)
    print("示例8: 添加水印")
    print("=" * 60)
    await example_add_watermark()


if __name__ == "__main__":
    asyncio.run(main())
