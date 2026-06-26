#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片文字合成模块
在生成的图片上添加宣传文案
"""

from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple
import os


class TextOverlay:
    """图片文字合成器"""
    
    def __init__(self):
        # 字体路径（优先使用系统字体）
        self.font_paths = [
            "/System/Library/Fonts/PingFang.ttc",  # macOS
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",  # Linux
            "C:\\Windows\\Fonts\\simhei.ttf",  # Windows
        ]
    
    def add_text(
        self,
        image_path: str,
        text: str,
        output_path: str = None,
        position: str = "bottom",
        font_size: int = 40,
        text_color: str = "white",
        bg_color: Optional[str] = "black",
        bg_opacity: int = 128
    ) -> str:
        """
        在图片上添加文字
        
        Args:
            image_path: 原图路径
            text: 文字内容
            output_path: 输出路径（默认覆盖原图）
            position: 位置 (top/bottom/left/right/center)
            font_size: 字体大小
            text_color: 文字颜色
            bg_color: 背景色（None 表示无背景）
            bg_opacity: 背景透明度 (0-255)
        
        Returns:
            输出文件路径
        """
        # 打开图片
        img = Image.open(image_path).convert('RGBA')
        draw = ImageDraw.Draw(img)
        
        # 获取字体
        font = self._get_font(font_size)
        
        # 计算文字位置
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        img_width, img_height = img.size
        x, y = self._calculate_position(position, img_width, img_height, text_width, text_height)
        
        # 绘制背景（如果有）
        if bg_color:
            bg_padding = 20
            bg_rect = [
                x - bg_padding,
                y - bg_padding,
                x + text_width + bg_padding,
                y + text_height + bg_padding
            ]
            # 创建半透明背景
            overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rectangle(bg_rect, fill=self._hex_to_rgba(bg_color, bg_opacity))
            img = Image.alpha_composite(img, overlay)
            draw = ImageDraw.Draw(img)
        
        # 绘制文字
        draw.text((x, y), text, font=font, fill=text_color)
        
        # 保存
        if output_path is None:
            output_path = image_path
        
        # 转换为 RGB（保存为 JPEG）
        if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
            img = img.convert('RGB')
        
        img.save(output_path)
        print(f"   ✓ 添加文字：{output_path}")
        return output_path
    
    def _get_font(self, size: int) -> ImageFont.FreeTypeFont:
        """获取字体"""
        for path in self.font_paths:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except:
                    continue
        
        # 回退到默认字体
        return ImageFont.load_default()
    
    def _calculate_position(
        self,
        position: str,
        img_width: int,
        img_height: int,
        text_width: int,
        text_height: int
    ) -> Tuple[int, int]:
        """计算文字位置"""
        padding = 40
        
        if position == "top":
            return (padding, padding)
        elif position == "bottom":
            return (padding, img_height - text_height - padding)
        elif position == "left":
            return (padding, padding)
        elif position == "right":
            return (img_width - text_width - padding, padding)
        elif position == "center":
            return ((img_width - text_width) // 2, (img_height - text_height) // 2)
        else:
            return (padding, padding)
    
    def _hex_to_rgba(self, hex_color: str, alpha: int = 255) -> Tuple[int, int, int, int]:
        """十六进制颜色转 RGBA"""
        # 命名颜色映射
        named_colors = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'gray': (128, 128, 128),
            'grey': (128, 128, 128),
        }
        
        # 处理命名颜色
        if hex_color.lower() in named_colors:
            r, g, b = named_colors[hex_color.lower()]
            return (r, g, b, alpha)
        
        # 处理十六进制颜色
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b, alpha)


# 便捷函数
def add_marketing_text(
    image_path: str,
    headline: str,
    subtext: str = "",
    output_path: str = None
) -> str:
    """
    添加营销文案（标题 + 副标题）
    
    Args:
        image_path: 原图路径
        headline: 主标题
        subtext: 副标题
        output_path: 输出路径
    
    Returns:
        输出文件路径
    """
    overlay = TextOverlay()
    
    # 先添加主标题（顶部）
    temp_path = image_path + ".temp.png"
    overlay.add_text(
        image_path,
        headline,
        temp_path,
        position="top",
        font_size=50,
        text_color="white",
        bg_color="black",
        bg_opacity=150
    )
    
    # 再添加副标题（底部）
    if output_path is None:
        output_path = image_path
    
    if subtext:
        overlay.add_text(
            temp_path,
            subtext,
            output_path,
            position="bottom",
            font_size=30,
            text_color="white",
            bg_color="black",
            bg_opacity=100
        )
    else:
        # 没有副标题，直接重命名
        os.rename(temp_path, output_path)
    
    # 清理临时文件
    if os.path.exists(temp_path):
        os.remove(temp_path)
    
    return output_path


if __name__ == '__main__':
    # 测试
    print("📝 图片文字合成器 - 测试")
    print("=" * 50)
    
    # 创建测试图片
    test_img = Image.new('RGB', (800, 600), color='blue')
    test_img.save('/tmp/test_overlay.png')
    
    # 添加文字
    overlay = TextOverlay()
    output = overlay.add_text(
        '/tmp/test_overlay.png',
        'Eternal Romance',
        position='center',
        font_size=40
    )
    
    print(f"✓ 测试完成：{output}")
