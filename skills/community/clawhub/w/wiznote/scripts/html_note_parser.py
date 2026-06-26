"""HTML 笔记解析器"""
import html2text

from note_parser import NoteParser
from note_fixer import NoteFixer


class HtmlNoteParser(NoteParser):
    """HTML 笔记解析器"""

    def parse_content(self, origin_content: str) -> str:
        """解析 HTML 内容为 Markdown"""
        markdown_content = html2text.html2text(origin_content)
        file_content = NoteFixer.fix(markdown_content)
        return file_content
