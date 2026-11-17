#!/usr/bin/env python3
"""Agent defense-in-depth score: validate an authored scorecard and render every output from it.

One authored file (scorecard.json) is the single source of truth. This script checks it,
computes scores, and renders:
  - the score table (stdout, default)
  - the website entry (--entry FILE): the website record for this agent, schema/entry.schema.json
  - the full markdown report (--report FILE)
  - the criteria catalog (--catalog): data/criteria.json for the website

Usage:
  python3 score.py --example > scorecard.json            # authoring template
  python3 score.py scorecard.json --repo /path/to/clone  # validate (incl. citations) + table
  python3 score.py scorecard.json --repo /path/to/clone --entry entry.json --report report.md
  python3 score.py --catalog > criteria.json

--repo checks that HEAD equals pinned_commit and that every cited file exists with the cited
line range in bounds. Always pass it when the clone is available.

Rules enforced: evidence on every parameter; 'inferred' <= L2; C and D at most one level
above S; caps known and on the right criterion, each with a reason; an 'alt' mechanism always
gets G1 and the criterion keeps the higher score; SA needs a search evidence item.
See references/output-format.md for every authored field.
"""
import json
import os
import re
import subprocess
import sys

SCHEMA_VERSION = "2.0"
SCORECARD_VERSION = "0.9"
WEIGHTS = {"S": 0.30, "C": 0.30, "D": 0.20, "B": 0.20}
PARAM_NAMES = {"S": "Strength", "C": "Coverage", "D": "Default & tamper-resistance", "B": "Blast radius"}
FRACTION = {0: 0.0, 1: 0.25, 2: 0.5, 3: 0.75, 4: 1.0}

CRITERIA = [
    ("C1", "Identity & least privilege",
     "Does the agent act with an identity scoped to its job, with authority checked per request rather than inherited?",
     ["ASI03", "T3", "T9"]),
    ("C2", "Approval gates",
     "Do consequential actions require a human's informed approval by default, with no path around the gate?",
     ["ASI09", "ASI02", "T10", "T15"]),
    ("C3", "Tool & action scoping",
     "Is each tool the narrowest thing that does its job, with arguments validated in code against allowlists and bounds?",
     ["ASI02", "T2", "LLM06"]),
    ("C4", "Code-execution isolation",
     "When model-influenced code runs, does a boundary the model cannot redefine contain it on every path?",
     ["ASI05", "T11", "LLM05"]),
    ("C5", "Untrusted input blast radius",
     "When the agent reads untrusted content, what limits how far that content can steer it?",
     ["ASI01", "ASI09", "ASI07", "T6", "T12", "T15", "LLM01"]),
    ("C6", "Memory, context & configuration integrity",
     "Can anything the agent reads persist into future behaviour through memory, retrieval, or auto-loaded files, and is that path controlled?",
     ["ASI06", "T1", "T5", "LLM04", "LLM08"]),
    ("C7", "Third-party extensions",
     "Are plugins, MCP servers and downloaded tools verified or isolated before they run with the agent's access?",
     ["ASI04", "T17", "LLM03"]),
    ("C8", "Secrets & sensitive-data protection",
     "Are credentials and sensitive data kept out of logs, telemetry, subprocesses, and the model provider?",
     ["ASI03", "LLM02", "T9"]),
    ("C9", "Audit & traceability",
     "Can you reconstruct what the agent did, for whom, and who approved it, from a record the agent couldn't alter?",
     ["T8", "ASI10"]),
    ("C10", "Limits & kill switch",
     "Are there hard limits on steps, time, and cost, and does stopping the agent actually stop everything?",
     ["ASI08", "ASI10", "T4", "LLM10"]),
]
CRIT = {c[0]: {"name": c[1], "question": c[2], "owasp": c[3], "number": i + 1} for i, c in enumerate(CRITERIA)}

OPT_IN, CRITICAL_GAP = 0.50, 0.25
CAPS = {  # id -> (max, criterion or None for global)
    "G1": (OPT_IN, None), "G2": (CRITICAL_GAP, None),
    "C1-SELFESC": (CRITICAL_GAP, "C1"), "C1-PASSTHRU": (CRITICAL_GAP, "C1"),
    "C2-SELFAPPROVE": (CRITICAL_GAP, "C2"), "C2-POWERBYPASS": (CRITICAL_GAP, "C2"),
    "C4-HOSTROOT": (CRITICAL_GAP, "C4"),
    "C5-WORSTCASE": (CRITICAL_GAP, "C5"), "C5-PUBLICTRIGGER": (CRITICAL_GAP, "C5"),
    "C6-REPOCONFIG": (CRITICAL_GAP, "C6"), "C7-RCELOAD": (CRITICAL_GAP, "C7"), "C8-MODELSECRETS": (CRITICAL_GAP, "C8"),
}
BANDS = [(8.5, "hardened", "Hardened", "green"), (7.0, "strong", "Strong", "green"),
         (5.0, "moderate", "Moderate", "amber"), (0.0, "weak", "Minimal", "red")]
