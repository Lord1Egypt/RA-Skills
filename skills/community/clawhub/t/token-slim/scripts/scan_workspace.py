#!/usr/bin/env python3
"""
token-slim: Workspace scanner
Scans workspace MD files and outputs a prioritized list of token optimization opportunities.

Usage:
    python3 scan_workspace.py [--workspace <path>] [--json] [--dry-run]

Output:
    Human-readable report, or raw JSON with --json.
    --dry-run: show what would be changed without modifying files.

Changes v2:
  - Token counting: tiktoken (cl100k_base) when available, fallback to
    Chinese-aware estimation (CJK chars ~0.6 tok/char, others ~0.25 tok/char)
  - Cross-file duplicate threshold raised to 0.55 for CJK content
  - memory/*.md files are now scanned (size + heavy sections)
  - count_lines excludes blank lines for accuracy
  - --dry-run mode: preview findings without writing history or modifying files
  - AGENTS.md injection uses HTML-comment anchors for idempotency
  - Mode C (Emergency) removed
  Note: undo backup is performed by the agent via bash before any file edits
        (see references/mode-a-onboarding.md Step 3), not by this script.
"""

import os
import re
import sys
import json
import argparse
import hashlib
import shutil
from pathlib import Path
from datetime import datetime


# ── Constants ─────────────────────────────────────────────────────────────────

ALWAYS_ON_FILES = [
    "MEMORY.md", "AGENTS.md", "SOUL.md", "USER.md",
    "HEARTBEAT.md", "IDENTITY.md", "TOOLS.md"
]

BOOTSTRAP_FILES = ["BOOTSTRAP.md"]

TEMPLATE_RESIDUES = [
    {
        "file": "TOOLS.md",
        "marker": "What Goes Here",
        "message": "TOOLS.md contains default template boilerplate (What Goes Here / Examples / Why Separate) — delete it, keep only your actual notes.",
        "severity": "high"
    },
    {
        "file": "TOOLS.md",
        "marker": "Why Separate?",
        "message": "TOOLS.md contains 'Why Separate?' template section — safe to delete.",
        "severity": "medium"
    },
    {
        "file": "BOOTSTRAP.md",
        "marker": None,
        "message": "BOOTSTRAP.md should be deleted after initial setup.",
        "severity": "high"
    },
    {
        "file": "AGENTS.md",
        "marker": "像人类一样使用表情回应",
        "message": "AGENTS.md contains verbose group chat / emoji reaction guide — compress to 1–2 lines.",
        "severity": "medium"
    },
]

# --workspace CLI arg overrides at runtime; these are fallback defaults.
# Cache goes under <workspace>/.cache/tiktoken (CWD-anchored, survives $HOME wipe
# on container/VM environments where only the working directory is persistent).
HISTORY_FILE = None          # set in main() based on --workspace
HISTORY_MAX = 30

TIKTOKEN_CACHE_DIR = None    # set in main() based on --workspace
BPE_CACHE_KEY = "9b5ad71b2ce5302211f9c61530b329a4922fc6a4"

# ── Token counting ────────────────────────────────────────────────────────────

_tiktoken_enc = None
_tiktoken_available = None


def _try_load_tiktoken():
    global _tiktoken_enc, _tiktoken_available
    if _tiktoken_available is not None:
        return _tiktoken_available

    # If TIKTOKEN_CACHE_DIR is not initialised yet (called outside main()),
    # fall back to a CWD-relative default.
    cache_dir = TIKTOKEN_CACHE_DIR
    if cache_dir is None:
        cache_dir = Path.cwd().resolve() / ".cache" / "tiktoken"

    # tiktoken will fetch the BPE vocab on first encode if the cache is empty
    # (network → openaipublic.blob.core.windows.net). We don't require it to
    # pre-exist or to match a specific SHA — tiktoken handles validation.
    try:
        import importlib.util
        if importlib.util.find_spec("tiktoken") is None:
            _tiktoken_available = False
            return False

        import tiktoken
        cache_dir.mkdir(parents=True, exist_ok=True)
        os.environ["TIKTOKEN_CACHE_DIR"] = str(cache_dir)
        _tiktoken_enc = tiktoken.get_encoding("cl100k_base")
        _tiktoken_available = True
        return True
    except Exception:
        _tiktoken_available = False
        return False


