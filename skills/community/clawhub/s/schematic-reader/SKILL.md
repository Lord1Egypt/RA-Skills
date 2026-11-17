---
name: schematic-reader
display_name: 原理图识别器
display_name_en: Schematic Reader
description: 原理图识别：把 Altium .PrjPCB、Cadence .DSN、KiCad .kicad_pro、立创 EDA .eprj3、OrCAD .dat、EAGLE .sch、netlist.json 解析成引脚级网表，查器件/网络/连通性、跑 ERC 枚举。触发词：原理图识别、网表提取、信号追踪、schematic parsing、netlist。只出确定性解析事实，不做审查判断。
description_zh: 把 Altium、Cadence、KiCad、立创EDA、OrCAD、Eagle、netlist.json 原理图解析成引脚级网表，支持器件、网络、连通性查询及 ERC 枚举；扫描版不可靠。
description_en: Parse schematics and netlists (Altium, Cadence, KiCad, EasyEDA, OrCAD, EAGLE, netlist.json) into pin-level netlists — query components, nets and connectivity, run ERC enumeration. Facts only; judgment left to the model.
version: "1.0.3"
author: fangcun
license: MIT
compatibility: 依赖 universal-netlist（四通道自动选：native 二进制 / PATH / managed npx / PATH npx，Node 20+ 仅 npx 通道需要；不装则用自研纯 Python 解析器覆盖 .dat 三件套 / Eagle XML / .netlist.json / 立创 eprj3-eprj2-esch2-epcb2）。PDF 文本层走纯 Python（缺 pymupdf 自动 pip --user 安装）。需要 Python 3.10+。扫描版/图片不支持。
---

# Schematic Reader

> Tested baselines: Altium PCA10056 (344 components / 236 nets, SHA-256 stable across reruns), KiCad CM5 carrier (U1 pin-level correct), Cadence MULTIO (with component notes), LCEDA official samples; vector PDF 12 pages -> 381 refdes; all 11 MCP tools tested individually.
> ERC triage calibration: CM5 carrier 126 single_pin -> 63 unconnected + 63 module-side + 0 manual; PCA10056's 2 are DNS decoupling pins. When bucket-3 is empty, report "no substantive issues".

Turns the user's schematic files into structured data by tier, for the LLM to reason over. Core discipline: **facts only, no conclusions; deterministic first — when uncertain, downgrade and say so, never guess**.

## Step 1: Identify the Tier (do this first)

