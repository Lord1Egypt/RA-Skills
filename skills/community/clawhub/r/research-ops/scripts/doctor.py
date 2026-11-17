#!/usr/bin/env python3
"""research-ops: check whether a group root follows the research workspace convention."""
import argparse
import json
import os
import sys

ALLOWED_ROOT_FILES = {"AGENTS.md", "README.md", "INDEX.md", "MEMORY.md", "TODO.md", "research.config.json"}
SKIP = {".tools", ".trash", "buffer", "shared", "archive", "chats", "projects"}


def main():
    ap = argparse.ArgumentParser(description="Audit a research group root")
    ap.add_argument("--root", required=True)
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()

    if not os.path.isdir(a.root):
        print(json.dumps({"status": "error", "message": f"not a dir: {a.root}"}))
        sys.exit(1)

    issues = []

    def add(sev, kind, detail):
        issues.append({"severity": sev, "kind": kind, "detail": detail})

    # dirs listed in INDEX.md are considered declared (flat project layout is allowed)
    declared = ""
    index_path = os.path.join(a.root, "INDEX.md")
    if os.path.isfile(index_path):
        with open(index_path, encoding="utf-8", errors="ignore") as fh:
            declared = fh.read()

    for req in ("AGENTS.md", "INDEX.md"):
        if not os.path.isfile(os.path.join(a.root, req)):
            add("medium", "missing_file", req)

    # root-level stray items (files other than allowed, dirs other than known)
    for name in os.listdir(a.root):
        if name.startswith("."):
            continue  # hidden/infra dirs (.login_tools/.tools/.trash) are allowed
        full = os.path.join(a.root, name)
        if os.path.isfile(full):
            if name not in ALLOWED_ROOT_FILES:
                add("low", "root_stray_file", name)
        elif os.path.isdir(full):
            if name not in SKIP and name not in declared:
                add("low", "root_dir", name)

    # buffer pending（扁平：文件直接放 buffer/）
    buf = os.path.join(a.root, "buffer")
    if os.path.isdir(buf):
        pending = [x for x in os.listdir(buf)
                   if not x.startswith(".") and x not in ("README.md", "_buffer_log.jsonl")]
        if pending:
            add("medium", "buffer_pending", f"{len(pending)} item(s) in buffer/")

    proj_root = os.path.join(a.root, "projects")
    if os.path.isdir(proj_root):
        for name in os.listdir(proj_root):
            p = os.path.join(proj_root, name)
            if os.path.isdir(p) and not name.startswith("."):
                if not os.path.isfile(os.path.join(p, "README.md")):
                    add("low", "project_no_readme", f"projects/{name}")

    by_sev = {}
    for it in issues:
        by_sev[it["severity"]] = by_sev.get(it["severity"], 0) + 1

    print(json.dumps({"status": "ok", "root": os.path.abspath(a.root),
                      "summary": {"by_severity": by_sev, "total": len(issues)},
                      "issues": issues}, ensure_ascii=False, indent=2))
    if a.strict and by_sev.get("high"):
        sys.exit(1)


if __name__ == "__main__":
    main()
