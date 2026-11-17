from .md_converter import MdToWechatConverter
from .html_converter import HtmlToWechatConverter

def get_converter(file_path: str):
    from pathlib import Path
    suffix = Path(file_path).suffix.lower()
    if suffix in ('.md', '.markdown'):
        return MdToWechatConverter()
    elif suffix in ('.html', '.htm'):
        return HtmlToWechatConverter()
    raise ValueError(f"不支持的文件格式: {suffix}")
