#!/usr/bin/env python3
"""Read-before-write access to a Supabase project's Auth config (Management API).

Subcommands
  show            GET /v1/projects/<ref>/config/auth, secrets redacted
  patch           PATCH only the keys you name, diff first, dry-run by default,
                  re-read afterwards and fail if anything else moved
  add-redirect    append one URL to uri_allow_list without dropping the others
  check-redirect  predict whether a magic-link redirect_to is honoured or
                  silently replaced by site_url
  advisors        GET the remote security/performance advisors

Guards (each refuses on absent, empty, wrong-typed input):
  * PINNED_REF below is the only project this copy of the script will touch.
    It is set by editing this file, never from the environment or a .env file.
  * The access token is read from SUPABASE_ACCESS_TOKEN and never printed.
  * The token is only sent to https://api.supabase.com, or to a loopback
    --api-base (for tests).
  * A PATCH body contains only the keys you requested, and only those whose
    value actually changes.

Exit codes: 0 ok · 1 advisors at/above --fail-on · 2 refused · 3 post-write
verification failed · 4 API/network error.

Stdlib only, Python 3.9+.  `python3 authcfg.py --selftest` runs the fixtures
against a local mock server; it never contacts a real project.
"""
import argparse
import io
import ipaddress
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

# ---- the pin: edit this line, review the diff. 20 lowercase letters. -------
PINNED_REF = "PIN_YOUR_PROJECT_REF"
# ----------------------------------------------------------------------------

OFFICIAL_API = "https://api.supabase.com"
REF_RE = re.compile(r"^[a-z]{20}$")
SECRET_KEY_RE = re.compile(
    r"(secret|smtp_pass|auth_token|access_key|api_key|_key$|private|password$)")
LEVELS = {"INFO": 1, "WARN": 2, "ERROR": 3}


class Refused(Exception):
    pass


class ApiError(Exception):
    pass


# ---------------------------------------------------------------- guards ----
def check_ref(ref):
    if not isinstance(PINNED_REF, str) or not REF_RE.match(PINNED_REF):
        raise Refused("PINNED_REF is not set in the script: edit it to your "
                      "20-letter project ref (a reviewed diff, not an env var)")
    if not isinstance(ref, str) or not ref:
        raise Refused("--ref is required and must equal PINNED_REF")
    if not REF_RE.match(ref):
        raise Refused("--ref is not a 20-letter project ref")
    if ref != PINNED_REF:
        raise Refused("--ref does not match PINNED_REF: this script is pinned "
                      "to another project")
    return ref


def check_base(base):
    if base is None or base == OFFICIAL_API:
        return OFFICIAL_API
    if not isinstance(base, str):
        raise Refused("--api-base must be a string")
    p = urllib.parse.urlparse(base)
    host = p.hostname or ""
    try:
        loop = ipaddress.ip_address(host).is_loopback
    except ValueError:
        loop = host == "localhost"
    if p.scheme != "http" or not loop or p.path not in ("", "/"):
        raise Refused("--api-base may only be %s or an http://loopback "
                      "test server; the token is never sent elsewhere"
                      % OFFICIAL_API)
    return base.rstrip("/")


def get_token():
    tok = os.environ.get("SUPABASE_ACCESS_TOKEN")
    if not isinstance(tok, str) or not tok.strip():
        raise Refused("SUPABASE_ACCESS_TOKEN is not set")
    if tok != tok.strip() or any(c.isspace() or ord(c) < 33 or ord(c) > 126
                                 for c in tok):
        raise Refused("SUPABASE_ACCESS_TOKEN contains whitespace or "
                      "non-printable characters")
    return tok


def redact(key, value):
    if isinstance(value, str) and value and SECRET_KEY_RE.search(key):
        return "<redacted>"
    return value


# ------------------------------------------------------------------ http ----
def call(method, url, tok, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + tok)
    req.add_header("Accept", "application/json")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        msg = e.read(300).decode("utf-8", "replace").replace(tok, "<token>")
        raise ApiError("%s %s -> HTTP %d: %s" % (method, urllib.parse.urlparse(
            url).path, e.code, msg))
    except (urllib.error.URLError, OSError) as e:
        raise ApiError("%s failed: %s" % (method, e))
    try:
        return json.loads(raw.decode("utf-8")) if raw else None
    except ValueError:
        raise ApiError("%s returned non-JSON" % method)


