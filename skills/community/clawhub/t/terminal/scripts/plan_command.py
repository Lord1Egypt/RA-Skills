#!/usr/bin/env python3
import argparse

def plan_from_intent(intent: str) -> str:
    lowered = intent.lower()

    if "current directory" in lowered or "where am i" in lowered or "pwd" in lowered:
        return "pwd"
    if "list files" in lowered or "show files" in lowered or "list directory" in lowered:
        return "ls -la"
    if "python file" in lowered or "find py files" in lowered:
        return "find . -name '*.py'"
    if "disk usage" in lowered or "folder size" in lowered or "size of this folder" in lowered:
        return "du -sh ."
    if "search text" in lowered or "grep" in lowered:
        return 'grep -R "keyword" .'
    if "show json files" in lowered:
        return "find . -name '*.json'"
    if "find markdown" in lowered or "md files" in lowered:
        return "find . -name '*.md'"
    if "show hidden files" in lowered:
        return "ls -la"
    if "recent files" in lowered:
        return "find . -type f -mtime -7"
    if "largest files" in lowered:
        return "find . -type f -exec du -h {} + | sort -h | tail -20"

    return "# Review and edit before running\n# Example:\nls -la"

def main():
    parser = argparse.ArgumentParser(description="Plan a shell command from user intent")
    parser.add_argument("--intent", required=True, help="Natural language intent")
    args = parser.parse_args()

    command = plan_from_intent(args.intent)
    print("Suggested command:")
    print(command)

if __name__ == "__main__":
    main()
