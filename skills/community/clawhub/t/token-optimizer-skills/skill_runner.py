"""
skill_runner.py — The Motor Cortex Dispatcher
Part of the Neuromorphic Agent Architecture (v3.0)

The brain's equivalent: the motor cortex executing a compiled movement program
(like riding a bike) without re-involving conscious thought.

Receives a tool name + args from the orchestrator, executes the correct script,
and returns the result + token cost delta. The agent never re-reasons about
HOW to run a known procedure — it just fires it.

Usage:
  python skill_runner.py --tool count_tokens --args '{"--input": "chat.txt", "--model": "gpt-4o"}'
  python skill_runner.py --tool distill_memory --args '{"--input": "history.json", "--output": "facts.json"}'
  python skill_runner.py --tool analyze_skills
  python skill_runner.py --list
"""

import sys
import json
import argparse
import os
import subprocess
import time

CONFIG_CANDIDATES = [
    os.path.join(os.path.dirname(__file__), "..", "orchestrator_config.json"),
    os.path.join(os.path.dirname(__file__), "orchestrator_config.json"),
    os.path.expanduser("~/.openclaw/orchestrator_config.json"),
]

SCRIPT_BASE = os.path.dirname(os.path.abspath(__file__))

def load_config() -> dict:
    for path in CONFIG_CANDIDATES:
        resolved = os.path.abspath(path)
        if os.path.exists(resolved):
            with open(resolved, "r") as f:
                return json.load(f)
    raise FileNotFoundError(
        "orchestrator_config.json not found. Checked:\n" + "\n".join(CONFIG_CANDIDATES)
    )

def resolve_script_path(script_relative: str) -> str:
    """Resolve script path relative to the skills root."""
    # Try relative to scripts/ dir first, then up one level
    candidates = [
        os.path.join(SCRIPT_BASE, os.path.basename(script_relative)),
        os.path.join(SCRIPT_BASE, "..", script_relative),
        os.path.abspath(script_relative),
    ]
    for c in candidates:
        if os.path.exists(os.path.abspath(c)):
            return os.path.abspath(c)
    raise FileNotFoundError(f"Script not found: {script_relative} (searched from {SCRIPT_BASE})")

def estimate_tokens(text: str) -> int:
    return len(text) // 4

def run_tool(tool_name: str, args_dict: dict, config: dict) -> dict:
    """
    Execute a registered tool script.
    Returns: {success, output, token_cost_estimate, duration_ms}
    """
    registry = config.get("tool_registry", {})
    if tool_name not in registry:
        return {
            "success": False,
            "error": f"Unknown tool '{tool_name}'. Register it in orchestrator_config.json.",
            "available_tools": list(registry.keys()),
        }

    entry = registry[tool_name]
    script_rel = entry.get("script")
    guardrail = entry.get("guardrail")

    # Honour guardrails — never silently bypass
    if guardrail == "OFFLINE_ONLY" and not args_dict.get("--dry-run"):
        return {
            "success": False,
            "error": (
                f"Tool '{tool_name}' has guardrail OFFLINE_ONLY. "
                "Add --dry-run flag to preview safely, or only use on offline documents. "
                "Never apply to live system prompts, schemas, or code."
            ),
        }

    try:
        script_path = resolve_script_path(script_rel)
    except FileNotFoundError as e:
        return {"success": False, "error": str(e)}

    # Build CLI command
    cmd = [sys.executable, script_path]
    for flag, value in args_dict.items():
        cmd.append(flag)
        if value is not True and value is not None:  # boolean flags have no value
            cmd.append(str(value))

    # Execute and capture
    start = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        duration_ms = int((time.time() - start) * 1000)
        output = proc.stdout.strip()
        stderr = proc.stderr.strip()

        return {
            "success": proc.returncode == 0,
            "tool": tool_name,
            "script": script_path,
            "output": output,
            "stderr": stderr if stderr else None,
            "exit_code": proc.returncode,
            "duration_ms": duration_ms,
            "token_cost_estimate": estimate_tokens(output),   # tokens the result will consume if injected into context
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"Tool '{tool_name}' timed out after 60 seconds."}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="Neuromorphic skill runner: executes compiled tool scripts without LLM reasoning."
    )
    parser.add_argument("--tool", help="Name of the tool to run (as registered in orchestrator_config.json).")
    parser.add_argument("--args", default="{}", help='JSON object of CLI args, e.g. \'{"--input": "file.txt"}\'')
    parser.add_argument("--list", action="store_true", help="List all registered tools and exit.")
    parser.add_argument("--json", action="store_true", help="Output raw JSON result.")
    args = parser.parse_args()

    try:
        config = load_config()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    registry = config.get("tool_registry", {})

    # --list mode
    if args.list:
        print("\n⚙️  Registered Procedural Tools\n")
        for name, entry in registry.items():
            guardrail = entry.get("guardrail", "none")
            print(f"  {name:<20} → {entry['script']:<40} [guardrail: {guardrail}]")
        print()
        return

    if not args.tool:
        parser.error("--tool is required unless using --list.")

    try:
        tool_args = json.loads(args.args)
    except json.JSONDecodeError as e:
        print(f"Error parsing --args JSON: {e}", file=sys.stderr)
        sys.exit(1)

    result = run_tool(args.tool, tool_args, config)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["success"]:
            print(f"\n✅ Tool '{result['tool']}' completed in {result['duration_ms']}ms")
            print(f"   Result token cost: ~{result['token_cost_estimate']} tokens if injected into context")
            print(f"\n--- Output ---\n{result['output']}")
        else:
            print(f"\n❌ Tool failed: {result.get('error', 'Unknown error')}")
            if result.get("stderr"):
                print(f"   Stderr: {result['stderr']}")

if __name__ == "__main__":
    main()
