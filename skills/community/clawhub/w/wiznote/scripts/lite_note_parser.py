"""Lite/Markdown 笔记解析器"""
from bs4 import BeautifulSoup

from note_parser import NoteParser
from note_fixer import NoteFixer


class LiteNoteParser(NoteParser):
    """Lite/Markdown 笔记解析器"""

    def parse_content(self, origin_content: str) -> str:
        """解析 Lite 内容为 Markdown"""
        markdown_content = self._parse(origin_content)
        file_content = NoteFixer.fix(markdown_content)
        return file_content

    @staticmethod
    def _parse(origin_content: str) -> str:
        """解析 Lite 格式内容"""
        soup = BeautifulSoup(origin_content, 'html.parser')
        body_tag = soup.find('body')
        if not body_tag:
            return origin_content
        pre_tag = body_tag.find('pre')
        if pre_tag:
            return pre_tag.get_text()
        return origin_content
