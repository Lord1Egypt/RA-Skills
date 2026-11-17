#!/usr/bin/env python3
"""Universal Netlist JSON (.netlist.json) 本地查询器 —— schematic-reader 的 L1-J 档。

定位：不依赖 MCP / Node / universal-netlist，纯 Python 直接查 .netlist.json。
用途：
1. MCP/npx 不可用时的完整查询兜底（批量查询本就该走本地）
2. 别处导出的 .netlist.json（格式是开放标准，可被任何工具消费）
3. 提交进 git 做版本 diff 的快照直接查

子命令与 un_mcp.py 对齐（同义不同源，Agent 可无缝切换）：
  python netlist_json.py nets <file>                     # 全部网络（名+成员数）
  python netlist_json.py components <file> [--type R]    # 器件清单
  python netlist_json.py comp <file> U1                  # 单器件全引脚+MPN+value
  python netlist_json.py xnet <file> --net VDD           # 按网名追连通链（穿透 0Ω/电感/磁珠）
  python netlist_json.py xnet <file> --pin U1.H23        # 按引脚追连通链
  python netlist_json.py search <file> --nets --pattern I2C     # 网名正则
  python netlist_json.py search <file> --by mpn --pattern TPS   # 器件字段搜索（refdes/mpn/description/value）
  python netlist_json.py overview <file>                 # 工程速览
  python netlist_json.py erc <file>                      # single_pin / NC / 未命名网 事实枚举
  python netlist_json.py nc <file> [refdes]              # NC（未连接）引脚枚举

口径说明（与 MCP 的差异，诚实声明）：
- xnet 的"串联穿透"是本地保守实现：只穿透 value 为 0Ω 类（0/0R/0Ω/0ohm）或
  refdes 前缀 L/FB 的两端器件。MCP 的穿透规则可能更宽，关键结论用 MCP 复核。
- netlistHash 软校验：上游 canonicalization（JS 侧）未复现，哈希不符只 warning
  不阻塞；完整性以 universal-netlist 加载结果为准。

只读、确定性、不猜。输出 JSON 或文本，退出码 0=正常 1=空/限制 2=用法或文件错误。
"""
import argparse
import json
import os
import re
import sys

# Windows GBK 控制台保护：中文输出强制 UTF-8
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SCHEMA_KEY = "universalNetlistSchemaVersion"

# 0Ω 类 value（归一化后比较，大小写/符号不敏感）
ZERO_OHM = {"0", "0r", "0ohm", "0ω", "0欧", "0欧姆", "0r0"}
# 串联穿透候选的 refdes 前缀（电感/磁珠，物理上就是串在线路里）
BRIDGE_PREFIXES = {"L", "FB", "FL"}

COMPONENT_PREFIXES = ["C", "R", "U", "D", "L", "Q", "J", "P", "K", "F", "T",
                      "SW", "MK", "Y", "FB", "RV", "TP", "X", "Z", "BT", "SP", "LED", "FL", "CN"]

MCU_KEYWORDS = ("mcu", "soc", "controller", "processor", "fpga", "transceiver",
                "bluetooth", "wifi", "cpu", "dsp")
# 词边界匹配，防 Socket 误中 soc / Connector 误中 cpu 这类子串坑
MCU_RE = re.compile(r"(?i)\b(" + "|".join(MCU_KEYWORDS) + r")\b")
POWER_NET_RE = re.compile(r"(?i)^(VDD|VCC|VBUS|VIN|VLDA|VLDB|VBAT|VOUT|V5|V3|V1|V2|V18|GND|AGND|DGND|PGND)")


# ---------------------------------------------------------------- 加载与校验

