#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
=============================================================================
商品检索与链接获取工具 (仅支持 Python 3，无第三方库依赖)

支持环境变量配置:
  OPENID      用于设置参数 openid (默认已内置可用值)
  INVITE_CODE 用于设置参数 inviteCode (默认已内置可用值)

使用说明：
本脚本包含两个主要功能：检索商品列表、获取指定商品的链接。

sourceType 说明：
   0: 全部, 1: 淘宝, 2: 京东, 3: 拼多多, 4: 苏宁, 5: 唯品会, 7: 抖音, 8: 快手, 22: 1688

1. 检索商品 (search)
   参数：
     --keyword    [必填] 搜索关键字
     --sourceType [可选] 来源平台类型，默认为 0
     --pages      [可选] 搜索页码，支持单页(1)或多页(1,2,3)，默认为 1
     --sort       [可选] 排序方式，传入 "price" 表示结果按价格排序输出，默认不排序
     --format     [可选] 输出格式，支持 csv 或 markdown，默认为 csv
   
   示例用法：
     python price.py search --keyword "营养早餐粥" --pages 1,2 --sort price
     python price.py search --keyword "营养早餐粥" --format markdown

2. 获取商品链接 (link)
   示例用法：
     python price.py link --goodsId "xxx" --sourceType 1
