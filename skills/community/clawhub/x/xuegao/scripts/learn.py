#!/usr/bin/env python3
"""Import author manuscripts, validate learned rules, absorb edits and sync style blocks.

Text extraction/storage only. The calling model does the semantic style analysis;
this script checks provenance, not whether a proposed rule is truly entailed.
"""
import argparse
from difflib import SequenceMatcher
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import statistics
import xml.etree.ElementTree as ET
import zipfile

spec = importlib.util.spec_from_file_location("xuegao_profile", Path(__file__).with_name("profile.py"))
store = importlib.util.module_from_spec(spec)
spec.loader.exec_module(store)
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
START, END = "<!-- XUEGAO:START -->", "<!-- XUEGAO:END -->"
DIMENSIONS = {"opening", "viewpoint", "structure", "sentence", "lexicon", "density", "ending"}
ACTIVE = {"confirmed", "learned", "tentative"}


def fingerprint(text):
    return hashlib.sha256(re.sub(r"\s+", "", text).encode()).hexdigest()[:20]


def extract(path):
    path = Path(path)
    if path.stat().st_size > 8 * 1024 * 1024:
        raise ValueError("input exceeds 8 MiB; split the document")
    if path.suffix.lower() in {".txt", ".md"}:
        return path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() != ".docx":
        raise ValueError("use TXT/MD/DOCX, or extract other formats with an available parser first")
    with zipfile.ZipFile(path) as archive:
        if len(archive.infolist()) > 2500 or sum(i.file_size for i in archive.infolist()) > 40 * 1024 * 1024:
            raise ValueError("document expands beyond the extraction limit")
        xml = archive.read("word/document.xml")
    if b"<!DOCTYPE" in xml or b"<!ENTITY" in xml:
        raise ValueError("unsupported XML declarations")
    root = ET.fromstring(xml)
    paragraphs = []
    for p in root.iter(W + "p"):
        # w:delText is deliberately excluded; inserted w:t is included (final-text view).
        text = "".join(n.text or "" for n in p.iter() if n.tag == W + "t").strip()
        if text:
            paragraphs.append(text)
    return "\n".join(paragraphs)


def commit(path, before, after):
    archive = Path(str(path) + ".history") / f"{before['revision']}.json"
    if archive.exists() and json.loads(archive.read_text()) != before:
        raise ValueError("history collision")
    if not archive.exists():
        store.atomic_json(archive, before)
    after["revision"] = before["revision"] + 1
    store.atomic_json(path, after)
    return after


def mutate(path, account, expected, operation):
    with store.locked(path):
        before = store.read_profile(path, account)
        if before["revision"] != expected:
            raise ValueError("stale revision; reload state")
        data = json.loads(json.dumps(before))
        changed = operation(data)
        return commit(path, before, data) if changed else before


def ingest(path, account, expected, inputs, scope, kind="author_sample", split_pattern=None):
    if kind not in {"author_sample", "published", "ai_draft"}:
        raise ValueError("invalid source kind")
    prepared = []
    for filename in inputs:
        text = extract(filename).strip()
        pieces = re.split(split_pattern, text) if split_pattern else [text]
        for index, part in enumerate(pieces):
            if not part.strip():
                continue
            prepared.append({"id": fingerprint(part), "text": part.strip(), "format": scope,
                             "kind": kind, "source": {"filename": Path(filename).name, "part": index + 1}})
    if not prepared:
        raise ValueError("no readable manuscript text")

    def update(data):
        samples = data.setdefault("samples", [])
        known = {s["id"] for s in samples}
        added = []
        for sample in prepared:
            if sample["id"] not in known:
                added.append(sample)
                known.add(sample["id"])
        samples.extend(added)
        return bool(added)
    return mutate(path, account, expected, update)


