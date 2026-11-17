#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Undo-First Guard — reversible-action infrastructure for AI agents.

Philosophy: NO UNDO PATH, NO ACTION. Before any side effect:
  1. snapshot  — capture verifiable state (sha256 manifest + backup copies)
  2. plan      — register an undo plan; the risk gate decides if the action may run
  3. act       — (the agent performs the action)
  4. verify    — diff current state against the snapshot
  5. restore   — roll back file-level changes; byte-identical, hash-verified,
                 and remove files created after the snapshot
  6. journal   — tamper-evident (hash-chained) local audit trail of every decision

Design invariants (plans and files are data, never executed):
  - The engine only hashes, copies, and gates; it never runs plan contents.
  - Restore works only from its own backup copies, verified against the manifest.
  - A tampered/corrupt backup is refused, not restored.
  - `selfcheck` is a literal-text heuristic over this file, not a proof.

Stdlib only. Exit codes: 0=ACCEPT  1=ACCEPT_WITH_WARNING  2=REJECT  4=error
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone

VERSION = "1.0.11"
JOURNAL_DIR = ".undo-journal"
SNAP_DIR = "snapshots"
JOURNAL_FILE = "journal.jsonl"

RISK_LEVELS = ["low", "medium", "high", "critical"]
UNDO_KINDS = ["builtin_restore", "commands", "compensation", "none"]
IRREVERSIBLE_TYPES = {"external_message", "deploy", "api_call", "payment", "publish", "delete_remote"}
FILE_TYPES = {"file_write", "file_delete", "file_move", "dir_change", "config_change"}

EXIT = {"ACCEPT": 0, "ACCEPT_WITH_WARNING": 1, "REJECT": 2, "ERROR": 4}


# ---------------------------------------------------------------------------
# Hashing & manifest
# ---------------------------------------------------------------------------
def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_targets(paths):
    """Expand paths to a deterministic list of files (relative to cwd)."""
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, names in os.walk(p):
                dirs[:] = sorted(d for d in dirs if d != JOURNAL_DIR and d != ".git")
                for n in sorted(names):
                    files.append(os.path.join(root, n))
        elif os.path.isfile(p):
            files.append(p)
        else:
            raise FileNotFoundError(p)
    return sorted(set(files))


def build_manifest(files):
    manifest = {}
    for f in files:
        st = os.stat(f)
        manifest[f] = {
            "sha256": sha256_file(f),
            "size": st.st_size,
            "mode": oct(st.st_mode & 0o777),
        }
    return manifest


# ---------------------------------------------------------------------------
# Journal
# ---------------------------------------------------------------------------
def journal_path():
    return os.path.join(JOURNAL_DIR, JOURNAL_FILE)


def _canonical(entry: dict) -> bytes:
    return json.dumps({k: v for k, v in entry.items() if k != "hash"},
                      sort_keys=True, ensure_ascii=False).encode("utf-8")


def _entry_hash(entry: dict) -> str:
    return hashlib.sha256(_canonical(entry)).hexdigest()