=============================================================================
"""

import json
import sys
import csv
import argparse
import time
import os
import gzip
import urllib.request as urllib_request
import urllib.parse as urllib_parse
from io import BytesIO


# ---------------- 日志与输出 ----------------
def log_err(msg):
    sys.stderr.write(str(msg) + "\n")
    sys.stderr.flush()


def log_out(msg):
    sys.stdout.write(str(msg) + "\n")
    sys.stdout.flush()


def to_str(val):
    return str(val) if val is not None else ''


# ---------------- 网络请求核心逻辑 ----------------
def get_common_headers(host, content_type):
    """
    统一生成模拟设备的请求头
    """
    openid = os.environ.get("OPENID", "dfe8842aaec8323c02dd534328b262c5")
    return {
        'clientAdd': 'lsII1AXmYoapUbyWxXgx6w==',
        'os': '1',
        'version': '4.0.2',
        'systemVersion': '15',
        'model': 'V2338A',
        'brand': 'vivo',
        'pati': '87ef65f64f18743e32badd8045db3b39',
        'Content-Type': content_type,
        'Host': host,
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/4.9.0',
        'openid': openid
    }


def send_request(url, data_bytes, headers):
    """
    统一发送请求，并透明处理 gzip 解压及 JSON 解析
    """
    req = urllib_request.Request(url, data=data_bytes, headers=headers)
    response = urllib_request.urlopen(req)
    
    encoding = response.getheader('Content-Encoding')
    res_data = response.read()
    
    # 处理 gzip 解压
    if encoding == 'gzip':
        buf = BytesIO(res_data)
        f = gzip.GzipFile(fileobj=buf)
        res_body = f.read()
    else:
        res_body = res_data
        
    res_body = res_body.decode('utf-8')
        
    return json.loads(res_body)


# ---------------- 业务接口 ----------------
def fetch_single_page(keyword, source_type, page):
    """
    内部函数：负责请求单页数据
    """
    url = 'https://appapi.maishou88.com/api/v1/homepage/searchList'
    headers = get_common_headers(host='appapi.maishou88.com', content_type='application/x-www-form-urlencoded')
    
    data = {
        'isCoupon': '0',
        'shopType': '',
        'keyword': keyword,
        'order': '',
        'page': str(page),
        'pddListId': '',
        'sort': '',
        'sourceType': str(source_type),
        'cateId': ''
    }
    
    encoded_data = urllib_parse.urlencode(data).encode('utf-8')
    
    try:
        res_json = send_request(url, encoded_data, headers)
        if res_json.get('status') == 'success':
            return res_json.get('data', [])
        else:
            log_err("警告: 第 {} 页接口返回错误: {}".format(page, res_json.get('message', '未知')))
            return []
    except Exception as e:
        log_err("警告: 第 {} 页请求失败: {}".format(page, str(e)))
        return []


def search_products(keyword, source_type, pages_str, sort_by, format_type):
    """
    接口1：检索多页商品列表并汇总输出
    """
    page_list = [p.strip() for p in pages_str.split(',')]
    all_items = []
    
    for page in page_list:
        log_err("正在抓取第 {} 页...".format(page))
        items = fetch_single_page(keyword, source_type, page)
        if items:
            all_items.extend(items)
        time.sleep(0.5)

    if not all_items:
        log_err("未检索到任何商品。")
        return

    # 若传入"price"，对结果集按实际价格重新排序
    if sort_by == 'price':
        def get_price(item):
            try:
                return float(item.get('actualPrice', 0))
            except (ValueError, TypeError):
                return 0.0
        all_items.sort(key=get_price)

    header_keys = ['ID', 'goodsId', 'sourceType', '商品', '店铺', '价格', '原价', '优惠', '月销']
    
    # 格式化输出
    if format_type == 'csv':
        writer = csv.writer(sys.stdout)
        writer.writerow(header_keys)
        for index, item in enumerate(all_items, start=1):
            row = [
                index,
                item.get('goodsId', ''),
                item.get('sourceType', ''),
                item.get('title', ''),
                item.get('shopName', ''),
                item.get('actualPrice', ''),
                item.get('originalPrice', ''),
                item.get('couponPrice', ''),
                item.get('monthSales', '')
            ]
            writer.writerow([to_str(x) for x in row])
            
    elif format_type == 'markdown':
        log_out("| " + " | ".join(header_keys) + " |")
        log_out("|" + "|".join(["---"] * len(header_keys)) + "|")
        for index, item in enumerate(all_items, start=1):
            row = [
                index,
                item.get('goodsId', ''),
                item.get('sourceType', ''),
                item.get('title', ''),
                item.get('shopName', ''),
                item.get('actualPrice', ''),
                item.get('originalPrice', ''),
                item.get('couponPrice', ''),
                item.get('monthSales', '')
            ]
            
            # Markdown 渲染须防干扰：过滤文本中的管线符与换行
            def escape_md(val):
                s = to_str(val)
                return s.replace("|", "&#124;").replace("\n", " ").replace("\r", "")
                
            escaped_row = [escape_md(x) for x in row]
            log_out("| " + " | ".join(escaped_row) + " |")


def get_product_link(goods_id, source_type):
    """
    接口2：获取商品链接并以 Key: Value 格式输出
    """
    url = 'https://msapi.maishou88.com/api/v1/share/getTargetUrl'
    headers = get_common_headers(host='msapi.maishou88.com', content_type='application/json')
    
    inviteCode = os.environ.get("INVITE_CODE", "46608499")
    data = {
        "goodsId": goods_id,
        "sourceType": str(source_type),
        "inviteCode": inviteCode,
        "supplierCode": "",
        "activityId": "",
        "isShare": "1",
        "token": "",
        "isDirectDetail": 0
    }
    
    encoded_data = json.dumps(data).encode('utf-8')
    
    try:
        res_json = send_request(url, encoded_data, headers)
        if res_json.get('status') == 'success' and 'data' in res_json:
            link_data = res_json['data']
            
            # 获取链接：appUrl -> schemaUrl -> 空
            app_url = link_data.get('appUrl')
            schema_url = link_data.get('schemaUrl')
            final_url = app_url if app_url else (schema_url if schema_url else "")
            
            # 获取口令
            kl = link_data.get('kl', "")
            
            log_out("链接：" + str(final_url))
            log_out("口令：" + str(kl))
        else:
            log_err("接口返回错误: {}".format(res_json.get('message', '未知错误')))
    except Exception as e:
        log_err("请求失败: {}".format(str(e)))


def main():
    parser = argparse.ArgumentParser(description="商品检索与链接获取工具")
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    search_parser = subparsers.add_parser('search', help='检索商品列表')
    search_parser.add_argument('--keyword', required=True, help='搜索关键字')
    search_parser.add_argument('--sourceType', default='0', help='来源平台类型 (默认: 0)')
    search_parser.add_argument('--pages', default='1', help='页码，多个用逗号隔开 (例如: 1 或 1,2,3)')
    search_parser.add_argument('--sort', default='', help='结果重新排序方式，传入 "price" 表示按价格排序 (默认: 不排序)')
    search_parser.add_argument('--format', default='csv', choices=['csv', 'markdown'], help='输出格式化，支持 csv 或 markdown (默认: csv)')
    
    link_parser = subparsers.add_parser('link', help='获取商品链接')
    link_parser.add_argument('--goodsId', required=True, help='商品ID (从search中获取)')
    link_parser.add_argument('--sourceType', required=True, help='来源平台类型 (例如: 1)')
    
    args = parser.parse_args()
    
    if args.command == 'search':
        search_products(args.keyword, args.sourceType, args.pages, args.sort, args.format)
    elif args.command == 'link':
        get_product_link(args.goodsId, args.sourceType)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()