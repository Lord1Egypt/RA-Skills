#!/usr/bin/env python3
import sys,requests,websocket,json

TEXT=sys.argv[1]
CDP="http://127.0.0.1:9222/json"

tabs=requests.get(CDP).json()
target=None
for t in tabs:
    if "weibo" in t.get("url",""):
        target=t
        break

if not target:
    raise SystemExit("No Weibo tab found. Open https://weibo.com and login first.")

ws=websocket.create_connection(target["webSocketDebuggerUrl"])

def send(method,params=None):
    ws.send(json.dumps({"id":1,"method":method,"params":params or {}}))
    return json.loads(ws.recv())

send("Runtime.evaluate",{
 "expression":f"""
var box=document.querySelector('textarea');
if(box){{box.value=`{TEXT}`}}
"""
})

send("Runtime.evaluate",{
 "expression":"var b=document.querySelector('[node-type=publishBtn]'); if(b){b.click()}"
})

print("Weibo post attempted")