CATEGORY_INFO = [  # (id, display label, what belongs), in the order the website lists them
    ("agent_frameworks", "Agent Frameworks",
     "Libraries and platforms for building agents, including low-code agent builders."),
    ("ai_assistants", "AI Assistants",
     "General and personal assistants, browser and computer-use agents, research agents, and email/calendar/docs agents."),
    ("coding", "Coding",
     "Coding CLIs, IDE agents, autonomous software engineers, code-review bots, and git/GitHub tool servers."),
    ("cybersecurity", "Cybersecurity",
     "Penetration-testing agents, SOC and alert triage, threat investigation, and cloud configuration auditing."),
    ("data_analytics", "Data & Analytics",
     "SQL and BI agents, data-science agents, and database or data-warehouse tool servers."),
    ("infrastructure_ops", "Infrastructure & Ops",
     "SRE, incident response, Kubernetes, cloud operations, infrastructure-as-code, and observability agents."),
]
CATEGORIES = [c[0] for c in CATEGORY_INFO]
CATEGORY_RULES = [
    "Category is the domain the agent acts on, judged from its primary documented use.",
    "Security beats infrastructure when the agent's job is finding or stopping threats.",
    "Domain beats generality for tool servers: a GitHub server is Coding, a Postgres server is Data & Analytics.",
    "Libraries and platforms for building agents are Agent Frameworks, even if they ship example agents.",
    "Truly general-purpose agents and general tool servers (filesystem, browser) are AI Assistants.",
]
CAPABILITIES = ["code_execution", "filesystem_write", "network_egress", "external_credentials", "persistent_memory",
                "untrusted_input", "third_party_extensions", "sub_agents", "external_communication"]
CRITICAL_B_CRITERIA = {"C1", "C4", "C5", "C7"}
SAFE_SOURCES = ("default", "opt_in", "operator")


class Problems:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


# ---------------------------------------------------------------- evidence

_REQUIRED_SEEN = set()


def require_contains(items, where, P, why):
    for i, ev in enumerate(items or []):
        key = (where, i)
        if isinstance(ev, dict) and "file" in ev and not ev.get("contains") and key not in _REQUIRED_SEEN:
            _REQUIRED_SEEN.add(key)
            P.err(f"{where}.evidence[{i}]: 'contains' is required here ({why}) - quote a short literal from the cited lines")


def check_evidence(items, where, P, repo=None, need_search=False):
    """Validate an evidence list in place. Returns True if it contains a search item."""
    if not isinstance(items, list) or not items:
        P.err(f"{where}: evidence must be a non-empty list")
        return False
    has_search = False
    for i, ev in enumerate(items):
        tag = f"{where}.evidence[{i}]"
        if not isinstance(ev, dict):
            P.err(f"{tag}: must be an object")
            continue
        if "file" in ev:
            extra = set(ev) - {"file", "lines", "note", "contains"}
            if extra:
                P.err(f"{tag}: unexpected keys {sorted(extra)}")
            f, lines = ev.get("file", ""), str(ev.get("lines", ""))
            if not f or f.startswith("/") or f.startswith("./"):
                P.err(f"{tag}: file must be repo-relative from the repository root, got {f!r}")
            m = re.fullmatch(r"(\d+)(?:-(\d+))?", lines)
            if not m:
                P.err(f"{tag}: lines must be 'N' or 'N-M', got {lines!r}")
                continue
            a, b = int(m.group(1)), int(m.group(2) or m.group(1))
            if a < 1 or b < a:
                P.err(f"{tag}: bad line range {lines!r}")
            if repo and f:
                path = os.path.join(repo, f)
                if not os.path.isfile(path):
                    P.err(f"{tag}: cited file does not exist in the repo: {f}")
                else:
                    with open(path, "r", encoding="utf-8", errors="replace") as fh:
                        file_lines = fh.read().split("\n")
                    n = len(file_lines) - (1 if file_lines and file_lines[-1] == "" else 0)
                    if b > n:
                        P.err(f"{tag}: {f} has {n} lines; cited {lines}")
                    elif ev.get("contains"):
                        span = "\n".join(file_lines[a - 1:b])
                        if ev["contains"] not in span:
                            P.err(f"{tag}: {f}:{lines} does not contain {ev['contains']!r} - wrong lines?")
        elif "search" in ev:
            extra = set(ev) - {"search", "scope", "hits", "note"}
            if extra:
                P.err(f"{tag}: unexpected keys {sorted(extra)}")
            if not ev.get("search") or not ev.get("scope") or not isinstance(ev.get("hits"), int):
                P.err(f"{tag}: search evidence needs 'search', 'scope', and integer 'hits'")
            elif repo:
                recheck_search(ev, tag, P, repo)
            has_search = True
        else:
            P.err(f"{tag}: needs either file+lines or search+scope+hits")
    if need_search and not has_search:
        P.err(f"{where}: structural absence needs at least one search evidence item")
    return has_search


