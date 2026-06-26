#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片搜索脚本
用于搜索指定城市的穿搭/时尚相关图片

使用方法：
    python search_images.py <query> [count]
    
示例：
    python search_images.py "Paris street style fashion" 5
    python search_images.py "杭州 西湖 风景" 10
    
输出：JSON 格式的图片 URL 列表
"""

import sys
import json
import urllib.request
import urllib.parse
from typing import List, Dict


def search_unsplash_images(query: str, count: int = 5) -> Dict:
    """
    使用 Unsplash API 搜索高质量图片
    
    Args:
        query: 搜索关键词
        count: 返回图片数量（默认 5 张）
    
    Returns:
        dict: 包含图片信息的字典
    """
    try:
        # Unsplash Source API（免费，无需 API key）
        # 注意：Unsplash Source 已停止服务，改用 Pexels 或其他方案
        
        # 使用 Pexels API（需要免费 API key）
        # 这里使用演示方式，实际使用时需要申请 API key
        
        # 临时方案：使用 Bing 图片搜索的公开接口（有限制）
        return search_bing_images(query, count)
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'images': []
        }


def search_bing_images(query: str, count: int = 5) -> Dict:
    """
    使用 Bing 图片搜索（简化版本）
    
    Args:
        query: 搜索关键词
        count: 返回图片数量
    
    Returns:
        dict: 图片搜索结果
    """
    try:
        # 编码查询
        encoded_query = urllib.parse.quote(query)
        
        # 构建搜索 URL
        search_url = f"https://www.bing.com/images/search?q={encoded_query}&first=1&count={count}"
        
        # 设置请求头（模拟浏览器）
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
        
        req = urllib.request.Request(search_url, headers=headers)
        
        # 注意：这个方法只能获取搜索页面，不能直接获取图片 URL
        # 实际应用中应该使用正式的 API（如 Pexels、Pixabay 等）
        
        # 返回提示信息
        return {
            'success': True,
            'message': '图片搜索功能需要配置正式 API',
            'search_query': query,
            'suggested_apis': [
                'Pexels API: https://www.pexels.com/api/',
                'Pixabay API: https://pixabay.com/api/docs/',
                'Unsplash API: https://unsplash.com/developers'
            ],
            'manual_search_url': f'https://www.bing.com/images/search?q={encoded_query}',
            'images': []
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'images': []
        }


def search_pexels_images(query: str, api_key: str, count: int = 5) -> Dict:
    """
    使用 Pexels API 搜索图片（推荐方式）
    
    需要先申请免费 API key: https://www.pexels.com/api/
    
    Args:
        query: 搜索关键词
        api_key: Pexels API key
        count: 返回图片数量
    
    Returns:
        dict: 包含图片信息的字典
    """
    try:
        # 编码查询
        encoded_query = urllib.parse.quote(query)
        
        # Pexels API URL
        url = f"https://api.pexels.com/v1/search?query={encoded_query}&per_page={count}"
        
        # 设置请求头
        headers = {
            'Authorization': api_key,
            'User-Agent': 'Weather Outfit Advisor / 1.0'
        }
        
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            images = []
            for photo in data.get('photos', []):
                images.append({
                    'url': photo['src']['large'],
                    'thumbnail': photo['src']['medium'],
                    'photographer': photo.get('photographer', 'Unknown'),
                    'width': photo.get('width', 0),
                    'height': photo.get('height', 0),
                    'alt': photo.get('alt', '')
                })
            
            return {
                'success': True,
                'total_results': data.get('total_results', 0),
                'query': query,
                'images': images
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'images': []
        }


def search_pixabay_images(api_key: str, query: str, count: int = 5) -> Dict:
    """
    使用 Pixabay API 搜索图片
    
    需要先申请免费 API key: https://pixabay.com/api/docs/
    
    Args:
        api_key: Pixabay API key
        query: 搜索关键词
        count: 返回图片数量
    
    Returns:
        dict: 包含图片信息的字典
    """
    try:
        # 编码查询
        encoded_query = urllib.parse.quote(query)
        
        # Pixabay API URL
        url = f"https://pixabay.com/api/?key={api_key}&q={encoded_query}&image_type=photo&per_page={count}"
        
        req = urllib.request.Request(url)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            images = []
            for hit in data.get('hits', []):
                images.append({
                    'url': hit.get('largeImageURL', ''),
                    'thumbnail': hit.get('previewURL', ''),
                    'photographer': hit.get('user', 'Unknown'),
                    'width': hit.get('imageWidth', 0),
                    'height': hit.get('imageHeight', 0),
                    'tags': hit.get('tags', '')
                })
            
            return {
                'success': True,
                'total_hits': data.get('totalHits', 0),
                'query': query,
                'images': images
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'images': []
        }


def generate_fashion_query(city: str, context: str = '') -> str:
    """
    生成时尚的搜索关键词
    
    Args:
        city: 城市名称
        context: 上下文（如季节、场合等）
    
    Returns:
        str: 优化后的搜索关键词
    """
    # 基础模板
    templates = [
        f"{city} street style fashion",
        f"{city} outfit ideas",
        f"{city} casual wear",
        f"{city} fashion inspiration",
        f"what to wear in {city}",
    ]
    
    # 如果有特定上下文
    if context:
        templates.extend([
            f"{city} {context} outfit",
            f"{city} {context} fashion",
        ])
    
    # 返回第一个作为默认
    return templates[0]


def format_output(result: Dict, show_urls: bool = True) -> str:
    """
    格式化输出结果
    
    Args:
        result: 搜索结果字典
        show_urls: 是否显示 URL
    
    Returns:
        str: 格式化的输出字符串
    """
    if not result.get('success'):
        return f"❌ 搜索失败：{result.get('error', '未知错误')}"
    
    output = []
    output.append(f"🔍 搜索关键词：{result.get('query', 'N/A')}")
    
    if 'total_results' in result:
        output.append(f"📊 找到 {result['total_results']} 张图片")
    elif 'total_hits' in result:
        output.append(f"📊 找到 {result['total_hits']} 张图片")
    
    images = result.get('images', [])
    if not images:
        if 'manual_search_url' in result:
            output.append("")
            output.append("💡 建议手动搜索:")
            output.append(f"   {result['manual_search_url']}")
            output.append("")
            output.append("📸 可使用的图片 API:")
            for api in result.get('suggested_apis', []):
                output.append(f"   - {api}")
        return '\n'.join(output)
    
    output.append("")
    output.append("🖼️ 图片列表:")
    
    for i, img in enumerate(images, 1):
        output.append(f"\n【图片 {i}】")
        if img.get('photographer'):
            output.append(f"  摄影师：{img['photographer']}")
        if img.get('width') and img.get('height'):
            output.append(f"  尺寸：{img['width']}x{img['height']}")
        if img.get('alt') or img.get('tags'):
            output.append(f"  描述：{img.get('alt', img.get('tags', ''))}")
        if show_urls:
            output.append(f"  查看：{img.get('url', img.get('thumbnail', ''))}")
    
    return '\n'.join(output)


def main():
    """主函数"""
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("用法：python search_images.py <query> [count]")
        print("示例：python search_images.py \"Paris fashion\" 5")
        print("      python search_images.py \"杭州 风景\" 10")
        print("\n如果不指定数量，默认返回 5 张图片")
        sys.exit(1)
    
    # 解析参数
    query = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    # 执行搜索
    print(f"正在搜索：{query}...", file=sys.stderr)
    
    # 尝试不同的 API
    # 方法 1: 使用 Pexels API（已配置 API key）
    pexels_api_key = "D6nVsjiUzdW7BctVWb3Hf8KdmkZ3qF0oZNPAu4labGgxbYsFHegeFNNO"
    
    if pexels_api_key and pexels_api_key != "your_api_key_here":
        result = search_pexels_images(query, pexels_api_key, count)
    else:
        # 降级方案：使用 Bing 搜索
        result = search_bing_images(query, count)
    
    # 输出结果（JSON 格式）
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 同时输出人类可读版本到 stderr
    print("\n=== 人类可读版本 ===", file=sys.stderr)
    print(format_output(result), file=sys.stderr)


if __name__ == '__main__':
    main()
