#!/usr/bin/env python3
"""
Info Search CLI - 舆情内容检索命令行工具
整合了API客户端和CLI功能

用法:
    python3 search_cli.py --query "热点新闻" --area "长沙" --days 7
    python3 search_cli.py --query "医疗问题" --media "微博,抖音" --sentiment negative
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# 加载 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# API配置
API_BASE_URL = "http://221.6.15.90:18011"
API_ENDPOINT = "/search-service/search"
API_KEY = os.getenv("FEEDAX_SEARCH_API_KEY", "")
DEFAULT_TIMEOUT = 30

# 输出配置
DEFAULT_OUTPUT_DIR = Path.home() / "Desktop" / "舆情搜索结果"

# 标准输出字段
STANDARD_FIELDS = ["title", "summary", "authorName", "publishTime", "platformName", "originalUrl"]

# 地域编码索引（延迟加载）
# 存储 name -> {province_code, city_code, county_code} 的映射
_AREA_CODE_INDEX: Optional[Dict[str, Dict[str, str]]] = None


def _load_area_codes() -> Dict[str, Dict[str, str]]:
    """从JSON文件加载地域编码数据，返回名称到编码信息的映射"""
    global _AREA_CODE_INDEX
    
    if _AREA_CODE_INDEX is not None:
        return _AREA_CODE_INDEX
    
    _AREA_CODE_INDEX = {}
    
    # 查找 area_codes.json 文件
    json_path = Path(__file__).parent.parent / "assets/area_codes.json"
    
    if not json_path.exists():
        return _AREA_CODE_INDEX
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 解析嵌套结构
        for province in data.get("data", []):
            province_name = province.get("name", "")
            province_code = province.get("code", "")
            
            # 添加省级
            _add_area_to_index(province_name, {
                "province_code": province_code,
                "city_code": "",
                "county_code": ""
            })
            
            # 处理市级（直辖市的children直接是区县）
            for city in province.get("children", []):
                city_name = city.get("name", "")
                city_code = city.get("code", "")
                city_children = city.get("children", [])
                
                if city_children:
                    # 有children，说明是市级
                    _add_area_to_index(city_name, {
                        "province_code": province_code,
                        "city_code": city_code,
                        "county_code": ""
                    })
                    
                    # 处理县/区级
                    for county in city_children:
                        county_name = county.get("name", "")
                        county_code = county.get("code", "")
                        _add_area_to_index(county_name, {
                            "province_code": province_code,
                            "city_code": city_code,
                            "county_code": county_code
                        })
                else:
                    # 无children，直辖市的区县
                    _add_area_to_index(city_name, {
                        "province_code": province_code,
                        "city_code": province_code,
                        "county_code": city_code
                    })
    except Exception:
        pass
    
    return _AREA_CODE_INDEX


def _add_area_to_index(name: str, info: Dict[str, str]) -> None:
    """添加地域到索引，支持多种名称变体"""
    if not name:
        return
    
    # 原始名称
    _AREA_CODE_INDEX[name] = info
    
    # 去掉后缀的简称
    for suffix in ["省", "市", "区", "县", "自治区", "自治州", "自治县", "特别行政区"]:
        if name.endswith(suffix) and len(name) > len(suffix):
            short_name = name[:-len(suffix)]
            if short_name and short_name not in _AREA_CODE_INDEX:
                _AREA_CODE_INDEX[short_name] = info


def _get_best_code(info: Dict[str, str]) -> str:
    """获取最精确的编码（优先县级 > 市级 > 省级）"""
    if info.get("county_code"):
        return info["county_code"]
    if info.get("city_code"):
        return info["city_code"]
    return info.get("province_code", "")


def _get_priority(info: Dict[str, str]) -> int:
    """计算优先级：县级=3, 市级=2, 省级=1"""
    if info.get("county_code"):
        return 3
    if info.get("city_code"):
        return 2
    return 1


def parse_area_to_codes(area_str: str) -> List[str]:
    """
    将地域名称字符串转换为国标区域编码列表
    
    Args:
        area_str: 地域名称，多个用逗号分隔，如 "北京,南京,上海"
        
    Returns:
        地域编码列表，如 ["110000", "320100", "310000"]
    """
    if not area_str:
        return []
    
    index = _load_area_codes()
    areas = [a.strip() for a in area_str.split(',') if a.strip()]
    codes = set()
    
    for area in areas:
        # 1. 直接匹配
        if area in index:
            codes.add(_get_best_code(index[area]))
            continue
        
        # 2. 组合地名解析（如"北京海淀"、"上海徐汇"）- 找最精确的匹配
        best_match = None
        best_priority = -1
        for name, info in index.items():
            if name in area:
                priority = _get_priority(info)
                if priority > best_priority:
                    best_match = info
                    best_priority = priority
        
        if best_match:
            codes.add(_get_best_code(best_match))
            continue
        
        # 3. 模糊匹配
        for name, info in index.items():
            if area in name or name in area:
                codes.add(_get_best_code(info))
                break
    
    return list(codes)


def parse_datetime_str(dt_str: str) -> Optional[int]:
    """
    解析日期时间字符串，返回毫秒时间戳
    
    Args:
        dt_str: 日期时间字符串，支持多种格式
        
    Returns:
        毫秒时间戳，解析失败返回 None
    """
    if not dt_str:
        return None
    
    dt_str = dt_str.strip()
    
    # 支持的格式
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d",
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(dt_str, fmt)
            return int(dt.timestamp() * 1000)
        except ValueError:
            continue
    
    return None


# 错误码映射
ERROR_CODES = {
    "GE1003": "未配置API Key，请前往 https://www.feedax.cn 申请，然后在项目根目录 .env 文件中配置 FEEDAX_SEARCH_API_KEY",
    "GE1004": "API Key已失效，请检查 .env 中的 FEEDAX_SEARCH_API_KEY 配置，或前往 https://www.feedax.cn 重新申请",
    "GE1005": "API Key已过期，请前往 https://www.feedax.cn 重新申请，并更新 .env 中的 FEEDAX_SEARCH_API_KEY",
    "GE1006": "API Key无效，请检查 .env 中的 FEEDAX_SEARCH_API_KEY 配置是否正确",
    "GE1007": "账户余额不足，请前往 https://www.feedax.cn 充值",
}

HTTP_ERROR_MESSAGES = {
    400: "请求参数错误，请检查输入",
    401: "未授权访问，API Key可能无效",
    403: "禁止访问，API Key可能已过期或失效",
    404: "接口不存在",
    429: "请求过于频繁，请稍后再试",
    500: "服务器内部错误",
    502: "服务暂时不可用，请稍后再试",
    503: "服务维护中，请稍后再试",
    504: "网关超时，请稍后再试",
}


def format_timestamp(ms_timestamp):
    """将毫秒时间戳转换为可读格式"""
    try:
        dt = datetime.fromtimestamp(ms_timestamp / 1000)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return str(ms_timestamp)


def display_summary(data, max_items=5):
    """在对话中展示前N条数据摘要"""
    if not data or not isinstance(data, list):
        print("暂无数据")
        return
    
    items = data[:max_items]
    total = len(data)
    
    print(f"\n{'='*60}")
    print(f"📊 搜索结果摘要（共 {total} 条，展示前 {len(items)} 条）")
    print(f"{'='*60}\n")
    
    for i, raw_item in enumerate(items, 1):
        item = normalize_item(raw_item)
        title = item['title'] or '无标题'
        
        print(f"【{i}】{item['platformName'] or '未知平台'}")
        print(f"    标题: {title[:60]}{'...' if len(title) > 60 else ''}")
        print(f"    作者: {item['authorName'] or '未知作者'}")
        print(f"    时间: {format_timestamp(item['publishTime'])}")
        if item['originalUrl']:
            print(f"    链接: {item['originalUrl']}")
        print()
    
    if total > max_items:
        print(f"... 还有 {total - max_items} 条数据，详见JSON文件\n")


def normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """提取数据项的标准字段"""
    return {field: item.get(field, "" if field != "publishTime" else 0) for field in STANDARD_FIELDS}


def save_to_json(result, query, request_body=None, output_dir=None):
    """将完整结果保存为JSON文件"""
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_query = "".join(c for c in query if c.isalnum() or c in ('_', '-'))[:20]
    filename = f"{safe_query}_{timestamp}.json"
    filepath = output_dir / filename
    
    # 转换数据为标准格式
    raw_data = result.get('data', []) if isinstance(result, dict) else []
    normalized_data = [normalize_item(item) for item in raw_data]
    
    search_info = {
        "query": query,
        "search_time": datetime.now().isoformat(),
        "total_results": len(normalized_data)
    }
    
    if request_body:
        search_info["request_body"] = request_body
    
    output_data = {
        "search_info": search_info,
        "data": normalized_data
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    return filepath


def parse_error_response(response_data: Dict[str, Any], http_code: int = None) -> Dict[str, Any]:
    """解析错误响应，返回友好的错误信息"""
    error_code = response_data.get("code") or response_data.get("errorCode")
    
    if error_code:
        if isinstance(error_code, str) and error_code in ERROR_CODES:
            return {
                "success": False,
                "code": error_code,
                "error": ERROR_CODES[error_code],
                "message": ERROR_CODES[error_code],
                "data": None
            }
        elif isinstance(error_code, int) and error_code in HTTP_ERROR_MESSAGES:
            return {
                "success": False,
                "code": f"HTTP_{error_code}",
                "error": HTTP_ERROR_MESSAGES[error_code],
                "message": HTTP_ERROR_MESSAGES[error_code],
                "data": None
            }
    
    if http_code and http_code in HTTP_ERROR_MESSAGES:
        return {
            "success": False,
            "code": f"HTTP_{http_code}",
            "error": HTTP_ERROR_MESSAGES[http_code],
            "message": HTTP_ERROR_MESSAGES[http_code],
            "data": None
        }
    
    error_msg = response_data.get("error") or response_data.get("message") or "未知错误"
    return {
        "success": False,
        "code": "UNKNOWN",
        "error": error_msg,
        "message": error_msg,
        "data": None
    }


class InfoSearchClient:
    """舆情内容检索API客户端"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or API_KEY
        self.base_url = base_url or API_BASE_URL
        self.endpoint = API_ENDPOINT
    
    def check_api_key(self) -> tuple[bool, Optional[str]]:
        """检查API Key是否有效"""
        if not self.api_key or not self.api_key.strip():
            return False, ERROR_CODES["GE1003"]
        return True, None
    
    def search_with_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """使用参数字典进行搜索"""
        is_valid, error_msg = self.check_api_key()
        if not is_valid:
            return {
                "success": False,
                "code": "GE1003",
                "error": error_msg,
                "message": error_msg,
                "data": None
            }
        
        query_string = params.get("queryString", "")
        if not query_string:
            return {
                "success": False,
                "code": "PARAM_ERROR",
                "error": "queryString不能为空",
                "message": "queryString不能为空",
                "data": None
            }
        
        payload = {
            "apiKey": self.api_key,
            "queryString": query_string,
            "size": params.get("size", 20),
            "sortField": params.get("sortField", "publish_time"),
            "sortOrder": params.get("sortOrder", "desc"),
        }
        
        # 可选参数
        optional_fields = [
            "searchAfter", "mediaNames", "messageTypes", "contentTypes",
            "sentiments", "mediaClasses", "domains", "scenes", "areaCodes",
            "noiseFlag", "verificationType", "publishTimeFrom", "publishTimeTo",
            "fansCountMin", "fansCountMax", "commentsCountMin", "commentsCountMax",
            "repostsCountMin", "repostsCountMax", "likesCountMin", "likesCountMax",
            "interactCountMin", "interactCountMax"
        ]
        
        for field in optional_fields:
            if field in params and params[field] is not None:
                payload[field] = params[field]
        
        url = f"{self.base_url}{self.endpoint}"
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers={
                    "Content-Type": "application/json; charset=UTF-8",
                    "x-api-key": self.api_key
                },
                timeout=DEFAULT_TIMEOUT
            )
            
            if response.status_code != 200:
                try:
                    error_data = response.json()
                except:
                    error_data = {"message": response.text}
                return parse_error_response(error_data, response.status_code)
            
            result = response.json()
            
            if result.get("code") not in [200, "200", None]:
                return parse_error_response(result)
            
            return {
                "success": True,
                "code": result.get("code", 200),
                "message": result.get("message", "检索成功"),
                "data": result.get("data", [])
            }
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "code": "TIMEOUT",
                "error": "请求超时，请稍后再试",
                "message": "请求超时，请稍后再试",
                "data": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "code": "CONNECTION_ERROR",
                "error": "无法连接到服务器，请检查网络或稍后再试",
                "message": "无法连接到服务器，请检查网络或稍后再试",
                "data": None
            }
        except Exception as e:
            return {
                "success": False,
                "code": "UNKNOWN_ERROR",
                "error": f"请求失败: {str(e)}",
                "message": f"请求失败: {str(e)}",
                "data": None
            }