def _read_journal():
    if not os.path.exists(journal_path()):
        return []
    entries = []
    with open(journal_path(), "r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                entries.append(json.loads(line))
    return entries


def _last_hash():
    for entry in reversed(_read_journal()):
        if entry.get("hash"):
            return entry["hash"]
    return ""


def journal_write(entry: dict):
    os.makedirs(JOURNAL_DIR, exist_ok=True)
    entry["ts"] = datetime.now(timezone.utc).isoformat()
    entry["version"] = VERSION
    entry["prev"] = _last_hash()
    entry["hash"] = _entry_hash(entry)
    with open(journal_path(), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def verify_journal():
    """Return (entries, problems, legacy_count) for the hash-chained journal."""
    entries = _read_journal()
    problems, legacy, prev = [], 0, ""
    for idx, entry in enumerate(entries, 1):
        stored = entry.get("hash")
        if not stored:
            # Strict: a stripped hash must not be accepted as a legacy entry,
            # otherwise an edited record could silently pass verification.
            legacy += 1
            problems.append("entry %d: missing hash (legacy or stripped) - cannot verify"
                            % idx)
            prev = ""
            continue
        if entry.get("prev", "") != prev:
            problems.append("entry %d: prev-hash link broken" % idx)
        if _entry_hash(entry) != stored:
            problems.append("entry %d: content hash mismatch (entry edited)" % idx)
        prev = stored
    return entries, problems, legacy


# ---------------------------------------------------------------------------
# snapshot
# ---------------------------------------------------------------------------
def cmd_snapshot(args):
    paths = args.paths or ["."]
    files = collect_targets(paths)
    if not files:
        print("nothing to snapshot")
        return EXIT["ERROR"]
    snap_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    snap_root = os.path.join(JOURNAL_DIR, SNAP_DIR, snap_id)
    backup_root = os.path.join(snap_root, "files")
    manifest = build_manifest(files)
    for f in files:
        dst = os.path.join(backup_root, f)
        os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
        shutil.copy2(f, dst)
    meta = {"id": snap_id, "created": datetime.now(timezone.utc).isoformat(),
            "roots": paths, "count": len(files), "manifest": manifest}
    with open(os.path.join(snap_root, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
    journal_write({"action": "snapshot", "snapshot": snap_id, "files": len(files),
                   "roots": paths})
    print("snapshot %s — %d files, manifest sha256-verified backups stored" % (snap_id, len(files)))
    return 0


# ---------------------------------------------------------------------------
# verify — diff current state vs snapshot
# ---------------------------------------------------------------------------
def load_manifest(snap_id):
    path = os.path.join(JOURNAL_DIR, SNAP_DIR, snap_id, "manifest.json")
    if not os.path.exists(path):
        raise FileNotFoundError("snapshot not found: %s" % snap_id)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def state_diff(meta):
    changed, deleted, intact = [], [], []
    for f, info in meta["manifest"].items():
        if not os.path.exists(f):
            deleted.append(f)
        elif sha256_file(f) != info["sha256"]:
            changed.append(f)
        else:
            intact.append(f)
    return changed, deleted, intact


def norm_rel(path: str) -> str:
    return os.path.normpath(path).replace("\\", "/")


def unsafe_destination(path: str) -> bool:
    """True when writing to path would traverse a symlink (directly or via parents)."""
    p = os.path.abspath(path)
    while True:
        if os.path.islink(p):
            return True
        parent = os.path.dirname(p)
        if parent == p:
            return False
        p = parent


def present_under(roots):
    """List regular files currently present under snapshot roots (no links/journal)."""
    present = []
    for p in roots:
        if os.path.isdir(p) and not os.path.islink(p):
            for root, dirs, names in os.walk(p):
                dirs[:] = sorted(d for d in dirs
                                 if d not in (JOURNAL_DIR, ".git")
                                 and not os.path.islink(os.path.join(root, d)))
                for n in sorted(names):
                    fp = os.path.join(root, n)
                    if not os.path.islink(fp):
                        present.append(fp)
        elif os.path.isfile(p) and not os.path.islink(p):
            present.append(p)
    return present


def snapshot_problems(snap_id, targets):
    """Validate a builtin_restore plan against the snapshot it claims to use."""
    if not snap_id:
        return ["undo.kind='builtin_restore' requires undo.snapshot (the snapshot id)"]
    try:
        meta = load_manifest(snap_id)
    except FileNotFoundError:
        return ["snapshot %r not found under %s — take one before acting"
                % (snap_id, os.path.join(JOURNAL_DIR, SNAP_DIR))]
    problems = []
    bad = []
    snap_root = os.path.join(JOURNAL_DIR, SNAP_DIR, str(snap_id), "files")
    for f, info in meta["manifest"].items():
        backup = os.path.join(snap_root, f)
        if not os.path.isfile(backup):
            bad.append("%s (backup missing)" % f)
        elif sha256_file(backup) != info["sha256"]:
            bad.append("%s (backup sha256 mismatch)" % f)
    if bad:
        problems.append("snapshot %r failed integrity check for %d file(s): %s"
                        % (snap_id, len(bad), "; ".join(bad[:5])))
    keys = {norm_rel(f) for f in meta["manifest"]}
    if not targets:
        problems.append("undo.kind='builtin_restore' requires action.target "
                        "(or action.targets) so snapshot coverage can be verified")
    for t in targets:
        n = norm_rel(t)
        if n in keys:
            continue
        if any(k.startswith(n + "/") for k in keys):
            if os.path.isdir(t):
                missing = [f for f in present_under([t]) if norm_rel(f) not in keys]
                if missing:
                    problems.append(
                        "snapshot %r covers only part of target directory %r "
                        "(%d current file(s) are not in the snapshot)"
                        % (snap_id, t, len(missing)))
            continue
        problems.append("snapshot %r does not cover action target %r" % (snap_id, t))
    return problems


def cmd_verify(args):
    meta = load_manifest(args.snapshot)
    changed, deleted, intact = state_diff(meta)
    print("verify %s: intact=%d changed=%d deleted=%d" % (
        args.snapshot, len(intact), len(changed), len(deleted)))
    for f in changed:
        print("  CHANGED %s" % f)
    for f in deleted:
        print("  DELETED %s" % f)
    journal_write({"action": "verify", "snapshot": args.snapshot,
                   "intact": len(intact), "changed": changed, "deleted": deleted})
    return 0


# ---------------------------------------------------------------------------
# restore — rollback from backup, refuse tampered backups
# ---------------------------------------------------------------------------
def cmd_restore(args):
    snap_root = os.path.join(JOURNAL_DIR, SNAP_DIR, args.snapshot)
    meta = load_manifest(args.snapshot)
    changed, deleted, intact = state_diff(meta)
    manifest_keys = {norm_rel(f) for f in meta["manifest"]}
    created = [f for f in present_under(meta.get("roots") or [])
               if norm_rel(f) not in manifest_keys]
    if not args.keep_created and created and not args.yes:
        print("restore plan for %s: %d changed, %d deleted, %d files created after the "
              "snapshot would be overwritten/removed" % (
                  args.snapshot, len(changed), len(deleted), len(created)))
        print("refusing destructive rollback without --yes (explicit confirmation); "
              "pass --keep-created to preserve new files")
        journal_write({"action": "restore_blocked", "snapshot": args.snapshot,
                       "reason": "confirmation required (--yes)",
                       "changed": changed, "deleted": deleted,
                       "created": created})
        return EXIT["ERROR"]
    if (changed or deleted) and not args.yes:
        print("restore plan for %s: %d changed, %d deleted files would be overwritten" % (
            args.snapshot, len(changed), len(deleted)))
        print("refusing destructive rollback without --yes (explicit confirmation)")
        journal_write({"action": "restore_blocked", "snapshot": args.snapshot,
                       "reason": "confirmation required (--yes)",
                       "changed": changed, "deleted": deleted, "created": created})
        return EXIT["ERROR"]
    restored, refused = [], []
    for f in changed + deleted:
        backup = os.path.join(snap_root, "files", f)
        if not os.path.exists(backup):
            refused.append((f, "no backup copy"))
            continue
        recorded = meta["manifest"][f]["sha256"]
        actual = sha256_file(backup)
        if actual != recorded:
            refused.append((f, "backup tampered (sha256 mismatch)"))
            continue
        if unsafe_destination(f):
            refused.append((f, "refusing to restore through a symlink"))
            continue
        os.makedirs(os.path.dirname(f) or ".", exist_ok=True)
        shutil.copy2(backup, f)
        if sha256_file(f) != recorded:
            refused.append((f, "post-restore verification failed"))
            continue
        restored.append(f)
    removed = []
    for f in ([] if args.keep_created else created):
        try:
            os.remove(f)
            removed.append(f)
        except OSError as exc:
            refused.append((f, "created after snapshot and could not be removed: %s" % exc))
    print("restore %s: restored=%d intact=%d removed_created=%d refused=%d" % (
        args.snapshot, len(restored), len(intact), len(removed), len(refused)))
    for f in restored:
        print("  RESTORED (byte-identical, sha256 verified) %s" % f)
    for f in removed:
        print("  REMOVED  (created after snapshot) %s" % f)
    for f, why in refused:
        print("  REFUSED  %s — %s" % (f, why))
    journal_write({"action": "restore", "snapshot": args.snapshot,
                   "restored": restored,
                   "removed_created": removed,
                   "refused": [{"file": f, "reason": why} for f, why in refused]})
    return 0 if not refused else EXIT["ERROR"]


# ---------------------------------------------------------------------------
# plan — risk gate (plans are DATA; this tool never executes plan contents)
# ---------------------------------------------------------------------------
def validate_plan(plan: dict):
    """Return (verdict, [reasons], [warnings]). Deterministic risk-gate rules."""
    reasons, warnings = [], []
    action = plan.get("action") or {}
    undo = plan.get("undo") or {}
    verify = plan.get("verify") or {}
    atype = action.get("type", "unknown")
    risk = plan.get("risk", "unknown")
    kind = undo.get("kind", "none")
    raw_steps = undo.get("steps") or []
    steps = [s for s in raw_steps if isinstance(s, str) and s.strip()]
    targets = action.get("targets")
    if targets is None and action.get("target"):
        targets = [action.get("target")]
    if isinstance(targets, str):
        targets = [targets]
    targets = [str(t) for t in (targets or []) if str(t).strip()]

    if atype not in FILE_TYPES | IRREVERSIBLE_TYPES:
        reasons.append("unknown action.type %r — classify the action first" % atype)
    if risk not in RISK_LEVELS:
        reasons.append("risk must be one of %s" % RISK_LEVELS)
    if kind not in UNDO_KINDS:
        reasons.append("undo.kind must be one of %s" % UNDO_KINDS)

    if atype in IRREVERSIBLE_TYPES:
        if kind != "compensation":
            reasons.append(
                "%s is irreversible in the real world — undo.kind must be 'compensation' "
                "(mitigation steps), not %r" % (atype, kind))
    if kind == "compensation" and not steps:
        reasons.append("undo.kind='compensation' requires non-empty undo.steps "
                       "(concrete mitigation for every action class)")
    if kind == "none":
        reasons.append("undo.kind='none' is not accepted for any side-effecting action — "
                       "take a snapshot (builtin_restore) or provide rollback steps")
    if kind == "builtin_restore":
        reasons.extend(snapshot_problems(undo.get("snapshot"), targets))
    if kind == "commands":
        if not steps:
            reasons.append("undo.kind='commands' requires non-empty undo.steps")
        if not verify.get("check"):
            reasons.append("undo.kind='commands' requires verify.check to prove restoration")
    if risk == "critical" and kind == "builtin_restore" and not verify.get("check"):
        warnings.append("critical risk with builtin_restore — add verify.check for extra assurance")
    if not action.get("description"):
        warnings.append("action.description missing — journal will be hard to audit")

    if reasons:
        return "REJECT", reasons, warnings
    if warnings:
        return "ACCEPT_WITH_WARNING", reasons, warnings
    return "ACCEPT", reasons, warnings


def cmd_plan(args):
    with open(args.plan_file, "r", encoding="utf-8") as fh:
        plan = json.load(fh)
    verdict, reasons, warnings = validate_plan(plan)
    print("PLAN GATE: %s  (%s)" % (verdict, args.plan_file))
    for r in reasons:
        print("  ✗ %s" % r)
    for w in warnings:
        print("  ⚠ %s" % w)
    journal_write({"action": "plan_gate", "plan_file": args.plan_file,
                   "verdict": verdict, "reasons": reasons, "warnings": warnings,
                   "plan": plan})
    return EXIT[verdict]


# ---------------------------------------------------------------------------
# journal / selfcheck
# ---------------------------------------------------------------------------
def cmd_journal(args):
    entries, problems, legacy = verify_journal()
    if not entries:
        print("journal is empty")
        return 0
    if args.verify:
        for p in problems:
            print("  ✗ %s" % p)
        if problems:
            print("journal BROKEN — %d problem(s); %d legacy entr(y/ies) without a hash chain"
                  % (len(problems), legacy))
            return EXIT["ERROR"]
        print("journal OK — %d entries, hash chain intact (legacy entries: %d)"
              % (len(entries), legacy))
        return 0
    for e in entries[-args.last:]:
        print("%s  %-11s %s" % (e.get("ts", "?"), e.get("action", "?"),
                                json.dumps({k: v for k, v in e.items()
                                            if k not in ("ts", "version", "action",
                                                         "plan", "prev", "hash")},
                                           ensure_ascii=False)[:120]))
    return 0


def cmd_selfcheck(args):
    """Heuristic source-text check of this file (not a proof of safety)."""
    src_path = os.path.abspath(__file__)
    with open(src_path, "r", encoding="utf-8") as fh:
        src = fh.read()
    # Build needles without embedding their literals in this source file.
    needles = ["os." + "system", "sub" + "process", "os." + "popen",
               "eval" + "(", "exec" + "(", "__imp" + "ort__",
               "commands." + "getoutput", "pty." + "spawn"]
    hits = [n for n in needles if n in src]
    print("selfcheck: heuristic scan of this source file for listed execution primitives…")
    for n in needles:
        print("  %-22s %s" % (n, "FOUND ✗" if n in hits else "absent ✓"))
    if hits:
        print("SELFCHECK FAILED — a listed execution primitive appears in this source file")
        return EXIT["ERROR"]
    print("SELFCHECK PASSED — none of the listed execution primitives appear in this source "
          "file (heuristic only; not a proof that the code cannot execute anything)")
    journal_write({"action": "selfcheck", "result": "PASS", "kind": "heuristic"})
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(prog="undo_guard",
                                description="Undo-First Guard: snapshot, risk-gated plans, verified restore.")
    ap.add_argument("--version", action="store_true")
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("snapshot", help="capture state + backups of target paths")
    p.add_argument("paths", nargs="*")

    p = sub.add_parser("verify", help="diff current state against a snapshot")
    p.add_argument("snapshot")

    p = sub.add_parser("restore", help="roll back to a snapshot (hash-verified)")
    p.add_argument("snapshot")
    p.add_argument("--yes", action="store_true",
                   help="explicitly confirm overwriting changed files and removing new ones")
    p.add_argument("--keep-created", action="store_true",
                   help="preserve files created after the snapshot")

    p = sub.add_parser("plan", help="risk-gate an undo plan (JSON)")
    p.add_argument("plan_file")

    p = sub.add_parser("journal", help="show the audit trail (tamper-evident hash chain)")
    p.add_argument("--last", type=int, default=20)
    p.add_argument("--verify", action="store_true", help="verify the journal hash chain")

    sub.add_parser("selfcheck", help="heuristically scan this source for listed execution primitives; not a safety proof")

    args = ap.parse_args(argv)
    if args.version:
        print("undo_guard %s" % VERSION)
        return 0
    if not args.cmd:
        ap.print_help()
        return EXIT["ERROR"]

    try:
        return {
            "snapshot": cmd_snapshot, "verify": cmd_verify, "restore": cmd_restore,
            "plan": cmd_plan, "journal": cmd_journal, "selfcheck": cmd_selfcheck,
        }[args.cmd](args)
    except FileNotFoundError as e:
        print("error: %s" % e, file=sys.stderr)
        return EXIT["ERROR"]
    except json.JSONDecodeError as e:
        print("error: invalid plan JSON: %s" % e, file=sys.stderr)
        return EXIT["ERROR"]


if __name__ == "__main__":
    sys.exit(main())
