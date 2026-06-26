#!/usr/bin/env python3
"""
招标采购信息搜索 API 客户端

使用方法:
    python bid_search.py --keyword "工程" --class-name "招标信息" --area "武汉"

凭证配置:
    - 环境变量 BID_API_KEY: API 密钥
    - 环境变量 BID_SERVER_URL: 服务器地址 (可选，默认 https://gate.gov-bid.com)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta

import requests


class BidSearchClient:
    """招标采购信息搜索 API 客户端"""
    
    def __init__(self, api_key=None, server_url=None):
        """
        初始化客户端
        
        Args:
            api_key: API 密钥，默认从环境变量 BID_API_KEY 读取
            server_url: 服务器地址，默认从环境变量 BID_SERVER_URL 读取
        """
        self.api_key = api_key or os.environ.get("BID_API_KEY")
        self.server_url = server_url or os.environ.get("BID_SERVER_URL", "https://gate.gov-bid.com")
        
        if not self.api_key:
            raise ValueError("API Key 未配置，请设置 BID_API_KEY 环境变量")
        
        self.base_url = f"{self.server_url}/outer-gateway/bid/SearchProjectForAI"
    
    def search(self,
               keyword=None,
               exclude_kw=None,
               include_kw=None,
               class_name=None,
               area_name=None,
               search_field="全部",
               start_date=None,
               end_date=None,
               page_id=1,
               page_number=20):
        """
        搜索招标采购项目
        
        Args:
            keyword: 搜索关键词（空格=同时出现，竖线=或关系）
            exclude_kw: 排除关键词（竖线分隔）
            include_kw: 必须包含关键词（竖线分隔）
            class_name: 项目类别（招标信息，中标信息，合同信息，采购意向，拍租信息）
            area_name: 地区名称（如"武汉"）
            search_field: 搜索字段（标题，内容，全部）
            start_date: 开始日期 (yyyy-MM-dd)，默认 7 天前
            end_date: 结束日期 (yyyy-MM-dd)，默认今天
            page_id: 页码
            page_number: 每页记录数 (最大 100，设为 0 仅返回总数)
        
        Returns:
            dict: API 响应数据
        """
        # 默认日期范围
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        # 构建请求参数
        payload = {
            "startDate": start_date,
            "endDate": end_date,
            "pageId": page_id,
            "pageNumber": page_number,
        }
        
        if keyword:
            payload["keyword"] = keyword
        if exclude_kw:
            payload["excludeKW"] = exclude_kw
        if include_kw:
            payload["inCludeKW"] = include_kw
        if class_name:
            payload["className"] = class_name
        if area_name:
            payload["areaName"] = area_name
        if search_field:
            payload["searchField"] = search_field
        
        # 发送请求
        url = f"{self.base_url}?key={self.api_key}"
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        return response.json()
    
    def search_all_pages(self, **kwargs):
        """
        分页获取全部结果
        
        Args:
            **kwargs: 传递给 search() 的参数
        
        Returns:
            list: 所有项目列表
        """
        all_results = []
        page = 1
        page_number = kwargs.get("page_number", 100)
        
        while True:
            result = self.search(page_id=page, page_number=page_number, **kwargs)
            
            if result.get("code") != 200:
                print(f"错误：{result.get('msg')}", file=sys.stderr)
                break
            
            items = result.get("data", {}).get("data", [])
            if not items:
                break
            
            all_results.extend(items)
            
            if not result.get("data", {}).get("hasNext", False):
                break
            
            page += 1
            print(f"已获取第 {page-1} 页，共 {len(all_results)} 条记录...", file=sys.stderr)
        
        return all_results
    
    def get_total_count(self, **kwargs):
        """
        获取搜索结果总数（不返回具体数据）
        
        Args:
            **kwargs: 传递给 search() 的参数
        
        Returns:
            int: 结果总数
        """
        result = self.search(page_number=0, **kwargs)
        if result.get("code") == 200:
            return result.get("data", {}).get("total", 0)
        return 0


def format_project(project):
    """格式化项目信息用于输出"""
    lines = []
    lines.append(f"标题：{project.get('title', 'N/A')}")
    lines.append(f"类型：{project.get('newsTypeName', 'N/A')} / {project.get('projectClass', 'N/A')}")
    lines.append(f"发布时间：{project.get('publishTime', 'N/A')}")
    lines.append(f"地区：{project.get('areaName', 'N/A')}")
    
    if project.get('projectMoney'):
        lines.append(f"金额：{project['projectMoney']}")
    
    # 甲方信息
    part_a = project.get('partAInfo', [])
    if part_a:
        lines.append(f"甲方：{part_a[0].get('name', 'N/A')}")
        if part_a[0].get('contactPhone'):
            lines.append(f"甲方电话：{part_a[0]['contactPhone']}")
    
    # 乙方信息
    part_b = project.get('partBInfo', [])
    if part_b:
        lines.append(f"乙方：{part_b[0].get('name', 'N/A')}")
    
    # 代理机构
    agency = project.get('agencyInfo', [])
    if agency:
        lines.append(f"代理：{agency[0].get('name', 'N/A')}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="招标采购信息搜索 API 客户端")
    parser.add_argument("--keyword", "-k", help="搜索关键词")
    parser.add_argument("--exclude", "-e", help="排除关键词（竖线分隔）")
    parser.add_argument("--include", "-i", help="必须包含关键词（竖线分隔）")
    parser.add_argument("--class-name", "-c", help="项目类别")
    parser.add_argument("--area", "-a", help="地区名称")
    parser.add_argument("--field", "-f", default="全部", help="搜索字段（标题/内容/全部）")
    parser.add_argument("--start-date", "-s", help="开始日期 (yyyy-MM-dd)")
    parser.add_argument("--end-date", "-d", help="结束日期 (yyyy-MM-dd)")
    parser.add_argument("--page", "-p", type=int, default=1, help="页码")
    parser.add_argument("--page-size", "-n", type=int, default=20, help="每页记录数")
    parser.add_argument("--all", action="store_true", help="获取全部结果（分页）")
    parser.add_argument("--count", action="store_true", help="仅获取总数")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--api-key", help="API 密钥（覆盖环境变量）")
    parser.add_argument("--server-url", help="服务器地址（覆盖环境变量）")
    
    args = parser.parse_args()
    
    try:
        client = BidSearchClient(
            api_key=args.api_key,
            server_url=args.server_url
        )
    except ValueError as e:
        print(f"错误：{e}", file=sys.stderr)
        print("请设置环境变量 BID_API_KEY 或使用 --api-key 参数", file=sys.stderr)
        sys.exit(1)
    
    # 仅获取总数
    if args.count:
        total = client.get_total_count(
            keyword=args.keyword,
            exclude_kw=args.exclude,
            include_kw=args.include,
            class_name=args.class_name,
            area_name=args.area,
            search_field=args.field,
            start_date=args.start_date,
            end_date=args.end_date
        )
        print(f"搜索结果总数：{total}")
        return
    
    # 获取全部结果
    if args.all:
        results = client.search_all_pages(
            keyword=args.keyword,
            exclude_kw=args.exclude,
            include_kw=args.include,
            class_name=args.class_name,
            area_name=args.area,
            search_field=args.field,
            start_date=args.start_date,
            end_date=args.end_date
        )
        
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"\n共获取 {len(results)} 条记录\n")
            for i, project in enumerate(results, 1):
                print(f"--- 第 {i} 条 ---")
                print(format_project(project))
                print()
        return
    
    # 单页搜索
    result = client.search(
        keyword=args.keyword,
        exclude_kw=args.exclude,
        include_kw=args.include,
        class_name=args.class_name,
        area_name=args.area,
        search_field=args.field,
        start_date=args.start_date,
        end_date=args.end_date,
        page_id=args.page,
        page_number=args.page_size
    )
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    # 格式化输出
    if result.get("code") != 200:
        print(f"错误：{result.get('msg')}", file=sys.stderr)
        sys.exit(1)
    
    data = result.get("data", {})
    print(f"总数：{data.get('total', 0)} | 页码：{data.get('pageId')} | 每页：{data.get('pageNumber')} | 有下一页：{data.get('hasNext')}")
    print()
    
    projects = data.get("data", [])
    if not projects:
        print("没有找到匹配的记录")
        return
    
    for i, project in enumerate(projects, 1):
        print(f"--- 第 {i} 条 ---")
        print(format_project(project))
        print()


if __name__ == "__main__":
    main()