def count_tokens_approx(path_or_text, is_text=False):
    """
    Count tokens accurately with tiktoken when available.
    Fallback: CJK chars ≈ 0.6 tok/char, others ≈ 0.25 tok/char (English ~4 chars/tok).
    Returns integer token estimate.
    """
    if is_text:
        text = path_or_text
    else:
        try:
            with open(path_or_text, encoding="utf-8") as f:
                text = f.read()
        except Exception:
            return 0

    if _try_load_tiktoken() and _tiktoken_enc is not None:
        try:
            return len(_tiktoken_enc.encode(text))
        except Exception:
            pass

    # Fallback: Chinese-aware estimation
    cjk = len(re.findall(r"[\u4e00-\u9fff\u3400-\u4dbf\u20000-\u2a6df]", text))
    other = len(text) - cjk
    return int(cjk * 0.6 + other * 0.25)


def count_lines(path, exclude_blank=True):
    """Count lines in a file; by default excludes blank lines for accuracy."""
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
        if exclude_blank:
            return sum(1 for l in lines if l.strip())
        return len(lines)
    except Exception:
        return 0


# ── Heavy section detection ───────────────────────────────────────────────────

def find_heavy_sections(path, min_lines=20):
    """Find self-contained sections that could be moved to memoryres/."""
    findings = []
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return findings

    sections = re.split(r"\n(?=#{1,3} )", content)
    for section in sections:
        lines = [l for l in section.strip().split("\n") if l.strip()]
        if len(lines) < min_lines:
            continue
        heading = lines[0].strip("# ").strip()

        skip_keywords = [
            "cron", "heartbeat", "reminde", "warn", "must", "never", "always",
            "禁止", "必须", "不可", "强制", "零容忍", "避坑", "rule", "principle",
            "规范", "准则"
        ]
        if any(k.lower() in heading.lower() for k in skip_keywords):
            continue

        has_table = any("|" in l for l in lines)
        has_code  = any(l.strip().startswith("```") for l in lines)
        has_list  = sum(1 for l in lines if l.strip().startswith(("- ", "* ")))

        movable_keywords = [
            "okr", "kpi", "vocab", "词汇", "glossar", "css", "工具库",
            "migration", "迁移", "backlog", "待迁", "reference", "参考", "schema",
            "spec", "规格", "api doc", "接口文档", "template", "模板", "历史",
            "history", "incident", "changelog", "变更", "tech debt", "技术债"
        ]
        is_movable = (
            any(k.lower() in heading.lower() for k in movable_keywords)
            or (has_table and len(lines) > 25)
            or (has_code and len(lines) > 30)
        )

        if is_movable:
            token_est = count_tokens_approx("\n".join(lines), is_text=True)
            findings.append({
                "section": heading,
                "lines": len(lines),
                "tokens_approx": token_est,
                "has_table": has_table,
                "has_code_block": has_code,
                "list_items": has_list,
                "suggestion": f"Move to memoryres/{_suggest_filename(heading)}"
            })

    return findings


def _suggest_filename(heading):
    name = heading.lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name).strip("-")
    mappings = {
        "okr": "okr", "vocab": "vocab", "词汇": "vocab", "css": "css-refs",
        "tool": "tools-ref", "工具": "tools-ref", "迁移": "migration-backlog",
        "migration": "migration-backlog", "api": "api-refs", "template": "templates",
    }
    for k, v in mappings.items():
        if k in name:
            return f"{v}.md"
    return f"{name[:30]}.md"


# ── Template residue checker ──────────────────────────────────────────────────

def check_template_residue(workspace_path):
    workspace = Path(workspace_path).expanduser()
    findings = []

    for residue in TEMPLATE_RESIDUES:
        fpath = workspace / residue["file"]
        if residue["marker"] is None:
            if fpath.exists():
                findings.append({
                    "file": residue["file"],
                    "lines": count_lines(fpath),
                    "tokens_approx": count_tokens_approx(fpath),
                    "always_loaded": True,
                    "issues": [{"severity": residue["severity"], "message": residue["message"]}],
                    "movable_sections": [],
                    "_source": "template_residue"
                })
        else:
            if not fpath.exists():
                continue
            try:
                content = fpath.read_text(encoding="utf-8")
            except Exception:
                continue
            if residue["marker"] in content:
                findings.append({
                    "file": residue["file"],
                    "lines": count_lines(fpath),
                    "tokens_approx": count_tokens_approx(fpath),
                    "always_loaded": True,
                    "issues": [{"severity": residue["severity"], "message": residue["message"]}],
                    "movable_sections": [],
                    "_source": "template_residue"
                })

    return findings


