#!/usr/bin/env python3
"""space-duck MCP client — the duck consumes external MCP servers.

[MCPC-080] Reverse direction of mcp_server.py: that script makes the duck
an MCP *server* (other AIs plug into the duck); this one gives the duck
MCP *client* plugs (the duck uses other people's tools).

Constitution (references/MCP-CLIENT-SPEC.md):
  1. Owner adds, owner holds creds — secrets in ~/.space-duck/
     mcp_secrets.json (0600), never platform-side, never on argv.
  2. Default-closed allowlist — a new server exposes ZERO tools until the
     owner runs `allow` (same doctrine as update_senders).
  3. Lane immutability — Lane A clients run on the owner's box only.
  4. Stdlib only. Transports: Streamable HTTP (single-response, tolerates
     SSE-formatted bodies) and stdio (newline-delimited JSON-RPC child).
  5. Honest passthrough of upstream results/errors.

Usage:
  mcp_client.py list-presets
  mcp_client.py add <preset> [--name N] [--arg k=v ...]
  mcp_client.py add-custom <name> (--url U [--bearer] | --command "CMD...")
  mcp_client.py remove <name> [--purge-secrets]
  mcp_client.py list
  mcp_client.py tools <name>
  mcp_client.py allow <name> (<tool> ... | --all)
  mcp_client.py deny <name> <tool> ...
  mcp_client.py call <name> <tool> ['{"json":"args"}']
  mcp_client.py status

Env:
  SPACEDUCK_CONFIG          override ~/.space-duck/config.json
  SPACEDUCK_MCP_CONSENT=yes non-interactive consent (owner-run scripts only)
"""
import getpass
import json
import os
import selectors
import shlex
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CFG_DIR = Path(os.environ.get("SPACEDUCK_CONFIG_DIR", str(Path.home() / ".space-duck")))
CFG_PATH = Path(os.environ.get("SPACEDUCK_CONFIG", str(CFG_DIR / "config.json")))
SECRETS_PATH = CFG_DIR / "mcp_secrets.json"
PROTO = "2025-03-26"
UA = "space-duck-mcp-client/0.1"
CALL_TIMEOUT = 30
MAX_RESP = 1 * 1024 * 1024
MAX_TEXT = 64 * 1024

