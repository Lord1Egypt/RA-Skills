#!/usr/bin/env python3
import sys,requests,websocket,json

TITLE=sys.argv[1]
BODY=sys.argv[2]

CDP="http://127.0.0.1:9222/json"

tabs=requests.get(CDP).json()
target=None
for t in tabs:
    if "xiaohongshu" in t.get("url",""):
        target=t
        break

if not target:
    raise SystemExit("No Xiaohongshu tab found. Open https://www.xiaohongshu.com and login first.")

ws=websocket.create_connection(target["webSocketDebuggerUrl"])

def send(method,params=None):
    ws.send(json.dumps({"id":1,"method":method,"params":params or {}}))
    return json.loads(ws.recv())

send("Runtime.evaluate",{
 "expression":f"""
var t=document.querySelector('input');
if(t){{t.value=`{TITLE}`}}
var b=document.querySelector('[contenteditable]');
if(b){{b.innerText=`{BODY}`}}
"""
})

send("Runtime.evaluate",{
 "expression":"var btn=document.querySelector('button'); if(btn){btn.click()}"
})

print("Xiaohongshu post attempted")