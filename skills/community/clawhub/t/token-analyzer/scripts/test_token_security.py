#!/usr/bin/env python3
import json
import asyncio
import websockets
import urllib.request

CHROME_WS_BASE = "ws://localhost:9222"

async def get_page_id():
    resp = urllib.request.urlopen("http://localhost:9222/json/list")
    tabs = json.loads(resp.read())
    for t in tabs:
        if t.get('type') == 'page':
            return t['id']
    return None

async def chrome_fetch(ws, url):
    js = f"fetch('{url}').then(r=>r.json())"
    await ws.send(json.dumps({'id':1,'method':'Runtime.evaluate','params':{'expression':js,'awaitPromise':True}}))
    resp = await ws.recv()
    result = json.loads(resp).get('result',{}).get('result',{})
    if result.get('type') == 'object':
        obj_id = result.get('objectId')
        if obj_id:
            await ws.send(json.dumps({'id':2,'method':'Runtime.callFunctionOn','params':{'objectId':obj_id,'functionDeclaration':'function(){return JSON.stringify(this)}'}}))
            resp2 = await ws.recv()
            json_str = json.loads(resp2).get('result',{}).get('result',{}).get('value','{}')
            return json.loads(json_str)
    return {}

async def main():
    page_id = await get_page_id()
    ws_url = f"{CHROME_WS_BASE}/devtools/page/{page_id}"
    
    async with websockets.connect(ws_url) as ws:
        # 测试安全检测 API，看能否获取创建者地址
        address = '0xe1c73aa0ac443f69aec9704d8b87209aa0a54444'
        params = "device_id=bf3bd459-9cc5-46f0-95bf-8297b8a58c72&fp_did=c44ca81f8d7dabb1d0dc62c33c0ee26d&client_id=gmgn_web_20260304-11376-fc51c8a&from_app=gmgn&app_ver=20260304-11376-fc51c8a&tz_name=Asia/Shanghai&tz_offset=28800&app_lang=zh-CN&os=web&worker=0"
        url = f"https://gmgn.ai/api/v1/mutil_window_token_security_launchpad/bsc/{address}?{params}"
        
        data = await chrome_fetch(ws, url)
        
        # 查找创建者地址
        creator = data.get('data', {}).get('security', {}).get('creator_address')
        print(f"Creator address: {creator}")
        
        if creator:
            # 查询开发者信息
            dev_url = f"https://gmgn.ai/api/v1/dev_created_tokens/bsc/{creator}?{params}"
            dev_data = await chrome_fetch(ws, dev_url)
            print(f"\nDev data:")
            print(json.dumps(dev_data, indent=2, ensure_ascii=False))

asyncio.run(main())
