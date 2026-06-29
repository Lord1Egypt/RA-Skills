#!/usr/bin/env python3
"""
把竖屏切片批量发布到微信视频号(经 social-auto-upload 的 tencent_uploader)。
读取 publish.json(见 examples/publish.example.json)。

前置:
  1. 已安装 social-auto-upload(见 setup.sh 或 README)，并在其 cookies/tencent_uploader/account.json 完成登录。
  2. 用其自带的 venv 运行本脚本，且 PYTHONPATH 指向 social-auto-upload 根目录。

用法(示例):
  cd <social-auto-upload>
  PYTHONPATH=. .venv/bin/python <skill>/scripts/publish_shipinhao.py \
      --config publish.json [--idx 1-12] [--draft]

⚠️ 视频号无官方发布 API，这是浏览器自动化，属平台灰色地带、有账号风险；
   短时间大批量易触发风控，脚本默认每条间隔 40s，建议错峰/小批量。
   注意：当前 social-auto-upload 的「保存草稿」选择器在新版视频号助手下会超时，
   稳定可用的是「直接发表」(is_draft=False)。
"""
import argparse, asyncio, json, os, sys, time

def parse_idx(arg, n):
    if not arg: return list(range(1, n+1))
    out=[]
    for part in str(arg).split(","):
        if "-" in part:
            a,b=part.split("-"); out+=list(range(int(a),int(b)+1))
        else: out.append(int(part))
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True)
    ap.add_argument("--idx",default=None,help="如 1-12 或 2,5,7；默认全部")
    ap.add_argument("--draft",action="store_true",help="存草稿(注意新版视频号助手可能超时)")
    ap.add_argument("--gap",type=float,default=40.0,help="每条间隔秒数")
    a=ap.parse_args()

    from conf import BASE_DIR  # noqa  (须 PYTHONPATH=social-auto-upload 根)
    from uploader.tencent_uploader.main import TENCENT_PUBLISH_STRATEGY_IMMEDIATE, TencentVideo

    cfg=json.load(open(a.config,encoding="utf-8"))
    account=os.path.expanduser(cfg.get("account_file",
        str(__import__("pathlib").Path(BASE_DIR)/"cookies"/"tencent_uploader"/"account.json")))
    vdir=os.path.expanduser(cfg["video_dir"])
    items=cfg["items"]
    idxs=parse_idx(a.idx,len(items))
    for k in idxs:
        it=items[k-1]
        f=os.path.join(vdir,it["file"])
        print(f"\n===== [{k}] {it['file']} ({'草稿' if a.draft else '发表'}) =====",flush=True)
        app=TencentVideo(
            title=it["title"], file_path=f, tags=it.get("tags",[]),
            publish_strategy=TENCENT_PUBLISH_STRATEGY_IMMEDIATE, publish_date=0,
            account_file=account, desc=it.get("desc",""),
            thumbnail_path=os.path.expanduser(it["thumbnail"]) if it.get("thumbnail") else None,
            short_title=it.get("short_title"), category=None, is_draft=a.draft,
        )
        try:
            asyncio.run(app.tencent_upload_video()); print(f">>> [{k}] 完成",flush=True)
        except Exception as e:
            print(f"!!! [{k}] 失败: {e}",flush=True)
        time.sleep(a.gap)
    print("\n>>> PUBLISH_DONE",flush=True)

if __name__=="__main__":
    main()
