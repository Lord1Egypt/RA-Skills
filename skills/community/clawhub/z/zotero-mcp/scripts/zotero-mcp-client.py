#!/usr/bin/env python3
"""
Zotero MCP Client
A simple wrapper to call Zotero MCP server tools from command line.
"""

import json
import subprocess
import sys
import argparse

ZOTERO_MCP_SERVER = "zotero-mcp-server"

def call_mcp(tool_name, arguments=None):
    """Call a tool on the Zotero MCP server."""
    if arguments is None:
        arguments = {}
    
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    # Start the MCP server and communicate via stdin/stdout
    proc = subprocess.Popen(
        ["node", "-e", f"""
const {{ spawn }} = require('child_process');
const cp = spawn('zotero-mcp-server', {{ stdio: ['pipe', 'pipe', 'pipe'] }});
const input = {json.dumps(json.dumps(request))};
cp.stdin.write(input);
cp.stdin.end();
cp.stdout.on('data', (data) => console.log(data.toString()));
cp.stderr.on('data', (data) => console.error(data.toString()));
cp.on('close', (code) => process.exit(code));
"""],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = proc.communicate()
    
    if stderr:
        print(f"Error: {stderr}", file=sys.stderr)
    
    if stdout:
        try:
            result = json.loads(stdout)
            if "result" in result:
                return result["result"]
        except json.JSONDecodeError:
            pass
    
    return None

def main():
    parser = argparse.ArgumentParser(description="Zotero MCP Client")
    parser.add_argument("tool", help="Tool name to call")
    parser.add_argument("--arg", action="append", help="Arguments as key=value")
    parser.add_argument("--search", help="Search query (shorthand for -a q=VALUE)")
    parser.add_argument("--list-tools", action="store_true", help="List available tools")
    
    args = parser.parse_args()
    
    if args.list_tools:
        result = call_mcp("ping")
        print(json.dumps(result, indent=2))
        return
    
    arguments = {}
    if args.arg:
        for a in args.arg:
            if "=" in a:
                key, value = a.split("=", 1)
                arguments[key] = value
    
    if args.search:
        arguments["q"] = args.search
    
    result = call_mcp(args.tool, arguments)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
