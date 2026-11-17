#!/usr/bin/env python3
"""Cadence OrCAD .dat 三件套解析器（pstxnet/pstxprt/pstchip）——原理图识别的
离线网表来源，不依赖 universal-netlist MCP（上游不支持此格式）。

三件套是什么：
  pstxnet.dat  EXPANDEDNETLIST   网络→(器件,引脚) 成员清单——连通性主体
  pstxprt.dat  EXPANDEDPARTLIST  器件→PART_VALUE 映射 + ROOT_DRAWING 元数据
  pstchip.dat  LIBRARY_PARTS     PART→引脚功能名（可选，美化输出）

典型场景：拿到的是 OrCAD 生成的第三方网表包（三个 .dat 同目录），没有 .DSN。

用法：
  python cadence_dat_parse.py <目录|pstxnet.dat>            # overview
  python cadence_dat_parse.py <路径> nets [--pattern REGEX]  # 网络清单/搜索
  python cadence_dat_parse.py <路径> comp U5                 # 器件全引脚
  python cadence_dat_parse.py <路径> xnet --net VBUS         # 网络连通成员
  python cadence_dat_parse.py <路径> search --by mpn --pattern TPS

定位（与 skill 一致）：只输出确定性解析事实，不做审查判断。
置信度：L1 级（文本直读，引脚号来自 EXPANDEDNETLIST，非推理）。
"""
import argparse
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


def find_dat_files(path):
    """入参可以是目录或 pstxnet.dat 路径；返回 (xnet, xprt, chip) 三件套路径。"""
    if os.path.isdir(path):
        d = path
    else:
        if not os.path.exists(path):
            die(f"路径不存在: {path}")
        d = os.path.dirname(os.path.abspath(path))
    xnet = os.path.join(d, "pstxnet.dat")
    xprt = os.path.join(d, "pstxprt.dat")
    chip = os.path.join(d, "pstchip.dat")
    if not os.path.exists(xnet):
        hint = ""
        dats = [f for f in os.listdir(d) if f.lower().endswith(".dat")] \
            if os.path.isdir(d) else []
        if dats:
            hint = f"\n  同目录 .dat: {dats}（标准三件套是 pstxnet/pstxprt/pstchip）"
        die(f"找不到 pstxnet.dat（EXPANDEDNETLIST，连通性主体）{hint}")
    return xnet, xprt, chip