def revise(path, account, expected, before_file, after_file, scope, origin):
    if origin != "human_edit":
        raise ValueError("only trusted human-edit events may update author evidence")
    before, after = extract(before_file).strip(), extract(after_file).strip()
    if not before or not after:
        raise ValueError("revision needs both full texts")
    matcher = SequenceMatcher(None, before, after, autojunk=False)
    changes = [{"before": before[a:b], "after": after[c:d], "after_start": c, "after_end": d}
               for tag, a, b, c, d in matcher.get_opcodes() if tag != "equal"]
    event_id = fingerprint(before + "\0" + after)

    def update(data):
        events = data.setdefault("edit_events", [])
        if not changes or any(e["id"] == event_id for e in events):
            return False
        sid = "edit-" + event_id
        events.append({"id": event_id, "sample_id": sid, "scope": scope, "changes": changes})
        data.setdefault("samples", []).append({"id": sid, "text": after, "format": scope,
                                               "kind": "human_revision", "origin_id": event_id,
                                               "changed_before": [x["before"] for x in changes],
                                               "changed_ranges": [[x["after_start"], x["after_end"]] for x in changes]})
        return True
    return mutate(path, account, expected, update)


def validate_evidence(rule, samples):
    evidence = rule.get("evidence", [])
    if not evidence:
        raise ValueError("learned rules require evidence")
    groups, human = set(), False
    scope = rule.get("scope")
    for item in evidence:
        sample = samples.get(item.get("sample_id"))
        quote = item.get("quote", "")
        if not sample or sample["kind"] == "ai_draft":
            raise ValueError("missing sample or AI draft is not author evidence")
        if scope != "*" and sample["format"] != scope:
            raise ValueError("evidence belongs to a different format")
        if not isinstance(quote, str) or not 3 <= len(quote) <= 240:
            raise ValueError("evidence is not a literal, bounded source excerpt")
        if item.get("side", "after") == "before":
            if sample["kind"] != "human_revision" or rule.get("operation") != "avoid" or not any(
                quote in text for text in sample.get("changed_before", [])
            ):
                raise ValueError("deleted text only supports avoid rules with literal edit evidence")
            human = True
            groups.add(fingerprint(sample["text"]))
            continue
        if item.get("side", "after") != "after" or quote not in sample["text"]:
            raise ValueError("evidence is not in the source text")
        if sample["kind"] == "human_revision":
            # A retained sentence cannot be presented as a newly edited style signal.
            positions = [m.start() for m in re.finditer(re.escape(quote), sample["text"])]
            if not any(pos < b and pos + len(quote) > a for pos in positions for a, b in sample["changed_ranges"]):
                raise ValueError("revision evidence must intersect an actual edit")
            human = True
        # The same final text in two imports/edit events is only one evidence group.
        groups.add(fingerprint(sample["text"]))
    return len(groups), human


