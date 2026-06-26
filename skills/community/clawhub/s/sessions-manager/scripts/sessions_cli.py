#!/usr/bin/env python3
"""
Sessions Manager CLI - List and delete OpenClaw sessions
"""

import json
import os
import sys
import argparse
from pathlib import Path

SESSIONS_FILE = Path.home() / ".openclaw" / "agents" / "main" / "sessions" / "sessions.json"
SESSIONS_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"


def load_sessions():
    """Load sessions from sessions.json"""
    if not SESSIONS_FILE.exists():
        return {}
    
    with open(SESSIONS_FILE, 'r') as f:
        return json.load(f)


def save_sessions(sessions):
    """Save sessions to sessions.json"""
    SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SESSIONS_FILE, 'w') as f:
        json.dump(sessions, f, indent=2)


def list_sessions(verbose=False):
    """List all sessions with their status"""
    sessions = load_sessions()
    
    if not sessions:
        print("No sessions found.")
        return
    
    print(f"Found {len(sessions)} session(s):\n")
    
    for session_key, session_data in sessions.items():
        session_id = session_data.get('sessionId', 'unknown')
        status = session_data.get('status', 'unknown')
        label = session_data.get('label', '')
        model = session_data.get('model', session_data.get('modelOverride', 'default'))
        started_at = session_data.get('startedAt', 0)
        updated_at = session_data.get('updatedAt', 0)
        
        # Format timestamp
        from datetime import datetime
        started_str = datetime.fromtimestamp(started_at/1000).strftime('%Y-%m-%d %H:%M:%S') if started_at else 'N/A'
        
        # Calculate duration
        duration_ms = updated_at - started_at if started_at and updated_at else 0
        duration_str = f"{duration_ms/1000:.1f}s" if duration_ms > 0 else 'N/A'
        
        print(f"📌 {session_key}")
        print(f"   ID: {session_id}")
        if label:
            print(f"   Label: {label}")
        print(f"   Status: {status}")
        print(f"   Model: {model}")
        print(f"   Started: {started_str}")
        print(f"   Duration: {duration_str}")
        
        if verbose:
            channel = session_data.get('channel', 'unknown')
            print(f"   Channel: {channel}")
            if 'lastChannel' in session_data:
                print(f"   Last Channel: {session_data.get('lastChannel')}")
        
        print()


def delete_session(session_id):
    """Delete a session by ID or session key"""
    sessions = load_sessions()
    
    # Find the session
    found_key = None
    found_data = None
    
    for session_key, session_data in sessions.items():
        if session_data.get('sessionId') == session_id or session_key == session_id:
            found_key = session_key
            found_data = session_data
            break
    
    if not found_key:
        print(f"❌ Session not found: {session_id}")
        return False
    
    # Remove from sessions.json
    del sessions[found_key]
    save_sessions(sessions)
    
    # Delete the session file if it exists
    session_file = SESSIONS_DIR / f"{found_data.get('sessionId', found_key)}.jsonl"
    if session_file.exists():
        session_file.unlink()
        print(f"🗑️  Deleted session file: {session_file}")
    
    print(f"✅ Deleted session: {found_key}")
    print(f"   ID: {found_data.get('sessionId')}")
    if found_data.get('label'):
        print(f"   Label: {found_data.get('label')}")
    
    return True


def main():
    parser = argparse.ArgumentParser(description='OpenClaw Sessions Manager')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all sessions')
    list_parser.add_argument('-v', '--verbose', action='store_true', help='Show verbose output')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a session')
    delete_parser.add_argument('id', help='Session ID or session key to delete')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        list_sessions(verbose=args.verbose)
    elif args.command == 'delete':
        delete_session(args.id)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
