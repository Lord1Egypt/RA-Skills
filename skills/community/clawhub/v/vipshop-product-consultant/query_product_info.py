#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商品信息查询脚本 - 调用唯品会商品信息接口
"""

import requests
import json
import re
import sys


def extract_json_from_jsonp(response_text, callback_name):
    """从JSONP响应中提取JSON数据"""
    pattern = rf'{callback_name}\((.*)\)\s*$'
    match = re.search(pattern, response_text, re.DOTALL)
    if match:
        return match.group(1)
    return None


def query_product_info(product_ids):
    """
    查询商品信息接口
    :param product_ids: 商品ID，多个用逗号分隔
    :return: 商品信息字典
    """
    url = "https://mapi-pc.vip.com/vips-mobile/rest/shopping/pc/product/module/list/v2"
    
    params = {
        "callback": "detailRecommendList",
        "app_name": "shop_pc",
        "app_version": "4.0",
        "warehouse": "VIP_NH",
        "fdc_area_id": "104104101",
        "client": "pc",
        "mobile_platform": "1",
        "province_id": "104104",
        "api_key": "70f71280d5d547b2a7bb370a529aeea1",
        "user_id": "302134333",
        "mars_cid": "1717465638168_f77af888f9f775b14e0d8044dc768fdc",
        "wap_consumer": "c",
        "is_default_area": "1",
        "productIds": product_ids,
        "scene": "detail_reco",
        "standby_id": "nature",
        "extParams": '{"preheatTipsVer":"3","couponVer":"v2","exclusivePrice":"1","iconSpec":"2x"}',
        "context": "",
        "tfs_fp_token": "BIpQm8gcVdEzjbWpjLe/awUCEg8JQONdi3AFLdiYa+wJEQlzFSv9ZKe/JQMAkjfuQNqKLppFJhkkd1W55/MBDLQ==",
        "_": "1770770678334"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://www.vip.com/"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        # 解析JSONP响应
        json_str = extract_json_from_jsonp(response.text, "detailRecommendList")
        if not json_str:
            print("错误：无法从响应中提取JSON数据")
            print(f"响应内容前500字符: {response.text[:500]}")
            return None
        
        data = json.loads(json_str)
        
        # 保存原始响应到文件
        with open('product_info_response.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("原始响应已保存到 product_info_response.json")
        
        # 检查响应状态 - 兼容code=0或code=1
        code = data.get('code', -1)
        if code not in [0, 1, 200]:
            print(f"API返回错误: code={code}, message={data.get('msg', '未知错误')}")
            return None
        
        # 提取商品信息
        result_data = data.get('data', {})
        products = result_data.get('products', [])
        
        if not products:
            print("警告：未找到商品信息")
            return None
        
        # 提取第一个商品的关键信息
        product = products[0]
        
        # 处理价格字段（可能是嵌套字典）
        price_info = product.get('price', {})
        if isinstance(price_info, dict):
            sale_price = price_info.get('salePrice', '未知')
            market_price = price_info.get('marketPrice', '未知')
            discount = price_info.get('saleDiscount', price_info.get('mixPriceLabel', '未知'))
            price_label = price_info.get('priceLabel', '')
        else:
            sale_price = price_info
            market_price = product.get('marketPrice', '未知')
            discount = product.get('discount', '未知')
            price_label = ''
        
        product_info = {
            'productId': product.get('productId'),
            'spuId': product.get('spuId'),
            'brandId': product.get('brandId'),
            'brandName': product.get('brandName'),
            'brandStoreSn': product.get('brandStoreSn'),
            'productName': product.get('productName'),
            'title': product.get('title'),
            'price': sale_price,
            'marketPrice': market_price,
            'discount': discount,
            'priceLabel': price_label,
            'image': product.get('image'),
            'category': product.get('category'),
            'raw_data': product
        }
        
        # 保存提取的信息
        with open('product_info.json', 'w', encoding='utf-8') as f:
            json.dump(product_info, f, ensure_ascii=False, indent=2)
        
        print("\n=== 商品信息提取成功 ===")
        print(f"商品名称: {product_info.get('productName') or product_info.get('title')}")
        print(f"品牌: {product_info.get('brandName')}")
        print(f"spuId: {product_info.get('spuId')}")
        print(f"brandId: {product_info.get('brandId')}")
        print(f"{price_label}: ¥{sale_price}")
        print(f"市场价: ¥{market_price}")
        print(f"折扣: {discount}")
        print("\n关键信息已保存到 product_info.json")
        print("请使用以下参数继续查询:")
        print(f"  spuId: {product_info.get('spuId')}")
        print(f"  brandId: {product_info.get('brandId')}")
        
        return product_info
        
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        print(f"响应内容前500字符: {response.text[:500]}")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None


if __name__ == "__main__":
    # 默认商品ID，可以通过命令行参数传入
    default_product_id = "6920078387106353303"
    
    if len(sys.argv) > 1:
        product_id = sys.argv[1]
    else:
        product_id = default_product_id
        print(f"使用默认商品ID: {product_id}")
        print(f"如需查询其他商品，请运行: python query_product_info.py <product_id>")
    
    result = query_product_info(product_id)
    
    if result:
        print("\n✅ 商品信息查询成功！")
        sys.exit(0)
    else:
        print("\n❌ 商品信息查询失败！")
        sys.exit(1)
