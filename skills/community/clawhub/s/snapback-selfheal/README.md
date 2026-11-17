# Snapback — OpenClaw Skill (ClawHub-submittable)

The Snapback agent skill: point any MCP-capable agent at Snapback to diagnose failed runs, catch loops/budget
breaches mid-run, and (optionally) pay per call. This folder is ready to publish to ClawHub (the OpenClaw
skill registry).

## Files
- `SKILL.md` — the skill (YAML frontmatter with name/version/description + metadata.openclaw env + mcp block,
  all 14 tools, worked examples, security section). No scripts, no binaries — safe by construction.
- `LICENSE` — MIT.

## Use it locally (any user)
1. Set `SNAPBACK_TOKEN` in the environment (a `vdk_` token from https://snapback.sh) — optional; most tools
   are free and need no token.
2. Register the MCP server:
   ```
   openclaw mcp add snapback --transport streamable-http --url https://api.snapback.sh/mcp \
     --header "Authorization: Bearer $SNAPBACK_TOKEN"
   openclaw mcp reload
   openclaw mcp probe snapback
   ```
   OR drop `SKILL.md` into `~/.openclaw/skills/snapback/SKILL.md` so it shows in `available_skills`.

### Installing the skill so your agent can see it
`clawhub install snapback-selfheal` installs **relative to the current directory** (into `./skills/`), so run
it from your OpenClaw **workspace root** — not a scratch/temp dir — or the skill lands where your agent can't
find it. To be certain it's in the agent's skills path:
```
cd ~/.openclaw            # or your OpenClaw workspace root
clawhub install snapback-selfheal
```
Then confirm it appears: the skill should show in `available_skills` after a reload. If it doesn't, it went to
the wrong directory — copy `SKILL.md` + `claw.json` into `~/.openclaw/skills/snapback-selfheal/` directly.

## Publish to ClawHub (operator, one-time)
ClawHub requires: valid YAML frontmatter (name/version/description), a unique name, at least one usage
example, and it runs an automated security scan (declared-vs-actual behavior). This skill meets all of them.
```
openclaw clawhub login                                   # needs a GitHub account old enough to pass the gate
openclaw clawhub validate ./integrations/openclaw-skill/SKILL.md   # dry-check before publishing
openclaw clawhub publish  ./integrations/openclaw-skill            # publish the folder (SKILL.md + LICENSE)
# later, publish an update with a bumped version + changelog:
openclaw clawhub publish  ./integrations/openclaw-skill --update
```
- Bump `version:` in the frontmatter for each release; tag `latest`.
- After publishing, `openclaw clawhub security-report snapback` shows the scan state.

## Distribution notes
- The SKILL.md is the OpenClaw-flavored wrapper; the MCP endpoint itself is universal, so the same skill works
  for Hermes / Copilot / Cursor / any MCP client (they can point at the endpoint directly, or reuse this file).
- ClawHub uses embeddings/vector search, so the rich `description` + trigger phrases matter for discovery.
- Keep it in sync: when tools change on the server, bump the version + re-publish.
