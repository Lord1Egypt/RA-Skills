# Rec League Scheduler

**The volunteer's scheduling brain: fixtures, real-attendance rotation, fairness audit, standings.**

## The problem

Volunteer-run rec leagues — badminton, squash, padel, chess, football 7s,
darts — all die the same death: scheduling becomes a second job for one
unpaid person, and the group chat becomes the database. Nobody knows who's
played whom, two players have absorbed 5 byes while others got zero, and the
standings are a photo of a whiteboard from three weeks ago.

## What it does

| Command | What you get |
|---|---|
| `player add` | Roster with optional 1–5 skill levels |
| `fixtures` | Circle-method round-robin (single/double), courts + rotating byes |
| `night` | **Match-day re-flow**: present players fill courts, byes go to the least-benched, printable sheet with score blanks |
| `absent` | Availability registry per date |
| `result` / `standings` | Scores → points table with head-to-head tiebreakers |
| `audit` | Fairness report: games/byes within ±1, no back-to-back byes, no repeated pairs |

## Quick start

```bash
python3 scripts/league.py player add "Alex" --level 4   # ×5-20 players
python3 scripts/league.py fixtures --courts 2            # season plan
python3 scripts/league.py night --courts 2 --absent "Sam,Kim"   # real Tuesday
python3 scripts/league.py result "Alex" 21 15 "Mel"
python3 scripts/league.py standings
python3 scripts/league.py audit
```

100% local (`league.json`), printable, no accounts — the anti-SaaS league tool.

## The guarantee

Circle-method fixtures mean **every pair meets exactly once per cycle**; the
night re-flow means **absences never consume playing time** and byes always
fall to the players with the fewest. The audit proves it with numbers.

MIT License. © 2026 Denis Voronin
