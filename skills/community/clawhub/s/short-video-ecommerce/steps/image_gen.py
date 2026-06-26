"""
第三步：AI图片生成
- 根据平台适配尺寸生成短视频封面
- 主图去logo处理
- 可选生成场景宣传图
"""

import os
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class ImageGenStep:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        
    def generate_cover(self, product_name: str, platform: str, script: str) -> dict:
        """
        生成短视频封面图
        """
        # 检查API
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            return {
                "success": True,
                "skipped": True,
                "reason": "OPENROUTER_API_KEY not configured"
            }
        
        # 获取正确尺寸
        aspect_ratio = self._get_aspect_ratio(platform)
        prompt = self._build_cover_prompt(product_name, script)
        
        logger.info(f"正在生成{platform}封面，比例: {aspect_ratio}")
        
        # TODO: 调用 nano-banana-pro-openrouter 生成
        # 返回保存路径
        
        return {
            "success": True,
            "skipped": False,
            "product": product_name,
            "aspect_ratio": aspect_ratio,
            "prompt": prompt
        }
    
    def remove_logo(self, image_path) -> dict:
        """
        去除商品主图logo，避免侵权
        """
        # TODO: 图像处理去logo
        return {
            "success": True,
            "processed": image_path
        }
    
    def generate_scene_image(self, product_name: str, script_section: str) -> dict:
        """
        生成场景宣传图
        """
        return {
            "success": True,
            "skipped": not os.environ.get("OPENROUTER_API_KEY")
        }
    
    def _get_aspect_ratio(self, platform: str) -> Tuple[int, int]:
        """根据平台获取宽高比"""
        platform = platform.lower()
        if platform in ["xiaohongshu", "rednote", "小红书"]:
            return (3, 4)
        return (9, 16)
    
    def _build_cover_prompt(self, product_name: str, script: str) -> str:
        """构建封面图提示词"""
        return f"""短视频封面图，商品：{product_name}
风格：吸睛，高对比度，清晰主体
文案突出卖点：{script[:50]}
电商爆款风格，适合手机端观看
"""
