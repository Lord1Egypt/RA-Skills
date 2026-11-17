#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy skill 使用管理指南 · 报告渲染器
把 usage_diag.py 的 JSON 输出渲染成 reports/YYYY-MM-DD.md，代码化、模板化、少让 LLM 自由发挥。

用法：
  python report_builder.py <diag.json> <state.md> [--mode daily] [--out <path>]
       [--push-status sent|failed|off] [--push-reason <text>] [--force]

输入：
  <diag.json>  usage_diag.py --json 的输出（文件路径；或传 "-" 从 stdin 读）
  <state.md>   本 skill 的状态文件绝对路径

输出：
  默认写到 <skill_dir>/reports/YYYY-MM-DD.md 并打印路径；
  若无发现（issue_count==0）且无未达标 checklist 项且非 --force → 打印 "SILENT" 且不落盘（供 agent 静默跳过）。
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass  # 有意忽略：防御性处理，失败不阻断

sys.path.insert(0, str(Path(__file__).resolve().parent))
from version import VERSION  # noqa: E402  单一版本源 = SKILL.md frontmatter

PUSH_LABEL = {"sent": "已推送", "failed": "未推送", "off": "未开启"}


def _coerce_state(val):
    """state 值归一：[]/{...} 走 JSON；纯数字转 int/float；空→None。"""
    if val is None:
        return None
    s = val.strip()
    if s == "" or s in ("null", "~", "None"):
        return None
    if s and (s[0] == "[" or s[0] == "{"):
        try:
            return json.loads(s)
        except Exception:
            return s
    try:
        return int(s)
    except Exception:
        pass
    try:
        return float(s)
    except Exception:
        pass
    return s


def read_state(path):
    """极简解析 state.md 的 key: value 与 pending_actions 条目，容忍缺字段。"""
    data = {}
    pendings = []
    if path and Path(path).exists():
        try:
            text = Path(path).read_text(encoding="utf-8")
        except Exception:
            text = ""
        cur_pending = None
        for raw in text.splitlines():
            line = raw.strip()
            if line.startswith("#") or not line:
                continue
            m = re.match(r"^([\w-]+):\s*(.*)$", line)
            if m:
                key, val = m.group(1), m.group(2).strip()
                if key == "pending_actions" and val in ("", "[]"):
                    continue
                data[key] = _coerce_state(val)
            elif line.startswith("- ") and ":" in line:
                # 形如 "- id: a1"：解析首个 key: value，避免把 "id: a1" 整串塞进 id
                m2 = re.match(r"^- ([^:]+):\s*(.*)$", line)
                cur_pending = {}
                if m2:
                    cur_pending[m2.group(1).strip()] = m2.group(2).strip()
                pendings.append(cur_pending)
            elif cur_pending is not None and re.match(r"^\s{2,}([\w-]+):", raw):
                km = re.match(r"^\s*([\w-]+):\s*(.*)$", raw)
                if km:
                    cur_pending[km.group(1)] = km.group(2).strip()
    data["_pendings"] = pendings
    return data


def classify(items):
    """按 severity 分组 issue_items（仅 P0/P1/P2 入报告；INFO 级忽略不入报告）。"""
    groups = {"P0": [], "P1": [], "P2": []}
    for it in items or []:
        sev = it.get("severity", "P1")
        if sev in groups:
            groups[sev].append(it)
    return groups


def fmt_time(ts):
    try:
        return time.strftime("%Y-%m-%d %H:%M", time.localtime(ts))
    except Exception:
        return ts or ""


def _improve_top3(diag):
    """建议动作：按严重度列未达标项，最多 3 条（只讲事实，不做分值补位）。"""
    fails = [it for it in (diag.get("checklist") or []) if it.get("status") == "fail"]
    sev_w = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    fails.sort(key=lambda x: sev_w.get(x.get("severity", "P2"), 2))
    return [{"id": it.get("id"), "domain": it.get("domain"),
             "evidence": it.get("evidence", ""), "action": ""}
            for it in fails[:3]]


