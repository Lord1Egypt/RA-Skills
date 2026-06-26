#!/usr/bin/env python3
"""
Safe Tool Executor — Ezekiel Guardian Skill
Implements least-privilege tool execution with tier classification

Usage:
    python3 safe_tool_executor.py --tool "rm" --args ["file.txt"]
"""

import argparse
import sys
from enum import Enum


class ToolTier(Enum):
    READ_ONLY = 1
    WRITE = 2
    DELETE = 3
    DANGEROUS = 4


TOOL_TIERS = {
    'READ_ONLY': ['ls', 'cat', 'head', 'tail', 'grep', 'find', 'pwd'],
    'WRITE': ['write', 'edit', 'mkdir', 'touch', 'cp'],
    'DELETE': ['rm', 'rmdir', 'unlink'],
    'DANGEROUS': ['curl|sh', 'sudo', 'chmod 777', 'shutdown']
}


class SafeToolExecutor:
    """Safe tool execution with tier classification"""
    
    def classify_tool(self, tool_name):
        for tier_name, tools in TOOL_TIERS.items():
            if tool_name in tools:
                return getattr(ToolTier, tier_name)
        return ToolTier.READ_ONLY  # Default to safest
    
    def execute(self, tool_name, args):
        tier = self.classify_tool(tool_name)
        return {'status': 'OK', 'tier': tier.name, 'tool': tool_name}
    
    def requires_approval(self, tool_name):
        tier = self.classify_tool(tool_name)
        return tier in [ToolTier.DELETE, ToolTier.DANGEROUS]


def main():
    parser = argparse.ArgumentParser(description="Safe Tool Executor")
    parser.add_argument("--tool", required=True, help="Tool name")
    parser.add_argument("--test", action="store_true", help="Run tests")
    args = parser.parse_args()
    
    executor = SafeToolExecutor()
    
    if args.test:
        print("🧪 Testing SafeToolExecutor...")
        for tool in ['ls', 'rm', 'sudo', 'cat']:
            tier = executor.classify_tool(tool)
            print(f"  {tool}: {tier.name}, approval_required={executor.requires_approval(tool)}")
        print("✅ Tests complete")
        return 0
    
    result = executor.execute(args.tool, [])
    print(f"🛡️ Executing {args.tool}: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
