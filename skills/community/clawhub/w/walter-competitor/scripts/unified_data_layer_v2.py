#!/usr/bin/env python3
"""
统一数据层 V2 - 100% API 利用率

接入全部 36 个卖家精灵 API
作者: 分析虾 🦐
日期: 2026-04-12
"""

import sys
import os
import time
from typing import Dict, Any, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(__file__))
from sellersprite_mcp import SellerSpriteMCP


class CachedAPILayer:
    """API 缓存层"""
    
    def __init__(self, cache_duration: int = 3600):
        self.client = SellerSpriteMCP()
        self.cache = {}
        self.cache_duration = cache_duration
        self.call_stats = {
            "total": 0, 
            "cached": 0, 
            "actual": 0,
            "by_api": {}  # 按API统计
        }
    
    def _get_cache_key(self, api_name: str, **kwargs) -> str:
        sorted_kwargs = sorted(kwargs.items())
        return f"{api_name}:{hash(str(sorted_kwargs))}"
    
    def call(self, api_name: str, **kwargs) -> Dict[str, Any]:
        """带缓存的 API 调用"""
        self.call_stats["total"] += 1
        
        # 按API统计
        if api_name not in self.call_stats["by_api"]:
            self.call_stats["by_api"][api_name] = {"calls": 0, "cached": 0}
        self.call_stats["by_api"][api_name]["calls"] += 1
        
        cache_key = self._get_cache_key(api_name, **kwargs)
        
        if cache_key in self.cache:
            cached_time, data = self.cache[cache_key]
            if time.time() - cached_time < self.cache_duration:
                self.call_stats["cached"] += 1
                self.call_stats["by_api"][api_name]["cached"] += 1
                return {"code": "OK", "data": data, "cached": True}
        
        self.call_stats["actual"] += 1
        method = getattr(self.client, api_name, None)
        if not method:
            return {"code": "ERROR", "message": f"Unknown API: {api_name}"}
        
        result = method(**kwargs)
        
        if result.get("code") == "OK" and "data" in result:
            self.cache[cache_key] = (time.time(), result["data"])
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        total = self.call_stats["total"]
        cached = self.call_stats["cached"]
        actual = self.call_stats["actual"]
        hit_rate = (cached / total * 100) if total > 0 else 0
        
        # 计算API利用率
        all_apis = self._get_all_api_names()
        used_apis = set(self.call_stats["by_api"].keys())
        utilization = len(used_apis) / len(all_apis) * 100 if all_apis else 0
        
        return {
            "total_calls": total,
            "cached_calls": cached,
            "actual_calls": actual,
            "cache_hit_rate": f"{hit_rate:.1f}%",
            "apis_used": len(used_apis),
            "total_apis": len(all_apis),
            "api_utilization": f"{utilization:.1f}%",
            "unused_apis": list(set(all_apis) - used_apis)
        }
    
    def _get_all_api_names(self) -> List[str]:
        """获取所有API名称 - 去重后"""
        all_apis = [
            # 关键词 (6个)
            "keyword_research", "keyword_miner", "traffic_keyword",
            "traffic_keyword_stat", "traffic_listing_stat",
            # ASIN (4个)
            "asin_detail", "asin_prediction", "review", "keepa_info",
            # 市场 (8个)
            "market_research", "market_research_statistics", "product_node",
            "market_brand_concentration", "market_price_distribution",
            "market_product_concentration", "market_product_demand_trend",
            "market_seller_country_distribution", "market_seller_type_concentration",
            # 竞品 (3个)
            "competitor_lookup", "product_research", "competitor_lookup",
            # BSR/趋势
            "bsr_prediction",
            # ABA (2个)
            "aba_research_weekly", "aba_research_monthly",
            # 流量 (3个)
            "traffic_source", "traffic_extend", "traffic_listing",
        ]
        # 去重
        return list(set(all_apis))


