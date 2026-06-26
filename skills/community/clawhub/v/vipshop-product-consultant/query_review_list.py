#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商品评价列表查询脚本 - 调用唯品会评价列表接口
"""

import requests
import json
import re
import sys
import time


def extract_json_from_jsonp(response_text, callback_name):
    """从JSONP响应中提取JSON数据"""
    pattern = rf'{callback_name}\((.*)\)\s*$'
    match = re.search(pattern, response_text, re.DOTALL)
    if match:
        return match.group(1)
    return None


def query_review_list(spu_id, brand_id, page=1, page_size=10):
    """
    查询商品评价列表接口
    :param spu_id: 商品SPU ID
    :param brand_id: 品牌ID
    :param page: 页码
    :param page_size: 每页数量
    :return: 评价列表字典
    """
    url = "https://mapi-pc.vip.com/vips-mobile/rest/content/reputation/queryBySpuId_for_pc"
    
    # 生成当前时间戳
    timestamp = int(time.time() * 1000)
    
    params = {
        "callback": "getCommentDataCb",
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
        "spuId": spu_id,
        "brandId": brand_id,
        "page": page,
        "pageSize": page_size,
        "functions": "angle",
        "timestamp": timestamp,
        "keyWordNlp": "全部-按默认排序",
        "tfs_fp_token": "BltVfgoZTN3XDZY5O1CcipyLDFtBC0a60NsYZ2qM/uJfQUOyBYCjdbamUKRRCr9cXl+UlnkvGDk2vjrA5+uQC9Q==",
        "_": timestamp - 1000
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
        json_str = extract_json_from_jsonp(response.text, "getCommentDataCb")
        if not json_str:
            print("错误：无法从响应中提取JSON数据")
            print(f"响应内容前500字符: {response.text[:500]}")
            return None
        
        data = json.loads(json_str)
        
        # 保存原始响应到文件
        with open('review_list_response.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("原始响应已保存到 review_list_response.json")
        
        # 检查响应状态 - 兼容code=0或code=1
        code = data.get('code', -1)
        if code not in [0, 1, 200]:
            print(f"API返回错误: code={code}, message={data.get('msg', '未知错误')}")
            return None
        
        # 提取评价列表信息 - data是list的情况
        result_data = data.get('data', [])
        
        if isinstance(result_data, list):
            reviews = result_data
            total = len(reviews)
        else:
            reviews = result_data.get('list', [])
            total = result_data.get('total', len(reviews))
        
        review_list = []
        for item in reviews:
            # 评价数据在 reputation 字段中
            reputation = item.get('reputation', {})
            user_info = item.get('reputationUser', {})
            product_info = item.get('reputationProduct', {})
            
            # 提取评价标签
            tags = []
            impresses_list = reputation.get('impressesTagList', [])
            for tag in impresses_list:
                tags.append(tag.get('tagValue', ''))
            
            # 提取图片列表
            images = []
            image_list = reputation.get('imageList', [])
            for img in image_list:
                images.append(img.get('url', ''))
            
            review_info = {
                'reputationId': reputation.get('reputationId'),
                'userName': user_info.get('authorName', '匿名用户'),
                'userLevel': user_info.get('memberLvl', ''),
                'userAddress': reputation.get('address', ''),
                'satisfiedStatus': reputation.get('satisfiedStatus', ''),
                'content': reputation.get('content', ''),
                'createTime': reputation.get('timeDesc', ''),
                'postTime': reputation.get('postTime', ''),
                'productInfo': f"{product_info.get('colorInfo', '')} {product_info.get('size', '')}".strip(),
                'likeCount': reputation.get('usefulCount', 0),
                'imageCount': reputation.get('imageCount', 0),
                'images': images,
                'tags': tags,
                'isAnonymous': reputation.get('isAnonymous', 'YES'),
                'extensionFlags': reputation.get('extensionFlags', {})
            }
            review_list.append(review_info)
        
        list_info = {
            'spuId': spu_id,
            'brandId': brand_id,
            'page': page,
            'pageSize': page_size,
            'total': total,
            'reviewCount': len(review_list),
            'reviews': review_list
        }
        
        # 保存提取的信息
        with open('review_list.json', 'w', encoding='utf-8') as f:
            json.dump(list_info, f, ensure_ascii=False, indent=2)
        
        print("\n=== 评价列表提取成功 ===")
        print(f"当前页: {page}")
        print(f"每页数量: {page_size}")
        print(f"总评价数: {total}")
        print(f"本次获取: {len(review_list)}条")
        
        if review_list:
            print(f"\n评价详情 (前3条):")
            for i, review in enumerate(review_list[:3], 1):
                satisfied = review.get('satisfiedStatus', '')
                satisfied_icon = "😊" if satisfied == "VERY_SATISFIED" else "😐" if satisfied == "SATISFIED" else "😞"
                print(f"\n【评价{i}】 {satisfied_icon}")
                print(f"  用户: {review.get('userName')} ({review.get('userAddress')})")
                print(f"  时间: {review.get('createTime')}")
                content = review.get('content', '').strip()
                if content:
                    print(f"  内容: {content[:100]}{'...' if len(content) > 100 else ''}")
                else:
                    print(f"  内容: [图片评价，无文字]")
                if review.get('tags'):
                    print(f"  标签: {', '.join(review.get('tags'))}")
                if review.get('productInfo'):
                    print(f"  规格: {review.get('productInfo')}")
                if review.get('imageCount', 0) > 0:
                    print(f"  图片: {review.get('imageCount')}张")
        
        print("\n关键信息已保存到 review_list.json")
        
        return list_info
        
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
    # 默认参数，可以通过命令行参数传入
    default_spu_id = "1243352167575445504"
    default_brand_id = "1710618487"
    
    if len(sys.argv) >= 3:
        spu_id = sys.argv[1]
        brand_id = sys.argv[2]
    else:
        spu_id = default_spu_id
        brand_id = default_brand_id
        print(f"使用默认参数:")
        print(f"  spuId: {spu_id}")
        print(f"  brandId: {brand_id}")
        print(f"\n如需查询其他商品，请运行: python query_review_list.py <spu_id> <brand_id>")
        print(f"提示: spuId和brandId可以从 query_product_info.py 的输出中获取\n")
    
    result = query_review_list(spu_id, brand_id)
    
    if result:
        print("\n✅ 评价列表查询成功！")
        sys.exit(0)
    else:
        print("\n❌ 评价列表查询失败！")
        sys.exit(1)
