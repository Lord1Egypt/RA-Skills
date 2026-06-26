#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
舆情报告生成 CLI 工具
基于 /search-service/report 接口封装

使用方法:
    python3 scripts/report_cli.py --query "关键词" [选项]

示例:
    python3 scripts/report_cli.py --query "(南京|金陵)&(医疗|卫生)" --days 3 --area "南京" --full-analysis
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

import requests
from dotenv import load_dotenv

# 加载 .env 文件（从脚本所在目录向上两级找到项目根目录）
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
load_dotenv(dotenv_path=PROJECT_ROOT / ".env", override=True)

# 固定 API 根地址
API_BASE_URL = "http://221.6.15.90:18011"
REPORT_ENDPOINT = "/search-service/report"
DEFAULT_API_KEY = (
    os.getenv("FEEDAX_REPORT_API_KEY", "").strip()
    or os.getenv("FEEDAX_SEARCH_API_KEY", "").strip()
)
DEFAULT_OUTPUT_DIR = os.path.expanduser("~/Desktop/舆情分析报告")


# ============== 地域解析功能 ==============

@dataclass
class AreaCodeResult:
    """地域编码查询结果"""
    province: str
    province_code: str
    city: str
    city_code: str
    county: str
    county_code: str
    
    def get_code(self) -> str:
        """获取最精确的编码（优先县级 > 市级 > 省级）"""
        if self.county_code and self.county_code != self.city_code:
            return self.county_code
        if self.city_code and self.city_code != self.province_code:
            return self.city_code
        return self.province_code
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "province": self.province,
            "province_code": self.province_code,
            "city": self.city,
            "city_code": self.city_code,
            "county": self.county,
            "county_code": self.county_code,
        }


_AREA_CODE_INDEX: Optional[Dict[str, AreaCodeResult]] = None
_AREA_CODE_BY_CODE: Optional[Dict[str, AreaCodeResult]] = None


def _load_area_codes() -> None:
    """从 JSON 文件加载地域编码数据"""
    global _AREA_CODE_INDEX, _AREA_CODE_BY_CODE
    
    if _AREA_CODE_INDEX is not None:
        return
    
    _AREA_CODE_INDEX = {}
    _AREA_CODE_BY_CODE = {}
    
    json_path = Path(__file__).parent.parent / "assets/area_codes.json"
    
    if not json_path.exists():
        return
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for province in data.get("data", []):
            province_name = province.get("name", "")
            province_code = province.get("code", "")
            
            result = AreaCodeResult(
                province=province_name,
                province_code=province_code,
                city="",
                city_code="",
                county="",
                county_code=""
            )
            _add_to_index(province_name, result)
            _AREA_CODE_BY_CODE[province_code] = result
            
            for city in province.get("children", []):
                city_name = city.get("name", "")
                city_code = city.get("code", "")
                city_children = city.get("children", [])
                
                if city_children:
                    city_result = AreaCodeResult(
                        province=province_name,
                        province_code=province_code,
                        city=city_name,
                        city_code=city_code,
                        county="",
                        county_code=""
                    )
                    _add_to_index(city_name, city_result)
                    _AREA_CODE_BY_CODE[city_code] = city_result
                    
                    for county in city_children:
                        county_name = county.get("name", "")
                        county_code = county.get("code", "")
                        
                        county_result = AreaCodeResult(
                            province=province_name,
                            province_code=province_code,
                            city=city_name,
                            city_code=city_code,
                            county=county_name,
                            county_code=county_code
                        )
                        _add_to_index(county_name, county_result)
                        _AREA_CODE_BY_CODE[county_code] = county_result
                else:
                    county_result = AreaCodeResult(
                        province=province_name,
                        province_code=province_code,
                        city=province_name,
                        city_code=province_code,
                        county=city_name,
                        county_code=city_code
                    )
                    _add_to_index(city_name, county_result)
                    _AREA_CODE_BY_CODE[city_code] = county_result
    except Exception:
        pass


def _add_to_index(name: str, result: AreaCodeResult) -> None:
    """添加到索引，支持多种名称变体"""
    if not name:
        return
    
    _AREA_CODE_INDEX[name] = result
    
    for suffix in ["省", "市", "区", "县", "自治区", "自治州", "自治县", "特别行政区"]:
        if name.endswith(suffix) and len(name) > len(suffix):
            short_name = name[:-len(suffix)]
            if short_name and short_name not in _AREA_CODE_INDEX:
                _AREA_CODE_INDEX[short_name] = result


