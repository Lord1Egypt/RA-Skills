#!/usr/bin/env python3
"""
System Commander - Translate natural language to optimal Linux/Python commands.
Parses user input and outputs system commands using patterns from SKILL.md.
"""

import sys
import re
import json

# Command pattern mappings - natural language to system commands
PATTERNS = {
    # File listing and search
    r"list|show|find.*files?|ls": {
        "cmd": "ls -la {path}",
        "python": "import os; print('\\n'.join(os.listdir('{path}')))"
    },
    # File content viewing
    r"cat|view|show.*content|read.*file": {
        "cmd": "cat {file}",
        "python": "with open('{file}') as f: print(f.read())"
    },
    # Line counting
    r"count.*lines?|wc.*l|how many lines": {
        "cmd": "wc -l {file}",
        "python": "print(sum(1 for _ in open('{file}')))"
    },
    # Word counting
    r"count.*words?|wc.*w": {
        "cmd": "wc -w {file}",
        "python": "print(len(open('{file}').read().split()))"
    },
    # File size
    r"size|du|disk usage|how big": {
        "cmd": "du -h {file}",
        "python": "import os; print(f'{os.path.getsize('{file}')} bytes')"
    },
    # Text search
    r"grep|search|find.*text": {
        "cmd": "grep -n '{pattern}' {file}",
        "python": "import re; [print(f'{i}:{l}') for i,l in enumerate(open('{file}'),1) if re.search('{pattern}',l)]"
    },
    # Sorting
    r"sort|order": {
        "cmd": "sort {file}",
        "python": "print(''.join(sorted(open('{file}'))))"
    },
    # Unique lines
    r"unique|uniq|dedup|remove duplicates": {
        "cmd": "sort {file} | uniq",
        "python": "print(''.join(set(open('{file}'))))"
    },
    # Extract columns
    r"cut|extract.*column|get.*field": {
        "cmd": "cut -d'{delim}' -f{field} {file}",
        "python": "[print(l.split('{delim}')[{field}-1]) for l in open('{file}')]"
    },
    # File type detection
    r"file.*type|what.*is|mime": {
        "cmd": "file {file}",
        "python": "import subprocess; print(subprocess.run(['file','{file}'],capture_output=True).stdout.decode())"
    },
    # Replace text
    r"sed|replace|substitute": {
        "cmd": "sed -i 's/{old}/{new}/g' {file}",
        "python": "f=open('{file}').read(); open('{file}','w').write(f.replace('{old}','{new}'))"
    },
    # Head/tail
    r"head|first.*lines?|top": {
        "cmd": "head -n {n} {file}",
        "python": "print(''.join(open('{file}').readlines()[:{n}]))"
    },
    r"tail|last.*lines?|bottom": {
        "cmd": "tail -n {n} {file}",
        "python": "print(''.join(open('{file}').readlines()[-{n}:]))"
    },
    # Find files
    r"find.*name|locate|search.*file": {
        "cmd": "find {path} -name '{pattern}'",
        "python": "import os; [print(os.path.join(r,f)) for r,d,files in os.walk('{path}') for f in files if '{pattern}'.replace('*','') in f]"
    },
    # Directory tree
    r"tree|directory.*structure": {
        "cmd": "tree {path}",
        "python": "import os; [print(os.path.join(r,f)) for r,d,files in os.walk('{path}') for f in files]"
    },
    # JSON processing
    r"jq|json|parse json": {
        "cmd": "cat {file} | jq '{query}'",
        "python": "import json; print(json.dumps(json.load(open('{file}')){query}))"
    },
    # CSV processing
    r"csv|tsv|parse.*csv": {
        "cmd": "awk -F',' '{print}' {file}",
        "python": "import csv; [print(r) for r in csv.reader(open('{file}'))]"
    }
}

def extract_params(text):
    """Extract parameters from natural language text."""
    params = {
        "file": None,
        "path": ".",
        "pattern": None,
        "n": 10,
        "delim": " ",
        "field": 1,
        "old": "",
        "new": "",
        "query": "."
    }
    
    # Extract file paths
    file_matches = re.findall(r'[\w\-./]+\.[\w]+|[\w\-./]+/|/[^\s]+', text)
    if file_matches:
        for m in file_matches:
            if '.' in m or m.endswith('/'):
                params["file"] = m
                params["path"] = m
                break
    
    # Extract number
    num_match = re.search(r'(\d+)', text)
    if num_match:
        params["n"] = num_match.group(1)
    
    # Extract quoted strings as pattern
    quoted = re.findall(r'["\']([^"\']+)["\']', text)
    if quoted:
        params["pattern"] = quoted[0]
    
    return params

def translate(text):
    """Translate natural language to system command."""
    text_lower = text.lower()
    params = extract_params(text)
    
    for pattern, commands in PATTERNS.items():
        if re.search(pattern, text_lower):
            try:
                cmd = commands["cmd"].format(**params)
                py_cmd = commands["python"].format(**params)
                return {
                    "success": True,
                    "bash_command": cmd,
                    "python_command": py_cmd,
                    "pattern_matched": pattern[:50]
                }
            except KeyError as e:
                return {
                    "success": False,
                    "error": f"Missing parameter: {e}",
                    "bash_command": f"# Need to specify: {e}"
                }
    
    return {
        "success": False,
        "error": "No matching pattern found",
        "suggestion": "Try: list files, count lines in file.txt, search for 'pattern' in file, head -20 file"
    }

def main():
    if len(sys.argv) < 2 and not sys.stdin.isatty():
        text = sys.stdin.read().strip()
    elif len(sys.argv) < 2:
        print("Usage: translate.py 'natural language task'", file=sys.stderr)
        print("Or: echo 'task' | translate.py", file=sys.stderr)
        sys.exit(1)
    else:
        text = " ".join(sys.argv[1:])
    
    result = translate(text)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
