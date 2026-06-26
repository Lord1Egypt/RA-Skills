#!/usr/bin/env python3
import sys, json, time, requests, websocket

if len(sys.argv) < 3:
    print("Usage: cdp_xhs_publish_v4.py <title> <body>")
    sys.exit(1)

TITLE = sys.argv[1][:64]
BODY = sys.argv[2]

CDP = "http://127.0.0.1:9222/json"

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

send(ws,"Page.bringToFront")

def click_text(text,timeout=10):
    start=time.time()
    while time.time()-start<timeout:
        script=f"""
        (function(){{
          const nodes=[...document.querySelectorAll('button,div,span')];
          for(const n of nodes){{
            if(n.innerText && n.innerText.includes('{text}')){{
              n.click();
              return true;
            }}
          }}
          return false;
        }})();
        """
        send(ws,"Runtime.evaluate",{"expression":script})
        time.sleep(1)

# try direct path
click_text("写长文")
click_text("发布笔记")
time.sleep(1)
click_text("写长文")

# new creation
click_text("新的创作")
time.sleep(3)

# title
send(ws,"Runtime.evaluate",{"expression":"document.querySelector('input')?.focus()"})
send(ws,"Input.insertText",{"text":TITLE})

time.sleep(1)

# body
send(ws,"Runtime.evaluate",{"expression":"document.querySelector('[contenteditable],textarea,div[class*=editor]')?.focus()"})
send(ws,"Input.insertText",{"text":"\n"+BODY})

time.sleep(1)

# layout
click_text("一键排版")
time.sleep(1)
click_text("简约")

# next
click_text("下一步")
time.sleep(2)

# publish
click_text("发布")

print("Xiaohongshu publish flow executed")
