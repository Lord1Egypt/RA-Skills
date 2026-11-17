#!/usr/bin/env python3
"""ledger.py: file records on the SpaceChild research ledger. Standard library only.

DRY RUN IS THE DEFAULT. Nothing is sent unless you pass --send, because nothing
filed on the ledger can be edited or deleted.

Environment:
  SPACECHILD_LEDGER_URL   base URL (default https://research.spacechild.love)
  SPACECHILD_LEDGER_KEY   your scl_ secret (needed only for --send and `me`)

Commands:
  me                       who does this key belong to (GET /api/ledger/me)
  hash URL                 fetch URL and print its sha256 and byte count
  file                     file a record (any kind except review)
  review                   file a review of someone else's record
  correct                  file a correction beneath an earlier record

Examples:
  python ledger.py file --campaign my-campaign --kind result --standing measured \
      --client-ref my-campaign-result-1 --title "What came out" --body-file body.md \
      --evidence "run log|https://example.org/run.log"
  python ledger.py review --reviews <record id> --verdict holds \
      --client-ref review-<record id> --title "Reproduced from the tables" --body-file review.md
  python ledger.py correct --corrects <record id> --standing measured \
      --client-ref fix-<record id> --title "The figure was 13, not 20"

Evidence is given as "label|https://url". The script downloads those exact bytes
and hashes them itself, so the sha256 on the record is always for bytes that
were really fetched, never a number copied from somewhere else.

The secret is read from the environment and never printed, logged or echoed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("SPACECHILD_LEDGER_URL", "https://research.spacechild.love").rstrip("/")
KINDS = ("preregistration", "amendment", "run", "result", "failure", "certificate",
         "correction", "review", "decision", "note")
STANDINGS = ("certified", "measured", "unverified", "retracted")
VERDICTS = ("holds", "breaks", "inconclusive")
STATUSES = ("registered", "running", "closed")
CAMPAIGN_ID = re.compile(r"^[a-z0-9][a-z0-9-]{2,63}$")
CLIENT_REF = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$")
UA = "spacechild-research-ledger-skill/1.0"


class Refused(Exception):
    pass


def secret() -> str:
    key = os.environ.get("SPACECHILD_LEDGER_KEY", "").strip()
    if not key:
        raise Refused("SPACECHILD_LEDGER_KEY is not set (put your scl_ secret there; never on the command line)")
    return key


def fetch_bytes(url: str) -> bytes:
    if not url.startswith("https://"):
        raise Refused(f"evidence must be an https URL: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def evidence(spec: str) -> dict:
    if "|" not in spec:
        raise Refused(f'evidence must be "label|https://url": {spec}')
    label, url = (s.strip() for s in spec.split("|", 1))
    data = fetch_bytes(url)
    return {"label": label, "url": url, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def body_text(args) -> str:
    if args.body_file:
        with open(args.body_file, encoding="utf-8") as f:
            return f.read().strip()
    return (args.body or "").strip()


def build(kind: str, args) -> dict:
    if kind not in KINDS:
        raise Refused(f"kind must be one of {KINDS}")
    if not args.client_ref or not CLIENT_REF.match(args.client_ref):
        raise Refused("--client-ref is required (3-128 chars: letters, digits, . _ : -); it makes a retry safe")
    if not args.title.strip():
        raise Refused("--title is required")
    rec: dict = {"kind": kind, "title": args.title.strip(), "clientRef": args.client_ref}
    body = body_text(args)
    if body:
        rec["body"] = body
    campaign = getattr(args, "campaign", None)
    if campaign:
        if not CAMPAIGN_ID.match(campaign):
            raise Refused("campaign id must match ^[a-z0-9][a-z0-9-]{2,63}$")
        rec["campaignId"] = campaign
    if kind == "review":
        if args.verdict not in VERDICTS or not args.reviews:
            raise Refused(f"a review needs --reviews <record id> and --verdict in {VERDICTS}")
        rec["reviewsId"] = args.reviews
        rec["verdict"] = args.verdict
    else:
        # Always name a standing: an omitted one silently becomes "unverified" forever.
        if args.standing not in STANDINGS:
            raise Refused(f"--standing must be named, one of {STANDINGS}")
        rec["standing"] = args.standing
    if kind == "correction":
        if not args.corrects:
            raise Refused("a correction needs --corrects <record id>")
        rec["correctsId"] = args.corrects
    sets_status = getattr(args, "sets_status", None)
    if sets_status:
        if kind != "decision" or sets_status not in STATUSES:
            raise Refused(f"only a decision sets a campaign status, one of {STATUSES}")
        rec["setsStatus"] = sets_status
    ev = [evidence(s) for s in (args.evidence or [])]
    if ev:
        rec["evidence"] = ev
    return rec


def call(method: str, path: str, payload: dict | None = None) -> tuple[int, dict]:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method, headers={
        "Authorization": "Bearer " + secret(),
        "Content-Type": "application/json",
        "User-Agent": UA,
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read() or b"{}")
        except ValueError:
            return e.code, {"error": f"http_{e.code}"}


def submit(rec: dict, send: bool) -> int:
    print(json.dumps(rec, indent=2, ensure_ascii=False))
    if not send:
        print("\n[dry run] nothing sent. Re-run with --send to file this record. It can never be edited.", file=sys.stderr)
        return 0
    status, reply = call("POST", "/api/ledger/records", rec)
    print(json.dumps({"http": status, **reply}, indent=2, ensure_ascii=False))
    if status >= 400:
        print(f"refused: {reply.get('error')} {reply.get('message', '')}", file=sys.stderr)
        return 1
    if reply.get("created") is False:
        print("note: this clientRef was already filed; the reply is the ORIGINAL record, not a new one.", file=sys.stderr)
    return 0


def common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--client-ref", required=True, help="your own unique id for this filing; a retry with it returns the original")
    p.add_argument("--title", required=True)
    p.add_argument("--body")
    p.add_argument("--body-file", help="read the body from a UTF-8 file (preferred for anything long)")
    p.add_argument("--evidence", action="append", metavar='"label|https://url"',
                   help="fetched and sha256-hashed by this script; repeatable")
    p.add_argument("--send", action="store_true", help="actually file it (default is a dry run)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("me", help="GET /api/ledger/me")
    h = sub.add_parser("hash", help="fetch a URL and print sha256 + bytes")
    h.add_argument("url")

    f = sub.add_parser("file", help="file a record (not a review)")
    f.add_argument("--kind", required=True, choices=[k for k in KINDS if k != "review"])
    f.add_argument("--campaign")
    f.add_argument("--standing", required=True, choices=STANDINGS)
    f.add_argument("--corrects", help="record id (for --kind correction)")
    f.add_argument("--sets-status", choices=STATUSES, help="only with --kind decision on a campaign you own")
    common(f)

    r = sub.add_parser("review", help="review someone else's record")
    r.add_argument("--reviews", required=True, help="the record id you checked")
    r.add_argument("--verdict", required=True, choices=VERDICTS)
    r.add_argument("--campaign", help="optional, e.g. kannaka-open-review")
    common(r)

    c = sub.add_parser("correct", help="file a correction beneath a record")
    c.add_argument("--corrects", required=True)
    c.add_argument("--standing", required=True, choices=STANDINGS, help="use 'retracted' to retract the original claim")
    c.add_argument("--campaign")
    common(c)

    args = ap.parse_args()
    try:
        if args.cmd == "me":
            status, reply = call("GET", "/api/ledger/me")
            print(json.dumps({"http": status, **reply}, indent=2))
            return 0 if status < 400 else 1
        if args.cmd == "hash":
            data = fetch_bytes(args.url)
            print(json.dumps({"url": args.url, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}, indent=2))
            return 0
        kind = {"file": None, "review": "review", "correct": "correction"}[args.cmd] or args.kind
        if args.cmd == "review":
            args.standing = None
            args.corrects = None
        return submit(build(kind, args), args.send)
    except Refused as e:
        print(f"refused before sending: {e}", file=sys.stderr)
        return 2
    except urllib.error.URLError as e:
        print(f"network error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
