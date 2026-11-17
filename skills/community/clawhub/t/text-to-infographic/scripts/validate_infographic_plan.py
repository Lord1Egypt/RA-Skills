#!/usr/bin/env python3
"""validate_infographic_plan.py — 信息图 plan 校验器（布局语义 + 结构 + 文本预算）。

实现《校验规则规格 v0.1》A 层（布局语义）为主，结构检查与 C 层文本预算内置；
B 层（数值 vs 原文）在提供 --source 时启用。

v1.4.0（A 方向）：
- 每条 finding 带**稳定规则码**（如 FLY-002），码表见 RULES，可用 --rules 列出；
- --json 输出机器回执：code / level / layer / subject / message / evidence / why / fix；
- 新增 --fail-on-warn：WARN 也判失败（CI、批处理、内容上线前把关）。

判级：ERROR（阻塞渲染）/ WARN（建议修）/ INFO（提示）。
退出码：0 = 通过；1 = 有 ERROR（或 --fail-on-warn 下有 WARN）；2 = 用法错误。

用法:
    python3 validate_infographic_plan.py plan.json [--source source.txt] [--json] [--explain]
    python3 validate_infographic_plan.py plan.json --json --fail-on-warn
    python3 validate_infographic_plan.py --rules
"""
import json
import re
import sys

ERROR, WARN, INFO = "ERROR", "WARN", "INFO"
SPEC = "infographic-plan-check/v1"
LAYOUTS = {"flywheel", "fishbone", "sankey", "pyramid", "timeline", "dashboard",
           "comparison", "quadrant", "flow", "venn"}
HEX_COLOR_RE = re.compile(r'^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')
TEMPORAL_WORDS = ("先", "然后", "接着", "随后", "之后", "再", "最终", "导致", "因此", "从而")
TIME_PAT = re.compile(r"(\d{4}|\d{1,2}月|\d{1,2}日|Q[1-4]|第\s*[一二三四五六七八九十\d]+\s*[步周月阶段天年]|周[一二三四五六日末]|早期|中期|后期|现在|未来)")
# v1.3.0：与渲染器 TOKEN_KEYS 对齐——四个颜色 token 全部只放行十六进制
TOKEN_KEYS = ("accent", "ink", "paper", "muted")

# ---------------------------------------------------------------- 规则码表
# code: (layer, default_level, 中文规则名)
# 码是稳定契约：修文案不改码，码变了就是规则语义变了。
RULES = {
    # 结构层
    "PLAN-001": ("struct", ERROR, "plan 版本必须为 1.0"),
    "PLAN-002": ("struct", ERROR, "layout 必须是十种 chart_family 之一"),
    "PLAN-003": ("struct", ERROR, "blocks 少于 2 个"),
    "PLAN-004": ("struct", ERROR, "block id 重复"),
    "PLAN-005": ("struct", ERROR, "relation 引用了不存在的 block"),
    "PLAN-006": ("struct", ERROR, "block 缺 title"),
    "SAFE-001": ("safe", ERROR, "颜色 token 不是十六进制（注入风险）"),
    "TEXT-001": ("text", WARN, "标题超过 24 字（C 层文本预算）"),
    "TEXT-002": ("text", WARN, "正文超过 120 字（C 层文本预算）"),
    # 布局语义层（A 层）
    "TIME-001": ("layout", ERROR, "timeline 节点缺可解析时标"),
    "PYR-001": ("layout", WARN, "pyramid 层级少于 3（退化为列表）"),
    "FLY-001": ("layout", ERROR, "flywheel 缺 relations"),
    "FLY-002": ("layout", ERROR, "flywheel 未构成覆盖全部 block 的闭环"),
    "FISH-001": ("layout", WARN, "fishbone 未显式标注 head"),
    "FISH-002": ("layout", ERROR, "fishbone head 多于一个"),
    "SANK-001": ("layout", ERROR, "sankey relations 全部缺 weight"),
    "SANK-002": ("layout", ERROR, "sankey 存在缺 weight 的 relation"),
    "SANK-003": ("layout", ERROR, "sankey 节点流量不守恒"),
    "DASH-001": ("layout", WARN, "dashboard 卡缺 metric"),
    "DASH-002": ("layout", ERROR, "dashboard 卡缺 value"),
    "DASH-003": ("layout", ERROR, "dashboard 卡缺 unit"),
    "DASH-004": ("layout", WARN, "dashboard 卡缺时间范围"),
    "CMP-001": ("layout", ERROR, "comparison 块缺 group"),
    "CMP-002": ("layout", ERROR, "comparison 只有一个 group（缺对照）"),
    "QDR-001": ("layout", ERROR, "quadrant 需恰好 4 个 block"),
    "FLOW-001": ("layout", WARN, "flow 缺 relations（按 blocks 顺序推断）"),
    "VENN-001": ("layout", ERROR, "venn 需 2-4 个集合圆"),
    "SEM-001": ("layout", WARN, "疑似并列内容被表达为时间线"),
    # 数值溯源层（B 层，需 --source）
    "SRC-001": ("source", ERROR, "source_ref 在原文中找不到"),
    "NUM-001": ("source", WARN, "数值未能在原文定位"),
}

