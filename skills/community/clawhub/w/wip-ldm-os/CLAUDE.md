# LDM OS (wip-ldm-os-private)

The installer, runtime, and hosted infrastructure for Kaleidoscope by WIP Computer, Inc.

## What this repo does

- **LDM OS installer** (`bin/ldm.js`): `ldm init`, `ldm install`, `ldm doctor`, `ldm status`. Scaffolds `~/.ldm/`, deploys extensions, wires up agents.
- **Kaleidoscope demo** (`src/hosted-mcp/demo/`): The live product at wip.computer/demo. Passkey auth, agent permission, wallet, image generation. This is the product, not a mockup.
- **Hosted MCP server** (`src/hosted-mcp/server.mjs`): OAuth 2.0 + PKCE, WebAuthn passkeys, agent auth flow, wallet tracking, Grok Imagine proxy. Lives on the VPS at wip.computer.
- **Bridge** (`src/bridge/`): Agent-to-agent communication. Local file inbox + hosted MCP.
- **Hooks** (`src/hooks/`): Claude Code and OpenClaw lifecycle hooks.
- **Shared templates** (`shared/`): CLAUDE.md templates, rules, docs deployed by `ldm install`.

## Product context

**Kaleidoscope** is the product. The consumer-facing harness. "Every AI. One experience."

**Lēsa** is the platform agent. Ours. She greets users, sets up their agents, coordinates everything. She is not the customer's agent. She makes agents for customers.

**Six products inside Kaleidoscope:**
1. Memory Crystal ... your AI remembers
2. Agent Pay ... your AI pays
3. Directory ... identity, passkeys, @handles
4. Bridge ... your AIs talk to each other
5. Code ... your AI builds
6. Crystal SDK ... add memory to your app

**LDM OS** is the kernel. Invisible. "Powered by LDM OS."

## Key files

```
bin/ldm.js              CLI entry point
lib/                    installer logic, deploy, config
src/hosted-mcp/
  server.mjs            MCP server (OAuth, WebAuthn, wallet, imagine)
  demo/
    index.html          Kaleidoscope demo (login + chat, ~1300 lines)
    agent.html          Agent access page
    agent.txt           Agent auth instructions (robots.txt for agents)
    footer.js           Shared footer template
    tos.html            Terms of service
    privacy.html        Privacy policy
    sprites.png         Kaleidoscope icon sprite sheet (8x3 grid)
src/bridge/             Agent-to-agent communication
src/hooks/              Lifecycle hooks
shared/                 Templates deployed by ldm install
SKILL.md                Agent skill file for LDM OS
```

## Build and test

```bash
# No build step. Plain JS (ESM).
node bin/ldm.js --help          # CLI
node bin/ldm.js install --dry-run
node bin/ldm.js doctor

# Deploy demo to VPS:
scp src/hosted-mcp/demo/* wip-vps:/var/www/wip.computer/app/mcp-server/demo/
scp src/hosted-mcp/server.mjs wip-vps:/var/www/wip.computer/app/mcp-server/
ssh wip-vps 'pm2 restart mcp-server'
```

## Conventions

- **Never commit to main.** Branch + PR. Branch prefix: `cc-mini/`, `oc-lesa-mini/`, `cc-air/`.
- **Never squash merge.** Every commit has co-authors.
- **Worktrees** for isolated work: `.worktrees/<repo>--<branch>/`
- **Release pipeline:** merge -> `wip-release patch` -> `deploy-public.sh`
- **Footer format:** WIP Computer, Inc. / Learning Dreaming Machines / Are you an AI Agent? | Privacy Policy | Terms of Use / Made in California.
- **Writing style:** No em dashes. Use periods, colons, semicolons, or ellipsis (...). PST timezone.

## Full system context

For the complete project context, boot sequence, memory tools, and agent instructions:
- Read `~/wipcomputerinc/CLAUDE.md`
- Read `~/wipcomputerinc/library/documentation/` for conventions
- Use `crystal_search` for cross-repo context

## Architecture docs

- `ai/product/product-ideas/vision-quest-01/architecture-spec.md` ... full product architecture
- `ai/product/product-ideas/vision-quest-01/vision-quest-02-agent-txt-era.md` ... agent.txt, four clients, MVVM
- `ai/product/product-ideas/vision-quest-01/kaleidoscope-executive-brief.md` ... one-page brief
- `ai/product/plans-prds/current/wip-code/` ... CLAUDE.md cascade plan, CWD bug journal
