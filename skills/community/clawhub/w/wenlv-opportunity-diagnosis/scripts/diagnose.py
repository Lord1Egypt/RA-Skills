#!/usr/bin/env python3
"""
文旅项目机会诊断判定脚本 — 五维决策门版

用法：
    python diagnose.py '<JSON>'

输入 JSON 格式：
{
    "project_name": "项目名称",
    "gate_results": {
        "gate0": {"passed": true, "violations": []},
        "gate1": {"red_count": 0, "critical_violations": []},
        "gate2": {"red_count": 1, "critical_violations": []},
        "gate3": {"red_count": 0, "critical_violations": []},
        "gate4": {"red_count": 2, "critical_violations": ["D4"]},
        "gate5": {"red_count": 0, "critical_violations": []}
    }
}

输出：逐门状态 + 综合判定 (GO / GO-WITH-CONDITIONS / NO-GO)
"""

import sys
import json

GATE_NAMES = {
    "gate0": "政策合规红线（一票否决）",
    "gate1": "资源价值判断",
    "gate2": "市场机会判断",
    "gate3": "产品设计判断",
    "gate4": "商业模型判断",
    "gate5": "运营传播判断",
}

GATE_CRITICAL_QUESTIONS = {
    "gate1": ["A10"],
    "gate2": ["B6"],
    "gate3": ["C1", "C3"],
    "gate4": ["D4"],
    "gate5": ["E1"],
}

GATE_QUESTIONS = {
    "gate1": ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"],
    "gate2": ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10"],
    "gate3": ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"],
    "gate4": ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10"],
    "gate5": ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10"],
}


def gate_status(gate_key: str, red_count: int, critical_violations: list) -> str:
    """计算单门状态：绿灯 / 黄灯 / 红灯"""
    criticals = GATE_CRITICAL_QUESTIONS.get(gate_key, [])
    has_critical_red = any(q in critical_violations for q in criticals)

    if has_critical_red:
        return "red"
    if red_count >= 2:
        return "yellow"
    return "green"


def overall_verdict(gate_results: dict) -> dict:
    """综合判读：GO / GO-WITH-CONDITIONS / NO-GO"""
    # 门0 一票否决
    if not gate_results.get("gate0", {}).get("passed", True):
        return {
            "verdict": "NO-GO",
            "reason": "门0 政策合规红线命中，一票否决。以主管部门认定为准。",
        }

    gates = {}
    any_red = False
    any_yellow = False
    conditions = []

    for gk in ["gate1", "gate2", "gate3", "gate4", "gate5"]:
        gr = gate_results.get(gk, {})
        red_count = gr.get("red_count", 0)
        critical_violations = gr.get("critical_violations", [])
        status = gate_status(gk, red_count, critical_violations)
        gates[gk] = {
            "name": GATE_NAMES[gk],
            "status": status,
            "red_count": red_count,
            "critical_violations": critical_violations,
        }
        if status == "red":
            any_red = True
            gates[gk]["note"] = "关键题红灯，该维度建议退出"
        elif status == "yellow":
            any_yellow = True
            gates[gk]["note"] = f"红灯≥2，限制条件推进"

    if any_red:
        red_gates = [v["name"] for v in gates.values() if v["status"] == "red"]
        return {
            "verdict": "NO-GO",
            "reason": f"以下维度红灯，建议退出：{'、'.join(red_gates)}",
            "gates": gates,
        }
    elif any_yellow:
        return {
            "verdict": "GO-WITH-CONDITIONS",
            "reason": "部分维度存在黄灯，需在限定条件下推进。",
            "gates": gates,
        }
    else:
        return {
            "verdict": "GO",
            "reason": "所有维度绿灯，项目机会良好，建议进入文旅操盘全链路评估。",
            "gates": gates,
            "next_step": "建议进入 wenlv-caopan（文旅操盘）做全链路评估。",
        }


def format_report(project_name: str, gate_results: dict) -> str:
    """格式化输出五维决策门诊断报告"""
    verdict = overall_verdict(gate_results)

    lines = []
    lines.append("=" * 60)
    lines.append(f"  文旅项目五维决策门 · 诊断报告")
    lines.append("=" * 60)
    lines.append(f"  项目名称：{project_name}")
    lines.append("")

    # 门0
    g0 = gate_results.get("gate0", {})
    passed = g0.get("passed", True)
    violations = g0.get("violations", [])
    if not passed:
        lines.append(f"【门0 · 政策合规红线】❌ 一票否决")
        for v in violations:
            lines.append(f"  命中红线：{v}")
        lines.append("  注：以主管部门认定为准")
        lines.append("")
    else:
        lines.append(f"【门0 · 政策合规红线】✅ 通过")
        lines.append("")

    # 门1-5
    if passed and verdict.get("gates"):
        for gk in ["gate1", "gate2", "gate3", "gate4", "gate5"]:
            g = verdict["gates"][gk]
            icon = {"green": "🟢", "yellow": "🟡", "red": "🔴"}[g["status"]]
            label = {"green": "绿灯", "yellow": "黄灯", "red": "红灯"}[g["status"]]
            lines.append(f"  {icon} {g['name']}：{label}")
            if g["red_count"] > 0:
                lines.append(f"     红灯数：{g['red_count']}/10")
                if g.get("critical_violations"):
                    lines.append(f"     关键题红灯：{', '.join(g['critical_violations'])}")
            if g.get("note"):
                lines.append(f"     提示：{g['note']}")
            lines.append("")

    # 综合结论
    verdict_icon = {"GO": "🟢", "GO-WITH-CONDITIONS": "🟡", "NO-GO": "🔴"}
    lines.append("【综合判定】")
    lines.append(f"  {verdict_icon.get(verdict['verdict'], '')} {verdict['verdict']}")
    lines.append(f"  {verdict['reason']}")
    if verdict.get("next_step"):
        lines.append(f"  → {verdict['next_step']}")
    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        example = {
            "project_name": "XX山文旅度假区",
            "gate_results": {
                "gate0": {"passed": True, "violations": []},
                "gate1": {"red_count": 0, "critical_violations": []},
                "gate2": {"red_count": 1, "critical_violations": []},
                "gate3": {"red_count": 0, "critical_violations": []},
                "gate4": {"red_count": 0, "critical_violations": []},
                "gate5": {"red_count": 0, "critical_violations": []},
            },
        }
        print("用法：python diagnose.py '<JSON>'\n")
        print("示例输入：")
        print(json.dumps(example, ensure_ascii=False, indent=2))
        print("\n--- 基于示例的运行结果 ---\n")
        print(format_report(example["project_name"], example["gate_results"]))
        return

    try:
        input_data = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误：{e}", file=sys.stderr)
        sys.exit(1)

    project_name = input_data.get("project_name", "未命名项目")
    gate_results = input_data.get("gate_results", {})

    # 校验
    required = ["gate0", "gate1", "gate2", "gate3", "gate4", "gate5"]
    missing = [g for g in required if g not in gate_results]
    if missing:
        missing_names = [GATE_NAMES.get(g, g) for g in missing]
        print(f"错误：缺少以下门的判读结果：{', '.join(missing_names)}", file=sys.stderr)
        sys.exit(1)

    print(format_report(project_name, gate_results))


if __name__ == "__main__":
    main()
