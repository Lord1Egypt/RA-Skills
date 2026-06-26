#!/usr/bin/env python3
"""
Evaluate a skill across all dimensions and return a score.
Usage: evaluate_skill.py <skill_name> [--local | --clawhub <skill_id>]
"""

import argparse
import json
import subprocess
import sys
from typing import Dict, Any


def run_cmd(cmd: list) -> tuple:
    """Run a command and return (stdout, stderr, returncode)."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode


def evaluate_local_skill(skill_name: str) -> Dict[str, Any]:
    """Evaluate a locally installed skill."""
    # Get skill info
    stdout, _, rc = run_cmd(["openclaw", "skills", "list"])
    if rc != 0:
        return {"error": "Failed to list local skills"}
    
    # Parse skill list to find the skill
    # This is a simplified version - actual implementation would parse properly
    
    # Default scoring for local skills (assume vetted)
    return {
        "skill_name": skill_name,
        "source": "local",
        "scores": {
            "quality": 85,  # Local skills assumed good quality
            "token_cost": 70,  # Neutral - will be refined with usage
            "security": 90,  # Local skills assumed safer
            "speed": 75   # Neutral
        },
        "estimates": {
            "tokens": "unknown",
            "time_seconds": "unknown"
        },
        "notes": "Local skill - assumed vetted"
    }


def evaluate_clawhub_skill(skill_id: str) -> Dict[str, Any]:
    """Evaluate a skill from clawhub."""
    # Search for skill info on clawhub
    stdout, _, rc = run_cmd(["clawhub", "info", skill_id])
    
    if rc != 0:
        return {"error": f"Failed to fetch skill info for {skill_id}"}
    
    # Parse clawhub output
    # This is a placeholder - actual implementation would parse JSON/output
    
    # Security check placeholder
    security_issues = check_security(skill_id)
    
    return {
        "skill_name": skill_id,
        "source": "clawhub",
        "scores": {
            "quality": 0,  # To be filled from clawhub data
            "token_cost": 0,
            "security": 100 if not security_issues else 30,
            "speed": 0
        },
        "security_check": security_issues or "passed",
        "estimates": {
            "tokens": "unknown",
            "time_seconds": "unknown"
        }
    }


def check_security(skill_id: str) -> list:
    """Perform basic security checks on a skill."""
    issues = []
    
    # Download and inspect skill code
    stdout, _, rc = run_cmd(["clawhub", "download", "--dry-run", skill_id])
    
    if rc != 0:
        return ["Failed to download for security check"]
    
    # Check for suspicious patterns (placeholder)
    # Real implementation would:
    # - Scan for network calls
    # - Check file system access patterns
    # - Look for credential access
    # - Verify author reputation
    
    return issues


def calculate_final_score(scores: Dict[str, int]) -> float:
    """Calculate weighted final score."""
    weights = {
        "quality": 0.35,
        "token_cost": 0.30,
        "security": 0.20,
        "speed": 0.15
    }
    
    final = sum(scores.get(k, 0) * w for k, w in weights.items())
    return round(final, 2)


def main():
    parser = argparse.ArgumentParser(description="Evaluate a skill")
    parser.add_argument("skill_name", help="Name of the skill to evaluate")
    parser.add_argument("--local", action="store_true", help="Evaluate local skill")
    parser.add_argument("--clawhub", metavar="ID", help="Evaluate clawhub skill by ID")
    
    args = parser.parse_args()
    
    if args.local:
        result = evaluate_local_skill(args.skill_name)
    elif args.clawhub:
        result = evaluate_clawhub_skill(args.clawhub)
    else:
        # Try local first, then clawhub
        result = evaluate_local_skill(args.skill_name)
        if "error" in result:
            result = evaluate_clawhub_skill(args.skill_name)
    
    if "error" in result:
        print(json.dumps(result, indent=2))
        sys.exit(1)
    
    # Calculate final score
    result["final_score"] = calculate_final_score(result["scores"])
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
