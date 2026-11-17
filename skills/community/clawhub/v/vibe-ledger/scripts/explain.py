"""explain.json: the agent's per-file explanations, checked against the code.

Function names must really be defined in the file, backticked identifiers in a
purpose must exist in the project, and history quotes must be in the conversations."""
from __future__ import annotations

import copy
import re
from pathlib import Path

import areas
from common import is_within, read_text
from graph import strip_comments
from verify import check_transcript

TOLERANCE = 3
_ID = r"[A-Za-z_$][\w$]*"
_MODS = r"(?:(?:public|private|protected|static|readonly|async|override|abstract|declare|get|set)[ \t]+)*"
JS_DEFS = [
    re.compile(rf"^[ \t]*(?:export[ \t]+)?(?:default[ \t]+)?(?:async[ \t]+)?function\b[ \t]*\*?[ \t]*({_ID})", re.M),
    re.compile(rf"^[ \t]*(?:export[ \t]+)?(?:default[ \t]+)?(?:abstract[ \t]+)?class[ \t]+({_ID})", re.M),
]
# a name that is given a value: it is a definition only when that value is a function (see _is_function_value)
VALUE_HEADS = [
    # the type annotation (`: React.FC<{…}>`, possibly over several lines) is skipped by _after_assign
    re.compile(rf"^[ \t]*(?:export[ \t]+)?(?:declare[ \t]+)?(?:const|let|var)[ \t]+({_ID})[ \t]*(?=[:=])", re.M),
    re.compile(rf"^[ \t]*({_ID})[ \t]*:(?!:)", re.M),  # object member
    re.compile(rf"^[ \t]*{_MODS}({_ID})[ \t]*(?::[^=\n]+)?=(?![=>])", re.M),  # class property
]
_FN_START = re.compile(rf"\s*(?:async[ \t]*)?(?:function\b|{_ID}[ \t]*=>)")
_FN_WRAPPER = re.compile(r"\s*(?:React\.)?(?:useCallback|memo|forwardRef|useEvent|debounce|throttle)[ \t]*\(")
_ARROW_PARAMS = re.compile(r"\s*(?:async[ \t]*)?(?:<[^>\n]*>[ \t]*)?\(")
_ARROW_TAIL = re.compile(r"\s*=>")
# a method: (modifiers) name<T>(params, maybe over several lines) (: ReturnType)? {
METHOD_HEAD = re.compile(rf"^[ \t]*{_MODS}\*?[ \t]*({_ID})[ \t]*(?:<[^>\n]*>)?[ \t]*\(", re.M)
METHOD_BODY = re.compile(r"\s*(?::[^;{=]+)?\{")
PY_DEFS = [re.compile(r"^[ \t]*(?:async[ \t]+)?def[ \t]+([A-Za-z_]\w*)[ \t]*\(", re.M),
           re.compile(r"^[ \t]*class[ \t]+([A-Za-z_]\w*)", re.M)]
NOT_A_DEFINITION = {"if", "for", "while", "switch", "catch", "function", "return", "with", "else", "do", "try"}
BACKTICK = re.compile(r"`([^`\n]+)`")
IDENT_TOKEN = re.compile(rf"^{_ID}(?:\.{_ID})*$")
FILE_TOKEN = re.compile(r"^[\w./-]+\.(?:js|jsx|ts|tsx|mjs|cjs|vue|svelte|py|json|html|css)$")


class ExplainError(Exception):
    def __init__(self, problems: list[str]):
        super().__init__("\n".join(problems))
        self.problems = problems


def validate(doc) -> None:
    if not isinstance(doc, dict):
        raise ExplainError(["explain.json must be a JSON object"])
    p: list[str] = []
    ev = doc.get("evidence", {})
    if not isinstance(ev, dict):
        p.append("evidence: must be an object")
        ev = {}
    for eid, e in ev.items():
        if not isinstance(e, dict) or e.get("kind") != "transcript":
            p.append(f"evidence {eid}: kind must be transcript")
            continue
        for f in ("session", "msg_id", "quote"):
            if f not in e:
                p.append(f"evidence {eid}: missing {f}")
    files = doc.get("files")
    if not isinstance(files, dict):
        raise ExplainError(p + ["files: must be an object mapping file paths to explanations"])
    for path, entry in files.items():
        where = f"file {path}"
        if not isinstance(entry, dict):
            p.append(f"{where}: must be an object")
            continue
        if not isinstance(entry.get("purpose_plain"), str) or not entry.get("purpose_plain", "").strip():
            p.append(f"{where}: purpose_plain must be a non-empty string")
        if not isinstance(entry.get("purpose_dev", ""), str):
            p.append(f"{where}: purpose_dev must be a string")
        for fn in entry.get("functions", []):
            if not isinstance(fn, dict) or not isinstance(fn.get("name"), str) or not isinstance(fn.get("plain"), str):
                p.append(f"{where}: each function needs a name and a plain sentence")
            elif not isinstance(fn.get("line"), int):
                p.append(f"{where} function {fn['name']}: line must be an integer")
        for h in entry.get("history", []):
            if not isinstance(h, dict) or not isinstance(h.get("plain"), str) or not isinstance(h.get("evidence"), list):
                p.append(f"{where}: each history item needs plain and an evidence list")
                continue
            for i in h["evidence"]:
                if i not in ev:
                    p.append(f"{where} history: unknown evidence id {i}")
    p += _journey_problems(doc.get("journeys", []))
    p += areas.problems(doc)
    if p:
        raise ExplainError(p)