# ── preset catalog — the pre-wired "Claude Connect" menu ─────────────────
# Each preset: transport, command template ({k} filled from --arg k=v),
# env_secrets (ENV_VAR -> secret store key), args (required --arg keys),
# desc. Templates reference official/first-party servers where they exist.
PRESETS = {
    "duck": {
        "transport": "http", "url_arg": "url", "bearer": True,
        "args": ["url"],
        "desc": "Another Space Duck's MCP endpoint — duck-to-duck tool use "
                "(their duck_status/read_workspace_file/send_peck etc.)"},
    "github": {
        "transport": "stdio",
        "command": ["npx", "-y", "@modelcontextprotocol/server-github"],
        "env_secrets": {"GITHUB_PERSONAL_ACCESS_TOKEN": "github_pat"},
        "desc": "GitHub — repos, PRs, issues, code search"},
    "filesystem": {
        "transport": "stdio", "args": ["dir"],
        "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "{dir}"],
        "desc": "Local filesystem under a chosen dir (Lane A / on-box only)"},
    "git": {
        "transport": "stdio", "args": ["repo"],
        "command": ["uvx", "mcp-server-git", "--repository", "{repo}"],
        "desc": "Local git repo ops (log, diff, commit)"},
    "playwright": {
        "transport": "stdio",
        "command": ["npx", "-y", "@playwright/mcp@latest"],
        "desc": "Real browser automation (navigate, click, screenshot)"},
    "stripe": {
        "transport": "stdio",
        "command": ["npx", "-y", "@stripe/mcp", "--tools=all"],
        "env_secrets": {"STRIPE_SECRET_KEY": "stripe_sk"},
        "desc": "Stripe — payments, customers, invoices"},
    "postgres": {
        "transport": "stdio",
        "command": ["npx", "-y", "@modelcontextprotocol/server-postgres",
                    "{POSTGRES_URL}"],
        "env_secrets": {"POSTGRES_URL": "postgres_url"},
        "desc": "Postgres — schema inspection + read-only SQL"},
    "sqlite": {
        "transport": "stdio", "args": ["db"],
        "command": ["uvx", "mcp-server-sqlite", "--db-path", "{db}"],
        "desc": "Local SQLite database"},
    "gdrive": {
        "transport": "stdio",
        "command": ["npx", "-y", "@modelcontextprotocol/server-gdrive"],
        "desc": "Google Drive (server manages its own OAuth on first run)"},
    "notion": {
        "transport": "stdio",
        "command": ["npx", "-y", "@notionhq/notion-mcp-server"],
        "env_secrets": {"NOTION_TOKEN": "notion_token"},
        "desc": "Notion — pages, databases, search"},
    "airtable": {
        "transport": "stdio",
        "command": ["npx", "-y", "airtable-mcp-server"],
        "env_secrets": {"AIRTABLE_API_KEY": "airtable_key"},
        "desc": "Airtable — bases, tables, records"},
    "slack": {
        "transport": "stdio",
        "command": ["npx", "-y", "@modelcontextprotocol/server-slack"],
        "env_secrets": {"SLACK_BOT_TOKEN": "slack_bot_token",
                        "SLACK_TEAM_ID": "slack_team_id"},
        "desc": "Slack — channels, messages, users"},
    "brave-search": {
        "transport": "stdio",
        "command": ["npx", "-y", "@modelcontextprotocol/server-brave-search"],
        "env_secrets": {"BRAVE_API_KEY": "brave_key"},
        "desc": "Brave web search"},
    "exa": {
        "transport": "stdio",
        "command": ["npx", "-y", "exa-mcp-server"],
        "env_secrets": {"EXA_API_KEY": "exa_key"},
        "desc": "Exa semantic web search"},
    "fetch": {
        "transport": "stdio",
        "command": ["uvx", "mcp-server-fetch"],
        "desc": "Fetch web pages as markdown (no key needed)"},
    "memory": {
        "transport": "stdio",
        "command": ["npx", "-y", "@modelcontextprotocol/server-memory"],
        "desc": "Persistent knowledge-graph memory scratch space"},
    "sentry": {
        "transport": "http", "url": "https://mcp.sentry.dev/mcp",
        "bearer": True,
        "desc": "Sentry error monitoring (remote; pre-issued OAuth bearer)"},
    "cloudflare-docs": {
        "transport": "http", "url": "https://docs.mcp.cloudflare.com/mcp",
        "desc": "Cloudflare docs search (remote, no auth)"},
    "aws-docs": {
        "transport": "stdio",
        "command": ["uvx", "awslabs.aws-documentation-mcp-server@latest"],
        "desc": "AWS documentation search"},
    # ── wave 2 [MCPC-081] — package names verified on npm/PyPI 2026-08-10 ──
    "zapier": {
        "transport": "http", "url_arg": "url", "bearer": True,
        "args": ["url"],
        "desc": "Zapier MCP — 9,000+ apps (incl. Gmail/Calendar/Sheets) via "
                "your personal endpoint from zapier.com/mcp"},
    "hubspot": {
        "transport": "stdio",
        "command": ["npx", "-y", "@hubspot/mcp-server"],
        "env_secrets": {"PRIVATE_APP_ACCESS_TOKEN": "hubspot_token"},
        "desc": "HubSpot CRM — contacts, companies, deals, tickets"},
    "supabase": {
        "transport": "stdio",
        "command": ["npx", "-y", "@supabase/mcp-server-supabase@latest"],
        "env_secrets": {"SUPABASE_ACCESS_TOKEN": "supabase_pat"},
        "desc": "Supabase — projects, tables, SQL, edge functions"},
    "shopify-dev": {
        "transport": "stdio",
        "command": ["npx", "-y", "@shopify/dev-mcp"],
        "desc": "Shopify dev docs + Admin GraphQL schema search (no key; "
                "store admin ops via zapier or add-custom)"},
    "google-calendar": {
        "transport": "stdio",
        "command": ["npx", "-y", "@cocal/google-calendar-mcp"],
        "env_secrets": {"GOOGLE_OAUTH_CREDENTIALS": "gcal_oauth_creds_path"},
        "desc": "Google Calendar — events, availability (secret value = "
                "path to your OAuth credentials JSON on this box)"},
    "snowflake": {
        "transport": "stdio", "args": ["config"],
        "command": ["uvx", "snowflake-labs-mcp",
                    "--service-config-file", "{config}"],
        "env_secrets": {"SNOWFLAKE_ACCOUNT": "snowflake_account",
                        "SNOWFLAKE_USER": "snowflake_user",
                        "SNOWFLAKE_PASSWORD": "snowflake_password"},
        "desc": "Snowflake — Cortex + SQL (needs a service config YAML)"},
}


