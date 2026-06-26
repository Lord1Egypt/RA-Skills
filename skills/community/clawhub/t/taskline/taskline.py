#!/usr/bin/env python3
"""
Main Taskline skill handler for OpenClaw integration.
Routes natural language requests through the AI dispatcher.
"""

import subprocess
import sys
import os

def handle_taskline_request(user_request: str) -> None:
    """
    Main entry point for Taskline natural language requests.
    Routes through AI dispatcher for intelligent processing.
    """
    # Ensure we're in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Route through AI dispatcher
    try:
        subprocess.run([
            'python3', 
            'scripts/taskline_ai.py', 
            user_request
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Taskline processing failed with exit code {e.returncode}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Taskline AI dispatcher not found. Please check installation.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("🤖 Taskline - AI-Powered Task Management")
        print()
        print("Usage: python taskline.py 'natural language request'")
        print()
        print("✨ Examples:")
        print("  'Add high priority task for Mobile project: fix login by Friday'")
        print("  'Ask Sarah to review the API docs by next Monday'") 
        print("  'What tasks are overdue?'")
        print("  'Show my in-progress tasks'")
        print("  'Mark the authentication task as done'")
        print()
        print("🧠 AI Features:")
        print("  📅 Smart dates: tomorrow, Friday, next week, end of week")
        print("  🏗️  Auto project creation and assignment") 
        print("  👥 People detection and executor assignment")
        print("  🔥 Priority intelligence: urgent, high, medium, low")
        print("  🤖 Intent detection: create, update, query")
        sys.exit(1)
    
    # Process the natural language request
    user_input = " ".join(sys.argv[1:])
    handle_taskline_request(user_input)