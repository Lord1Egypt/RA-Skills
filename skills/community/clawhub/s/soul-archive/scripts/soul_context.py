#!/usr/bin/env python3
"""
🧬 Soul Context Injector

主动介入：在每个 AI agent 会话开始时，
注入一份精简的人格摘要 + 关键行为模式提醒，
让 agent 的回复风格立即与"档案里的你"对齐。

输出特点：
- 默认 ≤ 800 tokens（约 ~2000 个中文字符），可通过 --token-budget 调整
- Markdown 格式，便于直接拼到 system prompt 末尾
- 自动识别"高频核心信息"：身份、口头禅、价值观、Top 主题、Top 行为模式
- 同时输出"主动一致性检查"提示，让 agent 在回复前自检风格

用法：
  python3 soul_context.py                       # 输出精简上下文
  python3 soul_context.py --format json         # JSON 输出（供脚本消费）
  python3 soul_context.py --token-budget 1200   # 放宽长度
  python3 soul_context.py --no-patterns         # 不附带行为模式
"""


# ── Windows console safety: force UTF-8 on stdout/stderr so Chinese / emoji
#    don't blow up under the default cp936 codec on Windows PowerShell / cmd.
#    No-op on POSIX terminals that are already UTF-8.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    _sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from soul_extract import SoulArchive  # noqa: E402
from soul_reflect import AgentMemory  # noqa: E402


def _approx_tokens(text: str) -> int:
    """粗略估算 token 数。中文 1 字 ≈ 1.5 token，英文 1 词 ≈ 1.3 token。
    这里用 max(中文字数*1.5, len/4) 作为近似上界，宁可保守。"""
    if not text:
        return 0
    cn_count = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
    return int(cn_count * 1.5 + max(0, len(text) - cn_count) / 4)


