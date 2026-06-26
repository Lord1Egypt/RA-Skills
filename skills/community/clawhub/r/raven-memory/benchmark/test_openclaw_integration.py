"""
Test Raven MCP server integration without needing OpenClaw.
Simulates JSON-RPC calls over subprocess stdio.

Usage:
    python3 test_openclaw_integration.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time


def rpc(proc, method: str, params: dict = {}, id: int = 1) -> dict:
    """Send a JSON-RPC request and read the response."""
    req = json.dumps({
        "jsonrpc": "2.0",
        "id": id,
        "method": method,
        "params": params,
    }) + "\n"
    proc.stdin.write(req.encode())
    proc.stdin.flush()

    # Read response
    line = proc.stdout.readline().decode().strip()
    if not line:
        return {}
    return json.loads(line)


def notify(proc, method: str, params: dict = {}):
    """Send a JSON-RPC notification (no response expected)."""
    req = json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
    }) + "\n"
    proc.stdin.write(req.encode())
    proc.stdin.flush()


def call_tool(proc, tool_name: str, arguments: dict = {}, id: int = 1) -> dict:
    """Call an MCP tool and return the parsed result."""
    resp = rpc(proc, "tools/call", {
        "name": tool_name,
        "arguments": arguments,
    }, id=id)
    if "error" in resp:
        raise RuntimeError(f"Tool error: {resp['error']}")
    content = resp.get("result", {}).get("content", [])
    if content:
        return json.loads(content[0]["text"])
    return {}


def main():
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "test_raven.db")
        env = {**os.environ, "RAVEN_DB_PATH": db_path}

        print("Starting Raven MCP server...")
        proc = subprocess.Popen(
            [sys.executable, "-m", "tcc.integration.mcp_server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )
        time.sleep(0.5)  # Let server initialize

        try:
            print("\n=== Test 1: MCP handshake ===")
            resp = rpc(proc, "initialize", {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0"},
            })
            assert resp["result"]["serverInfo"]["name"] == "raven-memory"
            notify(proc, "initialized")
            print("[PASS] MCP handshake")

            print("\n=== Test 2: List tools ===")
            resp = rpc(proc, "tools/list", id=2)
            tools = {t["name"] for t in resp["result"]["tools"]}
            expected = {
                "raven_start_session",
                "raven_record_event",
                "raven_end_session",
                "raven_search",
                "raven_rollback",
                "raven_get_status",
            }
            assert expected == tools, f"Missing tools: {expected - tools}"
            print(f"[PASS] {len(tools)} tools available")

            print("\n=== Test 3: Start session (fresh) ===")
            result = call_tool(proc, "raven_start_session", {
                "search_query": "iron man repulsor project",
            }, id=3)
            assert result["is_fresh"] is True
            assert "session_id" in result
            assert "summary" in result
            session_id = result["session_id"]
            print(f"[PASS] Session started: {session_id}")
            print(f"  Summary: {result['summary'][:80]}...")

            print("\n=== Test 4: Record events ===")
            r1 = call_tool(proc, "raven_record_event", {
                "event": "started repulsor geometry simulation",
                "actor": "agent",
                "result_summary": "validate aerodynamic profile",
                "tool_name": "run_simulation",
            }, id=4)
            assert r1["recorded"] is True

            r2 = call_tool(proc, "raven_record_event", {
                "event": "user approved titanium housing switch",
                "actor": "user",
                "result_summary": "carbon fiber too brittle under load",
            }, id=5)
            assert r2["recorded"] is True
            print("[PASS] 2 events recorded")

            print("\n=== Test 5: Get status ===")
            status = call_tool(proc, "raven_get_status", id=6)
            assert status["total_nodes"] >= 2
            assert status["is_fresh"] is False
            print(
                f"[PASS] {status['total_nodes']} nodes, "
                f"vec={'enabled' if status['vec_enabled'] else 'disabled'}"
            )

            print("\n=== Test 6: End session ===")
            end = call_tool(proc, "raven_end_session", {
                "notes": "sim passed, switching to titanium"
            }, id=7)
            assert end["recorded"] is True
            print("[PASS] Session ended")

            print("\n=== Test 7: Persistence across restart ===")
            proc.terminate()
            proc.wait()
            time.sleep(0.2)

            # Restart server with same DB
            proc = subprocess.Popen(
                [sys.executable, "-m", "tcc.integration.mcp_server"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )
            time.sleep(0.5)

            # Re-handshake
            rpc(proc, "initialize", {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0"},
            }, id=1)
            notify(proc, "initialized")

            # Start new session — should load history
            ctx = call_tool(proc, "raven_start_session", {
                "search_query": "repulsor simulation",
            }, id=2)
            assert ctx["is_fresh"] is False
            assert (
                "repulsor" in ctx["summary"].lower()
                or "titanium" in ctx["summary"].lower()
                or "simulation" in ctx["summary"].lower()
            )
            print("[PASS] History survived restart")
            print(f"  Summary preview: {ctx['summary'][:120]}...")

            print("\n=== Test 8: Semantic search ===")
            if status["vec_enabled"]:
                results = call_tool(proc, "raven_search", {
                    "query": "material switch decision",
                    "n": 3,
                }, id=3)
                print(f"[PASS] Search returned {results['n']} results")
                for result in results["results"]:
                    print(f"  - {result['event']}")
            else:
                print("[SKIP] sqlite-vec not enabled")

            print("\n=== Test 9: Rollback ===")
            call_tool(proc, "raven_get_status", id=4)
            rb = call_tool(proc, "raven_rollback", {"steps": 1}, id=5)
            assert "rolled_back_to" in rb
            print(f"[PASS] Rolled back to: {rb['rolled_back_to']}")

            print("\n" + "=" * 50)
            print("ALL OPENCLAW INTEGRATION TESTS PASSED")
            print("=" * 50)
            print("\nRaven MCP server is OpenClaw-compatible.")
            print("Add to openclaw config:")
            print(
                """
{
  "mcpServers": {
    "raven-memory": {
      "command": "python3",
      "args": ["-m", "tcc.integration.mcp_server"],
      "env": {
        "RAVEN_DB_PATH": "~/.raven/raven.db"
      }
    }
  }
}
"""
            )

        finally:
            proc.terminate()
            proc.wait()


if __name__ == "__main__":
    main()
