#!/usr/bin/env python3
"""
Shodan API 统一调用脚本

支持功能：
- host: 查询指定 IP 的详细信息
- search: 搜索设备
- count: 统计搜索结果数量
- dns-domain: 查询域名 DNS 信息
- dns-reverse: 反向 DNS 查询
- ports: 获取端口列表
- queries: 获取搜索查询列表
- myip: 获取当前 IP
- profile: 获取账户信息

授权方式: ApiKey
凭证Key: SHODAN_API_KEY
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

import requests


class ShodanAPI:
    """Shodan API 客户端"""

    BASE_URL = "https://api.shodan.io"

    def __init__(self):
        """初始化 API 客户端，从环境变量读取 API Key"""
        self.api_key = os.getenv("SHODAN_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "缺少 Shodan API Key。请检查环境变量 SHODAN_API_KEY"
            )

    def _request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        method: str = "GET",
    ) -> Dict[str, Any]:
        """
        发送 API 请求

        Args:
            endpoint: API 端点路径
            params: 请求参数
            method: HTTP 方法

        Returns:
            API 响应数据
        """
        url = f"{self.BASE_URL}{endpoint}"

        # 添加 API Key 到查询参数
        if params is None:
            params = {}
        params["key"] = self.api_key

        try:
            if method.upper() == "GET":
                response = requests.get(url, params=params, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, params=params, timeout=30)
            else:
                raise ValueError(f"不支持的 HTTP 方法: {method}")

            # 检查 HTTP 状态码
            if response.status_code == 401:
                raise Exception("API Key 无效或已过期")
            elif response.status_code == 403:
                raise Exception("权限不足，请检查 API 订阅计划")
            elif response.status_code == 429:
                raise Exception("请求频率超限，请稍后再试")
            elif response.status_code >= 400:
                error_msg = response.text[:200]
                raise Exception(f"HTTP 错误 {response.status_code}: {error_msg}")

            data = response.json()

            # 检查 API 错误
            if isinstance(data, dict) and "error" in data:
                raise Exception(f"API 错误: {data['error']}")

            return data

        except requests.exceptions.Timeout:
            raise Exception("请求超时，请检查网络连接")
        except requests.exceptions.ConnectionError:
            raise Exception("网络连接失败，请检查网络设置")
        except json.JSONDecodeError:
            raise Exception("响应格式错误，无法解析 JSON")
        except Exception as e:
            raise Exception(f"请求失败: {str(e)}")

    def host(self, ip: str, history: bool = False, minify: bool = False) -> Dict[str, Any]:
        """
        查询指定 IP 的详细信息

        Args:
            ip: IP 地址
            history: 是否包含历史数据
            minify: 是否返回简化数据

        Returns:
            主机详细信息
        """
        params = {}
        if history:
            params["history"] = "true"
        if minify:
            params["minify"] = "true"

        return self._request(f"/shodan/host/{ip}", params)

    def search(
        self,
        query: str,
        facets: Optional[str] = None,
        page: int = 1,
        minify: bool = False,
    ) -> Dict[str, Any]:
        """
        搜索设备

        Args:
            query: 搜索查询字符串
            facets: 要返回的统计维度，用逗号分隔
            page: 页码，从 1 开始
            minify: 是否返回简化数据

        Returns:
            搜索结果和统计信息
        """
        params = {"query": query, "page": str(page)}
        if facets:
            params["facets"] = facets
        if minify:
            params["minify"] = "true"

        return self._request("/shodan/host/search", params)

    def count(self, query: str, facets: Optional[str] = None) -> Dict[str, Any]:
        """
        统计搜索结果数量

        Args:
            query: 搜索查询字符串
            facets: 要返回的统计维度，用逗号分隔

        Returns:
            结果总数和统计信息
        """
        params = {"query": query}
        if facets:
            params["facets"] = facets

        return self._request("/shodan/host/count", params)

    def dns_domain(self, domain: str) -> Dict[str, Any]:
        """
        查询域名 DNS 信息

        Args:
            domain: 域名

        Returns:
            DNS 记录信息
        """
        return self._request(f"/dns/domain/{domain}")

    def dns_reverse(self, ip: str) -> Dict[str, Any]:
        """
        反向 DNS 查询

        Args:
            ip: IP 地址

        Returns:
            反向 DNS 记录
        """
        return self._request(f"/dns/reverse/{ip}")

    def ports(self) -> List[int]:
        """
        获取 Shodan 爬取的端口列表

        Returns:
            端口列表
        """
        return self._request("/shodan/ports")

    def queries(
        self,
        page: int = 1,
        sort: str = "votes",
        order: str = "desc",
    ) -> Dict[str, Any]:
        """
        获取搜索查询列表

        Args:
            page: 页码
            sort: 排序字段（votes, timestamp）
            order: 排序方向（asc, desc）

        Returns:
            查询列表
        """
        params = {"page": str(page), "sort": sort, "order": order}
        return self._request("/shodan/query", params)

    def myip(self) -> str:
        """
        获取当前 IP 地址

        Returns:
            当前 IP 地址
        """
        return self._request("/tools/myip")

    def profile(self) -> Dict[str, Any]:
        """
        获取账户信息

        Returns:
            账户详细信息
        """
        return self._request("/api-info")


def format_output(data: Any, format_type: str = "json") -> str:
    """
    格式化输出数据

    Args:
        data: 要格式化的数据
        format_type: 输出格式（json, pretty）

    Returns:
        格式化后的字符串
    """
    if format_type == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)
    else:
        return str(data)


def main():
    """主函数：解析命令行参数并执行相应操作"""
    parser = argparse.ArgumentParser(
        description="Shodan API 调用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s host 8.8.8.8
  %(prog)s search "port:80" --facets "country,org"
  %(prog)s count "product:nginx"
  %(prog)s dns-domain google.com
  %(prog)s dns-reverse 8.8.8.8
  %(prog)s ports
  %(prog)s queries
  %(prog)s myip
  %(prog)s profile
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # host 子命令
    host_parser = subparsers.add_parser("host", help="查询指定 IP 的详细信息")
    host_parser.add_argument("ip", help="IP 地址")
    host_parser.add_argument("--history", action="store_true", help="包含历史数据")
    host_parser.add_argument("--minify", action="store_true", help="返回简化数据")

    # search 子命令
    search_parser = subparsers.add_parser("search", help="搜索设备")
    search_parser.add_argument("query", help="搜索查询字符串")
    search_parser.add_argument("--facets", help="统计维度，用逗号分隔（如 country,org,port）")
    search_parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始")
    search_parser.add_argument("--minify", action="store_true", help="返回简化数据")

    # count 子命令
    count_parser = subparsers.add_parser("count", help="统计搜索结果数量")
    count_parser.add_argument("query", help="搜索查询字符串")
    count_parser.add_argument("--facets", help="统计维度，用逗号分隔")

    # dns-domain 子命令
    dns_domain_parser = subparsers.add_parser("dns-domain", help="查询域名 DNS 信息")
    dns_domain_parser.add_argument("domain", help="域名")

    # dns-reverse 子命令
    dns_reverse_parser = subparsers.add_parser("dns-reverse", help="反向 DNS 查询")
    dns_reverse_parser.add_argument("ip", help="IP 地址")

    # ports 子命令
    subparsers.add_parser("ports", help="获取端口列表")

    # queries 子命令
    queries_parser = subparsers.add_parser("queries", help="获取搜索查询列表")
    queries_parser.add_argument("--page", type=int, default=1, help="页码")
    queries_parser.add_argument("--sort", default="votes", help="排序字段（votes, timestamp）")
    queries_parser.add_argument("--order", default="desc", help="排序方向（asc, desc）")

    # myip 子命令
    subparsers.add_parser("myip", help="获取当前 IP 地址")

    # profile 子命令
    subparsers.add_parser("profile", help="获取账户信息")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        # 初始化 API 客户端
        api = ShodanAPI()

        # 执行相应命令
        if args.command == "host":
            result = api.host(args.ip, history=args.history, minify=args.minify)
        elif args.command == "search":
            result = api.search(
                args.query, facets=args.facets, page=args.page, minify=args.minify
            )
        elif args.command == "count":
            result = api.count(args.query, facets=args.facets)
        elif args.command == "dns-domain":
            result = api.dns_domain(args.domain)
        elif args.command == "dns-reverse":
            result = api.dns_reverse(args.ip)
        elif args.command == "ports":
            result = api.ports()
        elif args.command == "queries":
            result = api.queries(page=args.page, sort=args.sort, order=args.order)
        elif args.command == "myip":
            result = api.myip()
        elif args.command == "profile":
            result = api.profile()
        else:
            print(f"未知命令: {args.command}")
            sys.exit(1)

        # 输出结果
        print(format_output(result))

    except ValueError as e:
        print(f"配置错误: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"执行失败: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
