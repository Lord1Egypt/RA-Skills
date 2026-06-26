#!/usr/bin/env python3
"""
Analyze git changes to identify documentation impact.

This script helps identify which documentation files need to be updated
based on code changes in the current branch.
"""

import subprocess
import sys
import json
import argparse
from pathlib import Path

def run_git_command(args):
    """Run git command and return output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {' '.join(args)}", file=sys.stderr)
        print(f"Error: {e.stderr}", file=sys.stderr)
        return None

def get_changed_files(base_branch="main"):
    """Get list of changed files between base branch and HEAD."""
    # Try common base branches
    base_branches = [base_branch, "canary", "master", "develop"]
    
    for branch in base_branches:
        try:
            # Check if branch exists
            subprocess.run(["git", "rev-parse", "--verify", branch], 
                         capture_output=True, check=True)
            diff_cmd = ["diff", f"{branch}...HEAD", "--name-only"]
            changed_files = run_git_command(diff_cmd)
            if changed_files:
                return changed_files.split('\n')
        except subprocess.CalledProcessError:
            continue
    
    # Fallback: use HEAD~1
    changed_files = run_git_command(["diff", "HEAD~1", "--name-only"])
    if changed_files:
        return changed_files.split('\n')
    
    return []

def identify_doc_relevant_changes(changed_files):
    """Identify which changed files are relevant for documentation."""
    doc_relevant_patterns = [
        "packages/next/src/client/components/",
        "packages/next/src/server/",
        "packages/next/src/shared/lib/",
        "packages/next/src/build/",
        "packages/next/src/lib/",
        "packages/next/src/cli/",
        "docs/"
    ]
    
    relevant_files = []
    for file_path in changed_files:
        if any(pattern in file_path for pattern in doc_relevant_patterns):
            relevant_files.append(file_path)
    
    return relevant_files

def main():
    parser = argparse.ArgumentParser(description="Analyze git changes for doc impact")
    parser.add_argument("--base-branch", default="main", 
                       help="Base branch to compare against (default: main)")
    parser.add_argument("--json", action="store_true", 
                       help="Output in JSON format")
    
    args = parser.parse_args()
    
    changed_files = get_changed_files(args.base_branch)
    if not changed_files:
        print("No changed files found", file=sys.stderr)
        return 1
    
    relevant_files = identify_doc_relevant_changes(changed_files)
    
    if args.json:
        result = {
            "all_changed_files": changed_files,
            "doc_relevant_files": relevant_files,
            "total_changed": len(changed_files),
            "doc_relevant_count": len(relevant_files)
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"Total changed files: {len(changed_files)}")
        print(f"Documentation-relevant files: {len(relevant_files)}")
        print("\nRelevant files:")
        for file_path in relevant_files:
            print(f"  - {file_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())