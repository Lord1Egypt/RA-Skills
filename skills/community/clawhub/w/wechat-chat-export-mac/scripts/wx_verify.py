#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验收：stem 集合比对，输出缺口数（目标=0）。不要用感知哈希——会误报。
用法: python3 wx_verify.py --src <原始Img目录> --dst <交付目录>
      可选 --month-dir <按月份的原始目录，多个用逗号分隔>
"""
import os, glob, argparse

def stems_of(dat_dir):
    full, thumb = set(), set()
    for p in glob.glob(os.path.join(dat_dir, "**", "*.dat"), recursive=True):
        b = os.path.basename(p)
        if b.endswith("_t.dat"):
            thumb.add(b[:-6])
        else:
            full.add(b[:-4])
    return full, thumb

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="原始 .dat 目录（可递归）")
    ap.add_argument("--dst", required=True, help="交付目录（图片所在）")
    a = ap.parse_args()

    full, thumb = stems_of(a.src)
    # 需要交付的 = 有缩略图但没有原图的（原图缺失才需要补）
    need = thumb - full
    # 交付目录里所有图片 stem
    delivered = set()
    for f in os.listdir(a.dst):
        p = os.path.join(a.dst, f)
        if os.path.isdir(p):
            for g in os.listdir(p):
                delivered.add(os.path.splitext(g)[0])
        else:
            delivered.add(os.path.splitext(f)[0])

    missing = need - delivered
    # 同时看 full 里有没有漏交付
    miss_full = full - delivered
    print(f"原始 .dat : full={len(full)}  thumb={len(thumb)}")
    print(f"需补原图  : {len(need)}")
    print(f"已交付    : {len(delivered)}")
    print(f"thumb缺口 : {len(missing)}   full缺口: {len(miss_full)}")
    if missing:
        print("  缺 thumb 样例:", list(sorted(missing))[:5])
    if miss_full:
        print("  缺 full 样例:", list(sorted(miss_full))[:5])
    total = len(missing) + len(miss_full)
    print("\n" + ("✅ 缺口 = 0，验收通过" if total == 0 else f"❌ 总缺口 = {total}"))
    raise SystemExit(0 if total == 0 else 4)

if __name__ == "__main__":
    main()
