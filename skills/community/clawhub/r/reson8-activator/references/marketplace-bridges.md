# Marketplace Bridges — Platform-Specific Packaging

Each marketplace has its own format for distributing capabilities.
The activation map stays the same — only the packaging changes.

## 1. Anthropic / Claude (Cowork .plugin)

**Format:** .plugin file (zip with .claude-plugin/plugin.json manifest)
**How to ship:**
1. Use create-cowork-plugin skill to scaffold
2. Package skills as SKILL.md + references
3. Package commands as commands/*.md
4. Zip and rename to .plugin
5. Distribute via Cowork marketplace or direct install

**What ships:** Skills, commands, agents, hooks, MCP server configs
**Auth:** None needed for plugin install
**Status:** ACTIVE — reson8-activator is itself packaged this way

## 2. Google / Gemini Extensions

**Format:** Gemini Extension manifest + handler code
**How to ship:**
1. Export coherence-mcp tool definitions as OpenAPI spec
2. Create Gemini Extension config referencing the spec
3. Register via Gemini-CLI or Google AI Studio
4. Reference GEMINI-INIT.md for context injection

**What ships:** Tool definitions, context documents
**Auth:** Google OAuth
**Status:** READY — awaiting Google marketplace launch

## 3. xAI / Grok Actions

**Format:** Grok Action definition + X API integration
**How to ship:**
1. Use grok connector tools (grok_generate, grok_check_coherence)
2. Define actions via GROK-INIT.md context
3. Wire X API for content publishing
4. ATOM-AUTH for creator monetization flow

**What ships:** Actions, real-time tools, X API bridge
**Auth:** X OAuth 2.0 + Grok API key
**Status:** ACTIVE — grok connector in coherence-mcp

## 4. OpenAI / ChatGPT Plugins

**Format:** OpenAPI spec + ai-plugin.json manifest
**How to ship:**
1. Generate OpenAPI 3.0 spec from coherence-mcp tool definitions
2. Create ai-plugin.json with name, description, auth
3. Host the API (Cloudflare Workers ideal)
4. Submit to ChatGPT plugin store

**What ships:** API endpoints mirroring MCP tools
**Auth:** OAuth or API key
**Status:** PLANNED — needs hosted endpoint

## 5. npm Registry

**Format:** Node.js package (@toolate28/coherence-mcp)
**How to ship:**
1. Already published: npm install @toolate28/coherence-mcp
2. Version 0.3.1 live on registry
3. Update: bump version in package.json, npm publish

**What ships:** Full MCP server, 49 tools, test suite
**Auth:** npm token
**Status:** LIVE — v0.3.0 + v0.3.1

## 6. PyPI

**Format:** Python package (spiralsafe)
**How to ship:**
1. Create Python wrapper around WAVE + ATOM core
2. Use pyproject.toml with build system
3. python -m build && twine upload dist/*

**What ships:** WAVE analysis, ATOM trail, Fibonacci weighting
**Auth:** PyPI API token
**Status:** PLANNED

## 7. Cargo (crates.io)

**Format:** Rust crate (reson8-tui)
**How to ship:**
1. Create Cargo workspace in Reson8-Labs/crates/
2. Implement: crates/core (WAVE+ATOM), crates/tui (Ratatui dashboard), crates/websocket-bridge
3. cargo publish

**What ships:** TUI dashboard, WAVE scoring, POP websocket bridge
**Auth:** Cargo API token
**Status:** PLANNED — Grok has main.rs draft, needs Cargo workspace scaffold

## 8. Obsidian Community Plugin

**Format:** TypeScript Obsidian plugin with manifest.json
**How to ship:**
1. Write TypeScript plugin connecting to ws://127.0.0.1:8088
2. Expose GET_PLUGIN_MANIFEST handler
3. Handle EXECUTE_PIPELINE commands
4. Submit to Obsidian community plugins

**What ships:** POP bridge, pipeline executor, coherence reports
**Auth:** None (local websocket)
**Status:** PLANNED — POP protocol specified

## 9. Minecraft (Bukkit/Paper Plugin)

**Format:** Java plugin (.jar) for Paper/Spigot
**How to ship:**
1. ClaudeNPC.jar already built with quantum circuit generator
2. Extends with: RCON bridge, conservation verifier, redstone builder
3. Distribute via Modrinth or direct

**What ships:** NPC AI, quantum circuits, conservation verification
**Auth:** RCON password
**Status:** PARTIAL — ClaudeNPC exists, needs quantum-redstone integration

## 10. rentahuman.io

**Format:** Agent profile + capability manifest
**How to ship:**
1. Create agent profile with capability description
2. Define input/output contracts
3. Wire to coherence-mcp API endpoint (hosted)
4. Set pricing and availability

**What ships:** Agent-as-a-service: WAVE analysis, content generation, research
**Auth:** Platform auth
**Status:** PLANNED — needs hosted endpoint

## 11. ClawhubAI

**Format:** Skill listing + activation map
**How to ship:**
1. Export activation map as structured manifest
2. Create listing with skill descriptions and triggers
3. Include composition patterns as capability documentation

**What ships:** Skill definitions, activation patterns
**Auth:** Platform auth
**Status:** PLANNED

## 12. GitMCP

**Format:** gitmcp.io URL (zero-config)
**How to ship:**
1. Replace github.com with gitmcp.io in any repo URL
2. Instant MCP endpoint — no install, no config
3. Works for: coherence-mcp, Reson8-Labs, hope-ai-npc-suite

**What ships:** Full repo as MCP-queryable surface
**Auth:** None
**Status:** ACTIVE — instant for all public repos

Example URLs:
- gitmcp.io/toolate28/coherence-mcp
- gitmcp.io/toolate28/Reson8-Labs
- gitmcp.io/toolate28/hope-ai-npc-suite
