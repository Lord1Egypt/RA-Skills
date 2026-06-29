# SPDX-License-Identifier: MIT
"""`rtc-work` — RIP-302 agent job-market client.

    rtc-work jobs                       list open jobs
    rtc-work watch                      poll for jobs matching agent.toml
    rtc-work claim  <job_id>            reserve a job (no money moves)
    rtc-work deliver <job_id> --url U --summary S
    rtc-work rep [wallet]               show reputation

Endpoints (pinned to rip302_agent_economy.py on the live node):
    GET  /agent/jobs?status=open&category=&min_reward=&limit=
    GET  /agent/jobs/<id>            GET /agent/reputation/<wallet>
    POST /agent/jobs/<id>/claim      {worker_wallet}
    POST /agent/jobs/<id>/deliver    {worker_wallet, deliverable_url|result_summary, deliverable_hash}

Guardrails: claim/deliver require explicit confirmation unless --yes; --node
points at a testnet; watch is read-only. Flat routing — NOT DAG recursion.
"""

import argparse
import json
import os
import time
import urllib.parse
import urllib.request

NODE_URL = "https://rustchain.org"
C = {"g": "\033[32m", "y": "\033[33m", "c": "\033[36m", "d": "\033[2m",
     "b": "\033[1m", "r": "\033[31m", "x": "\033[0m"}


# --- manifest --------------------------------------------------------------------

def load_manifest(path="agent.toml"):
    """Load agent.toml: wallet, skills (categories), min_reward. Tolerant parser
    (stdlib tomllib if available, else a tiny key=value fallback)."""
    if not os.path.exists(path):
        return {}
    try:
        import tomllib
        with open(path, "rb") as f:
            data = tomllib.load(f)
        a = data.get("agent", data)
        return {
            "wallet": a.get("wallet", ""),
            "skills": [s.lower() for s in a.get("skills", [])],
            "min_reward": float(a.get("min_reward", 0)),
            "node": a.get("node", NODE_URL),
        }
    except Exception:
        out = {"skills": [], "min_reward": 0.0, "wallet": "", "node": NODE_URL}
        for line in open(path):
            line = line.split("#", 1)[0].strip()
            if "=" not in line:
                continue
            k, v = (x.strip() for x in line.split("=", 1))
            v = v.strip('"').strip("'")
            if k == "skills":
                out["skills"] = [s.strip().strip('"').strip("'").lower()
                                 for s in v.strip("[]").split(",") if s.strip()]
            elif k == "min_reward":
                try: out["min_reward"] = float(v)
                except ValueError: pass
            elif k in ("wallet", "node"):
                out[k] = v
        return out


# --- http ------------------------------------------------------------------------

def _get(node, path):
    with urllib.request.urlopen(node.rstrip("/") + path, timeout=20) as r:
        return json.loads(r.read().decode())


