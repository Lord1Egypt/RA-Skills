---
name: workflow-runner
description: Orchestrate small development workflows: parse requirements, spawn two persistent subagents (coding and testing, each with isolated 128k context), loop until tests pass, and produce local git commits. Use when a user asks to implement+test a workflow or invokes `run workflow: <spec>`.
---

# workflow-runner

Purpose

- Automate a small dev workflow inside the platform: main agent parses requirements, creates two persistent subagents (coding + testing), coordinates work and retries until tests pass, then makes a local git commit and writes artifacts to results/.

When to use

- Use when you want an end-to-end implement+test loop for a small feature or task and want persistent worker sessions for iterative work.

Core behavior (summary)

1. Main agent parses the requirement and splits into a coding task and a testing task.
2. Spawn two persistent subagents (role=coding and role=testing) with isolated contexts (128k). Subagent sessions are kept for a configurable TTL (default 24h).
3. Coding subagent implements code, produces patches and a short report.
4. Testing subagent designs and runs tests; if tests fail it returns structured failures to main agent.
5. Main agent reroutes failures to the coding subagent and repeats until tests pass or max retries reached.
6. On success: produce results/<wf-id>/, create a local git commit (no push by default).

Configurable parameters

- default_ttl_days: 1
- max_retries: 10
- auto_git_commit: true (local only)
- results_path: ./results/

Bundled resources

- scripts/ — orchestrator and helper scripts
- examples/ — a minimal sample workflow for smoke tests

How to trigger

- Natural language like: "Run workflow: implement <short spec>"
- Or explicit: `run workflow-runner: <spec>`


Notes

- The skill favors local, auditable actions (commits are local). It logs all artifacts to results/ and keeps subagent sessions available for reuse.
