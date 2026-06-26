#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_items

def get_prefix(item):
    if item.get("tiny") and item.get("energy") == "low":
        return "[Quick Win]"
    if item.get("type") == "commitment":
        return "[Honor the Promise]"
    if item.get("deadline"):
        return "[Avoid Firefighting]"

    created_at = item.get("created_at")
    if created_at:
        age_hours = (datetime.now() - datetime.fromisoformat(created_at)).total_seconds() / 3600
        if age_hours < 4:
            return "[Strike While Hot]"

    return "[Light Forward Motion]"

def score_item(item, energy=None, max_minutes=None):
    score = 0
    status = item.get("status")

    if status not in ["todo", "in_progress", "waiting"]:
        return -9999
    if status == "blocked":
        return -9999

    temp = item.get("temperature")
    if temp == "hot":
        score += 25
    elif temp == "warm":
        score += 10
    else:
        score -= 15

    if item.get("tiny"):
        score += 12

    if item.get("type") == "commitment":
        score += 20

    if energy and item.get("energy") == energy:
        score += 20
    elif energy and item.get("energy") != energy:
        score -= 10

    duration = item.get("duration_mins")
    if max_minutes:
        if duration is None:
            score -= 5
        elif duration <= max_minutes:
            score += 18
        else:
            overflow = duration - max_minutes
            score -= min(45, 12 + overflow // 4)

    if item.get("deadline"):
        score += 18

    if item.get("do_date"):
        try:
            do_date = datetime.fromisoformat(item["do_date"])
            if do_date.date() <= datetime.now().date():
                score += 15
        except ValueError:
            pass

    score += int(item.get("hot_score", 0) / 10)
    return score

def clearly_mismatched(item, energy=None, max_minutes=None):
    duration = item.get("duration_mins")
    energy_mismatch = bool(energy and item.get("energy") and item.get("energy") != energy)
    time_mismatch = bool(max_minutes and duration and duration > max_minutes)
    return energy_mismatch or time_mismatch

def reason_for(item, energy=None, max_minutes=None):
    duration = item.get("duration_mins")

    if item.get("tiny") and item.get("energy") == "low":
        return "Low friction, low energy cost, and easy to finish right now."
    if max_minutes and duration and duration > max_minutes:
        return "Important, but larger than your current time window, so it fits better later or after breakdown."
    if item.get("type") == "commitment":
        return "This is a commitment to someone else, so clearing it reduces social and mental pressure."
    if item.get("deadline"):
        return "It has a deadline, and handling it now helps you avoid future firefighting."
    if item.get("temperature") == "hot":
        return "It is still fresh in your mind, so this is the easiest moment to move it forward."
    return "This is the clearest next step that keeps your momentum moving."

def main():
    parser = argparse.ArgumentParser(description="Recommend what to do next")
    parser.add_argument("--energy", choices=["low", "medium", "high"])
    parser.add_argument("--max_minutes", type=int)
    args = parser.parse_args()

    data = load_items()
    items = list(data.get("items", {}).values())

    scored = []
    for item in items:
        scored.append((score_item(item, energy=args.energy, max_minutes=args.max_minutes), item))

    scored.sort(key=lambda x: x[0], reverse=True)
    picks = [item for score, item in scored if score > 0][:3]

    if not picks:
        print("No strong next action stands out right now.")
        print("Try a weekly review, or capture anything that is still looping in your head.")
        return

    if len(picks) == 1 and clearly_mismatched(picks[0], energy=args.energy, max_minutes=args.max_minutes):
        print("No strong next action fits your current window.")
        print("Consider capturing a smaller next step, breaking down a larger project, or revisiting later.")
        return

    labels = ["Top Pick", "Backup", "Backup"]
    for idx, item in enumerate(picks):
        print(f"{labels[idx]} — {get_prefix(item)} {item['title']}")
        print(f"  {reason_for(item, energy=args.energy, max_minutes=args.max_minutes)}")
        if item.get("duration_mins"):
            print(f"  Estimated time: {item['duration_mins']} min")
        print()

if __name__ == "__main__":
    main()
