import re
from pathlib import Path
from typing import Dict


class HtmlToWechatConverter:
    ALLOWED_TAGS = [
        'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'strong', 'b', 'em', 'i', 'u', 's', 'del',
        'a', 'br', 'hr', 'blockquote',
        'ul', 'ol', 'li', 'table', 'tbody', 'thead', 'tr', 'td', 'th',
        'img', 'div', 'span', 'section',
        'pre', 'code'
    ]
    
    ALLOWED_ATTRIBUTES = {
        'a': ['href', 'target'],
        'img': ['src', 'alt', 'width', 'height'],
        '*': ['style']
    }
    
    ALLOWED_CSS_PROPERTIES = [
        'color', 'background-color', 'background',
        'font-size', 'font-weight', 'font-style', 'font-family',
        'text-align', 'line-height',
        'margin', 'margin-top', 'margin-bottom', 'margin-left', 'margin-right',
        'padding', 'padding-top', 'padding-bottom', 'padding-left', 'padding-right',
        'border', 'border-left', 'border-right', 'border-top', 'border-bottom',
        'border-color', 'border-width', 'border-style',
        'width', 'height',
        'list-style-type', 'list-style-position',
        'overflow', 'overflow-x', 'overflow-y',
        'text-decoration', 'text-indent',
        'display', 'white-space', 'word-break',
        'border-radius'
    ]
    
    def convert(self, html_path: str, user_digest: str = "") -> Dict:
        from wechat_oa.core.utils import extract_digest
        
        with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
        
        title = self._extract_title(html)
        
        try:
            from premailer import Premailer
            p = Premailer(
                html,
                remove_classes=False,
                strip_important=False,
                include_star_selectors=False,
                disable_link_rewrites=True
            )
            html = p.transform()
        except ImportError:
            pass
        
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            body_tag = soup.body
            if body_tag:
                for tag in body_tag.find_all(True):
                    self._sanitize_tag(tag)
                
                for tag in body_tag.find_all(['ul', 'ol', 'li']):
                    if 'style' in tag.attrs:
                        style = tag['style']
                        style_parts = style.split(';')
                        cleaned_parts = []
                        for part in style_parts:
                            part = part.strip()
                            if part and not part.startswith('margin'):
                                cleaned_parts.append(part)
                        if cleaned_parts:
                            tag['style'] = '; '.join(cleaned_parts)
                        else:
                            del tag['style']
                
                for ul_or_ol in body_tag.find_all(['ul', 'ol']):
                    for child in ul_or_ol.contents:
                        if isinstance(child, str) and child.strip() == '':
                            child.extract()
                
                html_parts = []
                for child in body_tag.contents:
                    if isinstance(child, str):
                        stripped = child.strip()
                        if stripped:
                            html_parts.append(stripped)
                    else:
                        html_parts.append(str(child))
                html = ''.join(html_parts)
            else:
                html = self._clean_html_with_bs4(soup)
        except ImportError:
            try:
                import bleach
                html = bleach.clean(
                    html,
                    tags=self.ALLOWED_TAGS,
                    attributes=self.ALLOWED_ATTRIBUTES,
                    strip=True
                )
            except ImportError:
                pass
        
        html = self._clean_list_empty_lines(html)
        
        body = self._extract_body(html)
        
        if not title or title == "无标题":
            title = self._extract_title(html)
        
        return {
            "title": title,
            "body": body,
            "digest": user_digest if user_digest else extract_digest(body),
            "author": ""
        }
    
    def _sanitize_tag(self, tag):
        allowed_tags_lower = {tag.lower() for tag in self.ALLOWED_TAGS}
        
        if tag.name.lower() not in allowed_tags_lower:
            tag.unwrap()
            return
        
        attrs_to_remove = []
        for attr in tag.attrs:
            if attr == 'style':
                style = tag['style']
                cleaned_style = self._sanitize_style(style)
                if cleaned_style:
                    tag['style'] = cleaned_style
                else:
                    attrs_to_remove.append('style')
            elif attr == 'href':
                href = tag['href']
                if not href.startswith(('http://', 'https://', 'mailto:')):
                    attrs_to_remove.append('href')
            elif attr == 'target' and tag['target'] != '_blank':
                attrs_to_remove.append('target')
            elif attr not in self.ALLOWED_ATTRIBUTES.get(tag.name.lower(), []) and attr not in self.ALLOWED_ATTRIBUTES.get('*', []):
                attrs_to_remove.append(attr)
        
        for attr in attrs_to_remove:
            del tag[attr]
    
    def _clean_html_with_bs4(self, soup) -> str:
        allowed_tags_lower = {tag.lower() for tag in self.ALLOWED_TAGS}
        
        for tag in soup.find_all(True):
            self._sanitize_tag(tag)
        
        return str(soup)
    
    def _sanitize_style(self, style: str) -> str:
        properties = style.split(';')
        cleaned = []
        for prop in properties:
            prop = prop.strip()
            if not prop:
                continue
            if ':' in prop:
                key, value = prop.split(':', 1)
                key = key.strip().lower()
                if key in self.ALLOWED_CSS_PROPERTIES:
                    cleaned.append(f"{key}: {value.strip()}")
        return '; '.join(cleaned)
    
    def _clean_list_empty_lines(self, html: str) -> str:
        html = re.sub(r'<li>\s*<br\s*/?>\s*</li>', '</li>', html)
        html = re.sub(r'<li>\s*</li>', '', html)
        html = re.sub(r'</li>\s*<br\s*/?>\s*<li>', '</li><li>', html)
        html = re.sub(r'<ul>\s*<br\s*/?>', '<ul>', html)
        html = re.sub(r'<ol>\s*<br\s*/?>', '<ol>', html)
        html = re.sub(r'</ul>\s*<br\s*/?>', '</ul>', html)
        html = re.sub(r'</ol>\s*<br\s*/?>', '</ol>', html)
        
        html = re.sub(r'</li>\s+<li>', '</li><li>', html)
        html = re.sub(r'<ul>\s+', '<ul>', html)
        html = re.sub(r'\s+</ul>', '</ul>', html)
        html = re.sub(r'<ol>\s+', '<ol>', html)
        html = re.sub(r'\s+</ol>', '</ol>', html)
        
        return html
    
    def _extract_title(self, html: str) -> str:
        m = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
        if m:
            return m.group(1).strip()[:64]
        
        m = re.search(r'<h1[^>]*>([^<]+)</h1>', html, re.IGNORECASE)
        if m:
            return m.group(1).strip()[:64]
        
        return "无标题"
    
    def _extract_body(self, html: str) -> str:
        m = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(1).strip()
        
        return html.strip()
