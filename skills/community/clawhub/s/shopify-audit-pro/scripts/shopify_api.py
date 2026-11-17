#!/usr/bin/env python3
"""shopify_api.py - read-only Shopify Admin GraphQL client (stdlib only).

Talks ONLY to https://<your-store>.myshopify.com (domain is regex-validated),
plus one Shopify-hosted download URL for `bulk-query` results (host-checked).
It cannot write to a store: every command refuses GraphQL mutations/subscriptions,
and the recommended app only holds read_* scopes.

Env (or ~/.openclaw/secrets/shopify.env, mode 600):
  SHOPIFY_STORE_DOMAIN   my-store.myshopify.com   (required, validated)
  SHOPIFY_ACCESS_TOKEN   Admin API token           (never printed/logged) ...or, for Dev Dashboard apps:
  SHOPIFY_CLIENT_ID / SHOPIFY_CLIENT_SECRET        exchanged per run for a 24h token (in memory only;
                                                   app and store must be in the same Shopify org)
  SHOPIFY_API_VERSION    e.g. 2026-10              (optional; default = newest supported)
  SHOPIFY_AUDIT_LOG      path                      (optional; default ~/.openclaw/logs/shopify-audit.jsonl)

Commands: query | paginate | bulk-query | versions | scopes
Exit codes: 0 ok, 1 error.
"""
import argparse
import datetime
import hashlib
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

VERSION = "1.0.1"
USER_AGENT = f"openclaw-shopify-audit-pro/{VERSION}"
DOMAIN_RE = re.compile(r"^[a-z0-9][a-z0-9-]*\.myshopify\.com$")
VERSION_RE = re.compile(r"^(\d{4}-\d{2}|unstable)$")
PII_KEYS = {"email", "phone", "firstName", "lastName", "address1", "address2", "zip", "ip"}
TERMINAL = {"COMPLETED", "FAILED", "CANCELED", "EXPIRED"}
QUERY_FILE_SUFFIXES = {".graphql", ".gql", ".txt"}
BULK_DOWNLOAD_HOSTS = {"storage.googleapis.com"}
BULK_MAX_BYTES = 1 << 30  # 1 GiB
ENV_FILE_KEYS = {"SHOPIFY_STORE_DOMAIN", "SHOPIFY_CLIENT_ID", "SHOPIFY_CLIENT_SECRET",
                 "SHOPIFY_ACCESS_TOKEN", "SHOPIFY_API_VERSION"}


def die(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)


# ---------- config / transport ----------

