#!/usr/bin/env python3
"""
卖家精灵 MCP 封装模块

使用 mcporter 调用卖家精灵 MCP 服务
安装: npm install -g mcporter
配置: mcporter config add sellersprite-mcp https://mcp.sellersprite.com/mcp?secret-key=你的密钥

文档: https://open.sellersprite.com/mcp/43
"""

import json
import subprocess
import re
from typing import Optional, Dict, Any, List

def run_mcporter(command: str) -> Dict[str, Any]:
    """执行 mcporter 命令并返回解析后的 JSON"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            encoding='utf-8',
            errors='replace',
            timeout=30
        )
        stdout = result.stdout
        if not stdout:
            return {"code": "ERROR", "message": "No output from API"}
        
        # Parse JSON
        data = json.loads(stdout)
        
        # Ensure message is ASCII-safe
        if "message" in data and data["message"]:
            # Replace non-ASCII characters
            msg = data["message"]
            data["message"] = msg.encode('ascii', 'replace').decode('ascii')
        
        return data
    except subprocess.TimeoutExpired:
        return {"code": "ERROR", "message": "Command timed out"}
    except json.JSONDecodeError as e:
        return {"code": "ERROR", "message": "JSON parse error"}


class SellerSpriteMCP:
    """卖家精灵 MCP 客户端"""

    def __init__(self, server_name: str = "sellersprite-mcp"):
        self.server = server_name

    def _call(self, tool: str, **kwargs) -> Dict[str, Any]:
        """调用 MCP 工具"""
        args = " ".join([f'{k}: "{v}"' if isinstance(v, str) else f'{k}: {v}'
                         for k, v in kwargs.items()])
        cmd = f'mcporter call {self.server}.{tool} {args}'
        return run_mcporter(cmd)

    # ============ 关键词 APIs ============

    def keyword_research(self, keyword: str, marketplace: str = "US",
                         page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """关键词选品/挖掘"""
        return self._call("keyword_research",
                         marketplace=marketplace, keyword=keyword,
                         page=page, pageSize=page_size)

    def keyword_miner(self, keyword: str, marketplace: str = "US",
                     page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """关键词挖掘"""
        return self._call("keyword_miner",
                         marketplace=marketplace, keyword=keyword,
                         page=page, pageSize=page_size)

    def traffic_keyword(self, asin: str, marketplace: str = "US") -> Dict[str, Any]:
        """关键词反查(流量词列表)"""
        return self._call("traffic_keyword",
                         marketplace=marketplace, asin=asin)

    def traffic_keyword_stat(self, keyword: str, marketplace: str = "US") -> Dict[str, Any]:
        """流量词统计"""
        return self._call("traffic_keyword_stat",
                         marketplace=marketplace, keyword=keyword)

    # ============ ASIN APIs ============

    def asin_detail(self, asin: str, marketplace: str = "US") -> Dict[str, Any]:
        """ASIN 详情"""
        return self._call("asin_detail", marketplace=marketplace, asin=asin)

    def asin_prediction(self, asin: str, marketplace: str = "US") -> Dict[str, Any]:
        """ASIN 销量预测"""
        return self._call("asin_prediction", marketplace=marketplace, asin=asin)

    def review(self, asin: str, marketplace: str = "US",
               page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """评论数据"""
        return self._call("review",
                         marketplace=marketplace, asin=asin,
                         page=page, pageSize=page_size)

    def keepa_info(self, asin: str, marketplace: str = "US") -> Dict[str, Any]:
        """ASIN 历史趋势 (Keepa)"""
        return self._call("keepa_info", marketplace=marketplace, asin=asin)

    # ============ 市场 APIs ============

    def market_research(self, keyword: str, marketplace: str = "US") -> Dict[str, Any]:
        """市场调研"""
        return self._call("market_research", marketplace=marketplace, keyword=keyword)

    def market_research_statistics(self, keyword: str, marketplace: str = "US") -> Dict[str, Any]:
        """市场统计"""
        return self._call("market_research_statistics",
                         marketplace=marketplace, keyword=keyword)

    def market_brand_concentration(self, node_id_path: str,
                                   marketplace: str = "US",
                                   top_n: int = 10) -> Dict[str, Any]:
        """品牌集中度"""
        return self._call("market_brand_concentration",
                         marketplace=marketplace, nodeIdPath=node_id_path, topN=top_n)

    def market_price_distribution(self, node_id_path: str,
                                  marketplace: str = "US",
                                  top_n: int = 50) -> Dict[str, Any]:
        """价格分布"""
        return self._call("market_price_distribution",
                         marketplace=marketplace, nodeIdPath=node_id_path, topN=top_n)

    def market_product_concentration(self, node_id_path: str,
                                     marketplace: str = "US",
                                     top_n: int = 50) -> Dict[str, Any]:
        """商品集中度"""
        return self._call("market_product_concentration",
                         marketplace=marketplace, nodeIdPath=node_id_path, topN=top_n)

    def market_seller_country_distribution(self, node_id_path: str,
                                          marketplace: str = "US") -> Dict[str, Any]:
        """卖家所属地分布"""
        return self._call("market_seller_country_distribution",
                         marketplace=marketplace, nodeIdPath=node_id_path)

    def market_seller_type_concentration(self, node_id_path: str,
                                         marketplace: str = "US") -> Dict[str, Any]:
        """卖家类型集中度"""
        return self._call("market_seller_type_concentration",
                         marketplace=marketplace, nodeIdPath=node_id_path)

    # ============ 竞品 APIs ============

    def competitor_lookup(self, keyword: str, marketplace: str = "US",
                          page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """竞品列表"""
        return self._call("competitor_lookup",
                         marketplace=marketplace, keyword=keyword,
                         page=page, pageSize=page_size)

    def product_research(self, keyword: str, marketplace: str = "US",
                         page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """产品调研"""
        return self._call("product_research",
                         marketplace=marketplace, keyword=keyword,
                         page=page, pageSize=page_size)

    def product_node(self, keyword: str, marketplace: str = "US") -> Dict[str, Any]:
        """产品类目信息"""
        return self._call("product_node", marketplace=marketplace, keyword=keyword)

    # ============ BSR/趋势 APIs ============

    def bsr_prediction(self, node_id_path: str, marketplace: str = "US") -> Dict[str, Any]:
        """BSR 销量预测"""
        return self._call("bsr_prediction",
                         marketplace=marketplace, nodeIdPath=node_id_path)

    def market_product_demand_trend(self, node_id_path: str,
                                   marketplace: str = "US") -> Dict[str, Any]:
        """商品需求趋势"""
        return self._call("market_product_demand_trend",
                         marketplace=marketplace, nodeIdPath=node_id_path)

    # ============ ABA 数据 ============

    def aba_research_weekly(self, keyword: str, marketplace: str = "US") -> Dict[str, Any]:
        """ABA 数据选品(按周)"""
        return self._call("aba_research_weekly", marketplace=marketplace, keyword=keyword)

    def aba_research_monthly(self, keyword: str, marketplace: str = "US") -> Dict[str, Any]:
        """ABA 数据选品(按月)"""
        return self._call("aba_research_monthly", marketplace=marketplace, keyword=keyword)

    # ============ 流量 APIs ============

    def traffic_source(self, asin: str, marketplace: str = "US") -> Dict[str, Any]:
        """流量来源"""
        return self._call("traffic_source", marketplace=marketplace, asin=asin)

    def traffic_extend(self, asin: str, marketplace: str = "US") -> Dict[str, Any]:
        """拓展流量词"""
        return self._call("traffic_extend", marketplace=marketplace, asin=asin)

    def traffic_listing(self, asin: str, marketplace: str = "US") -> Dict[str, Any]:
        """流量列表"""
        return self._call("traffic_listing", marketplace=marketplace, asin=asin)

    def traffic_listing_stat(self, keyword: str, marketplace: str = "US") -> Dict[str, Any]:
        """列表流量统计"""
        return self._call("traffic_listing_stat", marketplace=marketplace, keyword=keyword)


def main():
    """测试示例"""
    client = SellerSpriteMCP()

    # 测试关键词搜索
    print("=== 关键词选品测试 ===")
    result = client.keyword_research(keyword="laptop stand", marketplace="US", page=1, page_size=5)
    print(f"code: {result.get('code')}")
    if result.get('code') == 'OK':
        items = result.get('data', {}).get('items', [])
        print(f"找到 {len(items)} 个关键词")
        for item in items[:3]:
            print(f"  - {item.get('keywords')}: 搜索量 {item.get('searches')}")
    else:
        print(f"错误: {result.get('message')}")


if __name__ == "__main__":
    main()
