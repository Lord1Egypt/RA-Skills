#!/usr/bin/env python3
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL 1.1.1+")
import os
import sys
import json
import time
import requests
from typing import Optional, List, Dict, Any

# 只读取TAVILY_API_KEY环境变量
with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"), "r") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            if key == "TAVILY_API_KEY":
                os.environ[key] = value.strip()

class TavilySearch:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY 未配置，请在 .env 文件中设置")
        self.base_url = "https://api.tavily.com"
    
    def search(
        self,
        query: str,
        search_depth: str = "basic",
        chunks_per_source: int = 3,
        max_results: int = 5,
        topic: str = "general",
        time_range: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        include_answer: bool = False,
        include_raw_content: bool = False,
        include_images: bool = False,
        include_image_descriptions: bool = False,
        include_favicon: bool = False,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        country: Optional[str] = None,
        auto_parameters: bool = False,
        exact_match: bool = False,
        include_usage: bool = False
    ) -> Dict[str, Any]:
        """执行 Tavily 搜索"""
        payload = {
            "query": query,
            "search_depth": search_depth,
            "chunks_per_source": chunks_per_source,
            "max_results": max_results,
            "topic": topic,
            "include_answer": include_answer,
            "include_raw_content": include_raw_content,
            "include_images": include_images,
            "include_image_descriptions": include_image_descriptions,
            "include_favicon": include_favicon,
            "auto_parameters": auto_parameters,
            "exact_match": exact_match,
            "include_usage": include_usage
        }
        
        if time_range:
            payload["time_range"] = time_range
        if start_date:
            payload["start_date"] = start_date
        if end_date:
            payload["end_date"] = end_date
        if include_domains:
            payload["include_domains"] = include_domains
        if exclude_domains:
            payload["exclude_domains"] = exclude_domains
        if country:
            payload["country"] = country
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.post(f"{self.base_url}/search", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def extract(
        self,
        urls: List[str],
        query: Optional[str] = None,
        chunks_per_source: int = 3,
        extract_depth: str = "basic",
        include_images: bool = False,
        include_favicon: bool = False,
        format: str = "markdown"
    ) -> Dict[str, Any]:
        """提取网页内容"""
        payload = {
            "urls": urls,
            "chunks_per_source": chunks_per_source,
            "extract_depth": extract_depth,
            "include_images": include_images,
            "include_favicon": include_favicon,
            "format": format
        }
        if query:
            payload["query"] = query
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.post(f"{self.base_url}/extract", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def create_research_task(
        self,
        input: str,
        model: str = "auto",
        stream: bool = False,
        output_schema: Optional[Dict] = None,
        citation_format: str = "numbered"
    ) -> Dict[str, Any]:
        """创建深度研究任务"""
        payload = {
            "input": input,
            "model": model,
            "stream": stream,
            "citation_format": citation_format
        }
        if output_schema:
            payload["output_schema"] = output_schema
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.post(f"{self.base_url}/research", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_research_result(self, request_id: str) -> Dict[str, Any]:
        """获取深度研究任务结果"""
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.get(f"{self.base_url}/research/{request_id}", headers=headers)
        response.raise_for_status()
        return response.json()
    
    def crawl(
        self,
        url: str,
        instructions: Optional[str] = None,
        max_depth: int = 1,
        max_breadth: int = 20,
        limit: int = 50,
        select_paths: Optional[List[str]] = None,
        select_domains: Optional[List[str]] = None,
        exclude_paths: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        allow_external: bool = True,
        include_images: bool = False,
        extract_depth: str = "basic",
        format: str = "markdown",
        include_favicon: bool = False
    ) -> Dict[str, Any]:
        """整站爬取"""
        payload = {
            "url": url,
            "max_depth": max_depth,
            "max_breadth": max_breadth,
            "limit": limit,
            "allow_external": allow_external,
            "include_images": include_images,
            "extract_depth": extract_depth,
            "format": format,
            "include_favicon": include_favicon
        }
        
        if instructions:
            payload["instructions"] = instructions
        if select_paths:
            payload["select_paths"] = select_paths
        if select_domains:
            payload["select_domains"] = select_domains
        if exclude_paths:
            payload["exclude_paths"] = exclude_paths
        if exclude_domains:
            payload["exclude_domains"] = exclude_domains
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.post(f"{self.base_url}/crawl", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def format_crawl_results(self, results: Dict[str, Any]) -> str:
        """格式化爬取结果"""
        output = []
        output.append("🕷️ 整站爬取结果：")
        output.append("=" * 80)
        
        output.append(f"🌐 根URL: {results.get('base_url', '未知')}")
        output.append(f"⏱️  耗时: {results.get('response_time', 0)}s")
        output.append(f"📄 共爬取 {len(results.get('results', []))} 个页面")
        output.append("")
        
        for i, page in enumerate(results["results"][:10], 1):  # 只显示前10个页面
            output.append(f"{i}. {page['url']}")
            output.append(f"   📝 内容摘要: {page['raw_content'][:200]}..." if len(page['raw_content']) > 200 else f"   📝 内容: {page['raw_content']}")
            output.append("")
        
        if len(results.get('results', [])) > 10:
            output.append(f"... 还有 {len(results['results']) - 10} 个页面未显示")
        
        if results.get("usage"):
            output.append(f"\n💡 本次调用消耗 {results['usage']['credits']} 个信用点")
        
        return "\n".join(output)
    
    def research(
        self,
        input: str,
        model: str = "auto",
        output_schema: Optional[Dict] = None,
        citation_format: str = "numbered",
        poll_interval: int = 5,
        max_polls: int = 60
    ) -> Dict[str, Any]:
        """执行完整深度研究（自动轮询结果）"""
        # 创建任务
        task = self.create_research_task(
            input=input,
            model=model,
            output_schema=output_schema,
            citation_format=citation_format
        )
        request_id = task["request_id"]
        print(f"✅ 研究任务已创建，ID: {request_id}，正在生成报告...")
        
        # 轮询结果
        for _ in range(max_polls):
            result = self.get_research_result(request_id)
            if result["status"] == "completed":
                return result
            elif result["status"] == "failed":
                raise Exception(f"研究任务失败: {result.get('error', '未知错误')}")
            time.sleep(poll_interval)
        
        raise Exception(f"研究任务超时，已等待 {max_polls * poll_interval} 秒")
    
    def get_usage(self) -> Dict[str, Any]:
        """查询API用量（完全按照官方文档实现）"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
        
        # 强制禁用所有缓存
        import socket
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # 清空DNS缓存
        socket.gethostbyname.cache_clear() if hasattr(socket.gethostbyname, 'cache_clear') else None
        
        response = requests.get(
            f"{self.base_url}/usage", 
            headers=headers,
            allow_redirects=False
        )
        response.raise_for_status()
        return response.json()
    
    def format_results(self, results: Dict[str, Any], show_content: bool = True) -> str:
        """格式化搜索结果为易读文本"""
        output = []
        
        if results.get("answer"):
            output.append("📝 直接答案：")
            output.append(results["answer"])
            output.append("")
        
        output.append(f"🔍 搜索结果（共 {len(results['results'])} 条，耗时 {results['response_time']}s）：")
        output.append("=" * 80)
        
        for i, result in enumerate(results["results"], 1):
            output.append(f"{i}. {result['title']}")
            output.append(f"   🔗 {result['url']}")
            if show_content:
                output.append(f"   📄 {result['content'][:300]}..." if len(result['content']) > 300 else f"   📄 {result['content']}")
            output.append(f"   ⭐ 相关性：{result['score']:.2f}")
            output.append("")
        
        if results.get("usage"):
            output.append(f"💡 本次调用消耗 {results['usage']['credits']} 个信用点")
        
        return "\n".join(output)
    
    def format_extract_results(self, results: Dict[str, Any]) -> str:
        """格式化提取结果"""
        output = []
        output.append(f"📄 内容提取结果（共 {len(results['results'])} 个页面）：")
        output.append("=" * 80)
        
        for data in results["results"]:
            output.append(f"🌐 {data['url']}")
            output.append(f"📝 标题：{data['title']}")
            output.append(f"📄 内容摘要：{data['raw_content'][:500]}..." if len(data['raw_content']) > 500 else f"📄 内容：{data['raw_content']}")
            output.append("")
        
        if results.get("usage"):
            output.append(f"💡 本次调用消耗 {results['usage']['credits']} 个信用点")
        
        return "\n".join(output)
    
    def format_research_results(self, results: Dict[str, Any]) -> str:
        """格式化研究报告"""
        output = []
        output.append("📚 深度研究报告：")
        output.append("=" * 80)
        
        output.append(f"🆔 任务ID: {results.get('request_id', '未知')}")
        output.append(f"⚡ 状态: {results.get('status', '未知')}")
        output.append(f"⏱️  耗时: {results.get('response_time', 0)}s")
        output.append("")
        
        if results.get("content"):
            output.append("📝 报告内容：")
            output.append(results["content"])
            output.append("")
        
        if results.get("sources"):
            output.append(f"🔗 参考来源（共 {len(results['sources'])} 个）：")
            for i, source in enumerate(results["sources"], 1):
                output.append(f"{i}. {source['title']} - {source['url']}")
        
        return "\n".join(output)
    
    def format_usage(self, usage: Dict[str, Any]) -> str:
        """格式化用量信息"""
        output = []
        output.append("📊 API 用量统计：")
        output.append("=" * 80)
        
        # API Key 级别用量
        output.append("🔑 API Key 用量：")
        key_usage = usage.get("key", {})
        output.append(f"  总使用量：{key_usage.get('usage', 0)} / {key_usage.get('limit', '无限制')}")
        output.append(f"  搜索：{key_usage.get('search_usage', 0)} 次")
        output.append(f"  提取：{key_usage.get('extract_usage', 0)} 次")
        output.append(f"  爬取：{key_usage.get('crawl_usage', 0)} 次")
        output.append(f"  站点地图：{key_usage.get('map_usage', 0)} 次")
        output.append(f"  深度研究：{key_usage.get('research_usage', 0)} 次")
        output.append("")
        
        # 账户级别用量
        output.append("💳 账户套餐用量：")
        account = usage.get("account", {})
        output.append(f"  当前套餐：{account.get('current_plan', '未知')}")
        output.append(f"  套餐使用：{account.get('plan_usage', 0)} / {account.get('plan_limit', '无限制')}")
        if account.get('paygo_limit') is not None:
            output.append(f"  按量付费：{account.get('paygo_usage', 0)} / {account.get('paygo_limit', '无限制')}")
        output.append(f"  搜索：{account.get('search_usage', 0)} 次")
        output.append(f"  提取：{account.get('extract_usage', 0)} 次")
        output.append(f"  爬取：{account.get('crawl_usage', 0)} 次")
        output.append(f"  站点地图：{account.get('map_usage', 0)} 次")
        output.append(f"  深度研究：{account.get('research_usage', 0)} 次")
        
        return "\n".join(output)

def main():
    import sys
    import argparse
    
    if len(sys.argv) < 2:
        print("使用方式: python search.py <命令> [参数]")
        print("命令:")
        print("  search <关键词>   网页搜索")
        print("  extract <url1,url2>  提取指定网页内容")
        print("  crawl <根URL>  整站爬取，自动遍历所有相关页面")
        print("  research <主题>  生成深度研究报告（自动等待结果）")
        print("  get-research <任务ID>  查询已有研究任务结果")
        print("  usage  查询API用量")
        print("\n搜索选项:")
        print("  --depth <basic/advanced/fast/ultra-fast>  搜索深度")
        sys.exit(1)
    
    command = sys.argv[1]
    ts = TavilySearch()
    
    if command == "usage":
        usage_data = ts.get_usage()
        output = ts.format_usage(usage_data)
        print(output)
        sys.exit(0)
    elif command == "search":
        if len(sys.argv) < 3:
            print("错误：search 命令需要关键词参数")
            sys.exit(1)
        
        parser = argparse.ArgumentParser()
        parser.add_argument("command")
        parser.add_argument("query")
        parser.add_argument("--depth", default="basic", choices=["basic", "advanced", "fast", "ultra-fast"])
        parser.add_argument("--chunks", type=int, default=3)
        parser.add_argument("--max", type=int, default=5, dest="max_results")
        parser.add_argument("--topic", default="general", choices=["general", "news", "finance"])
        parser.add_argument("--time", default=None, choices=["day", "week", "month", "year"], dest="time_range")
        parser.add_argument("--start-date", default=None)
        parser.add_argument("--end-date", default=None)
        parser.add_argument("--answer", action="store_true", dest="include_answer")
        parser.add_argument("--raw", action="store_true", dest="include_raw_content")
        parser.add_argument("--images", action="store_true", dest="include_images")
        parser.add_argument("--image-descriptions", action="store_true", dest="include_image_descriptions")
        parser.add_argument("--favicon", action="store_true", dest="include_favicon")
        parser.add_argument("--include", default=None, dest="include_domains")
        parser.add_argument("--exclude", default=None, dest="exclude_domains")
        parser.add_argument("--country", default=None)
        parser.add_argument("--auto-params", action="store_true", dest="auto_parameters")
        parser.add_argument("--exact", action="store_true", dest="exact_match")
        parser.add_argument("--usage", action="store_true", dest="include_usage")
        parser.add_argument("--json", action="store_true")
        
        args = parser.parse_args()
        
        # 处理域名列表
        include_domains = args.include_domains.split(",") if args.include_domains else None
        exclude_domains = args.exclude_domains.split(",") if args.exclude_domains else None
        
        results = ts.search(
            query=args.query,
            search_depth=args.depth,
            chunks_per_source=args.chunks,
            max_results=args.max_results,
            topic=args.topic,
            time_range=args.time_range,
            start_date=args.start_date,
            end_date=args.end_date,
            include_answer=args.include_answer,
            include_raw_content=args.include_raw_content,
            include_images=args.include_images,
            include_image_descriptions=args.include_image_descriptions,
            include_favicon=args.include_favicon,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            country=args.country,
            auto_parameters=args.auto_parameters,
            exact_match=args.exact_match,
            include_usage=args.include_usage
        )
        
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(ts.format_results(results))
        sys.exit(0)
    elif command == "extract":
        if len(sys.argv) < 3:
            print("错误：extract 命令需要URL参数")
            sys.exit(1)
        
        parser = argparse.ArgumentParser()
        parser.add_argument("command")
        parser.add_argument("urls")
        parser.add_argument("--query", default=None)
        parser.add_argument("--chunks", type=int, default=3)
        parser.add_argument("--extract-depth", default="basic", choices=["basic", "advanced"])
        parser.add_argument("--markdown", action="store_true")
        parser.add_argument("--images", action="store_true")
        parser.add_argument("--favicon", action="store_true")
        parser.add_argument("--json", action="store_true")
        
        args = parser.parse_args()
        urls = args.urls.split(",")
        
        results = ts.extract(
            urls=urls,
            query=args.query,
            chunks_per_source=args.chunks,
            extract_depth=args.extract_depth,
            include_images=args.images,
            include_favicon=args.favicon
        )
        
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(ts.format_extract_results(results))
        sys.exit(0)
    elif command == "crawl":
        if len(sys.argv) < 3:
            print("错误：crawl 命令需要根URL参数")
            sys.exit(1)
        
        parser = argparse.ArgumentParser()
        parser.add_argument("command")
        parser.add_argument("root_url")
        parser.add_argument("--instructions", default=None)
        parser.add_argument("--max-depth", type=int, default=1)
        parser.add_argument("--max-breadth", type=int, default=20)
        parser.add_argument("--limit", type=int, default=50)
        parser.add_argument("--select-paths", default=None)
        parser.add_argument("--exclude-paths", default=None)
        parser.add_argument("--allow-external", action="store_true", default=True)
        parser.add_argument("--extract-depth", default="basic", choices=["basic", "advanced"])
        parser.add_argument("--markdown", action="store_true")
        parser.add_argument("--images", action="store_true")
        parser.add_argument("--favicon", action="store_true")
        parser.add_argument("--json", action="store_true")
        
        args = parser.parse_args()
        
        select_paths = args.select_paths.split(",") if args.select_paths else None
        exclude_paths = args.exclude_paths.split(",") if args.exclude_paths else None
        
        results = ts.crawl(
            url=args.root_url,
            instructions=args.instructions,
            max_depth=args.max_depth,
            max_breadth=args.max_breadth,
            limit=args.limit,
            select_paths=select_paths,
            exclude_paths=exclude_paths,
            allow_external=args.allow_external,
            extract_depth=args.extract_depth,
            include_images=args.images,
            include_favicon=args.favicon
        )
        
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(ts.format_crawl_results(results))
        sys.exit(0)
    elif command == "research":
        if len(sys.argv) < 3:
            print("错误：research 命令需要研究主题参数")
            sys.exit(1)
        
        parser = argparse.ArgumentParser()
        parser.add_argument("command")
        parser.add_argument("topic")
        parser.add_argument("--model", default="auto", choices=["mini", "pro", "auto"])
        parser.add_argument("--citation", default="numbered", choices=["numbered", "mla", "apa", "chicago"])
        parser.add_argument("--json", action="store_true")
        
        args = parser.parse_args()
        
        results = ts.research(
            input=args.topic,
            model=args.model,
            citation_format=args.citation
        )
        
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(ts.format_research_results(results))
        sys.exit(0)
    elif command == "get-research":
        if len(sys.argv) < 3:
            print("错误：get-research 命令需要任务ID参数")
            sys.exit(1)
        
        task_id = sys.argv[2]
        results = ts.get_research(task_id)
        
        if "--json" in sys.argv:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(ts.format_research_results(results))
        sys.exit(0)
    else:
        print(f"错误：未知命令 {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
