#!/usr/bin/env python3
import asyncio, json, os, subprocess
from datetime import datetime

U = os.getenv("TWITTER_USER","")
A = os.getenv("AUTH_TOKEN","")
C = os.getenv("CT0","")
TB = os.getenv("TELEGRAM_BOT_TOKEN","")
TC = os.getenv("TELEGRAM_CHAT_ID","")

def log(m): print(f"[{datetime.now().strftime('%H:%M:%S')}] {m}", flush=True)

def get():
    if not A or not C: return None
    r = subprocess.run(["xreach","tweets",f"@{U}","-n","10","--auth-token",A,"--ct0",C,"--json"],capture_output=True,text=True,timeout=30)
    try: return json.loads(r.stdout).get("items")
    except: return None

async def send(m):
    if not TB or not TC: return
    import aiohttp
    async with aiohttp.ClientSession() as s:
        await s.post(f"https://api.telegram.org/bot{TB}/sendMessage",json={"chat_id":TC,"text":m})

async def main():
    log(f"Started: @{U}")
    await send(f"Twitter监控启动: @{U}")
    last = None
    while True:
        t = get()
        if t:
            from email.utils import parsedate_to_datetime
            for x in t: x['_ts']=parsedate_to_datetime(x['createdAt']).timestamp()
            t.sort(key=lambda x:x['_ts'],reverse=True)
            if last and t[0]['_ts']>last:
                await send(f"🐦 @{U} 新推文!\n\n{t[0]['text'][:300]}\n\nhttps://twitter.com/{U}/status/{t[0]['id']}")
            last = t[0]['_ts']
        await asyncio.sleep(60)

if __name__=="__main__": asyncio.run(main())
