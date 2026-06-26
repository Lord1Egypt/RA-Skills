#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票热度排名采集器 - Python版
A-Share Heat Rank Collector - Python Version

采集问财、雪球、东方财富三大平台人气榜单，计算复合热度分数
"""

import argparse
import gzip
import json
import os
import random
import re
import string
import subprocess
import sys
import time
import urllib.parse
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

import requests


@dataclass
class StockRank:
    """股票排名信息"""
    code: str
    name: str
    rank: int
    heat_score: int
    source: str


@dataclass
class CompositeRank:
    """复合排名"""
    code: str
    name: str = ""
    wencai_rank: int = 0
    xueqiu_rank: int = 0
    eastmoney_rank: int = 0
    composite_score: float = 0.0
    appear_count: int = 0


def rand_string(n: int) -> str:
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))


class WencaiClient:
    """问财客户端"""

    def __init__(self):
        self.session = requests.Session()
        self.other_uid = f"Ths_iwencai_Xuangu_{rand_string(32)}"
        self.cookies = {
            'other_uid': self.other_uid,
            'ta_random_userid': rand_string(10),
            'v': ''
        }
        self.js_path = self._find_js_path()

    def _find_js_path(self) -> str:
        """查找hexin_v.js路径"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        js_path = os.path.join(script_dir, 'lib', 'hexin_v.js')
        if os.path.exists(js_path):
            return js_path
        js_path = os.path.join(script_dir, '..', 'stock-heat-rank', 'lib', 'hexin_v.js')
        if os.path.exists(js_path):
            return js_path
        return 'lib/hexin_v.js'

    def _generate_hexin_v(self) -> str:
        """生成Hexin-V签名"""
        timestamp = f"{time.time():.3f}"
        try:
            result = subprocess.run(
                ['node', self.js_path, timestamp],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip()
        except Exception:
            return "default_hexin_v_value"

    def _visit_main(self):
        """访问主页获取初始cookies"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        try:
            resp = self.session.get('https://www.iwencai.com', headers=headers, timeout=15)
            for cookie in resp.cookies:
                self.cookies[cookie.name] = cookie.value
        except Exception:
            pass

    def _visit_search(self):
        """访问搜索页"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.iwencai.com',
        }
        try:
            resp = self.session.get('https://www.iwencai.com/unifiedwap/home/index', headers=headers, timeout=15)
            for cookie in resp.cookies:
                self.cookies[cookie.name] = cookie.value
        except Exception:
            pass

    def _visit_hint(self):
        """初始化会话"""
        hexin_v = self._generate_hexin_v()
        # 更新cookies中的v值为hexin_v
        self.cookies['v'] = hexin_v
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Origin': 'https://www.iwencai.com',
            'Referer': 'https://www.iwencai.com/unifiedwap/home/index',
            'Hexin-V': hexin_v,
        }
        data = {
            'dataType': 'history',
            'isAll': '1',
            'num': '20',
            'queryType': 'index',
            'relatedId': '',
        }
        try:
            resp = self.session.post(
                'https://www.iwencai.com/unifiedwap/suggest/V1/index/query-hint-list',
                headers=headers,
                data=data,
                cookies=self.cookies,
                timeout=15
            )
        except Exception:
            pass

    def fetch(self, top: int = 50) -> List[StockRank]:
        """获取问财人气排名"""
        print("→ 访问问财主页...")
        self._visit_main()
        time.sleep(0.3)

        print("→ 访问搜索页...")
        self._visit_search()
        time.sleep(0.3)

        print("→ 初始化会话...")
        self._visit_hint()
        time.sleep(0.3)

        print("→ 获取人气排名数据...")
        return self._get_data(top)

    def _get_data(self, top: int) -> List[StockRank]:
        """获取排名数据"""
        query = f"人气排名前{top}"
        payload = {
            "source": "Ths_iwencai_Xuangu",
            "version": "2.0",
            "query_area": "",
            "block_list": "",
            "add_info": '{"urp":{"scene":1,"company":1,"business":1},"contentType":"json","searchInfo":true}',
            "question": query,
            "perpage": top,
            "page": 1,
            "secondary_intent": "",
            "log_info": '{"input_type":"typewrite"}',
            "rsh": self.other_uid,
        }

        hexin_v = self._generate_hexin_v()
        # 更新cookies中的v值为hexin_v
        self.cookies['v'] = hexin_v

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Origin': 'https://www.iwencai.com',
            'Referer': f'https://www.iwencai.com/unifiedwap/result?w={urllib.parse.quote(query)}',
            'Hexin-V': hexin_v,
        }

        try:
            resp = self.session.post(
                'https://www.iwencai.com/customized/chart/get-robot-data',
                headers=headers,
                json=payload,
                cookies=self.cookies,
                timeout=30
            )
            return self._parse_response(resp.json(), top)
        except Exception as e:
            raise Exception(f"请求失败: {e}")

    def _parse_response(self, data: dict, top: int) -> List[StockRank]:
        """解析响应数据"""
        # 检查响应状态 - 可能是errno或status_code
        status = data.get('errno', data.get('status_code', -1))
        if status != 0:
            raise Exception(f"问财返回错误码: {status}")

        ranks = []
        try:
            # 尝试解析数据
            answer = data.get('data', {}).get('answer', [])
            if not answer:
                raise Exception("answer为空")
            
            txt_list = answer[0].get('txt', [])
            if not txt_list:
                raise Exception("txt为空")
            
            content = txt_list[0].get('content', {})
            components = content.get('components', [])
            if not components:
                raise Exception("components为空")
            
            datas = components[0].get('data', {}).get('datas', [])
            if not datas:
                raise Exception("datas为空")
            
            for i, item in enumerate(datas[:top]):
                code = item.get('股票代码', item.get('code', item.get('stockCode', '')))
                name = item.get('股票简称', item.get('name', item.get('stockName', '')))
                if code and name:
                    ranks.append(StockRank(
                        code=str(code),
                        name=str(name),
                        rank=i + 1,
                        heat_score=top - i,
                        source='wencai'
                    ))
        except (KeyError, IndexError) as e:
            raise Exception(f"解析失败: {e}")

        if not ranks:
            raise Exception("未解析到数据，可能需要更新反爬策略")
        return ranks


