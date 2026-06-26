# Skill Runner

## Purpose
This skill acts as an intermediary to run other OpenClaw skills via cron jobs or indirect calls.
It provides a secure way to execute a specific skill function within the OpenClaw runtime, ensuring the skill receives the necessary `context` object (including access to tools and sessions).

## How it works
1. Receives an `agentTurn` message (e.g., from a cron job).
2. The message content specifies which target skill to run (e.g., `run memory-enhancer`).
3. Dynamically imports and executes the `skill` function from the target skill's `index.js` file.
4. Passes its own `context` object to the target skill, allowing the target skill to use OpenClaw's tools (like `sessions_spawn`).

## Configuration
- Runs as a dedicated isolated agent.
- Uses the default model configured for agents.
- Expected message format: `run <skill-name>`

## Invocation
Primarily invoked via OpenClaw's cron jobs (`cron add` with `payload.kind="agentTurn"` targeting this skill).

## Example Cron Job Payload
```json
{
  "kind": "agentTurn",
  "message": "run memory-enhancer",
  "model": "google/gemini-2.5-flash",
  "sessionTarget": "isolated"
}
```