def read_text(path):
    """PSTWRITER 输出一般是 ASCII/latin-1 兼容；容错读。"""
    for enc in ("utf-8", "latin-1"):
        try:
            with open(path, encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    die(f"无法解码（非文本或损坏）: {path}")


def parse_xnet(path):
    """pstxnet.dat → {net: [(refdes, pin_number, pin_func_name), ...]}
    语法（实测 BeagleBone Black 样例）：
      NET_NAME 'VBUS' ... NODE_NAME<TAB>P3 1 <路径行> 'P1':;
    NODE_NAME 的 TAB 字段是 "REFDES PIN"，引脚功能名在两行后的 'NAME':;"""
    text = read_text(path)
    if "EXPANDEDNETLIST" not in text:
        die(f"{path} 不是 EXPANDEDNETLIST（FILE_TYPE 不符）——确认这是 pstxnet.dat")
    nets = {}
    cur = None
    pending_node = None   # (refdes, pin_num)
    for line in text.splitlines():
        ls = line.strip()
        if ls.startswith("NET_NAME"):
            cur = None
            pending_node = None
            continue
        if cur is None:
            m = re.match(r"^'(.+)':?;?$", ls)
            if m and not ls.startswith("C_"):
                cur = m.group(1)
                nets[cur] = []
            continue
        if ls.startswith("NODE_NAME"):
            body = ls[len("NODE_NAME"):].strip()
            m = re.match(r"^(.+)\s+(\S+)$", body)
            if not m:
                continue
            pending_node = (m.group(1), m.group(2))
            continue
        if pending_node is not None:
            # NODE_NAME 后固定两行：① 实例路径（'@XXX:INS...@...':，跳过）
            #                      ② 引脚功能名（'DDR_ODT':; 或 '2':;）
            # 实例路径必然含 '@'（@库.器件.实例 语法），功能名行不含——以此区分
            m = re.match(r"^'(.*)':?;?$", ls)
            if m and "@" not in m.group(1):
                refdes, pin = pending_node
                nets[cur].append((refdes, pin, m.group(1)))
                pending_node = None
    return nets


def parse_xprt(path):
    """pstxprt.dat → (root_drawing, {refdes: part_value})"""
    if not os.path.exists(path):
        return None, {}
    text = read_text(path)
    if "EXPANDEDPARTLIST" not in text:
        return None, {}
    root = None
    m = re.search(r"ROOT_DRAWING='([^']+)'", text)
    if m:
        root = m.group(1)
    parts = {}
    lines = text.splitlines()
    for i, line in enumerate(lines):
        ls = line.strip()
        if ls == "PART_NAME":
            m = re.match(r"^(.+?)\s+'(.+)':;$", lines[i + 1].strip())
            if m:
                parts[m.group(1)] = m.group(2)
    return root, parts


def parse_chip_pins(path):
    """pstchip.dat → {PART_NAME: {pin_number: pin_name}}（可选美化）"""
    if not os.path.exists(path):
        return {}
    text = read_text(path)
    result = {}
    cur_prim = None
    cur_pin = None
    in_pin_block = False
    for raw in text.splitlines():
        ls = raw.strip()
        m = re.match(r"^primitive\s+'(.+?)'", ls)
        if m:
            cur_prim = m.group(1)
            continue
        if ls == "pin":
            in_pin_block = True
            cur_pin = None
            continue
        if ls == "end_pin":
            in_pin_block = False
            continue
        if in_pin_block:
            mp = re.match(r"^'(.+?)':$", ls)
            if mp:
                cur_pin = mp.group(1)
                continue
            mn = re.match(r"^PIN_NUMBER='\(([^)]*)\)'", ls)
            if mn and cur_prim:
                result.setdefault(cur_prim, {})
                for pn in [p.strip() for p in mn.group(1).split(",") if p.strip()]:
                    result[cur_prim][pn] = cur_pin
    return result


def build_model(directory):
    xnet, xprt, chip = find_dat_files(directory)
    nets = parse_xnet(xnet)
    root, parts = parse_xprt(xprt)
    chip_pins = parse_chip_pins(chip)
    return {"dir": os.path.dirname(os.path.abspath(xnet)) or xnet,
            "root": root, "nets": nets, "parts": parts, "chip_pins": chip_pins}


def pin_display(refdes, pin, func, model):
    """显示引脚：号 + （若有）功能名。"""
    if func:
        return f"{pin}({func[:40]})"
    return pin


# ---------------------------------------------------------------- 子命令

def cmd_overview(model):
    n_nets = len(model["nets"])
    n_nodes = sum(len(v) for v in model["nets"].values())
    refs = sorted({r for members in model["nets"].values() for r, _, _ in members})
    by_prefix = {}
    for r in refs:
        by_prefix.setdefault(re.match(r"^[A-Za-z]+", r).group(0).upper(), []).append(r)
    print(f"root: {model['root'] or '(未声明，pstxprt 缺失)'}")
    print(f"网络总数: {n_nets}   连接节点: {n_nodes}   器件(出现在网表中): {len(refs)}")
    print("  " + "、".join(f"{k}×{len(v)}" for k, v in
                           sorted(by_prefix.items(), key=lambda x: -len(x[1]))))
    print(f"\n数据来源: pstxnet.dat(pstxprt {'有' if model['parts'] else '缺'})"
          f" —— L1 级确定性解析（引脚级连通性完整）")
    print("限制: variant/DNS 状态不在三件套内（那在 .DSN 的 CIS 数据里）；"
          "审查 variant 相关问题须拿 .DSN")


def cmd_nets(model, pattern=None):
    for net in sorted(model["nets"]):
        if pattern and not re.search(pattern, net, re.I):
            continue
        print(f"{net}  [{len(model['nets'][net])} 脚]")


def cmd_comp(model, refdes):
    hits = [(net, pin, func) for net, members in model["nets"].items()
            for (r, pin, func) in members if r.upper() == refdes.upper()]
    if not hits:
        print(f"{refdes}: 网表中无此器件（或只挂在未连线上）")
        return
    value = model["parts"].get(refdes, "?")
    print(f"{refdes}: {value}")
    print(f"  挂网 {len(hits)} 个:")
    for net, pin, func in sorted(hits):
        print(f"  {pin:<6} {pin_display(refdes, pin, func, model):<50} → {net}")


def cmd_xnet(model, net_name):
    members = model["nets"].get(net_name)
    if members is None:
        die(f"网络不存在: {net_name}（用 nets 子命令列全部）")
    print(f"{net_name} ({len(members)} 脚):")
    for refdes, pin, func in sorted(members):
        value = model["parts"].get(refdes, "")
        print(f"  {refdes:<8} {pin_display(refdes, pin, func, model):<50} {value[:40]}")


def cmd_search(model, by, pattern):
    try:
        rx = re.compile(pattern, re.I)
    except re.error as e:
        die(f"正则非法: {e}")
    if by == "nets":
        cmd_nets(model, pattern)
        return
    hits = set()
    for refdes, value in model["parts"].items():
        hay = value if by in ("mpn", "value") else refdes
        if rx.search(hay):
            hits.add(refdes)
    for r in sorted(hits):
        print(f"{r}: {model['parts'].get(r, '?')}")
    if not hits:
        print(f"（无命中——注意 .dat 三件套只有 PART_VALUE，无独立 MPN/description 字段；"
              f"PART_VALUE 通常是 libname+value 拼接）")


def cmd_erc_basic(model):
    """确定性枚举：single_pin 网络（只挂一个脚的网）——机器事实，不是审查结论。"""
    singles = {n: m for n, m in model["nets"].items() if len(m) == 1}
    print(f"single_pin 网络（确定性枚举，需大模型自行解读）: {len(singles)}")
    for n in sorted(singles):
        r, p, f = singles[n][0]
        print(f"  {n}: {r}.{p}")


def pin_sort_key(p):
    """引脚号排序：纯数字按数值，其余按字典——保证导出确定性（同一输入必同一字节）。"""
    try:
        return (0, int(p), "")
    except (TypeError, ValueError):
        return (1, 0, str(p))


def cmd_export_json(model, out_path=None):
    """导出 Universal Netlist JSON v2 —— 把 Cadence 三件套桥接到 .netlist.json 生态。

    为什么需要：netlist_json.py / universal-netlist 那套下游工具不吃 .dat，但吃 .netlist.json。
    导一份快照，Cadence 侧的工程就能用同一套 nets/comp/xnet/erc/nc 查询。

    口径（不猜原则）：只导出三件套里**实际存在**的事实——refdes / 引脚号 / 网名 / PART_VALUE。
    三件套里没有厂商 MPN 与 Manufacturer，一律写 "N.A."，不补不猜。
    """
    import datetime
    import hashlib

    nets_out, comps_out = {}, {}
    for net, members in model["nets"].items():
        entry = {}
        for refdes, pin, _func in members:
            entry.setdefault(refdes, [])
            if pin not in entry[refdes]:
                entry[refdes].append(pin)
            c = comps_out.setdefault(refdes, {"pins": {}})
            # 同一器件同引脚重复挂同名网时以先到为准（三件套里这是同一事实重复声明）
            c["pins"].setdefault(pin, net)
        for refdes in entry:
            entry[refdes].sort(key=pin_sort_key)
        nets_out[net] = entry
    for refdes, c in comps_out.items():
        value = model["parts"].get(refdes)
        ordered = {p: c["pins"][p] for p in sorted(c["pins"], key=pin_sort_key)}
        c["pins"] = ordered
        c["mpn"] = "N.A."
        c["manufacturer"] = "N.A."
        c["value"] = value or "N.A."
        c["description"] = (f"PART_VALUE={value}" if value
                            else "N.A.（pstxprt 未给出 PART_VALUE）")

    doc = {
        "universalNetlistSchemaVersion": 2,
        "metadata": {
            "generatedAt": datetime.datetime.now(datetime.timezone.utc)
                                   .strftime("%Y-%m-%dT%H:%M:%S.") +
                           datetime.datetime.now(datetime.timezone.utc)
                                   .strftime("%f")[:3] + "Z",
            "netlistHash": "",
            "origin": {
                "type": "vendor",
                "source": {"vendor": "Cadence", "fileType": ".dat/pstxnet"},
                "rootDrawing": model.get("root") or "",
            },
        },
        "nets": {k: nets_out[k] for k in sorted(nets_out)},
        "components": {k: comps_out[k] for k in sorted(comps_out)},
    }
    # 软校验哈希：canonical（排序键 + 紧凑分隔）后取 sha256；与 universal-netlist
    # 上游 JS 算法未必一致，下游按软校验处理（不符只 warning，不阻塞）
    canonical = json.dumps({"nets": doc["nets"], "components": doc["components"]},
                           ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    doc["metadata"]["netlistHash"] = "sha256:" + hashlib.sha256(
        canonical.encode("utf-8")).hexdigest()

    text = json.dumps(doc, ensure_ascii=False, indent=2)
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"written: {out_path}（{len(doc['nets'])} 网络 / "
              f"{len(doc['components'])} 器件）")
    else:
        print(text)


def main():
    ap = argparse.ArgumentParser(description="Cadence .dat 三件套解析器")
    ap.add_argument("path", help="三件套所在目录 或 pstxnet.dat 路径")
    sub = ap.add_subparsers(dest="cmd")
    p_nets = sub.add_parser("nets")
    p_nets.add_argument("--pattern")
    p_comp = sub.add_parser("comp")
    p_comp.add_argument("refdes")
    p_xnet = sub.add_parser("xnet")
    p_xnet.add_argument("--net", required=True)
    p_search = sub.add_parser("search")
    p_search.add_argument("--by", choices=["refdes", "mpn", "value", "nets"],
                          default="mpn")
    p_search.add_argument("--pattern", required=True)
    sub.add_parser("erc")
    sub.add_parser("overview")
    p_exp = sub.add_parser("export-json", help="导出 Universal Netlist JSON v2")
    p_exp.add_argument("--out", help="写入文件；不给则打印到 stdout")

    args = ap.parse_args()
    model = build_model(args.path)
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
        cmd_erc_basic(model)
    elif cmd == "export-json":
        cmd_export_json(model, getattr(args, "out", None))


if __name__ == "__main__":
    main()
