"""
第六步：一键商品上架
调用 ecommerce-api 自动上架到对应平台
- 自动填充商品信息
- 上传主图和视频
- 发布商品
"""

import os
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class PublishStep:
    def __init__(self):
        pass
        
    def publish(self, platform: str, product_info: Dict, image_path: str, video_path: str = None) -> dict:
        """
        一键发布商品到平台
        """
        # 检查平台API是否配置
        api_configured = self._check_api_configured(platform)
        
        if not api_configured:
            logger.info(f"{platform} API未配置，输出手动上架清单")
            return {
                "success": True,
                "auto_publish": False,
                "manual_info": self._generate_manual_info(product_info, image_path, video_path)
            }
            
        logger.info(f"正在自动上架到 {platform}")
        
        # TODO: 调用 ecommerce-api 发布
        # 返回商品链接
        
        return {
            "success": True,
            "auto_publish": True,
            "product_url": "https://example.com/product"
        }
    
    def _check_api_configured(self, platform: str) -> bool:
        """检查对应平台API是否配置"""
        platform_keys = {
            "douyin": ["DOUDIAN_APP_KEY", "DOUDIAN_APP_SECRET"],
            "kuaishou": ["KUAIHOU_APP_ID", "KUAIHOU_APP_SECRET"],
            "pinduoduo": ["PDD_CLIENT_ID", "PDD_CLIENT_SECRET"],
            "taobao": ["TB_APP_KEY", "TB_APP_SECRET"],
        }
        
        keys = platform_keys.get(platform.lower(), [])
        if not keys:
            return False
            
        return all(os.environ.get(key) for key in keys)
    
    def _generate_manual_info(self, product_info: Dict, image_path: str, video_path: str = None) -> str:
        """生成手动上架信息清单"""
        info = "====== 手动上架信息 ======\n"
        info += f"商品标题: {product_info.get('name', '')}\n"
        info += f"商品价格: {product_info.get('price', '')}\n"
        info += f"商品分类: {product_info.get('category', '请自动匹配')}\n"
        info += f"主图文件: {image_path}\n"
        if video_path:
            info += f"短视频文件: {video_path}\n"
        info += "\n请复制以上信息到平台后台手动上传\n"
        return info
