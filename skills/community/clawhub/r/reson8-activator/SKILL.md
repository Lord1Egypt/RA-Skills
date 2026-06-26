---
name: reson8-activate
description: >
  The meta-skill that knows its own activation surface. Use this skill whenever the user wants to
  "activate" a capability, asks "what can you do", wants to chain multiple skills together,
  needs help finding the right tool for a task, asks about available integrations or connectors,
  wants to publish to a marketplace, or says "activate", "inventory", "compose", "what tools",
  "what skills", "what can we use", "show me everything", or "tapestry". Also triggers when
  another agent (Grok, Gemini) needs to understand what capabilities exist and how to invoke them.
  This is the Tapestry of Skills — the self-aware orchestration layer.
version: 1.0.0
---

# Reson8 Activator — The Tapestry of Skills

This skill is the orchestration brain. It knows every tool, skill, MCP server, API, marketplace,
and external repo in the Reson8-Labs ecosystem. Its job is to take an intent and activate the
right combination of capabilities to fulfill it.

## Core Capabilities

1. **Inventory** — enumerate every activatable capability, filtered by domain or type
2. **Route** — given a natural language intent, select the optimal skill chain
3. **Compose** — wire skills together in sequence, with WAVE scoring at each transition
4. **Teach** — help other agents (Grok, Gemini, external) understand what's available
5. **Extend** — use skill-creator + create-cowork-plugin to build new capabilities on demand

## How Activation Works

When the user expresses an intent:

1. Parse the intent into capability requirements (what domains? what output format? what integrations?)
2. Search the activation map (`references/activation-map.md`) for matching capabilities
3. Check if the intent maps to a known composition pattern (`references/composition-patterns.md`)
4. If a pattern exists, propose it. If not, construct a novel chain from available primitives.
5. Present the proposed chain to the user for confirmation
6. Execute each step, applying WAVE coherence scoring at transitions
7. Log the entire execution as an ATOM trail entry

## The Activation Surface

Read `references/activation-map.md` for the complete inventory. Summary of what's available:

**MCP Tools (54 total):**
- coherence-mcp: 49 tools across 10 categories (WAVE, ATOM, Fibonacci, Vortex, Minecraft, Session, Bohmian, Content, SpiralSafe, Utility)
- Reson8-Labs MCP Server: 5 core tools (analyze_wave, track_atom, validate_gate, chaos_score, generate_atom_tag)

**Connected MCP Servers (13+):**
ChEMBL, bioRxiv/medRxiv, Open Targets, ClinicalTrials.gov, Cloudflare, Crypto Exchange, Mermaid Diagrams, Vercel, Google Drive, Google Calendar, Claude in Chrome, MCP Registry, Domain/Hosting

**Skills (71 total):**
11 core + 60 plugin across 10 domains: bio-research, data, enterprise-search, finance, legal, marketing, product-management, productivity, sales, cowork-plugin-management

**External Tool Repos (7):**
GitMCP, LightRAG, AutoFigure, MoLing-Minecraft, AI-Researcher, Claude Scientific Writer, Agent Squad

**Marketplace Surfaces (12):**
Anthropic/Claude, Google/Gemini, xAI/Grok, OpenAI/ChatGPT, npm, PyPI, Cargo, Obsidian, Minecraft, rentahuman.io, ClawhubAI, GitMCP

## Routing Logic

When matching intent to capabilities, prioritize:

1. **Exact match** — intent directly names a skill or tool (e.g., "run WAVE check" → wave_coherence_check)
2. **Domain match** — intent falls within a known domain (e.g., "draft a contract" → legal:contract-review)
3. **Composition match** — intent requires multiple steps that map to a known pattern (e.g., "research and publish" → Research→Publish pipeline)
4. **Capability match** — intent describes a capability type (e.g., "make a chart" → data:data-visualization)
5. **Discovery** — if no match, search MCP registry for new connectors, or suggest building a new skill

## WAVE Scoring at Transitions

Every skill chain transition gets WAVE scored. The coherence check ensures that output from step N
is coherent input for step N+1. If coherence drops below 0.85 at any transition:

- Pause the chain
- Report the coherence gap to the user
- Suggest: retry with modified parameters, skip the step, or abort

This is the conservation law in action — coherence must be preserved across the full pipeline.

## Teaching Other Agents

When another agent (or the user on behalf of another agent) asks what's available:

1. Read `references/activation-map.md` for the full inventory
2. Format the response for the target agent's expected input format:
   - For **Grok**: Focus on real-time tools, X API, Rust TUI integration, hardware monitoring
   - For **Gemini**: Focus on multimodal tools, Google integrations, RAG, scientific pipelines
   - For **Claude**: Full surface — everything is native
3. Include the INIT document reference (GROK-INIT.md, GEMINI-INIT.md, CLAUDE-INIT.md)
4. Include the CHECKPOINT document for full state awareness

## Extending the Surface

When a user needs a capability that doesn't exist:

1. Check if a close match exists and can be adapted
2. If not, propose building it:
   - For a new skill → invoke skill-creator
   - For a new plugin → invoke create-cowork-plugin
   - For a new MCP server → invoke mcp-builder
   - For a new connector → search MCP registry first
3. After building, update the activation map

## Marketplace Publishing

Read `references/marketplace-bridges.md` for platform-specific packaging instructions.
Each marketplace has its own format — the activation map stays the same, only the packaging changes.

## Conservation Law

Every activation must respect: **ALPHA + OMEGA = 15**

This means: the sum of intention (alpha) and outcome (omega) is conserved.
What goes in must equal what comes out. No information is created or destroyed —
only transformed across substrates.

The WAVE score measures this conservation at each transition.
The ATOM trail records the full transformation history.
