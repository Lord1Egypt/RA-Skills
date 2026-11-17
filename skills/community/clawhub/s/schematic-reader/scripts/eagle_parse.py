#!/usr/bin/env python3
"""Eagle .sch 解析器（EAGLE 6+ XML 格式）——原理图识别的 L1 级离线网表来源。

格式事实（2026-10-21 实测 SparkFun Pi_Wedge v12 样例验证）：
  EAGLE 6.0 (2011) 起 .sch 为 UTF-8 XML（eagle.dtd），连通性显式存在：
    drawing/schematic/parts/part          → 器件（name/value/library/deviceset）
    drawing/schematic/sheets/sheet/nets/net
      → <signal name="GND"> / segment / pinref(part, pin) = 连通成员
  EAGLE ≤5 为二进制，不公开——明确拒识并引导重存。
  .sch 扩展名被多工具共用（KiCad legacy/OrCAD/TINA/LTspice）——先看文件头判源。

用法：
  python eagle_parse.py <file.sch>                # overview
  python eagle_parse.py <file.sch> nets [--pattern RX]
  python eagle_parse.py <file.sch> comp U1
  python eagle_parse.py <file.sch> xnet --net GND
  python eagle_parse.py <file.sch> search --by value --pattern LM
  python eagle_parse.py <file.sch> erc            # single_pin 确定性枚举

定位：只输出确定性解析事实（XML 直读），不做审查判断。
"""
import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


def load(path):
    if not os.path.exists(path):
        die(f"文件不存在: {path}")
    with open(path, "rb") as f:
        head = f.read(512)
    if b"<eagle" not in head and b"eagle.dtd" not in head:
        if head.lstrip().startswith(b"<!DOCTYPE"):
            die("是 XML 但不是 Eagle 格式（无 <eagle> 根）——.sch 扩展名被多工具共用"
                "（KiCad legacy/OrCAD/LTspice/TINA），确认来源")
        die("不是 EAGLE 6+ XML 格式（EAGLE ≤5 为二进制不公开）。\n"
            "  处置: 用 Eagle/Fusion 打开重存为 XML 版 .sch，"
            "或用 KiCad 导入后转 .kicad_pro（本 skill 支持）")
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        die(f"XML 解析失败: {e}")
    root = tree.getroot()
    schem = root.find("drawing/schematic")
    if schem is None:
        die("是 Eagle XML 但没有 drawing/schematic 段——这可能是 .brd（板框文件）")
    return schem


def build_model(path):
    schem = load(path)
    parts = {}
    for p in schem.iter("part"):
        parts[p.get("name", "")] = {
            "value": p.get("value", ""),
            "library": p.get("library", ""),
            "deviceset": p.get("deviceset", ""),
            "device": p.get("device", ""),
        }
    nets = {}
    for net in schem.iter("net"):
        name = net.get("name", "")
        members = []
        for seg in net.iter("segment"):
            for pr in seg.findall("pinref"):
                members.append((pr.get("part", ""), pr.get("pin", "")))
        nets[name] = members
    return {"file": path, "parts": parts, "nets": nets}


# ---------------------------------------------------------------- 子命令

def cmd_overview(model):
    refs = sorted(model["parts"])
    by_prefix = {}
    for r in refs:
        by_prefix.setdefault(re.match(r"^[A-Za-z]+", r).group(0).upper(), []).append(r)
    print(f"文件: {model['file']}  (EAGLE 6+ XML, L1 级确定性解析)")
    print(f"器件总数: {len(refs)}   网络总数: {len(model['nets'])}")
    print("  " + "、".join(f"{k}×{len(v)}" for k, v in
                           sorted(by_prefix.items(), key=lambda x: -len(x[1]))))
    singles = [n for n, m in model["nets"].items() if len(m) <= 1]
    if singles:
        print(f"single_pin/空网: {len(singles)}（erc 子命令细看）")


def cmd_nets(model, pattern=None):
    for net in sorted(model["nets"]):
        if pattern and not re.search(pattern, net, re.I):
            continue
        print(f"{net}  [{len(model['nets'][net])} 脚]")


def cmd_comp(model, refdes):
    info = model["parts"].get(refdes)
    if info is None:
        print(f"{refdes}: parts 清单无此器件")
        return
    print(f"{refdes}: value={info['value']}")
    print(f"  deviceset={info['deviceset']}  library={info['library']}")
    hits = [(net, pin) for net, members in model["nets"].items()
            for (r, pin) in members if r == refdes]
    print(f"  挂网 {len(hits)} 个:")
    for net, pin in sorted(hits):
        print(f"  {pin:<8} → {net}")


def cmd_xnet(model, net_name):
    members = model["nets"].get(net_name)
    if members is None:
        die(f"网络不存在: {net_name}（nets 子命令列全部）")
    print(f"{net_name} ({len(members)} 脚):")
    for refdes, pin in sorted(members):
        info = model["parts"].get(refdes, {})
        print(f"  {refdes:<8} {pin:<10} {info.get('value', '')[:45]}")


def cmd_search(model, by, pattern):
    try:
        rx = re.compile(pattern, re.I)
    except re.error as e:
        die(f"正则非法: {e}")
    if by == "nets":
        cmd_nets(model, pattern)
        return
    for r, info in sorted(model["parts"].items()):
        hay = {"value": info.get("value", ""),
               "refdes": r,
               "deviceset": info.get("deviceset", "")}.get(by, "")
        if rx.search(hay):
            print(f"{r}: {info.get('value', '')}  [{info.get('deviceset', '')}]")


def cmd_erc(model):
    singles = {n: m for n, m in model["nets"].items() if len(m) == 1}
    print(f"single_pin 网络（确定性枚举，解读归大模型）: {len(singles)}")
    for n in sorted(singles):
        r, p = singles[n][0]
        print(f"  {n}: {r}.{p}")


def main():
    ap = argparse.ArgumentParser(description="Eagle 6+ .sch XML 解析器")
    ap.add_argument("sch")
    sub = ap.add_subparsers(dest="cmd")
    p_nets = sub.add_parser("nets")
    p_nets.add_argument("--pattern")
    p_comp = sub.add_parser("comp")
    p_comp.add_argument("refdes")
    p_xnet = sub.add_parser("xnet")
    p_xnet.add_argument("--net", required=True)
    p_search = sub.add_parser("search")
    p_search.add_argument("--by", choices=["refdes", "value", "deviceset", "nets"],
                          default="value")
    p_search.add_argument("--pattern", required=True)
    sub.add_parser("erc")
    sub.add_parser("overview")

    args = ap.parse_args()
    model = build_model(args.sch)
    cmd = args.cmd or "overview"
    if cmd == "overview":
        cmd_overview(model)
    elif cmd == "nets":
        cmd_nets(model, args.pattern)
    elif cmd == "comp":
        cmd_comp(model, args.refdes)
    elif cmd == "xnet":
        cmd_xnet(model, args.net)
    elif cmd == "search":
        cmd_search(model, args.by, args.pattern)
    elif cmd == "erc":
        cmd_erc(model)


if __name__ == "__main__":
    main()
