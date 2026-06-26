#!/usr/bin/env python3
"""
Calendar Free Slot Finder

Find common free time slots across multiple participants.
Usage: python calendar_free_slot_finder.py --user-ids user1,user2,user3 --date 2024-03-29
"""

import argparse
import subprocess
import json
import sys
from datetime import datetime, timedelta


def run_dws(args):
    """Run dws command and return JSON output."""
    cmd = ["dws"] + args + ["--jq", ".result"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def get_busy_slots(user_ids, start_time, end_time):
    """Get busy slots for all users."""
    result = run_dws([
        "calendar", "participant", "busy",
        "--user-ids", user_ids,
        "--start", start_time,
        "--end", end_time
    ])
    
    if not result:
        return []
    
    busy_slots = []
    for slot in result.get("busySlots", []):
        busy_slots.append({
            "start": slot.get("startTime"),
            "end": slot.get("endTime")
        })
    
    return busy_slots


def find_free_slots(busy_slots, work_start="09:00", work_end="18:00", slot_duration=30):
    """Find free slots given busy periods."""
    if not busy_slots:
        return []
    
    # Parse work hours
    work_start_h, work_start_m = map(int, work_start.split(":"))
    work_end_h, work_end_m = map(int, work_end.split(":"))
    
    # Sort busy slots by start time
    busy_slots.sort(key=lambda x: x["start"])
    
    free_slots = []
    current_time = None
    
    for busy in busy_slots:
        busy_start = datetime.fromisoformat(busy["start"].replace("Z", "+00:00"))
        busy_end = datetime.fromisoformat(busy["end"].replace("Z", "+00:00"))
        
        if current_time is None:
            current_time = busy_start.replace(hour=work_start_h, minute=work_start_m)
        
        if current_time < busy_start:
            # Found a free slot
            duration = (busy_start - current_time).total_seconds() / 60
            if duration >= slot_duration:
                free_slots.append({
                    "start": current_time.isoformat(),
                    "end": busy_start.isoformat(),
                    "duration_minutes": duration
                })
        
        current_time = max(current_time, busy_end)
    
    # Check end of day
    work_end_time = current_time.replace(hour=work_end_h, minute=work_end_m)
    if current_time < work_end_time:
        duration = (work_end_time - current_time).total_seconds() / 60
        if duration >= slot_duration:
            free_slots.append({
                "start": current_time.isoformat(),
                "end": work_end_time.isoformat(),
                "duration_minutes": duration
            })
    
    return free_slots


def main():
    parser = argparse.ArgumentParser(description="Find common free slots across participants")
    parser.add_argument("--user-ids", required=True, help="Comma-separated user IDs")
    parser.add_argument("--date", required=True, help="Date (YYYY-MM-DD)")
    parser.add_argument("--work-start", default="09:00", help="Work start time (HH:MM)")
    parser.add_argument("--work-end", default="18:00", help="Work end time (HH:MM)")
    parser.add_argument("--slot-duration", type=int, default=30, help="Minimum slot duration in minutes")
    
    args = parser.parse_args()
    
    # Convert date to ISO format
    start_time = f"{args.date}T00:00:00Z"
    end_time = f"{args.date}T23:59:59Z"
    
    print(f"Finding free slots for {args.user_ids} on {args.date}...")
    
    # Get busy slots
    busy_slots = get_busy_slots(args.user_ids, start_time, end_time)
    
    if busy_slots is None:
        print("Failed to get busy slots", file=sys.stderr)
        sys.exit(1)
    
    print(f"Found {len(busy_slots)} busy periods")
    
    # Find free slots
    free_slots = find_free_slots(
        busy_slots,
        args.work_start,
        args.work_end,
        args.slot_duration
    )
    
    if not free_slots:
        print("No common free slots found")
        sys.exit(0)
    
    print(f"\nAvailable time slots:")
    for slot in free_slots:
        start = datetime.fromisoformat(slot["start"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(slot["end"].replace("Z", "+00:00"))
        print(f"  {start.strftime('%H:%M')} - {end.strftime('%H:%M')} ({slot['duration_minutes']} min)")


if __name__ == "__main__":
    main()