class XueqiuFetcher:
    """雪球热榜采集器"""

    def __init__(self):
        self.session = requests.Session()

    def fetch(self) -> List[StockRank]:
        """获取雪球热榜A股前50"""
        html = self._fetch_page()
        ranks = self._parse_html(html)
        if not ranks:
            raise Exception("未能从页面解析到股票数据")
        return ranks

    def _fetch_page(self) -> str:
        """获取页面HTML"""
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        resp = self.session.get('https://xueqiu.com/hot/stock', headers=headers, timeout=15)
        return resp.text

    def _parse_html(self, html: str) -> List[StockRank]:
        """解析HTML获取股票数据"""
        ranks = []
        pattern = re.compile(r'"name":"([^"]+)","value":[^}]*"symbol":"(SH|SZ)(\d+)"')
        seen = set()

        for match in pattern.finditer(html):
            name, market, code = match.groups()
            full_code = market + code
            if full_code in seen or len(ranks) >= 50:
                continue
            seen.add(full_code)

            ranks.append(StockRank(
                code=code,
                name=name,
                rank=len(ranks) + 1,
                heat_score=100 - len(ranks),
                source='xueqiu'
            ))

        return ranks


class EastmoneyFetcher:
    """东方财富人气排名采集器"""

    def __init__(self):
        self.session = requests.Session()

    def fetch(self) -> List[StockRank]:
        """获取东方财富人气排名前50"""
        return self._get_rank_data()

    def _get_rank_data(self) -> List[StockRank]:
        """获取排名数据"""
        url = "https://emappdata.eastmoney.com/stockrank/getAllCurrentList"
        payload = {
            "appId": "stockrank",
            "globalId": "786e4c21-70dc-435a-93bb-38",
            "marketType": "",
            "rankType": "1",
            "pageNo": 1,
            "pageSize": 100,
            "fromDate": "",
            "toDate": "",
            "stockIndustry": "",
            "stockCode": "",
            "stockName": "",
            "clientSource": "web",
            "clientVersion": "1.0.0",
        }
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': 'application/json',
            'Origin': 'https://vipmoney.eastmoney.com',
            'Referer': 'https://vipmoney.eastmoney.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        resp = self.session.post(url, json=payload, headers=headers, timeout=15)
        data = resp.json()

        return self._parse_response(data)

    def _parse_response(self, data: dict) -> List[StockRank]:
        """解析响应数据"""
        if data.get('status', -1) != 0:
            raise Exception(f"API返回错误: status={data.get('status')}")

        ranks = []
        for item in data.get('data', [])[:50]:
            sc = item.get('sc', '')
            if len(sc) < 8:
                continue
            code = sc[2:]  # 去掉前缀

            ranks.append(StockRank(
                code=code,
                name='',
                rank=item.get('rk', len(ranks) + 1),
                heat_score=100 - len(ranks),
                source='eastmoney'
            ))

        return ranks


def normalize_code(code: str) -> str:
    """标准化股票代码"""
    if len(code) == 6:
        return validate_a_stock_code(code)
    if len(code) == 8 and code[:2] in ('SH', 'SZ'):
        return validate_a_stock_code(code[2:])
    if len(code) == 9 and code[6:] in ('.SH', '.SZ'):
        return validate_a_stock_code(code[:6])
    return ''


def validate_a_stock_code(code: str) -> str:
    """验证A股代码"""
    if len(code) != 6 or not code.isdigit():
        return ''
    first = code[0]
    if first not in ('6', '0', '3', '8', '4'):
        return ''
    return code