def _journey_problems(journeys) -> list[str]:
    if not isinstance(journeys, list):
        return ["journeys: must be a list"]
    p = []
    for n, j in enumerate(journeys, 1):
        where = f"journey #{n}"
        if not isinstance(j, dict):
            p.append(f"{where}: must be an object")
            continue
        if not isinstance(j.get("title"), str) or not j.get("title", "").strip():
            p.append(f"{where}: title must be a non-empty string (what the user does, e.g. \"你点「分析」时\")")
        if not isinstance(j.get("outcome", ""), str):
            p.append(f"{where}: outcome must be a string")
        steps = j.get("steps")
        if not isinstance(steps, list) or len(steps) < 2:
            p.append(f"{where}: needs at least 2 steps")
            continue
        for k, st in enumerate(steps, 1):
            if not isinstance(st, dict) or not isinstance(st.get("file"), str):
                p.append(f"{where} step {k}: needs a file")
            elif not isinstance(st.get("plain"), str) or not st["plain"].strip():
                p.append(f"{where} step {k}: plain must be a non-empty sentence")
            elif "function" in st and (not isinstance(st["function"], str) or not isinstance(st.get("line"), int)):
                p.append(f"{where} step {k}: a function needs its name and an integer line")
    return p


def find_definitions(text: str, lang: str) -> dict[str, list[int]]:
    clean = strip_comments(text, lang)
    found: dict[str, set] = {}
    for rx in (PY_DEFS if lang == "py" else JS_DEFS):
        for m in rx.finditer(clean):
            name = m.group(1)
            if name in NOT_A_DEFINITION:
                continue
            found.setdefault(name, set()).add(clean.count("\n", 0, m.start(1)) + 1)
    if lang != "py":
        for i, rx in enumerate(VALUE_HEADS):
            for m in rx.finditer(clean):
                # only `const|let|var name` stops before its `: Type =`; the others end past their `:`/`=`
                start = _after_assign(clean, m.end()) if i == 0 else m.end()
                if start > 0 and m.group(1) not in NOT_A_DEFINITION and _is_function_value(clean, start):
                    found.setdefault(m.group(1), set()).add(clean.count("\n", 0, m.start(1)) + 1)
        for m in METHOD_HEAD.finditer(clean):  # a call such as doThing(1); is not followed by a body
            name, close = m.group(1), _closing_paren(clean, m.end() - 1)
            if name not in NOT_A_DEFINITION and close > 0 and METHOD_BODY.match(clean, close + 1):
                found.setdefault(name, set()).add(clean.count("\n", 0, m.start(1)) + 1)
    return {name: sorted(lines) for name, lines in found.items()}


_OPEN, _CLOSE = "([{<", ")]}>"


def _skip_type(text: str, pos: int, stop: str) -> int:
    """From a `:` at text[pos], skip a TypeScript type — brackets and generics matched, so it may span
    lines and hold `{a: number; b = …}` or `(e: E) => void` — and return the index of the first
    top-level `=` (stop="=", not `==`/`=>`) or `=>` (stop="=>"), or -1."""
    depth, j, end = 0, pos + 1, min(len(text), pos + 4000)
    while j < end:
        if text.startswith("=>", j):
            if depth == 0 and stop == "=>":
                return j
            j += 2
            continue
        c = text[j]
        if c in _OPEN:
            depth += 1
        elif c in _CLOSE:
            if depth == 0:
                return -1
            depth -= 1
        elif depth == 0 and c == ";":
            return -1
        elif depth == 0 and c == "=" and stop == "=" and not text.startswith("==", j):
            return j
        j += 1
    return -1


def _after_assign(text: str, pos: int) -> int:
    """Index just after the `=` of `name[: Type] =` whose name ends at text[pos], or -1."""
    j = pos
    while j < len(text) and text[j] in " \t":
        j += 1
    if j < len(text) and text[j] == ":":
        j = _skip_type(text, j, "=")
        if j < 0:
            return -1
    if text.startswith("=", j) and not text.startswith(("==", "=>"), j):
        return j + 1
    return -1


