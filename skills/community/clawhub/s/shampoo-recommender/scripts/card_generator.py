#!/usr/bin/env python3
"""
娜可露露洗发水推荐卡片生成器
根据用户选择生成个性化推荐卡片
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

def create_recommendation_card(product_name, hair_type, scalp_issue, price_range, output_path):
    """
    生成单产品推荐卡片
    
    Args:
        product_name: 产品名称
        hair_type: 发质类型
        scalp_issue: 头皮问题
        price_range: 价格区间
        output_path: 输出文件路径
    """
    # 卡片尺寸
    width, height = 800, 450
    
    # 产品配色映射
    color_map = {
        "深层滋养修护": {"main": (139, 90, 43), "bg": (255, 248, 240)},
        "清爽控油": {"main": (70, 130, 180), "bg": (240, 248, 255)},
        "去屑止痒": {"main": (34, 139, 34), "bg": (240, 255, 240)},
        "防脱固发": {"main": (139, 69, 19), "bg": (255, 245, 238)},
        "氨基酸温和": {"main": (147, 112, 219), "bg": (248, 248, 255)},
        "蓬松丰盈": {"main": (255, 140, 0), "bg": (255, 250, 240)},
        "去氯修护": {"main": (0, 128, 128), "bg": (240, 255, 255)},
    }
    
    colors = color_map.get(product_name, {"main": (100, 100, 100), "bg": (255, 255, 255)})
    
    # 创建画布
    img = Image.new('RGB', (width, height), colors["bg"])
    draw = ImageDraw.Draw(img)
    
    # 尝试加载字体
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 48)
        font_subtitle = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)
        font_body = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 20)
        font_small = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 16)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 顶部装饰条
    draw.rectangle([0, 0, width, 10], fill=colors["main"])
    
    # 品牌名
    draw.text((30, 30), "娜可露露", font=font_subtitle, fill=(80, 80, 80))
    draw.line([(30, 60), (150, 60)], fill=colors["main"], width=2)
    
    # 产品名称（主标题）
    draw.text((30, 80), f"为您推荐", font=font_subtitle, fill=(100, 100, 100))
    draw.text((30, 120), product_name, font=font_title, fill=colors["main"])
    draw.text((30, 190), "洗发水", font=font_subtitle, fill=colors["main"])
    
    # 右侧装饰 - 产品图标区域
    icon_x, icon_y = 600, 80
    # 瓶身轮廓
    draw.rounded_rectangle([icon_x, icon_y, icon_x + 120, icon_y + 280], 
                           radius=20, fill=(255, 255, 255), outline=colors["main"], width=3)
    # 标签
    draw.rounded_rectangle([icon_x + 15, icon_y + 100, icon_x + 105, icon_y + 200], 
                           radius=10, fill=colors["bg"])
    draw.text((icon_x + 35, icon_y + 140), "娜可\n露露", font=font_small, fill=colors["main"])
    
    # 分隔线
    draw.line([(30, 280), (770, 280)], fill=(220, 220, 220), width=1)
    
    # 用户信息
    y_pos = 300
    draw.text((30, y_pos), f"适用发质：{hair_type}", font=font_body, fill=(80, 80, 80))
    draw.text((30, y_pos + 30), f"针对问题：{scalp_issue}", font=font_body, fill=(80, 80, 80))
    draw.text((30, y_pos + 60), f"参考价格：{price_range}", font=font_body, fill=colors["main"])
    
    # 底部品牌
    draw.text((30, 410), "NAKORURU HAIR CARE", font=font_small, fill=(180, 180, 180))
    
    # 保存
    img.save(output_path, "PNG")
    print(f"✅ 已生成推荐卡片: {output_path}")
    return output_path


def create_comparison_card(product1, product2, output_path):
    """
    生成双产品对比卡片
    
    Args:
        product1: 第一个产品信息字典
        product2: 第二个产品信息字典
        output_path: 输出文件路径
    """
    width, height = 1000, 500
    
    # 创建白色背景
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 36)
        font_subtitle = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)
        font_body = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 18)
        font_small = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 14)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 顶部标题
    draw.rectangle([0, 0, width, 60], fill=(100, 100, 100))
    draw.text((30, 15), "娜可露露 · 产品对比推荐", font=font_subtitle, fill=(255, 255, 255))
    
    # 产品配色
    color_map = {
        "深层滋养修护": (139, 90, 43),
        "清爽控油": (70, 130, 180),
        "去屑止痒": (34, 139, 34),
        "防脱固发": (139, 69, 19),
        "氨基酸温和": (147, 112, 219),
        "蓬松丰盈": (255, 140, 0),
        "去氯修护": (0, 128, 128),
    }
    
    # 绘制两个产品区域
    products = [product1, product2]
    for i, prod in enumerate(products):
        x_offset = i * 500
        color = color_map.get(prod["name"], (100, 100, 100))
        
        # 产品背景
        bg_color = tuple(min(255, c + 240) for c in color)
        draw.rectangle([x_offset, 60, x_offset + 500, height], fill=bg_color)
        
        # 产品名称
        draw.text((x_offset + 30, 80), prod["name"], font=font_title, fill=color)
        draw.text((x_offset + 30, 130), "洗发水", font=font_subtitle, fill=color)
        
        # 产品信息
        y = 180
        for key, value in prod.items():
            if key != "name":
                draw.text((x_offset + 30, y), f"{key}: {value}", font=font_body, fill=(80, 80, 80))
                y += 30
        
        # 分隔线
        if i == 0:
            draw.line([(500, 60), (500, height)], fill=(200, 200, 200), width=2)
    
    # 底部
    draw.rectangle([0, height - 40, width, height], fill=(240, 240, 240))
    draw.text((30, height - 30), "NAKORURU HAIR CARE", font=font_small, fill=(150, 150, 150))
    
    img.save(output_path, "PNG")
    print(f"✅ 已生成对比卡片: {output_path}")
    return output_path


if __name__ == "__main__":
    # 示例用法
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        # 生成示例卡片
        output_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 单产品推荐卡片示例
        create_recommendation_card(
            product_name="清爽控油",
            hair_type="油性发质",
            scalp_issue="头皮出油、发根塌陷",
            price_range="¥59-89",
            output_path=os.path.join(output_dir, "示例_单款推荐.png")
        )
        
        # 双产品对比卡片示例
        create_comparison_card(
            product1={
                "name": "清爽控油",
                "适用发质": "油性发质",
                "核心功效": "控油因子、持久蓬松",
                "价格区间": "¥59-89"
            },
            product2={
                "name": "去屑止痒",
                "适用发质": "中性/油性发质",
                "核心功效": "吡硫翁锌、舒缓头皮",
                "价格区间": "¥59-89"
            },
            output_path=os.path.join(output_dir, "示例_双款对比.png")
        )
        
        print("\n✅ 示例卡片生成完成！")
    else:
        print("用法: python card_generator.py demo")
        print("运行 demo 模式生成示例卡片")
