#!/usr/bin/env python3
"""
天眼查开放平台 API 调用封装

认证方式：Token认证，Header中携带 Authorization: Bearer <token>
基础URL: https://open.api.tianyancha.com
文档: https://open.tianyancha.com/open/1849

使用方式:
  1. 设置环境变量 VC_TIANYANCHA_API_KEY
  2. python3 scripts/tianyancha.py <command> [args]
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import hashlib
import time
import base64

# 加入缓存层
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from cache import cached, stats as cache_stats, cleanup as cache_cleanup

BASE_URL = "https://open.api.tianyancha.com"

def get_api_key():
    """获取API Key，优先环境变量，其次从配置文件读取"""
    key = os.environ.get("VC_TIANYANCHA_API_KEY", "")
    if key:
        return key
    # 尝试从配置文件读取
    config_path = os.path.expanduser("~/.openclaw/workspace/memory/vc-api-keys.md")
    if os.path.exists(config_path):
        with open(config_path) as f:
            for line in f:
                if "天眼查" in line and "未配置" not in line:
                    parts = line.split(":")
                    if len(parts) >= 2:
                        return parts[-1].strip()
    return ""

def get_auth_header():
    """构建认证Header"""
    key = get_api_key()
    if not key:
        return None
    # 天眼查V2版本使用 Bearer Token
    return {"Authorization": f"Bearer {key}"}

def api_get(path, params=None):
    """通用GET请求"""
    headers = get_auth_header()
    if not headers:
        return {"error": "天眼查API Key未配置", "configured": False}
    
    headers["Content-Type"] = "application/json"
    
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
    headers = get_auth_header()
    if not headers:
        return {"error": "天眼查API Key未配置", "configured": False}
    
    headers["Content-Type"] = "application/json"
    
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

def company_search(keyword, page=1, size=20):
    """
    企业搜索 - 按关键词搜索企业
    
    Args:
        keyword: 企业名称/品牌/人名
        page: 页码
        size: 每页数量
    """
    return api_get("/services/open/ic/baseinfo/normal", {
        "keyword": keyword,
        "pageNum": page,
        "pageSize": size
    })

def company_detail(company_name):
    """
    企业工商详情
    
    Args:
        company_name: 企业全称
    """
    return api_post("/services/open/ic/baseinfo/2.0", {
        "keyword": company_name
    })

def company_ip_info(company_name):
    """
    企业知识产权信息（专利、商标、软著）
    """
    return api_get("/services/open/ip/copyright/2.0", {
        "keyword": company_name,
        "pageSize": 50
    })

def company_financial_risk(company_name):
    """
    企业财务风险信息
    """
    return api_get("/services/open/risk/financial/2.0", {
        "keyword": company_name
    })

def company_judicial_risk(company_name):
    """
    企业司法风险（诉讼、执行、失信）
    """
    return api_get("/services/open/risk/judicial/2.0", {
        "keyword": company_name
    })

def company_shareholders(company_name):
    """
    企业股东信息及股权穿透
    """
    return api_get("/services/open/ic/shareholder/2.0", {
        "keyword": company_name
    })

def company_investment(company_name):
    """
    企业对外投资
    """
    return api_get("/services/open/ic/investment/2.0", {
        "keyword": company_name
    })

def company_team(company_name):
    """
    企业核心团队（高管、法人、实际控制人）
    """
    return api_get("/services/open/ic/companyteam/2.0", {
        "keyword": company_name
    })

def company_changes(company_name):
    """
    企业工商变更记录
    """
    return api_get("/services/open/ic/changeinfo/2.0", {
        "keyword": company_name,
        "pageSize": 50
    })

def vc_company_profile(company_name):
    """
    VC投资筛选专用：一键获取企业完整画像（带缓存）
    
    返回用于第四层（企业基本面评估）的全部基础数据：
    - 工商基本信息
    - 核心团队
    - 股权结构
    - 知识产权
    - 风险信息
    
    缓存策略：完整画像缓存7天，避免重复调用API
    """
    def _fetch_all():
        return {
            "basic_info": company_detail(company_name),
            "team": company_team(company_name),
            "shareholders": company_shareholders(company_name),
            "ip": company_ip_info(company_name),
            "financial_risk": company_financial_risk(company_name),
            "judicial_risk": company_judicial_risk(company_name),
        }
    
    return cached("tianyancha", "profile", {"keyword": company_name}, _fetch_all)


# === CLI入口 ===

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("天眼查API调用工具")
        print("")
        print("用法:")
        print("  python3 scripts/tianyancha.py search <关键词>        搜索企业")
        print("  python3 scripts/tianyancha.py detail <企业名称>       企业详情")
        print("  python3 scripts/tianyancha.py ip <企业名称>          知识产权")
        print("  python3 scripts/tianyancha.py risk <企业名称>        风险信息")
        print("  python3 scripts/tianyancha.py shareholders <企业名称> 股权结构")
        print("  python3 scripts/tianyancha.py team <企业名称>        核心团队")
        print("  python3 scripts/tianyancha.py profile <企业名称>      完整画像")
        print("")
        status = "已配置" if get_api_key() else "未配置"
        print(f"API Key状态: {status}")
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "search" and len(sys.argv) >= 3:
        result = company_search(sys.argv[2])
    elif cmd == "detail" and len(sys.argv) >= 3:
        result = company_detail(sys.argv[2])
    elif cmd == "ip" and len(sys.argv) >= 3:
        result = company_ip_info(sys.argv[2])
    elif cmd == "risk" and len(sys.argv) >= 3:
        result = company_financial_risk(sys.argv[2])
    elif cmd == "shareholders" and len(sys.argv) >= 3:
        result = company_shareholders(sys.argv[2])
    elif cmd == "team" and len(sys.argv) >= 3:
        result = company_team(sys.argv[2])
    elif cmd == "profile" and len(sys.argv) >= 3:
        result = vc_company_profile(sys.argv[2])
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))