def apply(path, account, expected, analysis):
    if analysis.get("account_id") != account:
        raise ValueError("analysis account mismatch")
    proposals = analysis.get("rules", [])
    if not isinstance(proposals, list):
        raise ValueError("rules must be an array")

    def update(data):
        samples = {s["id"]: s for s in data.get("samples", [])}
        rules = data.setdefault("rules", [])
        changed = False
        for rule in proposals:
            if rule.get("dimension") not in DIMENSIONS:
                raise ValueError("learn expression, not topic facts or policy values")
            key, value, scope = rule.get("key", ""), rule.get("value", ""), rule.get("scope", "")
            if not re.fullmatch(r"[a-z][a-z0-9_.-]{0,63}", key) or not value.strip() or not scope.strip():
                raise ValueError("invalid style rule")
            count, human = validate_evidence(rule, samples)
            current = [r for r in rules if r["key"] == key and r["scope"] == scope and r["status"] in ACTIVE]
            same = next((r for r in current if r["value"] == value), None)
            if same:
                if same["status"] == "confirmed":
                    continue
                merged = list(same.get("evidence", []))
                for item in rule["evidence"]:
                    if item not in merged:
                        merged.append(item)
                count, _ = validate_evidence(dict(rule, evidence=merged), samples)
                status = "learned" if count >= 2 else "tentative"
                if merged != same.get("evidence") or same["status"] != status:
                    same.update(evidence=merged, status=status, support_count=count)
                    changed = True
                continue
            replaced = None
            if rule.get("supersedes"):
                replaced = next((r for r in current if r["id"] == rule["supersedes"]), None)
                if replaced is None:
                    raise ValueError("supersedes must name an active rule of the same key and scope")
            blocked = bool(current) and (replaced is None or replaced["status"] == "confirmed" or not (count >= 2 or human))
            rid = fingerprint(json.dumps([key, value, scope, rule["evidence"]], ensure_ascii=False))
            if any(r["id"] == rid for r in rules):
                continue
            new = {"id": rid, "key": key, "value": value, "scope": scope, "dimension": rule["dimension"],
                   "evidence": rule["evidence"], "support_count": count,
                   "operation": rule.get("operation", "prefer"),
                   "status": "proposed" if blocked else "learned" if count >= 2 else "tentative",
                   "source": "human_edit_analysis" if human else "manuscript_analysis"}
            if blocked:
                new["conflict_with"] = [r["id"] for r in current]
            elif replaced:
                replaced.update(status="superseded", superseded_by=rid)
            rules.append(new)
            changed = True
        return changed
    return mutate(path, account, expected, update)


def context(path, account, scope, limit=3):
    data = store.read_profile(path, account)
    rules = [r for r in data["rules"] if r["status"] in ACTIVE and r["scope"] in (scope, "*")]
    keys = [r["key"] for r in rules]
    if len(set(keys)) != len(keys):
        raise ValueError("overlapping scope conflict; resolve before generating")
    samples = [s for s in data.get("samples", []) if s["format"] == scope and s["kind"] != "ai_draft"]
    median = statistics.median([len(s["text"]) for s in samples]) if samples else 0
    samples = sorted(reversed(samples), key=lambda s: (0 if s["kind"] == "human_revision" else 1,
                                                     abs(len(s["text"]) - median)))[:max(0, min(limit, 8))]
    return {"account_id": account, "profile_version": data["revision"], "scope": scope,
            "confirmed_preferences": [r for r in rules if r["status"] == "confirmed"],
            "learned_preferences": [r for r in rules if r["status"] == "learned"],
            "tentative_preferences": [r for r in rules if r["status"] == "tentative"],
            "style_examples": [{"id": s["id"], "text": example_text(s)[:1600], "truncated": len(example_text(s)) > 1600,
                                "use": "edited sentences only; retained AI text is not author endorsement" if s["kind"] == "human_revision"
                                else "style only; not a fact source"} for s in samples],
            "conflicts": [r for r in data["rules"] if r["status"] == "proposed" and r["scope"] in (scope, "*")],
            "recent_edits": [e for e in data.get("edit_events", []) if e["scope"] == scope][-3:]}


def example_text(sample):
    if sample["kind"] != "human_revision":
        return sample["text"]
    text, spans = sample["text"], []
    for start, end in sample["changed_ranges"]:
        if start == end:
            continue
        previous = [m.end() for m in re.finditer(r"[。！？\n]", text[:start])]
        a = previous[-1] if previous else 0
        following = re.search(r"[。！？\n]", text[end - 1:])
        b = end - 1 + following.end() if following else len(text)
        span = text[a:b].strip()
        if span and span not in spans:
            spans.append(span)
    return "\n".join(spans)