def _is_function_value(text: str, pos: int) -> bool:
    """Whether the value starting at text[pos] is a function: `function`, `x =>`, `(…) =>` (brackets matched,
    so a parenthesised expression or a call with a callback does not count), or a function wrapper."""
    if _FN_START.match(text, pos) or _FN_WRAPPER.match(text, pos):
        return True
    m = _ARROW_PARAMS.match(text, pos)
    if not m:
        return False
    close = _closing_paren(text, m.end() - 1)
    if close < 0:
        return False
    after = close + 1
    while after < len(text) and text[after] in " \t\r\n":
        after += 1
    if text.startswith(":", after):  # a return type, possibly an object type over several lines
        return _skip_type(text, after, "=>") > 0
    return bool(_ARROW_TAIL.match(text, after))


def _closing_paren(text: str, i: int) -> int:
    """Index of the ")" matching the "(" at text[i], or -1 (parameter lists may span lines)."""
    depth = 0
    for j in range(i, min(len(text), i + 4000)):
        if text[j] == "(":
            depth += 1
        elif text[j] == ")":
            depth -= 1
            if depth == 0:
                return j
    return -1


def _identifiers(text: str):
    for raw in BACKTICK.findall(text or ""):
        tok = raw.strip()
        tok = tok[:-2] if tok.endswith("()") else tok
        if FILE_TOKEN.match(tok):
            yield ("file", tok)
        elif IDENT_TOKEN.match(tok):
            yield ("ident", tok)
        # anything else (a command, a phrase) is not a name to check


def _exists(kind: str, tok: str, corpus: str, paths: set, labels: set, root: Path) -> bool:
    if kind == "file":
        on_disk = (root / tok).is_file() and is_within(root / tok, root)  # manifest.json, vendor/… are not graph nodes
        return on_disk or tok in paths or tok in labels or any(p.endswith("/" + tok) for p in paths)
    return re.search(r"(?<![\w$])" + re.escape(tok) + r"(?![\w$])", corpus) is not None


def _check_function(name: str, line: int, defs: dict) -> tuple[dict | None, str]:
    """(where the definition really is, "") or (None, why it was dropped)."""
    lines = defs.get(name, [])
    near = [n for n in lines if abs(n - line) <= TOLERANCE]
    if near:
        return {"line": min(near, key=lambda n: abs(n - line)), "line_corrected": False}, ""
    if len(lines) == 1:
        return {"line": lines[0], "line_corrected": True}, ""
    if lines:
        return None, f"defined {len(lines)} times in the file and none is within {TOLERANCE} lines of line {line}"
    return None, "not defined in this file"


def _verify_journeys(journeys: list, g: dict, root: Path, defs_of) -> tuple[list, list]:
    paths = {n["id"] for n in g["nodes"]}
    linked = {(e["from"], e["to"]) for e in g["edges"]}
    kept, rejected = [], []
    for j in journeys:
        steps, dropped = [], []
        for st in j["steps"]:
            if st["file"] not in paths:
                dropped.append({"file": st["file"], "reason": "not a file in the graph"})
                continue
            step = {"file": st["file"], "plain": st["plain"]}
            if "function" in st:
                where, why = _check_function(st["function"], st["line"], defs_of(st["file"]))
                if where:
                    step.update(function=st["function"], **where)
                else:
                    step["dropped_function"] = {"name": st["function"], "reason": why}
            if steps:
                # a step joins the most recent earlier step it really connects to — the same file, or an import
                # either way: a page that calls three helpers in turn links each of them back to the page
                for i in range(len(steps) - 1, -1, -1):
                    prev = steps[i]["file"]
                    if prev == st["file"] or (prev, st["file"]) in linked or (st["file"], prev) in linked:
                        step["linked"], step["from"] = True, i
                        break
                else:
                    step["linked"] = False
            steps.append(step)
        if len(steps) < 2:
            rejected.append({"title": j["title"], "reason": "fewer than 2 steps are files in the graph"})
            continue
        kept.append({"id": f"J{len(kept) + 1}", "title": j["title"], "outcome": j.get("outcome", ""),
                     "steps": steps, "dropped_steps": dropped})
    return kept, rejected


