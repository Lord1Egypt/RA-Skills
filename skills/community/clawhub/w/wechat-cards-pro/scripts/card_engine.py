#!/usr/bin/env python3
"""
微信公众号贴图卡片生成引擎

核心设计原则：
1. 追踪全局y坐标，防止重叠
2. 所有容器自适应高度
3. 统一间距和字体规范
4. 自动字体回退
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageChops


class Theme:
    """预设主题"""
    DARK_GOLD = {
        'bg': '#0a0a0a',
        'card_bg': '#1a1a1a',
        'text': '#e8e8e8',
        'text_dim': '#888888',
        'gold': '#c9a96e',
        'gold_dim': '#c9a96e88',
        'green': '#6b9e75',
        'red': '#c96b6b',
    }


class CardEngine:
    """卡片生成引擎"""
    
    def __init__(self, width=1080, height=1440, theme=None):
        self.W = width
        self.H = height
        self.theme = theme or Theme.DARK_GOLD
        self.colors = {k: self._hex(v) for k, v in self.theme.items()}
        self.margin_x = 60
        self.margin_top = 80
        self.margin_bottom = 60
        self.content_w = self.W - self.margin_x * 2
        self.y = self.margin_top
        self.img = None
        self.draw = None
        self._font_cache = {}
        self._setup_canvas()
    
    def _hex(self, h):
        h = h.lstrip('#')
        if len(h) == 6:
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        elif len(h) == 8:  # with alpha
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4, 6))
        return (255, 255, 255)
    
    def _get_font(self, size):
        key = size
        if key not in self._font_cache:
            fonts = [
                "/System/Library/Fonts/PingFang.ttc",
                "/System/Library/Fonts/STHeiti Light.ttc",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            ]
            for f in fonts:
                if os.path.exists(f):
                    try:
                        self._font_cache[key] = ImageFont.truetype(f, size)
                        break
                    except:
                        continue
            else:
                self._font_cache[key] = ImageFont.load_default()
        return self._font_cache[key]
    
    def _setup_canvas(self):
        self.img = Image.new('RGB', (self.W, self.H), self.colors['bg'])
        self.draw = ImageDraw.Draw(self.img)
    
    def _text_size(self, text, size):
        """获取文字尺寸"""
        font = self._get_font(size)
        bbox = self.draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    def _multiline_height(self, text, size, spacing=8, line_height=None):
        """计算多行文字总高度"""
        lines = text.count('\n') + 1
        if line_height is None:
            _, h = self._text_size("中", size)
            line_height = h
        return lines * line_height + (lines - 1) * spacing
    
    def _check_overflow(self, needed_height):
        """检查是否超出画布"""
        return self.y + needed_height > self.H - self.margin_bottom
    
    def reset(self):
        """重置画布和y坐标"""
        self.y = self.margin_top
        self._setup_canvas()
    
    def new_card(self):
        """开始新卡片"""
        self.reset()
        return self
    
    # ============ 组件方法 ============
    
    def top_bar(self, color='gold', height=2):
        """顶部装饰线"""
        self.draw.rectangle(
            [self.margin_x, self.y, self.W - self.margin_x, self.y + height],
            fill=self.colors[color]
        )
        self.y += height + 25
        return height + 25
    
    def title(self, text, size=48, color='text', bold=False, align='left'):
        """大标题"""
        font = self._get_font(size)
        c = self.colors[color]
        if align == 'center':
            w, h = self._text_size(text, size)
            x = (self.W - w) // 2
        else:
            x = self.margin_x
        self.draw.text((x, self.y), text, fill=c, font=font)
        self.y += size + 15
        return size + 15
    
    def subtitle(self, text, size=28, color='text_dim'):
        """副标题"""
        font = self._get_font(size)
        self.draw.text((self.margin_x, self.y), text, fill=self.colors[color], font=font)
        self.y += size + 10
        return size + 10
    
    def paragraph(self, text, size=22, color='text', spacing=6, line_height=None):
        """正文段落（支持多行）"""
        font = self._get_font(size)
        if line_height is None:
            _, line_height = self._text_size("中", size)
        
        lines = text.count('\n') + 1
        total_h = lines * line_height + (lines - 1) * spacing
        
        self.draw.multiline_text(
            (self.margin_x, self.y), text,
            fill=self.colors[color], font=font, spacing=spacing
        )
        self.y += total_h + 20
        return total_h + 20
    
    def quote_box(self, text, size=24, color='text', 
                  border_color='gold', bg_color='card_bg',
                  padding=18, radius=10, spacing=6):
        """引用/高亮框（自适应高度）"""
        font = self._get_font(size)
        _, line_h = self._text_size("中", size)
        lines = text.count('\n') + 1
        content_h = lines * line_h + (lines - 1) * spacing
        box_h = padding * 2 + content_h
        
        # 绘制框
        box_y = self.y
        if bg_color:
            self.draw.rounded_rectangle(
                [self.margin_x, box_y, self.W - self.margin_x, box_y + box_h],
                radius=radius, fill=self.colors[bg_color]
            )
        if border_color:
            self.draw.rounded_rectangle(
                [self.margin_x, box_y, self.W - self.margin_x, box_y + box_h],
                radius=radius, outline=self.colors[border_color], width=2
            )
        
        # 绘制文字
        self.draw.multiline_text(
            (self.margin_x + padding, box_y + padding),
            text, fill=self.colors[color], font=font, spacing=spacing
        )
        
        self.y += box_h + 25
        return box_h + 25
    
    def list_item(self, number, title, desc=None, 
                  title_size=26, desc_size=22,
                  title_color='gold', desc_color='text_dim',
                  spacing=8, item_spacing=20):
        """列表项（带序号）"""
        # 序号
        num_font = self._get_font(title_size)
        self.draw.text((self.margin_x, self.y), f"{number:02d}", 
                      fill=self.colors[title_color], font=num_font)
        
        # 标题
        title_w, title_h = self._text_size(f"{number:02d}", title_size)
        self.draw.text((self.margin_x + title_w + 12, self.y), title,
                      fill=self.colors['text'], font=num_font)
        self.y += title_h + 8
        
        # 描述（可选）
        if desc:
            desc_font = self._get_font(desc_size)
            lines = desc.count('\n') + 1
            _, line_h = self._text_size("中", desc_size)
            desc_h = lines * line_h + (lines - 1) * spacing
            
            self.draw.multiline_text(
                (self.margin_x + title_w + 12, self.y),
                desc, fill=self.colors[desc_color], font=desc_font, spacing=spacing
            )
            self.y += desc_h + item_spacing
            return title_h + 8 + desc_h + item_spacing
        
        self.y += item_spacing
        return title_h + item_spacing
    
    def bullet_list(self, items, prefix="•", size=22, 
                    color='text', spacing=30, indent=20):
        """项目符号列表"""
        font = self._get_font(size)
        _, line_h = self._text_size("中", size)
        total_h = 0
        
        for item in items:
            text = f"{prefix} {item}"
            self.draw.text((self.margin_x + indent, self.y), text,
                          fill=self.colors[color], font=font)
            self.y += line_h + spacing
            total_h += line_h + spacing
        
        return total_h
    
    def separator(self, color='gold', height=1, margin=20):
        """分隔线"""
        self.y += margin
        self.draw.rectangle(
            [self.margin_x, self.y, self.W - self.margin_x, self.y + height],
            fill=self.colors[color]
        )
        self.y += height + margin
        return height + margin * 2
    
    def spacer(self, height=20):
        """空白间距"""
        self.y += height
        return height
    
    def center_content_vertically(self):
        """将已绘制的内容垂直居中"""
        bg = Image.new('RGB', (self.W, self.H), self.colors['bg'])
        diff = ImageChops.difference(self.img, bg)
        bbox = diff.getbbox()
        
        if bbox is None:
            return  # 空内容，无需居中
        
        content_top = bbox[1]
        content_bottom = bbox[3]
        content_height = content_bottom - content_top + 1
        
        if content_height >= self.H:
            return  # 内容超出卡片高度，不居中
        
        target_top = (self.H - content_height) // 2
        
        if target_top != content_top:
            new_img = Image.new('RGB', (self.W, self.H), self.colors['bg'])
            region = self.img.crop((0, content_top, self.W, content_bottom + 1))
            new_img.paste(region, (0, target_top))
            self.img = new_img
            self.draw = ImageDraw.Draw(self.img)
    
    def footer(self, left_text, right_text=None, 
               left_color='gold_dim', right_color='text_dim', size=20):
        """底部标识"""
        y = self.H - 60
        font = self._get_font(size)
        self.draw.text((self.margin_x, y), left_text,
                      fill=self.colors[left_color], font=font)
        if right_text:
            w, _ = self._text_size(right_text, size)
            self.draw.text((self.W - self.margin_x - w, y), right_text,
                          fill=self.colors[right_color], font=font)
        return 40
    
    def save(self, path, quality=95):
        """保存卡片"""
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        self.img.save(path, 'PNG', quality=quality)
        print(f"✓ {path}")
        return path
    
    def to_jpeg(self, path, quality=95):
        """转换为JPEG（微信素材库要求）"""
        if self.img.mode in ('RGBA', 'P'):
            rgb = self.img.convert('RGB')
        else:
            rgb = self.img
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        rgb.save(path, 'JPEG', quality=quality)
        print(f"✓ {path}")
        return path


# ============ 快捷模板 ============

def create_cover(title, subtitle, out_path, **kwargs):
    """快速创建封面卡片"""
    engine = CardEngine()
    engine.top_bar()
    engine.title(title, size=kwargs.get('title_size', 56), color='gold')
    engine.spacer(15)
    engine.subtitle(subtitle, size=kwargs.get('subtitle_size', 28))
    engine.footer(kwargs.get('footer_left', 'AI Albert'), 
                  kwargs.get('footer_right', ''))
    return engine.save(out_path)


def create_content_card(title, paragraphs, out_path, **kwargs):
    """快速创建内容卡片"""
    engine = CardEngine()
    engine.top_bar()
    engine.title(title, size=kwargs.get('title_size', 44))
    engine.spacer(10)
    
    for p in paragraphs:
        if isinstance(p, dict):
            # 结构化段落
            if p.get('type') == 'quote':
                engine.quote_box(p['text'], size=p.get('size', 24))
            elif p.get('type') == 'list':
                engine.bullet_list(p['items'], size=p.get('size', 22))
            elif p.get('type') == 'separator':
                engine.separator()
            else:
                engine.paragraph(p['text'], size=p.get('size', 22))
        else:
            engine.paragraph(str(p), size=22)
    
    engine.footer(kwargs.get('footer_left', ''), kwargs.get('footer_right', ''))
    return engine.save(out_path)


if __name__ == '__main__':
    # 示例用法
    out_dir = "/tmp/card_demo"
    os.makedirs(out_dir, exist_ok=True)
    
    # 封面示例
    create_cover(
        "示例标题",
        "副标题说明文字",
        f"{out_dir}/cover.png",
        footer_left="公众号名称"
    )
    
    # 内容卡片示例
    create_content_card(
        "内容标题",
        [
            "这是第一段正文内容，可以很长很长。",
            {"type": "quote", "text": "这是一个引用框\n支持多行文字\n自适应高度"},
            "这是第二段正文。",
            {"type": "list", "items": ["要点一", "要点二", "要点三"]},
        ],
        f"{out_dir}/content.png",
        footer_left="公众号名称"
    )
    
    print(f"\n示例卡片已保存到: {out_dir}")