def exchange_client_credentials(domain, client_id, client_secret):
    """Dev Dashboard apps: trade client id/secret for a 24h Admin API token.
    Held in memory for this process only; never written to disk or logged."""
    body = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode()
    req = urllib.request.Request(
        f"https://{domain}/admin/oauth/access_token", data=body, method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded",
                 "Accept": "application/json",
                 "User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            tok = json.load(r).get("access_token", "")
    except urllib.error.HTTPError as e:
        hint = (" The app and the store must belong to the same Shopify organization, "
                "and the app must be installed on the store." if e.code in (400, 401, 403) else "")
        die(f"Token exchange failed (HTTP {e.code}).{hint}")
    except urllib.error.URLError as e:
        die(f"Token exchange failed: {e.reason}")
    if not tok:
        die("Token exchange returned no access_token.")
    return tok


def load_env_file():
    """Fallback for hosts where the secret store isn't injected (e.g. node hosts).
    Reads ~/.openclaw/secrets/shopify.env (or $SHOPIFY_ENV_FILE) as KEY=VALUE lines.
    Only the SHOPIFY_* keys listed in ENV_FILE_KEYS are used; real environment
    variables win. Refuses a file readable by group/others."""
    path = pathlib.Path(os.environ.get("SHOPIFY_ENV_FILE")
                        or pathlib.Path.home() / ".openclaw" / "secrets" / "shopify.env")
    if not path.is_file():
        return
    if path.stat().st_mode & 0o077:
        die(f"{path} must not be readable by group/others. Run: chmod 600 {path}")
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        if key in ENV_FILE_KEYS and not os.environ.get(key):
            os.environ[key] = val.strip().strip('"').strip("'")


def config():
    load_env_file()
    domain = os.environ.get("SHOPIFY_STORE_DOMAIN", "").strip().lower()
    token = os.environ.get("SHOPIFY_ACCESS_TOKEN", "").strip()
    if not DOMAIN_RE.match(domain):
        die("SHOPIFY_STORE_DOMAIN must look like my-store.myshopify.com "
            "(strict check so the token can never be sent to another host).")
    if not token:
        cid = os.environ.get("SHOPIFY_CLIENT_ID", "").strip()
        secret = os.environ.get("SHOPIFY_CLIENT_SECRET", "").strip()
        if not (cid and secret):
            die("Set SHOPIFY_ACCESS_TOKEN, or SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET "
                "(Dev Dashboard app).")
        token = exchange_client_credentials(domain, cid, secret)
    version = os.environ.get("SHOPIFY_API_VERSION", "").strip()
    if version and not VERSION_RE.match(version):
        die("SHOPIFY_API_VERSION must look like 2026-10.")
    return domain, token, version


def post(domain, token, version, query, variables=None, idempotent=True, retries=5):
    """POST one GraphQL document. Retries 429/THROTTLED always (Shopify did not run it);
    network errors and 5xx are retried only when idempotent (reads)."""
    url = f"https://{domain}/admin/api/{version}/graphql.json"
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": token,
        "User-Agent": USER_AGENT,
    }
    for attempt in range(retries):
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                payload = json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(float(e.headers.get("Retry-After", 2 ** attempt)))
                continue
            if e.code >= 500 and idempotent:
                time.sleep(2 ** attempt)
                continue
            detail = e.read()[:400].decode("utf-8", "replace")
            die(f"HTTP {e.code}: {detail}")
        except urllib.error.URLError as e:
            if idempotent:
                time.sleep(2 ** attempt)
                continue
            die(f"Network error ({e.reason}).")
        errors = payload.get("errors")
        if isinstance(errors, list) and any(
                isinstance(x, dict) and (x.get("extensions") or {}).get("code") == "THROTTLED"
                for x in errors):
            time.sleep(2 ** attempt)
            continue
        ts = ((payload.get("extensions") or {}).get("cost") or {}).get("throttleStatus")
        if ts and ts.get("currentlyAvailable", 1000) < 100:
            time.sleep((100 - ts["currentlyAvailable"]) / max(ts.get("restoreRate", 50), 1))
        return payload
    die("Gave up after repeated throttling / transient errors.")


def resolve_version(domain, token, pinned):
    if pinned:
        return pinned
    p = post(domain, token, "unstable", "{ publicApiVersions { handle supported } }")
    ok = [v["handle"] for v in (p.get("data") or {}).get("publicApiVersions", [])
          if v.get("supported") and re.match(r"^\d{4}-\d{2}$", v["handle"])]
    if not ok:
        die("Could not determine a supported API version; set SHOPIFY_API_VERSION.")
    return max(ok)


# ---------- read-only enforcement ----------

def executable_text(doc):
    """Return the GraphQL text with comments and string literals removed, using a
    small scanner (so a '#' inside a string, or a quote inside a comment, cannot
    hide a keyword)."""
    out, i, n = [], 0, len(doc)
    while i < n:
        c = doc[i]
        if doc.startswith('"""', i):
            j = doc.find('"""', i + 3)
            while j != -1 and doc[j - 1] == "\\":
                j = doc.find('"""', j + 1)
            i = n if j == -1 else j + 3
            out.append('""')
        elif c == '"':
            i += 1
            while i < n and doc[i] != '"':
                i += 2 if doc[i] == "\\" else 1
            i += 1
            out.append('""')
        elif c == "#":
            while i < n and doc[i] != "\n":
                i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def assert_read_only(doc, cmd):
    if re.search(r"\b(mutation|subscription)\b", executable_text(doc)):
        die(f"`{cmd}` is read-only: this skill refuses documents containing mutation/subscription.")


