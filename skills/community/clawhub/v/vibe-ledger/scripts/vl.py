#!/usr/bin/env python3
"""vibe-ledger command line.

start -> (the agent writes ledger.json) -> check -> render -> shot.
Every step prints the exact next command; run it as printed."""
from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

SELF = Path(__file__).resolve()
sys.path.insert(0, str(SELF.parent))

import candidates  # noqa: E402
import explain  # noqa: E402
import graph  # noqa: E402
import probes  # noqa: E402
import render  # noqa: E402
import requirements  # noqa: E402
import sessions  # noqa: E402
import shot  # noqa: E402
import verify  # noqa: E402
from common import (SOURCE_EXTS, __version__, detect_lang, git_ls_files, is_within, iter_files,  # noqa: E402
                    load_json, project_id, project_workdir, read_jsonl, rel, write_json, write_jsonl)
from ledger import LedgerError, merge  # noqa: E402
from ledger_report import diff as run_diff  # noqa: E402
from ledger_report import graph_page  # noqa: E402
from ledger_report.i18n import t  # noqa: E402

GUIDE = SELF.parent.parent / "references" / "extraction-guide.md"
EXPLAIN_GUIDE = SELF.parent.parent / "references" / "explain-guide.md"
REQ_GUIDE = SELF.parent.parent / "references" / "requirements-guide.md"


def cmd(*args) -> str:
    return " ".join(shlex.quote(str(a)) for a in ("python3", SELF, *args))


def _root(args) -> Path:
    root = Path(args.project).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"error: project folder not found: {root}")
    return root


def latest_run(root: Path) -> Path:
    marker = project_workdir(root) / "latest_run.txt"
    if not marker.exists():
        raise SystemExit(f"error: no run yet for {root}. Run start first:\n  {cmd('start', '--project', root)}")
    return Path(marker.read_text(encoding="utf-8").strip())


def claude_settings_path() -> Path:
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "settings.json"


def read_retention(path: Path) -> tuple[int, str]:
    if not path.exists():
        return 30, "default"
    try:
        value = json.loads(path.read_text(encoding="utf-8")).get("cleanupPeriodDays")
    except (json.JSONDecodeError, AttributeError):
        return 30, "unreadable settings file, assuming the default"
    return (value, "settings") if isinstance(value, int) else (30, "default")


def unattributed(root: Path, recs: list[dict]) -> list[str]:
    touched = {rel(f, root) for r in recs for f in r["files"] if is_within(f, root)}
    files = git_ls_files(root)
    if files is None:
        files = [rel(p, root) for p in iter_files(root, SOURCE_EXTS)]
    return sorted(f for f in files if Path(f).suffix.lower() in SOURCE_EXTS and f not in touched)


