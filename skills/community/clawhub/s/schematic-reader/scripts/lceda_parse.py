#!/usr/bin/env python3
"""立创EDA (EasyEDA Pro) 工程/文档解析器 —— schematic-reader 的 L1 扩展。

覆盖格式：
- .eprj  (.eprj2)  专业版单文件 SQLite 工程 —— 本解析器不支持；需自备 easyeda-pro-analyzer MCP（MIT，源码不随包发布）
- .eprj3           专业版文件夹工程（官方开放格式）—— 本脚本直接解析
- .esch2           原理图页文档（JSON-line）
- .epcb2           PCB 文档（JSON-line）

eprj3 结构（实测自官方样例 easyeda/easyeda-eprj3-format）：
  <工程>.eprj3        JSON 工程索引：profile.boards/schematics/sheets
  sch/<SCH>/<页>.esch2 每行一个文档：{head}||{body}|{extra...}|
    COMPONENT  body.partId=符号引用, x/y/rotation/isMirror; attrs 含 DeviceName
    ATTR       key=Designator/Device/Symbol/NET/Global Net Name, parentId 挂载体
    WIRE       容器（body 只有 zIndex），其后的 LINE 段是折线坐标
    LINE       startX/Y endX/Y（归最近的 WIRE）
    PIN        符号内嵌引脚（partId=PART id, x/y/rotation/length）
    PAD_NET(id=[type,partId,pad,pinId]) body.padNet=网名 —— PCB 侧 pad→net 直接映射

引脚级连通性限制：原理图侧引脚坐标在符号库（系统库），工程内未内联完整符号时，
  本脚本输出 L1.5 级（网名+导线拓扑+器件清单+PCB pad→net），并明确标注该限制。
  PCB 侧 PAD_NET 是直接的 pad→net 表，不依赖符号库。

输出：JSON（给 Agent 消费）。设计目标：只读、确定性、不猜。
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict

# Windows GBK 控制台保护：中文输出强制 UTF-8
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def parse_esch2(path):
    """esich2/epcb2 通用解析：每行 {head}||{body}|{extra}|...，返回 [(head, [bodies...])]"""
    docs = []
    try:
        f = open(path, encoding="utf-8")
    except OSError as e:
        print(f"ERROR: 打不开 {path}: {e}", file=sys.stderr)
        sys.exit(2)
    with f:
        try:
            for line in f:
                line = line.rstrip("\n")
                if "||" not in line:
                    continue
                head_str, rest = line.split("||", 1)
                try:
                    head = json.loads(head_str)
                except json.JSONDecodeError:
                    continue
                bodies = []
                for seg in rest.rstrip("|").split("|"):
                    seg = seg.strip()
                    if not seg:
                        continue
                    try:
                        bodies.append(json.loads(seg))
                    except json.JSONDecodeError:
                        pass
                docs.append((head, bodies))
        except UnicodeDecodeError as e:
            print(f"ERROR: {path} 不是 UTF-8 文本（{e}）——.esch2/.epcb2 应是 UTF-8 JSON-line，"
                  f"确认没拿错文件（如二进制备份/压缩残留）", file=sys.stderr)
            sys.exit(2)
    return docs


def first_body(bodies):
    return bodies[0] if bodies else {}


def parse_sch_page(path):
    """解析一页原理图 → components / wires(带网名与折线) / netlabels / pin-level nets

    引脚级连通性推导（2026-10-21 立创 CLI 实测验证，与官方 Protel 网表逐脚一致）：
      PART 块 = 内嵌符号定义（CLI 创建/保存过的工程符号几何完整内嵌）
      PIN 块  = 符号引脚（partId 归属符号，x/y 为符号局部坐标，ATTR 挂 Pin Number）
      LINE 块 = 导线段（lineGroup 关联 WIRE 组，startX/Y-endX/Y 为画布绝对坐标）
      引脚绝对坐标 = COMPONENT(x,y) + rotation 旋转 PIN(x,y)
      连通判定：LINE 端点 == 引脚绝对坐标 → 同 WIRE 组的引脚同网
      网名：NETFLAG 器件（partId 固定前缀 pid 的特殊 COMPONENT）Name ATTR；
            未命名的网用 WIRE 组 id 代名（立创文件里不存自动网名 $1N2）"""
    comps = {}   # id -> dict
    wires = {}   # wire_id -> {"net": str, "segs": [(x1,y1,x2,y2)...]}
    wire_net = {}
    labels = []  # (net, x, y)
    parts = {}   # part_id -> {"pins": {pin_head_id: {"num","x","y","rot"}}}（内嵌符号）
    pin_objs = {}  # (part_id, pin_head_id) -> body；PIN 短 id 在 PART 内命名空间会重复，
                   # 必须与 partId 联合做 key（2026-10-21 实测：R1/R2 符号都有 e3/e7）
    pin_num = {}   # (part_id, pin_head_id) -> pin number（顺序配对：PIN 块紧跟其 Pin Number ATTR）
    pending_pin = None

    docs = parse_esch2(path)
    current_wire = None
    for head, bodies in docs:
        t = head.get("type")
        b = first_body(bodies)
        cid = head.get("id")
        if t == "COMPONENT":
            if cid is None:
                continue
            comps[cid] = {
                "x": b.get("x"), "y": b.get("y"),
                "rotation": b.get("rotation"), "mirror": b.get("isMirror"),
                "device_name": None, "designator": "", "device_uuid": None,
                "symbol_uuid": None, "part_id": b.get("partId"),
            }
            attrs = b.get("attrs") or {}
            dn = attrs.get("DeviceName")
            if isinstance(dn, str) and dn.strip():
                try:
                    dnj = json.loads(dn)
                    comps[cid]["device_name"] = dnj.get("name")
                except json.JSONDecodeError:
                    comps[cid]["device_name"] = dn
        elif t == "PART":
            parts[cid] = {"pins": {}}
        elif t == "PIN":
            # PIN 属于最近 PART（文件顺序保证）；其 Pin Number ATTR **紧跟本块**——
            # 顺序配对是唯一可靠方式（PIN 短 id 跨 PART 重复，dict 按短 id 存会串号）
            pin_objs[(b.get("partId"), cid)] = b
            pending_pin = (b.get("partId"), cid)
        elif t == "WIRE":
            current_wire = cid
            if current_wire is not None:
                wires[current_wire] = {"net": "", "segs": []}
        elif t == "LINE" and current_wire and "startX" in b:
            wires[current_wire]["segs"].append(
                (b.get("startX"), b.get("startY"), b.get("endX"), b.get("endY")))
        elif t == "ATTR":
            pid, key, val = b.get("parentId"), b.get("key"), b.get("value")
            if pid in comps:
                if key == "Designator":
                    comps[pid]["designator"] = val or ""
                elif key == "Device":
                    comps[pid]["device_uuid"] = val
                elif key == "Symbol":
                    comps[pid]["symbol_uuid"] = val
                elif key == "Name" and str(comps[pid].get("part_id", "")).startswith("pid"):
                    # NETFLAG 器件：Name ATTR 就是网名（VCC/GND/...）
                    comps[pid]["netflag_net"] = val or ""
            elif pid in wires:
                if key == "NET":
                    wire_net[pid] = val or ""
            elif key == "Pin Number" and pending_pin is not None:
                # 文件顺序：PIN 块后紧跟其 Pin Number ATTR——顺序配对（实测 schema）
                pin_num[pending_pin] = val
                pending_pin = None
            if key in ("Net Label", "Global Net Name", "NetFlag") and b.get("x") is not None:
                labels.append({"net": val, "x": b.get("x"), "y": b.get("y")})
    for wid, net in wire_net.items():
        if wid in wires:
            wires[wid]["net"] = net

    # ---- 引脚级连通性推导 ----
    # 1. 符号引脚登记：pin 短 id（e3/e7）在 PART 内命名空间唯一、跨 PART 会重复——
    #    用 (part_id, pin_id) 联合做 key；Pin Number 已按"PIN 块紧跟其 ATTR"顺序配对
    for (part_id, pin_hid), body in pin_objs.items():
        if part_id and part_id in parts:
            parts[part_id]["pins"][(part_id, pin_hid)] = {
                "num": pin_num.get((part_id, pin_hid)),
                "x": body.get("x"), "y": body.get("y"),
                "rot": body.get("rotation", 0),
            }
    # 2. 实例化：COMPONENT 位置 + rotation 旋转符号引脚局部坐标
    def _rot(px, py, r):
        r = int(r or 0) % 360
        if r == 90:
            return -py, px
        if r == 180:
            return -px, -py
        if r == 270:
            return py, -px
        return px, py

    pin_at = {}   # (absx, absy) -> (comp_id, pin_number)
    for cid, c in comps.items():
        part_id = c.get("part_id")
        if part_id not in parts:
            continue
        cx, cy = c.get("x") or 0, c.get("y") or 0
        for pin in parts[part_id]["pins"].values():
            if pin["num"] is None:
                continue
            ax, ay = _rot(pin["x"], pin["y"], c.get("rotation"))
            key = (round(cx + ax, 3), round(cy + ay, 3))
            pin_at.setdefault(key, (cid, pin["num"]))

    # 3. 电气分网（union-find）：WIRE 组是**绘制合并**（编辑器把相连导线并成组），
    #    组 ≠ 电网络——必须按 LINE 端点重合做并查集（2026-10-21 R3 误判实测修正）
    parent = {}

    def _find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def _union(a, b):
        ra, rb = _find(a), _find(b)
        if ra != rb:
            parent[ra] = rb

    for wid, w in wires.items():
        for i, (x1, y1, x2, y2) in enumerate(w["segs"]):
            n1 = (wid, "seg", i)
            parent.setdefault(n1, n1)
            ea, eb = (round(x1, 3), round(y1, 3)), (round(x2, 3), round(y2, 3))
            for e in (ea, eb):
                parent.setdefault(("pt", e), ("pt", e))
                _union(n1, ("pt", e))
    # 跨组：相同坐标端点合并——("pt", coord) 单键天然同 key 合并，无需额外处理
    # 引脚命中：LINE 端点 == 引脚绝对坐标 → 引脚加入该线段节点
    pin_node = {}   # (comp_id, pin_num) -> node
    for wid, w in wires.items():
        for i, (x1, y1, x2, y2) in enumerate(w["segs"]):
            for pt in ((x1, y1), (x2, y2)):
                k = (round(pt[0], 3), round(pt[1], 3))
                hit = pin_at.get(k)
                if hit:
                    node = (wid, "seg", i)
                    pin_node[hit] = node
                    _union(node, ("pt", k))
    # NETFLAG 命中：其坐标在本组 LINE 端点 → 该节点带网名
    netflag_at = {}  # (x, y) -> net
    for cid, c in comps.items():
        nf = c.get("netflag_net")
        if nf:
            netflag_at[(round(c.get("x") or 0, 3), round(c.get("y") or 0, 3))] = nf
    node_net = {}
    for node in list(parent):
        if node[0] == "seg":
            for (x1, y1, x2, y2) in (wires[node[0]]["segs"][node[1]],):
                for pt in ((x1, y1), (x2, y2)):
                    k = (round(pt[0], 3), round(pt[1], 3))
                    if k in netflag_at:
                        node_net[node] = netflag_at[k]

    # 4. 网名输出：先在**整个连通分量**里找任一 NETFLAG 名（一个分量统一一个名）；
    #    无名的分量按最小节点 id 代名（确定性，对应立创自动名 $1N2）
    root_name = {}
    for node in list(parent):
        # seg 节点结构 (wire_id, "seg", i)——wire_id 才是 node[0]；
        # NETFLAG 判断不看 node[0] 字面量，按节点是否为线段（len==3 且 node[1]=='seg'）
        if len(node) == 3 and node[1] == "seg":
            x1, y1, x2, y2 = wires[node[0]]["segs"][node[2]]
            for pt in ((x1, y1), (x2, y2)):
                k = (round(pt[0], 3), round(pt[1], 3))
                if k in netflag_at:
                    root = _find(node)
                    # 一个分量挂多个 NETFLAG 名时取第一个（同网名必然相同）
                    root_name.setdefault(root, netflag_at[k])
    pin_nets = {}   # (designator, pin) -> net name
    for (cid, num), node in pin_node.items():
        root = _find(node)
        desig = comps[cid].get("designator") or cid
        name = root_name.get(root) or "$" + str(sorted(
            n for n in parent if _find(n) == root)[0])
        pin_nets[(desig, str(num))] = name
    return {"components": comps, "wires": wires, "net_labels": labels,
            "pin_nets": pin_nets}


def parse_pcb_doc(path):
    """解析 PCB 文档 → pad→net 表 + 元件放置"""
    pads = []     # {part_id, pad, pin_ele, net}
    comps = {}    # component id -> {designator,...}
    nets = set()
    current_part = None

    docs = parse_esch2(path)
    for head, bodies in docs:
        t = head.get("type")
        b = first_body(bodies)
        cid = head.get("id")   # 2026-10-24 修复：原先漏定义，遇 COMPONENT 块直接 NameError 崩溃，
                               # 导致 .epcb2（PCB pad→net）这条能力从来没跑通过
        if t == "PAD_NET":
            pid = None
            try:
                pid = json.loads(head["id"])[1]  # ["PAD_NET", partId, pad, pinEleId]
            except (json.JSONDecodeError, KeyError, IndexError):
                pid = None
            pads.append({"part": pid, "pad": json.loads(head["id"])[2] if pid else None,
                         "net": b.get("padNet")})
            if b.get("padNet"):
                nets.add(b["padNet"])
        elif t == "COMPONENT":
            if cid is not None:
                comps[cid] = {"attrs": b.get("attrs") or {}, "designator": ""}
        elif t == "ATTR":
            pid, key, val = b.get("parentId"), b.get("key"), b.get("value")
            if pid in comps and key == "Designator":
                comps[pid]["designator"] = val or ""
    return {"pads": pads, "components": comps, "nets": sorted(nets)}


def parse_eprj2_sqlite(path):
    """立创EDA Pro v4.x 主格式 .eprj2（SQLite 单文件，2026-10-21 逆向实锤）：
    documents 表 docType=1 原理图 / docType=3 PCB，dataStr 为 JSON-line 块序列
    （与 esch2/epcb2 的 head||body 同族，但格式是 [TYPE, ...args] 数组流）。
    原理图：COMPONENT(+ATTR Designator/Device) + WIRE + ATTR(NET)——导线级网络；
    PCB：PAD_NET(pad_obj, pin, net) + COMPONENT + ATTR Designator —— pad→net 引脚级。
    器件属性（厂商/立创编号/MPN）在 attributes 表按 device_uuid 查。"""
    try:
        import sqlite3
        conn = sqlite3.connect(path)
    except sqlite3.Error as e:
        return {"error": f"SQLite 打不开: {e}"}

    out = {"schematic": None, "pcb": None}
    docs = dict(conn.execute("SELECT docType, dataStr FROM documents").fetchall())

    # ---- 原理图（docType=1）----
    sch = docs.get(1)
    if sch:
        comps, wires = {}, {}
        # WIRE id -> 段落坐标
        for m in re.finditer(r'\["WIRE","([^"]+)",(\[\[[^\]]*\](?:,\[[^\]]*\])*\])', sch):
            wires[m.group(1)] = {"net": "", "segs": m.group(2)}
        wire_net = {}
        # ATTR(id, parentId, key, value, ..., x, y)
        for m in re.finditer(r'\["ATTR","([^"]+)","([^"]*)","([^"]+)","([^"]*)"', sch):
            aid, pid, key, val = m.group(1), m.group(2), m.group(3), m.group(4)
            if key == "NET" and pid in wires:
                wire_net[pid] = val
            elif key == "Designator" and not re.match(r"^e\d+$", val or "", re.I):
                # parentId 是 COMPONENT；Designator 值不应是对象 id
                c = comps.setdefault(pid, {"id": pid})
                c["designator"] = val
            elif key == "Device":
                c = comps.setdefault(pid, {"id": pid})
                c["device_uuid"] = val
            elif key == "Symbol":
                c = comps.setdefault(pid, {"id": pid})
                c["symbol_uuid"] = val
        for wid, net in wire_net.items():
            if wid in wires:
                wires[wid]["net"] = net
        # 器件属性表（按 device_uuid 查 MPN/厂商/立创编号）
        attr_rows = {}
        try:
            for du, k, v in conn.execute("SELECT device_uuid, key, value FROM attributes"):
                attr_rows.setdefault(du, {})[k] = v
        except sqlite3.Error:
            pass
        comp_list = []
        for cid, c in comps.items():
            if not c.get("designator"):
                continue
            dev = attr_rows.get(c.get("device_uuid") or "", {})
            comp_list.append({
                "designator": c["designator"],
                "device_uuid": c.get("device_uuid"),
                "mpn": dev.get("Manufacturer Part"),
                "manufacturer": dev.get("Manufacturer"),
                "lcsc_part": dev.get("Supplier Part"),
                "name": dev.get("LCSC Part Name"),
            })
        comp_list.sort(key=lambda x: x["designator"])
        out["schematic"] = {
            "component_count": len(comp_list),
            "components": comp_list,
            "wire_count": len(wires),
            "named_wires": sum(1 for w in wires.values() if w["net"]),
            "net_names": sorted({w["net"] for w in wires.values() if w["net"]}),
        }

    # ---- PCB（docType=3）----
    pcb = docs.get(3)
    if pcb:
        comp_desig = {}
        for m in re.finditer(r'\["COMPONENT","([^"]+)"', pcb):
            cid = m.group(1)
            seg = pcb[m.start():m.start() + 2500]
            dm = re.search(r'"Designator","([^"]+)"', seg)
            if dm:
                comp_desig[cid] = dm.group(1)
        pads = []
        nets = set()
        for m in re.finditer(r'\["PAD_NET","([^"]+)","([^"]+)","([^"]*)"', pcb):
            obj, pin, net = m.group(1), m.group(2), m.group(3)
            pads.append({"designator": comp_desig.get(obj, obj),
                         "pad": pin, "net": net})
            if net:
                nets.add(net)
        out["pcb"] = {
            "pad_net_count": len(pads),
            "pads": pads,
            "net_count": len(nets),
            "nets": sorted(nets),
        }
    conn.close()
    return out


def analyze_project(project_path):
    """入口：.eprj3（文件夹索引）或直接给 .esch2/.epcb2"""
    project_path = os.path.abspath(project_path)
    result = {"file": project_path, "format": None, "schematics": [], "pcb": None,
              "limits": []}

    base = None
    if project_path.endswith(".eprj3"):
        # eprj3 文件本身是 JSON 索引，工程文件夹与它同名（或它就是 <dir>/<name>.eprj3）
        result["format"] = "eprj3"
        try:
            with open(project_path, encoding="utf-8") as f:
                idx = json.load(f)
        except json.JSONDecodeError as e:
            result["limits"].append(f"索引解析失败: {e}")
            return result
        except (OSError, UnicodeDecodeError) as e:
            result["limits"].append(f"索引文件读不了: {e}")
            return result
        proj_dir = os.path.dirname(project_path)
        # 官方样例结构：<dir>/<name>/<sch>/<SCH>/P1.esch2；索引文件在 <dir>/<name>/<name>.eprj3
        inner = os.path.join(proj_dir, idx.get("name", ""))
        if not os.path.isdir(inner):
            inner = proj_dir
        base = inner
        sheets = []
        for sch_uuid, sch in (idx.get("profile", {}).get("schematics") or {}).items():
            sch_dir = os.path.join(base, "sch", sch.get("name", ""))
            if os.path.isdir(sch_dir):
                for f in sorted(os.listdir(sch_dir)):
                    if f.endswith(".esch2"):
                        sheets.append({"schematic": sch.get("name"), "page": f[:-6],
                                       "path": os.path.join(sch_dir, f)})
        for sh in sheets:
            page = parse_sch_page(sh["path"])
            real = {cid: c for cid, c in page["components"].items() if c["designator"]}
            result["schematics"].append({
                "schematic": sh["schematic"], "page": sh["page"],
                "component_count": len(real),
                "components": [c for c in real.values()],
                "wire_count": len(page["wires"]),
                "named_wires": sum(1 for w in page["wires"].values() if w["net"]),
                "net_labels": page["net_labels"],
                # pin_nets 键是 (designator, pin) 元组——JSON 化转 "DESIGNATOR.PIN"
                "pin_nets": {f"{d}.{p}": n for (d, p), n in
                             (page.get("pin_nets") or {}).items()},
            })
    elif project_path.endswith(".esch2"):
        result["format"] = "esch2"
        page = parse_sch_page(project_path)
        real = {cid: c for cid, c in page["components"].items() if c["designator"]}
        result["schematics"].append({
            "page": os.path.basename(project_path)[:-6],
            "component_count": len(real),
            "components": [c for c in real.values()],
            "wire_count": len(page["wires"]),
            "named_wires": sum(1 for w in page["wires"].values() if w["net"]),
            "net_labels": page["net_labels"],
            "pin_nets": {f"{d}.{p}": n for (d, p), n in
                         (page.get("pin_nets") or {}).items()},
        })
    elif project_path.endswith(".epcb2"):
        result["format"] = "epcb2"
        result["pcb"] = parse_pcb_doc(project_path)
    elif project_path.endswith((".eprj", ".eprj2")):
        result["format"] = "eprj2-sqlite"
        parsed = parse_eprj2_sqlite(project_path)
        if "error" in parsed:
            result["limits"].append(parsed["error"])
        else:
            if parsed.get("schematic"):
                result["schematics"].append(parsed["schematic"])
            if parsed.get("pcb"):
                result["pcb"] = parsed["pcb"]
            result["limits"].append(
                "eprj2 原理图侧为导线级网络（WIRE+NET 标签），引脚级需符号库几何"
                "（v4 客户端符号几何在云端系统库，本地 eprj2 不内嵌）；"
                "PCB 侧 PAD_NET 已是 pad→net 引脚级。")
    else:
        result["limits"].append(f"不认识的格式: {os.path.splitext(project_path)[1]}")

    if result["schematics"] or result["pcb"]:
        result["limits"].append(
            "引脚级连通性：原理图侧符号定义在系统库（本机未装立创EDA时不可得），"
            "输出为 L1.5 级（器件+网名+导线拓扑）；PCB 侧 PAD_NET 可直接给 pad→net。")
    return result


def main():
    ap = argparse.ArgumentParser(description="立创EDA Pro 工程/文档解析（eprj3/esch2/epcb2）")
    ap.add_argument("path", help=".eprj3 / .esch2 / .epcb2 路径")
    ap.add_argument("--out", help="写 JSON 到文件")
    args = ap.parse_args()
    if not os.path.exists(args.path):
        print(f"ERROR: 文件不存在 {args.path}", file=sys.stderr)
        sys.exit(2)
    result = analyze_project(args.path)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(text)
        print(f"written: {args.out}")
    else:
        print(text)
    # 退出码：0=解析出内容，1=有限制/空
    ok = bool(result["schematics"] or (result["pcb"] and result["pcb"]["pads"]))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