def render(diag, state, mode="daily", push_status="off", push_reason="",
            eco=None, self_evo=None):
    L = []
    now = time.localtime()
    date = time.strftime("%Y-%m-%d", now)
    issues = diag.get("issues", [])
    items = diag.get("issue_items", [])
    groups = classify(items)
    health = diag.get("health_score", 100)
    version = diag.get("version", VERSION)

    # 报告标题
    mode_label = "每日检查"
    L.append(f"# WorkBuddy skill 使用管理指南 · 建议报告（主动态 · {mode_label}）")
    L.append("")
    L.append(f"- 时间：{time.strftime('%Y-%m-%d %H:%M', now)}")
    L.append(f"- 模式：{mode_label}")
    L.append(f"- 推送状态：{PUSH_LABEL.get(push_status, push_status)}" +
             (f"（{push_reason}）" if push_reason and push_status != "off" else ""))
    L.append(f"- 版本自检：脚本 v{version} / 发布 v{VERSION}" +
             (" ✓ 一致" if version == VERSION else " ⚠️ 不一致，建议从源重新同步"))
    L.append(f"- 环境健康分：{health}/100")
    cl_pass = diag.get("checklist_pass")
    cl_appl = diag.get("checklist_applicable")
    if cl_appl:
        L.append(f"- 最佳实践达标：{cl_pass}/{cl_appl} 项（A 层脚本可判部分）")
    tier = diag.get("tier", "")
    tier_label = {"beginner": "初级用户", "intermediate": "进阶用户", "advanced": "高级用户"}.get(tier, "未判定")
    L.append(f"- 用户阶段：{tier_label}")
    L.append("")

    # 推送失败横幅
    if push_status == "failed" and push_reason:
        L.append(f"> ⚠️ 本次推送未送达（原因：{push_reason}），完整报告已存本文件，建议检查 agent-mail/企微连接器或下轮自动重试。")
        L.append("")

    # 发现（分级）
    L.append("## 发现")
    if not issues:
        L.append("无新发现问题（本次静默候选）。")
    else:
        for sev in ("P0", "P1", "P2"):
            if groups.get(sev):
                L.append(f"### {sev} 级")
                for it in groups[sev]:
                    L.append(f"- [{sev}] {it.get('text','')}")
                    hint = it.get("fix_hint", "")
                    if hint:
                        L.append(f"  - 建议：{hint}")
        L.append("")
    L.append("")

    # 最佳实践达标记分卡（模式 D）
    checklist = diag.get("checklist", [])
    if checklist:
        L.append("## 最佳实践达标（A 层 · 脚本可判）")
        L.append("")
        L.append("| 领域 | 检查项 | 状态 | 证据 |")
        L.append("|------|--------|------|------|")
        STATUS_LABEL = {"pass": "✅ 达标", "fail": "❌ 未达标", "na": "➖ 不适用"}
        for it in checklist:
            L.append(f"| {it.get('domain','')} | {it.get('id','')} | {STATUS_LABEL.get(it.get('status',''), it.get('status',''))} | {it.get('evidence','')} |")
        L.append("")
        L.append("> 仅列 A 层可机判项；B/C 层（启发式/自评）由 agent 在会话内判定后回写 state.md。")
        L.append("")

    # 建议动作（≤3 条，只针对脚本可判的未达标项）
    top3 = _improve_top3(diag)
    if top3:
        L.append("## 建议动作（≤3）")
        L.append("")
        for i, row in enumerate(top3, 1):
            L.append(f"{i}. **{row['id']}**（{row['domain']}）— {row['evidence']}")
            if row.get("action"):
                L.append(f"   - 建议：{row['action']}")
        L.append("")

    # 模块 E · skill 生态（覆盖度 / 缺口 / 精选推荐）
    eco_cov = state.get("ecosystem_coverage_score")
    eco_cov = eco_cov if eco_cov not in (None, "") else (eco or {}).get("coverage_score")
    if eco_cov is not None or (eco and (eco.get("gaps") or eco.get("recommendations"))):
        L.append("## skill 生态（模块 E）")
        L.append("")
        if eco_cov is not None:
            L.append(f"- 生态覆盖分：`{eco_cov}`/100（已装 / 主题积木应装）")
        gaps = (eco or {}).get("gaps", []) if eco else []
        recs = (eco or {}).get("recommendations", []) if eco else []
        if gaps:
            L.append("")
            L.append("### 生态缺口（对照主题积木）")
            L.append("")
            L.append("| 主题 | 技能 | 用途 | 二维(u/c) |")
            L.append("|------|------|------|--------------|")
            for g in gaps:
                L.append(f"| {g.get('theme', g.get('tier',''))} | {g.get('name','')} | {g.get('purpose','')} | {g.get('u','')}/{g.get('c','')} |")
        if recs:
            L.append("")
            L.append("### 精选推荐（③-4 · 二维评分）")
            L.append("")
            L.append("| 主题 | 技能 | 来源 | 二维(u/c) | workflow_set |")
            L.append("|------|------|------|--------------|--------------|")
            for r in recs:
                wf = ",".join(r.get("workflow_set", []) or [])
                L.append(f"| {r.get('theme', r.get('tier',''))} | {r.get('name','')} | {r.get('source','')} | {r.get('u','')}/{r.get('c','')} | {wf} |")
        L.append("")
        L.append("> ③-4 按「实际使用好用 / 可组合 workflow」二维评分；主题积木为人类管理员可维护。")
        L.append("")

    # 上轮采纳情况（反馈闭环）
    prev_pending = state.get("_pendings", [])
    L.append("## 上轮采纳情况")
    if not prev_pending:
        L.append("上轮无待确认项（无待办或已完成）。")
    else:
        done = [p for p in prev_pending if p.get("status") == "done"]
        other = [p for p in prev_pending if p.get("status") != "done"]
        L.append(f"- 已采纳：{len(done)} 条" + (f"（{', '.join(p.get('id','') for p in done)}）" if done else ""))
        L.append(f"- 未处理：{len(other)} 条" + (f"（{', '.join(p.get('id','') for p in other)}）" if other else ""))
    L.append("")

    # 采纳闭环战绩（只读 state.md，不在此累加——累加由 execution.md 步骤 7 在调本脚本前写回 state.md）
    checks_run = int(state.get("checks_run", 0) or 0)
    issues_found = int(state.get("issues_found", 0) or 0)
    issues_resolved = int(state.get("issues_resolved", 0) or 0)
    streak_days = int(state.get("streak_days", 0) or 0)
    L.append("## 采纳闭环战绩")
    L.append(f"- 战绩：本轮第 {checks_run} 次检查 · 累计发现 {issues_found} 项 · 已修复 {issues_resolved} 项 · 连续 {streak_days} 天")
    L.append("")

    # 模块 F · 自我学习（采纳率 / 学习事件）
    made = int(state.get("recommendations_made", 0) or 0)
    adopted = int(state.get("recommendations_adopted", 0) or 0)
    rejected = int(state.get("recommendations_rejected", 0) or 0)
    rate = (self_evo or {}).get("adoption_rate")
    if rate is None and made:
        rate = round(100.0 * adopted / made, 1)
    learnings = int(state.get("learnings_count", 0) or 0)
    last_se = state.get("last_self_evolution") or (self_evo or {}).get("last_self_evolution") or "—"
    self_has = bool(self_evo and (self_evo.get("adoption_rate") is not None
                                  or self_evo.get("learnings_count") is not None))
    if made or learnings or self_has:
        L.append("## 自我学习（模块 F）")
        L.append(f"- 技能推荐采纳率：{rate}% （采纳 {adopted} / 推荐 {made}" +
                 (f" · 拒收 {rejected}" if rejected else "") + "）")
        L.append(f"- 自我学习事件：{learnings} 条（上次折叠：{last_se}）")
        L.append("")

    # 健康分趋势（相对上轮）
    prev_health = state.get("last_health")
    if prev_health is not None and prev_health != "":
        try:
            prev = int(prev_health)
            delta = health - prev
            trend = "↑+" + str(delta) if delta > 0 else ("↓" + str(delta) if delta < 0 else "→持平")
            L.append(f"- 健康分趋势：{prev} → {health}（{trend}）")
        except Exception:
            pass  # 有意忽略：防御性处理，失败不阻断
    # 达标趋势（相对上轮，用同一个 checklist_score 口径）
    prev_cl = state.get("checklist_score")
    cur_cl = diag.get("checklist_score")
    if prev_cl not in (None, "") and cur_cl is not None:
        try:
            prev = int(prev_cl)
            delta = cur_cl - prev
            trend = "↑+" + str(delta) if delta > 0 else ("↓" + str(delta) if delta < 0 else "→持平")
            L.append(f"- 达标率趋势：{prev}% → {cur_cl}%（{trend}）")
        except Exception:
            pass  # 有意忽略：防御性处理，失败不阻断
    L.append("")

    # 待确认项
    L.append("## 待确认项（pending_actions）")
    L.append(state.get("pending_actions_summary", "见 state.md，交互态逐条确认"))
    L.append("")

    # 下一步
    L.append("## 下一步")
    L.append('打开对话说"看看建议"进入交互态确认执行；纯 P2 或无发现可忽略。')
    L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="把 usage_diag JSON 渲染成建议报告")
    ap.add_argument("diag", help="usage_diag.py --json 的输出文件，或 '-' 读 stdin")
    ap.add_argument("state", nargs="?", default=None, help="state.md 路径（可选）")
    ap.add_argument("--mode", choices=["daily"], default="daily")
    ap.add_argument("--out", default=None, help="输出文件路径（默认 <skill>/reports/YYYY-MM-DD.md）")
    ap.add_argument("--push-status", choices=["sent", "failed", "off"], default="off")
    ap.add_argument("--push-reason", default="")
    ap.add_argument("--eco", default=None, help="模块 E 数据 JSON 文件（gaps/recommendations/coverage_score）")
    ap.add_argument("--self", default=None, help="模块 F 数据 JSON 文件（adoption_rate/last_self_evolution）")
    ap.add_argument("--force", action="store_true", help="无发现也落盘")
    args = ap.parse_args()

    if args.diag == "-":
        try:
            diag = json.load(sys.stdin)
        except json.JSONDecodeError:
            print("[error] stdin 不是合法 JSON", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            diag = json.loads(Path(args.diag).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            print(f"[error] 无法读取诊断 JSON：{args.diag}", file=sys.stderr)
            sys.exit(1)

    state = read_state(args.state) if args.state else {}
    eco = None
    if args.eco:
        try:
            eco = json.loads(Path(args.eco).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            print(f"[error] 无法读取模块 E 数据：{args.eco}", file=sys.stderr)
            sys.exit(1)
    self_evo = None
    if args.self:
        try:
            self_evo = json.loads(Path(args.self).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            print(f"[error] 无法读取模块 F 数据：{args.self}", file=sys.stderr)
            sys.exit(1)

    # 静默判定：无发现、无未达标 checklist 项、非 --force → 不落盘
    has_issues = (diag.get("issue_count", 0) or 0) > 0
    has_fails = any(it.get("status") == "fail" for it in (diag.get("checklist") or []))
    eco_has_content = bool(eco and (eco.get("gaps") or eco.get("recommendations") or eco.get("coverage_score") is not None))
    self_has_content = bool(self_evo and (self_evo.get("adoption_rate") is not None or self_evo.get("learnings_count")))
    if not has_issues and not has_fails and not eco_has_content and not self_has_content and not args.force:
        print("SILENT")
        return

    out = args.out
    if not out:
        # 默认 <skill_dir>/reports/YYYY-MM-DD.md（skill_dir = 本脚本父目录的父目录）
        skill_dir = Path(__file__).resolve().parent.parent
        report_dir = skill_dir / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        out = str(report_dir / (time.strftime("%Y-%m-%d") + ".md"))

    content = render(diag, state, mode=args.mode,
                     push_status=args.push_status, push_reason=args.push_reason,
                     eco=eco, self_evo=self_evo)
    Path(out).write_text(content, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