def graph_stats(g: dict) -> dict:
    chosen = sum(1 for n in g["nodes"] if n["explain"])
    return {"files": len(g["nodes"]), "edges": len(g["edges"]), "externals": len(g["externals"]),
            "entries": len(g["entries"]), "explain": chosen, "explain_groups": -(-chosen // graph.EXPLAIN_CHUNK),
            "collapsed": g["collapsed"], "unresolved": len(g["unresolved"]), "excluded": g["excluded"]}


def top_file(g: dict) -> str | None:
    ranked = sorted(g.get("nodes", []), key=lambda n: (-n["score"], n["id"]))
    return ranked[0]["id"] if ranked else None


def do_start(args) -> int:
    root = _root(args)
    work = project_workdir(root)
    base = datetime.now().strftime("%Y%m%d-%H%M%S")
    run, n = work / "runs" / base, 1
    while run.exists():
        run, n = work / "runs" / f"{base}-{n}", n + 1
    run.mkdir(parents=True)

    claude_dir = Path(args.claude_dir).expanduser() if args.claude_dir else sessions.default_claude_dir()
    codex_dir = Path(args.codex_dir).expanduser() if args.codex_dir else sessions.default_codex_dir()
    recs, stats = sessions.collect(root, claude_dir, codex_dir, archive_dir=work / "digests")
    write_jsonl(run / "digest.jsonl", recs)
    cands = candidates.run(root, recs)
    packs = []
    for k, text in enumerate(cands.pop("packs_text"), 1):
        name = f"reading_pack_{k:02d}.md"
        (run / name).write_text(text, encoding="utf-8")
        packs.append(name)
    write_json(run / "candidates.json", cands)
    req_texts, req_info = requirements.build_packs(root, recs)
    req_info["packs"] = []
    for k, text in enumerate(req_texts, 1):
        name = f"requests_{k:02d}.md"
        (run / name).write_text(text, encoding="utf-8")
        req_info["packs"].append(name)
    pr = probes.run_all(root)
    write_json(run / "probes.json", pr)
    g = graph.build(root, recs, pr)
    write_json(run / "graph.json", g)
    (run / "explain_pack.md").write_text(graph.explain_pack(g, root, pr), encoding="utf-8")
    days, source = read_retention(claude_settings_path())
    claude_ts = [r["ts"] for r in recs if r["agent"] == "claude-code" and r["ts"]]
    manifest = {
        "version": __version__, "project_root": str(root), "project_name": root.name, "project_id": project_id(root),
        "run_dir": str(run), "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "lang": args.lang or detect_lang(r["text"] for r in recs if r["role"] == "user"),
        "sessions": stats.to_dict(), "candidates": cands["stats"],
        "probes": {"ran": pr["ran"], "skipped": pr["skipped"], "stack": pr["stack"]},
        "graph": graph_stats(g),
        "packs": packs, "requests": req_info, "unattributed": unattributed(root, recs),
        "retention": {"days": days, "source": source, "settings_path": str(claude_settings_path()),
                      "earliest": min(claude_ts) if claude_ts else ""},
    }
    write_json(run / "run.json", manifest)
    (work / "latest_run.txt").write_text(str(run), encoding="utf-8")  # only a complete run becomes current
    _print_start(manifest, run, root)
    return 0


def _print_start(m: dict, run: Path, root: Path) -> None:
    s, c, p = m["sessions"], m["candidates"], m["probes"]
    print(f"vibe-ledger {__version__} — run folder: {run}")
    if s["threads"]:
        print(f"Conversations: {s['threads']} ({', '.join(f'{k} {v}' for k, v in s['by_agent'].items())}), "
              f"{s['earliest'][:10]} → {s['latest'][:10]}; {s['archived_threads']} restored from the archive")
    else:
        print("No conversations were found for this project. Promises need a conversation source, so leave "
              "`promises` empty and record only map, access and paths from the code.")
    print(f"Candidates: {c['compromises']} error→change, {c['deferrals']} put off, {c['claims']} AI claims, "
          f"{c['todos']} code TODOs")
    print(f"Probes ran: {', '.join(p['ran']) or 'none'}; skipped: {', '.join(x['probe'] for x in p['skipped']) or 'none'}")
    if p["stack"]["unsupported"]:
        print(f"Not covered by probes: {', '.join(p['stack']['unsupported'])}")
    print(f"Reading packs: {len(m['packs'])} ({', '.join(f'{n} {k:,} chars' for n, k in zip(m['packs'], c['pack_chars']))})")
    q = m["requests"]
    print(f"Requests: {q['messages']} messages the user typed, in {len(q['packs'])} pack(s) "
          f"({', '.join(f'{n} {k:,} chars' for n, k in zip(q['packs'], q['chars']))})")
    print(f"Report language: {m['lang']}")
    r = m["retention"]
    print(f"Claude Code keeps transcripts for {r['days']} days ({r['source']}).")
    for w in s["warnings"]:
        print(f"WARNING: {w}")
    gs = m["graph"]
    print(f"File graph: {gs['files']} files, {gs['edges']} links, {gs['externals']} outside services, "
          f"{gs['entries']} entry points" + ("; large project, so folders start collapsed" if gs["collapsed"] else ""))
    if gs["unresolved"]:
        print(f"Imports that could not be resolved: {gs['unresolved']} (listed in {run / 'graph.json'})")
    print(f"Files to explain: {gs['explain']}" + (f" in {gs['explain_groups']} groups" if gs["explain_groups"] > 1 else ""))
    if r["days"] < 365 and s["by_agent"].get("claude-code"):
        print("NEXT (only after the user agrees — it edits their Claude Code settings):")
        print("  " + cmd("retention", "--set", 365))
    parts, pack = run / "parts", run / "explain_pack.md"
    print("NEXT: write three files, then run the checks.")
    if len(m["packs"]) == 1:
        print(f"  1. Ledger: read {run / m['packs'][0]}, {run / 'probes.json'} and the project code; write "
              f"{run / 'ledger.json'} as {GUIDE} describes.")
    else:
        print(f"  1. Ledger: give each reading pack in {run} to its own subagent (or do them one by one). Each writes "
              f"{parts}/part_NN.json with evidence, promises and compromises only ({GUIDE}). After the merge below, "
              f"add map, access and paths to {run / 'ledger.json'}.")
    if not q["messages"]:
        print("  2. Requirements: there are no user messages, so skip requirements.json.")
    elif len(q["packs"]) == 1:
        print(f"  2. Requirements: read {run / q['packs'][0]} and the code it is about; write "
              f"{run / 'requirements.json'} as {REQ_GUIDE} describes.")
    else:
        print(f"  2. Requirements: give each requests_NN.md in {run} to its own subagent (or do them in order). Each "
              f"writes {parts}/req_NN.json with the same NN ({REQ_GUIDE}).")
    if gs["explain_groups"] > 1:
        print(f"  3. Explanations: give each group in {pack} to its own subagent (or do them one by one). Each writes "
              f"the {parts}/explain_NN.json named in its heading, as {EXPLAIN_GUIDE} describes.")
    else:
        print(f"  3. Explanations: read {pack} and the files it lists; write {run / 'explain.json'} as "
              f"{EXPLAIN_GUIDE} describes.")
    if len(m["packs"]) > 1 or gs["explain_groups"] > 1 or len(q["packs"]) > 1:
        print("Merge the parts:")
        print("  " + cmd("merge", "--project", root))
    print("Then run:")
    print("  " + cmd("check", "--project", root))


def do_merge(args) -> int:
    root = _root(args)
    run = latest_run(root)
    parts_dir = Path(args.parts_dir) if args.parts_dir else run / "parts"
    ledger_files = sorted(parts_dir.glob("part_*.json"))
    explain_files = sorted(parts_dir.glob("explain_*.json"))
    req_files = sorted(parts_dir.glob("req_*.json"))
    if not ledger_files and not explain_files and not req_files:
        print(f"error: no part_*.json, explain_*.json or req_*.json files in {parts_dir}")
        return 2
    docs = {}
    for f in ledger_files + explain_files + req_files:
        try:
            docs[f] = load_json(f)
        except json.JSONDecodeError as exc:
            print(f"error: {f.name} is not valid JSON: {exc}")
            return 2
    if ledger_files:
        try:
            led = merge([docs[f] for f in ledger_files])
        except LedgerError as exc:
            print("The parts do not match the ledger format:")
            for problem in exc.problems:
                print("  -", problem)
            return 2
        write_json(run / "ledger.json", led)
        print(f"Merged {len(ledger_files)} parts: {len(led['promises'])} promises, {len(led['compromises'])} "
              f"compromises → {run / 'ledger.json'}")
    if explain_files:
        try:
            exp = explain.merge([docs[f] for f in explain_files])
        except explain.ExplainError as exc:
            print(f"The explanation parts do not match the explain.json format ({EXPLAIN_GUIDE}):")
            for problem in exc.problems:
                print("  -", problem)
            return 2
        write_json(run / "explain.json", exp)
        dup = f"; explained twice, kept the first: {', '.join(exp['duplicates'])}" if exp["duplicates"] else ""
        print(f"Merged {len(explain_files)} explanation parts: {len(exp['files'])} files{dup} → {run / 'explain.json'}")
    if req_files:
        try:
            req = requirements.merge([docs[f] for f in req_files])
        except requirements.RequirementsError as exc:
            print(f"The requirement parts do not match the requirements.json format ({REQ_GUIDE}):")
            for problem in exc.problems:
                print("  -", problem)
            return 2
        write_json(run / "requirements.json", req)
        print(f"Merged {len(req_files)} requirement parts: {len(req['requirements'])} requirements → "
              f"{run / 'requirements.json'}")
    if ledger_files:
        print(f"NEXT: add map, access and paths from the code ({GUIDE}), then run:")
    else:
        print("NEXT: run:")
    print("  " + cmd("check", "--project", root))
    return 0


def do_check(args) -> int:
    root = _root(args)
    run = latest_run(root)
    path = Path(args.ledger) if args.ledger else run / "ledger.json"
    if not path.exists():
        print(f"error: {path} does not exist yet; write the ledger first ({GUIDE})")
        return 2
    try:
        led = load_json(path)
    except json.JSONDecodeError as exc:
        print(f"error: {path} is not valid JSON: {exc}")
        return 2
    index = {obj["id"]: obj for _, obj in read_jsonl(run / "digest.jsonl") if obj}
    try:
        out = verify.verify_ledger(led, index, root, load_json(run / "probes.json"))
    except LedgerError as exc:
        print("The ledger does not match the format (references/ledger-schema.md):")
        for problem in exc.problems:
            print("  -", problem)
        print("NEXT: fix these, then run:\n  " + cmd("check", "--project", root))
        return 2
    write_json(run / "ledger.verified.json", out)
    for line in verify.summary_lines(out):
        print(line)
    code = _check_explain(args, root, run, index)
    if code:
        return code
    code = _check_requirements(args, root, run)
    if code:
        return code
    print("NEXT: if a quote, snippet or function line failed only because it was mis-copied, fix it from the real "
          "text and run check again. Otherwise run:")
    print("  " + cmd("render", "--project", root))
    return 0


def _check_explain(args, root: Path, run: Path, index: dict) -> int:
    verified = run / "explain.verified.json"
    verified.unlink(missing_ok=True)  # never let render use explanations from an earlier check
    again = "  " + cmd("check", "--project", root)
    if not (run / "graph.json").exists():
        print("error: this run has no graph.json (it was started by an older version of vibe-ledger). Start again:\n"
              "  " + cmd("start", "--project", root))
        print(f"Your ledger is not lost: copy {run / 'ledger.json'} (and explain.json, if you wrote one) into the new "
              "run folder that start prints, then run check there — it is checked against the current code again.")
        return 2
    path = Path(args.explain) if args.explain else run / "explain.json"
    if not path.exists():
        print(f"error: {path} does not exist yet. The flowchart needs it: write it from {run / 'explain_pack.md'} as "
              f"{EXPLAIN_GUIDE} describes (or merge parts/explain_NN.json), then run:\n{again}")
        return 2
    try:
        doc = load_json(path)
    except json.JSONDecodeError as exc:
        print(f"error: {path} is not valid JSON: {exc}")
        return 2
    try:
        out = explain.verify(doc, load_json(run / "graph.json"), root, index)
    except explain.ExplainError as exc:
        print(f"{path.name} does not match the format ({EXPLAIN_GUIDE}):")
        for problem in exc.problems:
            print("  -", problem)
        print("NEXT: fix these, then run:\n" + again)
        return 2
    write_json(verified, out)
    for line in explain.summary_lines(out):
        print(line)
    return 0


def _check_requirements(args, root: Path, run: Path) -> int:
    verified = run / "requirements.verified.json"
    verified.unlink(missing_ok=True)
    manifest = load_json(run / "run.json")
    if "requests" not in manifest:  # a run started before requirement coverage existed
        return 0
    if not manifest["requests"]["messages"]:
        print("Requirements: no user messages in the conversations, so there is nothing to check.")
        return 0
    again = "  " + cmd("check", "--project", root)
    path = Path(args.requirements) if args.requirements else run / "requirements.json"
    if not path.exists():
        print(f"error: {path} does not exist yet. The 需求对照 / Your asks tab needs it: write it from the "
              f"requests_NN.md files in {run} as {REQ_GUIDE} describes (or merge parts/req_NN.json), then run:\n{again}")
        return 2
    try:
        doc = load_json(path)
    except json.JSONDecodeError as exc:
        print(f"error: {path} is not valid JSON: {exc}")
        return 2
    recs = [obj for _, obj in read_jsonl(run / "digest.jsonl") if obj]
    try:
        out = requirements.verify(doc, recs, root, load_json(run / "probes.json"))
    except requirements.RequirementsError as exc:
        print(f"{path.name} does not match the format ({REQ_GUIDE}):")
        for problem in exc.problems:
            print("  -", problem)
        print("NEXT: fix these, then run:\n" + again)
        return 2
    write_json(verified, out)
    for line in requirements.summary_lines(out):
        print(line)
    if out["coverage"]["unaccounted"]:
        print("Every user message should be a requirement's source or listed under skipped; the ones above are "
              "neither. Add them, or leave them: the report lists them as unaccounted.")
    return 0


def _compare_problem(prev: Path, run: Path, manifest: dict) -> str | None:
    """Why `prev` cannot be compared with `run`, or None."""
    if not all((prev / name).is_file() for name in run_diff.NEEDED):
        return f"{prev} is not a finished run (it needs {', '.join(run_diff.NEEDED)})"
    if prev == Path(run).resolve():
        return f"{prev} is this run; pick an earlier one"
    other = load_json(prev / "run.json").get("project_root")
    if other and other != manifest.get("project_root"):
        return f"{prev} is a run of another project ({other})"
    try:
        json.loads((prev / "graph.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return f"{prev}/graph.json cannot be read, so that run cannot be compared"
    return None


def do_render(args) -> int:
    root = _root(args)
    run = latest_run(root)
    verified, explained = run / "ledger.verified.json", run / "explain.verified.json"
    if not verified.exists() or not explained.exists():
        print("error: run check first; it has to pass for both ledger.json and explain.json:\n  "
              + cmd("check", "--project", root))
        return 2
    manifest = load_json(run / "run.json")
    lang = args.lang or manifest["lang"]
    ledger_doc, probes_doc = load_json(verified), load_json(run / "probes.json")
    changes = None
    if not args.no_compare:
        prev = Path(args.compare).expanduser().resolve() if args.compare else run_diff.previous_run(run)
        problem = _compare_problem(prev, run, manifest) if prev is not None else None
        if prev is None:
            print(t(lang, "g_diff_cli_none"))
        elif problem:
            print(f"error: {problem}")
            return 2
        else:
            changes = run_diff.compare(prev, run, lang)
            print(run_diff.summary_line(changes, lang))
    req_doc = None
    if "requests" in manifest:
        if manifest["requests"]["messages"]:
            if not (run / "requirements.verified.json").exists():
                print("error: run check first; it has to pass for requirements.json too:\n  "
                      + cmd("check", "--project", root))
                return 2
            req_doc = load_json(run / "requirements.verified.json")
        else:
            req_doc = {"requirements": [], "none": True, "threads": manifest.get("sessions", {}).get("threads", 0)}
    data = graph_page.page_data(load_json(run / "graph.json"), load_json(explained), ledger_doc, probes_doc, root,
                                lang, bool(manifest.get("sessions", {}).get("records")), diff=changes,
                                requirements=req_doc)
    html = render.render_html(ledger_doc, manifest, probes_doc, lang, graph_data=data, requirements=req_doc)
    out = render.deliver(html, run, manifest["project_name"], args.out_dir)
    manifest["report_path"] = str(out)
    write_json(run / "run.json", manifest)
    print(f"Report: {out}")
    print("NEXT: take screenshots and look at the flowchart, a selected file and the overview before telling the "
          "user it is done:")
    print("  " + cmd("shot", "--project", root))
    return 0


def do_shot(args) -> int:
    root = _root(args)
    run = latest_run(root)
    report = load_json(run / "run.json").get("report_path")
    if not report or not Path(report).exists():
        print("error: render first:\n  " + cmd("render", "--project", root))
        return 2
    chrome = shot.find_chrome()
    if not chrome:
        print(f"Chrome or Chromium was not found, so no screenshots were taken. Open the report and look: {report}")
        return 1
    top = top_file(load_json(run / "graph.json")) if (run / "graph.json").exists() else None
    explained = run / "explain.verified.json"
    journeys = load_json(explained).get("journeys", []) if explained.exists() else []
    paths = shot.take_shots(Path(report), run / "shots", chrome, select=top,
                            journey=journeys[0]["id"] if journeys else None,
                            requirements="requests" in load_json(run / "run.json"),
                            dataflow=bool(explained.exists() and (load_json(explained).get("function_map") or {}).get("areas")))
    for p in paths:
        print(f"Screenshot: {p}")
    if not paths:
        print(f"Chrome did not produce screenshots. Open the report and look: {report}")
        return 1
    url = Path(report).resolve().as_uri() + (f"?select={quote(top, safe='/')}" if top else "")
    ok = _print_layout(shot.layout_report(shot.dump_dom(chrome, url)), top)
    print("NEXT: open every screenshot and check: the flowchart reads left to right and no cards overlap; the "
          "selected file's panel explains it; a journey shows numbered steps that follow the route; the overview diagrams are readable and the counts match the ledger; "
          "the requirements tab (requirements.png) lists the user's asks grouped by area with counts that match check; "
          "with a function map, the flowchart opens on the project's parts and dataflow.png shows what they read and write, top to bottom; "
          "the phone view has no text running off the edge. Fix and re-render if not.")
    return 0 if ok else 1


def _print_layout(rep: dict, top: str | None) -> bool:
    if not rep["done"]:
        print("Layout check: the flowchart did not finish drawing in headless Chrome. Open the report and look; "
              "a script error is the usual cause.")
        return False
    if rep["overlaps"]:
        pairs = "; ".join(f"{a} ↔ {b}" for a, b in rep["overlaps"][:10])
        print(f"Layout check FAILED: {len(rep['overlaps'])} pairs of cards overlap: {pairs}")
        return False
    if top and rep["selected"] != [top]:
        print(f"Layout check FAILED: opening the page with ?select={top} selected {rep['selected'] or 'nothing'}")
        return False
    sel = f"; selected {top}" if top else ""
    print(f"Layout check: {len(rep['nodes'])} cards drawn, none overlap{sel}.")
    return True


def do_retention(args) -> int:
    path = Path(args.settings).expanduser() if args.settings else claude_settings_path()
    days, source = read_retention(path)
    if args.set is None:
        print(f"Claude Code keeps transcripts for {days} days ({source}; {path}).")
        return 0
    if args.set < 1:
        print("error: --set needs a number of days of at least 1")
        return 2
    data, backup = {}, None
    if path.exists():
        text = path.read_text(encoding="utf-8")
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            print(f"error: {path} is not valid JSON; leaving it untouched")
            return 2
        backup = path.with_name(path.name + ".vibe-ledger.bak")
        backup.write_text(text, encoding="utf-8")
    data["cleanupPeriodDays"] = args.set
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Set cleanupPeriodDays to {args.set} in {path}" + (f" (backup: {backup})" if backup else ""))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="vl.py", description=__doc__)
    ap.add_argument("--version", action="version", version=f"vibe-ledger {__version__}")
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("start", help="find the conversations, write reading packs, run probes")
    p.add_argument("--project", required=True)
    p.add_argument("--lang", choices=("zh", "en"))
    p.add_argument("--claude-dir")
    p.add_argument("--codex-dir")
    p = sub.add_parser("merge", help="merge part files into ledger.json, explain.json and requirements.json")
    p.add_argument("--project", required=True)
    p.add_argument("--parts-dir")
    p = sub.add_parser("check", help="verify ledger.json")
    p.add_argument("--project", required=True)
    p.add_argument("--ledger")
    p.add_argument("--explain")
    p.add_argument("--requirements")
    p = sub.add_parser("render", help="write the HTML report")
    p.add_argument("--project", required=True)
    p.add_argument("--lang", choices=("zh", "en"))
    p.add_argument("--out-dir")
    which = p.add_mutually_exclusive_group()
    which.add_argument("--compare", help="an earlier run folder to compare with (default: the previous finished run)")
    which.add_argument("--no-compare", action="store_true", help="do not compare with an earlier run")
    p = sub.add_parser("shot", help="screenshot the report")
    p.add_argument("--project", required=True)
    p = sub.add_parser("retention", help="show or change how long Claude Code keeps transcripts")
    p.add_argument("--set", type=int)
    p.add_argument("--settings")
    args = ap.parse_args(argv)
    return {"start": do_start, "merge": do_merge, "check": do_check, "render": do_render,
            "shot": do_shot, "retention": do_retention}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
