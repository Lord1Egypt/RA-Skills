#!/usr/bin/env python3
"""把竖屏切片批量发抖音(经 social-auto-upload 的 douyin_uploader)。读取 publish.json。
前置: social-auto-upload 已装+已登录抖音; PYTHONPATH 指向其根目录, 用其 venv 运行。
  cd <social-auto-upload>
  PYTHONPATH=. .venv/bin/python <skill>/scripts/publish_douyin.py --config publish.json --idx 1
封面: 若 publish.json 的 item 有 thumbnail 字段则用作竖封面, 否则用视频首帧。"""
import argparse, asyncio, json, os, time
from pathlib import Path
from conf import BASE_DIR
from uploader.douyin_uploader.main import DOUYIN_PUBLISH_STRATEGY_IMMEDIATE, DouYinVideo
def pidx(a,n):
    if not a: return range(1,n+1)
    o=[]
    for p in str(a).split(","):
        o+=range(int(p.split('-')[0]),int(p.split('-')[1])+1) if '-' in p else [int(p)]
    return o
ap=argparse.ArgumentParser();ap.add_argument("--config",required=True);ap.add_argument("--idx");ap.add_argument("--gap",type=float,default=45.0);a=ap.parse_args()
cfg=json.load(open(a.config,encoding="utf-8"));acct=str(Path(BASE_DIR)/"cookies"/"douyin_uploader"/"account.json");vdir=os.path.expanduser(cfg["video_dir"]);items=cfg["items"]
for k in pidx(a.idx,len(items)):
    it=items[k-1];cv=os.path.expanduser(it["thumbnail"]) if it.get("thumbnail") else None
    print(f"\n=== 抖音[{k}] {it['file']} ===",flush=True)
    app=DouYinVideo(title=it["title"],file_path=os.path.join(vdir,it["file"]),tags=it.get("tags",[]),publish_date=0,
        account_file=acct,thumbnail_landscape_path=cv,thumbnail_portrait_path=cv,publish_strategy=DOUYIN_PUBLISH_STRATEGY_IMMEDIATE)
    try: asyncio.run(app.douyin_upload_video()); print(f">>> 抖音[{k}] 完成",flush=True)
    except Exception as e: print(f"!!! 抖音[{k}] 失败: {e}",flush=True)
    time.sleep(a.gap)
print(">>> DOUYIN_DONE",flush=True)
