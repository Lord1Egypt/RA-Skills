#!/usr/bin/env python3
"""
Auto-run script for scheduled execution (cron/heartbeat).
Runs skill discovery, processes pending skills, checks and applies updates.
Designed to run 1-2 times daily (morning and evening).
"""
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

def run_command(cmd, description):
    """Run a command and report results."""
    print(f"\n{'='*50}")
    print(f"📋 {description}")
    print('='*50)
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=False,
            text=True,
            timeout=300
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"⏱️  Timeout: {description}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def auto_run():
    """Execute the full auto-guardian workflow."""
    print("🛡️  Skill Guardian Auto-Run")
    print(f"⏰ Started at: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # 1. Process pending skills (move to active after 5-10 days)
    results.append((
        "Process pending skills",
        run_command(
            f"python3 {SCRIPT_DIR}/add_skill.py --process-pending",
            "Processing pending skills (5-10 day waiting period)"
        )
    ))
    
    # 2. Check for new updates
    results.append((
        "Check for updates",
        run_command(
            f"python3 {SCRIPT_DIR}/check_updates.py",
            "Checking for skill updates"
        )
    ))
    
    # 3. Apply updates (high trust immediate, others with delay)
    results.append((
        "Apply updates",
        run_command(
            f"python3 {SCRIPT_DIR}/apply_updates.py --all",
            "Applying eligible updates (high trust = immediate)"
        )
    ))
    
    # 4. Show current status
    results.append((
        "Show registry",
        run_command(
            f"python3 {SCRIPT_DIR}/list_skills.py",
            "Current registry status"
        )
    ))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 Summary")
    print('='*50)
    for name, success in results:
        status = "✅" if success else "⚠️"
        print(f"{status} {name}")
    
    print(f"\n⏰ Completed at: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return all(r[1] for r in results)

if __name__ == "__main__":
    success = auto_run()
    sys.exit(0 if success else 1)
