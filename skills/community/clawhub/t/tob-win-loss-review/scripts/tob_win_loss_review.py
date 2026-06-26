#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

PRIVATE_NAME_TOKENS = {"李宁", "李寧", "lining", "william"}
STOPWORDS = set("客户 我们 对方 竞品 虽然 但是 因为 所以 一个 这个 那个 阶段 有限 表现 更好 倾向 重新 评估".split())


@dataclass
class WinLossInput:
    industry: str
    size: str
    duration: str
    stage: str
    competitor: str
    event: str
    amount: str = ""


@dataclass
class RuleCause:
    name: str
    prob: int
    diagnosis: str
    rule_basis: str
    signals: list[str]
    actions: list[str]


def prompt_if_missing(v: str | None, label: str, default: str = "") -> str:
    if v:
        return v.strip()
    s = input(f"{label}{'（可选）' if default else ''}: ").strip()
    return s or default


def sanitize_filename(name: str) -> str:
    if not name:
        return ""
    base = Path(str(name)).name
    for token in PRIVATE_NAME_TOKENS:
        base = re.sub(re.escape(token), "", base, flags=re.IGNORECASE)
    base = re.sub(r"[-_—–\s]+(?=\.)", "", base)
    base = re.sub(r"^[-_—–\s]+|[-_—–\s]+$", "", base)
    return base or "已脱敏文件"


def sanitize_text(text: str) -> str:
    if not text:
        return ""

    def repl(m: re.Match[str]) -> str:
        return sanitize_filename(m.group(0))

    text = re.sub(
        r"/(?:Users|Volumes|private|tmp|var)/[^，。；：、（）()<>\[\]{}'\"]+?\.(?:pptx?|docx?|xlsx?|pdf|md|txt|xmind|html?)",
        repl,
        str(text),
        flags=re.IGNORECASE,
    )
    text = re.sub(r"/(?:Users|Volumes|private|tmp|var)/[^\s，。；：、（）()<>\[\]{}'\"]+", repl, text)
    text = re.sub(r"[A-Za-z]:\\[^\s，。；：、（）()<>\[\]{}'\"]+", repl, text)
    for token in PRIVATE_NAME_TOKENS:
        text = re.sub(re.escape(token), "", text, flags=re.IGNORECASE)
    return text.strip()


def has_any(text: str, words: list[str]) -> bool:
    low = text.lower()
    return any(w.lower() in low for w in words)


def extract_keywords(text: str) -> list[str]:
    terms: list[str] = []
    for t in re.findall(r"[\u4e00-\u9fffA-Za-z0-9%]+", text):
        if len(t) >= 2 and t not in STOPWORDS:
            terms.append(t)
    hints = ["价格", "预算", "功能", "CTO", "换人", "业务部门", "技术团队", "POC", "性能", "报价", "审批", "决策链", "价值"]
    for h in hints:
        if h.lower() in text.lower():
            terms.append(h)
    return list(dict.fromkeys(terms))[:12]


def industry_rules(industry: str) -> dict[str, Any]:
    profiles = {
        "零售": {
            "risks": ["ROI敏感", "上线速度敏感", "库存/会员/门店场景要求强"],
            "advice": "用门店效率、库存周转、复购提升三类指标包装价值，避免只讲功能。",
        },
        "金融": {
            "risks": ["合规敏感", "安全背书敏感", "决策链长"],
            "advice": "优先准备安全合规、审计、稳定性和同业背书材料。",
        },
        "制造": {
            "risks": ["现场落地敏感", "系统集成复杂", "停线风险高"],
            "advice": "用试点产线、设备/ERP/MES接口清单和停机风险预案降低顾虑。",
        },
        "政务": {
            "risks": ["流程合规敏感", "多部门协调", "预算审批慢"],
            "advice": "把方案拆成政策依据、审批路径、数据共享边界和阶段验收。",
        },
        "能源": {
            "risks": ["安全生产敏感", "资产分散", "运维成本压力"],
            "advice": "围绕安全、巡检效率、能耗与运维成本做价值量化。",
        },
    }
    for key, profile in profiles.items():
        if key in industry:
            return profile
    return {"risks": ["价值量化不足", "决策链不清", "落地路径不明确"], "advice": "先补行业场景、关键指标和分阶段落地路径。"}


