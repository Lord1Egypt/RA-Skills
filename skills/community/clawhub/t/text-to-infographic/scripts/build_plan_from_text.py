#!/usr/bin/env python3
"""build_plan_from_text.py — 文本 → plan 的自动构建器（text→plan 入口）。

这是「可编辑 plan」叙事的入口：文章/笔记不再一步直出图，而是
  ① --analyze   分析文本，启发式推荐 chart_family 布局（给证据，不武断）；
  ② --from-blocks  把 LLM 抽取出的 blocks 草稿组装成完整 plan
                   （自动填 version / layout / visual_system preset），
                   组装后立即调用校验器做布局语义检查；
  ③ 校验通过后再用 render_infographic_html.py 渲染。

设计原则：
- LLM 负责理解文本、抽取 blocks；脚本负责结构、preset、校验——各干各的；
- preset 只在 plan 层展开成十六进制颜色，渲染器保持「只认 hex」的安全边界不变；
- 零依赖：仅 Python 标准库。

用法:
    python3 build_plan_from_text.py --analyze article.md
    python3 build_plan_from_text.py --analyze - < article.md
    python3 build_plan_from_text.py --from-blocks draft.json -o plan.json \
        [--layout flywheel] [--style editorial] [--accent #C96F4A] \
        [--title 标题] [--subtitle 副标题]
    python3 build_plan_from_text.py --presets
"""
import argparse
import json
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import render_infographic_html as R          # noqa: E402  （PALETTES 单一事实源）
import validate_infographic_plan as V        # noqa: E402  （组装后立即校验）

# ---------------------------------------------------------------- 布局启发式
SIGNALS = {
    "flywheel": {
        "weight": 2.0,
        "words": ["飞轮", "循环", "闭环", "复利", "增长引擎", "反馈", "自增强",
                  "滚雪球", "回到起点", "周而复始", "network effect", "飞轮效应"],
    },
    "fishbone": {
        "weight": 2.0,
        "words": ["根因", "归因", "原因", "因素", "为什么", "问题分析", "鱼骨",
                  "影响因素", "成因", "病因", "排查", "复盘结论"],
    },
    "sankey": {
        "weight": 2.0,
        "words": ["流向", "流量", "分配", "占比", "去向", "花在", "预算", "漏斗",
                  "转化", "拆成", "分成", "来源", "分成三份", "流转"],
    },
    "pyramid": {
        "weight": 2.0,
        "words": ["层级", "底层", "顶层", "优先级", "递进", "金字塔", "分层",
                  "三层", "四层", "框架", "第一性", "由浅入深", "进阶"],
    },
    "timeline": {
        "weight": 1.5,
        "words": ["路线图", "里程碑", "阶段", "步骤", "上线", "发布", "节奏",
                  "计划", "规划", "roadmap", "里程碑事件"],
    },
    "dashboard": {
        "weight": 1.5,
        "words": ["指标", "KPI", "达成率", "环比", "同比", "数据看板", "核心数据",
                  "净值", "转化率", "留存", "%，", "%。"],
    },
    "comparison": {
        "weight": 2.0,
        "words": ["对比", "vs", "VS", "优劣", "区别", "差异", "相比", "对照",
                  "竞品", "优势", "劣势", "取舍", "权衡", "两种", "两侧"],
    },
    "quadrant": {
        "weight": 1.8,
        "words": ["四象限", "矩阵", "优先级矩阵", "重要紧急", "SWOT", "横轴",
                  "纵轴", "两个维度", "2x2", "2×2"],
    },
    "flow": {
        "weight": 1.5,
        "words": ["流程", "步骤", "怎么做", "how-to", "教程", "操作", "流程步骤",
                  "先后", "先…再…", "依次"],
    },
    "venn": {
        "weight": 1.5,
        "words": ["交集", "重合", "交叉", "共同", "重叠", "韦恩", "venn", "既要…又要…"],
    },
}
LAYOUT_HINT = {
    "flywheel": "适合讲「自我增强的循环」：最后一步回到第一步，中心有累积状态。",
    "fishbone": "适合讲「一个结果的多类原因」：一根主骨、若干类因。",
    "sankey": "适合讲「总量怎么分流」：每条边都要有权重，且中间节点守恒。",
    "pyramid": "适合讲「分层递进」：3 层以上，底座最宽最重。",
    "timeline": "适合讲「按时间推进」：每个节点必须有可解析的时标。",
    "dashboard": "适合讲「一组关键数字」：每张卡都要 value+unit，最好带 metric/time。",
    "comparison": "适合讲「A vs B 的优劣/取舍」：按 group 分列，两侧对照。",
    "quadrant": "适合讲「两个维度的四象限定位」：恰好 4 块，轴标签放 meta.x_label/y_label。",
    "flow": "适合讲「分步怎么做」：横向步骤卡 + 箭头，顺序靠 relations。",
    "venn": "适合讲「多个集合的交集/重合」：2-4 个圆，标题在圆上方。",
}


