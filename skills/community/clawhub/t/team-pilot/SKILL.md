---
name: team-pilot
description: Set up and operate TeamPilot from zero on a clean machine. Use when cloning the TeamPilot repository, installing dependencies, starting the multi-agent runtime, driving missions in auto/manual mode, replaying runs in web UI, and troubleshooting first-run issues.
---

Bootstrap and run TeamPilot end-to-end.

## Zero-to-run setup (clean environment)

1. Ensure prerequisites:
   - `git --version`
   - `node --version` (recommend Node 20+)
   - `npm --version`
2. Clone repository:
   - `git clone <TEAM_PILOT_REPO_URL> team-pilot`
   - `cd team-pilot`
3. Install dependencies:
   - `npm install`
4. Start service:
   - `npm run up`
5. Open web UI:
   - `http://localhost:3333`

If `EADDRINUSE` appears, stop the process occupying port 3333 or start with another port:
- `PORT=3334 npm run up`
- then open `http://localhost:3334`

## First mission (recommended flow)

1. In Mission Control, select a template.
2. Set execution mode:
   - `auto` for smoke tests
   - `manual` for deterministic demos and controlled outputs
3. Fill mission goal and launch.
4. Confirm graph starts changing (agent lane → task lane → result lane).

## Manual mode operation standard

For each task, update in two steps:

1. `task_started` (status=`running`, progress around `20-60`)
2. `task_done` (status=`done`, progress=`100`, complete output)

Endpoint:
- `POST /api/tasks/:taskId/update`

Suggested payload fields:
- `status`, `progress`, `output`, `score`, `eventType`, `assignee`

## Replay workflow

1. Switch to Replay mode.
2. Load a run with frames > 1.
3. Scrub slider to inspect each frame.
4. Open node detail to verify input/output at each step.

## Minimal API checklist

- `POST /api/missions` (create mission)
- `GET /api/state` (live state)
- `POST /api/tasks/:taskId/update` (manual updates)
- `GET /api/runs` (list traces)
- `GET /api/runs/:missionId` (load replay trace)
- `POST /api/missions/:missionId/mode` (auto/manual switch)

## Troubleshooting

- UI opens but no updates:
  - verify server log has no crash
  - verify WebSocket `/ws` is connected
- Replay seems flat:
  - ensure selected run has `frames > 1`
  - ensure task updates were posted to `/api/tasks/:taskId/update`
- Mission stuck queued:
  - check dependency chain and assignee spelling
  - in manual mode, ensure leader is sending task updates

## Output quality bar (content pipelines)

- PLAN: goal, structure, acceptance criteria
- RESEARCH: sources, extracted facts, citations
- VERIFY: confidence, risks, uncertainty
- BUILD: complete final draft
- DELIVER: publish-ready summary + readiness note