# ── Cross-file duplicate detection ───────────────────────────────────────────

def _extract_sections(path):
    sections = []
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return sections

    parts = re.split(r"\n(?=#{2,3} )", content)
    for part in parts:
        lines = part.strip().split("\n")
        m = re.match(r"^#{2,3}\s+(.+)", lines[0])
        if not m:
            continue
        heading = m.group(1).strip()
        body = lines[1:]
        sections.append((heading, body))
    return sections


def _keywords(text):
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"[#*_|>\-]", " ", text)
    text = re.sub(r"https?://\S+", "", text)

    tokens = re.findall(r"[\w\u4e00-\u9fff]{2,}", text.lower())
    stopwords = {
        "的", "了", "是", "在", "和", "与", "或", "不", "有", "这", "那",
        "要", "可以", "使用", "进行", "如果", "需要", "通过", "方式", "时候",
        "the", "a", "an", "is", "are", "was", "be", "to", "of", "in",
        "and", "or", "not", "for", "with", "this", "that", "it", "on",
        "at", "by", "as", "if", "when", "use", "can", "will", "do",
    }
    return set(t for t in tokens if t not in stopwords)


def _jaccard(set_a, set_b):
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


def check_cross_file_duplicates(workspace_path):
    workspace = Path(workspace_path).expanduser()
    findings = []

    file_sections = {}
    for filename in ALWAYS_ON_FILES:
        fpath = workspace / filename
        if fpath.exists():
            sections = _extract_sections(fpath)
            file_sections[filename] = [
                (h, body, _keywords("\n".join(body)))
                for h, body in sections
                if len(body) >= 2
            ]

    # Raised from 0.40 → 0.55 to reduce CJK false positives
    JACCARD_THRESHOLD = 0.55

    files = list(file_sections.keys())
    reported = set()

    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            fa, fb = files[i], files[j]
            for ha, body_a, kw_a in file_sections[fa]:
                for hb, body_b, kw_b in file_sections[fb]:
                    score = _jaccard(kw_a, kw_b)
                    if score < JACCARD_THRESHOLD:
                        continue
                    key = (fa, ha, fb, hb)
                    if key in reported:
                        continue
                    reported.add(key)

                    preview_a = " | ".join(l.strip() for l in body_a if l.strip())[:120]
                    preview_b = " | ".join(l.strip() for l in body_b if l.strip())[:120]

                    findings.append({
                        "file": f"{fa} ↔ {fb}",
                        "issues": [{
                            "severity": "info",
                            "message": (
                                f"Possible duplicate content (similarity {score:.0%}):\n"
                                f"  [{fa}] 「{ha}」: {preview_a}…\n"
                                f"  [{fb}] 「{hb}」: {preview_b}…\n"
                                f"  → 请人工确认是否真实重复"
                            )
                        }],
                        "movable_sections": []
                    })

    return findings


# ── Token history persistence ─────────────────────────────────────────────────

def _load_history():
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []


def _save_history(history):
    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        history = history[-HISTORY_MAX:]
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        # History write failure should not crash the scan report
        pass


def _record_scan_result(workspace_path, findings):
    workspace = Path(workspace_path).expanduser()
    file_tokens = {}
    total_tokens = 0
    for filename in ALWAYS_ON_FILES:
        fpath = workspace / filename
        if fpath.exists():
            t = count_tokens_approx(fpath)
            file_tokens[filename] = t
            total_tokens += t

    history = _load_history()
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_tokens": total_tokens,
        "files": file_tokens,
        "token_counter": "tiktoken" if _tiktoken_available else "estimate"
    }
    history.append(entry)
    _save_history(history)
    return history, total_tokens


# ── Skills directory scan ─────────────────────────────────────────────────────

