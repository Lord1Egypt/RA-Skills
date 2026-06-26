#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商品评价总结查询脚本 - 调用唯品会评价总结接口
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


def query_review_summary(spu_id):
    """
    查询商品评价总结接口
    :param spu_id: 商品SPU ID
    :return: 评价总结字典
    """
    url = "https://mapi-pc.vip.com/vips-mobile/rest/ugc/reputation/getSpuIdNlpKeywordV2_for_pc"
    
    params = {
        "callback": "getSpuIdNlpKeywordCb",
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
        "showTagOther": "1",
        "spuId": spu_id,
        "tfs_fp_token": "Bngk6emc/Br0YsyNUJfYuXSG4SMpaAJJLzcE+JhuQhsB1usVns8uWPRpPY8v944yFykhkm7LN6zf+FVj4h/K7Bg==",
        "_": "1770768093657"
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
        json_str = extract_json_from_jsonp(response.text, "getSpuIdNlpKeywordCb")
        if not json_str:
            print("错误：无法从响应中提取JSON数据")
            print(f"响应内容前500字符: {response.text[:500]}")
            return None
        
        data = json.loads(json_str)
        
        # 保存原始响应到文件
        with open('review_summary_response.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("原始响应已保存到 review_summary_response.json")
        
        # 检查响应状态 - 兼容code=0或code=1
        code = data.get('code', -1)
        if code not in [0, 1, 200]:
            print(f"API返回错误: code={code}, message={data.get('msg', '未知错误')}")
            return None
        
        # 提取评价总结信息
        result_data = data.get('data', {})
        
        # 提取NLP关键词列表
        keywords = []
        nlp_keyword_list = result_data.get('nlpKeyWordList', [])
        for kw in nlp_keyword_list:
            keywords.append({
                'word': kw.get('keyWordNlp'),
                'count': kw.get('keyWordCount'),
                'asKeyWordCount': kw.get('asKeyWordCount'),
                'type': kw.get('type')
            })
        
        # 提取描述信息
        description = result_data.get('description', {})
        descriptions = [description.get('description', '')] if description else []
        
        # 提取尺码感受统计
        size_feel_list = result_data.get('sizeFeelList', [])
        
        # 提取满意度
        satisfaction = result_data.get('satisfaction', '')
        satisfaction_degree = result_data.get('satisfactionDegree', '')
        
        summary_info = {
            'spuId': spu_id,
            'totalCount': result_data.get('defaultReputationNumber', '0'),
            'satisfaction': satisfaction,
            'satisfactionDegree': satisfaction_degree,
            'keywords': keywords,
            'descriptions': descriptions,
            'sizeFeelList': size_feel_list,
            'raw_data': result_data
        }
        
        # 保存提取的信息
        with open('review_summary.json', 'w', encoding='utf-8') as f:
            json.dump(summary_info, f, ensure_ascii=False, indent=2)
        
        print("\n=== 评价总结提取成功 ===")
        print(f"评价总数: {summary_info.get('totalCount')}")
        print(f"满意度: {summary_info.get('satisfactionDegree') or satisfaction}")
        
        if keywords:
            print(f"\n关键词标签 ({len(keywords)}个):")
            for kw in keywords[:10]:  # 只显示前10个
                count = kw.get('asKeyWordCount') or kw.get('count')
                if count and count != -1 and count != -4:
                    print(f"  • {kw.get('word')} ({count})")
        
        if descriptions and descriptions[0]:
            print(f"\n评价描述:")
            for desc in descriptions:
                print(f"  - {desc}")
        
        if size_feel_list:
            print(f"\n尺码感受统计:")
            for size_feel in size_feel_list:
                print(f"  {size_feel.get('sizeFeelName')}: {size_feel.get('count')}人")
        
        print("\n关键信息已保存到 review_summary.json")
        
        return summary_info
        
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
    # 默认spuId，可以通过命令行参数传入
    default_spu_id = "1243352167575445504"
    
    if len(sys.argv) > 1:
        spu_id = sys.argv[1]
    else:
        spu_id = default_spu_id
        print(f"使用默认spuId: {spu_id}")
        print(f"如需查询其他商品，请运行: python query_review_summary.py <spu_id>")
        print(f"提示: spuId可以从 query_product_info.py 的输出中获取\n")
    
    result = query_review_summary(spu_id)
    
    if result:
        print("\n✅ 评价总结查询成功！")
        sys.exit(0)
    else:
        print("\n❌ 评价总结查询失败！")
        sys.exit(1)
