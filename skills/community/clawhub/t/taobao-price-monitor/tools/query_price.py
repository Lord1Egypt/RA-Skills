#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
淘宝价格查询工具
支持淘宝/天猫商品价格抓取
"""

import requests
import re
import json
from datetime import datetime
from typing import Optional, Dict, Any

# 淘宝/天猫 API 端点（公开接口）
TAOBAO_ITEM_API = "https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Referer": "https://m.taobao.com",
}

def extract_item_id(url: str) -> Optional[str]:
    """从 URL 中提取商品 ID"""
    patterns = [
        r'id=(\d+)',
        r'item\.htm\?id=(\d+)',
        r'item\.taobao\.com/item\.htm\?id=(\d+)',
        r'detail\.tmall\.com/item\.htm\?id=(\d+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def query_taobao_price(item_id: str, cookie: Optional[str] = None) -> Dict[str, Any]:
    """
    查询淘宝商品价格
    
    Args:
        item_id: 商品 ID
        cookie: 可选的 Cookie（用于突破反爬）
    
    Returns:
        商品信息字典
    """
    params = {
        "api": "mtop.taobao.detail.getdetail",
        "v": "6.0",
        "data": json.dumps({"id": item_id}),
    }
    
    headers = HEADERS.copy()
    if cookie:
        headers["Cookie"] = cookie
    
    try:
        response = requests.get(TAOBAO_ITEM_API, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("data"):
            item_data = data["data"]
            return parse_item_data(item_data, item_id)
        else:
            return {"error": data.get("ret", ["未知错误"])[0]}
            
    except requests.RequestException as e:
        return {"error": f"请求失败：{str(e)}"}
    except json.JSONDecodeError as e:
        return {"error": f"解析失败：{str(e)}"}

def parse_item_data(data: Dict, item_id: str) -> Dict[str, Any]:
    """解析商品数据"""
    result = {
        "item_id": item_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "success": True,
    }
    
    # 商品标题
    if "item" in data:
        item = data["item"]
        result["title"] = item.get("title", "未知商品")
        result["price"] = item.get("price", "")
        
        # 价格信息
        price_info = item.get("priceInfo", {})
        if price_info:
            result["current_price"] = price_info.get("price", {}).get("priceText", "")
            result["original_price"] = price_info.get("originalPrice", {}).get("priceText", "")
        
        # 销量
        result["sales"] = item.get("soldCount", "未知")
        
        # 店铺信息
        if "shop" in data:
            shop = data["shop"]
            result["shop_name"] = shop.get("shopName", "未知店铺")
            result["shop_rating"] = shop.get("shopScore", {})
    
    # 尝试从其他字段获取价格
    if "price" not in result and "val" in data:
        val = data["val"]
        result["current_price"] = val.get("price", "")
        result["title"] = val.get("subject", "未知商品")
    
    return result

def query_price_simple(url: str) -> Dict[str, Any]:
    """
    简化版价格查询（通过移动端页面）
    
    Args:
        url: 商品 URL
    
    Returns:
        商品信息
    """
    item_id = extract_item_id(url)
    if not item_id:
        return {"error": "无法从 URL 中提取商品 ID"}
    
    # 尝试通过移动端页面获取
    mobile_url = f"https://m.taobao.com/awp/core/detail.htm?id={item_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    
    try:
        response = requests.get(mobile_url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text
        
        # 尝试从页面中提取价格
        price_match = re.search(r'"price":"([\d.]+)"', html)
        title_match = re.search(r'"title":"([^"]+)"', html)
        
        result = {
            "item_id": item_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "url": url,
        }
        
        if price_match:
            result["current_price"] = price_match.group(1)
        else:
            result["current_price"] = "无法获取"
        
        if title_match:
            result["title"] = title_match.group(1).replace("\\", "")
        else:
            result["title"] = "未知商品"
        
        result["success"] = True
        return result
        
    except requests.RequestException as e:
        return {
            "item_id": item_id,
            "error": f"请求失败：{str(e)}",
            "success": False,
        }

def main():
    """主函数 - 测试用"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python3 query_price.py <商品 URL 或 ID>")
        print("示例：python3 query_price.py https://item.taobao.com/item.htm?id=123456789")
        sys.exit(1)
    
    url_or_id = sys.argv[1]
    
    # 判断是 URL 还是 ID
    if url_or_id.startswith("http"):
        result = query_price_simple(url_or_id)
    else:
        result = query_taobao_price(url_or_id)
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
