"""笔记解析器基类"""
from abc import ABC, abstractmethod


class NoteParser(ABC):
    """笔记解析器抽象基类"""

    @abstractmethod
    def parse_content(self, origin_content: str) -> str:
        """
        解析笔记原始内容为 Markdown
        :param origin_content: 原始内容
        :return: Markdown 格式内容
        """
        pass
