"""
可视化模块
生成搭配图片
"""

import os
from typing import List, Dict, Optional
from PIL import Image, ImageDraw, ImageFont
import random

class OutfitVisualizer:
    """搭配可视化器"""
    
    def __init__(self, image_path: str = "./assets/images/outfits"):
        self.image_path = image_path
        self.default_size = (512, 512)
        
    def create_outfit_image(self, items: List[str], style: str = "default") -> Optional[str]:
        """
        创建搭配图片（PIL 拼图）
        
        Args:
            items: 单品名称列表
            style: 风格
        
        Returns:
            生成的图片路径
        """
        # 找匹配的参考图
        ref_images = self._find_reference_images(items, style)
        
        if not ref_images:
            # 没有参考图，生成文字版
            return self._create_text_only_image(items)
        
        # 创建拼图
        return self._create_composite_image(ref_images, items)
    
    def _find_reference_images(self, items: List[str], style: str) -> List[str]:
        """找匹配的参考图片"""
        images = []
        
        # 扫描 outfits 目录
        if os.path.exists(self.image_path):
            all_images = [f for f in os.listdir(self.image_path) 
                         if f.endswith(('.jpg', '.jpeg', '.png'))]
            
            # 随机选择一些
            if all_images:
                selected = random.sample(all_images, min(4, len(all_images)))
                images = [os.path.join(self.image_path, f) for f in selected]
        
        return images
    
    def _create_composite_image(self, ref_images: List[str], items: List[str]) -> str:
        """创建合成图片"""
        # 创建画布
        canvas = Image.new('RGB', (1024, 1024), color=(250, 248, 245))
        draw = ImageDraw.Draw(canvas)
        
        # 放置参考图（2x2 网格）
        positions = [(0, 0), (512, 0), (0, 512), (512, 512)]
        
        for i, img_path in enumerate(ref_images[:4]):
            try:
                img = Image.open(img_path)
                img = img.resize((512, 512), Image.Resampling.LANCZOS)
                canvas.paste(img, positions[i])
            except:
                pass
        
        # 添加标题
        title = " + ".join(items[:3])
        self._add_title(draw, title, (512, 30))
        
        # 保存
        output_path = f"./assets/images/temp_outfit_{random.randint(1000, 9999)}.jpg"
        canvas.save(output_path, "JPEG", quality=85)
        
        return output_path
    
    def _create_text_only_image(self, items: List[str]) -> str:
        """创建纯文字图片"""
        canvas = Image.new('RGB', (600, 400), color=(255, 255, 255))
        draw = ImageDraw.Draw(canvas)
        
        # 尝试加载字体
        try:
            font_title = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 32)
            font_text = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 24)
        except:
            font_title = ImageFont.load_default()
            font_text = ImageFont.load_default()
        
        # 标题
        draw.text((300, 50), "🌸 今日搭配", fill=(60, 60, 60), anchor="mt", font=font_title)
        
        # 单品列表
        y = 120
        for i, item in enumerate(items, 1):
            draw.text((300, y), f"{i}. {item}", fill=(80, 80, 80), anchor="mt", font=font_text)
            y += 50
        
        # 保存
        output_path = f"./assets/images/temp_outfit_{random.randint(1000, 9999)}.jpg"
        canvas.save(output_path, "JPEG", quality=85)
        
        return output_path
    
    def _add_title(self, draw: ImageDraw.Draw, title: str, position: tuple):
        """添加标题"""
        try:
            font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 28)
        except:
            font = ImageFont.load_default()
        
        # 添加半透明背景
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x, y = position
        draw.rectangle(
            [x - text_width//2 - 10, y - 5, x + text_width//2 + 10, y + text_height + 5],
            fill=(255, 255, 255, 180)
        )
        
        draw.text(position, title, fill=(60, 60, 60), anchor="mt", font=font)
    
    def create_wardrobe_grid(self, items: List[Dict]) -> str:
        """
        创建衣橱网格图
        
        Args:
            items: 单品列表
        
        Returns:
            生成的图片路径
        """
        # 每行4个，计算行数
        cols = 4
        rows = (len(items) + cols - 1) // cols
        
        cell_size = 200
        canvas = Image.new('RGB', (cols * cell_size, rows * cell_size + 50), color=(245, 245, 245))
        draw = ImageDraw.Draw(canvas)
        
        # 标题
        try:
            font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 24)
        except:
            font = ImageFont.load_default()
        
        draw.text((canvas.width // 2, 25), f"👗 我的衣橱 ({len(items)}件)", 
                 fill=(60, 60, 60), anchor="mt", font=font)
        
        # 绘制网格
        for i, item in enumerate(items):
            row = i // cols
            col = i % cols
            x = col * cell_size
            y = row * cell_size + 50
            
            # 绘制单元格
            draw.rectangle([x + 2, y + 2, x + cell_size - 2, y + cell_size - 2], 
                          fill=(255, 255, 255), outline=(200, 200, 200))
            
            # 绘制文字
            name = item.get('name', '未知')
            color = item.get('color', '')
            text = f"{color}{name}"[:8]
            
            try:
                small_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 16)
            except:
                small_font = ImageFont.load_default()
            
            draw.text((x + cell_size // 2, y + cell_size // 2), text,
                     fill=(80, 80, 80), anchor="mm", font=small_font)
        
        # 保存
        output_path = "./assets/images/wardrobe_grid.jpg"
        canvas.save(output_path, "JPEG", quality=85)
        
        return output_path
