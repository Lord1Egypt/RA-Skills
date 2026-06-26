#!/usr/bin/env python3
"""
Tavily Search Enhanced v1.0.0
Web搜索工具，使用Tavily API，包含缓存、错误处理和高级功能。
"""

import argparse
import json
import os
import pathlib
import re
import sys
import time
import hashlib
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any

# 配置常量
TAVILY_URL = "https://api.tavily.com/search"

# 默认值
DEFAULT_TIMEOUT = 30
DEFAULT_MAX_RESULTS = 5
DEFAULT_CACHE_TTL = 300  # 5分钟
DEFAULT_SEARCH_DEPTH = "basic"
DEFAULT_CACHE_DIR = pathlib.Path.home() / ".openclaw" / "cache" / "tavily"


class TavilySearchError(Exception):
    """Tavily搜索错误基类"""
    pass


class APIKeyError(TavilySearchError):
    """API密钥错误"""
    pass


class NetworkError(TavilySearchError):
    """网络错误"""
    pass


class Cache:
    """简单的文件缓存系统"""
    
    def __init__(self, cache_dir: pathlib.Path = DEFAULT_CACHE_DIR, ttl: int = DEFAULT_CACHE_TTL):
        self.cache_dir = cache_dir
        self.ttl = ttl
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_key(self, query: str, max_results: int, include_answer: bool, search_depth: str) -> str:
        """生成缓存键"""
        data = f"{query}_{max_results}_{include_answer}_{search_depth}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> pathlib.Path:
        """获取缓存文件路径"""
        return self.cache_dir / f"{cache_key}.json"
    
    def get(self, query: str, max_results: int, include_answer: bool, search_depth: str) -> Optional[Dict]:
        """从缓存获取数据"""
        cache_key = self._get_cache_key(query, max_results, include_answer, search_depth)
        cache_file = self._get_cache_path(cache_key)
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
            
            # 检查是否过期
            cached_time = datetime.fromisoformat(cached_data.get('_cached_at', '2000-01-01'))
            if datetime.now() - cached_time > timedelta(seconds=self.ttl):
                cache_file.unlink()  # 删除过期缓存
                return None
            
            return cached_data.get('data')
        
        except (json.JSONDecodeError, KeyError, ValueError):
            # 缓存文件损坏，删除它
            try:
                cache_file.unlink()
            except OSError:
                pass
            return None
    
    def set(self, query: str, max_results: int, include_answer: bool, search_depth: str, data: Dict):
        """设置缓存数据"""
        cache_key = self._get_cache_key(query, max_results, include_answer, search_depth)
        cache_file = self._get_cache_path(cache_key)
        
        cache_data = {
            'query': query,
            'max_results': max_results,
            'include_answer': include_answer,
            'search_depth': search_depth,
            'data': data,
            '_cached_at': datetime.now().isoformat()
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"警告: 无法写入缓存: {e}", file=sys.stderr)


