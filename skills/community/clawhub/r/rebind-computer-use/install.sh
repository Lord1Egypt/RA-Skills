#!/usr/bin/env bash
# rebind-computer-use — fallback installer for users not installing via ClawHub
# (air-gapped, private builds, pre-registry testing). Idempotent; fails loudly.
#
# Primary path is:  openclaw skills install @usinput/rebind-computer-use
set -euo pipefail

die() { echo "ERROR: $*" >&2; exit 1; }

cd "$(dirname "$0")"

# 1. preflight
command -v bun >/dev/null || die "bun is required: https://bun.sh"
command -v openclaw >/dev/null || die "OpenClaw not found: https://openclaw.ai"

# 2. copy the skill (this script lives alongside SKILL.md)
SKILLS="${OPENCLAW_HOME:-$HOME/.openclaw}/skills"
mkdir -p "$SKILLS/rebind-computer-use"
cp SKILL.md "$SKILLS/rebind-computer-use/"
echo "skill installed to $SKILLS/rebind-computer-use"

# 3. register the MCP server in OpenClaw config (merge, don't clobber).
# @rebind.gg/mcp-server ships via npm; bunx fetches it on demand.
# --no-probe: the default probe spawns the server and fails if the relay isn't
# running yet; the selftest below is the real verifier.
if openclaw mcp add rebind --no-probe \
  --command bunx --arg @rebind.gg/mcp-server \
  --env REBIND_URL=ws://127.0.0.1:19561; then
  echo "MCP server registered as 'rebind'"
else
  echo "WARNING: 'openclaw mcp add' failed — add the snippet in mcp.example.json to your OpenClaw config (~/.openclaw/openclaw.json) manually." >&2
fi

# 4. satisfy the skill's env gate. OpenClaw checks this against its own config,
# NOT the MCP server's env block — without it the skill stays "needs setup"
# and is invisible to the model.
openclaw config set skills.entries.rebind-computer-use.env.REBIND_URL ws://127.0.0.1:19561

# 5. verify the relay is reachable
bunx @rebind.gg/mcp-server --selftest || die "Rebind relay not reachable on ws://127.0.0.1:19561.
Start Rebind and load the Remote Access script, then re-run this installer
(or just: bunx @rebind.gg/mcp-server --selftest)."

echo
echo "Installed. IMPORTANT: start a NEW OpenClaw session — skills are"
echo "snapshotted at session start, so the current session cannot see this one."
echo "Then text your agent: \"take a screenshot and describe my screen\"."
