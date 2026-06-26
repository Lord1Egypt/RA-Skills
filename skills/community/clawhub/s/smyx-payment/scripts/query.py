#!/usr/bin/env python3
"""
symx_payment - 账户查询模块
调用云端 API 查询账户信息：已充值金额、余额、剩余次数、已使用次数
"""
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, parent_dir)

from http.client import responses
from typing import Dict

from .config import ApiEnum, ConstantEnum

from skills.smyx_common.scripts.api_service import ApiService as ApiServiceBase

from .api_service import ApiService

from .config import *
from .skill import skill
from .open_id import require_open_id, resolve_open_id

import sys
import json
import urllib.request
import urllib.error

# API 配置（从环境变量或配置文件读取）
API_CONFIG = {
    "baseUrl": "https://open.lifeemergence.com/smyx-open-api",  # 待用户确认
    "queryPath": "/api/quantity-query",
    "authType": "bearer",  # bearer | apikey | none
    "token": ""  # 待用户配置
}

def query_account(phone_number: str = None, token: str = None) -> Dict | str:
    """
    查询账户信息
    
    Args:
        phone_number: 增值账号（手机号）
        token: Bearer Token（可选，不传则使用默认配置）
    
    Returns:
        账户信息字典，包含：
        - totalRecharged: 已充值金额
        - balance: 账户余额
        - remainingUses: 剩余使用次数
        - usedCount: 已使用次数
        - isInsufficient: 余额是否不足
    """
    phone_number = require_open_id(phone_number)
    token = token or API_CONFIG.get("token", "")
    
    url = f"{API_CONFIG['baseUrl']}{API_CONFIG['queryPath']}"
    
    # 构建请求头
    headers = {
        "Content-Type": "application/json"
    }
    
    if API_CONFIG["authType"] == "bearer" and token:
        headers["Authorization"] = f"Bearer {token}"
    elif API_CONFIG["authType"] == "apikey" and token:
        headers["X-API-Key"] = token
    
    # 构建请求体
    # userId = f"SKILL-USER:{phone_number}"
    data = {
        # "account": phone_number,
        "userId": phone_number,
        # "sceneCode": "ALL-SKILL",
        # "bizTag": ""
    }
    
    try:

        # skill.quantity_query(data)

        # req = urllib.request.Request(
        #     url,
        #     data=json.dumps(data).encode('utf-8'),
        #     headers=headers,
        #     method='POST'
        # )

        response = skill.quantity_query(data)
        return response or "⚠️ 该账户还没有任何充值记录"
        if response:
            pass
            # return {
            #     "success": True,
            #     "data": response
            # }
        else:
            return "⚠️ 该账户还没有任何充值记录"

        # with skill.quantity_query(data) as response:
        #     print("*******=======>>>>>get resulr:", response)
        #
        #     # return response
        #
        #     return {
        #         "success": True,
        #         "data": response
        #     }
        #
    # except urllib.error.HTTPError as e:
    #     return {
    #         "success": False,
    #         "error": f"HTTP 错误：{e.code} - {e.reason}",
    #         "status_code": e.code
    #     }
    # except urllib.error.URLError as e:
    #     return {
    #         "success": False,
    #         "error": f"网络错误：{e.reason}"
    #     }
    except Exception as e:
        return  f"查询失败：{str(e)}"

def check_balance_sufficient(balance: float, threshold: float = 0) -> bool:
    """
    检查余额是否充足
    
    Args:
        balance: 当前余额
        threshold: 阈值（默认为 0）
    
    Returns:
        True: 余额充足，False: 余额不足
    """
    return balance > threshold

if __name__ == "__main__":
    # 测试用法：手机号/账号可选；未传时系统会自动完成内部身份关联
    phone_arg = sys.argv[1] if len(sys.argv) > 1 else None
    token = sys.argv[2] if len(sys.argv) > 2 else None

    phone = require_open_id(phone_arg)
    ConstantEnumBase.CURRENT__OPEN_ID = phone

    result = query_account(phone, token)
    print(result)
    # print(json.dumps(result, ensure_ascii=False, indent=2))