def recheck_search(ev, tag, P, repo):
    """Re-run an 'rg ...' search (no shell) over its scope and compare the matching-line count."""
    import shlex
    try:
        argv = shlex.split(ev["search"])
        scope = shlex.split(ev["scope"])
    except ValueError:
        P.warn(f"{tag}: could not parse search/scope for re-check")
        return
    if not argv or argv[0] != "rg" or any(a in ("--pre", "--pre-glob") for a in argv):
        return  # only plain ripgrep searches are re-run
    paths = [x for x in scope if os.path.exists(os.path.join(repo, x))]
    if not paths:
        P.warn(f"{tag}: search scope {ev['scope']!r} not found in repo; hits not re-checked")
        return
    try:
        r = subprocess.run(argv + paths, cwd=repo,
                           capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        P.warn(f"{tag}: could not re-run search ({e})")
        return
    if r.returncode not in (0, 1):
        P.warn(f"{tag}: search failed to run: {r.stderr.strip()[:160]}")
        return
    n = len([ln for ln in r.stdout.splitlines() if ln.strip()])
    if n != ev["hits"]:
        P.err(f"{tag}: re-ran search, got {n} matching lines, scorecard says {ev['hits']} - record the true count and explain irrelevant hits in 'note'")


def permalink(repo_url, commit, ev):
    m = re.match(r"https://github\.com/([^/]+)/([^/#?]+?)(?:\.git)?/?$", repo_url or "")
    if not m or "file" not in ev:
        return None
    a, _, b = ev["lines"].partition("-")
    frag = f"#L{a}" + (f"-L{b}" if b else "")
    return f"https://github.com/{m.group(1)}/{m.group(2)}/blob/{commit}/{ev['file']}{frag}"


# ---------------------------------------------------------------- scoring

def score_mechanism(cid, params, caps, label, P, repo, kind):
    tag = f"{cid}{'' if kind == 'default' else ' (alt)'}"
    if not isinstance(params, dict):
        P.err(f"{tag}: 'parameters' object with S, C, D, B is required")
        return None
    out, raw, inferred = {}, 0.0, 0
    for p, w in WEIGHTS.items():
        e = params.get(p)
        if not isinstance(e, dict):
            P.err(f"{tag}.{p}: missing")
            continue
        lvl, sa = e.get("level"), bool(e.get("structural_absence"))
        if lvl == "SA":
            lvl, sa = 4, True
        if lvl not in FRACTION:
            P.err(f"{tag}.{p}: level must be 0-4 or 'SA', got {lvl!r}")
            continue
        if sa and lvl != 4:
            P.err(f"{tag}.{p}: structural_absence requires level 4")
        status = str(e.get("status", "")).lower()
        if status not in ("verified", "inferred"):
            P.err(f"{tag}.{p}: status must be 'verified' or 'inferred'")
        if status == "inferred":
            inferred += 1
            if lvl > 2:
                P.err(f"{tag}.{p}: 'inferred' evidence cannot support a level above L2")
        if not str(e.get("finding", "")).strip():
            P.err(f"{tag}.{p}: 'finding' (one sentence) is required")
        check_evidence(e.get("evidence"), f"{tag}.{p}", P, repo, need_search=sa)
        if lvl >= 3 and not sa:
            require_contains(e.get("evidence"), f"{tag}.{p}", P, f"supports L{lvl}")
        cap_ids = {c.get("id") for c in caps or [] if isinstance(c, dict)}
        if cap_ids - {"G1"} or ("G1" in cap_ids and p == "D"):
            require_contains(e.get("evidence"), f"{tag}.{p}", P, "criterion has a cap")
        if lvl < 4 and not sa and not str(e.get("gap", "")).strip():
            P.warn(f"{tag}.{p}: below L4 without a 'gap' - name what the next level requires")
        extra = set(e) - {"level", "status", "finding", "evidence", "structural_absence", "gap"}
        if extra:
            P.err(f"{tag}.{p}: unexpected keys {sorted(extra)}")
        pts = round(w * FRACTION[lvl], 4)
        raw += pts
        out[p] = {"level": lvl, "structural_absence": sa, "status": status, "finding": e.get("finding", ""),
                  **({"gap": e["gap"]} if e.get("gap") else {}),
                  "evidence": e.get("evidence", []), "weight": w, "points": pts}
    if len(out) < 4:
        return None
    s = out["S"]
    if not s["structural_absence"]:
        for p in ("C", "D"):
            if not out[p]["structural_absence"] and out[p]["level"] > s["level"] + 1:
                P.err(f"{tag}.{p}: L{out[p]['level']} exceeds S (L{s['level']}) by more than one level - "
                      f"lower {p} to L{s['level'] + 1}")
    caps = list(caps or [])
    if (cid == "C5" and kind == "default" and out["B"]["level"] == 0 and not out["B"]["structural_absence"]
            and not any(isinstance(c, dict) and c.get("id") == "C5-WORSTCASE" for c in caps)):
        caps.append({"id": "C5-WORSTCASE",
                     "reason": "Worst case (B L0): a hijacked agent can leak data and take irreversible actions unattended."})
    cap = None
    for c in caps or []:
        if not isinstance(c, dict) or c.get("id") not in CAPS:
            P.err(f"{tag}: unknown or malformed cap {c!r}")
            continue
        if not str(c.get("reason", "")).strip():
            P.err(f"{tag}: cap {c['id']} needs a 'reason'")
        mx, scope = CAPS[c["id"]]
        if scope and scope != cid:
            P.err(f"{tag}: cap {c['id']} only applies to {scope}")
            continue
        if cap is None or mx < cap["max"]:
            cap = {"id": c["id"], "max": mx, "reason": c.get("reason", "")}
    if (kind == "default" and s["level"] >= 1 and out["D"]["level"] == 0
            and not any(isinstance(c, dict) and c.get("id") == "G1" for c in caps or [])):
        P.warn(f"{tag}: a mechanism exists (S=L{s['level']}) but D is L0 - if it is opt-in, add cap G1")
    raw = round(raw, 4)
    score = round(min(raw, cap["max"]) if cap else raw, 3)
    conf = "high" if inferred == 0 else ("medium" if inferred <= 2 else "low")
    return {"kind": kind, "label": label, "score": score, "raw": round(raw, 3), "cap": cap,
            "confidence": conf, "parameters": out}


def band(total):
    for floor, bid, label, color in BANDS:
        if total >= floor - 1e-9:
            return {"id": bid, "label": label, "color": color}
    return {"id": "weak", "label": "Minimal", "color": "red"}


def check_safe_setup(ss, P, repo=None):
    """Validate the optional 'safe_setup' section (SKILL.md step 6). It never affects a score."""
    if not isinstance(ss, dict):
        P.err("safe_setup must be an object")
        return
    for k in set(ss) - {"intro", "steps", "approving", "handling"}:
        P.err(f"safe_setup: unexpected key '{k}'")
    intro = str(ss.get("intro", "")).strip()
    if not intro:
        P.err("safe_setup.intro is required (1-3 sentences on what already ships protected)")
    elif len(re.findall(r"[.!?](?:\s|$)", intro)) > 3:
        P.warn("safe_setup.intro: keep it to 1-3 sentences")
    steps = ss.get("steps")
    if not isinstance(steps, list) or not 2 <= len(steps) <= 8:
        P.err("safe_setup.steps must be a list of 2-8 steps")
        steps = steps if isinstance(steps, list) else []
    for i, st in enumerate(steps):
        tag = f"safe_setup.steps[{i}]"
        if not isinstance(st, dict):
            P.err(f"{tag}: must be an object")
            continue
        for k in set(st) - {"setup", "how", "gives_you", "criterion", "source", "evidence"}:
            P.err(f"{tag}: unexpected key '{k}'")
        for k in ("setup", "how", "gives_you"):
            if not str(st.get(k, "")).strip():
                P.err(f"{tag}: '{k}' is required")
        if st.get("criterion") not in CRIT:
            P.err(f"{tag}: criterion must be one of C1..C10 (the finding this step comes from)")
        if st.get("source") not in SAFE_SOURCES:
            P.err(f"{tag}: source must be one of {list(SAFE_SOURCES)}")
        ev = st.setdefault("evidence", [])
        if not isinstance(ev, list):
            P.err(f"{tag}: evidence must be a list")
            continue
        if any(not isinstance(x, dict) or "file" not in x for x in ev):
            P.err(f"{tag}: evidence items must be code citations (file, lines, contains)")
            continue
        if st.get("source") in ("default", "opt_in"):
            if not ev:
                P.err(f"{tag}: a '{st.get('source')}' step needs evidence citing where each named flag, key or env var is defined")
                continue
            require_contains(ev, tag, P, "safe-setup names must be proven at the pinned commit")
        if ev:
            check_evidence(ev, tag, P, repo)
        if repo and ev and st.get("source") in ("default", "opt_in"):
            spans = []
            for x in ev:
                path = os.path.join(repo, str(x.get("file", "")))
                m = re.fullmatch(r"(\d+)(?:-(\d+))?", str(x.get("lines", "")))
                if m and os.path.isfile(path):
                    with open(path, "r", encoding="utf-8", errors="replace") as fh:
                        fl = fh.read().split("\n")
                    spans.append("\n".join(fl[int(m.group(1)) - 1:int(m.group(2) or m.group(1))]))
            cited = "\n".join(spans)
            for code in re.findall(r"`([^`]+)`", str(st.get("how", ""))):
                if not re.search(r"[-_=:./]|^[A-Z0-9]{3,}$", code):
                    continue  # a plain word (a class name, True), not a flag, key or env var
                names = [t for t in re.findall(r"[A-Za-z_][\w.-]{2,}", re.sub(r"<[^>]*>", "", code))]
                if names and not any(t.strip(".-") in cited for t in names):
                    P.warn(f"{tag}: `{code}` in 'how' does not appear in the cited lines - cite where it is defined")
    for k in ("approving", "handling"):
        v = ss.get(k)
        if v is not None and (not isinstance(v, list) or any(not str(x).strip() for x in v)):
            P.err(f"safe_setup.{k} must be a list of short non-empty strings")


def build_entry(card, P, repo=None):
    req = ["id", "name", "repo_url", "subpath", "description", "category", "pinned_commit",
           "version", "scored_date", "scored_configuration", "capability_profile", "headline", "criteria",
           "critical_findings", "rule_of_two", "fixes", "reaudit_log", "limitations"]
    for k in req:
        if k not in card:
            P.err(f"missing top-level field '{k}'")
    allowed = set(req) | {"schema_version", "scorecard_version", "safe_setup"}
    for k in set(card) - allowed:
        P.err(f"unexpected top-level field '{k}' (computed fields are added by the script)")
    if P.errors:
        return None
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", str(card["id"])):
        P.err("id must be a lowercase slug: [a-z0-9-]")
    if card["category"] not in CATEGORIES:
        P.err(f"category must be one of {CATEGORIES}")
    if not re.fullmatch(r"[0-9a-f]{40}", str(card["pinned_commit"])):
        P.err("pinned_commit must be the full 40-character lowercase SHA")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(card["scored_date"])):
        P.err("scored_date must be YYYY-MM-DD")
    if not str(card["repo_url"]).startswith("https://"):
        P.err("repo_url must start with https://")
    cp = card["capability_profile"]
    if not isinstance(cp, dict) or set(cp) != set(CAPABILITIES) or any(v not in ("yes", "no", "opt_in") for v in cp.values()):
        P.err(f"capability_profile needs exactly {CAPABILITIES}, each 'yes' | 'no' | 'opt_in'")
    if not str(card["headline"]).strip():
        P.err("headline is required")
    if not isinstance(card["limitations"], list) or not card["limitations"]:
        P.err("limitations must be a non-empty list of strings")

    if repo:
        try:
            head = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], capture_output=True, text=True,
                                  check=True).stdout.strip()
            if head != card["pinned_commit"]:
                P.err(f"--repo HEAD is {head}, scorecard pins {card['pinned_commit']}")
        except Exception as e:  # noqa: BLE001
            P.err(f"--repo: could not read git HEAD ({e})")

    # criteria
    by_id = {}
    for c in card["criteria"] if isinstance(card["criteria"], list) else []:
        cid = c.get("id") if isinstance(c, dict) else None
        if cid not in CRIT:
            P.err(f"unknown criterion {cid!r}")
        elif cid in by_id:
            P.err(f"duplicate criterion {cid}")
        else:
            by_id[cid] = c
    for cid in CRIT:
        if cid not in by_id:
            P.err(f"{cid}: missing (criteria must contain C1..C10)")

    out_criteria = []
    for cid, meta in CRIT.items():
        c = by_id.get(cid)
        if c is None:
            continue
        allowed_c = {"id", "summary", "structural_absence", "absence_evidence", "parameters", "caps", "alt", "notes"}
        for k in set(c) - allowed_c:
            P.err(f"{cid}: unexpected key '{k}'")
        if not str(c.get("summary", "")).strip():
            P.err(f"{cid}: 'summary' paragraph is required (the website shows it)")
        base = {"id": cid, "name": meta["name"], "number": meta["number"], "owasp": meta["owasp"],
                "question": meta["question"], "summary": c.get("summary", ""), "max": 1.0}
        if c.get("notes"):
            base["notes"] = c["notes"]
        if c.get("structural_absence"):
            check_evidence(c.get("absence_evidence"), f"{cid}.absence_evidence", P, repo, need_search=True)
            sa_param = {"level": 4, "structural_absence": True, "status": "verified",
                        "finding": "Risk surface absent at this commit.", "evidence": c.get("absence_evidence", []),
                        "weight": 0, "points": 0}
            params = {p: dict(sa_param, weight=w, points=w) for p, w in WEIGHTS.items()}
            mech = {"kind": "default", "label": "structural absence", "score": 1.0, "raw": 1.0, "cap": None,
                    "confidence": "high", "parameters": params}
            out_criteria.append(dict(base, status="structural_absence", score=1.0, counted="default",
                                     confidence="high", cap=None, parameters=params, mechanisms=[mech],
                                     absence_evidence=c.get("absence_evidence", [])))
            continue
        main = score_mechanism(cid, c.get("parameters"), c.get("caps", []), "default configuration", P, repo,
                               "default")
        mechs, winner = ([main] if main else []), main
        alt = c.get("alt")
        if alt is not None:
            if not isinstance(alt, dict) or not str(alt.get("label", "")).strip():
                P.err(f"{cid}.alt: needs a 'label' and 'parameters'")
            else:
                for k in set(alt) - {"label", "parameters", "caps"}:
                    P.err(f"{cid}.alt: unexpected key '{k}'")
                alt_caps = list(alt.get("caps", []) or [])
                if not any(isinstance(x, dict) and x.get("id") == "G1" for x in alt_caps):
                    alt_caps.append({"id": "G1", "reason": "Opt-in mechanism: off in the scored default configuration."})
                am = score_mechanism(cid, alt.get("parameters"), alt_caps, alt["label"], P, repo, "alt")
                if am:
                    mechs.append(am)
                    if main and am["score"] > main["score"]:
                        winner = am
        if winner is None:
            continue
        out_criteria.append(dict(base, status="scored", score=winner["score"], counted=winner["kind"],
                                 confidence=winner["confidence"], cap=winner["cap"],
                                 parameters=winner["parameters"], mechanisms=mechs))

    # report-level sections
    for i, f in enumerate(card["critical_findings"] or []):
        if not isinstance(f, dict) or f.get("criterion") not in CRIT or not f.get("summary"):
            P.err(f"critical_findings[{i}]: needs summary, criterion, owasp, evidence")
            continue
        for k in set(f) - {"summary", "criterion", "owasp", "evidence"}:
            P.err(f"critical_findings[{i}]: unexpected key '{k}'")
        check_evidence(f.get("evidence"), f"critical_findings[{i}]", P, repo)
        require_contains(f.get("evidence"), f"critical_findings[{i}]", P, "critical finding")
    r2 = card["rule_of_two"]
    if not isinstance(r2, dict) or set(r2) != {"untrusted_input", "sensitive_data", "state_change_or_egress",
                                               "same_session"} or not isinstance(r2.get("same_session"), bool):
        P.err("rule_of_two needs untrusted_input, sensitive_data, state_change_or_egress (strings), same_session (bool)")
    fixes = []
    if not isinstance(card["fixes"], list) or len(card["fixes"]) > 5:
        P.err("fixes must be a list of at most 5")
    for i, fx in enumerate(card["fixes"] or []):
        ok = (isinstance(fx, dict) and fx.get("criterion") in CRIT and fx.get("parameter") in WEIGHTS
              and fx.get("from_level") in FRACTION and fx.get("to_level") in FRACTION and fx.get("summary"))
        if not ok:
            P.err(f"fixes[{i}]: needs summary, criterion, parameter (S/C/D/B), from_level, to_level (0-4)")
            continue
        for k in set(fx) - {"summary", "criterion", "parameter", "from_level", "to_level", "playbook"}:
            P.err(f"fixes[{i}]: unexpected key '{k}'")
        gain = round(WEIGHTS[fx["parameter"]] * (FRACTION[fx["to_level"]] - FRACTION[fx["from_level"]]), 3)
        fixes.append(dict(fx, estimated_gain=gain))
    for i, r in enumerate(card["reaudit_log"] or []):
        ok = (isinstance(r, dict) and r.get("criterion") in CRIT and r.get("parameter") in WEIGHTS
              and r.get("from_level") in FRACTION and r.get("to_level") in FRACTION and r.get("reason"))
        if not ok:
            P.err(f"reaudit_log[{i}]: needs criterion, parameter, from_level, to_level, reason")

    if "safe_setup" in card:
        check_safe_setup(card["safe_setup"], P, repo)

    if P.errors:
        return None

    # cross-check critical findings against the deterministic rule
    flagged = {f["criterion"] for f in card["critical_findings"]}
    for c in out_criteria:
        default = c["mechanisms"][0]
        reasons = []
        if c["cap"] and c["cap"]["id"] != "G1" and c["counted"] == "default":
            reasons.append(f"cap {c['cap']['id']}")
        if default["cap"] and default["cap"]["id"] == "G2":
            reasons.append("G2")
        if (c["id"] in CRITICAL_B_CRITERIA and c["status"] == "scored"
                and default["parameters"]["B"]["level"] == 0):
            reasons.append("B at L0")
        if reasons and c["id"] not in flagged:
            P.warn(f"{c['id']}: {', '.join(reasons)} should appear in critical_findings")

    for c in out_criteria:
        for m in c["mechanisms"]:
            for prm in m["parameters"].values():
                for ev in prm["evidence"]:
                    url = permalink(card["repo_url"], card["pinned_commit"], ev)
                    if url:
                        ev["url"] = url
    for f in card["critical_findings"]:
        for ev in f["evidence"]:
            url = permalink(card["repo_url"], card["pinned_commit"], ev)
            if url:
                ev["url"] = url
    for st in (card.get("safe_setup") or {}).get("steps", []):
        for ev in st["evidence"]:
            url = permalink(card["repo_url"], card["pinned_commit"], ev)
            if url:
                ev["url"] = url

    from decimal import Decimal, ROUND_HALF_UP
    exact = sum(Decimal(str(c["score"])) for c in out_criteria)
    total = float(exact.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))
    applicable = [c for c in out_criteria if c["status"] == "scored"]
    app = round(sum(c["score"] for c in applicable), 2)
    entry = {
        "schema_version": SCHEMA_VERSION, "scorecard_version": SCORECARD_VERSION,
        **{k: card[k] for k in ["id", "name", "repo_url", "subpath", "description", "category",
                                "pinned_commit", "version", "scored_date", "scored_configuration"]},
        "score": total, "max_score": 10.0, "band": band(total),
        "applicable": {"count": len(applicable), "score": app, "max": float(len(applicable)),
                       "percent": round(100 * app / len(applicable)) if applicable else None},
        "capability_profile": card["capability_profile"], "headline": card["headline"],
        **({"safe_setup": card["safe_setup"]} if "safe_setup" in card else {}),
        "criteria": out_criteria, "critical_findings": card["critical_findings"],
        "rule_of_two": card["rule_of_two"], "fixes": fixes, "reaudit_log": card["reaudit_log"],
        "limitations": card["limitations"],
    }
    return entry