# ── config + secrets store ──────────────────────────────────────────────

def _load_cfg():
    if not CFG_PATH.exists():
        raise SystemExit(f"❌ {CFG_PATH} missing — pair the duck first (pair.py)")
    try:
        return json.loads(CFG_PATH.read_text())
    except Exception as e:
        raise SystemExit(f"❌ cannot parse {CFG_PATH}: {e}")


def _save_cfg(cfg):
    tmp = CFG_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(cfg, indent=2) + "\n")
    tmp.replace(CFG_PATH)


def _load_secrets():
    try:
        return json.loads(SECRETS_PATH.read_text())
    except Exception:
        return {}


def _save_secrets(sec):
    CFG_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(str(SECRETS_PATH), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(sec, f, indent=2)
        f.write("\n")


def _servers(cfg):
    v = cfg.get("mcp_clients")
    return v if isinstance(v, list) else []


def _find(cfg, name):
    for s in _servers(cfg):
        if isinstance(s, dict) and s.get("name") == name:
            return s
    return None


# ── transports ──────────────────────────────────────────────────────────

class HttpSession:
    """Streamable HTTP, single-response mode. Tolerates SSE-format bodies
    (event:/data: lines) that some remote servers emit."""

    def __init__(self, url, bearer=None):
        self.url = url
        self.bearer = bearer
        self._id = 0

    def rpc(self, method, params=None, notify=False):
        body = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            body["params"] = params
        if not notify:
            self._id += 1
            body["id"] = self._id
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json, text/event-stream",
                   "User-Agent": UA}
        if self.bearer:
            headers["Authorization"] = "Bearer " + self.bearer
        req = urllib.request.Request(self.url, data=json.dumps(body).encode(),
                                     method="POST", headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=CALL_TIMEOUT) as r:
                raw = r.read(MAX_RESP)
                ctype = r.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            raw = (e.read() or b"")[:2000]
            raise RuntimeError(f"HTTP {e.code}: {raw.decode('utf-8', 'replace')[:400]}")
        except Exception as e:
            raise RuntimeError(f"unreachable: {str(e)[:200]}")
        if notify:
            return None
        text = raw.decode("utf-8", "replace")
        if "text/event-stream" in ctype or text.lstrip().startswith(("event:", "data:")):
            # take the last data: payload
            datas = [ln[5:].strip() for ln in text.splitlines()
                     if ln.startswith("data:")]
            text = datas[-1] if datas else "{}"
        try:
            msg = json.loads(text or "{}")
        except Exception:
            raise RuntimeError(f"bad response: {text[:400]}")
        if isinstance(msg, dict) and msg.get("error"):
            e = msg["error"]
            raise RuntimeError(f"rpc error {e.get('code')}: {e.get('message')}")
        return msg.get("result") if isinstance(msg, dict) else msg

    def initialize(self):
        res = self.rpc("initialize", {
            "protocolVersion": PROTO,
            "capabilities": {},
            "clientInfo": {"name": "space-duck", "version": "0.1"}})
        try:
            self.rpc("notifications/initialized", notify=True)
        except Exception:
            pass  # some single-response servers 4xx notifications; harmless
        return res

    def close(self):
        pass