def search_area_code(name: str) -> Dict[str, Any]:
    """搜索地域编码"""
    _load_area_codes()
    
    results: List[AreaCodeResult] = []
    name = name.strip()
    if not name:
        return {"query": name, "count": 0, "results": []}
    
    if name in _AREA_CODE_INDEX:
        results.append(_AREA_CODE_INDEX[name])
    
    if not results:
        best_match = None
        best_priority = -1
        for key, value in _AREA_CODE_INDEX.items():
            if key in name:
                if value.county_code:
                    priority = 3
                elif value.city_code:
                    priority = 2
                else:
                    priority = 1
                
                if priority > best_priority:
                    best_match = value
                    best_priority = priority
        if best_match:
            results.append(best_match)
    
    if not results:
        for key, value in _AREA_CODE_INDEX.items():
            if name in key or key in name:
                results.append(value)
                break
    
    return {
        "query": name,
        "count": len(results),
        "results": [r.to_dict() for r in results]
    }


def parse_area_codes(area_names: List[str]) -> List[str]:
    """
    将地域名称列表转换为国标区域编码列表
    
    Args:
        area_names: 地域名称列表，如 ["北京", "上海", "江苏"]
        
    Returns:
        地域编码列表，如 ["110000", "310000", "320000"]
    """
    if not area_names:
        return []
    
    codes = set()
    for name in area_names:
        result = search_area_code(name)
        for r in result["results"]:
            if r.get("county_code"):
                codes.add(r["county_code"])
            elif r.get("city_code"):
                codes.add(r["city_code"])
            elif r.get("province_code"):
                codes.add(r["province_code"])
    
    return list(codes)


def parse_area(area_str: str) -> tuple:
    """
    解析地域参数，返回 (area_codes, area_name)
    
    Args:
        area_str: 地域名称，多个用逗号分隔
        
    Returns:
        (area_codes, area_name): 地域编码列表和地域名称
    """
    if not area_str:
        return [], None
    
    area_names = [a.strip() for a in area_str.split(",") if a.strip()]
    area_codes = parse_area_codes(area_names)
    area_name = "、".join(area_names)
    
    return area_codes, area_name


# ============== 地域解析功能结束 ==============


def get_default_aggregation_types():
    """默认聚合维度"""
    return ["sentiment", "keywords", "media_name", "area_code_province", "publish_time_histogram"]


def get_full_aggregation_types():
    """全维度聚合"""
    return ["sentiment", "area_code_province", "media_class", "verification_type", 
            "keywords", "media_name", "channel", "publish_time_histogram"]


def format_timestamp(ts):
    """格式化时间戳"""
    if not ts:
        return "未知时间"
    try:
        dt = datetime.fromtimestamp(ts / 1000)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return str(ts)


def parse_datetime(dt_str):
    """解析日期时间字符串为毫秒时间戳"""
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d"
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(dt_str, fmt)
            return int(dt.timestamp() * 1000)
        except ValueError:
            continue
    raise ValueError(f"无法解析时间格式: {dt_str}")


def get_section_number(num):
    """获取中文章节编号"""
    chinese_nums = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二"]
    return chinese_nums[num] if num < len(chinese_nums) else str(num)


def parse_sentiment(sentiment_str):
    """解析情感参数"""
    mapping = {
        "negative": [-1], "负面": [-1], "-1": [-1],
        "neutral": [0], "中性": [0], "0": [0],
        "positive": [1], "正面": [1], "1": [1],
        "all": [], "全部": []
    }
    return mapping.get(sentiment_str.lower(), [])


def parse_msg_type(msg_type_str):
    """解析消息类型"""
    mapping = {
        "original": [1], "原发": [1], "1": [1],
        "comment": [2], "评论": [2], "2": [2],
        "repost": [3], "转发": [3], "3": [3],
        "all": [1, 2, 3], "全部": [1, 2, 3]
    }
    return mapping.get(msg_type_str.lower(), [1])


def parse_content_type(content_type_str):
    """解析内容类型"""
    mapping = {
        "video": ["video"], "视频": ["video"],
        "picture": ["picture"], "图片": ["picture"],
        "text": ["text"], "文字": ["text"],
        "all": [], "全部": []
    }
    return mapping.get(content_type_str.lower(), [])


def parse_verification(verification_str):
    """解析认证类型"""
    mapping = {
        "blue": 1, "蓝v": 1, "蓝V": 1, "官方": 1,
        "yellow": 0, "黄v": 0, "黄V": 0,
        "normal": -1, "普通": -1
    }
    return mapping.get(verification_str, None)