def infer_causes(inp: WinLossInput) -> list[RuleCause]:
    event = sanitize_text(inp.event)
    stage = sanitize_text(inp.stage)
    industry = sanitize_text(inp.industry)
    competitor = sanitize_text(inp.competitor)
    profile = industry_rules(industry)
    causes: list[RuleCause] = []

    def add(name: str, prob: int, diagnosis: str, basis: str, signals: list[str], actions: list[str]) -> None:
        causes.append(RuleCause(name, prob, diagnosis, basis, signals, actions))

    price_words = ["价格", "报价", "预算", "高", "便宜", "成本", "贵", "降价"]
    if has_any(event + stage, price_words):
        add(
            "价格竞争力/价值包装不足",
            82,
            "客户把决策锚点拉到价格与预算；如果价值差异没有被量化成业务收益，功能更全也会被视为溢价。",
            f"行业[{industry}]+阶段[{stage}]+事件[价格/预算触发] → 价格竞争力风险",
            ["客户明确比较价格或预算", "报价谈判阶段仍未形成价值共识", *profile["risks"][:1]],
            ["把功能差异翻译成节省成本/提升收入/降低风险的量化账。", "报价前准备可降配版本、分阶段采购和ROI对照表。"],
        )

    if competitor and competitor not in {"无", "略", "未知", "未提供"}:
        add(
            "竞品打法未被拆解",
            72,
            "竞品进入客户比较框架后，需要区分输在价格、性能、品牌背书还是客户关系；否则反制动作容易失焦。",
            f"行业[{industry}]+阶段[{stage}]+竞品[{competitor}] → 竞争对标风险",
            ["客户提及明确竞品", "我方优势未转成客户评分项", "缺少竞品承诺反证材料"],
            ["补一页竞品对照：客户关心项、竞品承诺、我方反证材料。", "下次POC/方案阶段提前设置客户认可的评分表。"],
        )

    if has_any(event, ["换", "CTO", "CIO", "业务部门", "技术团队", "重新评估", "风向", "领导", "拍板"]):
        add(
            "决策链/关键人风险",
            78,
            "关键人或部门偏好变化会让原有共识失效，单线推进时风险暴露较晚。",
            f"行业[{industry}]+事件[关键人/部门变化] → 决策链风险",
            ["关键人变更或新增评审方", "业务/技术/预算多方目标不一致", "原支持者无法代表最终决策"],
            ["从第一轮开始画决策链：使用者/技术评审/预算方/拍板人/反对者。", "关键节点形成多角色共识材料，而不是只维护单一支持者。"],
        )

    if has_any(event + stage, ["POC", "试点", "测试", "性能", "接口", "集成", "演示", "demo"]):
        add(
            "POC/技术验证控制不足",
            70,
            "客户进入验证环节后，胜负手通常不是功能数量，而是验收标准、测试数据和关键场景覆盖度。",
            f"行业[{industry}]+阶段[{stage}]+事件[POC/验证触发] → 技术验证风险",
            ["POC标准不清", "测试场景未覆盖客户最关心问题", "技术结果没有转成业务结论"],
            ["POC前锁定评分表、样例数据、验收口径和失败兜底。", "把POC结果翻译成业务收益和上线风险清单。"],
        )

    stage_prob = 64 if has_any(stage, ["报价", "谈判", "合同", "POC", "方案"]) else 58
    add(
        f"{stage}阶段控制点不足",
        stage_prob,
        f"丢单发生在{stage}，说明上一阶段进入该节点前，客户评价标准、预算边界或胜负手可能没有锁定。",
        f"行业[{industry}]+阶段[{stage}] → 阶段推进控制风险",
        ["阶段进入条件不完整", "预算/决策人/评分标准未锁定", profile["advice"]],
        ["进入下一阶段前做Go/No-Go检查：预算、决策人、评分标准、竞品位置。", "把阶段风险前置为销售检查清单。"],
    )

    if not causes:
        add(
            "事实不足的综合判断",
            45,
            "当前输入缺少可稳定归因的触发词，需要补充预算、决策链、竞品承诺和内部反对意见。",
            f"行业[{industry}]+阶段[{stage}]+事件关键词[{','.join(extract_keywords(event)) or '不足'}] → 信息不足风险",
            ["关键事件描述过短", "缺少客户最终选择理由", "缺少关键会议纪要或客户原话"],
            ["补充客户最终选择理由。", "补充关键会议纪要或客户原话。"],
        )

    causes.sort(key=lambda c: c.prob, reverse=True)
    return causes[:3]


