"""Real local HTTP/process integration only; no public target coverage claim."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from test_collect import Base, ROOT, args, c


class LocalMCP(Base):
    def setUp(self):
        super().setUp()
        owner = self
        self.calls = []
        self.logged_in = True
        self.reject_auth = False
        self.sse = False
        self.missing_tools = False
        self.raw = c.fixture("xiaohongshu")
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *values): pass
            def do_CONNECT(self):
                self.send_error(407, "Proxy Authentication Required")
            def do_POST(self):
                if owner.reject_auth:
                    self.send_error(401)
                    return
                message = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                owner.calls.append(message)
                method, params = message["method"], message.get("params", {})
                if method == "initialize":
                    result = {"protocolVersion": "2024-11-05", "capabilities": {}, "serverInfo": {"name": "local-fixture", "version": "1"}}
                elif method == "notifications/initialized":
                    self.send_response(202); self.send_header("Content-Length", "0"); self.end_headers(); return
                elif method == "tools/list":
                    if owner.missing_tools:
                        result = {"tools": [], "nextCursor": "fixture-page"}
                    elif not params.get("cursor"):
                        result = {"tools": [{"name": "check_login_status"}, {"name": "search_feeds"}], "nextCursor": "fixture-page2"}
                    else:
                        result = {"tools": [{"name": "get_feed_detail"}]}
                elif method == "tools/call":
                    tool = params["name"]
                    if tool == "check_login_status":
                        result = {"content": [{"type": "text", "text": "✅ 已登录" if owner.logged_in else "❌ 未登录"}]}
                    elif tool == "search_feeds":
                        result = {"content": [{"type": "text", "text": json.dumps({"feeds": [{"modelType": "hot_query", "id": "ignored"}, {"modelType": "note", "id": "fixture-note-1", "xsecToken": "fixture-xsec-secret"}]})}]}
                    elif tool == "get_feed_detail":
                        result = {"content": [{"type": "text", "text": json.dumps(owner.raw)}]}
                    else:
                        result = {"isError": True, "content": []}
                else:
                    result = {}
                reply = json.dumps({"jsonrpc": "2.0", "id": message["id"], "result": result}).encode()
                if owner.sse:
                    reply = b"event: message\ndata: " + reply + b"\n\n"
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream" if owner.sse else "application/json")
                self.send_header("Mcp-Session-Id", "fixture-session")
                self.send_header("Content-Length", str(len(reply)))
                self.end_headers(); self.wfile.write(reply)
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_port}/mcp"
        os.environ["XHS_PROXY"] = "http://fixture-user:fixture-password@127.0.0.1:9"

    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join(timeout=2)
        super().tearDown()

    def test_json_and_sse_discovery_identity_mapping_read_only_and_token_redaction(self):
        for sse in [False, True]:
            self.sse, self.calls = sse, []
            result = c.xiaohongshu(args("xiaohongshu", "--mcp-url", self.url, "--query", "fixture query", "--limit", "3"))
            self.assertEqual(result["status"], "partial")
            self.assertEqual(result["observations"][0]["note_id"], "fixture-note-1")
            toolcalls = [m["params"] for m in self.calls if m["method"] == "tools/call"]
            self.assertEqual([m["name"] for m in toolcalls], ["check_login_status", "search_feeds", "get_feed_detail"])
            detail = toolcalls[-1]["arguments"]
            self.assertEqual((detail["feed_id"], detail["xsec_token"]), ("fixture-note-1", "fixture-xsec-secret"))
            self.assertEqual(detail["limit"], 3)
            self.assertFalse(detail["click_more_replies"])
            self.assertNotIn("fixture-xsec-secret", json.dumps(result))
            self.assertEqual(len([m for m in self.calls if m["method"] == "tools/list"]), 2)

    def test_missing_login_no_detail_call_and_discovery_page_cap(self):
        self.logged_in = False
        self.error("xhs_login_required", lambda: c.xiaohongshu(args("xiaohongshu", "--mcp-url", self.url, "--query", "fixture")), "missing_session")
        self.assertNotIn("get_feed_detail", [m.get("params", {}).get("name") for m in self.calls])
        self.missing_tools, self.calls = True, []
        self.error("xhs_tools_missing", lambda: c.xiaohongshu(args("xiaohongshu", "--mcp-url", self.url)), "unsupported_surface")
        self.assertEqual(len([m for m in self.calls if m["method"] == "tools/list"]), 3)

    def test_mcp_auth_rejection_and_actual_local_connect_407(self):
        self.reject_auth = True
        client = c.MCPClient(self.url)
        self.error("mcp_auth_required", lambda: client.call("initialize"), "blocked")
        os.environ["PROXYLANE_PROXY_URL"] = f"http://fixture-user:fixture-password@127.0.0.1:{self.server.server_port}"
        self.error("proxy_auth_required", lambda: c.transcript(args("youtube-transcript", "--target", "aircAruvnKk")), "blocked")


class CLIPipeline(unittest.TestCase):
    def environment(self):
        return {"PATH": os.environ.get("PATH", ""), "PROXYLANE_EVIDENCE_PYTHON": sys.executable}

    def run_cli(self, *arguments, environment=None):
        command = [sys.executable, str(ROOT / "scripts/collect.py"), *arguments]
        result = subprocess.run(command, capture_output=True, text=True, env=environment or self.environment(), timeout=25)
        return result, json.loads(result.stdout)

    def test_all_modes_stdout_artifact_contract_and_fixture_boundary(self):
        with tempfile.TemporaryDirectory() as temporary:
            result, data = self.run_cli("--mode", "demo", "--fixture", "--out", temporary)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(data["status"], "fixture_demo")
            self.assertEqual({r["mode"] for r in data["results"]}, set(c.MODES))
            for row in data["results"]:
                self.assertEqual(row["proof_mode"], "fixture")
                self.assertTrue(row["observations"])
                self.assertFalse(row["proxy"]["configured"])
                self.assertTrue((Path(temporary) / row["evidence"][0]["path"]).is_file())
            self.assertEqual(json.loads((Path(temporary) / "outcome.json").read_text()), data)

    def test_cli_bounds_missing_inputs_and_node_bridge(self):
        for arguments, status in [(('--mode', 'price', '--limit', '0'), 'input_error'), (('--mode', 'xiaohongshu'), 'missing_input'), (('--mode', 'demo'), 'input_error')]:
            result, data = self.run_cli(*arguments)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(data["status"], status)
        node = shutil.which("node")
        if not node:
            self.skipTest("Node bridge requires an installed Node executable")
        done = subprocess.run([node, str(ROOT / "scripts/proxylane-web-evidence.mjs"), "--mode", "demo", "--fixture"], capture_output=True, text=True, env=self.environment(), timeout=25)
        self.assertEqual(done.returncode, 0)
        self.assertEqual(json.loads(done.stdout)["status"], "fixture_demo")

    @unittest.skipUnless(os.name == "posix", "Collector process-group deadline contract is POSIX")
    def test_total_deadline_kills_real_descendant_and_private_config_cleanup(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            pidfile, configfile = directory / "pid", directory / "configpath"
            fake = directory / "fake-ytdlp"
            fake.write_text("#!" + sys.executable + "\nimport os,sys,subprocess,time\nfrom pathlib import Path\nchild=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)'])\nPath(os.environ['FIXTURE_PIDFILE']).write_text(str(child.pid))\nPath(os.environ['FIXTURE_CONFIGFILE']).write_text(sys.argv[sys.argv.index('--config-locations')+1])\ntime.sleep(60)\n")
            fake.chmod(0o700)
            env = {**self.environment(), "PROXYLANE_PROXY_URL": "http://fixture-user:fixture-password@127.0.0.1:9", "FIXTURE_PIDFILE": str(pidfile), "FIXTURE_CONFIGFILE": str(configfile)}
            started = time.monotonic()
            result, data = self.run_cli("--mode", "youtube-comments", "--target", "aircAruvnKk", "--ytdlp", str(fake), "--timeout", "10", environment=env)
            self.assertEqual((result.returncode, data["status"]), (2, "timeout"))
            self.assertLess(time.monotonic() - started, 18)
            self.assertTrue(pidfile.exists())
            pid = pidfile.read_text().strip()
            state = subprocess.run(["ps", "-p", pid, "-o", "stat="], capture_output=True, text=True).stdout.strip()
            self.assertTrue(not state or state.startswith("Z"), "Source descendant remains running")
            self.assertFalse(Path(configfile.read_text()).exists())
            self.assertNotIn("fixture-password", result.stdout)


if __name__ == "__main__":
    unittest.main()