def schema_check(entry, P):
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "schema", "entry.schema.json")
    try:
        import jsonschema  # type: ignore
    except ImportError:
        P.warn("jsonschema not installed; skipped schema validation (pip install jsonschema)")
        return
    with open(path) as f:
        schema = json.load(f)
    for e in sorted(jsonschema.Draft202012Validator(schema).iter_errors(entry), key=lambda e: list(e.path)):
        P.err(f"schema: {'/'.join(map(str, e.path)) or '(root)'}: {e.message[:200]}")


# ---------------------------------------------------------------- rendering

def lv(p):
    return "SA" if p["structural_absence"] else f"L{p['level']}"


def fmt_ev(ev, link=True):
    if "file" in ev:
        ref = f"`{ev['file']}:{ev['lines']}`"
        if link and ev.get("url"):
            ref = f"[{ev['file']}:{ev['lines']}]({ev['url']})"
        return ref + (f" ({ev['note']})" if ev.get("note") else "")
    return f"searched `{ev['search']}` in `{ev['scope']}` → {ev['hits']} hits" + (
        f" ({ev['note']})" if ev.get("note") else "")


def render_table(e, standalone=True):
    out = [f"**{e['name']}** @ `{e['pinned_commit'][:12]}` · scored {e['scored_date']}", ""] if standalone else []
    out += ["| # | Criterion | S | C | D | B | Raw | Cap | Score | Confidence |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for c in e["criteria"]:
        p = c["parameters"]
        raw = next(m["raw"] for m in c["mechanisms"] if m["kind"] == c["counted"])
        tag = " (SA)" if c["status"] == "structural_absence" else (" (alt)" if c["counted"] == "alt" else "")
        out.append(f"| {c['id']} | {c['name']} | {lv(p['S'])} | {lv(p['C'])} | {lv(p['D'])} | {lv(p['B'])} | "
                   f"{raw:.2f} | {c['cap']['id'] if c['cap'] else 'none'} | **{c['score']:.2f}**{tag} | "
                   f"{c['confidence'].capitalize()} |")
    out += [""]
    if standalone:
        out.append(f"**Total: {e['score']:.1f} / 10.0 ({e['band']['label']})**")
    a = e["applicable"]
    if a["count"] < 10:
        out.append(f"Controls where a risk surface exists: {a['score']:.2f} / {a['max']:.1f} "
                   f"({a['percent']}%); {10 - a['count']} {'criterion' if 10 - a['count'] == 1 else 'criteria'} scored SA (surface absent).")
    return "\n".join(out)


def md_cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def render_safe_setup(ss):
    L = ["## Safest setup", "", ss["intro"], "", "| Setup | How | What it gives you |", "|---|---|---|"]
    for st in ss["steps"]:
        refs = "; ".join(fmt_ev(x) for x in st["evidence"])
        L.append(f"| {md_cell(st['setup'])} | {md_cell(st['how'])}" + (f" ({md_cell(refs)})" if refs else "") +
                 f" | {md_cell(st['gives_you'])} ({st['criterion']}) |")
    for key, title in (("approving", "Approving with confidence"), ("handling", "Handling data")):
        if ss.get(key):
            L += ["", f"### {title}", ""] + [f"- {x}" for x in ss[key]]
    return L + [""]


def render_report(e):
    cp = e["capability_profile"]
    prof = " · ".join(f"{k.replace('_', ' ')} {v.replace('_', '-')}" for k, v in cp.items())
    L = [f"# Defense-in-depth score: {e['name']}", "",
         f"**Repo:** {e['repo_url']}" + (f" (`{e['subpath']}`)" if e["subpath"] else "") +
         f" · **Commit:** `{e['pinned_commit']}`" + (f" ({e['version']})" if e["version"] else "") +
         f" · **Reviewed:** {e['scored_date']}",
         f"**What it is:** {e['description']}",
         f"**Category:** {dict((c[0], c[1]) for c in CATEGORY_INFO).get(e['category'], e['category'])}",
         f"**Scored configuration:** {e['scored_configuration']}",
         f"**Agent surface (default):** {prof}", "",
         f"## Score: {e['score']:.1f} / 10.0 ({e['band']['label']})", "", render_table(e, standalone=False), "",
         e["headline"], ""]
    if e.get("safe_setup"):
        L += render_safe_setup(e["safe_setup"])
    L += ["## Critical gaps"]
    if e["critical_findings"]:
        for f in e["critical_findings"]:
            L.append(f"- {f['summary']} ({', '.join(f['owasp'])}; {f['criterion']}). Evidence: " +
                     "; ".join(fmt_ev(x) for x in f["evidence"]))
    else:
        L.append("- None: no criterion is capped and no blast radius is at the worst level.")
    L += ["", "## Criterion details"]
    for c in e["criteria"]:
        L += ["", f"### {c['id']} {c['name']}: {c['score']:.2f} ({c['confidence']} confidence)", "", c["summary"], ""]
        if c["status"] == "structural_absence":
            L.append("- **Structural absence:** " + "; ".join(fmt_ev(x) for x in c["absence_evidence"]))
        else:
            for m in c["mechanisms"]:
                if len(c["mechanisms"]) > 1:
                    star = " ← counted" if m["kind"] == c["counted"] else ""
                    capn = f", cap {m['cap']['id']}" if m["cap"] else ""
                    L.append(f"- **{m['label']}** ({m['kind']}; raw {m['raw']:.2f}{capn} → {m['score']:.2f}){star}")
                ind = "  " if len(c["mechanisms"]) > 1 else ""
                for pk in "SCDB":
                    pr = m["parameters"][pk]
                    L.append(f"{ind}- **{pk} {lv(pr)}:** {pr['finding']} Evidence: " +
                             "; ".join(fmt_ev(x) for x in pr["evidence"]) + f" ({pr['status']})")
                    if pr.get("gap"):
                        L.append(f"{ind}  - *To reach the next level:* {pr['gap']}")
            L.append(f"- **Cap:** {c['cap']['id'] + ': ' + c['cap']['reason'] if c['cap'] else 'none'}")
        if c.get("notes"):
            L.append(f"- **Notes:** {c['notes']}")
    r = e["rule_of_two"]
    L += ["", "## Rule-of-Two check",
          f"[A] untrusted input: {r['untrusted_input']} · [B] sensitive data/systems: {r['sensitive_data']} · "
          f"[C] state change / egress: {r['state_change_or_egress']} · Same default session? "
          f"{'Yes' if r['same_session'] else 'No'}", "", "## Highest-impact improvements"]
    for i, fx in enumerate(e["fixes"], 1):
        L.append(f"{i}. {fx['summary']} ({fx['criterion']} {fx['parameter']} L{fx['from_level']}→L{fx['to_level']}, "
                 f"+{fx['estimated_gain']:.3f} before caps" + (f"; {fx['playbook']}" if fx.get("playbook") else "") + ")")
    if not e["fixes"]:
        L.append("None proposed.")
    L += ["", "## Re-audit log"]
    L += [f"- {r['criterion']} {r['parameter']}: L{r['from_level']} → L{r['to_level']}. {r['reason']}"
          for r in e["reaudit_log"]] or ["- No changes."]
    L += ["", "## Limitations"] + [f"- {x}" for x in e["limitations"]]
    return "\n".join(L) + "\n"


def catalog():
    return {"scorecard_version": SCORECARD_VERSION,
            "parameters": [{"id": k, "name": PARAM_NAMES[k], "weight": w} for k, w in WEIGHTS.items()],
            "levels": [{"level": k, "fraction": v} for k, v in FRACTION.items()],
            "bands": [{"id": b, "label": l, "min_score": f, "color": c} for f, b, l, c in BANDS],
            "categories": [{"id": c, "label": l, "description": d} for c, l, d in CATEGORY_INFO],
            "category_rules": CATEGORY_RULES,
            "criteria": [{"id": cid, "number": m["number"], "name": m["name"], "question": m["question"],
                          "owasp": m["owasp"], "max": 1.0} for cid, m in CRIT.items()],
            "caps": [{"id": k, "max": v[0], "criterion": v[1]} for k, v in CAPS.items()]}


EXAMPLE_PARAM = {"level": 2, "status": "verified", "finding": "One sentence on what the code shows.",
                 "gap": "One sentence on what the next level requires that the code doesn't do.",
                 "evidence": [{"file": "src/agent/tools.py", "lines": "40-58", "contains": "def validate_path"}]}
EXAMPLE = {
    "id": "example-agent", "name": "Example Agent", "repo_url": "https://github.com/example/agent", "subpath": None,
    "description": "One line: what the project is.", "category": "coding",
    "pinned_commit": "0123456789abcdef0123456789abcdef01234567", "version": "v1.2.0",
    "scored_date": "2026-01-01", "scored_configuration": "Interactive CLI, no flags, fresh install.",
    "capability_profile": {k: "yes" for k in CAPABILITIES},
    "headline": "Two to four sentences for someone deploying this as shipped. Name the dominant risk.",
    "criteria": [{"id": cid, "summary": "One plain-language paragraph on what was found in the source.",
                  "parameters": {p: EXAMPLE_PARAM for p in "SCDB"}, "caps": []} for cid in CRIT],
    "critical_findings": [],
    "rule_of_two": {"untrusted_input": "...", "sensitive_data": "...", "state_change_or_egress": "...",
                    "same_session": True},
    "fixes": [{"summary": "The change.", "criterion": "C4", "parameter": "D", "from_level": 0, "to_level": 3,
               "playbook": "Playbook 3 step 1"}],
    "reaudit_log": [],
    "limitations": ["Static source review of the pinned commit only; nothing was executed, installed, or probed."],
}
EXAMPLE["criteria"][3]["alt"] = {"label": "opt-in container sandbox", "parameters": {p: EXAMPLE_PARAM for p in "SCDB"},
                                 "caps": []}
EXAMPLE["criteria"][5] = {"id": "C6", "summary": "No memory or auto-loaded workspace context exists.",
                          "structural_absence": True,
                          "absence_evidence": [{"search": "rg -n -S 'memory|dotenv|AGENTS.md'", "scope": "src/",
                                                "hits": 0}]}


def main(argv):
    flags = {a for a in argv[1:] if a.startswith("--")}
    vals = {}
    for i, a in enumerate(argv):
        if a in ("--repo", "--entry", "--report") and i + 1 < len(argv):
            vals[a] = argv[i + 1]
    positional = [a for i, a in enumerate(argv[1:], 1)
                  if not a.startswith("--") and argv[i - 1] not in ("--repo", "--entry", "--report")]
    if "--example" in flags:
        print(json.dumps(EXAMPLE, indent=2))
        return 0
    if "--catalog" in flags:
        print(json.dumps(catalog(), indent=2))
        return 0
    if not positional or "--help" in flags or "-h" in argv:
        print(__doc__)
        return 0 if ("--help" in flags or "-h" in argv) else 2
    with open(positional[0]) as f:
        card = json.load(f)
    P = Problems()
    entry = build_entry(card, P, repo=vals.get("--repo"))
    if entry:
        schema_check(entry, P)
    if "--repo" not in vals:
        P.warn("no --repo given: cited files and line ranges were not checked")
    for w in P.warnings:
        print(f"WARNING: {w}", file=sys.stderr)
    if P.errors:
        for e in P.errors:
            print(f"ERROR: {e}", file=sys.stderr)
        print(f"\n{len(P.errors)} error(s); fix the scorecard and rerun.", file=sys.stderr)
        return 1
    if "--entry" in vals:
        with open(vals["--entry"], "w") as f:
            json.dump(entry, f, indent=2, ensure_ascii=False)
            f.write("\n")
    if "--report" in vals:
        with open(vals["--report"], "w") as f:
            f.write(render_report(entry))
    if "--json" in flags:
        print(json.dumps(entry, indent=2, ensure_ascii=False))
    else:
        print(render_table(entry))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