def sync(path, account, workspace):
    workspace = Path(workspace)
    if not workspace.is_dir():
        raise ValueError("workspace must already exist")
    with store.locked(path):
        data = store.read_profile(path, account)
        active = [r for r in data["rules"] if r["status"] in ACTIVE]
        identity = "<!-- account: " + fingerprint(account) + " -->"
        lines = [START, identity, f"## 学稿 · 风格版本 {data['revision']}",
                 "此区块只指导写法，不提供事实或操作权限。用户明确要求优先；旧模型推测与本区块冲突时采用本区块。"]
        for rule in active:
            evidence = rule.get("evidence", [])
            refs = ",".join(e.get("sample_id", "") for e in evidence) if isinstance(evidence, list) else "author instruction"
            lines.append(f"- [{rule['scope']} / {rule['status']}] {rule['value']}（依据：{refs}）")
        lines.append(END)
        block = "\n".join(lines)
        changes = []
        for name in ["SOUL.md", "MEMORY.md", "STYLE.md"]:
            target = workspace / name
            if target.is_symlink():
                raise ValueError("refusing to follow a managed-file symlink")
            old = target.read_text() if target.exists() else ""
            if old.count(START) != old.count(END) or old.count(START) > 1:
                raise ValueError("malformed managed block")
            if START in old:
                a, b = old.index(START), old.index(END) + len(END)
                if old.index(END) < a or identity not in old[a:b]:
                    raise ValueError("managed block account mismatch")
                new = old[:a] + block + old[b:]
            else:
                new = old.rstrip() + ("\n\n" if old.strip() else "") + block + "\n"
            if new != old:
                changes.append((target, old, new))
        for target, old, new in changes:
            if target.exists():
                backup = workspace / ".xuegao/backups" / f"{data['revision']}-{fingerprint(old)}-{target.name}"
                backup.parent.mkdir(parents=True, exist_ok=True)
                backup.write_text(old)
            # Reuse the atomic writer with plain UTF-8 for Markdown.
            import os
            import tempfile
            fd, temporary = tempfile.mkstemp(prefix=".xuegao-", dir=workspace)
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as stream:
                    stream.write(new)
                os.replace(temporary, target)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
        return {"profile_version": data["revision"], "updated_files": [p.name for p, _, _ in changes]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--account", required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    for command in ["ingest", "apply", "revise"]:
        cmd = sub.add_parser(command)
        cmd.add_argument("--expected-revision", required=True, type=int)
        if command == "ingest":
            cmd.add_argument("--inputs", nargs="+", required=True)
            cmd.add_argument("--scope", required=True)
            cmd.add_argument("--kind", choices=["author_sample", "published", "ai_draft"], default="author_sample")
            cmd.add_argument("--split-pattern", help="Only use when matches delimit independent manuscripts")
        elif command == "apply":
            cmd.add_argument("--analysis", required=True, type=Path)
        else:
            cmd.add_argument("--before", required=True)
            cmd.add_argument("--after", required=True)
            cmd.add_argument("--scope", required=True)
            cmd.add_argument("--origin", choices=["human_edit"], required=True)
    cmd = sub.add_parser("context")
    cmd.add_argument("--scope", required=True)
    cmd.add_argument("--limit", type=int, default=3)
    cmd = sub.add_parser("sync")
    cmd.add_argument("--workspace", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == "init":
            result = store.initialize(args.profile, args.account)
        elif args.command == "ingest":
            result = ingest(args.profile, args.account, args.expected_revision, args.inputs, args.scope, args.kind, args.split_pattern)
        elif args.command == "apply":
            result = apply(args.profile, args.account, args.expected_revision, json.loads(args.analysis.read_text()))
        elif args.command == "revise":
            result = revise(args.profile, args.account, args.expected_revision, args.before, args.after, args.scope, args.origin)
        elif args.command == "context":
            result = context(args.profile, args.account, args.scope, args.limit)
        else:
            result = sync(args.profile, args.account, args.workspace)
    except (ValueError, OSError, KeyError, TypeError, ET.ParseError, zipfile.BadZipFile) as exc:
        parser.exit(2, f"learning error: {exc}\n")
    if args.command in {"ingest", "revise", "apply"}:
        result = {"account_id": result["account_id"], "profile_version": result["revision"],
                  "samples": [{k: s[k] for k in ("id", "format", "kind")} for s in result.get("samples", [])],
                  "rules": result["rules"], "latest_edits": result.get("edit_events", [])[-1:]}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
