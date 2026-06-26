"""
Word VBA Skill - Word文档处理工具包

基于Microsoft Word VBA/ActiveX的Python接口，提供完整的Word文档读写功能。

主要模块:
    - word_vba_reader: 文档读取，提取文本和格式
    - word_vba_writer: 文档写入，创建和格式化
    - word_vba_utils: 高级功能（合并、模板、批量处理）

使用示例:
    >>> from word_vba import WordReader, WordWriter
    >>> 
    >>> # 读取文档
    >>> reader = WordReader()
    >>> content = reader.read_document("document.docx")
    >>> 
    >>> # 创建文档
    >>> writer = WordWriter()
    >>> doc = writer.create_document()
    >>> writer.add_paragraph(doc, "Hello World", {'font_name': '宋体'})
    >>> writer.save_document(doc, "output.docx")

要求:
    - Windows操作系统
    - Microsoft Word 2010或更高版本
    - pywin32库

作者: SuperMike
版本: 2.0
日期: 2026-03-04
"""

__version__ = "2.0"
__author__ = "SuperMike"
__date__ = "2026-03-04"

# 导入主要类
from .word_vba_reader import WordReader
from .word_vba_writer import WordWriter
from .word_vba_utils import WordVBAUtils

# 定义公开接口
__all__ = [
    'WordReader',
    'WordWriter',
    'WordVBAUtils',
]