LAYER_NAMES = {
    "struct": "结构", "safe": "安全", "text": "文本预算",
    "layout": "布局语义", "source": "数值溯源",
}


class Findings:
    """findings 容器。append 保持旧签名兼容（level, msg, why, fix），新增可选 code/subject/evidence。"""

    def __init__(self):
        self.items = []

    def append(self, level, msg, why="", fix="", code=None, subject=None, evidence=None):
        layer = RULES.get(code, ("other", level, ""))[0] if code else "other"
        self.items.append({
            "code": code or "GEN-000",
            "level": level,
            "layer": layer,
            "subject": subject,
            "message": msg,
            "evidence": evidence or {},
            "why": why,
            "fix": fix,
        })

    def count(self, level):
        return sum(1 for x in self.items if x["level"] == level)

    @property
    def has_error(self):
        return self.count(ERROR) > 0

    @property
    def has_warn(self):
        return self.count(WARN) > 0

    def by_layer(self):
        out = {}
        for x in self.items:
            out[x["layer"]] = out.get(x["layer"], 0) + 1
        return out


def check(plan, findings):
    layout = plan.get("layout")
    blocks = plan.get("blocks", [])
    ids = [b.get("id") for b in blocks]
    rels = plan.get("relations", [])

    # ---- 结构基线
    if plan.get("version") != "1.0":
        findings.append(ERROR, "version 必须为 1.0",
                        why="plan 格式版本固定为 1.0，其他值说明这不是本工具认识的 plan。",
                        fix="把 version 字段改回 \"1.0\"。",
                        code="PLAN-001", subject="version",
                        evidence={"expected": "1.0", "actual": plan.get("version")})
    if layout not in LAYOUTS:
        findings.append(ERROR, f"layout 必须是 {sorted(LAYOUTS)} 之一",
                        why="渲染器只为这六种布局实现了专用几何/排版，未知布局无法渲染。",
                        fix=f"从 {sorted(LAYOUTS)} 中选一个，或先用 build_plan_from_text.py --analyze 让工具推荐布局。",
                        code="PLAN-002", subject="layout",
                        evidence={"allowed": sorted(LAYOUTS), "actual": layout})
    # ---- 安全：颜色 token 只放行十六进制（与渲染器边界一致，防止 CSS/SVG 注入）
    vs = plan.get("visual_system") or {}
    for field in TOKEN_KEYS:
        if vs.get(field) is not None:
            if not isinstance(vs[field], str) or not HEX_COLOR_RE.match(vs[field]):
                findings.append(ERROR, f"visual_system.{field} 必须是十六进制颜色（#RGB 或 #RRGGBB），收到: {vs[field]!r}",
                                why="颜色值会被直接插进 CSS/SVG，非十六进制值可能注入脚本或外链，这是安全边界。",
                                fix=f"把 {field} 改成形如 #C96F4A 或 #F0A 的十六进制颜色，或者删掉该字段用 palette 预设的默认值。",
                                code="SAFE-001", subject=f"visual_system.{field}",
                                evidence={"actual": vs[field], "pattern": "^#(RGB|RRGGBB)$"})
    if len(blocks) < 2:
        findings.append(ERROR, "blocks 至少 2 个",
                        why="少于 2 个信息块的「信息图」退化为一张标题页，没有信息结构可言。",
                        fix="把原文再拆一拆：至少抽出 2 个并列/递进/因果的要点作为 block。",
                        code="PLAN-003", subject="blocks",
                        evidence={"count": len(blocks), "min": 2})
    if len(ids) != len(set(ids)):
        dups = sorted({i for i in ids if ids.count(i) > 1}, key=str)
        findings.append(ERROR, "block id 存在重复",
                        why="id 是块的唯一标识，relations、修改定位都依赖它；重复会让「改一个块只重渲染一块」失效。",
                        fix="给重复的 id 换成唯一的 snake_case 名字，例如 step_1 / step_2。",
                        code="PLAN-004", subject="blocks[].id",
                        evidence={"duplicated": dups})
    for r in rels:
        if r.get("from") not in ids or r.get("to") not in ids:
            findings.append(ERROR, f"relation 引用了不存在的 block: {r}",
                            why="指向不存在块的连线会渲染成悬空引用。",
                            fix="修正 from/to 的 block id，或删掉这条 relation。",
                            code="PLAN-005", subject=f"relations[{r.get('from')}->{r.get('to')}]",
                            evidence={"from": r.get("from"), "to": r.get("to"),
                                      "known_ids": ids})

    for b in blocks:
        if not b.get("title"):
            findings.append(ERROR, f"block {b.get('id')} 缺 title",
                            why="title 是每个信息块的必选锚点，渲染器用它做节点标签。",
                            fix=f"给 block {b.get('id')} 补一个 ≤24 字的标题。",
                            code="PLAN-006", subject=b.get("id"))
        if len(b.get("title", "")) > 24:
            findings.append(WARN, f"block {b.get('id')} 标题超过 24 字（C 层文本预算）",
                            why="标题超长会在 SVG 节点里溢出或被截断，破坏排版。",
                            fix="压缩成一个短谓语短语（如「线索统一进 hub」），细节挪进 text。",
                            code="TEXT-001", subject=b.get("id"),
                            evidence={"length": len(b.get("title", "")), "limit": 24})
        if len(b.get("text", "")) > 120:
            findings.append(WARN, f"block {b.get('id')} 正文超过 120 字（C 层文本预算）",
                            why="信息图不是文章：正文超过 120 字说明这块塞了原文没消化的内容。",
                            fix="提炼成一句话；原始长句可放进 meta.source_note 留档。",
                            code="TEXT-002", subject=b.get("id"),
                            evidence={"length": len(b.get("text", "")), "limit": 120})

    # ---- A3 timeline 缺时标
    if layout == "timeline":
        for b in blocks:
            if not b.get("time") or not TIME_PAT.search(b.get("time", "")):
                findings.append(ERROR, f"timeline 节点 {b.get('id')} 缺可解析时间标记",
                                why="时间线的轴就是时间：没有可解析时标的节点会让轴失去意义，读者无法排序。",
                                fix=f"给 {b.get('id')} 的 time 字段写具体时间，如 2025Q3 / 3月 / 第 1 周。",
                                code="TIME-001", subject=b.get("id"),
                                evidence={"time": b.get("time")})

    # ---- A4 pyramid 层级过少
    if layout == "pyramid" and len(blocks) < 3:
        findings.append(WARN, f"pyramid 仅 {len(blocks)} 层（<3 将退化为列表）",
                        why="金字塔少于 3 层时三角形收缩不可见，视觉上就是普通列表，白占了形状语义。",
                        fix="补到 3 层以上；如果内容本来就只有两层，换 dashboard 或 timeline。",
                        code="PYR-001", subject="blocks",
                        evidence={"layers": len(blocks), "min": 3})

    # ---- A5 flywheel 未闭环
    if layout == "flywheel":
        if not rels:
            findings.append(ERROR, "flywheel 缺 relations（飞轮必须闭环）",
                            why="飞轮的定义就是「最后一步回到第一步」：没有闭环 relations，它只是个饼图。",
                            fix="为每个相邻环节补 from→to 关系，并让最后一个环节指回第一个。",
                            code="FLY-001", subject="relations",
                            evidence={"blocks": ids, "relations": 0})
        else:
            edges = {(r["from"], r["to"]) for r in rels}
            start = ids[0]
            cur, seen, closed = start, {start}, False
            path = [start]
            for _ in range(len(ids)):
                nxt = next((t for f, t in edges if f == cur), None)
                if nxt is None:
                    break
                if nxt == start:
                    closed = len(seen) == len(ids)
                    break
                if nxt in seen:
                    break
                seen.add(nxt)
                path.append(nxt)
                cur = nxt
            if not closed:
                findings.append(ERROR, "flywheel relations 未构成覆盖全部 block 的闭环",
                                why="存在环节没被接进环里，或链条中途断裂——飞轮叙事不成立。",
                                fix="检查每个环节是否恰好一个后继，且最后一个环节 from→to 指回 blocks[0]。",
                                code="FLY-002", subject="relations",
                                evidence={"walked_path": path,
                                          "covered": len(seen),
                                          "total_blocks": len(ids),
                                          "missing": [i for i in ids if i not in seen]})

    # ---- A6 fishbone 多头
    if layout == "fishbone":
        heads = [b for b in blocks if b.get("role") == "head"]
        if len(heads) == 0:
            findings.append(WARN, "fishbone 无 role=head 的块（默认取第一个 block 为 head，建议显式标注）",
                            why="鱼骨图恰好一个「鱼头」（被分析的结果）。没显式标注时工具只能猜第一个块。",
                            fix=f"把表示结果/问题的那个块加 \"role\": \"head\"（当前默认用 blocks[0]={ids[0]!r}）。",
                            code="FISH-001", subject="blocks[].role",
                            evidence={"assumed_head": ids[0] if ids else None})
        elif len(heads) > 1:
            findings.append(ERROR, f"fishbone 有 {len(heads)} 个 head（必须恰好 1 个）",
                            why="多个鱼头意味着其实是多张鱼骨图被塞进了一张，读者不知道看哪个结论。",
                            fix="只保留一个 head，其余拆成独立的 fishbone plan 或改为并列布局。",
                            code="FISH-002", subject="blocks[].role",
                            evidence={"heads": [b.get("id") for b in heads]})

    # ---- A7 sankey 不守恒
    if layout == "sankey":
        weighted = [r for r in rels if r.get("weight") is not None]
        if not weighted:
            findings.append(ERROR, "sankey 的 relations 全部缺 weight",
                            why="桑基图的带宽就是数值：没有 weight 无法画出流量，也没有守恒可言。",
                            fix="给每条 relation 补 weight（同一量纲，如人数/金额）。",
                            code="SANK-001", subject="relations[].weight",
                            evidence={"relations": len(rels)})
        else:
            if len(weighted) < len(rels):
                missing = [f"{r.get('from')}->{r.get('to')}" for r in rels
                           if r.get("weight") is None]
                findings.append(ERROR, "sankey 存在缺 weight 的 relation",
                                why="部分边没有宽度，渲染出来的流量是断裂的。",
                                fix="补齐所有 relation 的 weight。",
                                code="SANK-002", subject="relations[].weight",
                                evidence={"missing_weight": missing})
            for bid in ids:
                inflow = sum(r["weight"] for r in weighted if r["to"] == bid)
                outflow = sum(r["weight"] for r in weighted if r["from"] == bid)
                if inflow and outflow and abs(inflow - outflow) / max(inflow, outflow) > 0.01:
                    findings.append(ERROR, f"sankey 节点 {bid} 流量不守恒：入 {inflow} ≠ 出 {outflow}",
                                    why="中间节点流入≠流出，说明数字抄错或漏了一条边——这是信息正确性错误，不是排版问题。",
                                    fix="核对原文数字：要么修正 weight，要么补上缺失的流向（如损耗/其他）。",
                                    code="SANK-003", subject=bid,
                                    evidence={"inflow": inflow, "outflow": outflow,
                                              "delta": round(outflow - inflow, 6)})

    # ---- A8 dashboard 缺元数据
    if layout == "dashboard":
        for b in blocks:
            if not b.get("metric"):
                findings.append(WARN, f"dashboard 卡 {b.get('id')} 缺 metric",
                                why="没有指标名的数字无法解读（10 是什么？）。",
                                fix=f"给 {b.get('id')} 补 metric（指标名，如「周活跃」）。",
                                code="DASH-001", subject=b.get("id"))
            if not b.get("value"):
                findings.append(ERROR, f"dashboard 卡 {b.get('id')} 缺 value",
                                why="仪表盘卡片的核心是大数字，缺 value 这张卡没有内容。",
                                fix=f"给 {b.get('id')} 补 value。",
                                code="DASH-002", subject=b.get("id"))
            if not b.get("unit"):
                findings.append(ERROR, f"dashboard 卡 {b.get('id')} 缺 unit（无单位的数字等于没说）",
                                why="「500」可能是 500 人也可能是 500 万——缺单位是典型的数字误导。",
                                fix=f"给 {b.get('id')} 补 unit（人 / 万元 / % …）。",
                                code="DASH-003", subject=b.get("id"))
            if not b.get("time"):
                findings.append(WARN, f"dashboard 卡 {b.get('id')} 缺时间范围",
                                why="没有时间范围的指标无法对比也无法复现。",
                                fix=f"给 {b.get('id')} 补 time（如 2026-10 / 本周）。",
                                code="DASH-004", subject=b.get("id"))

    # ---- A9 comparison 缺对照语义
    if layout == "comparison":
        for b in blocks:
            if not b.get("group"):
                findings.append(ERROR, f"comparison 块 {b.get('id')} 缺 group",
                                why="对比双栏靠 group 区分左右侧：没有 group 就无法归列，读者看不出谁和谁比。",
                                fix=f"给 {b.get('id')} 加 \"group\"（如 \"免费堆量\"/\"按量付费\"），同侧块用同一 group 名。",
                                code="CMP-001", subject=b.get("id"))
        if len({b.get("group") for b in blocks if b.get("group")}) < 2:
            findings.append(ERROR, "comparison 只有一个 group（缺对照）",
                            why="对比至少要两侧；只有一个 group 等于单列表格，不构成「对比」。",
                            fix="至少给两个 block 分配不同的 group，形成左/右或更多列。",
                            code="CMP-002", subject="blocks[].group",
                            evidence={"groups": sorted({b.get("group") for b in blocks if b.get("group")})})

    # ---- A10 quadrant 需 4 块
    if layout == "quadrant" and len(blocks) != 4:
        findings.append(ERROR, f"quadrant 需恰好 4 个 block（2×2 四象限），当前 {len(blocks)} 个",
                        why="2×2 矩阵由两根轴切出四个象限，块数不是 4 就无法一一对应。",
                        fix="补/删到 4 个 block，分别对应左上/右上/左下/右下。",
                        code="QDR-001", subject="blocks",
                        evidence={"count": len(blocks), "expected": 4})

    # ---- A11 flow 需有序
    if layout == "flow" and not rels:
        findings.append(WARN, "flow 缺 relations（步骤顺序将按 blocks 顺序推断）",
                        why="流程的箭头靠 relations 表达；缺了它只能默认按 blocks 顺序串，容易漏掉分支/回环。",
                        fix="为相邻步骤补 from→to 关系，明确箭头方向。",
                        code="FLOW-001", subject="relations")

    # ---- A12 venn 需 2-4 个集合
    if layout == "venn" and not (2 <= len(blocks) <= 4):
        findings.append(ERROR, f"venn 需 2-4 个集合（circle），当前 {len(blocks)} 个",
                        why="韦恩图靠圆与圆的交叠表达重合；少于 2 没有交叠，多于 4 圆不可读。",
                        fix="把集合数调整到 2-4 之间。",
                        code="VENN-001", subject="blocks",
                        evidence={"count": len(blocks), "range": "2-4"})

    # ---- A1 并列误作流程（timeline 轻量启发）
    if layout == "timeline" and len(blocks) >= 3:
        flat = all(not any(w in (b.get("text") or "") or w in (b.get("title") or "")
                           for w in TEMPORAL_WORDS) for b in blocks)
        same_shape = len({len(b.get("text") or "") // 20 for b in blocks}) == 1
        if flat and same_shape:
            findings.append(WARN, "疑似并列内容被表达为时间线（A1）：全文无时序连接词且各条目同构",
                            why="并列事项排成时间线会暗示「先后/因果」，读者会读出不存在的顺序——AntV 官方也承认渲染器无法替作者判断这类语义。",
                            fix="确认这些条目真有先后顺序；若只是并列，换 dashboard 或 pyramid，并给每条加真实时标。",
                            code="SEM-001", subject="layout",
                            evidence={"blocks": len(blocks),
                                      "temporal_words_hit": 0,
                                      "same_shape": True})


def check_source(plan, source_text, findings):
    """B 层：数值可溯源 + 引用完整性。"""
    for b in plan.get("blocks", []):
        ref = b.get("source_ref")
        if ref and ref not in source_text:
            findings.append(ERROR, f"block {b.get('id')} source_ref 在原文中找不到（B5）",
                            why="source_ref 是「这个说法出自原文哪里」的锚点，锚点失效等于断了证据链。",
                            fix="核对原文后修正 source_ref（直接复制原文里连续的一小段），或删掉该引用。",
                            code="SRC-001", subject=b.get("id"),
                            evidence={"source_ref": ref})
        v = b.get("value")
        if v is not None:
            vs = str(v)
            if vs not in source_text and not any(ch.isdigit() and ch in source_text for ch in vs):
                findings.append(WARN, f"block {b.get('id')} 数值 {vs} 未能在原文定位（B1）",
                                why="数字在原文里找不到，可能是 AI 改写时算错/编造的——信息图最怕这种错。",
                                fix="回原文核对数字；若确实经过换算（如汇率/单位换算），在 meta.source_note 里写明换算口径。",
                                code="NUM-001", subject=b.get("id"),
                                evidence={"value": vs})


def print_rules():
    print(f"{'CODE':<10}{'LEVEL':<8}{'LAYER':<8}RULE")
    for code, (layer, level, name) in RULES.items():
        print(f"{code:<10}{level:<8}{LAYER_NAMES.get(layer, layer):<8}{name}")


def main():
    args = sys.argv[1:]
    if "--rules" in args:
        print_rules()
        return
    as_json = "--json" in args
    explain = "--explain" in args
    fail_on_warn = "--fail-on-warn" in args or "--strict" in args
    flags = ("--json", "--explain", "--fail-on-warn", "--strict")
    args = [a for a in args if a not in flags]
    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    plan_path = args[0]
    plan = json.loads(open(plan_path, encoding="utf-8").read())
    source_text = ""
    if "--source" in args:
        i = args.index("--source")
        if i + 1 >= len(args):
            print("--source 需要一个文件路径", file=sys.stderr)
            sys.exit(2)
        source_text = open(args[i + 1], encoding="utf-8").read()

    f = Findings()
    check(plan, f)
    if source_text:
        check_source(plan, source_text, f)

    # 判据：默认只看 ERROR；--fail-on-warn 时 WARN 也算失败
    failed = f.has_error or (fail_on_warn and f.has_warn)
    exit_code = 1 if failed else 0

    if as_json:
        payload = {
            "spec": SPEC,
            "ok": not failed,
            "decision": "fail" if failed else "pass",
            "exitCode": exit_code,
            "failOnWarn": fail_on_warn,
            "plan": plan_path,
            "layout": plan.get("layout"),
            "summary": {
                "error": f.count(ERROR),
                "warn": f.count(WARN),
                "info": f.count(INFO),
                "byLayer": f.by_layer(),
            },
            "findings": f.items,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if not f.items:
            print("✅ 通过：未发现问题")
        for x in f.items:
            icon = {"ERROR": "❌", "WARN": "⚠️ ", "INFO": "ℹ️ "}[x["level"]]
            subj = f" ({x['subject']})" if x.get("subject") else ""
            print(f"{icon} [{x['level']}] {x['code']}{subj} {x['message']}")
            if explain and (x.get("why") or x.get("fix")):
                if x.get("why"):
                    print(f"     为什么：{x['why']}")
                if x.get("fix"):
                    print(f"     怎么改：{x['fix']}")
        n_err, n_warn = f.count(ERROR), f.count(WARN)
        tail = f"—— {n_err} ERROR / {n_warn} WARN"
        if fail_on_warn and n_warn and not n_err:
            tail += "（--fail-on-warn：WARN 判失败）"
        print(tail)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