def calculate_composite(wencai: List[StockRank], xueqiu: List[StockRank], eastmoney: List[StockRank]) -> List[CompositeRank]:
    """计算复合热度"""
    stock_map: Dict[str, CompositeRank] = {}

    # 处理问财数据
    for r in wencai:
        code = normalize_code(r.code)
        if not code:
            continue
        if code not in stock_map:
            stock_map[code] = CompositeRank(code=code, name=r.name)
        stock_map[code].wencai_rank = r.rank
        stock_map[code].appear_count += 1

    # 处理雪球数据
    for r in xueqiu:
        code = normalize_code(r.code)
        if not code:
            continue
        if code not in stock_map:
            stock_map[code] = CompositeRank(code=code, name=r.name)
        stock_map[code].xueqiu_rank = r.rank
        stock_map[code].appear_count += 1

    # 处理东财数据
    for r in eastmoney:
        code = normalize_code(r.code)
        if not code:
            continue
        if code not in stock_map:
            stock_map[code] = CompositeRank(code=code, name=r.name)
        if not stock_map[code].name and r.name:
            stock_map[code].name = r.name
        stock_map[code].eastmoney_rank = r.rank
        stock_map[code].appear_count += 1

    # 计算复合得分
    for stock in stock_map.values():
        score = 0.0
        if stock.wencai_rank > 0:
            score += 100 - stock.wencai_rank
        if stock.xueqiu_rank > 0:
            score += 100 - stock.xueqiu_rank
        if stock.eastmoney_rank > 0:
            score += 100 - stock.eastmoney_rank

        if stock.appear_count == 2:
            score += 20
        elif stock.appear_count == 3:
            score += 50

        stock.composite_score = score / 3.5

    # 排序
    return sorted(stock_map.values(), key=lambda x: x.composite_score, reverse=True)


def print_table(ranks: List[CompositeRank], top: int):
    """打印表格"""
    print()
    print("┌──────┬──────────┬────────────┬──────┬──────┬──────┬──────────┬──────┐")
    print("│ 排名 │   代码   │    名称    │ 问财 │ 雪球 │ 东财 │  热度分  │ 出现 │")
    print("├──────┼──────────┼────────────┼──────┼──────┼──────┼──────────┼──────┤")

    for i, r in enumerate(ranks[:top]):
        wc = str(r.wencai_rank) if r.wencai_rank > 0 else "-"
        xq = str(r.xueqiu_rank) if r.xueqiu_rank > 0 else "-"
        em = str(r.eastmoney_rank) if r.eastmoney_rank > 0 else "-"

        print(f"│ {i+1:4d} │ {r.code:8s} │ {r.name:10s} │ {wc:>4s} │ {xq:>4s} │ {em:>4s} │ {r.composite_score:8.1f} │ {r.appear_count:4d} │")

    print("└──────┴──────────┴────────────┴──────┴──────┴──────┴──────────┴──────┘")
    print()


def print_json(ranks: List[CompositeRank], top: int):
    """打印JSON"""
    result = []
    for i, r in enumerate(ranks[:top]):
        result.append({
            "rank": i + 1,
            "code": r.code,
            "name": r.name,
            "wencai_rank": r.wencai_rank if r.wencai_rank > 0 else None,
            "xueqiu_rank": r.xueqiu_rank if r.xueqiu_rank > 0 else None,
            "eastmoney_rank": r.eastmoney_rank if r.eastmoney_rank > 0 else None,
            "composite_score": round(r.composite_score, 1),
            "appear_count": r.appear_count,
        })
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description='股票热度排名采集器 - Python版')
    parser.add_argument('--top', type=int, default=50, help='获取前N名 (默认: 50)')
    parser.add_argument('--format', choices=['table', 'json'], default='table', help='输出格式 (默认: table)')
    args = parser.parse_args()

    print("=== 股票热度排名采集器 ===")
    print(f"采集时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 采集问财数据
    print("【问财】正在采集...")
    wencai_ranks = []
    try:
        client = WencaiClient()
        wencai_ranks = client.fetch(50)
        print(f"  成功获取 {len(wencai_ranks)} 只股票")
    except Exception as e:
        print(f"  采集失败: {e}")

    # 采集雪球数据
    print("\n【雪球】正在采集...")
    xueqiu_ranks = []
    try:
        fetcher = XueqiuFetcher()
        xueqiu_ranks = fetcher.fetch()
        print(f"  成功获取 {len(xueqiu_ranks)} 只A股")
    except Exception as e:
        print(f"  采集失败: {e}")

    # 采集东财数据
    print("\n【东财】正在采集...")
    eastmoney_ranks = []
    try:
        fetcher = EastmoneyFetcher()
        eastmoney_ranks = fetcher.fetch()
        print(f"  成功获取 {len(eastmoney_ranks)} 只股票")
    except Exception as e:
        print(f"  采集失败: {e}")

    # 计算复合热度
    print("\n=== 复合热度排名 ===")
    print(f"问财: {len(wencai_ranks)} | 雪球: {len(xueqiu_ranks)} | 东财: {len(eastmoney_ranks)}")

    result = calculate_composite(wencai_ranks, xueqiu_ranks, eastmoney_ranks)

    if args.format == 'json':
        print_json(result, args.top)
    else:
        print_table(result, args.top)


if __name__ == '__main__':
    main()