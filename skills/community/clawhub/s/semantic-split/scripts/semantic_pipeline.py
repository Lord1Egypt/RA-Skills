#!/usr/bin/env python3
"""
semantic-split 三管线统一调度入口 v0.1.0

用法:
  python scripts/semantic_pipeline.py --text "帮我制作PPT"
  python scripts/semantic_pipeline.py --text "..." --flow
  python scripts/semantic_pipeline.py --text "..." --json --full
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import date

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from pipeline_b import analyze_structure, _regex_blocks, _regex_subjects, _regex_constraints, _regex_5w2h
from pipeline_a import analyze_semantic, match_json, classify_constraint, generalize_actions
from pipeline_c import build_reasoning_context

# ============================================================
# 路径
# ============================================================

DATA_DIR = SKILL_DIR.parent / ".standardization" / "semantic-split" / "data"
CAP_DIR = DATA_DIR / "capabilities"
RULE_DIR = DATA_DIR / "rules"

# ============================================================
# 钩子系统 — 流程门禁
# ============================================================

HOOK_STATUS = {
    "input_valid": False,
    "b_pipeline_done": False,
    "a_scan_done": False,
    "decision_made": False,
    "llm_generated": False,
    "focus_reasoning": False,      # 双视角：聚焦方案
    "divergent_reasoning": False,   # 双视角：发散方案
    "integration_reasoning": False, # 双视角：整合方案
    "template_saved": False,
    "wp_done": False,               # 共 10 道门禁
}

HOOK_LOG = []


def _hook(name: str, status: bool, detail: str = ""):
    """记录钩子状态"""
    HOOK_STATUS[name] = status
    HOOK_LOG.append({"hook": name, "status": "✅" if status else "⬇️", "detail": detail})


# ============================================================
# 模板库管理（自增强闭环核心）
# ============================================================

def _load_all_capabilities() -> list:
    """加载所有能力级 JSON 模板"""
    entries = []
    if not CAP_DIR.exists():
        return entries
    for f in sorted(CAP_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            data["_file"] = str(f)
            entries.append(data)
        except (json.JSONDecodeError, Exception):
            continue
    return entries


def _save_template(text: str, steps: list, five_w2h: dict):
    """
    [钩子: template_saved]
    执行后保存任务步骤为能力级 JSON 模板，实现自增强闭环。
    下次同类任务直接命中模板，跳过 LLM。
    """
    # 从输入中提取任务名
    task_name = re.sub(r'^(请|帮|帮我|我想|我需要|麻烦)', '', text.strip())[:20]
    clean_name = re.sub(r'[^\u4e00-\u9fff\w]', '', task_name)[:16]
    if not clean_name:
        clean_name = "task"

    # 通用化步骤
    actions = [s.get("action", "") or s.get("name", "") for s in steps]
    from pipeline_a import generalize_actions as _gen
    gen_actions = _gen(actions)

    # 构建能力级 JSON
    cap = {
        "id": f"{clean_name}_v1",
        "type": "capability",
        "name": clean_name,
        "version": "1.0.0",
        "created_at": str(date.today()),
        "description": f"自动生成的 {clean_name} 步骤模板",
        "generic_params": [],
        "steps": [
            {
                "id": f"s{i+1}",
                "name": s.get("name", f"步骤{i+1}"),
                "action": gen_actions[i] if i < len(gen_actions) else s.get("action", ""),
                "parallel_group": s.get("parallel_group"),
                "milestone": s.get("milestone", False),
                "dependency_heat": s.get("dependency_heat", 5),
                "depends_on": s.get("depends_on", []),
                "constraint_level": "none",
                "source": "auto_generated",
            }
            for i, s in enumerate(steps)
        ],
        "tags": [clean_name, "auto_generated"],
    }

    # 保存
    CAP_DIR.mkdir(parents=True, exist_ok=True)
    out_path = CAP_DIR / f"{clean_name}_v1.json"
    with open(str(out_path) + ".tmp", "w", encoding="utf-8") as f:
        json.dump(cap, f, ensure_ascii=False, indent=2)
    os.replace(str(out_path) + ".tmp", str(out_path))

    _hook("template_saved", True, f"已保存模板: {out_path.name} ({len(steps)} 步)")


def _scan_matching(text: str) -> list:
    """
    [钩子: a_scan_done]
    扫描模板库，返回命中结果。
    """
    caps = _load_all_capabilities()
    if not caps:
        _hook("a_scan_done", False, "模板库为空，无模板可命中")
        return []

    matches = match_json(text, caps)
    hits = [m for m in matches if m.get("score", 0) >= 0.6]

    if hits:
        _hook("a_scan_done", True, f"命中 {len(hits)} 个模板 (最高 {hits[0]['score']:.2f})")
    else:
        _hook("a_scan_done", False, f"未命中 (最高 {matches[0]['score']:.2f})" if matches else "无匹配")

    return hits


# ============================================================
# 标准处理
# ============================================================

def process(text: str, skip_llm: bool = False, full_output: bool = False) -> dict:
    result = {"status": "ok", "input": text[:200], "pipeline": {}}

    # [钩子] INPUT_VALID
    if not text or not text.strip():
        return {"status": "error", "message": "空输入"}
    _hook("input_valid", True, f"输入校验通过 ({len(text)} 字)")

    # ── Phase 1: Pipeline B - 结构分析 ──
    structure = analyze_structure(text)
    _hook("b_pipeline_done", True, f"B层={structure.get('pipeline_layers',['regex'])}")
    result["pipeline"]["b"] = {
        "subjects": structure.get("subjects", {}),
        "blocks_count": len(structure.get("blocks", {}).get("blocks", [])),
        "five_w2h": structure.get("five_w2h", {}),
        "constraints": structure.get("constraints_attention", {}).get("constraints", []),
        "layers_used": structure.get("pipeline_layers", ["regex"]),
    }

    # ── Phase 2: 扫描模板库（渐进加载）──
    matches = _scan_matching(text)
    five_w2h = structure.get("five_w2h", {})
    constraints = structure.get("constraints_attention", {}).get("constraints", [])

    if matches and matches[0].get("score", 0) >= 0.6:
        # [门禁通过] 命中模板 → 直接复用，0 LLM
        _hook("decision_made", True, f"命中模板 {matches[0]['id']} ({matches[0]['score']:.2f})，跳过 LLM")
        result["pipeline"]["a"] = {"json_matches": matches, "hit": True, "source": "template"}
        result["steps"] = [{"name": f"复用模板: {matches[0]['id']}", "action": "模板命中", "milestone": True}]
        result["method"] = "template"
        result["pipeline_summary"] = {"a_layers": ["regex", "embedding", "rerank"], "c_method": "template"}
        return result

    # 未命中 → 语义匹配（常规 Pipeline A）
    _hook("decision_made", False, "未命中模板，执行语义匹配")
    semantic = analyze_semantic(text)
    result["pipeline"]["a"] = {
        "json_matches": matches,
        "constraint": semantic.get("constraint", {}),
        "layers_used": semantic.get("pipeline_layers", ["regex"]),
    }

    # ── Phase 3: Pipeline C - 双视角推理 ──
    if skip_llm:
        _hook("llm_generated", False, "跳过 LLM（--skip-llm）")
        reasoning = {
            "steps": [{"name": "分析任务（骨架）", "action": "结构分析完成", "milestone": True}],
            "method": "skeleton",
        }
    else:
        _hook("llm_generated", True, "等待智能体推理完成")
        reasoning_context = build_reasoning_context(
            five_w2h, constraints,
            structure_analysis={
                "verbs": structure.get("five_w2h", {}).get("what", {}).get("all_verbs", []),
                "ner": structure.get("constraints_attention", {}).get("attention", {}).get("entity", []),
            },
            template_matches=matches,
        )
        reasoning = {
            "steps": [],
            "method": "agent_reasoning",
            "agent_context": reasoning_context,
        }

    # [钩子 6/7/8] 双视角推理子步骤门禁
    sub_steps = reasoning.get("agent_context", {}).get("sub_steps", [])
    for sub in sub_steps:
        sid = sub.get("id", "")
        sname = sub.get("name", "")
        hook_name = {
            "focus": "focus_reasoning",
            "diverge": "divergent_reasoning",
            "integration": "integration_reasoning",
        }.get(sid, "")
        if hook_name:
            _hook(hook_name, False, f"等待智能体执行: {sname}")
        elif sid == "decompose":
            _hook("wp_done", False, f"等待智能体: {sname}")

    result["pipeline"]["c"] = {
        "steps": reasoning.get("steps", []),
        "method": reasoning.get("method", "skeleton"),
        "agent_context": reasoning.get("agent_context"),
    }

    # [钩子] 模板保存（仅在 LLM 生成步骤且非 skip 时触发）
    if reasoning.get("method") == "agent_reasoning" and reasoning.get("steps"):
        _save_template(text, reasoning["steps"], five_w2h)

    # WP 分解
    from pipeline_c import decompose_wps
    wps = decompose_wps(reasoning.get("steps", []))
    result["pipeline"]["wps"] = wps
    _hook("wp_done", True, f"WP 分解: {len(wps)} 个工作包")

    result["pipeline_summary"] = {
        "b_layers": result["pipeline"]["b"]["layers_used"],
        "a_layers": result["pipeline"]["a"]["layers_used"],
        "c_method": result["pipeline"]["c"]["method"],
    }

    if not full_output:
        return {
            "status": "ok",
            "steps": reasoning.get("steps", []),
            "wps": wps,
            "method": result["pipeline_summary"]["c_method"],
            "pipeline_summary": result["pipeline_summary"],
            "agent_context": reasoning.get("agent_context"),
            "hooks": HOOK_LOG,
        }
    return result


# ============================================================
# CLI
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="semantic-split 三管线调度入口")
    parser.add_argument("--text", type=str, help="用户输入文本")
    parser.add_argument("--file", type=str, help="从文件读取输入")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--full", action="store_true", help="输出完整中间结果")
    parser.add_argument("--skip-llm", action="store_true", help="跳过智能体推理，返回骨架")
    parser.add_argument("--hooks", action="store_true", help="显示钩子门禁状态")

    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read().strip()
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        sys.exit(1)

    result = process(text, skip_llm=args.skip_llm, full_output=args.full)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.hooks:
        print(f"\n{'='*50}")
        print(f"  流程门禁状态")
        print(f"{'='*50}")
        for h in result.get("hooks", HOOK_LOG):
            s = "✅" if h["status"] == "✅" else "⬇️"
            print(f"  {s} {h['hook']:<20} {h['detail']}")
        print(f"{'='*50}")
    else:
        steps = result.get("steps", [])
        wps = result.get("wps", [])
        summary = result.get("pipeline_summary", {})
        print(f"\n{'='*50}")
        print(f"  semantic-split 处理结果")
        print(f"{'='*50}")
        print(f"  管线: B={summary.get('b_layers',[])}, C={summary.get('c_method','?')}")
        print(f"  步骤: {len(steps)}  WPs: {len(wps)}")
        for h in result.get("hooks", []):
            print(f"  {h['status']} {h['hook']:<20} {h['detail']}")
        print(f"{'='*50}")


if __name__ == "__main__":
    main()
