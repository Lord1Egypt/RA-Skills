"""Note 类 - 笔记数据模型"""


class Note:
    """笔记数据模型"""

    @staticmethod
    def is_collaboration_note(note_type: str) -> bool:
        """判断是否是协作笔记"""
        return note_type == 'collaboration'