def main():
    parser = argparse.ArgumentParser(
        description='舆情内容检索命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --query "热点新闻" --area "长沙" --days 7
  %(prog)s --query "医疗问题" --media "微博,抖音" --sentiment negative
  %(prog)s --query "交通事故" --domain "突发事件" --scene "交通事故"
        """
    )
    
    # === 必填参数 ===
    parser.add_argument('--query', '-q', required=True, help='搜索关键词 (queryString)')
    
    # === 分页与排序 (2.2) ===
    parser.add_argument('--size', '-s', type=int, default=50, help='返回条数，默认50 (size)')
    parser.add_argument('--search-after', help='深度分页游标，首次传空 (searchAfter)')
    parser.add_argument('--sort', default='publish_time',
                        choices=['publish_time', 'interact_count', 'comments_count',
                                'likes_count', 'reposts_count', 'fans_count'],
                        help='排序字段，默认按发布时间 (sortField)')
    parser.add_argument('--sort-order', default='desc', choices=['asc', 'desc'],
                        help='排序方式，默认降序 (sortOrder)')
    
    # === 内容筛选 (2.3) ===
    parser.add_argument('--media', '-m', help='媒体平台，逗号分隔 (mediaNames)')
    parser.add_argument('--author', help='作者名称，精确匹配 (authorName)')
    parser.add_argument('--msg-type', choices=['original', 'comment', 'repost'],
                        help='消息类型 (messageTypes)')
    parser.add_argument('--content-type', choices=['video', 'picture', 'text'],
                        help='内容类型 (contentTypes)')
    parser.add_argument('--sentiment', choices=['negative', 'neutral', 'positive', 'all'],
                        help='情感倾向 (sentiments)')
    parser.add_argument('--media-class', help='媒体分类：央媒/省媒/地市/商业/其他 (mediaClasses)')
    parser.add_argument('--domain', help='内容领域 (domains)')
    parser.add_argument('--scene', help='业务场景 (scenes)')
    parser.add_argument('--area', '-a', help='地域名称 (areaCodes)')
    parser.add_argument('--noise-flag', type=int, choices=[0, 1], default=0,
                        help='噪声标识：0=非噪声, 1=噪声 (noiseFlag)')
    parser.add_argument('--ai-abstract', type=int, choices=[0, 1],
                        help='摘要类型：0=算法摘要, 1=AI摘要 (aiAbstractFlag)')
    parser.add_argument('--verification', choices=['blue', 'yellow', 'normal'],
                        help='认证类型 (verificationType)')
    
    # === 时间筛选 (2.4) ===
    parser.add_argument('--days', '-d', type=int, default=7, help='时间范围（天），默认7天')
    parser.add_argument('--time-from', help='开始时间 (publishTimeFrom)，格式: yyyy-mm-dd HH:MM:SS')
    parser.add_argument('--time-to', help='结束时间 (publishTimeTo)，格式: yyyy-mm-dd HH:MM:SS')
    
    # === 互动数据筛选 (2.5) ===
    parser.add_argument('--min-interact', type=int, help='最小互动数 (interactCountMin)')
    parser.add_argument('--max-interact', type=int, help='最大互动数 (interactCountMax)')
    parser.add_argument('--min-comments', type=int, help='最小评论数 (commentsCountMin)')
    parser.add_argument('--max-comments', type=int, help='最大评论数 (commentsCountMax)')
    parser.add_argument('--min-reposts', type=int, help='最小转发数 (repostsCountMin)')
    parser.add_argument('--max-reposts', type=int, help='最大转发数 (repostsCountMax)')
    parser.add_argument('--min-likes', type=int, help='最小点赞数 (likesCountMin)')
    parser.add_argument('--max-likes', type=int, help='最大点赞数 (likesCountMax)')
    parser.add_argument('--min-fans', type=int, help='最小粉丝数 (fansCountMin)')
    parser.add_argument('--max-fans', type=int, help='最大粉丝数 (fansCountMax)')
    
    # === 输出控制 ===
    parser.add_argument('--output-dir', '-o', help='JSON文件输出目录')
    parser.add_argument('--show-count', type=int, default=5, help='对话中展示的条数，默认5条')
    
    args = parser.parse_args()
    
    # 构建搜索参数
    params = {
        "queryString": args.query,
        "size": args.size,
        "sortField": args.sort,
        "sortOrder": args.sort_order
    }
    
    # 处理深度分页游标
    if args.search_after:
        params["searchAfter"] = args.search_after
    
    # 处理时间范围
    import time as time_module
    
    if args.time_from or args.time_to:
        # 使用精确时间（内嵌解析）
        if args.time_from:
            ts = parse_datetime_str(args.time_from)
            if ts:
                params["publishTimeFrom"] = ts
            else:
                print(f"警告: 无法解析开始时间 '{args.time_from}'，使用默认时间范围", file=sys.stderr)
        
        if args.time_to:
            ts = parse_datetime_str(args.time_to)
            if ts:
                params["publishTimeTo"] = ts
            else:
                print(f"警告: 无法解析结束时间 '{args.time_to}'，使用当前时间", file=sys.stderr)
        
        # 如果只指定了一个时间，补充另一个
        if "publishTimeFrom" not in params:
            params["publishTimeFrom"] = params.get("publishTimeTo", int(time_module.time() * 1000)) - (args.days * 24 * 60 * 60 * 1000)
        if "publishTimeTo" not in params:
            params["publishTimeTo"] = int(time_module.time() * 1000)
    else:
        # 使用 days 参数
        publish_time_to = int(time_module.time() * 1000)
        publish_time_from = publish_time_to - (args.days * 24 * 60 * 60 * 1000)
        params["publishTimeFrom"] = publish_time_from
        params["publishTimeTo"] = publish_time_to
    
    # 处理地域（内嵌解析，支持省/市/区县）
    if args.area:
        codes = parse_area_to_codes(args.area)
        if codes:
            params["areaCodes"] = codes
    
    # 处理媒体平台
    if args.media:
        media_names = [m.strip() for m in args.media.split(',')]
        params["mediaNames"] = media_names
    
    # 处理作者名称
    if args.author:
        params["authorName"] = args.author
    
    # 处理情感倾向
    if args.sentiment:
        sentiment_map = {
            'negative': [-1],
            'neutral': [0],
            'positive': [1],
            'all': [-1, 0, 1]
        }
        params["sentiments"] = sentiment_map[args.sentiment]
    
    # 处理消息类型
    if args.msg_type:
        msg_type_map = {
            'original': [1],
            'comment': [2],
            'repost': [3]
        }
        params["messageTypes"] = msg_type_map[args.msg_type]
    
    # 处理领域和场景
    if args.domain:
        params["domains"] = [args.domain]
    if args.scene:
        params["scenes"] = [args.scene]
    
    # 处理媒体分类
    if args.media_class:
        params["mediaClasses"] = [args.media_class]
    
    # 处理噪声标识
    if args.noise_flag is not None:
        params["noiseFlag"] = args.noise_flag
    
    # 处理AI摘要
    if args.ai_abstract is not None:
        params["aiAbstractFlag"] = args.ai_abstract
    
    # 处理互动数筛选
    if args.min_interact:
        params["interactCountMin"] = args.min_interact
    if args.max_interact:
        params["interactCountMax"] = args.max_interact
    
    # 处理评论数筛选
    if args.min_comments:
        params["commentsCountMin"] = args.min_comments
    if args.max_comments:
        params["commentsCountMax"] = args.max_comments
    
    # 处理转发数筛选
    if args.min_reposts:
        params["repostsCountMin"] = args.min_reposts
    if args.max_reposts:
        params["repostsCountMax"] = args.max_reposts
    
    # 处理点赞数筛选
    if args.min_likes:
        params["likesCountMin"] = args.min_likes
    if args.max_likes:
        params["likesCountMax"] = args.max_likes
    
    # 处理粉丝数筛选
    if args.min_fans:
        params["fansCountMin"] = args.min_fans
    if args.max_fans:
        params["fansCountMax"] = args.max_fans
    
    # 处理内容类型
    if args.content_type:
        params["contentTypes"] = [args.content_type]
    
    # 处理认证类型
    if args.verification:
        verification_map = {
            'blue': 1,
            'yellow': 0,
            'normal': -1
        }
        params["verificationType"] = verification_map[args.verification]
    
    # 执行搜索
    try:
        client = InfoSearchClient()
        result = client.search_with_params(params)
        
        # 判断成功：code=200 或 success=True
        is_success = False
        if isinstance(result, dict):
            code = result.get('code')
            if code in [200, "200"] or result.get('success') is True:
                is_success = True
        
        if is_success:
            data = result.get('data') or []
            display_summary(data, max_items=args.show_count)
            filepath = save_to_json(result, args.query, request_body=params, output_dir=args.output_dir)
            print(f"📁 完整数据已保存至: {filepath}")
        else:
            error_msg = result.get('message') or result.get('error') or '未知错误' if isinstance(result, dict) else str(result)
            print(f"❌ 搜索失败: {error_msg}", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ 搜索失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
