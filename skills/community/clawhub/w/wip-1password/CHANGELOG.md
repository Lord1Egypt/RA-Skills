# Changelog



## 0.2.2 (2026-03-12)

## v0.2.2: AI-Native Homepage, MCP Fix, Plan Requirements

Ran wip-1password through the WIP DevOps toolbox and rebuilt the homepage from the ground up. The README is now an AI-compatible product page. All technical documentation lives in TECHNICAL.md. The MCP server that was crashing since v0.2.0 is fixed. 1Password plan requirements updated after direct conversations with 1Password support.

---

### README rebuilt as a product page

**The problem it solved:** The old README was 400+ lines of technical documentation. Quick Start, Agent Tools API, Config Resolution, CLI Commands, Write Support, Security, Troubleshooting, Developer Guide... all in one file. No human would read it. No agent could parse it efficiently.

**What changed:** The README is now a product page. One description, a "Teach Your AI" prompt block (Karpathy pattern), four human-readable bullets, and links to docs. That's it.

The "Teach Your AI" block is the key feature. You paste it into Claude Code, ChatGPT, or any MCP-compatible agent. The agent reads the SKILL.md, explains what the tools do, dry-runs the install, and waits for your go-ahead before writing anything to disk. The README talks to AI now.

All technical content moved to TECHNICAL.md: Quick Start (6 steps), Agent Tools API (3 tools with parameter tables), Config Secret Resolution (with the `memorySearch.remote` gotcha), CLI Commands, Write Support, Configuration, How It Works, Security, Troubleshooting, and a full Developer Guide with three integration options and patterns for common scenarios.

New description: "Give your AI secure access to 1Password. Never copy-paste an API key into a chat window again."

**What changed:**
- `README.md` ... gutted from 400+ lines to ~75. Product page only. Badges, description, Teach Your AI block, What It Does (4 bullets), Documentation links, License.
- `TECHNICAL.md` ... expanded with all content from README plus new Developer Guide section (3 integration options, common patterns, key rules, example projects table).

---

### MCP server fixed

**The problem it solved:** `mcp-server.mjs` crashed on startup with "Schema is missing a method literal." The MCP server shipped in v0.2.0 but never actually worked. Every Claude Code user who tried to connect op-secrets hit this error.

**Root cause:** `setRequestHandler` was called with raw strings (`"tools/list"`, `"tools/call"`) instead of SDK schema objects. The MCP SDK validates the first argument against its type system and rejects strings.

**The fix:**
```javascript
// Before (broken)
server.setRequestHandler("tools/list", async () => ({...}));
server.setRequestHandler("tools/call", async (request) => ({...}));

// After (working)
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";
server.setRequestHandler(ListToolsRequestSchema, async () => ({...}));
server.setRequestHandler(CallToolRequestSchema, async (request) => ({...}));
```

op-secrets MCP server now starts clean and connects to Claude Code.

**What changed:**
- `mcp-server.mjs` ... import `ListToolsRequestSchema` and `CallToolRequestSchema` from `@modelcontextprotocol/sdk/types.js`, replace string handlers with schema objects.

---

### 1Password plan requirements updated

Parker went back and forth with 1Password directly. The original docs said "Teams or Business" for service accounts. That was wrong.

**What we confirmed:**
- Service accounts work on **all plans**: Individual, Family, Teams, Business.
- Headless operation (no desktop app) confirmed on Teams and Business.
- Lower-tier plans may require the desktop app for initial setup.

**What changed:**
- `TECHNICAL.md` ... prerequisites section updated with correct plan requirements.
- `SKILL.md` ... compatibility line updated. Description changed from "OpenClaw plugin" to "AI plugin (Claude Code, OpenClaw)".

---

### Feature priority reordered

Agent tools (read/write secrets) is the #1 value of this tool. It was listed after config resolution. Reordered in both README and TECHNICAL.md:

1. Agent tools (read/write secrets on demand)
2. MCP server for Claude Code
3. Config resolution (`op://` refs at startup)
4. CLI diagnostics

---

### Files Changed

```
 README.md               | 389 ++----------------------------------------------
 SKILL.md                |   8 +-
 TECHNICAL.md            | 116 +++++++++++----
 mcp-server.mjs          |   5 +-
 5 files changed, 121 insertions(+), 412 deletions(-)
```

### Install

```bash
npm install -g @wipcomputer/wip-1password@0.2.2
```

Or update your local clone:
```bash
git pull origin main
```

---

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).

## 0.2.1 (2026-03-12)

Restore full README with all documentation, fix broken Teach URL

## 0.2.0 (2026-03-12)

# v0.2.0 ... Full Treatment

The 1Password plugin gets the full WIP treatment: standard SKILL.md, license compliance, reformatted README, and a new MCP server for Claude Code.

## What's New

### MCP Server for Claude Code (#10)
New `mcp-server.mjs` provides 1Password access directly from Claude Code via MCP. Uses the `op` CLI with service account token for headless access. Three tools: `op_read_secret`, `op_list_items`, `op_test`.

Register with:
```bash
claude mcp add --scope user wip-1password -- node /path/to/mcp-server.mjs
```

### SKILL.md (agentskills.io spec) (#2)
Root SKILL.md with proper frontmatter: lowercase-hyphen name, metadata block with display-name/version/homepage/author, openclaw install instructions, capability list.

### License Compliance (#4)
Dual MIT+AGPL via `wip-license-guard --from-standard`. CLA.md generated. Attribution in README.

### README Reformatted (#3)
README reformatted to WIP Computer standard via `wip-readme-format`. Technical content (quick start, agent tools, config resolution, developer guide) split to TECHNICAL.md.

## Interfaces

| Interface | File | Status |
|-----------|------|--------|
| Module | `dist/index.js` | Existing |
| OpenClaw Plugin | `openclaw.plugin.json` | Existing |
| Skill | `skills/op-secrets/SKILL.md` | Existing |
| MCP Server | `mcp-server.mjs` | **New** |
| Root Skill | `SKILL.md` | **New** |

## Closes
#2, #3, #4, #7, #10

