#!/usr/bin/env python3
"""ReflexLearn v1.1.1 — OpenClaw continuous learning via implicit feedback.
v1.1.1: path validation (writes restricted to ~/.openclaw/), model-download guard,
--offline flag, removed unused scikit-learn dependency.
"""
from __future__ import annotations
import argparse, json, os, re, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
import numpy as np

# ── Config defaults ──────────────────────────────────────────────────────────
SIMILARITY_THRESHOLD: float = 0.85
LOOKBACK_INTERACTIONS: int = 10
POSITIVE_REINFORCEMENT_DELAY: int = 3
REPEAT_COUNT_THRESHOLD: int = 2
SESSION_WINDOW_MINUTES: int = 60
MODE: str = "cautious"  # "cautious" | "aggressive"
MODIFIER_PATTERNS = re.compile(
    r"\b(more concise|be concise|shorter|longer|add examples?|with examples?|"
    r"use bullets?|in bullets?|in table|table format|add sources?|with sources?|"
    r"simpler|more detail|more verbose|step.by.step|step by step|"
    r"in json|as json|in markdown|as markdown|with type hints?|type hints?|"
    r"without|instead|but (also|with|use|include|make)|with annotations?|"
    r"try again|redo|rewrite|rephrase|format|style|annotated|typed|verbose|brief)\b",
    re.IGNORECASE
)
_model = None
_OPENCLAW_BASE: Path = Path(os.path.expanduser("~/.openclaw")).resolve()
_MODEL_NAME = "all-MiniLM-L6-v2"

def _model_is_cached() -> bool:
    try:
        from huggingface_hub import try_to_load_from_cache
        r = try_to_load_from_cache(f"sentence-transformers/{_MODEL_NAME}", "config.json")
        return r is not None and r != ""
    except Exception: return False

def _get_model(offline: bool = False):
    global _model
    if _model is None:
        try: from sentence_transformers import SentenceTransformer
        except ImportError:
            print("[ReflexLearn] ERROR: run install.sh or pip install sentence-transformers numpy",
                  file=sys.stderr); sys.exit(1)
        if not _model_is_cached():
            if offline:
                print("[ReflexLearn] ERROR: model not cached and --offline set. "
                      "Run install.sh to pre-cache.", file=sys.stderr); sys.exit(1)
            print(f"[ReflexLearn] WARNING: '{_MODEL_NAME}' not in local cache.")
            print("[ReflexLearn] One-time ~80 MB download from Hugging Face required.")
            print("[ReflexLearn] Pre-cache by running: bash install.sh")
        _model = SentenceTransformer(_MODEL_NAME)
        print("[ReflexLearn] Model ready.")
    return _model

def _validate_path(p: Path) -> Path:
    resolved = p.resolve()
    try: resolved.relative_to(_OPENCLAW_BASE)
    except ValueError:
        print(f"[ReflexLearn] SECURITY: refusing to write outside ~/.openclaw/: {resolved}",
              file=sys.stderr); sys.exit(1)
    return resolved

# ── Config loader ────────────────────────────────────────────────────────────
def load_config(skill_md: Path) -> None:
    global SIMILARITY_THRESHOLD, LOOKBACK_INTERACTIONS, POSITIVE_REINFORCEMENT_DELAY
    global REPEAT_COUNT_THRESHOLD, SESSION_WINDOW_MINUTES, MODE
    if not skill_md.exists(): return
    text = skill_md.read_text(encoding="utf-8")
    for key, pattern, cast in [
        ("SIMILARITY_THRESHOLD",        r"SIMILARITY_THRESHOLD:\s*([\d.]+)", float),
        ("LOOKBACK_INTERACTIONS",       r"LOOKBACK_INTERACTIONS:\s*(\d+)",   int),
        ("POSITIVE_REINFORCEMENT_DELAY",r"POSITIVE_REINFORCEMENT_DELAY:\s*(\d+)", int),
        ("REPEAT_COUNT_THRESHOLD",      r"REPEAT_COUNT_THRESHOLD:\s*(\d+)",  int),
        ("SESSION_WINDOW_MINUTES",      r"SESSION_WINDOW_MINUTES:\s*(\d+)",  int),
        ("MODE",                        r"MODE:\s*(cautious|aggressive)",     str),
    ]:
        m = re.search(pattern, text)
        if m: globals()[key] = cast(m.group(1))
    print(f"[ReflexLearn] Config: threshold={SIMILARITY_THRESHOLD} lookback={LOOKBACK_INTERACTIONS} repeats={REPEAT_COUNT_THRESHOLD} window={SESSION_WINDOW_MINUTES}min mode={MODE}")