def build_context_block(soul_dir: Path, token_budget: int = 800,
                        include_patterns: bool = True,
                        include_consistency_check: bool = True) -> str:
    archive = SoulArchive(str(soul_dir))
    if not archive.is_initialized():
        return ""

    data = archive.load_all()
    bi = data["basic_info"]
    ps = data["personality"]
    lang = data["language"]
    topics = data["topics"]
    workflow = data.get("workflow", {}) or {}
    aspirations = data.get("aspirations", {}) or {}
    profile = data["profile"]

    name = bi.get("name") or bi.get("nickname") or "User"

    # --- 头部 ---
    header = f"""## 🧬 用户人格摘要（来自 Soul Archive，完整度 {profile.get('completeness_score', 0):.0%}）
> 你正在与 **{name}** 对话。下方信息来自他/她过往会话沉淀，请据此自然调整回复风格、用词、详尽程度。"""

    # --- 身份卡 ---
    id_parts = []
    for key, label in [("occupation", "职业"), ("location", "所在地"),
                       ("age", "年龄"), ("company", "公司")]:
        if bi.get(key):
            id_parts.append(f"{label}{bi[key]}")
    identity_line = "**身份**：" + "、".join(id_parts) if id_parts else ""

    # --- 性格关键标签 ---
    pers_lines = []
    if ps.get("mbti"):
        pers_lines.append(f"MBTI {ps['mbti']}")
    if ps.get("traits"):
        pers_lines.append("特质：" + "、".join(ps["traits"][:6]))
    if ps.get("values"):
        pers_lines.append("价值观：" + "、".join(ps["values"][:5]))
    if ps.get("decision_style"):
        pers_lines.append(f"决策风格：{ps['decision_style']}")
    if ps.get("communication_preference"):
        pers_lines.append(f"沟通偏好：{ps['communication_preference']}")
    personality_block = "**性格**：" + "；".join(pers_lines) if pers_lines else ""

    # --- 语言风格（最关键）---
    lang_lines = []
    if lang.get("catchphrases"):
        cp_list = lang["catchphrases"][:5]
        lang_lines.append("口头禅：" + "、".join(repr(p) for p in cp_list))
    if lang.get("formality_level"):
        lang_lines.append(f"正式度：{lang['formality_level']}")
    if lang.get("verbosity"):
        lang_lines.append(f"详尽度：{lang['verbosity']}")
    if lang.get("humor_style"):
        lang_lines.append(f"幽默：{lang['humor_style']}")
    if lang.get("filler_words"):
        lang_lines.append(f"语气词：{'、'.join(lang['filler_words'][:5])}")
    examples = lang.get("examples", [])
    language_block = "**语言风格**：" + "；".join(lang_lines) if lang_lines else ""
    examples_block = ""
    if examples:
        ex_short = [f"> {e}" for e in examples[:3]]
        examples_block = "**典型说话样本**：\n" + "\n".join(ex_short)

    # --- Workflow ---
    wf_lines = []
    op = workflow.get("output_preferences") or {}
    op_parts = []
    if op.get("preferred_length"):
        op_parts.append(f"长度{op['preferred_length']}")
    if op.get("preferred_tone"):
        op_parts.append(f"语气{op['preferred_tone']}")
    if op.get("preferred_format"):
        op_parts.append(f"格式{op['preferred_format']}")
    if op.get("structure_first"):
        op_parts.append("结论先行")
    if op_parts:
        wf_lines.append("输出偏好：" + "、".join(op_parts))
    if workflow.get("hard_rules"):
        rules = workflow["hard_rules"][:6]
        wf_lines.append("硬规则（**必须遵守**）：" + "；".join(rules))
    if workflow.get("pet_peeves"):
        peeves = workflow["pet_peeves"][:5]
        wf_lines.append("反感（**避免触发**）：" + "、".join(peeves))
    workflow_block = "**工作偏好**：\n- " + "\n- ".join(wf_lines) if wf_lines else ""

    # --- Aspirations 简短：当前在做什么 ---
    asp_block = ""
    asp_parts = []
    proj_list = aspirations.get("active_projects") or []
    proj_strs = []
    for p in proj_list[:4]:
        if isinstance(p, dict):
            s = p.get("name", "")
            if p.get("status"):
                s += f"({p['status']})"
            proj_strs.append(s)
        elif isinstance(p, str):
            proj_strs.append(p)
    if proj_strs:
        asp_parts.append("在做：" + "、".join(proj_strs))
    if aspirations.get("long_term_goals"):
        asp_parts.append("长期目标：" + "、".join(aspirations["long_term_goals"][:2]))
    if asp_parts:
        asp_block = "**当前焦点**：" + "；".join(asp_parts)

    # --- Top 关注话题 ---
    topic_list = topics.get("topics", [])
    top_topics = sorted(topic_list, key=lambda x: x.get("frequency", 0), reverse=True)[:5]
    topics_block = ""
    if top_topics:
        topics_block = "**关注话题**：" + "、".join(t["name"] for t in top_topics)

    # --- 行为模式（来自 agent memory）---
    patterns_block = ""
    if include_patterns:
        try:
            agent = AgentMemory(soul_dir)
            patterns = agent.load_patterns()
            top_pats = sorted(
                patterns.values(),
                key=lambda p: (p.get("applications", 0), p.get("confidence", 0)),
                reverse=True
            )[:5]
            if top_pats:
                pat_lines = []
                for p in top_pats:
                    pat_lines.append(f"- **{p.get('name', '')}**：{p.get('pattern', '')}")
                patterns_block = "**与该用户协作的行为约定（务必遵守）**：\n" + "\n".join(pat_lines)
        except Exception:
            pass

    # --- 一致性自检 ---
    consistency_block = ""
    if include_consistency_check:
        consistency_block = """**回复前自检**：
- [ ] 长度/详尽度匹配上面的"详尽度"和"长度偏好"
- [ ] 关键术语保留用户惯用的中/英/缩写形式
- [ ] 如果是结论性问题：先给结论再给理由
- [ ] 如果用户语言风格记录了"直接/简洁"，就别铺垫"好的我来帮你"
- [ ] 用户的硬规则必须遵守，反感的事必须避免"""

    # --- 拼装 ---
    blocks = [header, identity_line, personality_block,
              language_block, examples_block,
              workflow_block, asp_block, topics_block,
              patterns_block, consistency_block]
    blocks = [b for b in blocks if b]
    text = "\n\n".join(blocks)

    # token 预算裁剪：保头部 + identity + personality + language + workflow（这 5 节最关键）
    # 超出预算时按倒序丢弃 examples / topics / patterns / asp
    must_keep = 5  # header / identity / personality / language / workflow
    while _approx_tokens(text) > token_budget and len(blocks) > must_keep + 1:
        # 删除最末之前的"次要"块（保留 consistency_block 在最末）
        if len(blocks) >= 2:
            blocks.pop(-2)
        else:
            blocks.pop()
        text = "\n\n".join(blocks)

    return text


