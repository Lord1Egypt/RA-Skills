#!/usr/bin/env python3
"""
人民数据 API 调用封装

人民数据（peopledata.com.cn）提供政企数据、舆情监控、企业信用等服务。

认证方式：Token认证，Header中携带 token
基础URL: https://api.peopledata.com.cn（具体baseURL以运营方提供的为准）

使用方式:
  1. 设置环境变量 VC_PEOPLE_DATA_KEY
  2. python3 scripts/people_data.py <command> [args]
  
注意：人民数据API的具体endpoint和参数格式可能因版本不同而有差异，
      以下为通用封装，运营方提供Key后根据实际文档调整endpoint。
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import time

# 加入缓存层
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from cache import cached, stats as cache_stats, cleanup as cache_cleanup

BASE_URL = os.environ.get("VC_PEOPLE_DATA_BASE_URL", "https://api.peopledata.com.cn")

def get_api_key():
    """获取API Key"""
    key = os.environ.get("VC_PEOPLE_DATA_KEY", "")
    if key:
        return key
    config_path = os.path.expanduser("~/.openclaw/workspace/memory/vc-api-keys.md")
    if os.path.exists(config_path):
        with open(config_path) as f:
            for line in f:
                if "人民数据" in line and "未配置" not in line and "待提供" not in line:
                    parts = line.split(":")
                    if len(parts) >= 2:
                        val = parts[-1].strip()
                        if val and val != "用户已有接口，待提供key":
                            return val
    return ""

def get_headers():
    """构建认证Header"""
    key = get_api_key()
    if not key:
        return None
    return {
        "Content-Type": "application/json",
        "token": key,
        "Authorization": f"Bearer {key}",
    }

def api_get(path, params=None):
    """通用GET请求"""
    headers = get_headers()
    if not headers:
        return {"error": "人民数据API Key未配置", "configured": False}

    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            data["configured"] = True
            return data
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}", "configured": True}
    except Exception as e:
        return {"error": str(e), "configured": True}

def api_post(path, body=None):
    """通用POST请求"""
    headers = get_headers()
    if not headers:
        return {"error": "人民数据API Key未配置", "configured": False}

    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode("utf-8") if body else b"{}"

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            result["configured"] = True
            return result
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}", "configured": True}
    except Exception as e:
        return {"error": str(e), "configured": True}


# === VC投资筛选常用接口 ===

def company_credit(company_name):
    """
    企业信用信息查询
    
    Args:
        company_name: 企业全称
    """
    return api_get("/api/v1/company/credit", {
        "companyName": company_name
    })

def policy_search(keyword, page=1, size=20):
    """
    政策文件搜索
    
    Args:
        keyword: 政策关键词
        page: 页码
        size: 每页数量
    """
    return api_get("/api/v1/policy/search", {
        "keyword": keyword,
        "page": page,
        "size": size
    })

def sentiment_search(keyword, start_date=None, end_date=None):
    """
    舆情监控搜索
    
    Args:
        keyword: 监控关键词（企业名/人名/事件）
        start_date: 开始日期 YYYY-MM-DD
        end_date: 结束日期 YYYY-MM-DD
    """
    params = {"keyword": keyword}
    if start_date:
        params["startDate"] = start_date
    if end_date:
        params["endDate"] = end_date
    return api_get("/api/v1/sentiment/search", params)

def industry_data(industry_name):
    """
    行业数据查询
    
    Args:
        industry_name: 行业名称
    """
    return api_get("/api/v1/industry/data", {
        "industry": industry_name
    })

def vc_policy_digest(keywords, days=30):
    """
    VC投资筛选专用：政策情报摘要
    
    获取与关注行业相关的最新政策动态
    
    Args:
        keywords: 关键词列表，如 ["人工智能", "医疗器械", "创新药"]
        days: 回溯天数
    """
    results = []
    for kw in keywords:
        data = policy_search(kw)
        results.append({"keyword": kw, "data": data})
    return {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source": "人民数据",
        "keywords": keywords,
        "days": days,
        "results": results
    }

def vc_sentiment_check(company_name, days=30):
    """
    VC投资筛选专用：企业舆情检查
    
    检查目标企业近期的舆情动态，用于风险预警
    
    Args:
        company_name: 企业名称
        days: 回溯天数
    """
    end = time.strftime("%Y-%m-%d")
    start = time.strftime("%Y-%m-%d", time.localtime(time.time() - days * 86400))
    
    return {
        "company": company_name,
        "period": f"{start} ~ {end}",
        "source": "人民数据",
        "data": sentiment_search(company_name, start, end)
    }


# === CLI入口 ===

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("人民数据API调用工具")
        print("")
        print("用法:")
        print("  python3 scripts/people_data.py credit <企业名称>          企业信用")
        print("  python3 scripts/people_data.py policy <关键词>            政策搜索")
        print("  python3 scripts/people_data.py sentiment <关键词>         舆情搜索")
        print("  python3 scripts/people_data.py industry <行业名称>        行业数据")
        print("  python3 scripts/people_data.py policy_digest <关键词1,关键词2>  政策摘要")
        print("  python3 scripts/people_data.py check <企业名称>           舆情检查")
        print("")
        status = "已配置" if get_api_key() else "未配置"
        print(f"API Key状态: {status}")
        print(f"Base URL: {BASE_URL}")
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "credit" and len(sys.argv) >= 3:
        result = company_credit(sys.argv[2])
    elif cmd == "policy" and len(sys.argv) >= 3:
        result = policy_search(sys.argv[2])
    elif cmd == "sentiment" and len(sys.argv) >= 3:
        result = sentiment_search(sys.argv[2])
    elif cmd == "industry" and len(sys.argv) >= 3:
        result = industry_data(sys.argv[2])
    elif cmd == "policy_digest" and len(sys.argv) >= 3:
        kws = sys.argv[2].split(",")
        result = vc_policy_digest(kws)
    elif cmd == "check" and len(sys.argv) >= 3:
        result = vc_sentiment_check(sys.argv[2])
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))
