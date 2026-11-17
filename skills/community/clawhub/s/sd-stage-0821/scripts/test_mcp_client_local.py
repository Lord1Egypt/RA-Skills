#!/usr/bin/env python3
"""[MCPC-080] Behavioral tests for mcp_client.py — run: python3 test_mcp_client_local.py
Covers: add, default-closed block, allow/deny, stdio call, env isolation
(beak env NOT leaked to child), HTTP+bearer (duck-to-duck), bad bearer,
consent gate. Uses throwaway HOME; no network beyond 127.0.0.1."""
import json, os, subprocess, sys, tempfile, threading, time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
FAILS = []

def check(name, cond):
    print(("  ✅ " if cond else "  ❌ ") + name)
    if not cond: FAILS.append(name)

FAKE_STDIO = r'''
import sys, json, os
for line in sys.stdin:
    try: m = json.loads(line)
    except Exception: continue
    mid, meth = m.get("id"), m.get("method")
    if meth == "initialize": r={"protocolVersion":"2025-03-26","capabilities":{"tools":{}},"serverInfo":{"name":"fake","version":"0"}}
    elif meth and meth.startswith("notifications/"): continue
    elif meth == "tools/list": r={"tools":[{"name":"echo","description":"Echo","inputSchema":{"type":"object"}},{"name":"envprobe","description":"env","inputSchema":{"type":"object"}}]}
    elif meth == "tools/call":
        p=m.get("params") or {}
        if p.get("name")=="echo": r={"content":[{"type":"text","text":"echo:"+json.dumps(p.get("arguments"))}],"isError":False}
        else: r={"content":[{"type":"text","text":"TESTKEY="+os.environ.get("TESTKEY","(unset)")+" BEAK="+os.environ.get("FAKE_BEAK","(absent)")}],"isError":False}
    else: r={}
    sys.stdout.write(json.dumps({"jsonrpc":"2.0","id":mid,"result":r})+"\n"); sys.stdout.flush()
'''

class HttpH(BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def do_POST(self):
        if self.headers.get("Authorization") != "Bearer duck-token-123":
            self.send_response(401); self.send_header("Content-Length","0"); self.end_headers(); return
        body=json.loads(self.rfile.read(int(self.headers.get("Content-Length",0))) or b"{}")
        m,mid=body.get("method"),body.get("id")
        if m=="initialize": r={"protocolVersion":"2025-03-26","capabilities":{"tools":{}},"serverInfo":{"name":"peer","version":"0"}}
        elif m and m.startswith("notifications/"):
            self.send_response(202); self.send_header("Content-Length","0"); self.end_headers(); return
        elif m=="tools/list": r={"tools":[{"name":"duck_status","description":"peer","inputSchema":{"type":"object"}}]}
        elif m=="tools/call": r={"content":[{"type":"text","text":"{\"status\":\"ready\"}"}],"isError":False}
        else: r={}
        raw=json.dumps({"jsonrpc":"2.0","id":mid,"result":r}).encode()
        self.send_response(200); self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(raw))); self.end_headers(); self.wfile.write(raw)

def run(env, *args, stdin=None):
    return subprocess.run([sys.executable, str(SCRIPTS/"mcp_client.py")]+list(args),
                          capture_output=True, text=True, env=env,
                          stdin=stdin if stdin is not None else subprocess.DEVNULL)

