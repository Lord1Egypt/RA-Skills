#!/usr/bin/env python3
"""把竖屏切片批量发小红书(经 social-auto-upload 的 xiaohongshu_uploader)。读取 publish.json。
⚠️ 小红书风控最严(搬运/重复内容/自动化),务必小批量、大间隔、先试 1 条;且会自动勾原创声明(搬运慎用)。
  cd <social-auto-upload>
  PYTHONPATH=. .venv/bin/python <skill>/scripts/publish_xiaohongshu.py --config publish.json --idx 1 --gap 90
注: 标题 ≤20 字; thumbnail 字段为封面图(建议 3:4)。"""
import argparse, asyncio, json, os, time
from pathlib import Path
from conf import BASE_DIR
from uploader.xiaohongshu_uploader.main import XIAOHONGSHU_PUBLISH_STRATEGY_IMMEDIATE, XiaoHongShuVideo
def pidx(a,n):
    if not a: return range(1,n+1)
    o=[]
    for p in str(a).split(","):
        o+=range(int(p.split('-')[0]),int(p.split('-')[1])+1) if '-' in p else [int(p)]
    return o
ap=argparse.ArgumentParser();ap.add_argument("--config",required=True);ap.add_argument("--idx");ap.add_argument("--gap",type=float,default=90.0);a=ap.parse_args()
cfg=json.load(open(a.config,encoding="utf-8"));acct=str(Path(BASE_DIR)/"cookies"/"xiaohongshu_uploader"/"account.json");vdir=os.path.expanduser(cfg["video_dir"]);items=cfg["items"]
for k in pidx(a.idx,len(items)):
    it=items[k-1];cv=os.path.expanduser(it["thumbnail"]) if it.get("thumbnail") else None
    print(f"\n=== 小红书[{k}] {it['file']} ===",flush=True)
    app=XiaoHongShuVideo(title=it["title"],file_path=os.path.join(vdir,it["file"]),desc=it.get("desc",""),tags=it.get("tags",[]),
        publish_strategy=XIAOHONGSHU_PUBLISH_STRATEGY_IMMEDIATE,publish_date=0,account_file=acct,thumbnail_path=cv)
    try: asyncio.run(app.xiaohongshu_upload_video()); print(f">>> 小红书[{k}] 完成",flush=True)
    except Exception as e: print(f"!!! 小红书[{k}] 失败: {e}",flush=True)
    time.sleep(a.gap)
print(">>> XHS_DONE",flush=True)
