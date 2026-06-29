# SPDX-License-Identifier: MIT
"""Offline tests for rtc-work job matching (the pure routing logic)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from rtc_work.__main__ import match_jobs

JOBS = [
    {"job_id": "a", "status": "open", "category": "code", "reward_rtc": 5, "tags": "python,cli"},
    {"job_id": "b", "status": "open", "category": "research", "reward_rtc": 2, "tags": ""},
    {"job_id": "c", "status": "claimed", "category": "code", "reward_rtc": 9, "tags": ""},
    {"job_id": "d", "status": "open", "category": "design", "reward_rtc": 1, "tags": "ui"},
    {"job_id": "e", "status": "open", "category": "misc", "reward_rtc": 8, "tags": "python"},
]

fails = 0
def check(c, label):
    global fails
    print(("  PASS: " if c else "  FAIL: ") + label)
    if not c: fails += 1

# skill filter by category
r = match_jobs(JOBS, ["code"], 0)
check([j["job_id"] for j in r] == ["a"], "category=code -> only open job a (claimed c excluded)")

# skill match via tags (job e is misc category but tagged python)
r = match_jobs(JOBS, ["python"], 0)
check(set(j["job_id"] for j in r) == {"a", "e"}, "skill=python matches via tags (a tagged python,cli + e tagged python)")

# reward floor
r = match_jobs(JOBS, [], 5)
check(set(j["job_id"] for j in r) == {"a", "e"}, "min_reward=5 keeps a(5),e(8)")

# sorted by reward desc
r = match_jobs(JOBS, [], 0)
check([j["job_id"] for j in r] == ["e", "a", "b", "d"], "sorted reward desc, claimed excluded")

# empty skills matches all open above floor
r = match_jobs(JOBS, [], 0)
check(all(j["status"] == "open" for j in r), "never returns non-open jobs")

print("\n" + ("ALL PASS" if fails == 0 else f"{fails} FAILED"))
raise SystemExit(1 if fails else 0)
