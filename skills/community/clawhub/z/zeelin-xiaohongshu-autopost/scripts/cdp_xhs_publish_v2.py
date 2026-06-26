#!/usr/bin/env python3
"""
Improved Xiaohongshu CDP publisher using Input.insertText (works with React editors)
"""
import sys, json, requests, websocket, time

if len(sys.argv) < 3:
    print("Usage: cdp_xhs_publish_v2.py <title> <body>")
    sys.exit(1)

TITLE=sys.argv[1]
BODY=sys.argv[2]
CDP="http://127.0.0.1:9222/json"

def find_tab():
    for t in requests.get(CDP).json():
        if "xiaohongshu" in t.get("url",""):
            return t
    return None


def send(ws,method,params=None):
    ws.send(json.dumps({"id":1,"method":method,"params":params or {}}))
    return json.loads(ws.recv())


tab=find_tab()
if not tab:
    raise SystemExit("No Xiaohongshu tab found")

ws=websocket.create_connection(tab["webSocketDebuggerUrl"])

# bring tab front
send(ws,"Page.bringToFront")

# focus title
focus_title="""
(function(){
 const el=document.querySelector('input');
 if(el){el.focus();return true;} return false;
})();
"""
send(ws,"Runtime.evaluate",{"expression":focus_title})

# type title
send(ws,"Input.insertText",{"text":TITLE})

time.sleep(1)

# focus editor
focus_body="""
(function(){
 const ed=document.querySelector('[contenteditable], textarea, div[class*=editor]');
 if(ed){ed.focus();return true;} return false;
})();
"""
send(ws,"Runtime.evaluate",{"expression":focus_body})

send(ws,"Input.insertText",{"text":"\n"+BODY})

print("XHS text inserted. Publish manually or extend script to auto-click.")