def scan_skills_directory(workspace_path):
    workspace = Path(workspace_path).expanduser()
    skills_dir = workspace / "skills"
    findings = []

    if not skills_dir.exists():
        return findings

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        if skill_dir.name == "token-slim":
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        lines = count_lines(skill_md)
        if lines > 200:
            findings.append({
                "file": f"skills/{skill_dir.name}/SKILL.md",
                "lines": lines,
                "tokens_approx": count_tokens_approx(skill_md),
                "always_loaded": False,
                "issues": [{
                    "severity": "low",
                    "message": (
                        f"Skill '{skill_dir.name}' has a large SKILL.md ({lines} non-blank lines) "
                        f"— only name/description/location are loaded per session (~24 tokens); "
                        f"full content is read on-demand. Large files slow down skill execution, not session start."
                    )
                }],
                "movable_sections": []
            })

    return findings


# ── memory/*.md scan (NEW) ────────────────────────────────────────────────────

def scan_memory_files(workspace_path):
    """
    Scan memory/*.md files for size issues.
    These are loaded on-demand (via MEMORY.md index), not every session,
    but large files still slow down retrieval and inflate context when loaded.
    """
    workspace = Path(workspace_path).expanduser()
    memory_dir = workspace / "memory"
    findings = []

    if not memory_dir.exists():
        return findings

    # Daily log files: flag accumulation
    daily_files = sorted(memory_dir.glob("????-??-??.md"))
    if len(daily_files) > 30:
        findings.append({
            "file": "memory/ (daily logs)",
            "lines": len(daily_files),
            "tokens_approx": 0,
            "issues": [{
                "severity": "low",
                "message": f"{len(daily_files)} daily memory files found. Consider archiving files older than 30 days into a monthly summary."
            }],
            "movable_sections": []
        })

    # Named reference files (memory/xxx.md): flag large ones
    ref_files = [f for f in memory_dir.glob("*.md") if not re.match(r"\d{4}-\d{2}-\d{2}\.md", f.name)]
    large_refs = []
    for ref in sorted(ref_files):
        lines = count_lines(ref)
        tokens = count_tokens_approx(ref)
        if lines > 80 or tokens > 800:
            large_refs.append({
                "name": f"memory/{ref.name}",
                "lines": lines,
                "tokens": tokens
            })

    if large_refs:
        details = "; ".join(f"{r['name']} ({r['lines']} lines, ~{r['tokens']} tokens)" for r in large_refs)
        findings.append({
            "file": "memory/ (reference files)",
            "lines": sum(r["lines"] for r in large_refs),
            "tokens_approx": sum(r["tokens"] for r in large_refs),
            "issues": [{
                "severity": "low",
                "message": (
                    f"{len(large_refs)} large memory reference file(s) found — "
                    f"these load into context when referenced via MEMORY.md index. "
                    f"Consider splitting or summarizing: {details}"
                )
            }],
            "movable_sections": []
        })

    return findings


# ── Main scanner ──────────────────────────────────────────────────────────────

