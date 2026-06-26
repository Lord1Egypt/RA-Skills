#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Truth (求真) v1.3 - 数据源管理模块
功能：对接公开事实数据源，多数据源fallback
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class DataSource:
    """数据源基类"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.enabled = config.get('enabled', True)
    
    def search(self, query: str) -> Optional[List[Dict]]:
        """搜索事实，返回结果列表 [{title, url, snippet}, ...]"""
        raise NotImplementedError


class BraveSearchDataSource(DataSource):
    """Brave Search API 免费公开数据源"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.api_key = config.get('api_key', '')
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        self.count = config.get('count', 5)  # 返回最多5条结果
    
    def search(self, query: str) -> Optional[List[Dict]]:
        """搜索查询"""
        if not self.enabled or not self.api_key:
            return None
        
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key
        }
        params = {
            "q": query,
            "count": self.count
        }
        
        try:
            resp = requests.get(self.base_url, headers=headers, params=params, timeout=5)
            if resp.status_code != 200:
                logger.warning(f"Brave Search API error: {resp.status_code}")
                return None
            
            data = resp.json()
            results = []
            for item in data.get('web', {}).get('results', []):
                results.append({
                    "title": item.get('title', ''),
                    "url": item.get('url', ''),
                    "snippet": item.get('description', '')
                })
            return results
        except Exception as e:
            logger.warning(f"Brave Search request error: {e}")
            return None


class DataSourceManager:
    """数据源管理器，支持多数据源 fallback"""
    
    def __init__(self, config: Dict):
        self.sources = []
        # 初始化已配置数据源
        if 'brave' in config:
            self.sources.append(BraveSearchDataSource(config['brave']))
    
    def search_fact(self, query: str) -> Tuple[Optional[List[Dict]], str]:
        """按顺序尝试数据源，返回第一个成功结果"""
        for source in self.sources:
            if not source.enabled:
                continue
            results = source.search(query)
            if results is not None:
                return results, source.__class__.__name__
        
        return None, "no available datasource"
    
    def get_search_results(self, sentence: str) -> Optional[List[Dict]]:
        """搜索句子相关事实参考"""
        # 简化：直接用句子作为query
        results, source = self.search_fact(sentence)
        logger.info(f"Fact search for '{sentence[:30]}...' from {source}: {len(results) if results else 0} results")
        return results
