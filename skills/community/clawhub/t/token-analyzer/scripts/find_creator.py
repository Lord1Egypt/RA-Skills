#!/usr/bin/env python3
import json
import asyncio
import websockets
import urllib.request

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
    ws_url = f"ws://localhost:9222/devtools/page/{page_id}"
    
    async with websockets.connect(ws_url) as ws:
        address = '0xe1c73aa0ac443f69aec9704d8b87209aa0a54444'
        params = "device_id=bf3bd459-9cc5-46f0-95bf-8297b8a58c72&fp_did=c44ca81f8d7dabb1d0dc62c33c0ee26d&client_id=gmgn_web_20260304-11376-fc51c8a&from_app=gmgn&app_ver=20260304-11376-fc51c8a&tz_name=Asia/Shanghai&tz_offset=28800&app_lang=zh-CN&os=web&worker=0"
        
        # 尝试 token_info API
        url = f"https://gmgn.ai/api/v1/token_info/bsc/{address}?{params}"
        data = await chrome_fetch(ws, url)
        
        if data.get('code') == 0:
            token_data = data.get('data', {})
            print("Keys in token_info:", list(token_data.keys())[:20])
            
            # 查找可能的创建者字段
            for key in ['creator', 'deployer', 'owner', 'creator_address', 'deployer_address']:
                if key in token_data:
                    print(f"\n{key}: {token_data[key]}")

asyncio.run(main())
