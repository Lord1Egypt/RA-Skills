#!/usr/bin/env python3
import json
import sys
import asyncio
import websockets
import urllib.request

CHROME_WS_BASE = "ws://localhost:9222"
GMGN_BASE = "https://gmgn.ai"

async def get_page_id():
    try:
        resp = urllib.request.urlopen(f"http://localhost:9222/json/list")
        tabs = json.loads(resp.read())
        for t in tabs:
            if t.get('type') == 'page':
                return t['id']
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
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
    address = '0x05f04a08df246ce66d04b718c343f7190fe0848c'
    chain = 'bsc'
    
    page_id = await get_page_id()
    ws_url = f"{CHROME_WS_BASE}/devtools/page/{page_id}"
    
    async with websockets.connect(ws_url) as ws:
        params = "device_id=bf3bd459-9cc5-46f0-95bf-8297b8a58c72&fp_did=c44ca81f8d7dabb1d0dc62c33c0ee26d&client_id=gmgn_web_20260304-11376-fc51c8a&from_app=gmgn&app_ver=20260304-11376-fc51c8a&tz_name=Asia/Shanghai&tz_offset=28800&app_lang=zh-CN&os=web&worker=0"
        url = f"{GMGN_BASE}/api/v1/dev_created_tokens/{chain}/{address}?{params}"
        
        print(f"Testing URL: {url}\n")
        data = await chrome_fetch(ws, url)
        print(json.dumps(data, indent=2, ensure_ascii=False))

asyncio.run(main())
