#!/usr/bin/env python3
import sys,requests,websocket,json

TITLE=sys.argv[1]
BODY=sys.argv[2]

CDP="http://127.0.0.1:9222/json"

tabs=requests.get(CDP).json()
target=None
for t in tabs:
    if "mp.weixin" in t.get("url","") or "channels.weixin" in t.get("url",""):
        target=t
        break

if not target:
    raise SystemExit("No WeChat publishing tab found. Open mp.weixin.qq.com or channels.weixin.qq.com and login first.")

ws=websocket.create_connection(target["webSocketDebuggerUrl"])

def send(method,params=None):
    ws.send(json.dumps({"id":1,"method":method,"params":params or {}}))
    return json.loads(ws.recv())

send("Runtime.evaluate",{
 "expression":f"""
var title=document.querySelector('input');
if(title){{title.value=`{TITLE}`}}
var body=document.querySelector('[contenteditable]');
if(body){{body.innerText=`{BODY}`}}
"""
})

send("Runtime.evaluate",{
 "expression":"var btn=document.querySelector('button'); if(btn){btn.click()}"
})

print("WeChat post attempted")