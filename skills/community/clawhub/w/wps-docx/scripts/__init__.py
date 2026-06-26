"""
DOCX Skill - Word 文档编辑与 HTML 转换工具集

子模块说明：
  edit_docx  - edit_docx：对 .docx 文件执行结构化编辑操作
  html2docx  - html2docx / html2docx_beautifulsoup：将 HTML 内容转换为 .docx 文件
  office     - pack_docx / unpack_docx / validate_docx：底层 Office XML 打包工具

使用方式：
    import sys
    sys.path.insert(0, "cooffice/skills/docx/scripts")
    from edit_docx import edit_docx
    from html2docx import html2docx
"""

from .edit_docx import edit_docx
from .html2docx import html2docx, html2docx_beautifulsoup
from .office import pack_docx, unpack_docx, validate_docx

__all__ = [
    # 编辑
    "edit_docx",
    # HTML 转换
    "html2docx",
    "html2docx_beautifulsoup",
    # Office XML 工具
    "pack_docx",
    "unpack_docx",
    "validate_docx",
]