def call_report_api(query, **kwargs):
    """调用报告API"""
    if not DEFAULT_API_KEY:
        print("❌ 错误: 未配置 API Key")
        print("   请在环境变量或 .env 中设置 FEEDAX_REPORT_API_KEY（或旧名 FEEDAX_SEARCH_API_KEY）")
        print("   或前往 https://www.feedax.cn 申请")
        return None
    
    payload = {
        "queryString": query,
        "size": min(kwargs.get("size", 10), 20),
        "sortField": kwargs.get("sort_field", "publish_time"),
        "sortOrder": kwargs.get("sort_order", "desc"),
        "hotArticles": kwargs.get("hot_articles", True),
        "aggregationTypes": kwargs.get("aggregation_types") or get_default_aggregation_types()
    }
    
    if kwargs.get("media_names"):
        payload["mediaNames"] = kwargs["media_names"]
    if kwargs.get("author_name"):
        payload["authorName"] = kwargs["author_name"]
    if kwargs.get("message_types"):
        payload["messageTypes"] = kwargs["message_types"]
    if kwargs.get("content_types"):
        payload["contentTypes"] = kwargs["content_types"]
    if kwargs.get("sentiments"):
        payload["sentiments"] = kwargs["sentiments"]
    if kwargs.get("media_classes"):
        payload["mediaClasses"] = kwargs["media_classes"]
    if kwargs.get("domains"):
        payload["domains"] = kwargs["domains"]
    if kwargs.get("scenes"):
        payload["scenes"] = kwargs["scenes"]
    if kwargs.get("area_codes"):
        payload["areaCodes"] = kwargs["area_codes"]
    if kwargs.get("verification_type") is not None:
        payload["verificationType"] = kwargs["verification_type"]
    if kwargs.get("time_from"):
        payload["timeFrom"] = kwargs["time_from"]
    if kwargs.get("time_to"):
        payload["timeTo"] = kwargs["time_to"]
    if kwargs.get("interact_count_min"):
        payload["interactCountMin"] = kwargs["interact_count_min"]
    if kwargs.get("interact_count_max"):
        payload["interactCountMax"] = kwargs["interact_count_max"]
    if kwargs.get("comments_count_min"):
        payload["commentsCountMin"] = kwargs["comments_count_min"]
    if kwargs.get("comments_count_max"):
        payload["commentsCountMax"] = kwargs["comments_count_max"]
    
    try:
        print("\n🔄 正在调用API...")
        response = requests.post(
            f"{API_BASE_URL}{REPORT_ENDPOINT}",
            json=payload,
            headers={"Content-Type": "application/json; charset=UTF-8", "x-api-key": DEFAULT_API_KEY},
            timeout=30
        )
        
        if response.status_code == 401:
            print("❌ API Key 无效或已过期")
            return None
        if response.status_code == 403:
            print("❌ API Key 权限不足")
            return None
        if response.status_code != 200:
            print(f"❌ API请求失败: HTTP {response.status_code}")
            return None
        
        result = response.json()
        result["_request_params"] = payload  # 保存请求参数
        return result
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请稍后重试")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ 网络连接失败，请检查网络")
        return None
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        return None


def display_report_summary(data, query):
    """在终端显示报告摘要"""
    if not data:
        print("暂无数据")
        return
    
    total = data.get("total", 0)
    aggregation = data.get("aggregation", {}) or {}
    
    print("\n" + "="*60)
    print("📊 舆情分析报告摘要")
    print("="*60)
    print(f"\n查询关键词: {query}")
    print(f"总数据量: {total:,} 条")
    
    sentiment_dist = aggregation.get("sentimentDistribution", [])
    if sentiment_dist:
        print("\n📈 情感倾向分布:")
        for item in sentiment_dist:
            key, count = item.get("key", ""), item.get("docCount", 0)
            pct = (count / total * 100) if total > 0 else 0
            print(f"   {key}: {count:,} 条 ({pct:.1f}%)")
    
    area_dist = aggregation.get("areaCodeProvinceDistribution", [])
    if area_dist:
        print("\n🗺️ 地域分布 TOP5:")
        for i, item in enumerate(area_dist[:5], 1):
            print(f"   {i}. {item.get('key', '')}: {item.get('docCount', 0):,} 条")
    
    keyword_dist = aggregation.get("keywordsDistribution", [])
    if keyword_dist:
        print("\n🔑 关键词 TOP10:")
        keywords = [item.get("key", "") for item in keyword_dist[:10]]
        print(f"   {', '.join(keywords)}")
    
    media_dist = aggregation.get("mediaNameDistribution", [])
    if media_dist:
        print("\n📺 主要媒体平台:")
        for i, item in enumerate(media_dist[:5], 1):
            print(f"   {i}. {item.get('key', '')}: {item.get('docCount', 0):,} 条")
    
    print("\n" + "="*60 + "\n")