def load_config() -> Dict[str, Any]:
    """从环境变量或配置文件加载所有配置"""
    # 默认值
    config_defaults = {
        "api_key": None,
        "cache_dir": DEFAULT_CACHE_DIR,
        "default_timeout": DEFAULT_TIMEOUT,
        "default_cache_ttl": DEFAULT_CACHE_TTL,
        "default_max_results": DEFAULT_MAX_RESULTS,
        "default_search_depth": DEFAULT_SEARCH_DEPTH
    }
    
    # 初始化配置为默认值
    config = config_defaults.copy()
    
    # 环境变量映射
    env_mapping = {
        "TAVILY_API_KEY": "api_key",
        "TAVILY_KEY": "api_key",
        "TAVILY_CACHE_DIR": "cache_dir",
        "TAVILY_DEFAULT_TIMEOUT": "default_timeout",
        "TAVILY_CACHE_TTL": "default_cache_ttl",
        "TAVILY_MAX_RESULTS": "default_max_results",
        "TAVILY_SEARCH_DEPTH": "default_search_depth"
    }
    
    # 1. 首先检查环境变量
    for env_var, config_key in env_mapping.items():
        value = os.environ.get(env_var)
        if value:
            if config_key == "api_key":
                config[config_key] = value.strip()
            elif config_key == "cache_dir":
                config[config_key] = pathlib.Path(value.strip())
            elif config_key in ["default_timeout", "default_cache_ttl", "default_max_results"]:
                try:
                    config[config_key] = int(value.strip())
                except ValueError:
                    print(f"警告: {env_var} 的值 '{value}' 不是有效的整数，使用默认值", file=sys.stderr)
            elif config_key == "default_search_depth":
                depth = value.strip().lower()
                if depth in ["basic", "advanced"]:
                    config[config_key] = depth
                else:
                    print(f"警告: {env_var} 的值 '{value}' 无效，必须是 'basic' 或 'advanced'，使用默认值", file=sys.stderr)
    
    # 2. 检查 ~/.openclaw/.env 配置文件
    env_path = pathlib.Path.home() / ".openclaw" / ".env"
    if env_path.exists():
        try:
            txt = env_path.read_text(encoding="utf-8", errors="ignore")
            file_config = {}
            
            # 从配置文件读取所有配置项
            for env_var, config_key in env_mapping.items():
                pattern = rf"^\s*{env_var}\s*=\s*(.+?)\s*$"
                m = re.search(pattern, txt, re.M | re.I)
                if m:
                    value = m.group(1).strip().strip('"').strip("'")
                    if value:
                        file_config[config_key] = value
            
            # 应用配置文件中的设置（但环境变量优先级更高）
            for config_key, value in file_config.items():
                # 如果环境变量已经设置了此配置，跳过（环境变量优先级更高）
                if config_key == "api_key" and config["api_key"]:
                    continue
                elif config_key in env_mapping.values() and config[config_key] != config_defaults.get(config_key):
                    # 如果环境变量修改了默认值，跳过
                    continue
                
                # 应用配置文件中的值
                if config_key == "api_key":
                    config[config_key] = value
                elif config_key == "cache_dir":
                    config[config_key] = pathlib.Path(value)
                elif config_key in ["default_timeout", "default_cache_ttl", "default_max_results"]:
                    try:
                        config[config_key] = int(value)
                    except ValueError:
                        print(f"警告: 配置文件中的 {[k for k,v in env_mapping.items() if v==config_key][0]} 值 '{value}' 无效，使用默认值", file=sys.stderr)
                elif config_key == "default_search_depth":
                    depth = value.lower()
                    if depth in ["basic", "advanced"]:
                        config[config_key] = depth
                    else:
                        print(f"警告: 配置文件中的 TAVILY_SEARCH_DEPTH 值 '{value}' 无效，必须是 'basic' 或 'advanced'，使用默认值", file=sys.stderr)
                        
        except Exception as e:
            print(f"警告: 读取.env文件时出错: {e}", file=sys.stderr)
    
    return config


def validate_query(query: str) -> bool:
    """验证搜索查询"""
    if not query or not query.strip():
        return False
    
    # 检查查询长度
    if len(query.strip()) < 2:
        return False
    
    # 检查是否只包含空白字符
    if not re.search(r'\w', query):
        return False
    
    return True