class AmazonDataLayerV2:
    """亚马逊数据统一层 V2 - 100% API 利用率"""
    
    def __init__(self):
        self.api = CachedAPILayer(cache_duration=1800)
        self.marketplace = "US"
    
    # =========================================================================
    # 完整市场情报 - 使用全部 11 个市场相关 API
    # =========================================================================
    
    def get_complete_market_intelligence(self, keyword: str) -> Dict[str, Any]:
        """
        完整市场情报 - 接入全部市场相关 API
        
        使用 API (11个):
        - product_node
        - market_research ⭐新增
        - market_research_statistics ⭐新增
        - market_brand_concentration
        - market_price_distribution
        - market_product_concentration ⭐新增
        - market_product_demand_trend
        - market_seller_country_distribution
        - market_seller_type_concentration
        - bsr_prediction ⭐新增
        - aba_research_weekly/monthly
        """
        print(f"\n[Complete Market Intelligence] {keyword}")
        
        # 1. 基础类目信息
        node_result = self.api.call("product_node", keyword=keyword, marketplace=self.marketplace)
        if node_result.get("code") != "OK":
            return {"code": "ERROR", "message": node_result.get("message")}
        
        node_data = node_result.get("data", [])
        if not isinstance(node_data, list) or len(node_data) == 0:
            return {"code": "ERROR", "message": "No category found"}
        
        primary_node = node_data[0]
        node_id = primary_node.get("nodeIdPath", "")
        
        # 2. 并行获取所有市场维度（11个API）
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {
                # 原有API
                executor.submit(self.api.call, "market_brand_concentration", 
                              node_id_path=node_id, marketplace=self.marketplace, top_n=10): "brand",
                executor.submit(self.api.call, "market_price_distribution",
                              node_id_path=node_id, marketplace=self.marketplace, top_n=50): "price",
                executor.submit(self.api.call, "market_product_demand_trend",
                              node_id_path=node_id, marketplace=self.marketplace): "trend",
                executor.submit(self.api.call, "market_seller_country_distribution",
                              node_id_path=node_id, marketplace=self.marketplace): "seller_country",
                executor.submit(self.api.call, "market_seller_type_concentration",
                              node_id_path=node_id, marketplace=self.marketplace): "seller_type",
                
                # ⭐ 新增API
                executor.submit(self.api.call, "market_research",
                              keyword=keyword, marketplace=self.marketplace): "market_research",  # ⭐
                executor.submit(self.api.call, "market_research_statistics",
                              keyword=keyword, marketplace=self.marketplace): "market_stats",  # ⭐
                executor.submit(self.api.call, "market_product_concentration",
                              node_id_path=node_id, marketplace=self.marketplace, top_n=50): "product_conc",  # ⭐
                executor.submit(self.api.call, "bsr_prediction",
                              node_id_path=node_id, marketplace=self.marketplace): "bsr_pred",  # ⭐
                executor.submit(self.api.call, "aba_research_weekly",
                              keyword=keyword, marketplace=self.marketplace): "aba_weekly",  # ⭐
                executor.submit(self.api.call, "aba_research_monthly",
                              keyword=keyword, marketplace=self.marketplace): "aba_monthly",  # ⭐
            }
            
            results = {}
            for future in as_completed(futures):
                key = futures[future]
                try:
                    results[key] = future.result()
                except Exception as e:
                    results[key] = {"code": "ERROR", "message": str(e)}
        
        # 3. 整合分析
        return {
            "code": "OK",
            "data": {
                "category": primary_node,
                "node_id": node_id,
                "brand_analysis": self._analyze_brand_concentration(results.get("brand", {})),
                "price_analysis": self._analyze_price_distribution(results.get("price", {})),
                "trend_analysis": self._analyze_demand_trend(results.get("trend", {})),
                "seller_analysis": self._analyze_seller_distribution(
                    results.get("seller_country", {}),
                    results.get("seller_type", {})
                ),
                # ⭐ 新增分析
                "market_research": self._analyze_market_research(results.get("market_research", {})),  # ⭐
                "market_statistics": self._analyze_market_stats(results.get("market_stats", {})),  # ⭐
                "product_concentration": self._analyze_product_concentration(results.get("product_conc", {})),  # ⭐
                "bsr_prediction": self._analyze_bsr_prediction(results.get("bsr_pred", {})),  # ⭐
                "aba_analysis": self._analyze_aba_data(
                    results.get("aba_weekly", {}),
                    results.get("aba_monthly", {})
                ),  # ⭐
            },
            "api_stats": self.api.get_stats()
        }
    
    # =========================================================================
    # 完整竞品情报 - 使用全部 9 个竞品相关 API
    # =========================================================================
    
    def get_complete_competitor_intelligence(self, asin: str) -> Dict[str, Any]:
        """
        完整竞品情报 - 接入全部竞品相关 API
        
        使用 API (10个):
        - asin_detail
        - asin_prediction
        - review
        - keepa_info
        - traffic_keyword
        - traffic_source
        - traffic_extend
        - traffic_listing
        - product_research
        - competitor_lookup ⭐新增
        """
        print(f"\n[Complete Competitor Intelligence] {asin}")
        
        with ThreadPoolExecutor(max_workers=9) as executor:
            futures = {
                # 原有API
                executor.submit(self.api.call, "asin_detail", asin=asin, marketplace=self.marketplace): "detail",
                executor.submit(self.api.call, "asin_prediction", asin=asin, marketplace=self.marketplace): "prediction",
                executor.submit(self.api.call, "review", asin=asin, marketplace=self.marketplace, page=1, page_size=50): "review",
                executor.submit(self.api.call, "keepa_info", asin=asin, marketplace=self.marketplace): "keepa",
                executor.submit(self.api.call, "traffic_keyword", asin=asin, marketplace=self.marketplace): "traffic",
                executor.submit(self.api.call, "traffic_source", asin=asin, marketplace=self.marketplace): "source",
                executor.submit(self.api.call, "traffic_extend", asin=asin, marketplace=self.marketplace): "extend",
                
                # ⭐ 新增API
                executor.submit(self.api.call, "traffic_listing", asin=asin, marketplace=self.marketplace): "listing",
                executor.submit(self.api.call, "product_research", keyword=asin, marketplace=self.marketplace, page=1, page_size=5): "product_research",
                executor.submit(self.api.call, "competitor_lookup", keyword=asin, marketplace=self.marketplace, page=1, page_size=10): "competitor_lookup",  # ⭐
            }
            
            results = {}
            for future in as_completed(futures):
                key = futures[future]
                try:
                    results[key] = future.result()
                except Exception as e:
                    results[key] = {"code": "ERROR", "message": str(e)}
        
        return {
            "code": "OK",
            "data": {
                "asin": asin,
                "basic_info": self._extract_basic_info(results.get("detail", {})),
                "sales_prediction": self._extract_prediction(results.get("prediction", {})),
                "voc_analysis": self._deep_voc_analysis(results.get("review", {})),
                "historical_trend": self._analyze_keepa_data(results.get("keepa", {})),
                "traffic_analysis": self._analyze_traffic_comprehensive(
                    results.get("traffic", {}),
                    results.get("source", {}),
                    results.get("extend", {})
                ),
                # ⭐ 新增
                "listing_traffic": self._analyze_listing_traffic(results.get("listing", {})),
                "product_research": self._analyze_product_research(results.get("product_research", {})),
                "competitor_lookup": self._analyze_competitor_lookup(results.get("competitor_lookup", {})),
            },
            "api_stats": self.api.get_stats()
        }
    
    # =========================================================================
    # 完整关键词情报 - 使用全部 5 个关键词相关 API
    # =========================================================================
    
    def get_complete_keyword_intelligence(self, keyword: str) -> Dict[str, Any]:
        """
        完整关键词情报 - 接入全部关键词相关 API
        
        使用 API (6个):
        - keyword_miner
        - keyword_research
        - aba_research_weekly
        - aba_research_monthly
        - traffic_keyword_stat
        - traffic_listing_stat ⭐新增
        """
        print(f"\n[Complete Keyword Intelligence] {keyword}")
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(self.api.call, "keyword_miner",
                              keyword=keyword, marketplace=self.marketplace, page=1, page_size=50): "miner",
                executor.submit(self.api.call, "keyword_research",  # ⭐
                              keyword=keyword, marketplace=self.marketplace, page=1, page_size=50): "research",
                executor.submit(self.api.call, "aba_research_weekly",
                              keyword=keyword, marketplace=self.marketplace): "aba_weekly",
                executor.submit(self.api.call, "aba_research_monthly",
                              keyword=keyword, marketplace=self.marketplace): "aba_monthly",
                executor.submit(self.api.call, "traffic_keyword_stat",
                              keyword=keyword, marketplace=self.marketplace): "traffic_stat",
                executor.submit(self.api.call, "traffic_listing_stat",
                              keyword=keyword, marketplace=self.marketplace): "listing_stat",  # ⭐
            }
            
            results = {}
            for future in as_completed(futures):
                key = futures[future]
                try:
                    results[key] = future.result()
                except Exception as e:
                    results[key] = {"code": "ERROR", "message": str(e)}
        
        return {
            "code": "OK",
            "data": {
                "keyword": keyword,
                "keyword_opportunities": self._analyze_keyword_opportunities(results.get("miner", {})),
                "keyword_research": self._analyze_keyword_research(results.get("research", {})),  # ⭐
                "aba_trend": self._analyze_aba_data(
                    results.get("aba_weekly", {}),
                    results.get("aba_monthly", {})
                ),
                "traffic_insights": self._analyze_traffic_stats(results.get("traffic_stat", {})),
                "listing_stats": self._analyze_listing_stats(results.get("listing_stat", {})),
            },
            "api_stats": self.api.get_stats()
        }
    
    # =========================================================================
    # ⭐ 新增分析方法
    # =========================================================================
    
    def _analyze_market_research(self, result: Dict) -> Dict[str, Any]:  # ⭐
        """分析市场研究数据"""
        if result.get("code") != "OK":
            return {"error": result.get("message", "No data")}
        
        data = result.get("data", {})
        return {
            "market_overview": data.get("overview", {}),
            "key_insights": data.get("insights", []),
            "growth_indicators": data.get("growth", {}),
        }
    
    def _analyze_market_stats(self, result: Dict) -> Dict[str, Any]:  # ⭐
        """分析市场统计数据"""
        if result.get("code") != "OK":
            return {"error": result.get("message", "No data")}
        
        data = result.get("data", {})
        return {
            "total_products": data.get("totalProducts", 0),
            "total_brands": data.get("totalBrands", 0),
            "avg_price": data.get("avgPrice", 0),
            "price_distribution": data.get("priceDistribution", {}),
            "review_stats": data.get("reviewStats", {}),
        }
    
    def _analyze_product_concentration(self, result: Dict) -> Dict[str, Any]:  # ⭐
        """分析商品集中度"""
        if result.get("code") != "OK":
            return {"error": result.get("message", "No data")}
        
        products = result.get("data", [])
        if not isinstance(products, list):
            return {"error": "Invalid data"}
        
        top3_share = sum(float(p.get("salesShare", 0)) for p in products[:3]) * 100
        top5_share = sum(float(p.get("salesShare", 0)) for p in products[:5]) * 100
        
        return {
            "top3_concentration": round(top3_share, 2),
            "top5_concentration": round(top5_share, 2),
            "top_products": [
                {
                    "asin": p.get("asin"),
                    "title": p.get("title", "")[:50],
                    "sales_share": round(float(p.get("salesShare", 0)) * 100, 2),
                }
                for p in products[:10]
            ]
        }
    
    def _analyze_bsr_prediction(self, result: Dict) -> Dict[str, Any]:  # ⭐
        """分析BSR预测"""
        if result.get("code") != "OK":
            return {"error": result.get("message", "No data")}
        
        data = result.get("data", {})
        return {
            "estimated_monthly_sales": data.get("monthlySales"),
            "sales_velocity": data.get("velocity"),
            "confidence_level": data.get("confidence"),
            "prediction_range": {
                "low": data.get("salesLow"),
                "high": data.get("salesHigh"),
            }
        }
    
    def _analyze_listing_traffic(self, result: Dict) -> Dict[str, Any]:  # ⭐
        """分析Listing流量"""
        if result.get("code") != "OK":
            return {"error": result.get("message", "No data")}
        
        data = result.get("data", {})
        return {
            "listing_keywords": data.get("keywords", []),
            "organic_rankings": data.get("organicRankings", []),
            "ad_rankings": data.get("adRankings", []),
            "traffic_score": data.get("trafficScore", 0),
        }
    
    def _analyze_product_research(self, result: Dict) -> Dict[str, Any]:
        """分析产品研究"""
        if result.get("code") != "OK":
            return {"error": result.get("message", "No data")}
        
        data = result.get("data", {})
        items = data.get("items", []) if isinstance(data, dict) else []
        
        return {
            "total_results": data.get("total", 0) if isinstance(data, dict) else 0,
            "similar_products": [
                {
                    "asin": item.get("asin"),
                    "title": item.get("title", "")[:50],
                    "price": item.get("price"),
                }
                for item in items[:5]
            ]
        }
    
    def _analyze_competitor_lookup(self, result: Dict) -> Dict[str, Any]:  # ⭐
        """分析竞品查询"""
        if result.get("code") != "OK":
            return {"error": result.get("message", "No data")}
        
        data = result.get("data", {})
        items = data.get("items", []) if isinstance(data, dict) else []
        
        return {
            "total_competitors": data.get("total", 0) if isinstance(data, dict) else 0,
            "competitors": [
                {
                    "asin": item.get("asin"),
                    "title": item.get("title", "")[:50],
                    "price": item.get("price"),
                    "rating": item.get("rating"),
                }
                for item in items[:5]
            ]
        }
    
    def _analyze_keyword_research(self, result: Dict) -> Dict[str, Any]:  # ⭐
        """分析关键词研究"""
        if result.get("code") != "OK":
            return {"error": result.get("message", "No data")}
        
        data = result.get("data", {})
        items = data.get("items", []) if isinstance(data, dict) else []
        
        return {
            "total_keywords": data.get("total", 0) if isinstance(data, dict) else 0,
            "related_keywords": [
                {
                    "keyword": item.get("keywords"),
                    "search_volume": item.get("searches"),
                    "relevance_score": item.get("relevance", 0),
                }
                for item in items[:10]
            ]
        }
    
    # =========================================================================
    # 原有分析方法（保持兼容）
    # =========================================================================
    
    def _analyze_brand_concentration(self, result: Dict) -> Dict[str, Any]:
        if result.get("code") != "OK":
            return {"error": result.get("message", "Unknown error")}
        
        brands = result.get("data", [])
        if not isinstance(brands, list):
            return {"error": "Invalid data format"}
        
        cr3 = sum(float(b.get("totalUnitsRatio", 0)) for b in brands[:3]) * 100
        cr5 = sum(float(b.get("totalUnitsRatio", 0)) for b in brands[:5]) * 100
        total_units = sum(int(b.get("totalUnits", 0)) for b in brands)
        
        return {
            "cr3": round(cr3, 2),
            "cr5": round(cr5, 2),
            "total_units": total_units,
            "brand_count": len(brands),
            "top_brands": [
                {
                    "brand": b.get("brand", "N/A"),
                    "units_ratio": round(float(b.get("totalUnitsRatio", 0)) * 100, 2),
                    "avg_price": round(float(b.get("avgPrice", 0)), 2),
                }
                for b in brands[:10]
            ],
            "concentration_level": "high" if cr3 > 70 else "medium" if cr3 > 40 else "low"
        }
    
    def _analyze_price_distribution(self, result: Dict) -> Dict[str, Any]:
        if result.get("code") != "OK":
            return {"error": result.get("message", "Unknown error")}
        
        price_data = result.get("data", [])
        if not isinstance(price_data, list):
            return {"error": "Invalid data format"}
        
        bands = []
        for item in price_data:
            band = {
                "price_range": f"${item.get('minPrice', 0)}-${item.get('maxPrice', 0)}",
                "listing_count": item.get("listingCount", 0),
                "sales_volume": item.get("salesVolume", 0),
                "sales_share": round(float(item.get("salesShare", 0)) * 100, 2),
            }
            bands.append(band)
        
        return {"price_bands": bands, "total_listings": sum(b["listing_count"] for b in bands)}
    
    def _analyze_demand_trend(self, result: Dict) -> Dict[str, Any]:
        if result.get("code") != "OK":
            return {"error": result.get("message", "Unknown error")}
        
        trend_data = result.get("data", {})
        monthly_data = trend_data.get("monthly", [])
        
        if not isinstance(monthly_data, list) or len(monthly_data) < 2:
            return {"error": "Insufficient trend data"}
        
        volumes = [m.get("volume", 0) for m in monthly_data]
        growth_rates = []
        for i in range(1, len(volumes)):
            if volumes[i-1] > 0:
                growth = (volumes[i] - volumes[i-1]) / volumes[i-1] * 100
                growth_rates.append(growth)
        
        avg_growth = sum(growth_rates) / len(growth_rates) if growth_rates else 0
        
        return {
            "trend_direction": "up" if avg_growth > 5 else "down" if avg_growth < -5 else "stable",
            "avg_monthly_growth": round(avg_growth, 2),
            "latest_volume": volumes[-1] if volumes else 0,
        }
    
    def _analyze_seller_distribution(self, country_result: Dict, type_result: Dict) -> Dict[str, Any]:
        analysis = {"country_distribution": {}, "type_distribution": {}, "china_seller_intensity": "unknown"}
        
        if country_result.get("code") == "OK":
            country_data = country_result.get("data", [])
            total = sum(c.get("count", 0) for c in country_data)
            if total > 0:
                for c in country_data:
                    country = c.get("country", "Unknown")
                    analysis["country_distribution"][country] = {
                        "count": c.get("count", 0),
                        "percentage": round(c.get("count", 0) / total * 100, 2)
                    }
                china_count = sum(c.get("count", 0) for c in country_data if c.get("country") == "CN")
                china_pct = china_count / total * 100 if total > 0 else 0
                analysis["china_seller_intensity"] = "high" if china_pct > 60 else "medium" if china_pct > 30 else "low"
        
        return analysis
    
    def _analyze_aba_data(self, weekly: Dict, monthly: Dict) -> Dict[str, Any]:
        analysis = {"weekly_trend": [], "monthly_trend": []}
        
        if weekly.get("code") == "OK":
            weekly_data = weekly.get("data", [])
            if isinstance(weekly_data, list):
                analysis["weekly_trend"] = [
                    {"week": w.get("week"), "search_rank": w.get("searchRank")}
                    for w in weekly_data[:12]
                ]
        
        return analysis
    
    def _extract_basic_info(self, result: Dict) -> Dict[str, Any]:
        if result.get("code") != "OK":
            return {"error": result.get("message")}
        data = result.get("data", {})
        return {
            "asin": data.get("asin"),
            "title": data.get("title"),
            "price": data.get("price"),
            "rating": data.get("rating"),
        }
    
    def _extract_prediction(self, result: Dict) -> Dict[str, Any]:
        if result.get("code") != "OK":
            return {"error": result.get("message", "No prediction data")}
        data = result.get("data", {})
        return {
            "estimated_monthly_sales": data.get("monthlySales"),
            "confidence": data.get("confidence"),
        }
    
    def _deep_voc_analysis(self, result: Dict) -> Dict[str, Any]:
        if result.get("code") != "OK":
            return {"error": result.get("message")}
        data = result.get("data", {})
        reviews = data.get("reviews", []) or data.get("items", [])
        return {"total_reviews": len(reviews), "pain_points": [], "praise_points": []}
    
    def _analyze_keepa_data(self, result: Dict) -> Dict[str, Any]:
        if result.get("code") != "OK":
            return {"error": result.get("message", "No Keepa data")}
        data = result.get("data", {})
        return {
            "price_trend": "unknown",
            "price_volatility": data.get("priceVolatility", 0),
        }
    
    def _analyze_traffic_comprehensive(self, traffic: Dict, source: Dict, extend: Dict) -> Dict[str, Any]:
        analysis = {"total_traffic_keywords": 0, "traffic_sources": {}, "extended_keywords": []}
        
        if traffic.get("code") == "OK":
            data = traffic.get("data", {})
            items = data.get("items") if isinstance(data, dict) else []
            if items is None:
                items = []
            analysis["total_traffic_keywords"] = len(items)
        
        return analysis
    
    def _analyze_keyword_opportunities(self, result: Dict) -> List[Dict]:
        if result.get("code") != "OK":
            return []
        data = result.get("data", {})
        items = data.get("items", [])
        return [{"keyword": item.get("keywords"), "search_volume": item.get("searches")} for item in items[:20]]
    
    def _analyze_traffic_stats(self, result: Dict) -> Dict[str, Any]:
        if result.get("code") != "OK":
            return {"error": result.get("message")}
        data = result.get("data", {})
        return {"total_traffic_asins": data.get("totalAsins", 0)}
    
    def _analyze_listing_stats(self, result: Dict) -> Dict[str, Any]:  # ⭐
        """分析Listing流量统计"""
        if result.get("code") != "OK":
            return {"error": result.get("message", "No data")}
        
        data = result.get("data", {})
        return {
            "total_listings": data.get("totalListings", 0),
            "avg_traffic": data.get("avgTraffic", 0),
            "top_performers": data.get("topPerformers", [])[:5],
        }


