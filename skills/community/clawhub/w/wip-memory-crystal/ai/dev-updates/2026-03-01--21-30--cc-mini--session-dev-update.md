# Dev Update: 2026-03-01 ~21:30 PST

**Author:** CC-Mini
**Branch:** cc-mini/cloud-mcp (memory-crystal-private)
**Also touched:** wip-dev-tools-private (main)

---

## What Happened This Session

### wip-dev-tools: Built and shipped wip-repo-permissions-hook

Built a new tool that blocks repos from going public without a -private counterpart. Four surfaces: CLI, Claude Code PreToolUse hook, OpenClaw plugin, cron audit.

- Built: core.mjs, cli.js, guard.mjs, openclaw.plugin.json, package.json, README.md, SKILL.md
- Added visibility-audit.sh to ldm-jobs
- Deployed to ~/.ldm/extensions/wip-repo-permissions-hook
- Added PreToolUse:Bash hook to ~/.claude/settings.json
- Fixed cli.js switch fall-through bug
- PR, merge, tag v1.1.0, GitHub release, deploy-public.sh to wipcomputer/wip-dev-tools
- Updated main README with new tool section, source table, cron schedule
- v1.1.1: README updates
- v1.1.2: CHANGELOG + SKILL.md catch-up
- v1.1.3: Full repo audit found 5 bugs, fixed all:
  1. pre-pull.sh/pre-push.sh: wrong npx package name (@wipcomputer/license-hook -> @wipcomputer/wip-license-hook)
  2. wip-release package.json: test script referenced cli.mjs instead of cli.js
  3. wip-release CHANGELOG.md: extra blank lines
  4. DEV-GUIDE.md: missing visibility-audit.sh in .app structure diagram
  5. Removed duplicate skill/SKILL.md subfolder from wip-license-hook

### wip-dev-tools: Flipped 5 repos to private

Found 7 repos went public on Feb 28 via batch automation. Flipped 5 to private:
- wip-bridge, wip-mirror-test, wip-weekly-tuning, wip-private-mode, wip-root-key

wip-xai-x and wip-dev-tools already had -private counterparts, kept public.

### wip-dev-tools: Updated DEV-GUIDE with hard rule

Added to both DEV-GUIDE.md (public) and DEV-GUIDE-private.md:
"Never make a repo public unless it has a -private counterpart."

### Memory Crystal: README restructure

- Renamed Local to **Local Recall**
- Added **Import** section (Total Recall)
- Added **Memory Consolidation** section (Dream Weaver Protocol)
- Added second bullet to **Relay**: uses Cloudflare infrastructure, currently free for individual use
- All on cc-mini/cloud-mcp branch, uncommitted

### Memory Crystal: Interface-First Checkout decision

Major product decision captured in `ai/notes/2026-03-01--cc-mini--interface-first-checkout.md`:

- No website checkout. No consent page. No signup form.
- The agent is the entire interface for discovery, signup, payment, and installation.
- The nudge: after N memory saves, agent suggests Relay. User opts in or ignores.
- Signup: agent collects name + email, sends to API. Parker manually approves (for now).
- Payment: wip-agent-pay opens Stripe with Apple Pay. Not crypto. Regular money.
- Prior art: Morning Stew ($0.10/issue via x402) and Pawr ($19 create via x402) already do agent-first commerce.
- The OAuth consent page in worker-mcp.ts is wrong for local users. That's only for ChatGPT/Claude MCP client connections.
- The website exists for reading/docs, but the "install button" is a prompt you paste into your agent.

### Memory Crystal: What's still blocked

- **R2 activation on Cloudflare**: Parker needs to enable R2 on the dashboard (1 min). Blocks deploy.
- **cc-mini/cloud-mcp branch**: Has uncommitted work (README, deploy-cloud.sh fix, wrangler-mcp.toml, dev updates, plans). Needs commit and PR.

---

## Next Session Pickup

1. Commit all uncommitted work on cc-mini/cloud-mcp
2. PR the branch for Parker to review
3. Parker enables R2 on Cloudflare
4. Run deploy-cloud.sh
5. Test end-to-end: OAuth flow, memory tools, relay
6. Rework the consent page / auth flow based on interface-first checkout decision (agent-driven signup, manual approval gate, no browser form for local users)
7. wip-release after deploy is verified
