#!/usr/bin/env python3
"""run_checks.py - runs checks/questions.json through scripts/aa.py and reports pass or fail.

This checks OUR DATA PATH (the live API and the script), not a language model.
Python standard library only. About 25 API calls, paced. Usage:

  python run_checks.py            run all 25
  python run_checks.py q06 q15    run only those
Exit code 0 = all passed, 1 = at least one failed.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AA = os.path.join(HERE, "..", "scripts", "aa.py")
ENVELOPE_KEYS = ("request_url", "source", "record_date", "fetched_at", "credit")


def run(cmd):
    r = subprocess.run([sys.executable, AA] + cmd, capture_output=True, text=True, encoding="utf-8",
                       env=dict(os.environ, PYTHONUTF8="1"))
    if r.returncode != 0:
        return None, (r.stderr or r.stdout).strip()
    return json.loads(r.stdout), None


MISSING = object()


def dig(obj, path):
    """Dotted path. 'a.b[].c' maps over a list and returns a list. Missing -> MISSING."""
    cur = obj
    parts = path.split(".")
    for i, part in enumerate(parts):
        if part.endswith("[]"):
            key = part[:-2]
            cur = cur.get(key, MISSING) if isinstance(cur, dict) else MISSING
            if not isinstance(cur, list):
                return MISSING
            rest = ".".join(parts[i + 1:])
            return [dig(x, rest) if rest else x for x in cur]
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return MISSING
    return cur


def evaluate(check, env):
    v = dig(env, check["path"])
    notes = []
    ok = True
    if check.get("unrecorded"):
        if not (v is MISSING or v is None):
            ok = False
            notes.append("expected UNRECORDED but the record holds %r" % (v,))
    if "equals" in check and v != check["equals"]:
        ok = False
        notes.append("expected %r, got %r" % (check["equals"], None if v is MISSING else v))
    if "equals_str" in check and str(v) != check["equals_str"]:
        ok = False
        notes.append("expected %r, got %r" % (check["equals_str"], None if v is MISSING else v))
    if "contains" in check and not (isinstance(v, str) and check["contains"] in v):
        ok = False
        notes.append("expected text containing %r, got %r" % (check["contains"], None if v is MISSING else v))
    if "all_equal" in check:
        if not isinstance(v, list) or any(x != check["all_equal"] for x in v):
            ok = False
            notes.append("expected every item to equal %r, got %r" % (check["all_equal"], None if v is MISSING else v))
    if "all_startwith" in check:
        if not isinstance(v, list) or any(not (isinstance(x, str) and x.startswith(check["all_startwith"])) for x in v):
            ok = False
            notes.append("expected every item to start with %r" % check["all_startwith"])
    if "min_len" in check and not (isinstance(v, list) and len(v) >= check["min_len"]):
        ok = False
        notes.append("expected a list of at least %d" % check["min_len"])
    if "min_len_at" in check:
        w = dig(env, check["min_len_at"][0])
        if not (isinstance(w, list) and len(w) >= check["min_len_at"][1]):
            ok = False
            notes.append("expected %s to hold at least %d items" % tuple(check["min_len_at"]))
    if "also" in check:
        ok2, n2 = evaluate(check["also"], env)
        ok = ok and ok2
        notes += n2
    return ok, notes


def main():
    want = set(sys.argv[1:])
    qs = json.load(open(os.path.join(HERE, "questions.json"), encoding="utf-8"))["questions"]
    cache, passed, failed = {}, 0, []
    unrec = 0
    for q in qs:
        if want and q["id"] not in want:
            continue
        key = tuple(q["cmd"])
        if key not in cache:
            cache[key] = run(q["cmd"])
        env, err = cache[key]
        if env is None:
            failed.append(q["id"])
            print("FAIL %s  %s\n     could not run: %s" % (q["id"], q["question"], err))
            continue
        ok, notes = evaluate(q["check"], env)
        # Every output must keep its url, source, record date and credit.
        for k in ENVELOPE_KEYS:
            if not env.get(k):
                ok = False
                notes.append("output is missing %s" % k)
        if q["cmd"][0] == "camp" and not str(dig(env, "data.camp.url")).startswith("https://davelalande.com/camps/"):
            ok = False
            notes.append("camp record has no url")
        if q["right_answer"].startswith("unrecorded") or q["check"].get("unrecorded"):
            unrec += 1
        if ok:
            passed += 1
            print("PASS %s  %s -> %s" % (q["id"], q["question"], q["right_answer"]))
        else:
            failed.append(q["id"])
            print("FAIL %s  %s\n     %s" % (q["id"], q["question"], "; ".join(notes)))
            print("     record: %s" % q["record_url"])
    print("\n%d passed, %d failed, %d of the questions have 'unrecorded' as the right answer." % (passed, len(failed), unrec))
    if failed:
        print("FAILED: " + ", ".join(failed) + ". Read each one: a failure may be a data change or a real data problem.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