def get_auth(base, ref, tok):
    cfg = call("GET", "%s/v1/projects/%s/config/auth" % (base, ref), tok)
    if not isinstance(cfg, dict) or not cfg:
        raise Refused("GET config/auth returned an empty or non-object body: "
                      "refusing to diff against nothing")
    return cfg


# ----------------------------------------------------------- validation ----
def json_or_str(raw):
    try:
        return json.loads(raw)
    except ValueError:
        return raw


def coerce(key, value, before, from_cli):
    """Return value typed like the remote field, or raise Refused."""
    if isinstance(before, (list, dict)):
        raise Refused("%s is a nested field; this tool patches scalars only"
                      % key)
    if from_cli:
        if isinstance(before, str):
            value = value            # keep the literal text: "587" stays "587"
        else:
            value = json_or_str(value)
    if before is None:
        if isinstance(value, (list, dict)):
            raise Refused("%s: nested values are not supported" % key)
        return value
    if isinstance(before, bool):
        if not isinstance(value, bool):
            raise Refused("%s is boolean remotely; got %r" % (key, value))
    elif isinstance(before, (int, float)):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise Refused("%s is numeric remotely; got %r" % (key, value))
    elif isinstance(before, str):
        if not isinstance(value, str):
            raise Refused("%s is a string remotely; got %r" % (key, value))
    return value


def split_list(s):
    return [u.strip() for u in (s or "").split(",") if u.strip()]


def check_url_entry(url):
    if not isinstance(url, str) or not url or "://" not in url:
        raise Refused("redirect URL must be absolute (scheme://...)")
    if "," in url or any(c.isspace() for c in url):
        raise Refused("redirect URL may not contain commas or whitespace: "
                      "uri_allow_list is one comma-separated string")
    return url


def domain_checks(changes, before, allow_remove):
    if "site_url" in changes:
        p = urllib.parse.urlparse(changes["site_url"] or "")
        if p.scheme not in ("http", "https") or not p.netloc:
            raise Refused("site_url must be an absolute http(s) URL: every "
                          "magic link that fails the allow-list lands there")
    if "uri_allow_list" in changes:
        new = split_list(changes["uri_allow_list"])
        for u in new:
            check_url_entry(u)
        dropped = [u for u in split_list(before.get("uri_allow_list"))
                   if u not in new]
        if dropped and not allow_remove:
            raise Refused("uri_allow_list would drop %d existing entr%s (%s). "
                          "The field is replaced, not merged: use add-redirect,"
                          " or pass --allow-remove" % (
                              len(dropped), "y" if len(dropped) == 1 else "ies",
                              ", ".join(dropped)))


# ------------------------------------------------------------- commands ----
def show(key, value):
    return json.dumps(redact(key, value))


def do_patch(base, ref, requested, allow_remove, apply, out):
    """requested: dict key -> (value, from_cli)."""
    tok = get_token()
    if not requested:
        raise Refused("nothing requested")
    before = get_auth(base, ref, tok)
    unknown = [k for k in requested if k not in before]
    if unknown:
        raise Refused("unknown field(s) %s: not present in GET config/auth "
                      "(typo, or not exposed on this plan)" % ", ".join(unknown))
    target = {k: coerce(k, v, before[k], cli) for k, (v, cli) in
              requested.items()}
    domain_checks(target, before, allow_remove)
    changes = {k: v for k, v in target.items() if before[k] != v}
    if not changes:
        out.write("No change: remote already has the requested values.\n")
        return 0
    out.write("Project %s — auth config diff:\n" % ref)
    for k in sorted(changes):
        out.write("  %s: %s -> %s\n" % (k, show(k, before[k]),
                                        show(k, changes[k])))
    if not apply:
        out.write("DRY RUN. Nothing sent. Re-run with --apply to PATCH.\n")
        return 0
    if not set(changes) <= set(requested):       # invariant, cannot be off
        raise Refused("internal: body would carry unrequested keys")
    call("PATCH", "%s/v1/projects/%s/config/auth" % (base, ref), tok, changes)
    after = get_auth(base, ref, tok)
    bad = []
    for k, v in changes.items():
        if after.get(k) != v:
            bad.append("%s did not take: now %s" % (k, show(k, after.get(k))))
    for k in sorted(set(before) | set(after)):
        if k in changes:
            continue
        if before.get(k) != after.get(k) or (k in before) != (k in after):
            bad.append("%s changed without being requested: %s -> %s" % (
                k, show(k, before.get(k)), show(k, after.get(k))))
    if bad:
        out.write("VERIFY FAILED after PATCH:\n")
        for b in bad:
            out.write("  " + b + "\n")
        return 3
    out.write("VERIFIED: %d field(s) changed, nothing else moved.\n"
              % len(changes))
    return 0


