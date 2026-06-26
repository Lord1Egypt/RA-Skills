"""协作笔记解析器"""
import json
import re

from note_parser import NoteParser
from note_fixer import NoteFixer
from wiz_logging import get_logger

logger = get_logger()


class BlockTextConverter:
    """协作笔记文本块转换器"""

    @staticmethod
    def to_text(text_dict: dict) -> str:
        """将文本对象转换为 Markdown 文本"""
        if not text_dict:
            return ""

        attributes = text_dict.get("attributes", {})

        # wiki-link
        if attributes.get("type") == "wiki-link":
            return BlockTextConverter.handle_wiki_link(text_dict)

        # math 公式
        if attributes.get("type") == "math":
            tex = attributes.get("tex", "").strip()
            return f'${tex}$'

        # link
        if attributes.get("link"):
            return BlockTextConverter.handle_link(text_dict)

        # style-code
        if attributes.get("style-code"):
            return BlockTextConverter.handle_code(text_dict)

        # style-bold
        if attributes.get("style-bold"):
            return BlockTextConverter.handle_bold(text_dict)

        # style-italic
        if attributes.get("style-italic"):
            return BlockTextConverter.handle_italic(text_dict)

        # style-strikethrough
        if attributes.get("style-strikethrough"):
            return BlockTextConverter.handle_strikethrough(text_dict)

        # 普通文本
        return text_dict.get("insert", "")

    @classmethod
    def handle_link(cls, text_dict: dict) -> str:
        """处理链接"""
        return f'[{text_dict["insert"]}]({text_dict["attributes"]["link"]})'

    @classmethod
    def handle_code(cls, text_dict: dict) -> str:
        """处理行内代码"""
        return f'`{text_dict["insert"]}`'

    @classmethod
    def handle_italic(cls, text_dict: dict) -> str:
        """处理斜体"""
        return f'*{text_dict["insert"]}*'

    @classmethod
    def handle_bold(cls, text_dict: dict) -> str:
        """处理粗体"""
        return f'**{text_dict["insert"]}**'

    @classmethod
    def handle_strikethrough(cls, text_dict: dict) -> str:
        """处理删除线"""
        return f'~~{text_dict["insert"]}~~'

    @classmethod
    def handle_wiki_link(cls, text_dict: dict) -> str:
        """处理 wiki 链接"""
        attributes = text_dict["attributes"]
        name = attributes.get("name", "")
        secondary_name = attributes.get("secondaryName", "")

        if name.endswith('.md'):
            name = name[:-3]

        if secondary_name:
            return f'[[{secondary_name}|{name}]]'
        else:
            return f'[[{name}]]'


class TextStrategy:
    """文本块策略"""

    def __init__(self, data: dict):
        self.data = data

    def to_text(self, block_row: dict) -> str:
        """转换文本块为 Markdown"""
        block_type = block_row.get("type", "")
        
        if block_type == "code":
            return self.handle_code(block_row)
        elif block_type == "math":
            return self.handle_math(block_row)
        elif block_row.get("quoted"):
            return self.handle_quote(block_row['text'])
        elif block_row.get("heading"):
            return self.handle_header(block_row, block_row['text'])
        else:
            return self.handle_text(block_row['text'])

    def handle_code(self, block_row: dict) -> str:
        """处理代码块"""
        code = block_row.get("code", "")
        language = block_row.get("language", "")
        if language and language.lower() != "plain text":
            return f"```{language}\n{code}\n```\n"
        else:
            return f"```\n{code}\n```\n"

    def handle_math(self, block_row: dict) -> str:
        """处理数学公式块"""
        math = block_row.get("math", "")
        display_mode = block_row.get("displayMode", False)
        if display_mode:
            return f"$$\n{math}\n$$\n"
        else:
            return f"${math}$\n"

    def handle_text(self, text_arr: list) -> str:
        """处理文本数组"""
        if not text_arr:
            return ''
        return ''.join(BlockTextConverter.to_text(t) for t in text_arr)

    def handle_header(self, block_row: dict, text_arr: list) -> str:
        """处理标题"""
        level = block_row.get("heading", 1)
        text = ' '.join(BlockTextConverter.to_text(t) for t in text_arr)
        return f'{"#" * level} {text}\n'

    def handle_quote(self, json_data: list) -> str:
        """处理引用"""
        text = ''.join(BlockTextConverter.to_text(t) for t in json_data)
        return f"> {text}\n"


class ListStrategy:
    """列表块策略"""

    def __init__(self, data: dict):
        self.data = data

    def to_text(self, block_row: dict) -> str:
        """转换列表块为 Markdown"""
        if block_row.get("ordered"):
            return self.handle_ordered_list(block_row)
        else:
            return self.handle_unordered_list(block_row)

    def handle_unordered_list(self, block_row: dict) -> str:
        """处理无序列表"""
        indent = (block_row['level'] - 1) * 2 * ' '
        text = f'{indent}- '

        # checkbox 支持
        checkbox = block_row.get("checkbox")
        if checkbox == "checked":
            text += "[x] "
        elif checkbox == "unchecked":
            text += "[ ] "

        text += ''.join(BlockTextConverter.to_text(t) for t in block_row["text"])
        return text + '\n'

    def handle_ordered_list(self, block_row: dict) -> str:
        """处理有序列表"""
        indent = (block_row['level'] - 1) * 2 * ' '
        start = block_row.get("start", 1)
        text = f'{indent}{start}. '
        text += ''.join(BlockTextConverter.to_text(t) for t in block_row["text"])
        return text + '\n'