def scan_workspace(workspace_path):
    workspace = Path(workspace_path).expanduser()
    findings = []

    # 1. Always-on files
    for filename in ALWAYS_ON_FILES:
        fpath = workspace / filename
        if not fpath.exists():
            continue

        lines = count_lines(fpath)
        tokens = count_tokens_approx(fpath)

        file_finding = {
            "file": filename,
            "lines": lines,
            "tokens_approx": tokens,
            "always_loaded": True,
            "issues": [],
            "movable_sections": []
        }

        if filename == "MEMORY.md" and lines > 200:
            file_finding["issues"].append({
                "severity": "high",
                "message": f"MEMORY.md is {lines} non-blank lines — target is < 150. Burns ~{tokens} tokens every session."
            })
        elif filename == "HEARTBEAT.md" and lines > 60:
            file_finding["issues"].append({
                "severity": "medium",
                "message": f"HEARTBEAT.md is {lines} non-blank lines — target is < 50. Loaded on every heartbeat."
            })
        elif filename == "AGENTS.md" and lines > 300:
            file_finding["issues"].append({
                "severity": "medium",
                "message": f"AGENTS.md is {lines} non-blank lines — consider splitting operational rules from reference content."
            })

        if filename in ("MEMORY.md", "AGENTS.md", "TOOLS.md"):
            movable = find_heavy_sections(fpath)
            if movable:
                file_finding["movable_sections"] = movable
                total_movable_tokens = sum(s["tokens_approx"] for s in movable)
                file_finding["issues"].append({
                    "severity": "high" if total_movable_tokens > 500 else "medium",
                    "message": f"Found {len(movable)} section(s) that can be moved to memoryres/ — saving ~{total_movable_tokens} tokens/session."
                })

        if file_finding["issues"] or file_finding["movable_sections"]:
            findings.append(file_finding)

    # 2. Bootstrap files
    for filename in BOOTSTRAP_FILES:
        fpath = workspace / filename
        if fpath.exists():
            tokens = count_tokens_approx(fpath)
            findings.append({
                "file": filename,
                "lines": count_lines(fpath),
                "tokens_approx": tokens,
                "always_loaded": True,
                "issues": [{
                    "severity": "high",
                    "message": f"{filename} is a one-time setup guide — delete it to save ~{tokens} tokens/session."
                }],
                "movable_sections": []
            })

    # 3. memoryres/ exists?
    memoryres = workspace / "memoryres"
    if not memoryres.exists():
        findings.append({
            "file": "memoryres/ (missing)",
            "issues": [{
                "severity": "info",
                "message": "No memoryres/ directory found. Create it to store reference content that doesn't need to load every session."
            }],
            "movable_sections": []
        })

    # 4. memory/*.md (daily logs + reference files)
    findings.extend(scan_memory_files(workspace_path))

    # 5. Template residue
    template_findings = check_template_residue(workspace_path)
    existing_files = {f["file"] for f in findings}
    for tf in template_findings:
        already = any(
            f["file"] == tf["file"] and
            any(i["message"] == tf["issues"][0]["message"] for i in f.get("issues", []))
            for f in findings
        )
        if not already:
            findings.append(tf)

    # 6. Cross-file duplicates
    findings.extend(check_cross_file_duplicates(workspace_path))

    # 7. Skills directory
    findings.extend(scan_skills_directory(workspace_path))

    # 8. Record scan history (skip when dry_run to preserve "no file writes" semantics)
    if not getattr(scan_workspace, "_dry_run", False):
        history, total_tokens = _record_scan_result(workspace_path, findings)
    else:
        history = _load_history()
        total_tokens = sum(
            count_tokens_approx(Path(workspace_path).expanduser() / fn)
            for fn in ALWAYS_ON_FILES
            if (Path(workspace_path).expanduser() / fn).exists()
        )

    findings.insert(0, {
        "_meta": True,
        "_history": history,
        "_total_tokens": total_tokens,
        "_token_counter": "tiktoken" if _tiktoken_available else "estimate"
    })

    return findings


# ── Report printer ────────────────────────────────────────────────────────────