class StdioSession:
    """Newline-delimited JSON-RPC over a spawned child. Minimal env:
    the duck's own environment (beak_key etc.) is NOT inherited."""

    def __init__(self, command, extra_env=None):
        env = {"PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"),
               "HOME": os.environ.get("HOME", "/tmp"),
               "LANG": os.environ.get("LANG", "C.UTF-8")}
        env.update(extra_env or {})
        self.proc = subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, env=env)
        self._id = 0
        self._pending = b""
        self._sel = selectors.DefaultSelector()
        self._sel.register(self.proc.stdout, selectors.EVENT_READ)

    def _readline(self, timeout):
        deadline = time.time() + timeout
        buf, self._pending = self._pending, b""
        if b"\n" in buf:
            line, _, rest = buf.partition(b"\n")
            self._pending = rest
            return line
        while time.time() < deadline:
            if self.proc.poll() is not None and not self._sel.select(0):
                raise RuntimeError("server process exited")
            events = self._sel.select(timeout=min(1.0, max(0.05, deadline - time.time())))
            if not events:
                continue
            ch = self.proc.stdout.read1(65536)
            if not ch:
                raise RuntimeError("server closed stdout")
            buf += ch
            if b"\n" in buf:
                line, _, rest = buf.partition(b"\n")
                self._pending = rest
                return line
            if len(buf) > MAX_RESP:
                raise RuntimeError("response too large")
        raise RuntimeError(f"timeout after {timeout}s")

    def rpc(self, method, params=None, notify=False, timeout=CALL_TIMEOUT):
        body = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            body["params"] = params
        if not notify:
            self._id += 1
            body["id"] = self._id
        try:
            self.proc.stdin.write((json.dumps(body) + "\n").encode())
            self.proc.stdin.flush()
        except Exception as e:
            raise RuntimeError(f"cannot write to server: {e}")
        if notify:
            return None
        # read lines until we see our id (skip server notifications/logs)
        for _ in range(50):
            line = self._readline(timeout)
            try:
                msg = json.loads(line.decode("utf-8", "replace"))
            except Exception:
                continue
            if isinstance(msg, dict) and msg.get("id") == self._id:
                if msg.get("error"):
                    e = msg["error"]
                    raise RuntimeError(
                        f"rpc error {e.get('code')}: {e.get('message')}")
                return msg.get("result")
        raise RuntimeError("no matching response")

    def initialize(self):
        res = self.rpc("initialize", {
            "protocolVersion": PROTO,
            "capabilities": {},
            "clientInfo": {"name": "space-duck", "version": "0.1"}},
            timeout=60)  # npx/uvx may download on first run
        self.rpc("notifications/initialized", notify=True)
        return res

    def close(self):
        try:
            self.proc.stdin.close()
        except Exception:
            pass
        try:
            self.proc.terminate()
            self.proc.wait(timeout=5)
        except Exception:
            try:
                self.proc.kill()
            except Exception:
                pass


def _connect(srv):
    """Open + initialize a session for a configured server dict."""
    secrets = _load_secrets()
    if srv.get("transport") == "http":
        bearer = None
        if srv.get("bearer_secret"):
            bearer = secrets.get(srv["bearer_secret"])
            if not bearer:
                raise RuntimeError(
                    f"secret '{srv['bearer_secret']}' missing from "
                    f"{SECRETS_PATH} — re-run add")
        sess = HttpSession(srv["url"], bearer=bearer)
    else:
        extra_env = {}
        for env_var, key in (srv.get("env_secrets") or {}).items():
            val = secrets.get(key)
            if not val:
                raise RuntimeError(
                    f"secret '{key}' missing from {SECRETS_PATH} — re-run add")
            extra_env[env_var] = val
        cmd = [a.format(**extra_env) if "{" in a else a
               for a in (srv.get("command") or [])]
        if not cmd:
            raise RuntimeError("server has no command configured")
        sess = StdioSession(cmd, extra_env=extra_env)
    sess.initialize()
    return sess


# ── commands ────────────────────────────────────────────────────────────