def glob_to_regex(pattern):
    if any(c in pattern for c in "[]{}\\"):
        raise Refused("pattern %r uses [..], {..} or escapes: this checker "
                      "only models *, ** and ?; test it against the real "
                      "server instead" % pattern)
    out, i = [], 0
    while i < len(pattern):
        if pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif pattern[i] == "*":
            out.append("[^./]*")
            i += 1
        elif pattern[i] == "?":
            out.append("[^./]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("^" + "".join(out) + "$", re.S)


def _port(p):
    try:
        return p.port
    except ValueError:
        return "invalid"


def redirect_verdict(url, site_url, allow_list):
    """Mirror of the Auth server's redirect check. Returns (ok, reason)."""
    if not isinstance(url, str) or not url:
        return False, "empty redirect_to"
    if not isinstance(site_url, str) or not site_url:
        raise Refused("site_url is empty: cannot evaluate")
    b, r = urllib.parse.urlparse(site_url), urllib.parse.urlparse(url)
    rh = r.hostname or ""
    local = rh == "localhost"
    try:
        ip = ipaddress.ip_address(rh)
        local = local or ip.is_loopback
    except ValueError:
        ip = None
    if (b.hostname == rh and b.scheme == r.scheme
            and (_port(b) == _port(r) or local)):
        return True, "same scheme/host as site_url"
    if re.fullmatch(r"[0-9]+", rh):
        return False, "decimal-IP host is always rejected"
    if ip is not None:
        return (ip.is_loopback,
                "loopback IP is always allowed" if ip.is_loopback
                else "non-loopback IP literal is always rejected")
    if r.scheme in ("http", "https") and not re.fullmatch(
            r"[a-zA-Z0-9]([a-zA-Z0-9.-]*[a-zA-Z0-9])?", rh):
        return False, "irregular hostname"
    target = url.split("#", 1)[0]
    for pat in split_list(allow_list):
        if glob_to_regex(pat).match(target):
            return True, "matches allow-list entry %s" % pat
    return False, "no allow-list entry matches (query string included)"


def do_check_redirect(url, site_url, allow_list, out):
    ok, why = redirect_verdict(url, site_url, allow_list)
    if ok:
        out.write("ACCEPTED: %s\n" % why)
        return 0
    out.write("FALLBACK: %s. The link will land on site_url (%s), silently.\n"
              % (why, site_url))
    return 1


def do_advisors(base, ref, kinds, fail_on, out):
    tok = get_token()
    worst = 0
    for kind in kinds:
        res = call("GET", "%s/v1/projects/%s/advisors/%s" % (base, ref, kind),
                   tok)
        if not isinstance(res, dict) or not isinstance(res.get("lints"), list):
            raise Refused("advisors/%s: unexpected body, expected {lints: []}"
                          % kind)
        out.write("[%s] %d finding(s)\n" % (kind, len(res["lints"])))
        for l in res["lints"]:
            if not isinstance(l, dict):
                raise Refused("advisors/%s: lint entry is not an object" % kind)
            lvl = str(l.get("level", "")).upper()
            if lvl not in LEVELS:
                raise Refused("advisors/%s: unknown level %r" % (kind, lvl))
            worst = max(worst, LEVELS[lvl])
            out.write("  %-5s %s — %s\n" % (lvl, l.get("name", "?"),
                                          l.get("title", "")))
    if fail_on and worst >= LEVELS[fail_on]:
        return 1
    return 0


# ------------------------------------------------------------------ cli ----
def build_parser():
    ap = argparse.ArgumentParser(prog="authcfg.py")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")

    def common(p):
        p.add_argument("--ref")
        p.add_argument("--api-base")

    p = sub.add_parser("show")
    common(p)
    p.add_argument("--keys", help="comma-separated subset")
    p = sub.add_parser("patch")
    common(p)
    p.add_argument("--set", action="append", default=[], metavar="KEY=VALUE")
    p.add_argument("--body", help="JSON object file (requires --keys)")
    p.add_argument("--keys", help="exact key list the --body must contain")
    p.add_argument("--allow-remove", action="store_true")
    p.add_argument("--apply", action="store_true")
    p = sub.add_parser("add-redirect")
    common(p)
    p.add_argument("url")
    p.add_argument("--apply", action="store_true")
    p = sub.add_parser("check-redirect")
    common(p)
    p.add_argument("url")
    p.add_argument("--site-url")
    p.add_argument("--allow-list")
    p = sub.add_parser("advisors")
    common(p)
    p.add_argument("--type", choices=["security", "performance", "all"],
                   default="all")
    p.add_argument("--fail-on", choices=["INFO", "WARN", "ERROR"])
    return ap


def parse_sets(sets):
    req = {}
    for s in sets:
        if not isinstance(s, str) or "=" not in s:
            raise Refused("--set expects KEY=VALUE, got %r" % s)
        k, v = s.split("=", 1)
        if not re.fullmatch(r"[a-z0-9_]+", k):
            raise Refused("bad key %r" % k)
        if k in req:
            raise Refused("key %s given twice" % k)
        req[k] = (v, True)
    return req


def parse_body(path, keys):
    if not keys:
        raise Refused("--body requires --keys listing exactly its keys")
    declared = [k.strip() for k in keys.split(",") if k.strip()]
    if not declared:
        raise Refused("--keys is empty")
    try:
        with open(path, encoding="utf-8") as f:
            body = json.load(f)
    except (OSError, ValueError) as e:
        raise Refused("cannot read --body: %s" % e)
    if not isinstance(body, dict) or not body:
        raise Refused("--body must be a non-empty JSON object")
    extra = sorted(set(body) - set(declared))
    missing = sorted(set(declared) - set(body))
    if extra or missing:
        raise Refused("--body keys differ from --keys (unrequested: %s; "
                      "missing: %s)" % (extra or "-", missing or "-"))
    return {k: (v, False) for k, v in body.items()}


def main(argv, out=None, err=None):
    out, err = out or sys.stdout, err or sys.stderr
    args = build_parser().parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.cmd:
        err.write("usage: authcfg.py {show,patch,add-redirect,check-redirect,"
                  "advisors} ... | --selftest\n")
        return 2
    try:
        if args.cmd == "check-redirect" and args.site_url is not None:
            return do_check_redirect(args.url, args.site_url,
                                     args.allow_list or "", out)
        base = check_base(args.api_base)
        ref = check_ref(args.ref)
        if args.cmd == "show":
            cfg = get_auth(base, ref, get_token())
            keys = split_list(args.keys) if args.keys else sorted(cfg)
            missing = [k for k in keys if k not in cfg]
            if missing:
                raise Refused("unknown key(s): %s" % ", ".join(missing))
            json.dump({k: redact(k, cfg[k]) for k in keys}, out, indent=1)
            out.write("\n")
            return 0
        if args.cmd == "patch":
            if args.set and args.body:
                raise Refused("use --set or --body, not both")
            req = parse_body(args.body, args.keys) if args.body else \
                parse_sets(args.set)
            return do_patch(base, ref, req, args.allow_remove, args.apply, out)
        if args.cmd == "add-redirect":
            url = check_url_entry(args.url)
            cfg = get_auth(base, ref, get_token())
            if "uri_allow_list" not in cfg:
                raise Refused("uri_allow_list missing from GET config/auth")
            cur = split_list(cfg["uri_allow_list"])
            if url in cur:
                out.write("No change: already in uri_allow_list.\n")
                return 0
            return do_patch(base, ref,
                            {"uri_allow_list": (",".join(cur + [url]), False)},
                            False, args.apply, out)
        if args.cmd == "check-redirect":
            cfg = get_auth(base, ref, get_token())
            return do_check_redirect(args.url, cfg.get("site_url"),
                                     cfg.get("uri_allow_list") or "", out)
        if args.cmd == "advisors":
            kinds = ["security", "performance"] if args.type == "all" \
                else [args.type]
            return do_advisors(base, ref, kinds, args.fail_on, out)
    except Refused as e:
        err.write("REFUSED: %s\n" % e)
        return 2
    except ApiError as e:
        err.write("API ERROR: %s\n" % e)
        return 4
    return 2


# ------------------------------------------------------------- selftest ----
def selftest():
    import copy
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    REF, OTHER = "abcdefghijklmnopqrst", "zyxwvutsrqponmlkjihg"
    TOK, SECRET = "sbp_" + "0" * 40, "fixture-smtp-value-not-real"
    SEED = {"site_url": "https://app.example.com",
            "uri_allow_list": "https://app.example.com/auth/callback,"
                              "https://*.preview.example.com/**",
            "disable_signup": False, "jwt_exp": 3600,
            "mailer_autoconfirm": False, "password_hibp_enabled": False,
            "smtp_port": "587", "smtp_pass": SECRET,
            "password_required_characters": ""}
    st = {"cfg": None, "mode": "normal", "log": []}

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, obj=None, raw=None):
            data = raw if raw is not None else json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _handle(self, method):
            n = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(n)) if n else None
            st["log"].append((method, self.path, body))
            if self.headers.get("Authorization") != "Bearer " + TOK \
                    or st["mode"] == "401":
                return self._send(401, {"message": "Unauthorized"})
            if self.path == "/v1/projects/%s/config/auth" % REF:
                if method == "GET":
                    m = st["mode"]
                    if m == "empty":
                        return self._send(200, {})
                    if m == "array":
                        return self._send(200, [])
                    if m == "notjson":
                        return self._send(200, raw=b"<html>")
                    return self._send(200, st["cfg"])
                if st["mode"] != "ignore":
                    st["cfg"].update(body)
                if st["mode"] == "reset_other":
                    st["cfg"]["mailer_autoconfirm"] = True
                return self._send(200, st["cfg"])
            if self.path.startswith("/v1/projects/%s/advisors/" % REF):
                lv = "WARN" if self.path.endswith("security") else "INFO"
                if st["mode"] == "bad_advisors":
                    return self._send(200, {"result": []})
                return self._send(200, {"lints": [
                    {"name": "x_lint", "title": "t", "level": lv}]})
            return self._send(404, {"message": "not found"})

        def do_GET(self):
            self._handle("GET")

        def do_PATCH(self):
            self._handle("PATCH")

    srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % srv.server_address[1]
    bodyfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            ".selftest-body.json")
    results = []

    def run(name, argv, code, mode="normal", pin=REF, token=TOK,
            patches=None, contains=(), body=None, check=None):
        st["cfg"], st["mode"], st["log"] = copy.deepcopy(SEED), mode, []
        globals()["PINNED_REF"] = pin
        if token is None:
            os.environ.pop("SUPABASE_ACCESS_TOKEN", None)
        else:
            os.environ["SUPABASE_ACCESS_TOKEN"] = token
        if body is not None:
            with open(bodyfile, "w") as f:
                f.write(body)
        o, e = io.StringIO(), io.StringIO()
        rc = main(argv, o, e)
        text = o.getvalue() + e.getvalue()
        sent = [b for (m, _, b) in st["log"] if m == "PATCH"]
        ok = rc == code
        why = "" if ok else "rc=%s want %s" % (rc, code)
        if ok and patches is not None and len(sent) != patches:
            ok, why = False, "PATCH count %d want %d" % (len(sent), patches)
        for c in contains:
            if ok and c not in text:
                ok, why = False, "missing %r" % c
        if ok and (TOK in text or SECRET in text):
            ok, why = False, "leaked token or secret in output"
        if ok and check is not None and not check(sent):
            ok, why = False, "check failed on PATCH body %r" % sent
        results.append((ok, name, why or text.strip().splitlines()[-1:]))

    P = ["patch", "--api-base", base]
    R = ["--ref", REF]
    # --- hostile: pin, ref, token, base
    run("pin placeholder refuses", P + R + ["--set", "jwt_exp=7200",
        "--apply"], 2, pin="PIN_YOUR_PROJECT_REF", patches=0)
    run("pin empty refuses", P + R + ["--set", "jwt_exp=7200", "--apply"], 2,
        pin="", patches=0)
    run("pin None refuses", P + R + ["--set", "jwt_exp=7200", "--apply"], 2,
        pin=None, patches=0)
    run("ref absent refuses", P + ["--set", "jwt_exp=7200", "--apply"], 2,
        patches=0)
    run("ref different refuses", P + ["--ref", OTHER, "--set",
        "jwt_exp=7200", "--apply"], 2, patches=0)
    run("ref malformed refuses", P + ["--ref", REF.upper(), "--set",
        "jwt_exp=7200", "--apply"], 2, patches=0)
    run("token absent refuses", P + R + ["--set", "jwt_exp=7200", "--apply"],
        2, token=None, patches=0)
    run("token blank refuses", P + R + ["--set", "jwt_exp=7200", "--apply"],
        2, token="   ", patches=0)
    run("non-loopback base refuses", ["patch", "--api-base",
        "http://api.example.com", "--ref", REF, "--set", "jwt_exp=7200",
        "--apply"], 2, patches=0)
    run("https lookalike base refuses", ["show", "--api-base",
        "https://api.supabase.com.example.com", "--ref", REF], 2)
    run("401 is an API error, token not echoed", P + R + ["--set",
        "jwt_exp=7200"], 4, mode="401", patches=0)
    # --- hostile: remote bodies
    run("GET {} refuses", P + R + ["--set", "jwt_exp=7200", "--apply"], 2,
        mode="empty", patches=0)
    run("show on GET {} refuses", ["show", "--api-base", base, "--ref",
        REF], 2, mode="empty")
    run("GET [] refuses", P + R + ["--set", "jwt_exp=7200", "--apply"], 2,
        mode="array", patches=0)
    run("GET non-JSON refuses", P + R + ["--set", "jwt_exp=7200", "--apply"],
        4, mode="notjson", patches=0)
    # --- hostile: requests
    run("no --set refuses", P + R + ["--apply"], 2, patches=0)
    run("unknown key refuses", P + R + ["--set", "jwt_expiry=7200",
        "--apply"], 2, patches=0)
    run("bool given text refuses", P + R + ["--set", "disable_signup=yes",
        "--apply"], 2, patches=0)
    run("int given bool refuses", P + R + ["--set", "jwt_exp=true",
        "--apply"], 2, patches=0)
    run("empty site_url refuses", P + R + ["--set", "site_url=", "--apply"],
        2, patches=0)
    run("relative site_url refuses", P + R + ["--set", "site_url=/home",
        "--apply"], 2, patches=0)
    run("allow-list shrink refuses", P + R + ["--set",
        "uri_allow_list=https://app.example.com/auth/callback", "--apply"],
        2, patches=0, contains=["replaced, not merged"])
    run("--body with unrequested key refuses", P + R + ["--body", bodyfile,
        "--keys", "jwt_exp", "--apply"], 2, patches=0,
        body='{"jwt_exp": 7200, "mailer_autoconfirm": true}')
    run("--body without --keys refuses", P + R + ["--body", bodyfile,
        "--apply"], 2, patches=0, body='{"jwt_exp": 7200}')
    run("--body {} refuses", P + R + ["--body", bodyfile, "--keys", "jwt_exp",
        "--apply"], 2, patches=0, body="{}")
    run("--body null refuses", P + R + ["--body", bodyfile, "--keys",
        "jwt_exp", "--apply"], 2, patches=0, body="null")
    run("--body string-for-int refuses", P + R + ["--body", bodyfile,
        "--keys", "jwt_exp", "--apply"], 2, patches=0,
        body='{"jwt_exp": "7200"}')
    run("--set and --body together refuse", P + R + ["--set", "jwt_exp=1",
        "--body", bodyfile, "--keys", "jwt_exp"], 2, patches=0,
        body='{"jwt_exp": 7200}')
    run("duplicate --set refuses", P + R + ["--set", "jwt_exp=1", "--set",
        "jwt_exp=2", "--apply"], 2, patches=0)
    # --- post-write verification
    run("server resets another field -> exit 3", P + R + ["--set",
        "jwt_exp=7200", "--apply"], 3, mode="reset_other", patches=1,
        contains=["mailer_autoconfirm changed without being requested"])
    run("server ignores PATCH -> exit 3", P + R + ["--set", "jwt_exp=7200",
        "--apply"], 3, mode="ignore", patches=1, contains=["did not take"])
    # --- happy paths
    run("dry-run sends nothing", P + R + ["--set", "jwt_exp=7200"], 0,
        patches=0, contains=["DRY RUN", "jwt_exp: 3600 -> 7200"])
    run("apply sends only the requested key", P + R + ["--set",
        "jwt_exp=7200", "--set", "disable_signup=false", "--apply"], 0,
        patches=1, contains=["VERIFIED"],
        check=lambda s: s == [{"jwt_exp": 7200}])
    run("string field keeps literal text", P + R + ["--set",
        "smtp_port=2525", "--apply"], 0, patches=1,
        check=lambda s: s == [{"smtp_port": "2525"}])
    run("no-op sends nothing", P + R + ["--set", "jwt_exp=3600", "--apply"],
        0, patches=0, contains=["No change"])
    run("secret diff is redacted", P + R + ["--set", "smtp_pass=newpass"], 0,
        patches=0, contains=["<redacted>"])
    run("body path sends exactly body", P + R + ["--body", bodyfile, "--keys",
        "password_hibp_enabled", "--apply"], 0, patches=1,
        body='{"password_hibp_enabled": true}',
        check=lambda s: s == [{"password_hibp_enabled": True}])
    run("add-redirect keeps existing entries", ["add-redirect", "--api-base",
        base, "--ref", REF, "https://staging.example.com/auth/callback",
        "--apply"], 0, patches=1, check=lambda s: s == [{"uri_allow_list":
        SEED["uri_allow_list"] + ",https://staging.example.com/auth/callback"
        }])
    run("add-redirect duplicate is a no-op", ["add-redirect", "--api-base",
        base, "--ref", REF, "https://app.example.com/auth/callback",
        "--apply"], 0, patches=0)
    run("add-redirect comma refuses", ["add-redirect", "--api-base", base,
        "--ref", REF, "https://a.example.com,https://b.example.com",
        "--apply"], 2, patches=0)
    run("add-redirect wrong ref refuses", ["add-redirect", "--api-base", base,
        "--ref", OTHER, "https://x.example.com/cb", "--apply"], 2, patches=0)
    run("show redacts secrets", ["show", "--api-base", base, "--ref", REF], 0,
        contains=["<redacted>", "smtp_port"])
    run("advisors fail-on WARN", ["advisors", "--api-base", base, "--ref",
        REF, "--fail-on", "WARN"], 1, contains=["[security] 1 finding"])
    run("advisors fail-on ERROR passes", ["advisors", "--api-base", base,
        "--ref", REF, "--fail-on", "ERROR"], 0)
    run("advisors odd body refuses", ["advisors", "--api-base", base, "--ref",
        REF], 2, mode="bad_advisors")
    # --- redirect checker (offline, mirrors the Auth server rule)
    S, A = "https://app.example.com", SEED["uri_allow_list"]
    for url, want in [
            ("https://app.example.com/anything?x=1", 0),       # same host
            ("https://app.example.com:8443/x", 1),             # port differs
            ("https://app.example.com/auth/callback", 0),
            ("https://evil.example.org/auth/callback", 1),
            ("https://pr-12.preview.example.com/a/b", 0),      # * and **
            ("https://a.b.preview.example.com/a", 1),          # * stops at .
            ("http://127.0.0.1:5173/cb", 0),                   # loopback IP
            ("http://10.0.0.5/cb", 1),                         # private IP
            ("", 1)]:
        run("check-redirect %r" % url, ["check-redirect", url, "--site-url",
            S, "--allow-list", A], want)
    run("check-redirect exact entry + query string falls back",
        ["check-redirect", "https://other.example.com/cb?next=/x",
         "--site-url", S, "--allow-list", "https://other.example.com/cb"], 1,
        contains=["FALLBACK"])
    run("check-redirect unmodelled glob refuses", ["check-redirect",
        "https://x.example.com", "--site-url", S, "--allow-list",
        "https://{a,b}.example.com"], 2)
    run("check-redirect empty site_url refuses", ["check-redirect",
        "https://x.example.com", "--site-url", "", "--allow-list", A], 2)

    srv.shutdown()
    if os.path.exists(bodyfile):
        os.remove(bodyfile)
    globals()["PINNED_REF"] = "PIN_YOUR_PROJECT_REF"
    fails = [r for r in results if not r[0]]
    for ok, name, why in results:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", name,
                            "" if ok else "  -> %s" % (why,)))
    print("%d/%d passed" % (len(results) - len(fails), len(results)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