def load_netlist(path):
    """加载 .netlist.json 并做结构硬校验 + 哈希软校验。返回 (doc, warnings)。"""
    if not os.path.exists(path):
        print(f"ERROR: 文件不存在 {path}", file=sys.stderr)
        sys.exit(2)
    try:
        with open(path, encoding="utf-8") as f:
            doc = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: 不是合法 JSON（{e}）。"
              f"确认是 universal-netlist 导出的 .netlist.json（导出命令："
              f"npx -y @intelligentelectron/universal-netlist export-json <design>）", file=sys.stderr)
        sys.exit(2)
    except UnicodeDecodeError as e:
        print(f"ERROR: 文件不是 UTF-8 文本（{e}）——.netlist.json 应为 UTF-8 JSON", file=sys.stderr)
        sys.exit(2)

    warnings = []
    ver = doc.get(SCHEMA_KEY)
    if not isinstance(ver, int):
        print(f"ERROR: 缺少 {SCHEMA_KEY} 或不是整数——普通 JSON 不是 Universal Netlist，"
              f"即使它含有 nets/components 键", file=sys.stderr)
        sys.exit(2)
    if ver not in (1, 2):
        warnings.append(f"schema 版本 v{ver} 不在已知范围 (1,2)，按通用结构解析")

    nets, comps = doc.get("nets"), doc.get("components")
    if not isinstance(nets, dict) or not isinstance(comps, dict):
        print("ERROR: nets/components 缺失或不是对象——文件结构不符 Universal Netlist schema",
              file=sys.stderr)
        sys.exit(2)
    for refdes, c in comps.items():
        if not isinstance(c, dict) or not isinstance(c.get("pins"), dict):
            warnings.append(f"器件 {refdes} 缺 pins 对象（schema 违规，跳过该器件的引脚查询）")

    meta = doc.get("metadata") or {}
    declared = meta.get("netlistHash")
    if not declared:
        warnings.append("metadata.netlistHash 缺失（结构不完整）")
    else:
        # 软校验：上游 JS canonicalization 未复现，不符只警告不阻塞
        warnings.append(f"netlistHash 声明值 {declared[:23]}…（软校验未复现上游算法，"
                        f"完整性以 universal-netlist 加载为准）")
    return doc, warnings


# ---------------------------------------------------------------- 数据访问辅助

