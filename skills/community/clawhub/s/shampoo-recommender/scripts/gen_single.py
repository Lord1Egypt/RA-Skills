from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO

def create_image(product_name, color_hex, bg_hex):
    width, height = 1200, 628
    color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
    bg = tuple(int(bg_hex[i:i+2], 16) for i in (1, 3, 5))
    img = Image.new('RGB', (width, height), bg)
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc', 72)
        font_sub = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 36)
        font_small = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 24)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_small = ImageFont.load_default()
    draw.rectangle([0, 0, width, 15], fill=color)
    draw.rectangle([0, 0, 15, height], fill=color)
    draw.text((50, 50), '娜可露露', font=font_small, fill=(80, 80, 80))
    draw.line([(50, 85), (180, 85)], fill=color, width=3)
    draw.text((50, 130), product_name, font=font_title, fill=color)
    draw.text((50, 220), '洗发水', font=font_sub, fill=color)
    bx, by = 850, 120
    draw.rounded_rectangle([bx+35, by, bx+85, by+40], radius=5, fill=color)
    draw.rounded_rectangle([bx, by+40, bx+120, by+380], radius=25, fill=(255,255,255), outline=color, width=4)
    draw.rounded_rectangle([bx+15, by+140, bx+105, by+280], radius=10, fill=bg)
    draw.text((bx+30, by+190), '娜可', font=font_small, fill=color)
    draw.text((bx+30, by+220), '露露', font=font_small, fill=color)
    draw.line([(50, 480), (1150, 480)], fill=(200,200,200), width=2)
    draw.text((50, 500), '专业护发 · 娜可露露', font=font_small, fill=(150,150,150))
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()

# 生成深层滋养修护广告图的base64
name = '深层滋养修护'
b64 = create_image(name, '#8B5A2B', '#FFF8F0')
print(b64)
