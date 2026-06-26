---
name: wger-fitness
description: Manage gym routines and fitness tracking in wger via API. Use for viewing, editing, creating workouts, logs, nutrition plans, and progress analysis. Integrates with OpenClaw crons/subagents for automated tracking. Triggers on fitness/gym/wger queries: (1) Log workouts, (2) View routines/plans, (3) Update goals, (4) Generate reports, (5) API-based pulls/pushes.
---

# wger Fitness Manager

wger is an open-source fitness tracker with REST API for routines, logs, nutrition, and progress. This skill handles API interactions for seamless integration with OpenClaw (exec/curl for calls, subagents for analysis).

## Setup (One-Time)
- API Base: https://wger.de/api/v2/ (or self-hosted URL).
- Auth: Token from wger dashboard (User > API). Set env WGER_TOKEN=your_key or pass in commands.
- Test: exec curl -H "Authorization: Token $WGER_TOKEN" https://wger.de/api/v2/workout/ (lists routines).

## Core Workflows

### 1. View Routines & Plans
Load current workouts/logs.

Example:
- List routines: exec curl -H "Authorization: Token $WGER_TOKEN" "https://wger.de/api/v2/workout/?format=json&limit=5"
- Get log: exec curl -H "Authorization: Token $WGER_TOKEN" "https://wger.de/api/v2/workoutlog/?workout=[ID]&format=json"
- Analyze: Subagent parses JSON (reps/weight trends), ties to goals (e.g., "Squat progress +10lbs—good for stamina").

Action: Use read tool on scripts/view_logs.py for formatted output.

### 2. Edit/Create Workouts
Add/update routines/logs.

Example:
- Create log: exec curl -X POST -H "Authorization: Token $WGER_TOKEN" -H "Content-Type: application/json" -d '{"date": "2026-04-15", "workout": [ID], "exercises": [{"reps": 10, "weight": 135, "exercise": [SQUAT_ID]}]}' https://wger.de/api/v2/workoutlog/
- Update routine: exec curl -X PATCH -H "Authorization: Token $WGER_TOKEN" -H "Content-Type: application/json" -d '{"name": "Updated Cyber Grind"}' https://wger.de/api/v2/workout/[ID]/

Action: Run scripts/create_log.py or edit_log.py with params (date, exercise, reps).

### 3. Nutrition & Goals
Track meals, set targets.

Example:
- Log meal: exec curl -X POST -H "Authorization: Token $WGER_TOKEN" -d '{"date": "2026-04-15", "meal": [ID], "nutritional_values": {"calories": 500, "protein": 30}}' https://wger.de/api/v2/nutritionlog/
- View goals: exec curl -H "Authorization: Token $WGER_TOKEN" https://wger.de/api/v2/weight/

Action: Use references/nutrition.md for macros; scripts/set_goal.py for updates.

### 4. Reports & Analysis
Generate progress, export.

Example:
- Progress report: exec python scripts/generate_report.py --period week --output pdf (uses API for data, matplotlib for charts).
- Cron Integration: In subagents, pull data, analyze (e.g., "Adherence 80%—suggest HIIT for JITA").

## Bundled Resources
- scripts/view_logs.py: Fetch and format logs (JSON to readable).
- scripts/create_log.py: POST new workout entry (params: date, routine_id, exercises).
- references/api_endpoints.md: Full wger API ref (routines, logs, nutrition).
- assets/progress_template.html: Basic chart template for reports.

## When to Use
Trigger on: "Log my workout", "View wger routine", "Update fitness plan", "wger API call", "Fitness progress report". For automation: Crons/subagents (e.g., daily pull to health.md).

Security: Token in env; self-host for privacy (Docker setup in references/selfhost.md). Rate: 100/min—fine for pulls.