def _post(node, path, payload):
    req = urllib.request.Request(
        node.rstrip("/") + path, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return True, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try: return False, json.loads(e.read().decode())
        except Exception: return False, {"error": f"HTTP {e.code}"}
    except Exception as e:
        return False, {"error": str(e)}


def fetch_jobs(node, category="", min_reward=0.0, limit=50):
    q = {"status": "open", "min_reward": min_reward, "limit": limit}
    if category:
        q["category"] = category
    path = "/agent/jobs?" + urllib.parse.urlencode(q)
    data = _get(node, path)
    return data.get("jobs", data) if isinstance(data, dict) else data


# --- matching (pure, testable offline) -------------------------------------------

def match_jobs(jobs, skills, min_reward):
    """Filter+rank open jobs by skill (category/tags) and reward floor.

    Pure function — no network — so it's unit-testable. Returns jobs sorted by
    reward desc. Empty `skills` matches everything (reward floor still applies).
    """
    skills = set(s.lower() for s in (skills or []))
    out = []
    for j in jobs or []:
        if (j.get("status", "open") or "open").lower() != "open":
            continue
        reward = float(j.get("reward_rtc", 0) or 0)
        if reward < float(min_reward or 0):
            continue
        if skills:
            cat = (j.get("category", "") or "").lower()
            tags = j.get("tags", "")
            tagset = set(t.strip().lower() for t in
                         (tags.split(",") if isinstance(tags, str) else (tags or [])))
            if cat not in skills and not (skills & tagset):
                continue
        out.append(j)
    out.sort(key=lambda j: float(j.get("reward_rtc", 0) or 0), reverse=True)
    return out


def _confirm(prompt, args):
    if getattr(args, "yes", False):
        return True
    try:
        return input(f"  {C['y']}{prompt} [y/N] {C['x']}").strip().lower() in ("y", "yes")
    except (EOFError, KeyboardInterrupt):
        return False


# --- commands --------------------------------------------------------------------

def cmd_jobs(args):
    node = args.node or NODE_URL
    jobs = fetch_jobs(node, args.category or "", args.min_reward or 0.0)
    if not jobs:
        print(f"{C['d']}No open jobs.{C['x']}"); return 0
    for j in jobs:
        print(f"  {C['b']}{j.get('reward_rtc','?')} RTC{C['x']}  "
              f"[{j.get('category','?')}] {j.get('title','(untitled)')}  "
              f"{C['d']}{j.get('job_id','')[:16]}{C['x']}")
    return 0


def cmd_watch(args):
    m = load_manifest(args.manifest)
    node = args.node or m.get("node") or NODE_URL
    skills = (args.skills.split(",") if args.skills else m.get("skills", []))
    min_reward = args.min_reward if args.min_reward is not None else m.get("min_reward", 0.0)
    wallet = m.get("wallet", "")
    print(f"{C['c']}watching{C['x']} node={node} skills={skills or 'any'} "
          f"min_reward={min_reward} {'(auto-claim)' if args.auto else '(report-only)'}")
    seen = set()
    while True:
        try:
            jobs = match_jobs(fetch_jobs(node), skills, min_reward)
        except Exception as e:
            print(f"{C['r']}poll error: {e}{C['x']}"); time.sleep(args.interval); continue
        for j in jobs:
            jid = j.get("job_id")
            if jid in seen:
                continue
            seen.add(jid)
            print(f"  {C['g']}match{C['x']} {j.get('reward_rtc')} RTC "
                  f"[{j.get('category')}] {j.get('title')} {C['d']}{jid[:16]}{C['x']}")
            if args.auto and wallet:
                if _confirm(f"auto-claim {jid[:16]}?", args):
                    ok, r = _post(node, f"/agent/jobs/{jid}/claim", {"worker_wallet": wallet})
                    print(f"    {'claimed' if ok and not r.get('error') else 'claim failed: '+str(r.get('error'))}")
        if args.once:
            return 0
        time.sleep(args.interval)


def cmd_claim(args):
    node = args.node or NODE_URL
    wallet = args.wallet or load_manifest(args.manifest).get("wallet", "")
    if not wallet:
        print(f"{C['r']}No wallet (set --wallet or agent.toml).{C['x']}"); return 1
    print(f"  claim job {args.job_id[:16]} as {wallet}")
    if not _confirm("claim this job?", args):
        print(f"{C['d']}cancelled.{C['x']}"); return 1
    ok, r = _post(node, f"/agent/jobs/{args.job_id}/claim", {"worker_wallet": wallet})
    print(f"{C['g']}claimed{C['x']}" if ok and not r.get("error") else f"{C['r']}{r}{C['x']}")
    return 0 if ok and not r.get("error") else 1


def cmd_deliver(args):
    node = args.node or NODE_URL
    wallet = args.wallet or load_manifest(args.manifest).get("wallet", "")
    if not (args.url or args.summary):
        print(f"{C['r']}Need --url or --summary.{C['x']}"); return 1
    payload = {"worker_wallet": wallet, "deliverable_url": args.url or "",
               "result_summary": args.summary or "", "deliverable_hash": args.hash or ""}
    print(f"  deliver job {args.job_id[:16]}: url={args.url or '-'} summary={(args.summary or '')[:40]}")
    if not _confirm("submit this delivery?", args):
        print(f"{C['d']}cancelled.{C['x']}"); return 1
    ok, r = _post(node, f"/agent/jobs/{args.job_id}/deliver", payload)
    print(f"{C['g']}delivered{C['x']}" if ok and not r.get("error") else f"{C['r']}{r}{C['x']}")
    return 0 if ok and not r.get("error") else 1


def cmd_rep(args):
    node = args.node or NODE_URL
    wallet = args.wallet or load_manifest(args.manifest).get("wallet", "")
    if not wallet:
        print(f"{C['r']}No wallet.{C['x']}"); return 1
    print(json.dumps(_get(node, f"/agent/reputation/{wallet}"), indent=2))
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="rtc-work", description="RIP-302 agent job-market client")
    p.add_argument("--node", default=None, help=f"node URL (default {NODE_URL})")
    p.add_argument("--manifest", default="agent.toml", help="agent manifest path")
    p.add_argument("--wallet", default=None, help="worker wallet (overrides manifest)")
    p.add_argument("--yes", "-y", action="store_true", help="skip confirmations")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("jobs", help="list open jobs")
    s.add_argument("--category", default=""); s.add_argument("--min-reward", dest="min_reward", type=float, default=0.0)
    s.set_defaults(func=cmd_jobs)

    s = sub.add_parser("watch", help="poll for matching jobs")
    s.add_argument("--skills", default=""); s.add_argument("--min-reward", dest="min_reward", type=float, default=None)
    s.add_argument("--interval", type=int, default=60); s.add_argument("--auto", action="store_true",
                   help="auto-claim matches (still confirms unless --yes)")
    s.add_argument("--once", action="store_true", help="one poll then exit")
    s.set_defaults(func=cmd_watch)

    s = sub.add_parser("claim", help="claim a job"); s.add_argument("job_id"); s.set_defaults(func=cmd_claim)
    s = sub.add_parser("deliver", help="deliver a claimed job"); s.add_argument("job_id")
    s.add_argument("--url", default=""); s.add_argument("--summary", default=""); s.add_argument("--hash", default="")
    s.set_defaults(func=cmd_deliver)
    s = sub.add_parser("rep", help="show reputation"); s.set_defaults(func=cmd_rep)

    args = p.parse_args(argv)
    return args.func(args) or 0


if __name__ == "__main__":
    raise SystemExit(main())