def generate_markdown_report(data, query, output_path):
    """生成Markdown格式报告"""
    total = data.get("total", 0)
    aggregation = data.get("aggregation", {}) or {}
    articles = data.get("articles", [])
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    has_data = {k: v for k, v in aggregation.items() if v is not None and isinstance(v, list) and len(v) > 0}
    
    md = f"""# 舆情分析报告

**生成时间**: {now}  
**查询关键词**: {query}  
**总数据量**: {total:,} 条

---

## 一、报告概览

本次分析共采集到 **{total:,}** 条相关舆情数据。

"""
    
    section_num = 2
    
    if "sentimentDistribution" in has_data:
        md += f"---\n\n## {get_section_number(section_num)}、情感倾向分析\n\n"
        section_num += 1
        md += "| 情感类型 | 数量 | 占比 |\n|---------|------|------|\n"
        for item in has_data["sentimentDistribution"]:
            key, count = item.get("key", ""), item.get("docCount", 0)
            pct = (count / total * 100) if total > 0 else 0
            md += f"| {key} | {count:,} | {pct:.1f}% |\n"
        md += "\n"
    
    if "areaCodeProvinceDistribution" in has_data:
        md += f"---\n\n## {get_section_number(section_num)}、地域分布分析\n\n"
        section_num += 1
        md += "### TOP10 省份/地区\n\n| 排名 | 省份/地区 | 数量 |\n|-----|----------|------|\n"
        for i, item in enumerate(has_data["areaCodeProvinceDistribution"][:10], 1):
            md += f"| {i} | {item.get('key', '')} | {item.get('docCount', 0):,} |\n"
        md += "\n"
    
    if "keywordsDistribution" in has_data:
        md += f"---\n\n## {get_section_number(section_num)}、关键词分析\n\n"
        section_num += 1
        md += "### TOP20 关键词\n\n| 排名 | 关键词 | 出现次数 |\n|-----|--------|---------|\n"
        for i, item in enumerate(has_data["keywordsDistribution"][:20], 1):
            md += f"| {i} | {item.get('key', '')} | {item.get('docCount', 0):,} |\n"
        md += "\n"
    
    if "mediaNameDistribution" in has_data:
        md += f"---\n\n## {get_section_number(section_num)}、媒体平台分布\n\n"
        section_num += 1
        md += "### TOP10 媒体平台\n\n| 排名 | 媒体平台 | 数量 |\n|-----|---------|------|\n"
        for i, item in enumerate(has_data["mediaNameDistribution"][:10], 1):
            md += f"| {i} | {item.get('key', '')} | {item.get('docCount', 0):,} |\n"
        md += "\n"
    
    if "mediaClassDistribution" in has_data:
        md += f"---\n\n## {get_section_number(section_num)}、媒体分类分布\n\n"
        section_num += 1
        md += "| 媒体分类 | 数量 | 占比 |\n|---------|------|------|\n"
        for item in has_data["mediaClassDistribution"]:
            key, count = item.get("key", ""), item.get("docCount", 0)
            pct = (count / total * 100) if total > 0 else 0
            md += f"| {key} | {count:,} | {pct:.1f}% |\n"
        md += "\n"
    
    if "verificationTypeDistribution" in has_data:
        md += f"---\n\n## {get_section_number(section_num)}、认证类型分布\n\n"
        section_num += 1
        md += "| 认证类型 | 数量 | 占比 |\n|---------|------|------|\n"
        for item in has_data["verificationTypeDistribution"]:
            key, count = item.get("key", ""), item.get("docCount", 0)
            pct = (count / total * 100) if total > 0 else 0
            md += f"| {key} | {count:,} | {pct:.1f}% |\n"
        md += "\n"
    
    if "channelDistribution" in has_data:
        md += f"---\n\n## {get_section_number(section_num)}、通道分布\n\n"
        section_num += 1
        md += "| 通道 | 数量 |\n|-----|------|\n"
        for item in has_data["channelDistribution"][:10]:
            md += f"| {item.get('key', '')} | {item.get('docCount', 0):,} |\n"
        md += "\n"
    
    if "publishTimeTrend" in has_data:
        md += f"---\n\n## {get_section_number(section_num)}、时间趋势分析\n\n"
        section_num += 1
        md += "| 时间 | 数量 |\n|-----|------|\n"
        for item in has_data["publishTimeTrend"][-24:]:
            time_str = format_timestamp(item.get("key"))
            md += f"| {time_str} | {item.get('docCount', 0):,} |\n"
        md += "\n"
    
    if articles:
        md += f"---\n\n## {get_section_number(section_num)}、热文列表\n\n"
        section_num += 1
        for i, article in enumerate(articles[:10], 1):
            title = article.get("title", "无标题")
            author = article.get("authorName", "未知")
            media = article.get("mediaName", "未知")
            pub_time = format_timestamp(article.get("publishTime"))
            interact = article.get("interactCount", 0)
            url = article.get("url", "")
            
            md += f"### {i}. {title}\n\n"
            md += f"- **作者**: {author}\n"
            md += f"- **平台**: {media}\n"
            md += f"- **发布时间**: {pub_time}\n"
            md += f"- **互动数**: {interact:,}\n"
            if url:
                md += f"- **链接**: {url}\n"
            md += "\n"
    
    md += "---\n\n*报告由舆情分析系统自动生成*\n"
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)
    
    return output_path