def render_report(inp: WinLossInput) -> str:
    safe = WinLossInput(**{k: sanitize_text(str(v)) for k, v in asdict(inp).items()})
    causes = infer_causes(safe)
    labels = ["🔴 核心原因", "🟡 辅助原因", "🟢 潜在风险"]

    lines: list[str] = []
    lines.append("📉 丢单复盘报告")
    lines.append("")
    lines.append("【项目画像】")
    lines.append(f"行业: {safe.industry} | 规模: {safe.size} | 跟进: {safe.duration}")
    lines.append(f"丢单阶段: {safe.stage} | 竞品: {safe.competitor or '未提供'}" + (f" | 金额: {safe.amount}" if safe.amount else ""))
    lines.append(f"关键事件: {safe.event}")
    lines.append("")

    lines.append("【根因分析（按概率排序）】")
    for idx, c in enumerate(causes):
        lines.append(f"{idx + 1}. {labels[min(idx, 2)]}：{c.name}（概率 {c.prob}%）")
        lines.append(f"   - 诊断：{c.diagnosis}")
        lines.append(f"   - 规则依据：{c.rule_basis}")
        lines.append("")

    lines.append("【风险信号对照】")
    for c in causes:
        lines.append(f"- ☑️ {c.name}：规则触发（{c.rule_basis}）")
        for signal in c.signals[:3]:
            lines.append(f"  - {signal}")
    lines.append("")

    lines.append("【改进建议】")
    lines.append("如果重来一次：")
    short: list[str] = []
    mid: list[str] = []
    for c in causes:
        short.extend(c.actions[:1])
        mid.extend(c.actions[1:2])
    short_unique = list(dict.fromkeys(short))[:3]
    mid_unique = list(dict.fromkeys(mid))[:3]
    lines.append("- 短期（下次遇到类似情况）：" + "；".join(short_unique))
    lines.append("- 中期（提升能力/方法）：" + "；".join(mid_unique or ["沉淀行业/竞品/阶段风险检查清单，把复盘结论转成售前动作。"]))
    lines.append("- 长期（体系化）：建立丢单案例库字段：行业、阶段、竞品、关键事件、最终原因、规则触发、下次反制动作。")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="ToB销售丢单复盘助手（纯规则引擎）")
    ap.add_argument("--industry")
    ap.add_argument("--size")
    ap.add_argument("--duration")
    ap.add_argument("--stage")
    ap.add_argument("--competitor", default="")
    ap.add_argument("--event")
    ap.add_argument("--amount", default="")
    ap.add_argument("--json", action="store_true", help="输出调试JSON")
    args = ap.parse_args()

    inp = WinLossInput(
        industry=prompt_if_missing(args.industry, "客户行业"),
        size=prompt_if_missing(args.size, "客户规模"),
        duration=prompt_if_missing(args.duration, "跟进时长"),
        stage=prompt_if_missing(args.stage, "丢单阶段"),
        competitor=prompt_if_missing(args.competitor, "竞品", "未提供"),
        event=prompt_if_missing(args.event, "关键事件"),
        amount=args.amount or "",
    )

    if args.json:
        safe_input = {k: sanitize_text(str(v)) for k, v in asdict(inp).items()}
        safe_inp = WinLossInput(**safe_input)
        print(json.dumps({"input": safe_input, "causes": [asdict(c) for c in infer_causes(safe_inp)]}, ensure_ascii=False, indent=2))
    else:
        print(render_report(inp))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