def tavily_search(
    query: str, 
    max_results: int = None, 
    include_answer: bool = False, 
    search_depth: str = None,
    timeout: int = None,
    use_cache: bool = True,
    cache_ttl: int = None,
    verbose: bool = False
) -> Dict:
    """
    执行Tavily搜索
    
    Args:
        query: 搜索查询
        max_results: 最大结果数（如为None则使用配置默认值）
        include_answer: 是否包含答案
        search_depth: 搜索深度 (basic/advanced)（如为None则使用配置默认值）
        timeout: 请求超时时间（如为None则使用配置默认值）
        use_cache: 是否使用缓存
        cache_ttl: 缓存TTL（秒）（如为None则使用配置默认值）
        verbose: 详细模式
    
    Returns:
        搜索结果字典
    """
    
    # 加载配置
    config = load_config()
    
    # 使用配置默认值填充未提供的参数
    if max_results is None:
        max_results = config["default_max_results"]
    if search_depth is None:
        search_depth = config["default_search_depth"]
    if timeout is None:
        timeout = config["default_timeout"]
    if cache_ttl is None:
        cache_ttl = config["default_cache_ttl"]
    
    # 验证查询
    if not validate_query(query):
        raise ValueError("无效的搜索查询")
    
    # 检查API密钥
    key = config["api_key"]
    if not key:
        raise APIKeyError(
            "未找到Tavily API密钥。请设置以下之一：\n"
            "1. 环境变量: export TAVILY_API_KEY='your_key'\n"
            "2. 添加到 ~/.openclaw/.env 文件: TAVILY_API_KEY=your_key"
        )
    
    # 检查缓存
    if use_cache:
        cache = Cache(cache_dir=config["cache_dir"], ttl=cache_ttl)
        cached_result = cache.get(query, max_results, include_answer, search_depth)
        if cached_result:
            if verbose:
                print("从缓存加载结果", file=sys.stderr)
            return cached_result
    
    # 准备请求数据
    payload = {
        "api_key": key,
        "query": query,
        "max_results": min(max_results, 10),  # Tavily限制最大10个结果
        "search_depth": search_depth,
        "include_answer": bool(include_answer),
        "include_images": False,
        "include_raw_content": False,
    }
    
    if verbose:
        print(f"发送请求到Tavily API...", file=sys.stderr)
        print(f"查询: {query}", file=sys.stderr)
        print(f"参数: {json.dumps(payload, indent=2)}", file=sys.stderr)
    
    # 发送请求
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        TAVILY_URL,
        data=data,
        headers={
            "Content-Type": "application/json", 
            "Accept": "application/json",
            "User-Agent": "OpenClaw-Tavily-Search/1.0.0"
        },
        method="POST",
    )
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status_code = resp.getcode()
            body = resp.read().decode("utf-8", errors="replace")
            
            if verbose:
                print(f"响应状态: {status_code}", file=sys.stderr)
                print(f"响应长度: {len(body)} 字符", file=sys.stderr)
            
            # 解析响应
            try:
                obj = json.loads(body)
            except json.JSONDecodeError as e:
                raise TavilySearchError(f"Tavily返回了无效的JSON响应: {e}\n响应内容: {body[:500]}")
            
            # 检查错误
            if "error" in obj:
                error_msg = obj.get("error", "未知错误")
                raise TavilySearchError(f"Tavily API错误: {error_msg}")
            
            # 构建输出
            out = {
                "query": query,
                "answer": obj.get("answer"),
                "results": [],
                "metadata": {
                    "total_results": len(obj.get("results") or []),
                    "search_depth": search_depth,
                    "cached": False,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            for r in (obj.get("results") or [])[:max_results]:
                out["results"].append({
                    "title": r.get("title", "").strip() or "无标题",
                    "url": r.get("url", ""),
                    "content": r.get("content", "").strip(),
                    "score": r.get("score", 0.0)
                })
            
            if not include_answer:
                out.pop("answer", None)
            
            # 保存到缓存
            if use_cache:
                cache.set(query, max_results, include_answer, search_depth, out)
                out["metadata"]["cached"] = False  # 这是新结果，不是从缓存来的
            
            return out
            
    except urllib.error.URLError as e:
        raise NetworkError(f"网络错误: {e}")
    except TimeoutError:
        raise NetworkError(f"请求超时 (超时时间: {timeout}秒)")
    except Exception as e:
        raise TavilySearchError(f"搜索过程中发生错误: {e}")


def to_brave_like(obj: dict) -> dict:
    """转换为Brave搜索兼容格式"""
    results = []
    for r in obj.get("results", []) or []:
        results.append({
            "title": r.get("title"),
            "url": r.get("url"),
            "snippet": r.get("content"),
            "score": r.get("score", 0.0)
        })
    
    out = {
        "query": obj.get("query"),
        "results": results,
        "metadata": obj.get("metadata", {})
    }
    
    if "answer" in obj:
        out["answer"] = obj.get("answer")
    
    return out


def to_markdown(obj: dict) -> str:
    """转换为Markdown格式"""
    lines = []
    
    # 添加答案（如果有）
    if obj.get("answer"):
        lines.append("## 📝 答案摘要")
        lines.append(obj["answer"].strip())
        lines.append("")
    
    # 添加结果
    if obj.get("results"):
        lines.append("## 🔍 搜索结果")
        for i, r in enumerate(obj.get("results", []) or [], 1):
            title = r.get("title", "").strip() or r.get("url", "") or "(无标题)"
            url = r.get("url", "")
            snippet = r.get("content", "").strip()
            score = r.get("score", 0.0)
            
            lines.append(f"{i}. **{title}**")
            if url:
                lines.append(f"   🔗 {url}")
            if snippet:
                # 限制摘要长度
                if len(snippet) > 200:
                    snippet = snippet[:197] + "..."
                lines.append(f"   📄 {snippet}")
            if score > 0:
                lines.append(f"   ⭐ 相关性: {score:.2f}")
            lines.append("")
    
    # 添加元数据
    metadata = obj.get("metadata", {})
    if metadata:
        lines.append("---")
        lines.append(f"*搜索时间: {metadata.get('timestamp', '未知')}*")
        lines.append(f"*搜索深度: {metadata.get('search_depth', 'basic')}*")
        lines.append(f"*总结果数: {metadata.get('total_results', 0)}*")
        if metadata.get('cached'):
            lines.append("*📦 从缓存加载*")
    
    return "\n".join(lines).strip() + "\n"


def to_simple_text(obj: dict) -> str:
    """转换为简单文本格式"""
    lines = []
    
    if obj.get("answer"):
        lines.append(f"答案: {obj['answer'].strip()}")
        lines.append("")
    
    for i, r in enumerate(obj.get("results", []) or [], 1):
        title = r.get("title", "").strip() or "无标题"
        url = r.get("url", "")
        lines.append(f"{i}. {title}")
        if url:
            lines.append(f"   链接: {url}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Tavily Web搜索工具 v1.0.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --query "OpenClaw是什么" --max-results 3
  %(prog)s -q "AI发展" -m 5 --include-answer --format md
  %(prog)s -q "Python教程" --search-depth advanced --timeout 45
  %(prog)s -q "常见问题" --cache-ttl 600 --no-cache
        """
    )
    
    # 必需参数（除非清除缓存）
    parser.add_argument(
        "--query", "-q",
        required=False,
        help="搜索查询字符串"
    )
    
    # 加载配置以获取默认值
    config = load_config()
    
    # 可选参数
    parser.add_argument(
        "--max-results", "-m",
        type=int,
        default=None,
        help=f"最大结果数量 (默认: {config['default_max_results']}, 范围: 1-10)"
    )
    
    parser.add_argument(
        "--include-answer", "-a",
        action="store_true",
        help="包含答案摘要"
    )
    
    parser.add_argument(
        "--search-depth",
        default=None,
        choices=["basic", "advanced"],
        help=f"搜索深度 (默认: {config['default_search_depth']})"
    )
    
    parser.add_argument(
        "--format",
        default="raw",
        choices=["raw", "brave", "md", "text"],
        help="输出格式 (默认: raw)"
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        default=None,
        help=f"请求超时时间（秒）(默认: {config['default_timeout']})"
    )
    
    parser.add_argument(
        "--cache-ttl",
        type=int,
        default=None,
        help=f"缓存时间（秒）(默认: {config['default_cache_ttl']})"
    )
    
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="禁用缓存"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="详细输出模式"
    )
    
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="清除所有缓存"
    )
    
    args = parser.parse_args()
    
    # 清除缓存
    if args.clear_cache:
        try:
            import shutil
            cache_dir = config["cache_dir"]
            if cache_dir.exists():
                shutil.rmtree(cache_dir)
                print(f"✅ 缓存已清除: {cache_dir}", file=sys.stderr)
            else:
                print(f"ℹ️  缓存目录不存在: {cache_dir}", file=sys.stderr)
            return
        except Exception as e:
            print(f"❌ 清除缓存失败: {e}", file=sys.stderr)
            sys.exit(1)
    
    # 检查必需参数
    if not args.query:
        print("错误: 必须提供 --query 参数", file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    
    # 验证参数
    max_results = args.max_results or config["default_max_results"]
    timeout = args.timeout or config["default_timeout"]
    cache_ttl = args.cache_ttl or config["default_cache_ttl"]
    search_depth = args.search_depth or config["default_search_depth"]
    
    if max_results < 1 or max_results > 10:
        print("错误: max-results 必须在 1-10 之间", file=sys.stderr)
        sys.exit(1)
    
    if timeout < 1:
        print("错误: timeout 必须大于0", file=sys.stderr)
        sys.exit(1)
    
    try:
        # 执行搜索
        result = tavily_search(
            query=args.query,
            max_results=max_results,
            include_answer=args.include_answer,
            search_depth=search_depth,
            timeout=timeout,
            use_cache=not args.no_cache,
            cache_ttl=cache_ttl,
            verbose=args.verbose
        )
        
        # 根据格式输出
        if args.format == "md":
            sys.stdout.write(to_markdown(result))
        elif args.format == "text":
            sys.stdout.write(to_simple_text(result))
        elif args.format == "brave":
            result = to_brave_like(result)
            json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
            sys.stdout.write("\n")
        else:  # raw
            json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
            sys.stdout.write("\n")
        
        # 在详细模式下显示统计信息
        if args.verbose:
            metadata = result.get("metadata", {})
            print(f"\n📊 统计信息:", file=sys.stderr)
            print(f"   查询: {args.query}", file=sys.stderr)
            print(f"   结果数: {len(result.get('results', []))}", file=sys.stderr)
            print(f"   搜索深度: {args.search_depth or config['default_search_depth']}", file=sys.stderr)
            print(f"   缓存: {'启用' if not args.no_cache else '禁用'}", file=sys.stderr)
            if metadata.get('cached'):
                print(f"   来源: 缓存", file=sys.stderr)
            else:
                print(f"   来源: API请求", file=sys.stderr)
            print(f"   时间戳: {metadata.get('timestamp', '未知')}", file=sys.stderr)
            
            # 显示配置信息
            print(f"\n⚙️  配置信息:", file=sys.stderr)
            print(f"   缓存目录: {config['cache_dir']}", file=sys.stderr)
            print(f"   默认超时: {config['default_timeout']}秒", file=sys.stderr)
            print(f"   默认缓存TTL: {config['default_cache_ttl']}秒", file=sys.stderr)
            print(f"   默认最大结果: {config['default_max_results']}", file=sys.stderr)
            print(f"   默认搜索深度: {config['default_search_depth']}", file=sys.stderr)
            print(f"\n🎯 实际使用的参数:", file=sys.stderr)
            print(f"   最大结果: {max_results}", file=sys.stderr)
            print(f"   搜索深度: {search_depth}", file=sys.stderr)
            print(f"   超时时间: {timeout}秒", file=sys.stderr)
            print(f"   缓存TTL: {cache_ttl}秒", file=sys.stderr)
    
    except APIKeyError as e:
        print(f"❌ API密钥错误: {e}", file=sys.stderr)
        sys.exit(1)
    except NetworkError as e:
        print(f"🌐 网络错误: {e}", file=sys.stderr)
        sys.exit(1)
    except TavilySearchError as e:
        print(f"🔍 搜索错误: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"⚠️  参数错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"💥 未知错误: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()