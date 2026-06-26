#!/usr/bin/env python3
"""
Assemble file send instruction JSON
Receives file path(s) from agent, outputs JSON for plugin to parse
"""
import argparse
import json
import sys
import os
import datetime

LOG_FILE = "/tmp/yunjia-file-transfer.log"

def log(message):
    """Print log with timestamp to stderr and log file"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [yunjia-file-transfer] {message}"
    
    # Print to stderr
    print(log_line, file=sys.stderr)
    
    # Append to log file
    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_line + "\n")
    except Exception:
        pass  # Ignore file write errors

def assemble_instruction(file_paths: list, text: str = "") -> dict:
    """
    Assemble send instruction JSON
    
    Args:
        file_paths: List of absolute file paths
        text: Additional text from user request
    
    Returns:
        dict with filePaths, text and mode
    """
    log(f"Skill called with {len(file_paths)} file(s)")
    if text:
        log(f"  Text: {text}")
    
    for i, path in enumerate(file_paths, 1):
        log(f"  File {i}: {path}")
        # Validate path is absolute (cross-platform)
        # Unix/Linux: starts with /
        # Windows: starts with drive letter (C:, D:, etc.) followed by :\ or :/
        import re
        is_unix_absolute = path.startswith('/')
        is_windows_absolute = re.match(r'^[A-Za-z]:[\\/]', path) is not None
        
        if not (is_unix_absolute or is_windows_absolute):
            log(f"  ERROR: Path must be absolute: {path}")
            log(f"  Unix paths must start with / (e.g., /home/user/file.txt)")
            log(f"  Windows paths must start with drive letter (e.g., C:\\Users\\user\\file.txt)")
            return {
                "success": False,
                "error": f"Path must be absolute. Unix: /path/to/file, Windows: C:\\path\\to\\file"
            }
        # Check file exists
        if not os.path.exists(path):
            log(f"  WARNING: File does not exist: {path}")
        else:
            file_size = os.path.getsize(path)
            log(f"  File exists, size: {file_size} bytes")
    
    # Build result - text is the original user request
    result = {
        "filePaths": file_paths,
        "text": text,
        "mode": "sendFileToChat"
    }
    
    log(f"Assembled instruction: {json.dumps(result, ensure_ascii=False)}")
    log("Skill execution completed")
    
    return result

def main():
    log("=" * 50)
    log("Skill started")
    
    parser = argparse.ArgumentParser(
        description='Assemble file send instruction JSON'
    )
    parser.add_argument(
        '--file',
        required=True,
        action='append',
        help='Absolute file path (can specify multiple)'
    )
    parser.add_argument(
        '--text',
        default='',
        help='Additional text from user request'
    )
    
    args = parser.parse_args()
    
    log(f"Arguments received: {args.file}, text: {args.text}")
    
    result = assemble_instruction(args.file, args.text)
    
    # Print JSON to stdout for agent to parse
    output = json.dumps(result, ensure_ascii=False, indent=2)
    log(f"Output to stdout: {output}")
    print(output)
    
    # Exit with error if validation failed
    if not result.get("success", True):
        log("Skill failed")
        sys.exit(1)
    
    log("Skill succeeded")
    log("=" * 50)
    sys.exit(0)

if __name__ == '__main__':
    main()
