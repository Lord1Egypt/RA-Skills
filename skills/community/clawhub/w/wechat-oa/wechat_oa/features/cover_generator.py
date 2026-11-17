from PIL import Image, ImageDraw, ImageFont
import os
import sys
from pathlib import Path


def generate_cover(title: str, save_path: str = "", font_path: str = "") -> str:
    width, height = 900, 400
    
    img = Image.new('RGB', (width, height), color=(0, 102, 204))
    
    draw = ImageDraw.Draw(img)
    
    if font_path:
        font_file = font_path
    else:
        platform_fonts = {
            "darwin": [
                "/Library/Fonts/msyh.ttf",
                "/Library/Fonts/SimHei.ttf",
                "/Library/Fonts/Simsun.ttc",
                "/Library/Fonts/Arial Unicode.ttf",
                "/System/Library/Fonts/HelveticaNeue.ttc",
            ],
            "win32": [
                "C:/Windows/Fonts/msyh.ttc",
                "C:/Windows/Fonts/simhei.ttf",
                "C:/Windows/Fonts/simsun.ttc",
                "C:/Windows/Fonts/msyhbd.ttc",
            ],
            "linux": [
                "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            ],
        }
        
        current_platform = sys.platform
        font_paths = platform_fonts.get(current_platform, [])
        
        font_paths += [
            "/Library/Fonts/msyh.ttf",
            "/Library/Fonts/SimHei.ttf",
            "/Library/Fonts/Simsun.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
        
        font_file = None
        for fp in font_paths:
            if os.path.exists(fp):
                font_file = fp
                break
    
    if font_file:
        title_font = ImageFont.truetype(font_file, 48)
        subtitle_font = ImageFont.truetype(font_file, 24)
    else:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    title_text = title[:12] + "..." if len(title) > 12 else title
    
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    title_x = (width - title_width) // 2
    title_y = (height - title_height) // 2
    
    draw.text((title_x - 2, title_y - 2), title_text, font=title_font, fill=(0, 0, 0))
    draw.text((title_x + 2, title_y - 2), title_text, font=title_font, fill=(0, 0, 0))
    draw.text((title_x - 2, title_y + 2), title_text, font=title_font, fill=(0, 0, 0))
    draw.text((title_x + 2, title_y + 2), title_text, font=title_font, fill=(0, 0, 0))
    draw.text((title_x, title_y), title_text, font=title_font, fill=(255, 255, 255))
    
    subtitle_text = "WeChat Official Account"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + title_height + 20
    
    draw.text((subtitle_x, subtitle_y), subtitle_text, font=subtitle_font, fill=(200, 220, 255))
    
    for i in range(10):
        circle_x = int(width * (0.1 + i * 0.08))
        circle_y = int(height * (0.2 + (i % 3) * 0.3))
        radius = 30 + i * 5
        alpha = 50 + i * 10
        
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.ellipse((circle_x - radius, circle_y - radius, circle_x + radius, circle_y + radius), fill=(255, 255, 255, alpha))
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    if save_path:
        output_path = save_path
    else:
        cache_dir = Path(__file__).parent.parent.parent / ".cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        output_path = cache_dir / "cover.png"
    
    img.save(output_path)
    
    return str(output_path)