def print_report(findings, dry_run=False):
    history = []
    total_tokens = 0
    token_counter = "estimate"
    real_findings = []

    for f in findings:
        if f.get("_meta"):
            history = f.get("_history", [])
            total_tokens = f.get("_total_tokens", 0)
            token_counter = f.get("_token_counter", "estimate")
        else:
            real_findings.append(f)
    findings = real_findings

    counter_label = "🎯 tiktoken 精确计数" if token_counter == "tiktoken" else "📐 中英分计估算（误差±40%）"
    if dry_run:
        print("\n🔍 [DRY-RUN] Token Saver Scan — 预览模式，不会修改任何文件")
    else:
        print("\n🔍 Token Saver Scan Results")
    print(f"{'='*50}")
    print(f"  Token 计数方式: {counter_label}")

    if not findings:
        print("✅ No significant token waste found. Workspace looks lean!")
        _print_history_trend(history, total_tokens)
        return

    high   = [f for f in findings if any(i["severity"] == "high"   for i in f.get("issues", []))]
    medium = [f for f in findings if any(i["severity"] == "medium" for i in f.get("issues", []))]
    low    = [f for f in findings if any(i["severity"] in ("low", "info") for i in f.get("issues", []))]

    total_movable_tokens = sum(
        s["tokens_approx"]
        for f in findings
        for s in f.get("movable_sections", [])
    )

    _print_history_trend(history, total_tokens)
    print(f"  High priority:   {len(high)} file(s)")
    print(f"  Medium priority: {len(medium)} file(s)")
    print(f"  Low/Info:        {len(low)} item(s)")
    if total_movable_tokens > 0:
        print(f"  Potential savings: ~{total_movable_tokens} tokens/session")
    if dry_run:
        print(f"\n  ⚠️  DRY-RUN: 以下是会被修改的内容预览，未实际执行\n")
    print()

    severity_order = ["high", "medium", "low", "info"]
    all_sorted = sorted(findings, key=lambda f: min(
        severity_order.index(i["severity"]) for i in f.get("issues", [{"severity": "info"}])
    ))

    for finding in all_sorted:
        fname  = finding["file"]
        lines  = finding.get("lines", "?")
        tokens = finding.get("tokens_approx", "?")

        print(f"📄 {fname}  ({lines} non-blank lines, ~{tokens} tokens)")
        for issue in finding.get("issues", []):
            sev = issue["severity"].upper()
            icons = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🔵", "INFO": "ℹ️"}
            print(f"  {icons.get(sev, '  ')} [{sev}] {issue['message']}")

        for section in finding.get("movable_sections", []):
            action = "→ [DRY-RUN] Would move" if dry_run else "→ Section"
            print(f"     {action}: \"{section['section']}\" ({section['lines']} lines, ~{section['tokens_approx']} tokens)")
            print(f"       Suggested: {section['suggestion']}")
        print()

    _print_before_after(history)


def _print_history_trend(history, total_tokens):
    if len(history) >= 2:
        prev = history[-2]
        prev_tokens = prev.get("total_tokens", 0)
        delta = total_tokens - prev_tokens
        sign = "+" if delta >= 0 else ""
        print(f"  📈 上次: {prev_tokens} tokens → 本次: {total_tokens} tokens（变化 {sign}{delta}）")
    else:
        print(f"  📊 本次扫描: {total_tokens} tokens（首次记录，下次扫描将显示趋势）")


def _print_before_after(history):
    if len(history) < 2:
        return

    first_tokens = history[0].get("total_tokens", 0)
    last_tokens  = history[-1].get("total_tokens", 0)

    if first_tokens == 0:
        return

    saved   = first_tokens - last_tokens
    pct     = round(saved / first_tokens * 100, 1) if first_tokens > 0 else 0
    daily   = saved * 100
    monthly = daily * 22

    print(f"\n📊 Token History:")
    print(f"  Before optimization: {first_tokens} tokens/session")
    print(f"  After optimization:  {last_tokens} tokens/session")
    print(f"  Saved: {saved} tokens/session (~{pct}% reduction)")
    print(f"  Est. daily savings:   ~{daily:,} tokens (100 sessions/day)")
    print(f"  Est. monthly savings: ~{monthly:,} tokens (22 working days/month)")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    global HISTORY_FILE, TIKTOKEN_CACHE_DIR

    parser = argparse.ArgumentParser(description="Scan workspace for token optimization opportunities")
    parser.add_argument(
        "--workspace", default=None,
        help="Workspace path. Defaults to the current working directory.",
    )
    parser.add_argument("--json",    action="store_true", help="Output raw JSON")
    parser.add_argument("--dry-run", action="store_true", help="Preview mode: show what would change without modifying files")
    args = parser.parse_args()

    # Resolve workspace: --workspace > $TOKEN_SLIM_WORKSPACE > CWD
    workspace = args.workspace or os.environ.get("TOKEN_SLIM_WORKSPACE") or str(Path.cwd())
    ws_path = Path(workspace).expanduser().resolve()

    # Anchor per-workspace state directories
    HISTORY_FILE = ws_path / ".token-slim" / "token-history.json"
    TIKTOKEN_CACHE_DIR = ws_path / ".cache" / "tiktoken"

    # Pre-load tiktoken silently
    _try_load_tiktoken()

    # Pass dry_run flag to scan_workspace via function attribute
    scan_workspace._dry_run = args.dry_run

    findings = scan_workspace(str(ws_path))

    if args.json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
    else:
        print_report(findings, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
