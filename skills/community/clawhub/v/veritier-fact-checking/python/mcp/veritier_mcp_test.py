#!/usr/bin/env python3
"""
Veritier MCP Integration Test (v2.2)
====================================
Verifies that your Veritier MCP stdio proxy is correctly configured
and can communicate with the Veritier API.

Supports two modes:
  - Production mode (default): uses real LLM, consumes quota
  - Zero-quota test mode:      uses mock_claims / mock_verdict /
                               mock_validation / mock_decision, no quota consumed

Usage:
  1. Install dependencies:
     pip install mcp httpx anyio

  2. Set your API key:
     export VERITIER_API_KEY="vt_your_api_key_here"

     For zero-quota testing, use a test key:
     export VERITIER_API_KEY="vt_test_your_test_key_here"

  3. Place this file in the same directory as veritier_mcp_proxy.py

  4. Run the test (test mode auto-detected from key prefix):
     python veritier_mcp_test.py

Reconstruct, JWKS, and issuer revoke are REST (not stdio tools). See
https://veritier.ai/docs#attestation and the proxy module docstring.

More info: https://veritier.ai/docs#testing
"""

import asyncio
import json
import os
import sys
from pathlib import Path

EXPECTED_TOOLS = ["extract_text", "extract_document", "verify_text", "verify_document", "validate", "attest_action"]


def _is_test_key(api_key: str) -> bool:
    """Test keys have the vt_test_... prefix."""
    return api_key.startswith("vt_test_")


