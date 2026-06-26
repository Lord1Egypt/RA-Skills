# Composition Patterns — Skill Chains That Work

These are tested, validated skill chains. When an intent matches one of these patterns,
propose it as the activation plan. Each chain includes WAVE scoring at every transition.

## 1. Research → Publish Pipeline

**Triggers:** "research and publish", "write a paper", "investigate and report", "literature review"

```
enterprise-search:search-strategy
  → data:data-exploration
  → data:data-visualization
  → [AutoFigure — if publication-ready figures needed]
  → [AI-Researcher — if full paper generation needed]
  → docx (or pdf)
  → [Vercel:deploy_to_vercel — if web publishing needed]
```

**WAVE checkpoints:** After search (coherence of sources), after visualization (data integrity), after writing (narrative coherence)

## 2. Competitive Intelligence Pipeline

**Triggers:** "competitor analysis", "battlecard", "market landscape", "how do we compare"

```
sales:account-research
  → sales:competitive-intelligence
  → marketing:competitive-analysis
  → data:interactive-dashboard-builder
  → pptx (or create-an-asset)
```

**WAVE checkpoints:** After research (source diversity), after analysis (claim validation), after presentation (narrative flow)

## 3. Institutional Formation Pipeline

**Triggers:** "set up the company", "legal formation", "compliance review", "board prep"

```
legal:compliance
  → legal:contract-review
  → finance:financial-statements
  → legal:meeting-briefing
  → internal-comms
  → docx
```

**WAVE checkpoints:** After compliance (regulatory coverage), after financials (number validation), after comms (audience alignment)

## 4. Paper Generation Pipeline

**Triggers:** "write a scientific paper", "generate figures for paper", "prepare manuscript"

```
bio-research:scientific-problem-selection
  → [LightRAG — knowledge graph query]
  → [AI-Researcher — algorithm design + implementation]
  → [AutoFigure — SVG generation with quality scoring]
  → data:data-visualization (supplementary figures)
  → pdf
```

**WAVE checkpoints:** After RAG (source relevance), after AI-Researcher (methodology coherence), after figures (visual-text alignment)

## 5. Minecraft Conservation Pipeline

**Triggers:** "place circuit", "verify conservation in-world", "quantum redstone"

```
coherence-mcp:mc_place_circuit
  → coherence-mcp:mc_verify_conservation
  → coherence-mcp:wave_coherence_check
  → coherence-mcp:atom_track
```

**WAVE checkpoints:** After placement (block integrity), after verification (ALPHA + OMEGA = 15)

## 6. Edge Deployment Pipeline

**Triggers:** "deploy to edge", "Cloudflare Workers", "set up infrastructure", "eliminate session amnesia"

```
Cloudflare:d1_database_create (session persistence)
  → Cloudflare:kv_namespace_create (WAVE score cache)
  → Cloudflare:r2_bucket_create (artifact storage)
  → [code: write Worker script]
  → Vercel:deploy_to_vercel (frontend)
  → coherence-mcp:wave_validate (deployment coherence)
```

**WAVE checkpoints:** After each infrastructure step (provisioning validation), after deployment (end-to-end coherence)

## 7. Daily Operations Pipeline

**Triggers:** "start my day", "morning briefing", "what's on my plate", "daily update"

```
productivity:memory-management (load context)
  → sales:daily-briefing (prioritized brief)
  → Google Calendar:list_gcal_events (schedule)
  → enterprise-search:search-strategy (cross-source updates)
  → productivity:task-management (update TASKS.md)
```

**WAVE checkpoints:** After briefing (completeness), after search (relevance)

## 8. Drug Discovery Pipeline

**Triggers:** "find compounds", "target validation", "drug repurposing", "clinical landscape"

```
ChEMBL:compound_search (or target_search)
  → ChEMBL:get_bioactivity
  → ChEMBL:get_mechanism
  → Open Targets:query_open_targets_graphql
  → ClinicalTrials:search_trials
  → data:interactive-dashboard-builder
```

**WAVE checkpoints:** After compound search (structural relevance), after mechanism (target validation), after trials (clinical relevance)

## 9. Content Monetization Pipeline

**Triggers:** "publish to X", "monetize content", "creator flow", "social publishing"

```
content_generate (draft)
  → wave_coherence_check (quality gate)
  → content_score (engagement prediction)
  → [Claude in Chrome — publish to X/social]
  → atom_track (record publication event)
```

**WAVE checkpoints:** After generation (coherence), after scoring (quality threshold), after publishing (verification)

## 10. Full Plugin Build Pipeline

**Triggers:** "build a plugin", "create marketplace listing", "package for distribution"

```
skill-creator (design the skill)
  → create-cowork-plugin (package as .plugin)
  → [marketplace-specific adapter — see marketplace-bridges.md]
  → wave_validate (plugin coherence)
  → atom_track (release event)
```

**WAVE checkpoints:** After skill creation (instruction coherence), after packaging (structural integrity)

## 11. Minecraft Trace-n-Braid

**Triggers:** "trace_n_braid", "check minecraft status", "verify npc suite", "MC_super_skill"

```
minecraft-weaver:trace_n_braid
  → coherence-mcp:mc_server_status
  → coherence-mcp:mc_rcon_command (census)
  → coherence-mcp:mc_verify_conservation
  → atom_track (status log)
```

**WAVE checkpoints:** After directory audit (physical integrity), after RCON (connectivity), after conservation (logical stability).

---

## Composing Novel Chains

When no existing pattern matches, construct a chain by:

1. Identify the **input domain** (what the user has)
2. Identify the **output domain** (what the user wants)
3. Find skills that bridge from input → output
4. If a direct bridge doesn't exist, find intermediate skills
5. Wire them together with WAVE checks at each transition
6. Log the novel chain — if it works well, propose adding it to this file
