#!/usr/bin/env python3
"""
skill_wrapper.py — Wrap any skill with self-learning capabilities

Usage:
    python3 skill_wrapper.py --skill my-skill --call "some_tool --arg value"

This runs the skill command, catches failures, logs them, and applies
any learned fixes before returning the result.
"""
import subprocess, sys, json, argparse
from pathlib import Path
from self_learning import (
    log_failure, log_success, learn_from_failure,
    ensure_dirs, CONTEXT_LOG, PATTERN_INDEX
)

def run_skill(skill_name: str, command: list) -> dict:
    """
    Run a skill command with self-learning wrapper.
    Returns {"success": bool, "output": str, "failure_id": str or None}
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            log_success(skill_name, {"command": " ".join(command)}, result.stdout)
            return {"success": True, "output": result.stdout, "failure_id": None}
        else:
            # Log the failure
            error_msg = result.stderr or result.stdout
            fid = log_failure(
                skill_name,
                Exception(error_msg),
                {"command": " ".join(command), "returncode": result.returncode},
                stack_trace=None
            )
            return {"success": False, "output": error_msg, "failure_id": fid}
    
    except subprocess.TimeoutExpired:
        fid = log_failure(
            skill_name,
            Exception("TimeoutExpired: command took longer than 60s"),
            {"command": " ".join(command)},
            stack_trace=None
        )
        return {"success": False, "output": "Timeout", "failure_id": fid}
    
    except Exception as e:
        fid = log_failure(
            skill_name,
            e,
            {"command": " ".join(command)},
            stack_trace=None
        )
        return {"success": False, "output": str(e), "failure_id": fid}

def main():
    parser = argparse.ArgumentParser(description="Self-learning skill wrapper")
    parser.add_argument("--skill", required=True, help="Skill name")
    parser.add_argument("--call", required=True, help="Command to run (as string)")
    parser.add_argument("--learn", action="store_true", help="Run 举一反三 after failure")
    parser.add_argument("--auto-fix", action="store_true", help="Automatically apply learned fixes")
    args = parser.parse_args()
    
    command = args.call.split()
    
    result = run_skill(args.skill, command)
    
    if result["success"]:
        print(result["output"])
        sys.exit(0)
    else:
        print(f"Error: {result['output']}", file=sys.stderr)
        
        if args.learn and result["failure_id"]:
            print(f"\nRunning 举一反三 analysis...", file=sys.stderr)
            learning = learn_from_failure(result["failure_id"])
            print(f"Patterns analyzed: {learning['patterns_analyzed']}", file=sys.stderr)
            for report in learning["fix_reports"]:
                print(f"  {report['pattern_type']}: {report['failures_fixed']} failures fixed", file=sys.stderr)
        
        if args.auto_fix:
            from self_learning import apply_learned_fixes, PATTERN_INDEX
            patterns = json.load(open(PATTERN_INDEX)) if PATTERN_INDEX.exists() else {}
            for pt in patterns.keys():
                result = apply_learned_fixes(pt)
                if result["failures_fixed"]:
                    print(f"Auto-fixed {len(result['failures_fixed'])} failures for {pt}", file=sys.stderr)
        
        sys.exit(1)

if __name__ == "__main__":
    main()
