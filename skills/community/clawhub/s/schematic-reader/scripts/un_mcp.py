#!/usr/bin/env python3
"""universal-netlist MCP stdio 客户端：不依赖 MCP client，直接 stdio 调用工具。

用途：
1. 给 skill 当后端：在 WorkBuddy 的 universal-netlist 连接器未启用时，
   skill 可以用本脚本走 stdio 直接查（list_nets / query_component / run_erc ...）
2. 给 skill 开发自测：逐一验证 MCP 工具面

三条通道（按可用性自动选）：
  C native binary : %LOCALAPPDATA%\\universal-netlist\\bin\\universal-netlist-windows-x64.exe（无 Node 依赖，最快）
  B managed npx   : %LOCALAPPDATA%\\workbuddy\\binaries\\node\\versions\\*\\npx.cmd（按版本目录自动发现）
  A PATH npx      : shutil.which("npx")

用法：
  python un_mcp.py tools                          # 列工具
  python un_mcp.py designs [目录]                 # 发现工程
  python un_mcp.py overview <design>              # 工程速览
  python un_mcp.py nets <design>                  # 列网络
  python un_mcp.py components <design> [--type R] # 器件清单（type 可省略，省略=全量）
  python un_mcp.py comp <design> U1               # 单器件全引脚+MPN
  python un_mcp.py xnet <design> --net VDD        # 按网名追连通链
  python un_mcp.py xnet <design> --pin U1.H23     # 从引脚追连通链
  python un_mcp.py search <design> --nets --pattern "^SWD"          # 搜网名
  python un_mcp.py search <design> --by mpn --pattern "TPS"         # 搜器件（refdes/mpn/description/value）
  python un_mcp.py erc <design> [--triage]        # ERC（--triage 三分法降噪）
  python un_mcp.py variants <design>              # 列 variant
  python un_mcp.py vdns <design> <variant>        # 该 variant 的 DNS 清单
  python un_mcp.py vdiff <design> <A> <B>         # 两 variant diff
  python un_mcp.py export <design> [out.json]     # export-json 导出 .netlist.json（批量查询前先导一次）
  python un_mcp.py call <tool> --design <d> [--args '{"json":...}']  # 通用入口

前置检查：design 路径存在性 + 扩展名识别，缺文件给精确补件指引（不裸栈）。
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

# Windows GBK 控制台保护：中文输出强制 UTF-8
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# native exe 候选位置：环境变量 > 官方 install.ps1 的 LOCALAPPDATA 默认位置
NATIVE_CANDIDATES = [
    os.environ.get("UNIVERSAL_NETLIST_EXE", ""),
    os.path.join(os.environ.get("LOCALAPPDATA", ""),
                 "universal-netlist", "bin", "universal-netlist.exe"),
]
NATIVE_CANDIDATES = [p for p in NATIVE_CANDIDATES if p]
NATIVE_EXE = next((p for p in NATIVE_CANDIDATES if os.path.exists(p)), "")


def managed_npx_candidates():
    """WorkBuddy 托管 Node 的 npx：按版本目录动态发现，不写死机器路径。"""
    base = os.path.join(os.environ.get("LOCALAPPDATA", ""),
                        "workbuddy", "binaries", "node", "versions")
    out = []
    if os.path.isdir(base):
        for name in sorted(os.listdir(base), reverse=True):
            p = os.path.join(base, name, "npx.cmd")
            if os.path.exists(p):
                out.append(p)
    return out
PKG = "@intelligentelectron/universal-netlist"
PROTO_VER = "2024-11-05"

# design 扩展名识别：给缺件/错件精确指引
DESIGN_KINDS = {
    ".dsn": "cadence",
    ".schdoc": "altium-sheet",     # 单独给不行，要 .PrjPcb
    ".prjpcb": "altium",
    ".kicad_pro": "kicad",
    ".kicad_sch": "kicad-sheet",   # 单独给可能行（root sheet），优先 .kicad_pro
    ".netlist.json": "netlist-json",
    ".eprj3": "lceda",
    ".esch2": "lceda",
    ".epcb2": "lceda",
}


def extract_json_obj(text):
    """从 MCP content text 里稳健抽出第一个完整 JSON 对象（raw_decode 不受嵌套影响）。
    比正则 \\{.*\\} 贪婪匹配可靠：大 JSON/嵌套/前后有杂文都不会截断。"""
    for i, ch in enumerate(text):
        if ch == "{":
            try:
                obj, _ = json.JSONDecoder().raw_decode(text[i:])
                return obj
            except json.JSONDecodeError:
                continue
    return None


# ---------------------------------------------------------------- 通道发现

def find_server():
    """四条通道找 universal-netlist：native exe（显式候选 + PATH）> managed npx > PATH npx。
    返回 (argv_list, channel_name)。"""
    if os.path.exists(NATIVE_EXE):
        return [NATIVE_EXE], "native"
    # 他人机器：官方 install.ps1 装完会把 bin 目录加进用户 PATH
    path_native = shutil.which("universal-netlist")
    if path_native:
        return [path_native], "native"
    for managed in managed_npx_candidates():
        return [managed, "-y", PKG], "managed-npx"
    hit = shutil.which("npx")
    if hit:
        return [hit, "-y", PKG], "path-npx"
    return None, None


def preflight_design(path):
    """design 路径预检：存在性 + 扩展名识别。返回 (ok, hint)。缺件给精确指引。"""
    if not os.path.exists(path):
        return False, (f"路径不存在: {path}\n"
                       f"  确认拼写；目录也可以（designs 子命令先发现工程）")
    if os.path.isdir(path):
        # 目录：directly 给 overview/nets 等会撞 "Unsupported design file format ''"，
        # 主动扫同目录工程，给下一步精确指引
        found = []
        try:
            for f in sorted(os.listdir(path)):
                fl = f.lower()
                if fl.endswith((".prjpcb", ".dsn", ".kicad_pro", ".netlist.json")):
                    found.append(os.path.join(path, f))
        except OSError:
            pass
        hint = "给的是目录——MCP 只吃工程文件。本目录发现的工程："
        hint += "\n  " + "\n  ".join(found) if found else \
            "给的是目录——其中没发现工程文件（.PrjPcb/.DSN/.kicad_pro/.netlist.json）"
        hint += f"\n  或先发现: python un_mcp.py designs \"{path}\""
        return False, hint
    lower = path.lower()
    # 复合扩展名优先于 splitext（.netlist.json 的 splitext 只会给 .json）
    if lower.endswith(".netlist.json"):
        return True, None  # MCP 也直接吃 .netlist.json
    ext = os.path.splitext(lower)[1]
    kind = DESIGN_KINDS.get(ext)
    if ext == ".net" and kind is None:
        # 实测（2026-10-21）：上游不吃裸 .net（文档写 committed netlist，但只认
        # .kicad_pro/.kicad_sch 入口，.net 是工程旁的引用文件）——拒识带正确指引
        sib = [f for f in (os.listdir(os.path.dirname(os.path.abspath(path))) or [])
               if f.lower().endswith(".kicad_pro")]
        if sib:
            return False, (f"给的是 KiCad 导出网表（.net）——它不能单独喂给解析器，"
                           f"要给工程文件。同目录发现 .kicad_pro 工程：\n  {sib}\n"
                           f"  → 改给 .kicad_pro（解析器会自动用旁边的 .net）")
        return False, ("给的是 KiCad 导出网表（.net）——它不能单独喂给解析器，"
                       "要给 .kicad_pro（或根 .kicad_sch）工程文件，"
                       "且 .net 需与工程同目录")
    if kind == "altium-sheet":
        prj = os.path.join(os.path.dirname(os.path.abspath(path)), "..",
                           "")  # 提示去上层找 .PrjPcb
        sib = [f for f in (os.listdir(os.path.dirname(os.path.abspath(path))) or [])
               if f.lower().endswith(".prjpcb")]
        hint = (f"只给了 .SchDoc 单页——universal-netlist 通过 .PrjPcb 发现工程"
                f"（多页经端口/页条目/总线连接）。请给 .PrjPcb：")
        if sib:
            hint += f"\n  同目录发现: {sib} → 试 `python un_mcp.py designs \"{os.path.dirname(os.path.abspath(path))}\"`"
        else:
            hint += "\n  在 EDA 里另存为/打包完整工程（.PrjPcb + 全部 .SchDoc）"
        return False, hint
    if kind == "kicad-sheet":
        sib = [f for f in (os.listdir(os.path.dirname(os.path.abspath(path))) or [])
               if f.lower().endswith(".kicad_pro")]
        hint = "单独 .kicad_sch 可能是 root sheet（可试），但推荐给 .kicad_pro 工程："
        if sib:
            hint += f"\n  同目录发现: {sib}"
        else:
            hint += "\n  或工程旁放一个导出的 .net 文件（kicad-cli 导出，本机无 kicad-cli 时免安装）"
        return True, hint  # 不拦，让 MCP 自己判（root sheet 确实能读）
    if kind == "netlist-json":
        return True, None  # 兼容：splitext 路径一般走不到这里，双保险
    if kind is None:
        return False, (f"不认识的扩展名 {ext or '(无)'}——L1 支持: .DSN / .PrjPcb / "
                       f".kicad_pro / .netlist.json（KiCad 导出 .net 也可直吃）；"
                       f"立创 .eprj3 用 lceda_parse.py；.dat 三件套用 cadence_dat_parse.py；"
                       f"Eagle .sch 用 eagle_parse.py；PDF 先用 pdf_probe.py 探档位")
    return True, None


class McpClient:
    def __init__(self):
        argv, channel = find_server()
        if argv is None:
            print("ERROR: 找不到 universal-netlist 启动方式。任选其一：\n"
                  "  1) 装 native 二进制（推荐，无 Node 依赖）: \n"
                  "     PowerShell 运行  irm https://raw.githubusercontent.com/IntelligentElectron/universal-netlist/main/install.ps1 | iex\n"
                  "  2) 装 Node 20+ 后确保 npx 在 PATH\n"
                  "  3) 或直接用 CLI: npx -y @intelligentelectron/universal-netlist export-json <design>",
                  file=sys.stderr)
            sys.exit(2)
        self.channel = channel
        self.argv = argv
        try:
            # Popen 默认继承 os.environ——加密 OrCAD 密码 env
            # （UNIVERSAL_NETLIST_DSN_PASSWORD[_FILE]）随之透传给解析器。
            # 上游承诺：密码只从环境读取，永不进工具调用/结果/日志。
            self.proc = subprocess.Popen(
                argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding="utf-8",
            )
        except OSError as e:
            print(f"ERROR: 启动 universal-netlist 失败（{channel}）: {e}\n"
                  f"  argv={argv}\n"
                  f"  npx 通道首次运行要拉 npm 包（需网络）；native 通道应免网络。"
                  f" 可换通道: 删掉 %LOCALAPPDATA%\\universal-netlist 强制走 npx，或反之",
                  file=sys.stderr)
            sys.exit(2)
        self._id = 0
        try:
            self._initialize()
        except Exception as e:
            self._fail_init(e)
        print(f"[channel: {channel}]", file=sys.stderr)

    def _fail_init(self, e):
        stderr_tail = ""
        try:
            if self.proc.poll() is not None:
                stderr_tail = (self.proc.stderr.read() or "")[:600]
        except Exception:
            pass
        print(f"ERROR: MCP initialize 失败: {e}\n"
              f"  channel={self.channel} argv={self.argv}\n"
              f"  stderr: {stderr_tail or '(无)'}\n"
              f"  排查: Node 20+？npx 首次拉包要网络；native exe 被杀毒软件拦？",
              file=sys.stderr)
        try:
            self.proc.terminate()
        except Exception:
            pass
        sys.exit(2)

    def _send(self, obj):
        self.proc.stdin.write(json.dumps(obj) + "\n")
        self.proc.stdin.flush()

    def _readline(self):
        line = self.proc.stdout.readline()
        if not line:
            err = ""
            try:
                if self.proc.poll() is not None:
                    err = (self.proc.stderr.read() or "")[:600]
            except Exception:
                pass
            raise RuntimeError(f"MCP 无响应（exit={self.proc.poll()}）{err}")
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            raise RuntimeError(f"MCP 返回非 JSON 行: {line[:200]}")

    def _initialize(self):
        self._send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                    "params": {"protocolVersion": PROTO_VER, "capabilities": {},
                               "clientInfo": {"name": "schematic-reader", "version": "0.4.0"}}})
        resp = self._readline()
        if "error" in resp:
            raise RuntimeError(f"initialize 失败: {resp['error']}")
        self.server_info = resp.get("result", {}).get("serverInfo", {})
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def call(self, tool, arguments):
        self._id += 1
        self._send({"jsonrpc": "2.0", "id": 2 + self._id, "method": "tools/call",
                    "params": {"name": tool, "arguments": arguments}})
        while True:
            resp = self._readline()
            if resp.get("id") == 2 + self._id:
                if "error" in resp:
                    raise RuntimeError(f"{tool} 调用失败: {resp['error']}")
                return resp["result"]

    def list_tools(self):
        self._id += 1
        self._send({"jsonrpc": "2.0", "id": 2 + self._id, "method": "tools/list"})
        while True:
            resp = self._readline()
            if resp.get("id") == 2 + self._id:
                return resp["result"]["tools"]

    def close(self):
        try:
            self.proc.stdin.close()
        except Exception:
            pass
        try:
            self.proc.terminate()
            self.proc.wait(timeout=5)
        except Exception:
            try:
                self.proc.kill()
            except Exception:
                pass


def content_text(result):
    parts = result.get("content", [])
    texts = [p.get("text", "") for p in parts if p.get("type") == "text"]
    return "\n".join(texts)


class DesignError(Exception):
    """MCP 返回 design 级错误（缺工程文件/文件损坏/无网表/加密未给密码等）。
    这类错误必须透出给用户，禁止静默吞掉——吞掉的后果是把
    "No netlist for X" 显示成"器件总数 0"，误导性极强。"""


BENIGN_PREFIX_RE = re.compile(r"No components with prefix '.*?' found in design", re.I)


def is_benign_prefix_error(e):
    """前缀查询空结果是正常形态（该板没有这个前缀的器件），不算 design 级错误。"""
    return bool(BENIGN_PREFIX_RE.search(str(e)))


def call_json(client, tool, arguments):
    """调 MCP 工具并抽 JSON。design 级 error 抛 DesignError（核心防线）。"""
    raw = client.call(tool, arguments)
    text = content_text(raw)
    dd = extract_json_obj(text)
    if dd is None:
        raise DesignError(f"{tool} 返回无法解析的内容:\n{text[:500]}")
    if "error" in dd:
        raise DesignError(str(dd["error"]))
    return dd


def fail_design(e, design):
    """design 级错误的统一出口：原文透出 + 常见原因 + exit 2。
    查询 miss（网名/refdes 不存在）单独给对症指引，不甩无关处置清单。"""
    msg = str(e)
    if "Net " in msg and "not found" in msg:
        print(f"ERROR: 网名不存在: {msg}\n"
              f"  下一步: 用 `nets` 列全部网名，或 `search --nets --pattern <关键词>` 模糊找；\n"
              f"  KiCad 网名带页路径前缀（如 /CM5/BT_nDis），要带全", file=sys.stderr)
        sys.exit(2)
    if "omponent " in msg and "not found" in msg:
        print(f"ERROR: 器件不存在: {msg}\n"
              f"  下一步: 用 `components` 列全部器件，或 `search --by refdes --pattern <前缀>`；\n"
              f"  refdes 大小写不敏感，但前缀要对（U1 不是 U2 的兄弟就别猜）", file=sys.stderr)
        sys.exit(2)
    extra = ""
    if "design variants" in msg and "design_variant" in msg:
        extra = ("\n  ★ 该设计声明了多个 variant（Altium Not-Fitted 分组 / CIS variant）——"
                 "查询命令加 --variant <名字> 即可，如: "
                 "python un_mcp.py overview <design> --variant <名字>；"
                 "名字见报错原文或 `variants <design>`")
    if "Password-protected" in msg or "password" in msg.lower():
        extra = ("\n  ★ 这是加密 OrCAD 设计：设 UNIVERSAL_NETLIST_DSN_PASSWORD_FILE"
                 "=密码文件路径（每行一个密码）或 UNIVERSAL_NETLIST_DSN_PASSWORD=单个密码，"
                 "重跑即解。密码只从环境读取，不进本工具的任何输出。")
    print(f"ERROR: 解析器返回 design 级错误（{design}）:\n  {e}{extra}\n"
          f"  常见原因与处置:\n"
          f"    给的是目录 → 先 `designs <目录>` 发现工程，再给工程文件路径\n"
          f"    KiCad 缺 .net/.kicad_sch → 工程旁放导出的 .net，或给完整 .kicad_pro\n"
          f"    Altium 只给了单页 .SchDoc → 补 .PrjPcb 完整工程\n"
          f"    加密 OrCAD .DSN → 设 UNIVERSAL_NETLIST_DSN_PASSWORD_FILE（见 SKILL.md 加密段）\n"
          f"    文件损坏/不完整 → 重新导出或打包工程", file=sys.stderr)
    sys.exit(2)


def triage_single_pin(erc_result):
    """single_pin 三分法降噪：把 ERC 的 errors.net.single_pin 分成
    1) 无意义（KiCad unconnected- 前缀，ERC 工具自己就标过的未连接脚）
    2) 模块/连接器对侧单脚（Module* / 连接器 refdes 挂的载卡正常形态）
    3) 需人工确认的剩余项
    """
    erc = erc_result.get("errors", {}) if isinstance(erc_result, dict) else {}
    sp = erc.get("net.single_pin", {})
    module_refs = {"MODULE", "J", "CN", "P", "X", "SW"}
    buckets = {"ignored_unconnected": [], "module_side": [], "needs_review": {}}
    for net, pins in sp.items():
        # KiCad 未连接脚的网名/引脚名带 unconnected- 标记，解析器自己就知道无意义
        if any("unconnected" in p.lower() or "unconnected" in net.lower() for p in pins):
            buckets["ignored_unconnected"].append(net)
            continue
        if any(p.split(".")[0].rstrip("0123456789").upper() in module_refs or p.split(".")[0].upper().startswith("MODULE") for p in pins):
            buckets["module_side"].append(net)
            continue
        buckets["needs_review"][net] = pins
    return buckets


# ---------------------------------------------------------------- 子命令

# 静态兜底前缀表（自发现失败时用；含 FID/BAT 等非常见前缀）
ALL_PREFIXES = ["C", "R", "U", "D", "L", "Q", "J", "P", "K", "F", "T", "SW", "MK",
                "Y", "FB", "RV", "TP", "X", "Z", "BT", "SP", "LED", "FL", "CN", "SB",
                "FID", "BAT", "RN", "VR", "OP", "HS", "MP", "PG", "AE", "FD"]


# 词边界关键词（防 Socket 误中 soc / Connector 误中 cpu）
MCU_RE = re.compile(r"(?i)\b(mcu|soc|controller|processor|fpga|transceiver|bluetooth|wifi|cpu|dsp)\b")


def discover_prefixes(client, design, variant=None):
    """自发现 design 的真实 refdes 前缀全集：用不存在的 type '*' 触发报错，
    从 'Available prefixes: [...]' 解析。
    注意：这是唯一"故意触发错误"的地方——若报错不是前缀清单而是 design 级
    错误（无网表/文件坏），必须 re-raise 透出，禁止退静态表装作没事。"""
    arguments = {"type": "*", "design": design}
    if variant:
        arguments["design_variant"] = variant
    try:
        call_json(client, "list_components", arguments)
    except DesignError as e:
        m = re.search(r"Available prefixes\s*:\s*\[([^\]]+)\]", str(e))
        if m:
            return [p.strip().strip("'\"") for p in m.group(1).split(",") if p.strip()]
        raise                        # design 级错误：透出，不吞
    except RuntimeError:
        pass                         # 传输层异常：退静态表（宽松）
    return ALL_PREFIXES


def list_all_components(client, design, variant=None):
    """遍历全部 refdes 前缀收集器件（list_components 的 type 必填，这是全量收集的标准打法）。
    前缀先自发现（报错信息给全集），失败退静态表——保证不漏件。"""
    prefixes = discover_prefixes(client, design, variant=variant)
    all_refs = {}
    for prefix in prefixes:
        arguments = {"type": prefix, "design": design}
        if variant:
            arguments["design_variant"] = variant
        try:
            dd = call_json(client, "list_components", arguments)
        except DesignError as e:
            if is_benign_prefix_error(e):
                continue            # 该前缀无器件：正常，跳过
            raise                   # 设计级错误：透出
        for group in dd.get("components", []):
            for ref in group.get("refdes", []):
                all_refs[ref] = {"value": group.get("value"),
                                 "dns": bool(group.get("dns")),
                                 "mpn": group.get("mpn"),
                                 "description": group.get("description"),
                                 "notes": group.get("notes", [])}
    return all_refs, prefixes


def variant_args(args, base=None):
    """统一拼 variant 参数：args 上有 --variant 且非空才加 design_variant。"""
    d = dict(base or {})
    v = getattr(args, "variant", None)
    if v:
        d["design_variant"] = v
    return d


def cmd_components(client, args):
    if args.type:
        dd = call_json(client, "list_components",
                       variant_args(args, {"type": args.type, "design": args.design}))
        print(json.dumps(dd, ensure_ascii=False, indent=2))
        return
    all_refs, prefixes = list_all_components(client, args.design)
    print(f"器件总数: {len(all_refs)}（全量收集：list_components 的 type 必填，"
          f"已自发现 {len(prefixes)} 个前缀: {' '.join(prefixes)}）")
    by_prefix = {}
    for ref, info in all_refs.items():
        p = ref.upper().rstrip("0123456789")
        by_prefix.setdefault(p, []).append((ref, info))
    for p in sorted(by_prefix, key=lambda k: -len(by_prefix[k])):
        print(f"  {p}×{len(by_prefix[p])}: {' '.join(r for r, _ in sorted(by_prefix[p])[:12])}"
              + (" …" if len(by_prefix[p]) > 12 else ""))


def cmd_search(client, args):
    if not args.pattern:
        print("ERROR: search 需要 --pattern（正则，大小写不敏感）", file=sys.stderr)
        sys.exit(2)
    if args.nets:
        dd = call_json(client, "search_nets",
                       variant_args(args, {"design": args.design, "pattern": args.pattern}))
        print(json.dumps(dd, ensure_ascii=False, indent=2))
        return
    field = args.by or "mpn"
    tool = {"refdes": "search_components_by_refdes",
            "mpn": "search_components_by_mpn",
            "description": "search_components_by_description",
            "value": "search_components_by_description"}[field]
    dd = call_json(client, tool,
                   variant_args(args, {"design": args.design, "pattern": args.pattern}))
    print(json.dumps(dd, ensure_ascii=False, indent=2))
    if field == "value":
        print("提示: value 搜索走 description 工具（MCP 无专用 value 搜索），结果可能含描述命中",
              file=sys.stderr)


def cmd_export(client, args):
    argv, channel = find_server()
    out = args.out or (args.design + ".netlist.json")
    if channel == "native":
        cmd = [argv[0], "export-json", args.design, out]
    else:
        cmd = argv + ["export-json", args.design, out]
    if getattr(args, "variant", None):
        cmd += ["--design-variant", args.variant]
    print(f"导出中（{channel}）: {' '.join(cmd)}", file=sys.stderr)
    if getattr(args, "variant", None):
        print("⚠ 实测（2026-10-21 NanoESP32）：export-json 的 --design-variant 导出的"
              ".netlist.json 不含 variant/DNS 标记（MCP 查询通道有，CLI 导出没有）——"
              "variant 相关结论（谁不贴装）以 MCP 查询通道为准，export 只用于连通性批量查",
              file=sys.stderr)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           timeout=300)
    except subprocess.TimeoutExpired:
        print("ERROR: export-json 超时（300s）——大工程首次解析慢，重试或检查文件完整性",
              file=sys.stderr)
        sys.exit(2)
    if r.returncode != 0:
        msg = (r.stderr or r.stdout or "").strip()[:500]
        extra = ""
        if "Password-protected" in msg or "password" in msg.lower():
            extra = ("\n  加密 OrCAD 设计：设 UNIVERSAL_NETLIST_DSN_PASSWORD_FILE=密码文件路径"
                     "（每行一个密码）后重试；或 UNIVERSAL_NETLIST_DSN_PASSWORD=单个密码")
        print(f"ERROR: export-json 失败（exit {r.returncode}）: {msg}{extra}\n"
              f"  解析器会命名第一个缺陷；通常是文件损坏或非完整工程", file=sys.stderr)
        sys.exit(2)
    print(r.stdout.strip())
    print(f"\n导出成功: {out}")
    print("之后批量查询走本地（毫秒级）: python netlist_json.py <子命令> " + out)


def cmd_overview(client, args):
    # 1) 器件统计（按前缀；前缀自发现，不漏件）
    counts = {}
    for prefix in discover_prefixes(client, args.design, variant=getattr(args, "variant", None)):
        try:
            dd = call_json(client, "list_components",
                           variant_args(args, {"type": prefix, "design": args.design}))
        except DesignError as e:
            if is_benign_prefix_error(e):
                continue            # 该前缀无器件：正常，跳过
            raise                   # 设计级错误（缺 .net/文件坏/加密）：透出
        n = sum(len(g.get("refdes", [])) for g in dd.get("components", []))
        if n:
            counts[prefix] = n
    total = sum(counts.values())
    print(f"器件总数: {total}")
    print("  " + "、".join(f"{k}×{v}" for k, v in sorted(counts.items(), key=lambda x: -x[1])))
    # 2) 主控/核心器件候选（词边界匹配，防 Socket 误中 soc）
    dd = call_json(client, "list_components", variant_args(args, {"type": "U", "design": args.design}))
    print("\n主控/核心候选（U 类，词边界关键词）:")
    hit = 0
    for g in dd.get("components", []):
        desc = g.get("description", "") or ""
        val = g.get("value", "") or ""
        if MCU_RE.search(f"{desc} {val}"):
            for ref in g.get("refdes", []):
                print(f"  {ref}: {val} — {desc[:70]}")
                hit += 1
    if not hit:
        print("  （无命中，用 search --by description 自查）")
    # 3) 电源网络
    dd = call_json(client, "search_nets",
                   variant_args(args, {"design": args.design,
                                       "pattern": r"(?i)^(VDD|VCC|VBUS|VIN|VLDA|VLDB|VBAT|VOUT|V5|V3)"}))
    for nets in (dd.get("results") or {}).values():
        print(f"\n电源网络候选 ({len(nets)}):")
        for n in nets:
            print("  ", n)


def main():
    ap = argparse.ArgumentParser(description="universal-netlist MCP stdio 客户端")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("tools", help="列出 MCP 工具")

    p_call = sub.add_parser("call", help="调用任意工具")
    p_call.add_argument("tool")
    p_call.add_argument("--design")
    p_call.add_argument("--args", help='额外参数 JSON，如 \'{"pattern":"^SWD"}\'')

    p_designs = sub.add_parser("designs", help="发现目录下的工程")
    p_designs.add_argument("design", nargs="?")

    p_nets = sub.add_parser("nets", help="列全部网络")
    p_nets.add_argument("design")
    p_nets.add_argument("--variant", default=None,
                        help="design variant 名（声明了 variant 的设计必传，如 NanoESP32 的 ABX00083）")

    p_comps = sub.add_parser("components", help="器件清单（省略 --type 则全量收集）")
    p_comps.add_argument("design")
    p_comps.add_argument("--type", help="按 refdes 前缀过滤（如 R/C/U），省略=全量")
    p_comps.add_argument("--variant", default=None, help="design variant 名")

    p_erc = sub.add_parser("erc", help="ERC 电气检查（--triage 三分法降噪：single_pin 分桶，①NC ②模块对侧 ③需人工）")
    p_erc.add_argument("design")
    p_erc.add_argument("--triage", action="store_true",
                       help="single_pin 三分法降噪：连接器NC脚/模块对侧单脚归为确认项，只留真正需人工看的")
    p_erc.add_argument("--format", choices=["text", "json"], default="text")
    p_erc.add_argument("--variant", default=None, help="design variant 名")

    sub.add_parser("variants", help="列出设计的全部 variant（供选择/对比）").add_argument("design")

    p_vdiff = sub.add_parser("vdiff", help="两个 variant 的器件清单 diff（DNI 变化）")
    p_vdiff.add_argument("design")
    p_vdiff.add_argument("variant_a")
    p_vdiff.add_argument("variant_b")
    p_vdiff.add_argument("--type", default=None, help="按 refdes 前缀过滤（如 R/C/U），默认全部")

    p_vlist = sub.add_parser("vdns", help="列出一个 variant 下的 DNS（不贴装）器件")
    p_vlist.add_argument("design")
    p_vlist.add_argument("variant")
    p_vlist.add_argument("--type", default=None)

    p_over = sub.add_parser("overview", help="工程速览：器件统计+主控候选+电源网络（认识一块板子的第一步）")
    p_over.add_argument("design")
    p_over.add_argument("--variant", default=None, help="design variant 名")

    p_search = sub.add_parser("search", help="正则搜网名或器件字段（refdes/mpn/description/value）")
    p_search.add_argument("design")
    p_search.add_argument("--nets", action="store_true", help="搜网名（默认搜器件）")
    p_search.add_argument("--by", choices=["refdes", "mpn", "description", "value"],
                          default="mpn", help="器件搜索字段（默认 mpn）")
    p_search.add_argument("--pattern", help="正则（大小写不敏感）")
    p_search.add_argument("--variant", default=None, help="design variant 名")

    p_export = sub.add_parser("export", help="export-json 导出 .netlist.json（批量查询前先导一次，之后本地毫秒级查）")
    p_export.add_argument("design")
    p_export.add_argument("out", nargs="?", help="输出路径（默认 <design>.netlist.json）")
    p_export.add_argument("--variant", default=None,
                          help="design variant 名（注意实测：导出物不含 DNS/variant 标记，variant 结论以 MCP 查询为准）")

    p_comp = sub.add_parser("comp", help="单器件全引脚连接+MPN/描述（引脚反查的主力命令）")
    p_comp.add_argument("design")
    p_comp.add_argument("refdes")
    p_comp.add_argument("--variant", default=None, help="design variant 名")

    p_xnet = sub.add_parser("xnet", help="追连通链：穿透串联 0Ω/磁珠（--net 按网名 / --pin 按引脚 REFDES.PIN）")
    p_xnet.add_argument("design")
    p_xnet.add_argument("--net")
    p_xnet.add_argument("--pin")
    p_xnet.add_argument("--variant", default=None, help="design variant 名")

    args = ap.parse_args()

    # ---- 前置检查：design 路径（designs 子命令允许无参数/目录）----
    design_arg = getattr(args, "design", None)
    if args.cmd != "designs" and design_arg:
        ok, hint = preflight_design(design_arg)
        if not ok:
            print(f"ERROR: design 预检失败\n  {hint}", file=sys.stderr)
            sys.exit(2)
        if hint:
            print(f"提示: {hint}", file=sys.stderr)

    # --args JSON 预解析（错误给 hint，含 Windows ^ 坑）
    extra_args = None
    if args.cmd == "call" and args.args:
        try:
            extra_args = json.loads(args.args)
        except json.JSONDecodeError as e:
            print(f"ERROR: --args 不是合法 JSON: {e}\n"
                  f"  Windows cmd 坑: JSON 不能以 ^ 开头（^ 被当转义符吃掉），"
                  f"如 {{\"pattern\":\"^SWD\"}} 会坏——换不含 ^ 的 pattern、加引号、或改走文件传参",
                  file=sys.stderr)
            sys.exit(2)

    client = McpClient()

    try:
        if args.cmd == "tools":
            for t in client.list_tools():
                print(f"{t['name']}: {t.get('description', '')[:80]}")
        elif args.cmd == "call":
            arguments = {}
            if args.design:
                arguments["design"] = args.design
            if extra_args:
                arguments.update(extra_args)
            print(content_text(client.call(args.tool, arguments)))
        elif args.cmd == "export":
            cmd_export(client, args)
        elif args.cmd == "search":
            cmd_search(client, args)
        elif args.cmd == "overview":
            cmd_overview(client, args)
        elif args.cmd == "designs":
            arguments = {"path": args.design} if args.design else {}
            print(json.dumps(call_json(client, "list_designs", arguments),
                             ensure_ascii=False, indent=2))
        elif args.cmd == "vdiff":
            def collect(variant):
                return list_all_components(client, args.design, variant=variant)[0]
            a, b_ = collect(args.variant_a), collect(args.variant_b)
            only_a = {k: v for k, v in a.items() if k not in b_}
            only_b = {k: v for k, v in b_.items() if k not in a}
            dns_change = {k: (a[k], b_[k]) for k in a if k in b_ and a[k]["dns"] != b_[k]["dns"]}
            print(f"variant diff: {args.variant_a} vs {args.variant_b}")
            print(f"仅 {args.variant_a} 有 ({len(only_a)}):", sorted(only_a) or "-")
            print(f"仅 {args.variant_b} 有 ({len(only_b)}):", sorted(only_b) or "-")
            print(f"DNS 状态变化 ({len(dns_change)}):")
            for k, (va, vb) in sorted(dns_change.items()):
                print(f"  {k}: dns {va['dns']}→{vb['dns']}  value={va['value']}→{vb['value']}")
        elif args.cmd == "vdns":
            all_refs, _ = list_all_components(client, args.design, variant=args.variant)
            dns_list = sorted(r for r, v in all_refs.items() if v["dns"])
            print(f"variant '{args.variant}' 的 DNS 器件 ({len(dns_list)}):")
            for r in dns_list:
                print("  ", r)
        elif args.cmd == "variants":
            data = call_json(client, "list_designs", {"path": args.design if os.path.isdir(args.design) else (os.path.dirname(os.path.abspath(args.design)) or ".")})
            target_name = os.path.basename(args.design.rstrip("/\\"))
            for d in data.get("designs", []):
                dname = d.get("name", "")
                dpath = d.get("path", "")
                if dname == target_name or dpath.endswith(target_name):
                    for v in d.get("design_variants", []):
                        print(v.get("name"), "| fabrication:", v.get("fabrication"))
                    if not d.get("design_variants"):
                        print("<Default>（该设计未声明 CIS variant）")
        elif args.cmd == "erc":
            if args.triage:
                erc = call_json(client, "run_erc", variant_args(args, {"design": args.design}))
                buckets = triage_single_pin(erc)
                if args.format == "json":
                    print(json.dumps({"design": args.design, "triage": buckets},
                                     ensure_ascii=False, indent=2))
                else:
                    print(f"single_pin 三分法（共 {sum(len(v) if isinstance(v, (list, dict)) else 0 for v in buckets.values())}）:")
                    print(f"  ① 无意义(NC/unconnected): {len(buckets['ignored_unconnected'])}")
                    print(f"  ② 模块/连接器对侧单脚(载卡等正常形态): {len(buckets['module_side'])}")
                    print(f"  ③ 需人工确认: {len(buckets['needs_review'])}")
                    for net, pins in buckets["needs_review"].items():
                        print(f"     {net} → {pins}")
            else:
                print(json.dumps(call_json(client, "run_erc", variant_args(args, {"design": args.design})),
                                 ensure_ascii=False, indent=2))
        elif args.cmd == "nets":
            print(json.dumps(call_json(client, "list_nets", variant_args(args, {"design": args.design})),
                             ensure_ascii=False, indent=2))
        elif args.cmd == "components":
            cmd_components(client, args)
        elif args.cmd == "comp":
            print(json.dumps(call_json(client, "query_component",
                                       variant_args(args, {"design": args.design, "refdes": args.refdes})),
                             ensure_ascii=False, indent=2))
        elif args.cmd == "xnet":
            if args.net:
                print(json.dumps(call_json(client, "query_xnet_by_net_name",
                                           variant_args(args, {"design": args.design, "net_name": args.net})),
                                 ensure_ascii=False, indent=2))
            elif args.pin:
                print(json.dumps(call_json(client, "query_xnet_by_pin_name",
                                           variant_args(args, {"design": args.design, "pin_name": args.pin})),
                                 ensure_ascii=False, indent=2))
            else:
                ap.error("需要 --net 或 --pin")
    except DesignError as e:
        fail_design(e, getattr(args, "design", None) or "(未知 design)")
    finally:
        client.close()


if __name__ == "__main__":
    main()