def main():
    tmp = tempfile.mkdtemp(prefix="mcpc-t-")
    home = Path(tmp)/"home"; (home/".space-duck").mkdir(parents=True)
    (home/".space-duck"/"config.json").write_text(json.dumps(
        {"spaceduck_id":"TESTDUCK","beak_key":"bk_test"}))
    fake = Path(tmp)/"fake_stdio.py"; fake.write_text(FAKE_STDIO)
    env = {**os.environ, "HOME": str(home), "FAKE_BEAK":"leaked",
           "SPACEDUCK_MCP_CONSENT":"yes"}
    env.pop("SPACEDUCK_CONFIG", None)

    print("stdio transport:")
    r = run(env, "add-custom", "fake", "--command", f"{sys.executable} {fake}")
    check("add-custom ok", r.returncode==0)
    r = run(env, "call", "fake", "echo", '{"a":1}')
    check("default-closed blocks call (rc=3)", r.returncode==3 and "🔒" in r.stdout)
    r = run(env, "tools", "fake")
    check("live tools/list shows locked", "🔒 echo" in r.stdout)
    run(env, "allow", "fake", "echo")
    r = run(env, "call", "fake", "echo", '{"a":1}')
    check("allowed call works", r.returncode==0 and 'echo:{"a": 1}' in r.stdout)
    sec = home/".space-duck"/"mcp_secrets.json"
    sec.write_text(json.dumps({"testkey":"s3cr3t","peer_bearer":"duck-token-123"}))
    cfgp = home/".space-duck"/"config.json"; cfg=json.loads(cfgp.read_text())
    for s in cfg["mcp_clients"]:
        if s["name"]=="fake": s["env_secrets"]={"TESTKEY":"testkey"}
    cfgp.write_text(json.dumps(cfg))
    run(env, "allow", "fake", "envprobe")
    r = run(env, "call", "fake", "envprobe")
    check("secret injected into child", "TESTKEY=s3cr3t" in r.stdout)
    check("duck env NOT leaked to child", "BEAK=(absent)" in r.stdout)
    run(env, "deny", "fake", "echo")
    r = run(env, "call", "fake", "echo", '{}')
    check("deny re-locks (rc=3)", r.returncode==3)

    print("http transport (duck-to-duck):")
    srv = HTTPServer(("127.0.0.1", 0), HttpH)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_port}/"
    cfg=json.loads(cfgp.read_text())
    cfg["mcp_clients"].append({"name":"peer","transport":"http","url":url,
        "bearer_secret":"peer_bearer","allowed_tools":["duck_status"]})
    cfgp.write_text(json.dumps(cfg))
    r = run(env, "call", "peer", "duck_status")
    check("http+bearer call works", r.returncode==0 and "ready" in r.stdout)
    sec.write_text(json.dumps({"testkey":"s3cr3t","peer_bearer":"WRONG"}))
    r = run(env, "call", "peer", "duck_status")
    check("bad bearer fails cleanly (401)", r.returncode==1 and "401" in r.stdout)
    srv.shutdown()

    print("consent gate:")
    env2 = {k:v for k,v in env.items() if k != "SPACEDUCK_MCP_CONSENT"}
    r = run(env2, "add", "fetch")
    check("no consent, non-tty -> refused", r.returncode==1 and "consent" in r.stdout)


    print("preset catalog lint:")
    sys.path.insert(0, str(SCRIPTS))
    import mcp_client as mc
    bad = []
    for name, p in mc.PRESETS.items():
        if p.get("transport") not in ("http", "stdio"): bad.append(name+":transport")
        if p["transport"] == "stdio" and not p.get("command"): bad.append(name+":no-command")
        if p["transport"] == "http" and not (p.get("url") or p.get("url_arg") or "url" in (p.get("args") or [])): bad.append(name+":no-url")
        for a in (p.get("command") or []):
            if "{" in a:
                k = a.strip("{}").split("}")[0].strip("{")
                pool = set(p.get("args") or []) | set(p.get("env_secrets") or {})
                if k not in pool: bad.append(f"{name}:unfillable:{a}")
    check(f"all {len(mc.PRESETS)} presets well-formed", not bad)
    if bad: print("   bad:", bad)

    print()
    if FAILS:
        print(f"❌ {len(FAILS)} failure(s): {FAILS}"); return 1
    print("✅ all mcp_client tests passed"); return 0

if __name__ == "__main__":
    sys.exit(main())
