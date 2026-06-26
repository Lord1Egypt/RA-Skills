# Dev Update: Smart Install + Platform Compatibility

**Date:** 2026-03-10 22:40 PST
**Author:** Claude Code (cc-mini)
**Version:** v1.7.8 (pending)
**Branches:** cc-mini/smart-install, cc-mini/platform-compat-v2

## Smart Install (wip-install)

Parker's feedback: "I want to make sure we're not going to replace stuff unless we need to. It should be smart enough to know I have this extension installed, and it's the same one."

The Universal Installer was doing blind `rm -rf` and re-copy on every run. Now it checks versions first:

- **Extensions (LDM + OpenClaw):** Reads `package.json` version from the installed extension. If it matches the source version, skip. If different, upgrade. If missing, fresh install. Dry-run shows "would upgrade v1.2.3 -> v1.2.4" vs "would deploy v1.2.4" vs "already at v1.2.4".
- **CLI:** Checks `npm list -g` for the installed version. Same version = skip.
- **MCP:** Checks if already registered at the same server path. Same path = skip.
- **CC Hooks:** Already had duplicate detection (unchanged).

No more destroying things that don't need updating.

## Platform Compatibility (SKILL.md)

Parker's feedback after testing with Grok: "Grok said 'I'll run wip-install' but it literally cannot. It's hallucinating capabilities."

First version listed platforms as "first-class / MCP-compatible / not compatible." Parker corrected: "We don't need to say 'not compatible' because Claude iOS can install stuff now. We just need to be clear about what the tool needs."

Rewrote to capability requirements:

| Interface | Requires |
|-----------|----------|
| CLI | Shell access |
| MCP Server | MCP client support |
| CC Hook | Claude Code CLI with hooks |
| OpenClaw Plugin | OpenClaw runtime |
| Skill | Ability to read this file |
| Module | Node.js import |

Key instruction to agents: "Check which capabilities you have and match them to the table. Do not claim you can run commands you cannot execute."

This is future-proof. When a platform adds MCP or shell access, the SKILL.md doesn't need updating. The agent assesses itself.

## Cross-Platform Testing Results

Three AIs read the same SKILL.md onboarding prompt:

- **Claude Code (another instance):** Read it, explained all tools correctly, offered dry-run first. Responded with "HOLY SHIT!!!" (impressed by the tooling).
- **Lesa (OpenClaw, Claude Opus 4.6):** Perfect breakdown. Every tool categorized correctly. Called out the auto-detect dev updates feature specifically. Offered dry-run first.
- **Grok (xAI):** Initially tried to roleplay as Lesa/Claude Code (read the attribution line and adopted the persona). When corrected, gave accurate breakdown. But claimed it would run `wip-install` when it cannot. This exposed the need for the Platform Compatibility section.

The SKILL.md is working. Three different AIs, three different platforms, all understood the toolbox correctly from one file.
