"""NoteFixer - Markdown 后处理"""
import re


HEADING_PATTERN = re.compile(r'^(#{1,6})(?!\s+)(\w+)')


def fix_markdown_title(content: str) -> str:
    """修复标题#后面可能没有空格的问题"""
    lines = content.split('\n')
    output_lines = []
    for line in lines:
        if HEADING_PATTERN.match(line):
            result = re.sub(HEADING_PATTERN, r'\1 \2', line)
            output_lines.append(result)
        else:
            output_lines.append(line)
    return '\n'.join(output_lines)


def fix_markdown_code_block(content: str) -> str:
    """修复代码块多余的空行"""
    line_num = 0
    code_block = False
    fix_content = []
    lines = content.split('\n')
    for line in lines:
        if line.startswith('```'):
            code_block = not code_block
            line_num = 0
        if code_block:
            line_num += 1
            if line_num % 2 == 0:
                if line.isspace() or len(line) == 0:
                    continue
        fix_content.append(line)
    return '\n'.join(fix_content)


def fix_markdown_list(content: str) -> str:
    """将文本中的所有 \\- 开头的文字替换为 -"""
    return content.replace('\\- ', '- ')


class NoteFixer:
    """Markdown 内容修复类"""

    @staticmethod
    def fix(markdown_content: str) -> str:
        """修复 Markdown 内容"""
        file_content = fix_markdown_title(markdown_content)
        file_content = fix_markdown_code_block(file_content)
        file_content = fix_markdown_list(file_content)
        # 多个换行合并
        file_content = file_content.replace('\n\n\n\n', '\n\n')
        file_content = file_content.replace('\n\n \n\n', '\n\n')
        return file_content
