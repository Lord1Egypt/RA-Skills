#!/usr/bin/env python3
"""
Calendar Meeting Scheduler

Create event + add participants + find & book meeting room.
Usage: python calendar_schedule_meeting.py --title "Team Meeting" --date 2024-03-29 --time 14:00 --duration 60 --users user1,user2
"""

import argparse
import subprocess
import json
import sys
from datetime import datetime, timedelta


def run_dws(args):
    """Run dws command and return JSON output."""
    cmd = ["dws"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def run_dws_action(args, execute=False):
    """Run dws action command.
    
    Args:
        args: Command arguments
        execute: If True, add --yes to perform mutation. Default is False (dry-run).
    
    Safety: Defaults to dry-run mode. Must explicitly pass execute=True to mutate.
    """
    cmd = ["dws"] + args
    if execute:
        cmd.append("--yes")
    else:
        cmd.append("--dry-run")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return False
    print(result.stdout)
    return True


def search_meeting_room(keyword="Meeting Room"):
    """Search for available meeting rooms."""
    result = run_dws(["calendar", "room", "search", "--keyword", keyword])
    if not result:
        return []
    return result.get("result", [])


def create_event(title, start_time, end_time, participants=None, location=None, dry_run=False):
    """Create calendar event."""
    args = [
        "calendar", "event", "create",
        "--title", title,
        "--start", start_time,
        "--end", end_time
    ]
    
    if participants:
        args.extend(["--participants", participants])
    if location:
        args.extend(["--location", location])
    
    return run_dws_action(args, dry_run)


def main():
    parser = argparse.ArgumentParser(description="Schedule meeting with room booking")
    parser.add_argument("--title", required=True, help="Meeting title")
    parser.add_argument("--date", required=True, help="Meeting date (YYYY-MM-DD)")
    parser.add_argument("--time", default="14:00", help="Meeting time (HH:MM)")
    parser.add_argument("--duration", type=int, default=60, help="Duration in minutes")
    parser.add_argument("--users", help="Participant user IDs (comma-separated)")
    parser.add_argument("--room-keyword", default="Meeting Room", help="Meeting room search keyword")
    parser.add_argument("--execute", action="store_true", help="Actually book meeting (default is dry-run)")
    
    args = parser.parse_args()
    
    # Safety: Default to dry-run
    execute = args.execute
    
    # Calculate start and end times
    start_dt = datetime.strptime(f"{args.date} {args.time}", "%Y-%m-%d %H:%M")
    end_dt = start_dt + timedelta(minutes=args.duration)
    
    start_iso = start_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_iso = end_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    print(f"Scheduling meeting:")
    print(f"  Title: {args.title}")
    print(f"  Date: {args.date}")
    print(f"  Time: {args.time} ({args.duration} min)")
    print(f"  Participants: {args.users or 'None'}")
    
    if not execute:
        print("\n⚠️  DRY-RUN MODE (default)")
        print("No booking will be made. Use --execute to actually book.")
    
    # Search for meeting room
    print(f"\nSearching for meeting room: {args.room_keyword}")
    rooms = search_meeting_room(args.room_keyword)
    
    if not rooms:
        print("No meeting rooms found")
        sys.exit(1)
    
    print(f"Found {len(rooms)} room(s):")
    for room in rooms[:3]:  # Show first 3
        print(f"  - {room.get('name', 'Unknown')} (Capacity: {room.get('capacity', 'N/A')})")
    
    # Use first available room
    room = rooms[0]
    room_name = room.get("name", "Unknown")
    print(f"\nSelected room: {room_name}")
    
    # Create event
    print(f"\nCreating calendar event...")
    if create_event(args.title, start_iso, end_iso, args.users, room_name, execute=execute):
        print("Meeting scheduled successfully!")
    else:
        print("Failed to schedule meeting")
        sys.exit(1)


if __name__ == "__main__":
    main()
