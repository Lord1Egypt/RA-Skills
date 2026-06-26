#!/usr/bin/env python3
"""
Xiaohongshu CDP publisher v3
Implements full workflow:
1. Click 发布笔记
2. Click 写长文
3. Fill title (<=64 chars)
4. Fill body
5. Click 一键排版 -> 简约基础
6. Click 下一步
7. Click 发布

Requires Chrome started with --remote-debugging-port=9222
and user logged into https://creator.xiaohongshu.com
"""

import sys, json, time, requests, websocket

if len(sys.argv) < 3:
    print("Usage: cdp_xhs_publish_v3.py <title> <body>")
    sys.exit(1)

TITLE=sys.argv[1][:64]
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

send(ws,"Page.bringToFront")

def click_text(text):
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

# Step1 发布笔记
click_text("发布笔记")
time.sleep(2)

# Step2 写长文
click_text("写长文")
time.sleep(3)

# Step3 填标题
send(ws,"Runtime.evaluate",{"expression":"document.querySelector('input')?.focus()"})
send(ws,"Input.insertText",{"text":TITLE})

time.sleep(1)

# Step4 填正文
send(ws,"Runtime.evaluate",{"expression":"document.querySelector('[contenteditable],textarea,div[class*=editor]')?.focus()"})
send(ws,"Input.insertText",{"text":"\n"+BODY})

time.sleep(1)

# Step5 一键排版
click_text("一键排版")
time.sleep(1)
click_text("简约")
time.sleep(1)

# Step6 下一步
click_text("下一步")
time.sleep(2)

# Step7 发布
click_text("发布")

print("Xiaohongshu publish flow executed")