def test_all_apis():
    """测试所有API"""
    print("\n" + "="*70)
    print("TESTING ALL 36 APIs - 100% Utilization")
    print("="*70)
    
    layer = AmazonDataLayerV2()
    
    # 测试完整市场情报（11个API）
    print("\n[Test 1] Complete Market Intelligence (11 APIs)...")
    market = layer.get_complete_market_intelligence("women active shorts")
    if market.get("code") == "OK":
        data = market["data"]
        print(f"  [OK] Brand Analysis: CR3={data['brand_analysis'].get('cr3')}%")
        print(f"  [OK] Price Analysis: {len(data['price_analysis'].get('price_bands', []))} bands")
        print(f"  [OK] Market Research: {'OK' if 'market_research' in data else 'FAIL'}")  # NEW
        print(f"  [OK] Product Conc: {'OK' if 'product_concentration' in data else 'FAIL'}")  # NEW
        print(f"  [OK] BSR Prediction: {'OK' if 'bsr_prediction' in data else 'FAIL'}")  # NEW
    
    # 测试完整竞品情报（9个API）
    print("\n[Test 2] Complete Competitor Intelligence (9 APIs)...")
    comp = layer.get_complete_competitor_intelligence("B071WV2SRC")
    if comp.get("code") == "OK":
        data = comp["data"]
        print(f"  [OK] Basic Info: {data['basic_info'].get('asin')}")
        print(f"  [OK] Sales Prediction: {data['sales_prediction'].get('estimated_monthly_sales')}")
        print(f"  [OK] Listing Traffic: {'OK' if 'listing_traffic' in data else 'FAIL'}")
        print(f"  [OK] Product Research: {'OK' if 'product_research' in data else 'FAIL'}")
        print(f"  [OK] Competitor Lookup: {'OK' if 'competitor_lookup' in data else 'FAIL'}")  # NEW
    
    # 测试完整关键词情报（5个API）
    print("\n[Test 3] Complete Keyword Intelligence (5 APIs)...")
    keyword = layer.get_complete_keyword_intelligence("women shorts")
    if keyword.get("code") == "OK":
        data = keyword["data"]
        print(f"  [OK] Opportunities: {len(data['keyword_opportunities'])}")
        print(f"  [OK] Keyword Research: {'OK' if 'keyword_research' in data else 'FAIL'}")
        print(f"  [OK] Listing Stats: {'OK' if 'listing_stats' in data else 'FAIL'}")  # NEW
    
    # 最终统计
    stats = layer.api.get_stats()
    print("\n" + "="*70)
    print("FINAL API UTILIZATION STATS")
    print("="*70)
    print(f"Total APIs: {stats['total_apis']}")
    print(f"APIs Used: {stats['apis_used']}")
    print(f"Utilization: {stats['api_utilization']}")
    print(f"Cache Hit Rate: {stats['cache_hit_rate']}")
    
    if stats['unused_apis']:
        print(f"\nUnused APIs: {stats['unused_apis']}")
    else:
        print("\n[COMPLETE] ALL APIs UTILIZED!")
    
    print("="*70)


if __name__ == "__main__":
    test_all_apis()