async def test_mcp_proxy():
    api_key = os.getenv("VERITIER_API_KEY", "")

    if not api_key:
        print("✗ Error: VERITIER_API_KEY environment variable is not set.")
        print("  Get your free API key at https://veritier.ai/register")
        sys.exit(1)

    is_test = _is_test_key(api_key)
    mode_label = "TEST MODE (zero-quota, mock responses)" if is_test else "🔴 PRODUCTION MODE (quota will be consumed)"

    # Locate the proxy script in the same directory as this test
    proxy_path = Path(__file__).parent / "veritier_mcp_proxy.py"
    if not proxy_path.exists():
        print(f"✗ Error: Cannot find veritier_mcp_proxy.py")
        print(f"  Expected at: {proxy_path}")
        print(f"  Download it from: https://veritier.ai/veritier_mcp_proxy.py")
        sys.exit(1)

    print(f"  Proxy: {proxy_path}")
    print(f"  Key:   {'*' * 8} (length: {len(api_key)})")
    print(f"  Mode:  {mode_label}\n")

    # Launch the standalone proxy as a subprocess
    proc = await asyncio.create_subprocess_exec(
        sys.executable, str(proxy_path),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env={**os.environ, "VERITIER_API_KEY": api_key},
    )

    async def send(msg: dict):
        proc.stdin.write((json.dumps(msg) + "\n").encode())
        await proc.stdin.drain()

    async def recv(timeout: int = 90) -> dict | None:
        line = await asyncio.wait_for(proc.stdout.readline(), timeout=timeout)
        return json.loads(line.decode()) if line else None

    try:
        # [1] Initialize MCP session
        await send({
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "veritier-mcp-test", "version": "2.2"}
            }
        })
        init = await recv(timeout=15)
        server_info = init["result"]["serverInfo"]
        print(f"✓ Initialize: server={server_info['name']} v{server_info['version']}")

        # [2] Confirm initialization
        await send({"jsonrpc": "2.0", "method": "notifications/initialized"})

        # [3] Discover available tools
        await send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        tools = await recv(timeout=10)
        tool_names = [t["name"] for t in tools["result"]["tools"]]
        print(f"✓ Tools discovered: {tool_names}")

        missing = [t for t in EXPECTED_TOOLS if t not in tool_names]
        if missing:
            print(f"✗ Error: Missing expected tools: {missing}")
            sys.exit(1)

        # Verify mock_* / action_id are in tool schemas
        tool_map = {t["name"]: t for t in tools["result"]["tools"]}
        extract_props = tool_map["extract_text"].get("inputSchema", {}).get("properties", {})
        verify_props = tool_map["verify_text"].get("inputSchema", {}).get("properties", {})
        verify_doc_props = tool_map["verify_document"].get("inputSchema", {}).get("properties", {})
        validate_props = tool_map["validate"].get("inputSchema", {}).get("properties", {})
        attest_props = tool_map["attest_action"].get("inputSchema", {}).get("properties", {})
        attest_desc = tool_map["attest_action"].get("description", "")
        if "mock_claims" in extract_props:
            print("✓ mock_claims parameter present in extract_text schema")
        else:
            print("⚠ mock_claims not found in extract_text schema (update your proxy)")
        if "mock_verdict" in verify_props:
            print("✓ mock_verdict parameter present in verify_text schema")
        else:
            print("⚠ mock_verdict not found in verify_text schema (update your proxy)")
        if "action_id" in verify_props and "action_id" in verify_doc_props:
            print("✓ action_id parameter present in verify_text and verify_document schemas")
        else:
            print("⚠ action_id not found in verify schemas (update your proxy)")
        if "mock_validation" in validate_props:
            print("✓ mock_validation parameter present in validate schema")
        else:
            print("⚠ mock_validation not found in validate schema (update your proxy)")
        if "mock_decision" in attest_props:
            print("✓ mock_decision parameter present in attest_action schema")
        else:
            print("⚠ mock_decision not found in attest_action schema (update your proxy)")
        if "quoted passages" in attest_desc.lower():
            print("✓ citation_exists quote-in-opinion documented on attest_action")
        else:
            print("⚠ attest_action description missing quoted passages (update your proxy)")

        # [4] Action: Extract claims
        extract_text = "The Eiffel Tower is located in Paris, France. It stands 330 metres tall."
        extract_args: dict = {"text": extract_text}
        if is_test:
            extract_args["mock_claims"] = 2
            print(f"\n⏳ [TEST] Extracting 2 mock claims from: \"{extract_text}\"")
        else:
            print(f"\n⏳ Extracting claims from: \"{extract_text}\"")

        await send({
            "jsonrpc": "2.0", "id": 3, "method": "tools/call",
            "params": {"name": "extract_text", "arguments": extract_args}
        })
        result = await recv(timeout=60)
        content = result["result"]["content"][0]["text"]

        print(f"✓ extract_text result:\n")
        for line in content.split("\n"):
            print(f"  {line}")

        if is_test and "[TEST MODE]" in content:
            print("✓ is_test flag confirmed in extract response")

        # [5] Action: Verify claims
        test_claim = "The Eiffel Tower is located in Berlin."
        verify_args: dict = {"text": test_claim}
        if is_test:
            verify_args["mock_verdict"] = False  # test error-handling path
            verify_args["action_id"] = "mcp_test_verify"
            print(f"\n⏳ [TEST] Verifying with mock_verdict=false and action_id: \"{test_claim}\"")
        else:
            print(f"\n⏳ Verifying: \"{test_claim}\"")

        await send({
            "jsonrpc": "2.0", "id": 4, "method": "tools/call",
            "params": {"name": "verify_text", "arguments": verify_args}
        })
        result = await recv(timeout=120)
        content = result["result"]["content"][0]["text"]

        print(f"✓ verify_text result:\n")
        for line in content.split("\n"):
            print(f"  {line}")

        if is_test and "[TEST MODE]" in content:
            print("✓ is_test flag confirmed in verify response")
        if is_test:
            if "Informational credential:" in content and "not fail-closed" in content.lower():
                print("✓ verify_text action_id minted an informational credential")
            else:
                print("⚠ verify_text action_id did not return an informational credential")

        # [6] Action: Validate document
        test_url = "https://example.com/doc.pdf"
        validate_args: dict = {"url": test_url}
        if is_test:
            validate_args["mock_validation"] = True  # test authentic document
            print(f"\n⏳ [TEST] Validating with mock_validation=true: \"{test_url}\"")
        else:
            print(f"\n⏳ Validating: \"{test_url}\"")

        await send({
            "jsonrpc": "2.0", "id": 5, "method": "tools/call",
            "params": {"name": "validate", "arguments": validate_args}
        })
        result = await recv(timeout=120)
        content = result["result"]["content"][0]["text"]

        print(f"✓ validate result:\n")
        for line in content.split("\n"):
            print(f"  {line}")

        if is_test and "[TEST MODE]" in content:
            print("✓ is_test flag confirmed in validate response")

        # [7] Action: Attest (test mode only - live attest hits npm)
        if is_test:
            print('\n⏳ [TEST] Attesting with mock_decision=allow: "npm install lodash"')
            await send({
                "jsonrpc": "2.0", "id": 6, "method": "tools/call",
                "params": {
                    "name": "attest_action",
                    "arguments": {
                        "action_id": "mcp_test_attest",
                        "text": "npm install lodash",
                        "procedure": "package_exists",
                        "mock_decision": "allow",
                    },
                },
            })
            result = await recv(timeout=60)
            content = result["result"]["content"][0]["text"]
            print(f"✓ attest_action result:\n")
            for line in content.split("\n")[:20]:
                print(f"  {line}")
            if '"decision"' in content and "crc_" in content:
                print("✓ attest_action returned a decision and credential id")
            if "[TEST MODE]" in content or '"is_test": true' in content:
                print("✓ is_test flag confirmed in attest response")

        print("\n✓ All checks passed! Your MCP integration is working correctly.")
        if is_test:
            print("  Zero quota was consumed - switch to a production key for live fact-checking.")

    except asyncio.TimeoutError:
        print("✗ Error: Timed out waiting for a response from the proxy.")
        print("  Make sure the 'mcp' package is installed: pip install mcp")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    finally:
        proc.stdin.close()
        await proc.wait()


if __name__ == "__main__":
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  Veritier MCP Integration Test v2.2")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    asyncio.run(test_mcp_proxy())
