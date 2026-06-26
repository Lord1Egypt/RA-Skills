from PIL import Image, ImageDraw, ImageFont
import os

# 创建输出目录 - 使用当前目录
output_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(output_dir, "images")
os.makedirs(images_dir, exist_ok=True)

# 产品信息
products = [
    {"name": "深层滋养修护", "subtitle": "角蛋白修护 · 深层补水", "color": (139, 90, 43), "bg_color": (255, 248, 240)},
    {"name": "清爽控油", "subtitle": "控油因子 · 持久蓬松", "color": (70, 130, 180), "bg_color": (240, 248, 255)},
    {"name": "去屑止痒", "subtitle": "吡硫翁锌 · 舒缓头皮", "color": (34, 139, 34), "bg_color": (240, 255, 240)},
    {"name": "防脱固发", "subtitle": "生姜萃取 · 强健发根", "color": (139, 69, 19), "bg_color": (255, 245, 238)},
    {"name": "氨基酸温和", "subtitle": "氨基酸表活 · 低刺激", "color": (147, 112, 219), "bg_color": (248, 248, 255)},
    {"name": "蓬松丰盈", "subtitle": "蓬松因子 · 轻盈配方", "color": (255, 140, 0), "bg_color": (255, 250, 240)},
    {"name": "去氯修护", "subtitle": "去氯因子 · 修护损伤", "color": (0, 128, 128), "bg_color": (240, 255, 255)},
]

# 广告图尺寸 (1200 x 628 - 社交媒体标准)
width, height = 1200, 628

def create_ad_image(product, index):
    # 创建背景
    img = Image.new('RGB', (width, height), product["bg_color"])
    draw = ImageDraw.Draw(img)
    
    # 尝试加载字体，如果没有则使用默认
    try:
        # Windows 系统字体
        font_title = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 72)
        font_subtitle = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 36)
        font_brand = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 28)
        font_small = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_brand = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 绘制装饰元素 - 顶部色块
    draw.rectangle([0, 0, width, 15], fill=product["color"])
    
    # 绘制左侧装饰线
    draw.rectangle([0, 0, 15, height], fill=product["color"])
    
    # 绘制品牌名
    draw.text((60, 50), "娜可露露", font=font_brand, fill=(80, 80, 80))
    draw.line([(60, 90), (200, 90)], fill=product["color"], width=3)
    
    # 绘制产品名称 - 主标题
    draw.text((60, 140), product["name"], font=font_title, fill=product["color"])
    
    # 绘制副标题
    draw.text((60, 240), product["subtitle"], font=font_subtitle, fill=(100, 100, 100))
    
    # 绘制右侧装饰 - 模拟洗发水瓶子轮廓
    bottle_x = 850
    bottle_y = 120
    # 瓶盖
    draw.rounded_rectangle([bottle_x + 35, bottle_y, bottle_x + 85, bottle_y + 35], 
                           radius=5, fill=product["color"], outline=(60, 60, 60), width=2)
    # 瓶身
    draw.rounded_rectangle([bottle_x, bottle_y + 35, bottle_x + 120, bottle_y + 350], 
                           radius=25, fill=(255, 255, 255), outline=product["color"], width=4)
    # 瓶身标签背景
    draw.rounded_rectangle([bottle_x + 15, bottle_y + 120, bottle_x + 105, bottle_y + 260], 
                           radius=10, fill=product["bg_color"])
    # 标签文字
    draw.text((bottle_x + 30, bottle_y + 170), "娜可", font=font_brand, fill=product["color"])
    draw.text((bottle_x + 30, bottle_y + 205), "露露", font=font_brand, fill=product["color"])
    
    # 绘制功效标签
    tags = ["专业护发", "温和配方"]
    tag_x = 60
    for tag in tags:
        # 标签背景
        draw.rounded_rectangle([tag_x, 320, tag_x + 120, 360], radius=20, fill=product["color"])
        # 标签文字
        draw.text((tag_x + 20, 328), tag, font=font_small, fill=(255, 255, 255))
        tag_x += 140
    
    # 绘制底部装饰线
    draw.line([(60, 480), (1140, 480)], fill=(220, 220, 220), width=2)
    
    # 底部品牌信息
    draw.text((60, 510), "专业护发 · 娜可露露", font=font_brand, fill=(150, 150, 150))
    draw.text((60, 550), "NAKORURU HAIR CARE", font=font_small, fill=(180, 180, 180))
    
    # 绘制右下角装饰圆圈
    draw.ellipse([1080, 520, 1160, 600], outline=product["color"], width=4)
    
    # 绘制右上角小装饰
    for i in range(3):
        draw.ellipse([1000 + i*40, 50, 1030 + i*40, 80], fill=product["color"])
    
    return img

# 生成所有产品广告图
print("开始生成广告图...")
for i, product in enumerate(products):
    img = create_ad_image(product, i)
    filename = f"{product['name']}_广告图.png"
    filepath = os.path.join(images_dir, filename)
    img.save(filepath, "PNG")
    print(f"✓ 已生成: {filename}")

print(f"\n✅ 共生成 {len(products)} 张广告图")
print(f"📁 保存位置: {images_dir}")
