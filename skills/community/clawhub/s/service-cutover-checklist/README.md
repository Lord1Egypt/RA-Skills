# Service Cutover Checklist

A skill for moving one running service from an old server to a new one: inventory both sides,
plan what moves when, rehearse on the new server, switch in a short window with a measured
outage, keep a tested rollback, observe, and only then retire the old copy.

- Works with shell access (read-only commands are given) or in paste mode, where the owner runs
  the commands and pastes the output.
- The owner performs the switch: stopping production, changing DNS, and retiring the old copy.
  The agent prepares the runbook, keeps the clock, and runs the checks.
- Every change, and every step that sends data or starts work elsewhere (a partner call, a test
  message, a backup run, a restore), is its own step and needs the owner's approval for exactly
  that step.
- Credentials are recorded by name and location only; their values are left out of every
  output.
- Nothing is deleted during the move; the old copy stays intact until the owner decides.

Written from real moves of a workflow engine with its helper services, a small monitoring app,
and a larger agent gateway between Linux servers.

Use it for: moving a web app, a workflow engine, a bot, or a small API with its data and
scheduled jobs to another server or provider.

Not for: planning a data model migration between two different systems (use a data migration
planner), or comparing desired and observed infrastructure state.
