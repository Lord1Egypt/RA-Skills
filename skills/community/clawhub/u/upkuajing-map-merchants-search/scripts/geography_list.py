#!/usr/bin/env python3
"""
地理列表查询脚本
调用跨境魔方开放平台API，获取国家/州省/城市列表
"""
import argparse
import sys
import json
from common import make_request, print_json_output


# 地理类型到API端点的映射
GEO_ENDPOINTS = {
    'country': '/common/country/list',
    'province': '/common/province/list',
    'city': '/common/city/list'
}


def get_geography_list(geo_type, country_id=None):
    """
    获取地理列表

    Args:
        geo_type: 地理类型 (country/province/city)
        country_id: 国家ID (province/city 必填)

    Returns:
        dict: {
            'type': str,           # 地理类型
            'country_id': int,     # 国家ID
            'status': str,         # success/fail
            'total': int,          # 总条数
            'list': list,          # 地理列表
            'error_msg': str       # 错误信息（如果有）
        }
    """
    # 参数校验
    if geo_type not in GEO_ENDPOINTS:
        return {
            "type": geo_type,
            "country_id": country_id,
            "status": "fail",
            "total": 0,
            "list": [],
            "error_msg": f"不支持的地理类型: {geo_type}，请使用 country/province/city"
        }

    if geo_type in ('province', 'city') and not country_id:
        return {
            "type": geo_type,
            "country_id": None,
            "status": "fail",
            "total": 0,
            "list": [],
            "error_msg": f"获取{geo_type}列表需要提供 country_id"
        }

    # 构建请求参数
    params = {}
    if country_id:
        params["id"] = country_id

    # 显示查询信息
    if geo_type == 'country':
        print("获取国家列表...")
    elif geo_type == 'province':
        print(f"获取国家ID {country_id} 的州省列表...")
    else:
        print(f"获取国家ID {country_id} 的城市列表...")

    # 发起请求
    endpoint = GEO_ENDPOINTS[geo_type]
    response = make_request(endpoint, params, require_auth = False)

    # 检查响应
    if response.get('code') != 0:
        return {
            "type": geo_type,
            "country_id": country_id,
            "status": "fail",
            "total": 0,
            "list": [],
            "error_msg": response.get('msg', '未知错误')
        }

    geo_list = response.get('data', {}).get('list', [])

    return {
        "type": geo_type,
        "country_id": country_id,
        "status": "success",
        "total": len(geo_list),
        "list": geo_list,
        "error_msg": ""
    }


def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台获取地理列表'
    )
    parser.add_argument(
        '--type',
        type=str,
        required=True,
        choices=['country', 'province', 'city'],
        help='地理类型: country-国家列表, province-州省列表, city-城市列表'
    )
    parser.add_argument(
        '--country_id',
        type=int,
        default=None,
        help='国家ID，查询省份和城市时必填'
    )

    args = parser.parse_args()

    # 执行查询
    result = get_geography_list(args.type, args.country_id)

    # 输出结果
    if result['status'] == 'success':
        print(f"\n获取成功，共 {result['total']} 条数据")
        for item in result['list']:
            print(f"  ID: {item.get('id')}, 名称: {item.get('name')}, 英文名: {item.get('nameEn', '')}")

        # 保存到文件
        filename = f"{result['type']}_list.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result['list'], f, ensure_ascii=False, indent=2)
        print(f"结果已保存到: {filename}")
    else:
        print(f"\n获取失败：{result['error_msg']}", file=sys.stderr)

    # 输出 JSON 结果
    print_json_output(result)

    # 如果有错误，返回非0退出码
    if result['status'] != 'success':
        sys.exit(1)


if __name__ == '__main__':
    main()
