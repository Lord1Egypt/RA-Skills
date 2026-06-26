#!/usr/bin/env python3
import json
import asyncio
import websockets
import urllib.request

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
    resp = urllib.request.urlopen("http://localhost:9222/json/list")
    tabs = json.loads(resp.read())
    page_id = [t['id'] for t in tabs if t.get('type') == 'page'][0]
    
    async with websockets.connect(f"ws://localhost:9222/devtools/page/{page_id}") as ws:
        params = "device_id=bf3bd459-9cc5-46f0-95bf-8297b8a58c72&fp_did=c44ca81f8d7dabb1d0dc62c33c0ee26d&client_id=gmgn_web_20260304-11376-fc51c8a&from_app=gmgn&app_ver=20260304-11376-fc51c8a&tz_name=Asia/Shanghai&tz_offset=28800&app_lang=zh-CN&os=web&worker=0"
        
        dev_addr = "0xfdae25a95c1d608efd8181370fb19327e09692af"
        url = f"https://gmgn.ai/api/v1/dev_created_tokens/bsc/{dev_addr}?{params}"
        data = await chrome_fetch(ws, url)
        
        print("Response keys:", list(data.keys()))
        print("\nData structure:")
        print(json.dumps(data, indent=2)[:500])

asyncio.run(main())