def save_json_report(data, output_path):
    """保存JSON格式报告"""
    # report_info = API调用参数
    request_params = data.get("_request_params", {})
    request_params["report_time"] = datetime.now().isoformat()
    request_params["total"] = data.get("total", 0)
    
    report = {
        "report_info": request_params,
        "data": {
            "articles": data.get("articles", []),
            "aggregation": data.get("aggregation", {})
        }
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    return output_path


def generate_html_report(data, query, output_path):
    """生成HTML格式报告"""
    total = data.get("total", 0)
    aggregation = data.get("aggregation", {}) or {}
    articles = data.get("articles", [])
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 情感分布数据
    sentiment_data = aggregation.get("sentimentDistribution", [])
    negative_count = sum(item.get("docCount", 0) for item in sentiment_data if item.get("key") == "负面")
    neutral_count = sum(item.get("docCount", 0) for item in sentiment_data if item.get("key") == "中性")
    positive_count = sum(item.get("docCount", 0) for item in sentiment_data if item.get("key") == "正面")
    
    negative_pct = (negative_count / total * 100) if total > 0 else 0
    neutral_pct = (neutral_count / total * 100) if total > 0 else 0
    positive_pct = (positive_count / total * 100) if total > 0 else 0
    
    # 确定主要情感倾向
    if negative_pct >= neutral_pct and negative_pct >= positive_pct:
        main_sentiment = "负面"
        sentiment_color = "#ff6b6b"
    elif positive_pct >= neutral_pct:
        main_sentiment = "正面"
        sentiment_color = "#26de81"
    else:
        main_sentiment = "中性"
        sentiment_color = "#feca57"
    
    # 渠道分布
    channel_data = aggregation.get("channelDistribution") or []
    channel_rows = ""
    for item in channel_data[:10]:
        key = item.get("key", "")
        count = item.get("docCount", 0)
        pct = (count / total * 100) if total > 0 else 0
        channel_rows += f'<tr><td>{key}</td><td>{count:,}</td><td>{pct:.2f}%</td><td><div class="bar"><div class="fill" style="width:{pct}%"></div></div></td></tr>'
    
    # 媒体平台分布
    media_data = aggregation.get("mediaNameDistribution") or []
    media_rows = ""
    for item in media_data[:10]:
        key = item.get("key", "")
        count = item.get("docCount", 0)
        pct = (count / total * 100) if total > 0 else 0
        media_rows += f'<tr><td>{key}</td><td>{count:,}</td><td>{pct:.2f}%</td></tr>'
    
    # 地域分布
    area_data = aggregation.get("areaCodeProvinceDistribution") or []
    area_cards = ""
    for item in area_data[:15]:
        name = item.get("key", "")
        count = item.get("docCount", 0)
        area_cards += f'<div class="area-card"><div class="name">{name}</div><div class="count">{count:,}</div></div>'
    
    # 关键词云
    keywords_data = aggregation.get("keywordsDistribution") or []
    colors = ["#667eea", "#764ba2", "#ff6b6b", "#26de81", "#feca57"]
    keyword_tags = ""
    max_count = keywords_data[0].get("docCount", 1) if keywords_data else 1
    for i, item in enumerate(keywords_data[:20]):
        key = item.get("key", "")
        count = item.get("docCount", 0)
        font_size = max(13, min(27, int(13 + (count / max_count) * 14)))
        color = colors[i % len(colors)]
        keyword_tags += f'<span class="kw-tag" style="font-size:{font_size}px;background:{color}">{key} ({count:,})</span>'
    
    # 时间趋势数据
    trend_data = aggregation.get("publishTimeTrend") or []
    trend_labels = [item.get("key", "") for item in trend_data[-24:]]
    trend_values = [item.get("docCount", 0) for item in trend_data[-24:]]
    
    # 热门文章
    article_items = ""
    for i, article in enumerate(articles[:20], 1):
        title = article.get("title") or "无标题"
        summary = article.get("summary") or ""
        author = article.get("authorName") or "未知"
        platform = article.get("platformName") or "未知"
        pub_time = format_timestamp(article.get("publishTime"))
        url = article.get("originalUrl") or "#"
        
        article_items += f'''<div class="article-item">
<div class="article-title"><a href="{url}" target="_blank">{i}. {title[:80]}{"..." if len(title) > 80 else ""}</a></div>
<div class="article-meta">
<span>📰 {platform}</span>
<span>👤 {author}</span>
<span>🕐 {pub_time}</span>
</div>
<div class="article-summary">摘要：{summary[:100]}{"..." if len(summary) > 100 else ""}</div>
</div>'''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>舆情分析报告 - {query[:30]}</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: "Microsoft YaHei", sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); min-height: 100vh; padding: 20px; }}
.container {{ max-width: 1200px; margin: 0 auto; background: #fff; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }}
.header {{ background: linear-gradient(135deg, #1e3c72, #2a5298); color: white; padding: 40px; text-align: center; }}
.header h1 {{ font-size: 28px; margin-bottom: 10px; }}
.content {{ padding: 30px 40px; }}
.section {{ margin-bottom: 45px; }}
.section-title {{ font-size: 20px; color: #1e3c72; padding-bottom: 12px; border-bottom: 3px solid #667eea; margin-bottom: 25px; font-weight: 600; }}

.stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 25px; }}
.stat-card {{ padding: 25px; border-radius: 12px; text-align: center; color: white; }}
.stat-card.total {{ background: linear-gradient(135deg, #667eea, #764ba2); }}
.stat-card.negative {{ background: linear-gradient(135deg, #ff6b6b, #ee5a5a); }}
.stat-card.neutral {{ background: linear-gradient(135deg, #feca57, #f9c846); color: #333; }}
.stat-card.positive {{ background: linear-gradient(135deg, #26de81, #20bf6b); }}
.stat-card .number {{ font-size: 32px; font-weight: 700; }}

.progress-bar {{ height: 12px; background: #e8e8e8; border-radius: 6px; overflow: hidden; display: flex; margin-bottom: 20px; }}
.progress-bar .fill.negative {{ background: #ff6b6b; }}
.progress-bar .fill.neutral {{ background: #feca57; }}
.progress-bar .fill.positive {{ background: #26de81; }}

.chart-container {{ background: #f8f9fa; border-radius: 12px; padding: 20px; }}
.chart-box {{ height: 350px; }}

.keyword-cloud {{ display: flex; flex-wrap: wrap; gap: 10px; padding: 20px; justify-content: center; }}
.kw-tag {{ padding: 6px 16px; border-radius: 20px; color: white; }}

.article-item {{ background: #f8f9fa; border-radius: 12px; padding: 15px; margin-bottom: 15px; }}
.article-title {{ font-size: 15px; color: #1e3c72; font-weight: 600; margin-bottom: 8px; }}
.article-title a {{ color: inherit; text-decoration: none; }}
.article-meta {{ font-size: 12px; color: #666; display: flex; gap: 15px; }}
.article-summary {{ font-size: 13px; color: #555; margin-top: 8px; }}

table {{ width: 100%; border-collapse: collapse; }}
th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #eee; }}
th {{ background: #f8f9fa; font-weight: 600; }}
.bar {{ height: 8px; background: #e8e8e8; border-radius: 4px; overflow: hidden; }}
.fill {{ height: 100%; background: #667eea; }}

.area-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; }}
.area-card {{ background: #f8f9fa; padding: 15px; border-radius: 10px; text-align: center; }}
.area-card .name {{ font-size: 14px; color: #333; }}
.area-card .count {{ font-size: 20px; font-weight: 700; color: #667eea; }}

.summary-box {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 25px; border-radius: 12px; margin-top: 20px; }}
.summary-box h3 {{ margin-bottom: 15px; }}
.summary-box ul {{ list-style: none; padding: 0; }}
.summary-box li {{ padding: 6px 0; opacity: 0.95; }}
.summary-box li::before {{ content: "✓"; margin-right: 10px; }}

.footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #666; font-size: 13px; }}
@media (max-width: 900px) {{ .stats-grid {{ grid-template-columns: repeat(2, 1fr); }} .area-grid {{ grid-template-columns: repeat(3, 1fr); }} }}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>📊 舆情分析报告</h1>
<p>查询关键词: {query} | 生成时间: {now}</p>
</div>
<div class="content">

<div class="section">
<h2 class="section-title">📊 舆情概况</h2>
<div class="stats-grid">
<div class="stat-card total"><div class="number">{total:,}</div><div>信息总量</div></div>
<div class="stat-card negative"><div class="number">{negative_count:,}</div><div>负面</div></div>
<div class="stat-card neutral"><div class="number">{neutral_count:,}</div><div>中性</div></div>
<div class="stat-card positive"><div class="number">{positive_count:,}</div><div>正面</div></div>
</div>
<div class="progress-bar">
<div class="fill negative" style="width:{negative_pct:.2f}%"></div>
<div class="fill neutral" style="width:{neutral_pct:.2f}%"></div>
<div class="fill positive" style="width:{positive_pct:.2f}%"></div>
</div>
<p>整体舆情情绪偏向<strong style="color:{sentiment_color}">{main_sentiment}</strong>，{main_sentiment}信息占比{max(negative_pct, neutral_pct, positive_pct):.1f}%。</p>
</div>

<div class="section">
<h2 class="section-title">📡 传播渠道分布</h2>
<table><thead><tr><th>渠道</th><th>数量</th><th>占比</th><th>趋势</th></tr></thead><tbody>{channel_rows}</tbody></table>
</div>

<div class="section">
<h2 class="section-title">📺 媒体平台分布</h2>
<table><thead><tr><th>平台</th><th>数量</th><th>占比</th></tr></thead><tbody>{media_rows}</tbody></table>
</div>

<div class="section">
<h2 class="section-title">🗺️ 省级地域分布</h2>
<div class="area-grid">{area_cards}</div>
</div>

<div class="section">
<h2 class="section-title">🔑 关键词云</h2>
<div class="keyword-cloud">{keyword_tags}</div>
</div>

<div class="section">
<h2 class="section-title">📈 传播趋势</h2>
<div id="trendChart" class="chart-box"></div>
</div>

<script>
var trendChart = echarts.init(document.getElementById('trendChart'));
var trendOption = {{
    tooltip: {{ trigger: 'axis' }},
    xAxis: {{ type: 'category', data: {trend_labels} }},
    yAxis: {{ type: 'value', name: '数量' }},
    series: [{{
        data: {trend_values},
        type: 'line',
        smooth: true,
        areaStyle: {{ opacity: 0.3 }},
        itemStyle: {{ color: '#667eea' }},
        lineStyle: {{ width: 3 }}
    }}]
}};
trendChart.setOption(trendOption);
</script>

<div class="section">
<h2 class="section-title">🔥 热门文章</h2>
{article_items}
</div>

<div class="section">
<h2 class="section-title">📋 总结</h2>
<div class="summary-box">
<h3>核心发现</h3>
<ul>
<li>本次分析共采集到 {total:,} 条相关舆情数据</li>
<li>舆情以{main_sentiment}为主({max(negative_pct, neutral_pct, positive_pct):.1f}%)</li>
<li>主要传播渠道: {", ".join([item.get("key", "") for item in channel_data[:3]])}</li>
<li>热门关键词: {", ".join([item.get("key", "") for item in keywords_data[:5]])}</li>
</ul>
</div>
</div>

</div>
<div class="footer">
<p>报告生成时间: {now} | 数据来源: 舆情分析系统</p>
</div>
</div>
</body>
</html>'''
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    return output_path


def create_argument_parser():
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="舆情报告生成 CLI 工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础查询
  python3 scripts/report_cli.py --query "比亚迪"
  
  # 指定时间范围
  python3 scripts/report_cli.py --query "比亚迪" --days 7
  
  # 全维度分析
  python3 scripts/report_cli.py --query "(南京|金陵)&(医疗|卫生)" --days 3 --area "南京" --full-analysis
  
  # 指定媒体平台和情感
  python3 scripts/report_cli.py --query "新能源汽车" --media "微博,抖音" --sentiment negative
  
  # 按热度排序
  python3 scripts/report_cli.py --query "热点事件" --sort interact_count --size 20
"""
    )
    
    parser.add_argument("--query", "-q", required=True, help="查询关键词 (支持 &|!() 运算符)")
    
    parser.add_argument("--size", "-n", type=int, default=10, help="返回条数 (1-20, 默认10)")
    parser.add_argument("--sort", "-s", default="publish_time", 
                        choices=["publish_time", "interact_count", "comments_count", "likes_count", "reposts_count", "fans_count"],
                        help="排序字段 (默认: publish_time)")
    parser.add_argument("--sort-order", default="desc", choices=["asc", "desc"], help="排序方式 (默认: desc)")
    
    parser.add_argument("--media", "-m", help="媒体平台 (逗号分隔, 如: 微博,抖音)")
    parser.add_argument("--author", "-a", help="作者名称")
    parser.add_argument("--msg-type", choices=["original", "comment", "repost", "all"], help="消息类型")
    parser.add_argument("--content-type", choices=["video", "picture", "text", "all"], help="内容类型")
    parser.add_argument("--sentiment", choices=["negative", "neutral", "positive", "all"], help="情感倾向")
    parser.add_argument("--media-class", help="媒体分类 (如: 中央媒体)")
    parser.add_argument("--domain", help="内容领域")
    parser.add_argument("--scene", help="业务场景")
    parser.add_argument("--area", help="地域名称")
    parser.add_argument("--verification", choices=["blue", "yellow", "normal"], help="认证类型")
    
    parser.add_argument("--days", "-d", type=int, help="最近N天 (与 --time-from/--time-to 互斥)")
    parser.add_argument("--time-from", help="开始时间 (格式: YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--time-to", help="结束时间 (格式: YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS)")
    
    parser.add_argument("--interact-min", type=int, help="互动数最小值")
    parser.add_argument("--interact-max", type=int, help="互动数最大值")
    parser.add_argument("--comments-min", type=int, help="评论数最小值")
    parser.add_argument("--comments-max", type=int, help="评论数最大值")
    
    parser.add_argument("--full-analysis", "-f", action="store_true", help="全维度分析模式")
    parser.add_argument("--no-articles", action="store_true", help="不返回热文列表")
    parser.add_argument("--output-dir", "-o", default=DEFAULT_OUTPUT_DIR, help="报告输出目录")
    parser.add_argument("--json-only", action="store_true", help="仅输出JSON格式")
    parser.add_argument("--quiet", action="store_true", help="静默模式，不显示摘要")
    
    return parser


def main():
    """主函数"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    time_from = None
    time_to = None
    
    if args.days:
        now = datetime.now()
        time_from = int((now - timedelta(days=args.days)).timestamp() * 1000)
        time_to = int(now.timestamp() * 1000)
    else:
        if args.time_from:
            time_from = parse_datetime(args.time_from)
        if args.time_to:
            time_to = parse_datetime(args.time_to)
    
    api_kwargs = {
        "size": args.size,
        "sort_field": args.sort,
        "sort_order": args.sort_order,
        "hot_articles": not args.no_articles,
        "aggregation_types": get_full_aggregation_types() if args.full_analysis else get_default_aggregation_types(),
        "time_from": time_from,
        "time_to": time_to
    }
    
    if args.media:
        api_kwargs["media_names"] = [m.strip() for m in args.media.split(",")]
    if args.author:
        api_kwargs["author_name"] = args.author
    if args.msg_type:
        api_kwargs["message_types"] = parse_msg_type(args.msg_type)
    if args.content_type:
        api_kwargs["content_types"] = parse_content_type(args.content_type)
    if args.sentiment:
        api_kwargs["sentiments"] = parse_sentiment(args.sentiment)
    if args.media_class:
        api_kwargs["media_classes"] = [args.media_class]
    if args.domain:
        api_kwargs["domains"] = [args.domain]
    if args.scene:
        api_kwargs["scenes"] = [args.scene]
    if args.area:
        area_codes, _ = parse_area(args.area)
        if area_codes:
            api_kwargs["area_codes"] = area_codes
    if args.verification:
        api_kwargs["verification_type"] = parse_verification(args.verification)
    if args.interact_min:
        api_kwargs["interact_count_min"] = args.interact_min
    if args.interact_max:
        api_kwargs["interact_count_max"] = args.interact_max
    if args.comments_min:
        api_kwargs["comments_count_min"] = args.comments_min
    if args.comments_max:
        api_kwargs["comments_count_max"] = args.comments_max
    
    data = call_report_api(args.query, **api_kwargs)
    
    if not data:
        sys.exit(1)
    
    if not args.quiet:
        display_report_summary(data, args.query)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_query = args.query[:20].replace("/", "_").replace("\\", "_").replace("|", "_").replace("&", "_")
    base_filename = f"report_{safe_query}_{timestamp}"
    
    json_path = os.path.join(args.output_dir, f"{base_filename}.json")
    json_path = save_json_report(data, json_path)
    print(f"✅ JSON报告已保存: {json_path}")
    
    if not args.json_only:
        md_path = os.path.join(args.output_dir, f"{base_filename}.md")
        md_path = generate_markdown_report(data, args.query, md_path)
        print(f"✅ Markdown报告已保存: {md_path}")
        
        html_path = os.path.join(args.output_dir, f"{base_filename}.html")
        html_path = generate_html_report(data, args.query, html_path)
        print(f"✅ HTML报告已保存: {html_path}")
    
    print("\n🎉 报告生成完成!")


if __name__ == "__main__":
    main()