def cmd_list_presets():
    print("🦆 Space Duck — pre-wired MCP connectors\n")
    for name, p in PRESETS.items():
        needs = []
        if p.get("env_secrets"):
            needs += list(p["env_secrets"])
        if p.get("bearer"):
            needs.append("bearer token")
        if p.get("args"):
            needs += [f"--arg {a}=…" for a in p["args"]]
        need = (" — needs: " + ", ".join(needs)) if needs else ""
        print(f"  {name:<16} {p['desc']}{need}")
    print("\nAdd one:   mcp_client.py add <preset>")
    print("Custom:    mcp_client.py add-custom <name> --url … | --command '…'")
    return 0


def _consent(name):
    if os.environ.get("SPACEDUCK_MCP_CONSENT", "").lower() in ("yes", "1", "true"):
        return True
    if not sys.stdin.isatty():
        print("❌ consent required — run interactively or set "
              "SPACEDUCK_MCP_CONSENT=yes (owner-run only)")
        return False
    ans = input(f"🦆 Connect '{name}' as a tool source for this duck? "
                f"Tools stay locked until you `allow` them. [y/N] ").strip().lower()
    return ans in ("y", "yes")


def _prompt_secret(label, key, secrets):
    if secrets.get(key):
        print(f"  {label}: already stored ({key}) — keeping")
        return
    if not sys.stdin.isatty():
        print(f"  ⚠️ {label} not set — add later: store as '{key}' in {SECRETS_PATH}")
        return
    val = getpass.getpass(f"  {label} (input hidden, stored 0600 locally): ").strip()
    if val:
        secrets[key] = val


