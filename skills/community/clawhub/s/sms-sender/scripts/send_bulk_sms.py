#!/usr/bin/env python3
"""
CloudSMS 群发短信 Skill
发送批量短信到多个手机号码
"""

import sys
import json
import os
import requests
from datetime import datetime, timezone

# 禁用代理，确保直连
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

API_URL = "https://cpaas-sms.cmidict.com:1820/uips"

def send_sms(channel, auth_key, mobile_list, content, signature=None, original_addr=None):
    """发送群发短信"""

    # 生成时间戳
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # 构建请求参数
    payload = {
        "uip_head": {
            "METHOD": "SMS_SEND_REQUEST",
            "SERIAL": 1,
            "TIME": timestamp,
            "CHANNEL": channel,
            "AUTH_KEY": auth_key
        },
        "uip_body": {
            "SMS_CONTENT": content,
            "DESTINATION_ADDR": mobile_list,
            "PRIORITY": 1
        },
        "uip_version": 2
    }

    # 添加可选参数
    if signature:
        payload["uip_body"]["SIGNATURE"] = signature
        payload["uip_body"]["SIGNATURE_TYPE"] = "HEAD_BOLDFACE_SQUARE"

    if original_addr:
        payload["uip_body"]["ORIGINAL_ADDR"] = original_addr

    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        result = response.json()

        uip_head = result.get("uip_head", {})
        uip_body = result.get("uip_body", {})

        result_code = uip_head.get("RESULT_CODE", "")
        result_desc = uip_head.get("RESULT_DESC", "")

        success = result_code == 1 and result_desc == "OK"

        output = {
            "success": success,
            "result_code": result_code,
            "result_desc": result_desc,
            "raw_response": result
        }

        # 特殊错误提示
        if "AUTHKEY" in str(result_desc):
            output["hint"] = "账号或密钥错误，请联系平台管理员获取正确的凭证"
        elif "BALANCE" in str(result_desc):
            output["hint"] = "余额不足，请联系平台管理员充值"
        elif "SIGN" in str(result_desc):
            output["hint"] = "签名未报备，请联系平台管理员报备签名"

        return output

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"网络请求失败: {str(e)}"
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"响应解析失败: {str(e)}"
        }

def main():
    if len(sys.argv) < 4:
        print(json.dumps({
            "success": False,
            "error": "参数不足。用法: send_bulk_sms.py <channel> <auth_key> <mobile> <content> [signature]"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    channel = sys.argv[1]
    auth_key = sys.argv[2]
    mobile = sys.argv[3]
    content = sys.argv[4]
    signature = sys.argv[5] if len(sys.argv) > 5 else None

    # 处理手机号列表
    mobile_list = [m.strip() for m in mobile.split(',')]

    result = send_sms(channel, auth_key, mobile_list, content, signature)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    sys.exit(0 if result["success"] else 1)

if __name__ == "__main__":
    main()