def build_context_json(soul_dir: Path) -> dict:
    """JSON 形式输出，方便脚本/Agent 消费。"""
    archive = SoulArchive(str(soul_dir))
    if not archive.is_initialized():
        return {"initialized": False}

    data = archive.load_all()
    bi = data["basic_info"]
    ps = data["personality"]
    lang = data["language"]
    topics = data["topics"]
    workflow = data.get("workflow", {}) or {}
    aspirations = data.get("aspirations", {}) or {}
    profile = data["profile"]

    try:
        agent = AgentMemory(soul_dir)
        patterns = agent.load_patterns()
        top_pats = sorted(
            patterns.values(),
            key=lambda p: (p.get("applications", 0), p.get("confidence", 0)),
            reverse=True
        )[:10]
    except Exception:
        top_pats = []

    return {
        "initialized": True,
        "name": bi.get("name") or bi.get("nickname"),
        "completeness": profile.get("completeness_score", 0),
        "identity": {k: bi.get(k) for k in ("occupation", "location", "company", "age")
                    if bi.get(k)},
        "personality": {
            "mbti": ps.get("mbti"),
            "traits": (ps.get("traits") or [])[:6],
            "values": (ps.get("values") or [])[:5],
            "decision_style": ps.get("decision_style"),
            "communication_preference": ps.get("communication_preference"),
        },
        "language": {
            "catchphrases": (lang.get("catchphrases") or [])[:5],
            "formality_level": lang.get("formality_level"),
            "verbosity": lang.get("verbosity"),
            "humor_style": lang.get("humor_style"),
            "filler_words": (lang.get("filler_words") or [])[:5],
            "examples": (lang.get("examples") or [])[:3],
        },
        "workflow": {
            "hard_rules": (workflow.get("hard_rules") or [])[:8],
            "pet_peeves": (workflow.get("pet_peeves") or [])[:6],
            "output_preferences": workflow.get("output_preferences") or {},
            "tools_summary": {
                cat: (items or [])[:5]
                for cat, items in (workflow.get("tools") or {}).items() if items
            },
        },
        "aspirations": {
            "active_projects": (aspirations.get("active_projects") or [])[:5],
            "long_term_goals": (aspirations.get("long_term_goals") or [])[:3],
            "knowledge_gaps": (aspirations.get("knowledge_gaps") or [])[:5],
        },
        "top_topics": [t["name"] for t in
                      sorted(topics.get("topics", []),
                             key=lambda x: x.get("frequency", 0), reverse=True)[:5]],
        "top_patterns": top_pats,
    }


def main():
    from soul_paths import resolve_soul_dir
    default_soul_dir = resolve_soul_dir()
    parser = argparse.ArgumentParser(description="🧬 Soul Context Injector — 主动介入用的精简人格摘要")
    parser.add_argument("--soul-dir", type=Path, default=default_soul_dir,
                        help=f"灵魂数据目录（默认: {default_soul_dir}）")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown",
                        help="输出格式")
    parser.add_argument("--token-budget", type=int, default=800,
                        help="估算 token 预算（默认 800）")
    parser.add_argument("--no-patterns", action="store_true",
                        help="不附带行为模式")
    parser.add_argument("--no-self-check", action="store_true",
                        help="不附带回复前自检 checklist")

    args = parser.parse_args()

    if args.format == "json":
        print(json.dumps(build_context_json(args.soul_dir), ensure_ascii=False, indent=2))
        return

    text = build_context_block(
        args.soul_dir,
        token_budget=args.token_budget,
        include_patterns=not args.no_patterns,
        include_consistency_check=not args.no_self_check
    )
    if not text:
        print("❌ 灵魂存档尚未初始化或为空。请先运行 soul_init.py 并积累一些对话。",
              file=sys.stderr)
        sys.exit(1)
    print(text)


if __name__ == "__main__":
    main()
