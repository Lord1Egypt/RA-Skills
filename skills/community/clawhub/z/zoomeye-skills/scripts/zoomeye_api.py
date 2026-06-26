#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZoomEye API 封装脚本

功能：
- 用户信息查询
- 主机资产搜索
- Web应用搜索
- 资源统计

授权方式: ApiKey
凭证Key: ZOOMEYE_API_KEY
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Optional, Any
import requests


class ZoomEyeAPI:
    """ZoomEye API 客户端"""
    
    BASE_URL = "https://api.zoomeye.org"
    
    def __init__(self, api_key: str):
        """
        初始化 ZoomEye API 客户端
        
        Args:
            api_key: ZoomEye API Key
        """
        self.api_key = api_key
        self.headers = {
            "API-KEY": api_key,
            "Content-Type": "application/json"
        }
    
    def get_user_info(self) -> Dict[str, Any]:
        """
        查询用户信息
        
        Returns:
            用户信息字典，包含用户名、积分、VIP等级等
        """
        url = f"{self.BASE_URL}/resources-info"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 401:
                raise Exception("认证失败：API Key 无效或已过期")
            elif response.status_code == 403:
                raise Exception("访问被拒绝：权限不足或配额已用完")
            elif response.status_code >= 400:
                raise Exception(f"HTTP请求失败: 状态码 {response.status_code}, 响应内容: {response.text}")
            
            data = response.json()
            return {
                "success": True,
                "data": data
            }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API调用失败: {str(e)}")
    
    def host_search(self, query: str, facets: str = "", page: int = 1) -> Dict[str, Any]:
        """
        主机资产搜索
        
        Args:
            query: 查询语句
            facets: 聚合字段，多个用逗号分隔（如：app,os,country）
            page: 页码，默认第1页
            
        Returns:
            搜索结果字典
        """
        url = f"{self.BASE_URL}/host/search"
        params = {
            "query": query,
            "page": page
        }
        
        if facets:
            params["facet"] = facets
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 401:
                raise Exception("认证失败：API Key 无效或已过期")
            elif response.status_code == 403:
                raise Exception("访问被拒绝：权限不足或配额已用完")
            elif response.status_code == 429:
                raise Exception("请求过于频繁：请稍后再试")
            elif response.status_code >= 400:
                raise Exception(f"HTTP请求失败: 状态码 {response.status_code}, 响应内容: {response.text}")
            
            data = response.json()
            
            # 格式化输出
            result = {
                "success": True,
                "total": data.get("total", 0),
                "page": page,
                "facets": data.get("facets", {}),
                "matches": []
            }
            
            # 提取关键信息
            matches = data.get("matches", [])
            for match in matches:
                item = {
                    "ip": match.get("ip", ""),
                    "port": match.get("portinfo", {}).get("port", ""),
                    "service": match.get("portinfo", {}).get("service", ""),
                    "app": match.get("portinfo", {}).get("app", ""),
                    "version": match.get("portinfo", {}).get("version", ""),
                    "os": match.get("portinfo", {}).get("os", ""),
                    "country": match.get("geoinfo", {}).get("country", {}).get("names", {}).get("zh-CN", ""),
                    "city": match.get("geoinfo", {}).get("city", {}).get("names", {}).get("zh-CN", ""),
                    "asn": match.get("geoinfo", {}).get("asn", 0),
                    "domain": match.get("portinfo", {}).get("domain", [])
                }
                result["matches"].append(item)
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API调用失败: {str(e)}")
    
    def web_search(self, query: str, facets: str = "", page: int = 1) -> Dict[str, Any]:
        """
        Web应用搜索
        
        Args:
            query: 查询语句
            facets: 聚合字段，多个用逗号分隔
            page: 页码，默认第1页
            
        Returns:
            搜索结果字典
        """
        url = f"{self.BASE_URL}/web/search"
        params = {
            "query": query,
            "page": page
        }
        
        if facets:
            params["facet"] = facets
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 401:
                raise Exception("认证失败：API Key 无效或已过期")
            elif response.status_code == 403:
                raise Exception("访问被拒绝：权限不足或配额已用完")
            elif response.status_code == 429:
                raise Exception("请求过于频繁：请稍后再试")
            elif response.status_code >= 400:
                raise Exception(f"HTTP请求失败: 状态码 {response.status_code}, 响应内容: {response.text}")
            
            data = response.json()
            
            # 格式化输出
            result = {
                "success": True,
                "total": data.get("total", 0),
                "page": page,
                "facets": data.get("facets", {}),
                "matches": []
            }
            
            # 提取关键信息
            matches = data.get("matches", [])
            for match in matches:
                item = {
                    "site": match.get("site", ""),
                    "ip": match.get("ip", ""),
                    "port": match.get("portinfo", {}).get("port", ""),
                    "title": match.get("webapp", [{}])[0].get("title", "") if match.get("webapp") else "",
                    "webapp": match.get("webapp", []),
                    "headers": match.get("headers", {}),
                    "country": match.get("geoinfo", {}).get("country", {}).get("names", {}).get("zh-CN", ""),
                    "city": match.get("geoinfo", {}).get("city", {}).get("names", {}).get("zh-CN", "")
                }
                result["matches"].append(item)
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API调用失败: {str(e)}")
    
    def get_stats(self, query: str, facet: str = "app") -> Dict[str, Any]:
        """
        获取搜索统计信息
        
        Args:
            query: 查询语句
            facet: 统计字段（如：app, os, country, port）
            
        Returns:
            统计结果字典
        """
        url = f"{self.BASE_URL}/host/search"
        params = {
            "query": query,
            "facet": facet,
            "page": 1
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 401:
                raise Exception("认证失败：API Key 无效或已过期")
            elif response.status_code == 403:
                raise Exception("访问被拒绝：权限不足或配额已用完")
            elif response.status_code >= 400:
                raise Exception(f"HTTP请求失败: 状态码 {response.status_code}, 响应内容: {response.text}")
            
            data = response.json()
            
            return {
                "success": True,
                "query": query,
                "facet": facet,
                "total": data.get("total", 0),
                "facets": data.get("facets", {})
            }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API调用失败: {str(e)}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="ZoomEye API 工具")
    parser.add_argument("--action", required=True, 
                       choices=["user-info", "host-search", "web-search", "stats"],
                       help="操作类型：user-info(用户信息)、host-search(主机搜索)、web-search(Web搜索)、stats(统计)")
    parser.add_argument("--query", help="查询语句")
    parser.add_argument("--facets", help="聚合字段，多个用逗号分隔")
    parser.add_argument("--facet", help="统计字段（用于stats操作）")
    parser.add_argument("--page", type=int, default=1, help="页码，默认第1页")
    
    args = parser.parse_args()
    
    # 获取 API Key
    api_key = os.getenv("ZOOMEYE_API_KEY")
    
    if not api_key:
        print(json.dumps({
            "success": False,
            "error": "缺少 API Key，请在环境变量中配置 ZOOMEYE_API_KEY"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    # 初始化客户端
    client = ZoomEyeAPI(api_key)
    
    try:
        # 执行操作
        if args.action == "user-info":
            result = client.get_user_info()
        
        elif args.action == "host-search":
            if not args.query:
                print(json.dumps({
                    "success": False,
                    "error": "缺少查询语句，请使用 --query 参数指定"
                }, ensure_ascii=False, indent=2))
                sys.exit(1)
            result = client.host_search(args.query, args.facets or "", args.page)
        
        elif args.action == "web-search":
            if not args.query:
                print(json.dumps({
                    "success": False,
                    "error": "缺少查询语句，请使用 --query 参数指定"
                }, ensure_ascii=False, indent=2))
                sys.exit(1)
            result = client.web_search(args.query, args.facets or "", args.page)
        
        elif args.action == "stats":
            if not args.query:
                print(json.dumps({
                    "success": False,
                    "error": "缺少查询语句，请使用 --query 参数指定"
                }, ensure_ascii=False, indent=2))
                sys.exit(1)
            result = client.get_stats(args.query, args.facet or "app")
        
        # 输出结果
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
