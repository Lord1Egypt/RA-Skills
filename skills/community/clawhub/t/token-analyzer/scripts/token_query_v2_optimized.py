#!/usr/bin/env python3
"""
Token Query Script v2.2 - 优化版：并行 API 调用
"""

import json
import sys
import asyncio
import websockets
import urllib.request

CHROME_WS_BASE = "ws://localhost:9222"
GMGN_BASE = "https://gmgn.ai"
DEVICE_ID = "bf3bd459-9cc5-46f0-95bf-8297b8a58c72"
FP_DID = "c44ca81f8d7dabb1d0dc62c33c0ee26d"
CLIENT_ID = "gmgn_web_20260304-11376-fc51c8a"
FROM_APP = "gmgn"
APP_VER = "20260304-11376-fc51c8a"
TZ_NAME = "Asia/Shanghai"
TZ_OFFSET = "28800"
APP_LANG = "zh-CN"
OS = "web"
WORKER = "0"

def get_common_params():
    return f"device_id={DEVICE_ID}&fp_did={FP_DID}&client_id={CLIENT_ID}&from_app={FROM_APP}&app_ver={APP_VER}&tz_name={TZ_NAME}&tz_offset={TZ_OFFSET}&app_lang={APP_LANG}&os={OS}&worker={WORKER}"

def fmt_num(n):
    if n is None: return "N/A"
    n = float(n)
    if n >= 1e9: return f"${n/1e9:.2f}B"
    if n >= 1e6: return f"${n/1e6:.2f}M"
    if n >= 1e3: return f"${n/1e3:.1f}K"
    return f"${n:.2f}"

def fmt_price(p):
    if p is None: return "N/A"
    p = float(p)
    if p >= 1: return f"${p:.4f}"
    if p >= 0.001: return f"${p:.8f}".rstrip('0')
    return f"${p:.12f}".rstrip('0')

async def get_page_id():
    try:
        resp = urllib.request.urlopen(f"http://localhost:9222/json/list")
        tabs = json.loads(resp.read())
        for tab in tabs:
            if tab.get('type') == 'page':
                return tab['id']
    except Exception as e:
        print(f"Error getting page ID: {e}")
    return None

async def chrome_fetch(ws, url):
    """通过浏览器 fetch API 获取数据"""
    try:
        js_code = f"fetch('{url}').then(r => r.json())"
        await ws.send(json.dumps({
            'id': 1,
            'method': 'Runtime.evaluate',
            'params': {
                'expression': js_code,
                'awaitPromise': True
            }
        }))
        
        response = await ws.recv()
        result = json.loads(response)
        
        if result.get('result', {}).get('result', {}).get('type') == 'object':
            object_id = result['result']['result']['objectId']
            await ws.send(json.dumps({
                'id': 2,
                'method': 'Runtime.callFunctionOn',
                'params': {
                    'objectId': object_id,
                    'functionDeclaration': 'function() { return JSON.stringify(this); }'
                }
            }))
            
            response2 = await ws.recv()
            result2 = json.loads(response2)
            json_str = result2.get('result', {}).get('result', {}).get('value', '{}')
            return json.loads(json_str)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return {}