# ---------- helpers ----------

def audit(entry):
    path = pathlib.Path(os.environ.get(
        "SHOPIFY_AUDIT_LOG", "~/.openclaw/logs/shopify-audit.jsonl")).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    entry["ts"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    with os.fdopen(fd, "a") as f:
        f.write(json.dumps(entry) + "\n")


def digest(query, variables):
    return hashlib.sha256((query + json.dumps(variables, sort_keys=True)).encode()).hexdigest()[:16]


def redact(obj):
    if isinstance(obj, dict):
        return {k: ("***" if k in PII_KEYS and isinstance(v, str) else redact(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact(x) for x in obj]
    return obj


def user_errors(obj, found=None):
    found = [] if found is None else found
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "userErrors" and v:
                found.extend(v)
            else:
                user_errors(v, found)
    elif isinstance(obj, list):
        for x in obj:
            user_errors(x, found)
    return found


def read_user_file(path_str, allowed_suffixes, what):
    path = pathlib.Path(path_str).expanduser()
    if path.suffix.lower() not in allowed_suffixes:
        die(f"{what} must be a {'/'.join(sorted(allowed_suffixes))} file.")
    if not path.is_file():
        die(f"{what} not found: {path}")
    return path.read_text()


def load_doc(args):
    if args.file:
        return read_user_file(args.file, QUERY_FILE_SUFFIXES, "--file")
    if args.query:
        return args.query
    die("Provide --query or --file.")


def load_vars(args):
    if getattr(args, "vars_file", None):
        return json.loads(read_user_file(args.vars_file, {".json"}, "--vars-file"))
    return json.loads(args.vars) if getattr(args, "vars", None) else {}


def emit(payload, args):
    if getattr(args, "redact_pii", False):
        payload = redact(payload)
    print(json.dumps(payload, indent=2))


def dig(data, path):
    for part in path.split("."):
        data = (data or {}).get(part)
    return data


def download_bulk_result(url, out):
    """Download a bulk-operation result. Only https URLs on Shopify's storage host are
    accepted; no credentials are sent; the file is created mode 600 and never overwritten."""
    u = urllib.parse.urlparse(url)
    if u.scheme != "https" or u.hostname not in BULK_DOWNLOAD_HOSTS:
        die(f"Refusing to download from unexpected host: {u.hostname!r}")
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        die(f"{out} already exists; choose a new --out path (nothing downloaded).")
    fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    total = 0
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": USER_AGENT}),
                                timeout=300) as r, os.fdopen(fd, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            total += len(chunk)
            if total > BULK_MAX_BYTES:
                f.close()
                out.unlink()
                die("Bulk result exceeds 1 GiB; narrow the query. Partial file removed.")
            f.write(chunk)


# ---------- commands ----------

def cmd_query(args):
    doc, variables = load_doc(args), load_vars(args)
    assert_read_only(doc, "query")
    domain, token, pinned = config()
    version = resolve_version(domain, token, pinned)
    res = post(domain, token, version, doc, variables)
    audit({"cmd": "query", "store": domain, "version": version, "hash": digest(doc, variables)})
    emit(res, args)
    sys.exit(1 if res.get("errors") else 0)


def cmd_paginate(args):
    doc, variables = load_doc(args), load_vars(args)
    assert_read_only(doc, "paginate")
    domain, token, pinned = config()
    version = resolve_version(domain, token, pinned)
    nodes, cursor = [], None
    for _ in range(args.max_pages):
        res = post(domain, token, version, doc, {**variables, "cursor": cursor})
        if res.get("errors"):
            emit(res, args)
            sys.exit(1)
        conn = dig(res.get("data"), args.path)
        if conn is None:
            die(f"Path '{args.path}' not found in response data.")
        nodes += conn.get("nodes") or [e["node"] for e in conn.get("edges", [])]
        info = conn.get("pageInfo") or {}
        if not info.get("hasNextPage"):
            break
        cursor = info.get("endCursor")
    else:
        print(f"WARNING: stopped at --max-pages={args.max_pages}; results are partial.", file=sys.stderr)
    audit({"cmd": "paginate", "store": domain, "version": version,
           "hash": digest(doc, variables), "count": len(nodes)})
    emit({"count": len(nodes), "nodes": nodes}, args)


def cmd_bulk(args):
    inner = load_doc(args)
    assert_read_only(inner, "bulk-query")
    if pathlib.Path(args.out).expanduser().exists():
        die(f"{args.out} already exists; choose a new --out path (nothing started).")
    domain, token, pinned = config()
    version = resolve_version(domain, token, pinned)
    # `bulkOperationRunQuery` is Shopify's way of starting an asynchronous READ export.
    # It needs only read scopes and changes no store data.
    start = ("mutation($q:String!){ bulkOperationRunQuery(query:$q){ "
             "bulkOperation{ id status } userErrors{ field message } } }")
    res = post(domain, token, version, start, {"q": inner}, idempotent=False)
    errs = user_errors(res.get("data"))
    if res.get("errors") or errs:
        die(f"Could not start bulk operation (only one bulk query may run per shop): "
            f"{json.dumps(res.get('errors') or errs)}")
    op_id = res["data"]["bulkOperationRunQuery"]["bulkOperation"]["id"]
    poll = ("query($id:ID!){ node(id:$id){ ... on BulkOperation "
            "{ id status errorCode objectCount url partialDataUrl } } }")
    deadline, op = time.time() + args.timeout, {}
    while time.time() < deadline:
        op = post(domain, token, version, poll, {"id": op_id})["data"]["node"]
        if op["status"] in TERMINAL:
            break
        time.sleep(3)
    else:
        die(f"Timed out waiting for {op_id}; it is still running on Shopify.")
    audit({"cmd": "bulk-query", "store": domain, "version": version, "hash": digest(inner, {}),
           "status": op["status"], "objects": op.get("objectCount")})
    if op["status"] != "COMPLETED" or not op.get("url"):
        die(f"Bulk operation ended {op['status']} ({op.get('errorCode')}).")
    out = pathlib.Path(args.out).expanduser()
    download_bulk_result(op["url"], out)
    print(json.dumps({"status": "COMPLETED", "objects": op["objectCount"], "file": str(out),
                      "format": "JSONL; child rows carry __parentId"}, indent=2))


def cmd_versions(args):
    domain, token, _ = config()
    res = post(domain, token, "unstable", "{ publicApiVersions { handle supported } }")
    emit(res, args)


def cmd_scopes(args):
    domain, token, pinned = config()
    version = resolve_version(domain, token, pinned)
    res = post(domain, token, version, "{ currentAppInstallation { accessScopes { handle } } }")
    emit(res, args)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--version", action="version", version=f"shopify-audit-pro {VERSION}")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--query")
        sp.add_argument("--file", help="a .graphql/.gql/.txt file containing the query")
        sp.add_argument("--vars")
        sp.add_argument("--vars-file", help="a .json file with query variables")
        sp.add_argument("--redact-pii", action="store_true", help="mask email/phone/name/address in output")

    q = sub.add_parser("query", help="read-only GraphQL query"); common(q); q.set_defaults(fn=cmd_query)
    g = sub.add_parser("paginate", help="follow pageInfo; query must take $cursor"); common(g)
    g.add_argument("--path", required=True, help="dot path to the connection, e.g. products")
    g.add_argument("--max-pages", type=int, default=20)
    g.set_defaults(fn=cmd_paginate)
    b = sub.add_parser("bulk-query", help="run a Shopify bulk read, download JSONL"); common(b)
    b.add_argument("--out", required=True, help="new file path (existing files are never overwritten)")
    b.add_argument("--timeout", type=int, default=600)
    b.set_defaults(fn=cmd_bulk)
    v = sub.add_parser("versions"); v.add_argument("--redact-pii", action="store_true"); v.set_defaults(fn=cmd_versions)
    s = sub.add_parser("scopes"); s.add_argument("--redact-pii", action="store_true"); s.set_defaults(fn=cmd_scopes)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
