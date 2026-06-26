"""
工具函数
- 文件操作
- 图片下载
- 格式转换
- 路径处理
"""

import os
import re
import logging
from pathlib import Path
from typing import Optional, List
import requests

logger = logging.getLogger(__name__)

def ensure_output_dir(output_dir: str = None) -> Path:
    """
    确保输出目录存在
    默认使用 C:\Users\123\Desktop\选品
    """
    if output_dir is None:
        output_dir = os.environ.get("SHORT_VIDEO_OUTPUT_DIR", r"C:\Users\123\Desktop\选品")
    
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path

def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除非法字符
    """
    # 替换Windows文件系统不允许的字符
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    # 限制长度
    if len(sanitized) > 50:
        sanitized = sanitized[:47] + "..."
    return sanitized.strip()

def generate_product_filename(index: int, name: str, ext: str = "jpg") -> str:
    """
    生成商品主图文件名: 序号_商品名称.ext
    """
    safe_name = sanitize_filename(name)
    return f"{index}_{safe_name}.{ext}"

def download_image(url: str, save_path: Path) -> bool:
    """
    下载图片到指定路径
    返回是否成功
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(save_path, "wb") as f:
            f.write(response.content)
        
        # 检查文件大小，小于1KB视为失败
        if save_path.stat().st_size < 1024:
            save_path.unlink(missing_ok=True)
            logger.warning(f"图片下载失败，文件过小: {url}")
            return False
        
        logger.info(f"图片下载成功: {save_path}")
        return True
    except Exception as e:
        logger.error(f"图片下载失败 {url}: {str(e)}")
        return False

def check_api_key(key_name: str) -> Optional[str]:
    """
    检查环境变量中是否存在API密钥
    返回密钥值或None
    """
    key = os.environ.get(key_name)
    if not key or key == f"your_{key_name.lower()}_here":
        return None
    return key

def format_product_line(index: int, name: str, price: float, url: str) -> str:
    """
    格式化商品信息行
    [序号]. 名称：XXX 价格：XXX 链接：XXX
    """
    return f"[{index}]. 名称：{name} 价格：{price:.2f} 链接：{url}"

def split_script_15s(script: str) -> List[str]:
    """
    将15秒文案切分为三段（每段5秒）
    按照 0-5s / 5-10s / 10-15s 切分
    """
    # 如果已经分段，直接返回
    lines = [line.strip() for line in script.split('\n') if line.strip()]
    if len(lines) >= 3:
        return lines[:3]
    
    # 否则按句子切分
    sentences = re.split(r'[。！？!?]+', script)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) >= 3:
        return sentences[:3]
    
    # 如果句子太少，强制切分三段
    total_len = len(script)
    part1 = script[:total_len//3].strip()
    part2 = script[total_len//3:2*total_len//3].strip()
    part3 = script[2*total_len//3:].strip()
    
    return [part1, part2, part3]

def get_platform_aspect_ratio(platform: str) -> tuple:
    """
    根据平台获取推荐宽高比
    返回 (width, height)
    抖音/快手: 9:16
    小红书: 3:4
    """
    platform = platform.lower()
    if platform in ["xiaohongshu", "rednote", "小红书"]:
        return (3, 4)
    else: # douyin, kuaishou, 抖音, 快手
        return (9, 16)