def aslist(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def pin_net(entry):
    """PinEntry: 字符串=网名；对象={name, net}。"""
    if isinstance(entry, dict):
        return entry.get("net") or ""
    return entry or ""


def pin_name(entry, num):
    if isinstance(entry, dict):
        return entry.get("name") or num
    return num


def norm_value(v):
    return (v or "").strip().lower().replace(" ", "").replace("ω", "ω")


def is_bridge(refdes, comp):
    """是否串联穿透候选：0Ω 类 value 或 L/FB/FL 前缀。"""
    if refdes.upper().rstrip("0123456789") in BRIDGE_PREFIXES:
        return True
    return norm_value(comp.get("value")) in ZERO_OHM


def other_net_of(comp, cur_net):
    """两端器件的另一端网络（None 表示是终点/多端器件）。"""
    others = []
    for entry in (comp.get("pins") or {}).values():
        n = pin_net(entry)
        if n and n != cur_net:
            others.append(n)
    uniq = list(dict.fromkeys(others))
    return uniq[0] if len(uniq) == 1 else None


def expand_nets(doc, start_nets):
    """从起始网络集合 BFS 穿透串联器件，返回 (全网集合, 穿透路径列表)。"""
    nets, comps = doc["nets"], doc["components"]
    seen = set(n for n in start_nets if n in nets)
    frontier = list(seen)
    bridges = []
    while frontier:
        net = frontier.pop()
        for refdes, pins in (nets.get(net) or {}).items():
            comp = comps.get(refdes)
            if not comp or not is_bridge(refdes, comp):
                continue
            for pin in aslist(pins):
                other = other_net_of(comp, net)
                if other and other not in seen:
                    seen.add(other)
                    frontier.append(other)
                    bridges.append({"via": refdes, "value": comp.get("value"),
                                    "from_net": net, "to_net": other})
    return seen, bridges


def find_pin_net(doc, refdes, pin):
    comp = doc["components"].get(refdes)
    if not comp:
        return None
    entry = (comp.get("pins") or {}).get(pin)
    if entry is None:
        return None
    return pin_net(entry) or None


# ---------------------------------------------------------------- 子命令实现

def cmd_nets(doc, args):
    nets = doc["nets"]
    rows = []
    for name, members in sorted(nets.items()):
        pin_count = sum(len(aslist(p)) for p in members.values())
        rows.append({"net": name, "refdes_count": len(members), "pin_count": pin_count})
    if args.pattern:
        rx = re.compile(args.pattern, re.IGNORECASE)
        rows = [r for r in rows if rx.search(r["net"])]
    print(f"网络总数: {len(nets)}" + (f"（pattern 命中 {len(rows)}）" if args.pattern else ""))
    for r in rows:
        print(f"  {r['net']}  [{r['refdes_count']} 器件 / {r['pin_count']} 脚]")


def cmd_components(doc, args):
    comps = doc["components"]
    rows = []
    for refdes, c in comps.items():
        prefix = refdes.upper().rstrip("0123456789")
        if args.type and not refdes.upper().startswith(args.type.upper()):
            continue
        rows.append((refdes, prefix, c))
    print(f"器件总数: {len(comps)}" + (f"（type={args.type} 命中 {len(rows)}）" if args.type else ""))
    for refdes, prefix, c in rows:
        mpn = c.get("mpn") or c.get("internal_pn") or "-"
        val = c.get("value") or "-"
        desc = (c.get("description") or "")[:60]
        dns = " [DNS]" if c.get("dns") else ""
        print(f"  {refdes:8s} {val:16s} {mpn:28s} {desc}{dns}")


def cmd_comp(doc, args):
    comps = doc["components"]
    if args.refdes not in comps:
        near = [r for r in comps if r.upper() == args.refdes.upper()]
        if near:
            print(f"提示: refdes 大小写不匹配，实际是 {near[0]}", file=sys.stderr)
        print(f"ERROR: 器件 {args.refdes} 不存在。全部器件: {len(comps)} 个，"
              f"先 `components` 子命令列清单", file=sys.stderr)
        sys.exit(2)
    c = comps[args.refdes]
    print(f"{args.refdes}: {c.get('value') or '-'} | {c.get('mpn') or '-'} | "
          f"{c.get('manufacturer') or '-'} | {c.get('description') or '-'}")
    if c.get("dns"):
        print("  标记: DNS（不贴装）")
    if c.get("comment"):
        print(f"  注释: {c['comment']}")
    print(f"引脚 ({len(c.get('pins') or {})}):")
    for num, entry in sorted((c.get("pins") or {}).items(),
                             key=lambda kv: (len(kv[0]), kv[0])):
        net = pin_net(entry) or "NC(未连接)"
        print(f"  {num:>5s} {pin_name(entry, num):12s} → {net}")


def cmd_xnet(doc, args):
    if args.net:
        start = [args.net] if args.net in doc["nets"] else []
        if not start:
            print(f"ERROR: 网络 {args.net} 不存在。先 `nets` 列全部网络名", file=sys.stderr)
            sys.exit(2)
        origin = f"net:{args.net}"
    elif args.pin:
        if "." not in args.pin:
            print("ERROR: --pin 格式是 REFDES.PIN（如 U1.H23）", file=sys.stderr)
            sys.exit(2)
        refdes, pin = args.pin.split(".", 1)
        net = find_pin_net(doc, refdes, pin)
        if net is None:
            print(f"ERROR: 引脚 {args.pin} 不存在或未连接（NC）", file=sys.stderr)
            sys.exit(2)
        start = [net]
        origin = f"pin:{args.pin}"
    else:
        print("ERROR: 需要 --net 或 --pin", file=sys.stderr)
        sys.exit(2)

    reached, bridges = expand_nets(doc, start)
    print(f"连通链（起点 {origin}，穿透 {len(bridges)} 个串联器件，共 {len(reached)} 个网络）:")
    if bridges:
        print("穿透路径:")
        for b in bridges:
            print(f"  {b['from_net']} —[{b['via']} {b['value']}]— {b['to_net']}")
    print("网络成员:")
    for net in sorted(reached):
        members = doc["nets"].get(net, {})
        detail = ", ".join(f"{r}:{'/'.join(aslist(p))}" for r, p in sorted(members.items()))
        print(f"  {net}: {detail}")


def cmd_search(doc, args):
    if not args.pattern:
        print("ERROR: search 需要 --pattern", file=sys.stderr)
        sys.exit(2)
    try:
        rx = re.compile(args.pattern, re.IGNORECASE)
    except re.error as e:
        print(f"ERROR: 正则无效: {e}", file=sys.stderr)
        sys.exit(2)
    if args.nets:
        hits = [n for n in doc["nets"] if rx.search(n)]
        print(f"网名命中 ({len(hits)}):")
        for n in hits:
            print("  ", n)
    else:
        field = args.by or "mpn"
        hits = []
        for refdes, c in doc["components"].items():
            if field == "refdes":
                if rx.search(refdes):
                    hits.append((refdes, c))
            elif rx.search(c.get(field) or ""):
                hits.append((refdes, c))
        print(f"器件 {field} 命中 ({len(hits)}):")
        for refdes, c in hits:
            print(f"  {refdes}: {c.get('value') or '-'} | {c.get('mpn') or '-'} | "
                  f"{(c.get('description') or '')[:50]}")


def cmd_overview(doc, args):
    comps, nets = doc["components"], doc["nets"]
    counts = {}
    for refdes in comps:
        p = refdes.upper().rstrip("0123456789")
        counts[p] = counts.get(p, 0) + 1
    print(f"器件总数: {sum(counts.values())}")
    print("  " + "、".join(f"{k}×{v}" for k, v in sorted(counts.items(), key=lambda x: -x[1])))
    print(f"网络总数: {len(nets)}")
    print("\n主控/核心候选（关键词命中 description/value）:")
    hit = 0
    for refdes, c in comps.items():
        text = f"{c.get('description') or ''} {c.get('value') or ''}"
        if MCU_RE.search(text):
            print(f"  {refdes}: {c.get('value') or '-'} — {(c.get('description') or '')[:60]}")
            hit += 1
    if not hit:
        print("  （无命中，用 search --by description 自查）")
    print("\n电源/地网络候选:")
    for n in sorted(nets):
        if POWER_NET_RE.match(n):
            print("  ", n)
    nc = sum(1 for c in comps.values() for e in (c.get("pins") or {}).values()
             if not pin_net(e))
    sp = sum(1 for n, m in nets.items() if sum(len(aslist(p)) for p in m.values()) == 1)
    print(f"\nNC(未连接)引脚: {nc} 个 | 单脚网络: {sp} 个（erc 子命令看明细）")


def cmd_erc(doc, args):
    """事实枚举：single_pin / NC / 未命名网。不是审查结论，是解析器视角的机器事实。"""
    nets, comps = doc["nets"], doc["components"]
    single = []
    for name, members in nets.items():
        if sum(len(aslist(p)) for p in members.values()) == 1:
            single.append((name, members))
    nc = []
    for refdes, c in comps.items():
        for num, entry in (c.get("pins") or {}).items():
            if not pin_net(entry):
                nc.append((refdes, num))
    unnamed = [n for n in nets if re.match(r"(?i)^(net|n\$|wire)", n)]
    if getattr(args, "format", "text") == "json":
        print(json.dumps({
            "single_pin": {n: m for n, m in single},
            "nc_pins": [f"{r}.{num}" for r, num in nc],
            "unnamed_nets": unnamed,
            "note": "解析事实枚举；正常/异常判断交给使用者",
        }, ensure_ascii=False, indent=2))
        return
    print(f"single_pin（网络只挂一个脚）: {len(single)}")
    for name, members in single:
        print(f"  {name} → {members}")
    print(f"NC（引脚未连接，net 为空）: {len(nc)}")
    for refdes, num in nc:
        print(f"  {refdes}.{num}")
    print(f"未命名风格网络（NetC3_2/N$5 这类自动名）: {len(unnamed)}")
    for n in unnamed:
        print("  ", n)
    print("口径: 以上为解析事实枚举，正常/异常判断交给使用者")


def cmd_nc(doc, args):
    comps = doc["components"]
    rows = []
    for refdes, c in comps.items():
        if args.refdes and refdes != args.refdes:
            continue
        for num, entry in (c.get("pins") or {}).items():
            if not pin_net(entry):
                rows.append((refdes, num, pin_name(entry, num), c.get("value")))
    if getattr(args, "format", "text") == "json":
        print(json.dumps({
            "count": len(rows),
            "pins": [{"refdes": r, "pin": num, "pin_name": name, "value": val}
                     for r, num, name, val in rows],
        }, ensure_ascii=False, indent=2))
        return
    print(f"NC 引脚: {len(rows)}")
    for refdes, num, name, val in rows:
        print(f"  {refdes}.{num} ({name}) {val or ''}")
    if rows:
        print("提示: 与 datasheet 引脚总数对照 = 未用脚集合（'哪些脚没用'的标准答法）")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Universal Netlist JSON 本地查询器（L1-J）")
    ap.add_argument("--format", choices=["text", "json"], default="text",
                    help="erc/nc 等可输出 JSON（默认 text）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("nets", help="列全部网络")
    p.add_argument("file")
    p.add_argument("--pattern", help="网名正则过滤")

    p = sub.add_parser("components", help="器件清单")
    p.add_argument("file")
    p.add_argument("--type", help="按 refdes 前缀过滤（如 R/C/U）")

    p = sub.add_parser("comp", help="单器件全引脚")
    p.add_argument("file")
    p.add_argument("refdes")

    p = sub.add_parser("xnet", help="追连通链（穿透 0Ω/电感/磁珠）")
    p.add_argument("file")
    p.add_argument("--net")
    p.add_argument("--pin", help="格式 REFDES.PIN")

    p = sub.add_parser("search", help="搜索网名或器件字段")
    p.add_argument("file")
    p.add_argument("--nets", action="store_true", help="搜网名（默认搜器件）")
    p.add_argument("--by", choices=["refdes", "mpn", "description", "value"],
                   default="mpn", help="器件搜索字段（默认 mpn）")
    p.add_argument("--pattern", help="正则（大小写不敏感）")

    sub.add_parser("overview", help="工程速览").add_argument("file")

    p = sub.add_parser("erc", help="single_pin/NC/未命名网 事实枚举")
    p.add_argument("file")

    p = sub.add_parser("nc", help="NC（未连接）引脚枚举")
    p.add_argument("file")
    p.add_argument("refdes", nargs="?", help="只看某个器件")

    args = ap.parse_args()
    doc, warnings = load_netlist(args.file)

    meta = doc.get("metadata") or {}
    if args.format == "text":
        print(f"文件: {args.file}")
        print(f"schema: v{doc.get(SCHEMA_KEY)} | 生成于 {meta.get('generatedAt') or '?'} | "
              f"来源: {json.dumps(meta.get('origin') or {}, ensure_ascii=False)}")
        for w in warnings:
            print(f"⚠ {w}")
        print()

    {"nets": cmd_nets, "components": cmd_components, "comp": cmd_comp,
     "xnet": cmd_xnet, "search": cmd_search, "overview": cmd_overview,
     "erc": cmd_erc, "nc": cmd_nc}[args.cmd](doc, args)


if __name__ == "__main__":
    main()
