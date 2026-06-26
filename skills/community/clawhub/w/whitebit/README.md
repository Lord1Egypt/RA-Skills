# ClawHub WhiteBIT Trading Skill

MCP-first WhiteBIT trading research, training, and API-planning workflow for OpenClaw, packaged as a ClawHub skill.

Published skill page:
- `https://clawhub.ai/zonder/whitebit`

## What This Skill Does
- Guides safe trade planning (`buy`/`sell`, market/limit).
- Supports training scenarios and operator onboarding for WhiteBIT trading workflows.
- Validates parameters against WhiteBIT docs via MCP.
- Prepares documented API requests and execution checklists.
- Supports ClawHub lifecycle actions (`search`, `install`, `update`, `publish`, `sync`).

## Training Uses
- Learn WhiteBIT spot trading terminology, order flow, and request structure.
- Practice market and limit order scenarios without claiming live execution.
- Build onboarding walkthroughs for authentication, signing, request validation, and post-trade checks.
- Review example responses, user-provided fills, and error payloads for training or troubleshooting.
- Rehearse bankroll controls, order sizing, and spot `BUY`/`SELL` behavior before using an external executor.

## Prerequisites
- OpenClaw installed.
- `clawhub` CLI installed.
- `whitebit-docs` MCP access in your OpenClaw environment.
- A separate execution system only if you want to place live orders.

## What To Consider Before Installing
1. Confirm credential model before live use.
- Decide where trading credentials live for your external executor.
- This skill does not require runtime trading credentials by itself.
- Never upload credentials when publishing to ClawHub.

2. Confirm runtime dependencies are available.
- Ensure `clawhub` CLI is installed and authenticated for install/publish/update flows.
- Ensure `whitebit-docs` is present for documentation lookup.
- Do not assume this skill can execute trades unless you have a separate execution path.
- For training-only use, `whitebit-docs` is sufficient.

3. Restrict autonomous execution.
- Start with dry-run or sandbox-capable systems whenever possible.
- Require explicit human confirmation before any live trade in your external executor.

4. Review publish contents.
- Inspect local files before `clawhub publish` or `clawhub sync`.
- Exclude secrets and local artifacts (`.env`, keys, logs, build outputs).

5. Verify manifest/dependency declarations.
- This skill declares runtime requirements in `SKILL.md` frontmatter:
- `requires.bins`: `clawhub`
- If your deployment model adds a real execution connector, update metadata before advertising live execution.

## Install

### Option 1: From ClawHub
```bash
clawhub install whitebit
```

Then start a new OpenClaw session so the skill is loaded.

To pull latest updates later:

```bash
clawhub update whitebit
```

### Option 2: From GitHub
1. Clone this repository.
2. Put this folder in your OpenClaw skills directory as:
`<workspace>/skills/clawhub-whitebit-trading`
3. Start a new OpenClaw session.

## API Keys Setup

This skill does not require runtime WhiteBIT API credentials on its own.
If you use a separate executor, provide credentials there according to that system's configuration.

Example environment variables for an external executor:

```bash
export WHITEBIT_API_KEY="your_public_api_key"
export WHITEBIT_API_SECRET="your_secret_api_key"
```

If your external MCP server uses config-based env injection, use the same variables in that server config:

```json
{
  "mcpServers": {
    "external-whitebit-executor": {
      "env": {
        "WHITEBIT_API_KEY": "your_public_api_key",
        "WHITEBIT_API_SECRET": "your_secret_api_key"
      }
    }
  }
}
```

Use the exact variable names expected by your external execution system.

## Quick Verification
1. In OpenClaw, run: `What MCP tools do you have available?`
2. Confirm `whitebit-docs` is available.
3. For training, ask the skill for a sample WhiteBIT order walkthrough.
4. Verify separately that your external execution system exists before attempting any live trade.

## Security Notes
- Never commit API keys or secrets to Git.
- Use least-privilege API permissions.
- Rotate keys immediately if exposed.
