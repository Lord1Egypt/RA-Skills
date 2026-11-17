import re
from pathlib import Path
from typing import Dict


class MdToWechatConverter:
    def __init__(self, theme: str = "blue"):
        self.theme = theme
    
    def convert(self, md_path: str, user_digest: str = "") -> Dict:
        from wechat_oa.core.utils import extract_digest
        
        with open(md_path, 'r', encoding='utf-8', errors='ignore') as f:
            md_content = f.read()
        
        try:
            from md2wxhtml import WeChatConverter
            converter = WeChatConverter(content_theme=self.theme, code_theme="monokai")
            result = converter.convert(md_content)
            body_html = result.html
        except ImportError:
            from mistune import create_markdown
            try:
                body_html = create_markdown()(md_content)
            except ImportError:
                raise ConvertError("md2wxhtml 和 mistune 均未安装")
        
        title = self._extract_title(md_content)
        
        return {
            "title": title,
            "body": body_html,
            "digest": user_digest if user_digest else extract_digest(body_html),
            "author": ""
        }
    
    def _extract_title(self, md_content: str) -> str:
        for m in re.finditer(r'^(#{1,3})\s+(.+)$', md_content, re.MULTILINE):
            raw = m.group(2).strip()
            raw = re.sub(r'\*\*(.+?)\*\*', r'\1', raw)
            raw = re.sub(r'\*(.+?)\*', r'\1', raw)
            raw = re.sub(r'`(.+?)`', r'\1', raw)
            if raw:
                return raw[:64]
        return "无标题"


class ConvertError(Exception):
    pass