# ── Math ──────────────────────────────────────────────────────────────────────
def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return float(np.dot(a, b) / (na * nb)) if na and nb else 0.0

# ── History helpers ───────────────────────────────────────────────────────────
def load_history(path: Path) -> list[dict]:
    if not path.exists(): return []
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
        return d if isinstance(d, list) else []
    except (json.JSONDecodeError, OSError): return []

def save_history(path: Path, history: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")

def append_interaction(path: Path, query: str, emb: list[float], signal: str = "neutral") -> list[dict]:
    history = load_history(path)
    history.append({"ts": datetime.now(timezone.utc).isoformat(), "query": query,
                    "embedding": emb, "signal": signal, "reinforced": False})
    history = history[-max(LOOKBACK_INTERACTIONS * 2, 30):]
    save_history(path, history)
    return history

# ── Markdown memory helpers ───────────────────────────────────────────────────
def _ts() -> str: return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def append_memory(path: Path, entry: str) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(existing + f"\n\n<!-- ReflexLearn [{_ts()}] -->\n{entry}\n", encoding="utf-8")
    print("[ReflexLearn] MEMORY.md updated.")

def append_pending(path: Path, entry: str) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else \
        "# ReflexLearn Pending Reviews\n\nReview and approve these proposed updates.\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(existing + f"\n\n<!-- Pending [{_ts()}] -->\n{entry}\n", encoding="utf-8")
    print(f"[ReflexLearn] Pending update written to: {path}")

def upsert_soul_pattern(path: Path, key: str, value: str) -> None:
    content = path.read_text(encoding="utf-8") if path.exists() else ""
    header, bullet = "## ReflexLearn Patterns", f"- **{key}**: {value}"
    if header not in content:
        content = content.rstrip() + f"\n\n{header}\n{bullet}\n"
    else:
        pat = re.compile(r"(## ReflexLearn Patterns.*?)(- \*\*" + re.escape(key) + r"\*\*:.*?)(\n)", re.DOTALL)
        content = pat.sub(lambda m: m.group(1) + bullet + m.group(3), content) \
            if pat.search(content) else content.replace(header, f"{header}\n{bullet}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"[ReflexLearn] SOUL.md pattern updated: {key}")

# ── Core detection ────────────────────────────────────────────────────────────
def _slug(text: str) -> str: return re.sub(r"[^a-z0-9]+", "-", text.lower().strip())[:40].strip("-")
def _within_window(ts_str: str) -> bool:
    try: return (datetime.now(timezone.utc) - datetime.fromisoformat(ts_str)) <= timedelta(minutes=SESSION_WINDOW_MINUTES)
    except Exception: return True
def is_modifier_rephrase(query: str) -> bool: return bool(MODIFIER_PATTERNS.search(query))

def detect_repetition(emb: np.ndarray, history: list[dict]) -> Optional[dict]:
    lookback = history[-LOOKBACK_INTERACTIONS:]
    best_sim, best = 0.0, None
    for entry in lookback:
        s = cosine_sim(emb, np.array(entry["embedding"], dtype=np.float32))
        if s > best_sim: best_sim, best = s, entry
    return {"entry": best, "similarity": best_sim} if best_sim >= SIMILARITY_THRESHOLD else None

def count_recent_repeats(emb: np.ndarray, history: list[dict]) -> int:
    return sum(1 for e in history
        if cosine_sim(emb, np.array(e["embedding"], dtype=np.float32)) >= SIMILARITY_THRESHOLD
        and _within_window(e.get("ts", "")))

def detect_reinforcement(history: list[dict]) -> list[dict]:
    candidates, n = [], len(history)
    for i, entry in enumerate(history):
        if entry.get("reinforced") or i + POSITIVE_REINFORCEMENT_DELAY >= n: continue
        emb = np.array(entry["embedding"], dtype=np.float32)
        if not any(cosine_sim(emb, np.array(history[j]["embedding"], dtype=np.float32)) >= SIMILARITY_THRESHOLD
                   for j in range(i + 1, min(i + 1 + POSITIVE_REINFORCEMENT_DELAY, n))):
            candidates.append(entry)
    return candidates

# ── Writers ───────────────────────────────────────────────────────────────────
def _ollama_reflect(original: str, repeated: str, model: str) -> str:
    try:
        import urllib.request
        payload = json.dumps({"model": model, "stream": False, "prompt":
            f"An AI assistant gave an unsatisfying answer. The user asked again.\n"
            f"Original: {original}\nRepeated: {repeated}\n"
            f"In 2-3 sentences, identify what went wrong and suggest an improvement."
        }).encode("utf-8")
        req = urllib.request.Request("http://localhost:11434/api/generate", data=payload,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8")).get("response", "").strip()
    except Exception as exc:
        print(f"[ReflexLearn] Ollama unavailable ({exc}), using local reflection.")
        return (f"User repeated a similar query.\nOriginal: \"{original}\"\n"
                f"Repeated: \"{repeated}\"\n**Implication**: Previous answer was insufficient.")

def write_preference_extraction(mem: Path, pending: Path, soul: Path, query: str, original: str) -> None:
    modifier = MODIFIER_PATTERNS.search(query)
    modifier_text = modifier.group(0) if modifier else "style change"
    body = (f"User refined their query with: \"{modifier_text}\".\n"
            f"Original: \"{original}\"\nRefined: \"{query}\"\n"
            f"**Preference extracted**: User prefers responses with '{modifier_text}' "
            f"for this type of query.")
    append_memory(mem, f"### Preference Extraction: Intentional Refinement\n\n{body}")
    key = f"pref:{_slug(modifier_text)}"
    value = f"User prefers '{modifier_text}' style for queries like '{original[:50]}…'"
    if MODE == "aggressive":
        upsert_soul_pattern(soul, key, value)
    else:
        append_pending(pending,
            f"### Proposed Preference Update\n\n{body}\n\n"
            f"**Proposed SOUL.md entry**: `{key}`: {value}\n\n"
            f"To approve: move this entry to SOUL.md under `## ReflexLearn Patterns`.\n"
            f"To reject: delete this block.")
    print(f"[ReflexLearn] Preference extracted (modifier detected): {modifier_text}")

def write_reflection(mem: Path, pending: Path, soul: Path, original: str, repeated: str,
                     sim: float, use_ollama: bool = False, ollama_model: str = "llama3") -> str:
    if use_ollama:
        body = _ollama_reflect(original, repeated, ollama_model)
    else:
        body = (f"User repeated a similar query {REPEAT_COUNT_THRESHOLD}+ times "
                f"(similarity={sim:.3f}).\n"
                f"Original: \"{original}\"\nRepeated: \"{repeated}\"\n"
                f"**Implication**: The previous answer did not fully satisfy the user. "
                f"Review and improve the response style, completeness, or factual accuracy.")
    append_memory(mem, f"### Reflection: Answer Improvement Needed\n\n{body}\n\n"
                       f"**Action**: Update response strategy for queries similar to: \"{repeated}\"")
    key = f"improve:{_slug(repeated)}"
    value = (f"User repeated '{repeated[:60]}…' — previous answer was insufficient. "
             f"Prioritise completeness and clarity for this topic.")
    if MODE == "aggressive":
        upsert_soul_pattern(soul, key, value)
    else:
        append_pending(pending,
            f"### Proposed Improvement Update\n\n{body}\n\n"
            f"**Proposed SOUL.md entry**: `{key}`: {value}\n\n"
            f"To approve: move this entry to SOUL.md under `## ReflexLearn Patterns`.\n"
            f"To reject: delete this block.")
        print(f"[ReflexLearn] Cautious mode: update staged to pending file (not yet in SOUL.md).")
    return body

def write_reinforcement(mem: Path, soul: Path, entry: dict) -> None:
    q = entry["query"]
    append_memory(mem, f"### Reinforcement: Successful Pattern\n\n"
                       f"The answer to \"{q}\" was not repeated — the user was satisfied.\n"
                       f"**Action**: Strengthen this response pattern.")
    upsert_soul_pattern(soul, f"keep:{_slug(q)}",
        f"Answer to '{q[:60]}…' satisfied the user. Maintain this style/approach.")
    print(f"[ReflexLearn] Positive reinforcement written for: {q[:60]}")

# ── Slash commands ────────────────────────────────────────────────────────────
def handle_slash_command(cmd: str, hist: Path, pending: Path) -> bool:
    cmd = cmd.strip().lower()
    if cmd == "/reflex status":
        history = load_history(hist)
        print(f"[ReflexLearn] Status: {len(history)} interactions logged.")
        print(f"[ReflexLearn] Mode: {MODE} | Threshold: {SIMILARITY_THRESHOLD} | "
              f"Repeat threshold: {REPEAT_COUNT_THRESHOLD}")
        if pending.exists():
            lines = pending.read_text(encoding="utf-8").count("### Proposed")
            print(f"[ReflexLearn] Pending reviews: {lines} item(s) in {pending}")
        return True
    if cmd == "/reflex ignore-last":
        history = load_history(hist)
        if history:
            removed = history.pop()
            save_history(hist, history)
            print(f"[ReflexLearn] Removed last interaction: \"{removed.get('query', '')}\"")
        else:
            print("[ReflexLearn] No interactions to remove.")
        return True
    return False

# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    p = argparse.ArgumentParser(description="ReflexLearn v1.1.1 — OpenClaw continuous learning")
    p.add_argument("--query",        type=str, default=None)
    p.add_argument("--memory-file",  type=str, default=os.path.expanduser("~/.openclaw/MEMORY.md"))
    p.add_argument("--soul-file",    type=str, default=os.path.expanduser("~/.openclaw/SOUL.md"))
    p.add_argument("--history-file", type=str, default=os.path.expanduser("~/.openclaw/reflex_history.json"))
    p.add_argument("--pending-file", type=str, default=os.path.expanduser("~/.openclaw/reflexlearn-pending.md"))
    p.add_argument("--skill-md",     type=str, default=str(Path(__file__).parent / "SKILL.md"))
    p.add_argument("--use-ollama",   action="store_true")
    p.add_argument("--ollama-model", type=str, default="llama3")
    p.add_argument("--heartbeat",    action="store_true")
    p.add_argument("--offline",      action="store_true",
                   help="Abort if model weights are not already cached locally")
    args = p.parse_args()
    mem  = _validate_path(Path(args.memory_file))
    soul = _validate_path(Path(args.soul_file))
    hist = _validate_path(Path(args.history_file))
    pending = _validate_path(Path(args.pending_file))
    load_config(Path(args.skill_md))
    if args.heartbeat:
        print("[ReflexLearn] Heartbeat: scanning for reinforcement candidates…")
        history = load_history(hist)
        candidates = detect_reinforcement(history)
        if candidates:
            print(f"[ReflexLearn] Found {len(candidates)} reinforcement candidate(s).")
            for entry in candidates:
                write_reinforcement(mem, soul, entry); entry["reinforced"] = True
            save_history(hist, history)
        else:
            print("[ReflexLearn] No reinforcement candidates found.")
        return
    if not args.query: print("[ReflexLearn] No --query provided.", file=sys.stderr); sys.exit(0)
    if handle_slash_command(args.query, hist, pending): return
    query = args.query.strip()
    print(f"[ReflexLearn] Analysing query: \"{query}\"")
    emb: np.ndarray = _get_model(offline=args.offline).encode(query, convert_to_numpy=True)
    history = load_history(hist)
    hit = detect_repetition(emb, history)
    signal = "neutral"
    if hit:
        orig, sim = hit["entry"]["query"], hit["similarity"]
        if is_modifier_rephrase(query):
            m = MODIFIER_PATTERNS.search(query)
            print(f"[ReflexLearn] Modifier detected (\"{m.group(0)}\") → preference extraction.")
            write_preference_extraction(mem, pending, soul, query, orig)
            signal = "preference"
        else:
            repeat_count = count_recent_repeats(emb, history)
            print(f"[ReflexLearn] Repeat #{repeat_count}/{REPEAT_COUNT_THRESHOLD} (sim={sim:.4f})")
            if repeat_count >= REPEAT_COUNT_THRESHOLD:
                print(f"[ReflexLearn] *** FAILURE SIGNAL *** orig=\"{orig[:50]}\" repeated=\"{query[:50]}\"")
                reflection = write_reflection(mem, pending, soul, orig, query, sim,
                                              args.use_ollama, args.ollama_model)
                print(f"[ReflexLearn] Reflection written.")
                signal = "negative"
            else:
                print(f"[ReflexLearn] Watching — need {REPEAT_COUNT_THRESHOLD} repeats to flag. Logging only.")
                signal = "watching"
    else:
        print("[ReflexLearn] No repetition detected.")
    append_interaction(hist, query, emb.tolist(), signal)
    print(f"[ReflexLearn] Interaction logged (signal={signal}).")
if __name__ == "__main__":
    main()