def analyze(text):
    """启发式布局推荐：返回按得分排序的 [(layout, score, evidence)]。"""
    scores = {}
    evidence = {}
    for layout, cfg in SIGNALS.items():
        hits = [w for w in cfg["words"] if w in text]
        scores[layout] = len(hits) * cfg["weight"]
        evidence[layout] = hits
    time_hits = V.TIME_PAT.findall(text)
    scores["timeline"] += min(len(time_hits), 6) * 1.0
    evidence["timeline"] = evidence["timeline"] + [t for t, in time_hits[:6]]
    n_digits = len(re.findall(r"\d+(?:\.\d+)?%?", text))
    scores["dashboard"] += min(n_digits, 12) * 0.8
    evidence["dashboard"] = evidence["dashboard"] + [f"{n_digits} 处数字"]
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    return [(lay, sc, evidence[lay]) for lay, sc in ranked if sc > 0]


def print_analyze(text):
    ranked = analyze(text)
    n_blocks_hint = max(2, min(8, len(re.findall(r"[。；;！!？?\n]", text)) // 2 + 1))
    if not ranked:
        print("⚠️ 未捕获到明显布局信号。建议：内容是并列要点 → dashboard；"
              "有先后顺序 → timeline；先跑 --presets 看风格。")
        return 2
    top, sc, ev = ranked[0]
    print(f"推荐布局：{top}（得分 {sc:.1f}）")
    print(f"  理由：命中信号 {ev or ['（时间/数字密度触发）']}")
    print(f"  该布局的叙事前提：{LAYOUT_HINT[top]}")
    alts = [f"{lay}({s:.1f})" for lay, s, _ in ranked[1:3]]
    if alts:
        print(f"  备选：{' / '.join(alts)}")
    print(f"  建议块数：约 {n_blocks_hint} 个（2-8 为宜）")
    print("下一步：按 schemas/infographic-plan.schema.json 抽取 blocks 草稿 → "
          "build_plan_from_text.py --from-blocks draft.json --layout " + top)
    return 0


def load_presets():
    return {name: p["accent"] for name, p in R.PALETTES.items()}


def from_blocks(draft, args):
    plan = {
        "version": "1.0",
        "meta": dict(draft.get("meta") or {}),
        "layout": args.layout or draft.get("layout"),
        "blocks": draft.get("blocks") or [],
    }
    if draft.get("relations"):
        plan["relations"] = draft["relations"]
    if args.title:
        plan["meta"]["title"] = args.title
    if args.subtitle:
        plan["meta"]["subtitle"] = args.subtitle
    vs = dict(draft.get("visual_system") or {})
    vs.setdefault("palette", args.style or "terracotta")
    if args.accent:
        vs["accent"] = args.accent
    plan["visual_system"] = {k: v for k, v in vs.items() if v}

    if not plan["layout"]:
        print("❌ 未指定布局：draft 里没有 layout 字段，也没给 --layout。\n"
              "   先跑 --analyze 拿推荐，再带 --layout 重新组装。", file=sys.stderr)
        sys.exit(2)

    # 组装后立即校验：ERROR 直接退出，不产出坏 plan
    f = V.Findings()
    V.check(plan, f)
    for x in f.items:
        icon = {"ERROR": "❌", "WARN": "⚠️ ", "INFO": "ℹ️ "}[x["level"]]
        print(f"{icon} [{x['level']}] {x['message']}")
        if x.get("fix"):
            print(f"   怎么改：{x['fix']}")
    if f.has_error:
        print("—— plan 未生成（先修复 ERROR）")
        sys.exit(1)

    out = json.dumps(plan, ensure_ascii=False, indent=2)
    if args.output and args.output != "-":
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
        n_warn = sum(1 for x in f.items if x["level"] == "WARN")
        print(f"OK -> {args.output}（{n_warn} WARN；下一步："
              f"python3 scripts/validate_infographic_plan.py {args.output} "
              f"&& python3 scripts/render_infographic_html.py {args.output} out.html）")
    else:
        print(out)


def main():
    ap = argparse.ArgumentParser(add_help=True, description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--analyze", metavar="TEXT_FILE",
                    help="分析文本并推荐布局（'-' 读 stdin）")
    ap.add_argument("--from-blocks", metavar="DRAFT_JSON",
                    help="用 blocks 草稿组装 plan")
    ap.add_argument("-o", "--output", default="-", help="输出 plan 路径（默认 stdout）")
    ap.add_argument("--layout", choices=sorted(V.LAYOUTS), help="覆盖布局")
    ap.add_argument("--style", choices=sorted(R.PALETTES), help="visual_system.palette 预设")
    ap.add_argument("--accent", help="覆盖 accent（必须十六进制）")
    ap.add_argument("--title")
    ap.add_argument("--subtitle")
    ap.add_argument("--presets", action="store_true", help="列出可用风格 preset")
    args = ap.parse_args()

    if args.presets:
        for name, accent in load_presets().items():
            print(f"{name:<12} accent={accent}")
        return
    if args.analyze:
        text = sys.stdin.read() if args.analyze == "-" else \
            open(args.analyze, encoding="utf-8").read()
        sys.exit(print_analyze(text))
    if args.from_blocks:
        draft = json.loads(open(args.from_blocks, encoding="utf-8").read())
        from_blocks(draft, args)
        return
    ap.print_help()


if __name__ == "__main__":
    main()