def cmd_add(preset_name, name=None, argmap=None):
    p = PRESETS.get(preset_name)
    if not p:
        print(f"❌ unknown preset '{preset_name}' — see list-presets")
        return 1
    argmap = argmap or {}
    name = name or preset_name
    cfg = _load_cfg()
    if _find(cfg, name):
        print(f"❌ server '{name}' already configured — remove it first")
        return 1
    for a in p.get("args", []):
        if a not in argmap:
            print(f"❌ preset '{preset_name}' requires --arg {a}=…")
            return 1
    if not _consent(name):
        return 1
    secrets = _load_secrets()
    srv = {"name": name, "preset": preset_name,
           "transport": p["transport"], "allowed_tools": [],
           "added_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    if p["transport"] == "http":
        srv["url"] = argmap.get(p.get("url_arg") or "url") or p.get("url")
        if not srv["url"]:
            print("❌ this preset needs --arg url=…")
            return 1
        if p.get("bearer"):
            key = f"{name}_bearer"
            _prompt_secret(f"{name} bearer token", key, secrets)
            if secrets.get(key):
                srv["bearer_secret"] = key
    else:
        srv["command"] = [a.format(**{**argmap,
                                      **{e: "{%s}" % e for e in
                                         (p.get("env_secrets") or {})}})
                          for a in p["command"]]
        if p.get("env_secrets"):
            srv["env_secrets"] = dict(p["env_secrets"])
            for env_var, key in p["env_secrets"].items():
                _prompt_secret(env_var, key, secrets)
    _save_secrets(secrets)
    cfg.setdefault("mcp_clients", [])
    cfg["mcp_clients"] = _servers(cfg) + [srv]
    _save_cfg(cfg)
    print(f"✅ '{name}' added (tools locked — default-closed).")
    print(f"   Next: mcp_client.py tools {name}    # see what it offers")
    print(f"         mcp_client.py allow {name} <tool> …   # open the ones you trust")
    return 0


def cmd_add_custom(name, url=None, bearer=False, command=None):
    cfg = _load_cfg()
    if _find(cfg, name):
        print(f"❌ server '{name}' already configured")
        return 1
    if not url and not command:
        print("❌ need --url or --command")
        return 1
    if not _consent(name):
        return 1
    secrets = _load_secrets()
    srv = {"name": name, "preset": None, "allowed_tools": [],
           "added_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    if url:
        srv["transport"] = "http"
        srv["url"] = url
        if bearer:
            key = f"{name}_bearer"
            _prompt_secret(f"{name} bearer token", key, secrets)
            if secrets.get(key):
                srv["bearer_secret"] = key
    else:
        srv["transport"] = "stdio"
        srv["command"] = shlex.split(command)
    _save_secrets(secrets)
    cfg["mcp_clients"] = _servers(cfg) + [srv]
    _save_cfg(cfg)
    print(f"✅ '{name}' added (tools locked — default-closed). "
          f"Run: tools {name}, then allow.")
    return 0


def cmd_remove(name, purge_secrets=False):
    cfg = _load_cfg()
    srv = _find(cfg, name)
    if not srv:
        print(f"❌ no server '{name}'")
        return 1
    cfg["mcp_clients"] = [s for s in _servers(cfg) if s.get("name") != name]
    _save_cfg(cfg)
    if purge_secrets:
        secrets = _load_secrets()
        keys = list((srv.get("env_secrets") or {}).values())
        if srv.get("bearer_secret"):
            keys.append(srv["bearer_secret"])
        for k in keys:
            secrets.pop(k, None)
        _save_secrets(secrets)
        print(f"✅ '{name}' removed, {len(keys)} secret(s) purged")
    else:
        print(f"✅ '{name}' removed (secrets kept; --purge-secrets to wipe)")
    return 0


def cmd_list():
    cfg = _load_cfg()
    servers = _servers(cfg)
    if not servers:
        print("No MCP servers configured. Start with: mcp_client.py list-presets")
        return 0
    print("🦆 Configured MCP tool sources\n")
    for s in servers:
        allowed = s.get("allowed_tools") or []
        mark = f"✅ {len(allowed)} tool(s) allowed" if allowed else "🔒 all locked"
        where = s.get("url") if s.get("transport") == "http" \
            else " ".join(s.get("command") or [])
        print(f"  {s.get('name'):<16} [{s.get('transport')}] {mark}")
        print(f"  {'':<16} {where[:80]}")
    return 0


def cmd_tools(name):
    cfg = _load_cfg()
    srv = _find(cfg, name)
    if not srv:
        print(f"❌ no server '{name}' — see list")
        return 1
    try:
        sess = _connect(srv)
    except Exception as e:
        print(f"❌ connect failed: {e}")
        return 1
    try:
        res = sess.rpc("tools/list") or {}
    except Exception as e:
        print(f"❌ tools/list failed: {e}")
        return 1
    finally:
        sess.close()
    allowed = set(srv.get("allowed_tools") or [])
    tools = res.get("tools") or []
    print(f"🦆 {name} — {len(tools)} tool(s)\n")
    for t in tools:
        tn = t.get("name", "?")
        mark = "✅" if (tn in allowed or "*" in allowed) else "🔒"
        desc = (t.get("description") or "").strip().split("\n")[0][:90]
        print(f"  {mark} {tn:<28} {desc}")
    if not allowed:
        print(f"\nAll locked (default-closed). Open with:\n"
              f"  mcp_client.py allow {name} <tool> …   or   allow {name} --all")
    return 0


def cmd_allow(name, tools, all_=False):
    cfg = _load_cfg()
    srv = _find(cfg, name)
    if not srv:
        print(f"❌ no server '{name}'")
        return 1
    if all_:
        srv["allowed_tools"] = ["*"]
    else:
        cur = [t for t in (srv.get("allowed_tools") or []) if t != "*"]
        srv["allowed_tools"] = sorted(set(cur) | set(tools))
    _save_cfg(cfg)
    print(f"✅ {name} allowed_tools = {srv['allowed_tools']}")
    return 0


def cmd_deny(name, tools):
    cfg = _load_cfg()
    srv = _find(cfg, name)
    if not srv:
        print(f"❌ no server '{name}'")
        return 1
    cur = srv.get("allowed_tools") or []
    if "*" in cur:
        print("⚠️ was '--all'; switching to explicit list requires re-allow")
        cur = []
    srv["allowed_tools"] = [t for t in cur if t not in set(tools)]
    _save_cfg(cfg)
    print(f"✅ {name} allowed_tools = {srv['allowed_tools']}")
    return 0


def cmd_call(name, tool, args_json=None):
    cfg = _load_cfg()
    srv = _find(cfg, name)
    if not srv:
        print(f"❌ no server '{name}'")
        return 1
    allowed = srv.get("allowed_tools") or []
    # DEFAULT-CLOSED enforcement — the whole point.
    if "*" not in allowed and tool not in allowed:
        print(f"🔒 tool '{tool}' is not allowed on '{name}' (default-closed).\n"
              f"   Owner can open it: mcp_client.py allow {name} {tool}")
        return 3
    try:
        args = json.loads(args_json) if args_json else {}
        if not isinstance(args, dict):
            raise ValueError("args must be a JSON object")
    except Exception as e:
        print(f"❌ bad args JSON: {e}")
        return 1
    try:
        sess = _connect(srv)
    except Exception as e:
        print(f"❌ connect failed: {e}")
        return 1
    try:
        res = sess.rpc("tools/call", {"name": tool, "arguments": args}) or {}
    except Exception as e:
        print(f"❌ call failed: {e}")
        return 1
    finally:
        sess.close()
    is_err = bool(res.get("isError"))
    out = []
    for c in res.get("content") or []:
        if isinstance(c, dict) and c.get("type") == "text":
            out.append(str(c.get("text") or ""))
    text = ("\n".join(out) or json.dumps(res))[:MAX_TEXT]
    print(("⚠️ tool error:\n" if is_err else "") + text)
    return 2 if is_err else 0


def cmd_status():
    cfg = _load_cfg()
    servers = _servers(cfg)
    if not servers:
        print("No MCP servers configured.")
        return 0
    for s in servers:
        name = s.get("name")
        try:
            sess = _connect(s)
            info = sess.rpc("tools/list") or {}
            sess.close()
            n = len(info.get("tools") or [])
            print(f"  ✅ {name:<16} up — {n} tool(s)")
        except Exception as e:
            print(f"  ❌ {name:<16} {str(e)[:100]}")
    return 0


# ── CLI plumbing ────────────────────────────────────────────────────────

def main(argv):
    if not argv:
        print(__doc__)
        return 1
    cmd, rest = argv[0], argv[1:]
    if cmd == "list-presets":
        return cmd_list_presets()
    if cmd == "add":
        if not rest:
            print("usage: add <preset> [--name N] [--arg k=v ...]")
            return 1
        preset, name, argmap = rest[0], None, {}
        i = 1
        while i < len(rest):
            if rest[i] == "--name" and i + 1 < len(rest):
                name = rest[i + 1]; i += 2
            elif rest[i] == "--arg" and i + 1 < len(rest):
                k, _, v = rest[i + 1].partition("=")
                argmap[k] = v; i += 2
            else:
                print(f"unknown flag {rest[i]}"); return 1
        return cmd_add(preset, name, argmap)
    if cmd == "add-custom":
        if not rest:
            print("usage: add-custom <name> (--url U [--bearer] | --command 'CMD')")
            return 1
        name, url, bearer, command = rest[0], None, False, None
        i = 1
        while i < len(rest):
            if rest[i] == "--url" and i + 1 < len(rest):
                url = rest[i + 1]; i += 2
            elif rest[i] == "--bearer":
                bearer = True; i += 1
            elif rest[i] == "--command" and i + 1 < len(rest):
                command = rest[i + 1]; i += 2
            else:
                print(f"unknown flag {rest[i]}"); return 1
        return cmd_add_custom(name, url, bearer, command)
    if cmd == "remove":
        if not rest:
            print("usage: remove <name> [--purge-secrets]"); return 1
        return cmd_remove(rest[0], purge_secrets="--purge-secrets" in rest)
    if cmd == "list":
        return cmd_list()
    if cmd == "tools":
        if not rest:
            print("usage: tools <name>"); return 1
        return cmd_tools(rest[0])
    if cmd == "allow":
        if not rest:
            print("usage: allow <name> (<tool> ... | --all)"); return 1
        return cmd_allow(rest[0], [t for t in rest[1:] if t != "--all"],
                         all_="--all" in rest[1:])
    if cmd == "deny":
        if len(rest) < 2:
            print("usage: deny <name> <tool> ..."); return 1
        return cmd_deny(rest[0], rest[1:])
    if cmd == "call":
        if len(rest) < 2:
            print("usage: call <name> <tool> ['{json}']"); return 1
        return cmd_call(rest[0], rest[1], rest[2] if len(rest) > 2 else None)
    if cmd == "status":
        return cmd_status()
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