| Tier | Input | Capability | Confidence |
|---|---|---|---|
| **L1 full** | .PrjPCB / .DSN / .kicad_pro (or root .kicad_sch) | Pin-level netlist: components, nets, connectivity, ERC | Certain (parser reads, not infers) |
| **L1-J universal** | .netlist.json (universal-netlist export or any tool's) | Same queries as L1, pure Python locally (no MCP/Node) | Certain (schema hard check; hash soft check) |
| **L1-D OrCAD netlist** | .dat trio (pstxnet/pstxprt/pstchip, same dir) | Pin-level netlist + PART_VALUE + pin function names, pure Python | Certain (text parse; no variant/DNS — that lives in .DSN) |
| **L1-E Eagle** | .sch (EAGLE 6+ XML) | Pin-level netlist (explicit signal/pinref connectivity), pure Python | Certain (XML parse; 5-and-below binary rejected with guidance) |
| **L2 preview** | Vector PDF from EDA (has text layer) | refdes list, net labels, page structure, page locator | Partial (no connectivity; must declare) |
| **L3 reject** | Scanned PDF / image / text-less PDF / EAGLE 5-and-below binary / LTspice .asc | No guessing | Tagged "unreliable"; ask for L1/L2 files |

Decision method:
- Extension decides: L1 formats go straight to step 2; `.netlist.json` runs netlist_json.py; **a directory input triggers auto-discovery** of projects inside (or run `python un_mcp.py designs <dir>`).
- **KiCad .net alone will not work** (tested: upstream requires the project entry) — give .kicad_pro; the parser auto-uses the adjacent .net.
- PDF: probe the text layer with `python scripts/pdf_probe.py <file.pdf>` — refdes/net-label structure means L2; pure images mean L3.
- L3 fixed response: "This file cannot be identified at pin level (scanned/image). Export from your EDA: Altium -> Smart PDF or project package; KiCad -> File > Export > Schematic PDF or provide .kicad_pro."

## Step 2: L1 Full Parse (universal-netlist, three auto-selected channels)

**Launch channels (script picks automatically)**: native binary (`%LOCALAPPDATA%\universal-netlist\bin\universal-netlist-windows-x64.exe`, no Node needed) -> managed npx -> PATH npx. Install native via the upstream PowerShell one-liner. If the host has the universal-netlist connector enabled, MCP tools work equally.

**stdio client commands:**

```bash
python scripts/un_mcp.py tools                              # 11 tools
python scripts/un_mcp.py designs <dir>                      # discover projects
python scripts/un_mcp.py overview <design>                  # stats + MCU candidates + power nets
python scripts/un_mcp.py nets <design>                      # all nets
python scripts/un_mcp.py components <design>                # full component list (auto prefix discovery)
python scripts/un_mcp.py comp <design> U1                   # one component: all pins + MPN + description
python scripts/un_mcp.py xnet <design> --net VDD_nRF        # connectivity chain by net
python scripts/un_mcp.py xnet <design> --pin U1.H23         # connectivity chain from pin
python scripts/un_mcp.py search <design> --nets --pattern "SWD"
python scripts/un_mcp.py search <design> --by mpn --pattern "TPS"
python scripts/un_mcp.py erc <design>                       # raw ERC
python scripts/un_mcp.py erc <design> --triage              # ERC + single_pin triage (recommended)
python scripts/un_mcp.py variants <design>                  # list variants
python scripts/un_mcp.py vdns <design> <variant>            # DNS list for a variant
python scripts/un_mcp.py vdiff <design> <A> <B>             # variant diff
python scripts/un_mcp.py export <design> [out.json]         # export-json -> local netlist_json.py (ms-level)
python scripts/un_mcp.py call <tool> --design <d> --args '{"json":...}'
```

**Design preflight built in**: missing path / lone .SchDoc (hints sibling .PrjPcb) / bad extension -> precise guidance, never a raw stack trace.

**list_components prefix self-discovery**: type is required with no wildcard — the script triggers one `type:"*"` error, parses `Available prefixes: [...]`, then iterates the real prefix set (PCA10056: 16 prefixes incl. FID/BAT; KiCad CM5: H/M/MODULE/USB). **Never hardcode a static prefix table.**

**Cadence .dat trio (OrCAD third-party netlist) — custom parser (MCP does not support it):**

```bash
python scripts/cadence_dat_parse.py <dir-or-pstxnet.dat>          # overview
python scripts/cadence_dat_parse.py <path> nets [--pattern VBUS]
python scripts/cadence_dat_parse.py <path> comp U5
python scripts/cadence_dat_parse.py <path> xnet --net VBUS
python scripts/cadence_dat_parse.py <path> erc
```

- Connectivity comes from pstxnet.dat (FILE_TYPE=EXPANDEDNETLIST); **pin-level complete, L1 confidence**.
- Tested on the official BeagleBone Black netlist: 312 nets / 1710 nodes / 385 components; AM3358 pin function names (AIN0-7/MDC/DDR_A13) directly readable.
- **Boundary**: the trio lacks CIS variant/DNS assembly info (that lives in .DSN) — variant questions require the .DSN.

**Eagle (EAGLE 6+ XML) — custom parser:**

```bash
python scripts/eagle_parse.py <board.sch> overview|nets|comp|xnet|search|erc
```

- EAGLE 6.0 (2011)+ .sch is UTF-8 XML with explicit `nets/net/segment/pinref` connectivity — **L1 confidence** (tested SparkFun Pi_Wedge v12: 28 components / 20 nets, SDA -> JP3.11/JP8.SDA pin-level correct).
- The .sch extension is shared by many tools (KiCad legacy / OrCAD / LTspice / TINA) — the parser checks the file header and rejects non-Eagle XML with precise guidance.
- EAGLE 5-and-below binary: rejected; LTspice .asc: out of scope (canvas format, no explicit netlist).

**LCEDA Pro (EasyEDA) — standalone parser:**

```bash
python scripts/lceda_parse.py <project.eprj3>   # folder project
python scripts/lceda_parse.py <page.esch2>      # single sheet
python scripts/lceda_parse.py <board.epcb2>     # PCB: PAD_NET gives pad->net directly
```

- `.eprj3` is an open format (JSON index + JSON-line docs); output is L1.5 (component + Designator + DeviceName + net names + wire topology). Sheet-side pin-level connectivity is derived via PART/PIN/LINE union-find plus NETFLAG naming, verified pin-for-pin against an official Protel netlist; example-only projects (unsaved system-library geometry) degrade to wire level. PCB-side PAD_NET is pin-level regardless.
- `.eprj` (old SQLite format) is not parsed by this package.

**L1-J: .netlist.json local queries (pure Python, no MCP/Node/npx):**

```bash
python scripts/netlist_json.py overview <file>
python scripts/netlist_json.py nets <file> [--pattern I2C]
python scripts/netlist_json.py components <file> [--type R]
python scripts/netlist_json.py comp <file> U1               # NC pins listed = unused pins
python scripts/netlist_json.py xnet <file> --net VDD        # pierces 0-ohm/L/FB/FL conservatively
python scripts/netlist_json.py erc <file>                   # single_pin/NC/unnamed facts
python scripts/netlist_json.py nc <file> [refdes]           # NC enumeration
```

Deviations from MCP (declare when using): xnet piercing is conservative (0-ohm values and L/FB/FL prefixes only — recheck critical conclusions via MCP); netlistHash is soft-checked (upstream canonicalization not reproduced); schema is hard-checked (missing `universalNetlistSchemaVersion`/nets/components -> reject).

**MCP tool surface (11 tools, all tested):** list_designs; list_components/list_nets; search_nets; search_components_by_refdes|mpn|description; query_component; query_xnet_by_net_name; query_xnet_by_pin_name (params are `net_name` / `pin_name`, format `REFDES.PIN`); run_erc.

**Batch-query standard play**: each MCP call re-parses the whole project (~5.4s tested). Run one `export` to .netlist.json, then query locally via netlist_json.py (millisecond level) — same source, same numbers (PCA10056: 344/236 verified on both sides).

**Multi-variant export boundary (tested)**: export-json CLI output carries **no DNS/variant markers** — DNS conclusions must go through MCP (`vdns` / `comp --variant`); export is for connectivity/component bulk queries only.

**xnet output aggregates by MPN**: identical components merge into one entry with `refdes` as an array — **never conclude "missing components" from the first refdes**; iterate the whole array.

Output contract: component/net counts + file source + "results come from a deterministic parser; pin-level data is trustworthy".

## Step 3: L2 PDF Preview

```bash
python scripts/pdf_probe.py board.pdf            # text layer? refdes/net hits? pages?
python scripts/pdf_probe.py board.pdf --dump out.md
```

Always state: "**PDF extraction contains text labels only, no connectivity; provide the native project for pin-level connections**". Per-page refdes statistics answer "what is this board, which page is power".

## Role: Hands and Eyes for the LLM

**This skill only "identifies" — it turns design files into queryable structured data. It does not "judge"**:

- No review verdicts ("this design is good/bad") — judgment is the LLM's job with the data this skill feeds it.
- No built-in rule libraries / checklists / scoring / Go-No-Go outputs.
- Only: parse (netlists), query (components/nets/connectivity), enumerate (ERC/variant/DNS raw facts).

**Review scenario playbook (6 scenarios tested)** — core lesson: **pin back-tracing beats net-name guessing**. Power-domain decoupling: `xnet --net VDD_xxx` then per-component values. Antenna/clock matching: xnet topology plus values. I2C/SPI pull-ups: do NOT guess net names — `comp <MCU>` to find SCL/SDA pins, take nets, then xnet. USB/connector protection: pin back-trace (D+/D-) for ESD parts and testpoints. Crystal: xnet on XL1/XL2 nets including solder-bridge state. NC/unused pins: full pin list plus erc triage plus **external datasheet pin-count comparison**.

**Two known gaps and mitigations (tested)**: (1) NC review — schematic symbols often omit NC pins (PCA10056 U1: 0 of 74 pins named NC); mitigate by datasheet pin total minus netlist pins = unused set. (2) Net-name discovery — semantic searches fail (search "I2C" finds nothing; actual names are SCL/SDA); always back-trace from pins, or enumerate all nets.

**ERC triage** (`erc --triage`) does data de-noising only — three buckets by pure topology facts: (1) parser-marked unconnected, (2) module/connector-side single pins, (3) everything else, left for the LLM. Calibration priors: CM5 126 single_pin -> bucket-3 empty; PCA10056's 2 were DNS decoupling. The LLM decides what bucket-3 means.

**Variant/BOM comparison** (multi-variant designs):

```bash
python scripts/un_mcp.py variants <design>
python scripts/un_mcp.py vdns <design> <variant> [--type R]
python scripts/un_mcp.py vdiff <design> <A> <B>
```

Tested: LAUNCHXL-CC1310 Standard variant -> vdns reports 13 DNS. **Boundary**: CIS variant-only unmounted components may lack the `dns` flag in list_components groupings, but `query_component` returns `dns:true, manufacturer:"DO NOT MOUNT"` — **vdns counts can undercount actual DNI**; always re-verify key components via query_component.

ERC finding translations (machine facts): `net.single_pin` = net has one pin; `net.unnamed` = auto-generated name; `skipped.dns` = N components not stuffed in this variant.

## Supported / Not Supported

| Supported | Not supported |
|---|---|
| Altium .PrjPCB + .SchDoc (multipage/harness/ports/buses) | .PcbDoc / .kicad_pcb / Gerber / ODB++ (layout — separate concern) |
| Cadence OrCAD .DSN (CIS variant / Do-Not-Stuff) | LTspice .asc / TINA / Qucs |
| Cadence .dat trio (custom parser, BeagleBone-tested) | EAGLE 5-and-below binary .sch (reject; resave as XML) |
| KiCad .kicad_pro / .kicad_sch (adjacent .net path works without kicad-cli) | Scanned PDF / images / hand-drawn (hard reject, no OCR guessing) |
| Eagle 6+ .sch XML (custom parser, Pi_Wedge-tested) | LCEDA schematic-side pin level for example-only projects (wire level available) |
| LCEDA Pro .eprj3 / .esch2 / .epcb2 / .eprj2 (custom parsers; PCB pad-to-net pin-level tested) | netlistHash strong validation (upstream JS canonicalization not reproduced; soft only) |
| .netlist.json universal netlist (L1-J local, export round-trip tested) | Encrypted .DSN without a user-supplied password |
| Vector PDF text-layer preview (L2) | EMC/SI/thermal analysis |
| ERC electrical checks | BOM cost/supply analysis |

## Known Boundaries (honest list)

- KiCad tested (cm5-minima): adjacent .net parses without kicad-cli; U1=LIS3DH pin-level correct; 126 single_pins fully triaged (63 NC + 63 module-side, 0 manual).
- Cadence .DSN tested (MULTIO): parse/ERC fine; list_components requires `{"type":"U"}`.
- The .dat trio lacks CIS variant/DNS info — variant questions require the .DSN; with only .dat, DNS evidence is Value-tagging only.
- Encrypted OrCAD .DSN: set `UNIVERSAL_NETLIST_DSN_PASSWORD_FILE` or `UNIVERSAL_NETLIST_DSN_PASSWORD`; passwords are only read from the environment (upstream promise).
- DesignError guard: design-level errors exit 2 with the parser message and a remedy list — **never "0 components"**; 0 components plus a clean exit means the script is too old, update it.
- KiCad net names carry page-path prefixes (`/CM5/BT_nDis`) — query_xnet needs the full name; run search_nets first.
- LCEDA sheet connectivity: saved-project geometry is embedded in esch2 (PART/PIN blocks) and fully supported; example-only projects degrade to wire level.
- .netlist.json: schema v1/v2 both readable; xnet piercing is conservative — recheck critical conclusions via MCP; plain JSON without the schema marker is rejected.
- Lone .SchDoc/.kicad_sch: preflight rejects (root .kicad_sch exception); the script hints sibling projects.
- This skill is an **identification base (hands and eyes)**: outputs facts only; review conclusions belong to the LLM.

## Troubleshooting (selected)

| Symptom | Remedy |
|---|---|
| Net not found | `nets` to list all, or `search --nets`; KiCad names need the full page prefix |
| Component not found | `components` or `search --by refdes` |
| .net alone fails preflight | Expected: provide .kicad_pro instead |
| MCP unavailable | Three auto channels (native/npx); or export then netlist_json.py; or CLI fallback |
| "No universal-netlist launcher" | Install the native binary or Node 20+ |
| list_components "No components with prefix '*'" | Normal — that is prefix discovery; use `components` |
| export fails | File corrupt or incomplete project (lone .SchDoc) |
| xnet -32602 | Param names are `net_name`/`pin_name` (`REFDES.PIN`) |
| Cadence "Default refused" | Variant declared: pick one via list_designs plus design_variant |
| .dat "Unsupported format" | MCP does not take .dat — use cadence_dat_parse.py |
| .sch "not EAGLE 6+ XML" | Check the header: binary=EAGLE 5-and-below, kicad_sch=KiCad legacy (convert), LTspice/TINA=unsupported |
| LLM asks for a verdict | This skill provides data, not judgment |
| PDF probe 0 hits | Likely scanned -> L3 script |
| JSON args parse fail on Windows | Do not start patterns with a caret (cmd eats it); use file-based args |
| Python cannot find files | Use Windows-style paths; Git Bash /d/... paths fail in Windows Python |