class EmbedStrategy:
    """嵌入块策略"""

    def __init__(self, data: dict):
        self.data = data

    def to_text(self, block_row: dict) -> str:
        """转换嵌入块为 Markdown"""
        embed_type = block_row.get("embedType", "")
        embed_data = block_row.get("embedData", {})

        if embed_type == "image":
            return self.handle_image(embed_data)
        elif embed_type == "toc":
            return "\n[TOC]\n\n"
        elif embed_type == "hr":
            return "\n---\n\n"
        elif embed_type == "office":
            return self.handle_office(embed_data)
        elif embed_type == "drawio":
            return self.handle_drawio(embed_data)
        elif embed_type == "mermaid":
            return self.handle_mermaid(embed_data)
        elif embed_type == "math":
            return self.handle_math(embed_data)
        elif embed_type == "webpage":
            return self.handle_webpage(embed_data)
        else:
            logger.warning(f"不支持的 embed 类型: {embed_type}")
            return ""

    def handle_image(self, embed_data: dict) -> str:
        """处理图片"""
        src = embed_data.get("src", "")
        file_name = embed_data.get("fileName", "")
        return f"![{file_name}]({src})\n\n"

    def handle_office(self, embed_data: dict) -> str:
        """处理 Office 附件"""
        file_name = embed_data.get('fileName', '')
        src = embed_data.get('src', '')
        return f'\n[{file_name}](wiz-collab-attachment://{src})\n\n'

    def handle_drawio(self, embed_data: dict) -> str:
        """处理流程图"""
        src = embed_data.get("src", "")
        file_name = "流程图"
        return f'\n[{file_name}](wiz-collab-attachment://{src})\n\n'

    def handle_mermaid(self, embed_data: dict) -> str:
        """处理 Mermaid 流程图"""
        mermaid_text = embed_data.get("mermaidText", "")
        if mermaid_text:
            return f'\n```mermaid\n{mermaid_text}\n```\n\n'
        else:
            src = embed_data.get("src", "")
            if src:
                file_name = "Mermaid流程图"
                return f'\n[{file_name}](wiz-collab-attachment://{src})\n\n'
            return ""

    def handle_math(self, embed_data: dict) -> str:
        """处理数学公式"""
        math_text = embed_data.get("mathjaxText", "")
        align = embed_data.get("align", "center")
        if math_text:
            if align == "center":
                return f"\n$$\n{math_text}\n$$\n"
            else:
                return f"${math_text}$\n"
        return ""

    def handle_webpage(self, embed_data: dict) -> str:
        """处理网页嵌入"""
        src = embed_data.get("src", "")
        return f"\n[webpage]({src})\n\n"


class TableStrategy:
    """表格块策略"""

    def __init__(self, data: dict):
        self.data = data

    def to_text(self, block_row: dict) -> str:
        """转换表格块为 Markdown"""
        cols = block_row.get("cols", 0)
        children = block_row.get("children", [])

        if not children or cols == 0:
            return ""

        # 从 data 中获取 cell 内容
        children_text = []
        for child_id in children:
            if child_id in self.data:
                cell_text = self.data[child_id][0].get("text", [])
                text_content = ''.join(BlockTextConverter.to_text(t) for t in cell_text)
                children_text.append(text_content)
            else:
                children_text.append('')

        # 分离表头和表体
        headers = children_text[:cols]
        body = children_text[cols:]

        # 构建 Markdown 表格
        md_table = "| " + " | ".join(headers) + " |\n"
        md_table += "| " + " | ".join(["-----"] * cols) + " |\n"

        # 分割表体行
        body_rows = [body[i:i + cols] for i in range(0, len(body), cols)]
        for row in body_rows:
            md_table += "| " + " | ".join(row) + " |\n"

        return '\n' + md_table + '\n'


class MarkdownConverter:
    """Markdown 转换器"""

    STRATEGY_MAP = {
        "text": TextStrategy,
        "list": ListStrategy,
        "embed": EmbedStrategy,
        "table": TableStrategy,
        "code": TextStrategy,
        "math": TextStrategy
    }

    @staticmethod
    def to_text(data: dict, block: dict) -> str:
        """将协作笔记块转换为 Markdown"""
        block_type = block.get("type")
        strategy_class = MarkdownConverter.STRATEGY_MAP.get(block_type)

        if not strategy_class:
            logger.warning(f"不支持的块类型: {block_type}")
            return ""

        strategy = strategy_class(data)
        return strategy.to_text(block)


class CollaborationNoteParser(NoteParser):
    """协作笔记解析器"""

    def parse_content(self, origin_content: str) -> str:
        """解析协作笔记 JSON 内容为 Markdown"""
        markdown_content = self._parse(origin_content)
        file_content = NoteFixer.fix(markdown_content)
        return file_content

    def _parse(self, origin_content: str) -> str:
        """解析 JSON 内容"""
        json_content = json.loads(origin_content)
        blocks = json_content.get('data', {}).get('data', {}).get("blocks", [])

        # 构建数据映射（用于表格等引用）
        data_map = json_content.get('data', {}).get('data', {})

        text_parts = []
        for block in blocks:
            block_text = MarkdownConverter.to_text(data_map, block)
            text_parts.append(block_text)

        return ''.join(text_parts)
