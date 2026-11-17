#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""定位解密三参数：wxid / 会话hash / 月份目录。不改任何文件，只读。"""
import os, glob, json, argparse

def find_base():
    root = os.path.expanduser("~/Library/Containers/com.tencent.xinWeChat/"
                              "Data/Documents/xwechat_files")
    if not os.path.isdir(root):
        raise SystemExit("未找到微信数据目录（仅支持 macOS 微信桌面版）")
    cands = [d for d in os.listdir(root) if d.startswith("wxid_") or d.startswith("gh_")]
    # 优先取含 msg/ 的
    good = [d for d in cands if os.path.isdir(os.path.join(root, d, "msg"))]
    if not good:
        raise SystemExit("没找到带 msg/ 的账号目录，请确认微信已登录")
    return root, sorted(good)

def key_wxid(dirname):
    """wxid_xxx_yyy -> wxid_xxx（去掉最后一段后缀）；已验证 md5(CODE+key_wxid)[:16]"""
    parts = dirname.split("_")
    if len(parts) >= 3 and not parts[-1].isdigit():
        return "_".join(parts[:-1])
    return dirname

def sessions(base, month=None):
    out = []
    att = os.path.join(base, "msg", "attach")
    if not os.path.isdir(att):
        return out
    for h in os.listdir(att):
        hp = os.path.join(att, h)
        if not os.path.isdir(hp):
            continue
        months = sorted(m for m in os.listdir(hp) if os.path.isdir(os.path.join(hp, m)))
        if not months:
            continue
        imgs = sum(len(glob.glob(os.path.join(hp, m, "Img", "*.dat"))) for m in months)
        vids = sum(len(glob.glob(os.path.join(hp, m, "*.dat"))) for m in months)
        out.append({"hash": h, "months": months, "img_dat": imgs, "video_dat": vids})
    out.sort(key=lambda x: -x["img_dat"])
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", help="只显示含该月份的会话，如 2026-10")
    a = ap.parse_args()
    root, accs = find_base()
    for acc in accs:
        base = os.path.join(root, acc)
        print("=" * 60)
        print(f"账号目录 : {acc}")
        print(f"解密用WXID: {key_wxid(acc)}      <-- 传给 --wxid")
        print(f"视频目录 : {os.path.join(base, 'msg', 'video')}")
        ss = sessions(base, a.month)
        print(f"会话数   : {len(ss)}（按图片块数降序）")
        for s in ss[:15]:
            if a.month and a.month not in s["months"]:
                continue
            print(f"  hash={s['hash']}  月份={','.join(s['months'])}  "
                  f"img.dat={s['img_dat']}")
        # 视频月份
        vd = os.path.join(base, "msg", "video")
        if os.path.isdir(vd):
            ms = sorted(m for m in os.listdir(vd) if os.path.isdir(os.path.join(vd, m)))
            print(f"视频月份 : {','.join(ms)}")
    print("=" * 60)
    print("下一步: python3 wx_probe.py --code <CODE> --wxid <上面的WXID> --dat <任一.dat>")

if __name__ == "__main__":
    main()