def verify(doc: dict, g: dict, root, index: dict) -> dict:
    validate(doc)
    root = Path(root).resolve()
    out = copy.deepcopy(doc)
    out.setdefault("evidence", {})
    for e in out["evidence"].values():
        e.update(check_transcript(e, index))
    paths = {n["id"] for n in g["nodes"]}
    labels = {n["label"] for n in g["nodes"]}
    corpus = "\n".join(read_text(root / p) for p in sorted(paths))
    cache: dict[str, dict] = {}

    def defs_of(path: str) -> dict:
        if path not in cache:
            cache[path] = find_definitions(read_text(root / path), "py" if path.endswith(".py") else "js")
        return cache[path]

    files, rejected = {}, []
    for path, entry in out["files"].items():
        if path not in paths:
            rejected.append({"path": path, "reason": "not a file in the graph"})
            continue
        defs = defs_of(path)
        kept, dropped = [], []
        for fn in entry.get("functions", []):
            where, why = _check_function(fn["name"], fn["line"], defs)
            if where:
                kept.append({**fn, **where})
            else:
                dropped.append({"name": fn["name"], "reason": why})
        missing = sorted({tok for text in (entry.get("purpose_plain", ""), entry.get("purpose_dev", ""))
                          for kind, tok in _identifiers(text) if not _exists(kind, tok, corpus, paths, labels, root)})
        history = []
        for h in entry.get("history", []):
            ok_ids = [i for i in h["evidence"] if out["evidence"].get(i, {}).get("ok")]
            if ok_ids:
                history.append({**h, "evidence": ok_ids})
        files[path] = {**entry, "ok": True, "functions": kept, "dropped_functions": dropped,
                       "purpose_unverified": bool(missing), "missing_identifiers": missing, "history": history}
    out["files"] = files
    out["rejected"] = rejected
    out["journeys"], out["rejected_journeys"] = _verify_journeys(out.get("journeys", []), g, root, defs_of)
    out["function_map"] = areas.verify(out, g, root)
    out["verification"] = {
        "journeys": len(out["journeys"]), "journeys_rejected": len(out["rejected_journeys"]),
        "journey_steps_dropped": sum(len(j["dropped_steps"]) for j in out["journeys"]),
        "unlinked_steps": sum(1 for j in out["journeys"] for st in j["steps"] if st.get("linked") is False),
        "files": len(files), "rejected": len(rejected),
        "functions_dropped": sum(len(f["dropped_functions"]) for f in files.values()),
        "unverified_purposes": sum(1 for f in files.values() if f["purpose_unverified"]),
        "evidence_failed": [{"id": k, "reason": e.get("reason", "")} for k, e in out["evidence"].items() if not e.get("ok")],
    }
    return out


def merge(parts: list[dict]) -> dict:
    out: dict = {"evidence": {}, "files": {}, "duplicates": [], "journeys": []}
    for n, part in enumerate(parts, 1):
        validate(part)
        pre = f"p{n}_"
        for eid, e in part.get("evidence", {}).items():
            out["evidence"][pre + eid] = copy.deepcopy(e)
        for path, entry in part["files"].items():
            if path in out["files"]:
                out["duplicates"].append(path)
                continue
            e = copy.deepcopy(entry)
            e["history"] = [{**h, "evidence": [pre + i for i in h["evidence"]]} for h in e.get("history", [])]
            out["files"][path] = e
        titles = {j["title"] for j in out["journeys"]}
        out["journeys"] += [copy.deepcopy(j) for j in part.get("journeys", []) if j["title"] not in titles]
    validate(out)
    return out


def summary_lines(verified: dict) -> list[str]:
    v = verified["verification"]
    lines = [f"Explanations: {v['files']} files kept, {v['rejected']} rejected"]
    lines += [f"  ✗ {r['path']}: {r['reason']}" for r in verified["rejected"]]
    lines.append(f"Functions dropped: {v['functions_dropped']}")
    for path, f in verified["files"].items():
        lines += [f"  - {path}: {d['name']} — {d['reason']}" for d in f["dropped_functions"]][:20]
    lines.append(f"Purposes marked unverified: {v['unverified_purposes']}")
    for path, f in verified["files"].items():
        if f["purpose_unverified"]:
            lines.append(f"  - {path}: not found in the project: {', '.join(f['missing_identifiers'])}")
    lines += [f"  ✗ evidence {x['id']}: {x['reason']}" for x in v["evidence_failed"]]
    lines.append(f"Journeys: {v['journeys']} kept, {v['journeys_rejected']} rejected; "
                 f"{v['journey_steps_dropped']} steps dropped; {v['unlinked_steps']} links not found in the imports (drawn dashed)")
    lines += [f"  ✗ {r['title']}: {r['reason']}" for r in verified["rejected_journeys"]]
    for j in verified["journeys"]:
        lines += [f"  - {j['title']}: dropped {d['file']} — {d['reason']}" for d in j["dropped_steps"]]
        lines += [f"  - {j['title']}: {st['file']} {st['dropped_function']['name']} — {st['dropped_function']['reason']}"
                  for st in j["steps"] if "dropped_function" in st]
    return lines + areas.summary_lines(verified.get("function_map"))
