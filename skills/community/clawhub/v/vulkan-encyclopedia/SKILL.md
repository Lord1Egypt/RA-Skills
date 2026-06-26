---
name: vulkan-encyclopedia
description: >-
  Vulkan specification/reference workflow for Vulkan-API-specific questions,
  exact command and structure semantics, valid-usage and VUID lookup,
  synchronization reasoning, pipeline/resource setup, extension/feature
  checks, limits/formats/capabilities review, and code review in a Vulkan API
  context. Use when the request is clearly about Vulkan itself: `Vk*` types,
  `vk*` commands, VUIDs, instance/physical-device/logical-device setup,
  swapchains, queues, command buffers, descriptors, render passes or dynamic
  rendering, pipelines, memory/resources, synchronization, SPIR-V in a Vulkan
  pipeline context, or extension/feature behavior. Do not use for generic
  graphics programming, engine-level rendering design, shader-language-only
  questions, OpenGL, Direct3D, Metal, CUDA, or generic shader authoring
  unless the Vulkan API/spec layer is materially involved.
metadata: {"openclaw":{"emoji":"🌋","homepage":"https://docs.vulkan.org/spec/latest/index.html"}}
---

# Vulkan Encyclopedia

## Overview

Use a docs-first workflow for Vulkan work. Prefer the official Vulkan specification/reference docs at `https://docs.vulkan.org/spec/latest/index.html`, consult cached local copies under `.Vulkan-Encyclopedia/` before re-fetching, and record useful authoritative excerpts plus environment-specific operational learnings so future work gets faster, safer, and more grounded.

This skill is for the **Vulkan API/spec layer**, not for generic rendering theory and not for standalone shader-language questions unless they are being asked in direct service of Vulkan API behavior.

## Workflow

1. **Classify the task**
   - Decide whether the task is a Vulkan API question, specification lookup, code-review task, validation/debugging task, architecture/design task, or live implementation task.
   - Use this skill when the task materially depends on Vulkan API semantics, Vulkan object/command structure, extension/feature behavior, synchronization rules, limits/capabilities/formats, or validation/spec interpretation.
   - Do not use this skill for generic graphics concepts, standalone shader-language work, or engine-level rendering discussion unless the Vulkan API/spec layer is actually in play.

2. **Check local cache first**
   - Use `.Vulkan-Encyclopedia/` as the local knowledge/cache root.
   - Check these locations first when relevant:
     - `.Vulkan-Encyclopedia/docs/docs.vulkan.org/spec/latest/...`
     - `.Vulkan-Encyclopedia/notes/components/...`
     - `.Vulkan-Encyclopedia/notes/patterns/...`
     - `.Vulkan-Encyclopedia/inventory/...`
   - If a cached page or note already answers the question well enough, use it.

3. **Consult authoritative Vulkan docs before answering or acting**
   - Before answering direct or indirect Vulkan questions that depend on API semantics, exact command/structure rules, feature or extension behavior, synchronization guarantees, limits, valid usage, or version-sensitive details, consult the official Vulkan docs unless the answer is already well-supported by the local cache.
   - Before performing non-trivial Vulkan code review or implementation guidance, consult the relevant docs first when:
     - exact member names, allowed states, or command rules matter
     - synchronization or resource-lifetime behavior is easy to misremember
     - the task involves VUID interpretation, extension/feature enabling, or pipeline/resource correctness
   - If the problem is really about GLSL syntax/qualifiers/stage interfaces rather than Vulkan API semantics, prefer the GLSL skill instead of stretching this one.
   - Do not improvise fragile Vulkan answers from memory when the spec is easy to check.

4. **Cache consulted docs locally**
   - When you consult a Vulkan docs page, save a normalized cache copy under `.Vulkan-Encyclopedia/docs/docs.vulkan.org/spec/latest/...`.
   - Mirror the official docs path structure as much as practical.
   - Cache only pages actually consulted; do not try to mirror the whole spec eagerly.
   - Use `scripts/cache_doc.py` when appropriate.

5. **Separate authoritative documentation from local observations**
   - Store official-doc-derived material under `.Vulkan-Encyclopedia/docs/...`.
   - Store environment-specific operational knowledge under:
     - `.Vulkan-Encyclopedia/notes/components/`
     - `.Vulkan-Encyclopedia/notes/patterns/`
     - `.Vulkan-Encyclopedia/inventory/`
   - Distinguish clearly between:
     - authoritative documented behavior
     - observed project/environment state
     - inferred best-practice guidance

6. **Record useful local learnings**
   - After useful live work, save durable notes such as:
     - project-specific Vulkan architecture notes
     - recurring validation/debugging patterns
     - extension/feature adoption decisions
     - synchronization/resource-management gotchas
     - safe/unsafe operational boundaries for the codebase or environment
   - Prefer concise durable notes over re-learning the same Vulkan details later.

## Live Work Rules

- Treat spec lookup as the default preflight for non-trivial Vulkan work.
- Prefer read/inspect first when entering unfamiliar Vulkan code.
- Treat synchronization, memory/resource lifetime, queue ownership, layout transitions, extension/feature gating, and validation/VUID interpretation as higher-sensitivity areas.
- When uncertainty remains after checking cache + docs, say so and avoid bluffing.
- When answering a question, mention when useful whether the answer comes from cached official docs, a fresh official docs lookup, or live observed project state.

## Data Root

Use this workspace-local root for cache and notes:

- `.Vulkan-Encyclopedia/`

Expected structure:

- `.Vulkan-Encyclopedia/docs/docs.vulkan.org/spec/latest/...`
- `.Vulkan-Encyclopedia/notes/components/...`
- `.Vulkan-Encyclopedia/notes/patterns/...`
- `.Vulkan-Encyclopedia/inventory/...`

Use `scripts/init_workspace.py` to create or repair the expected directory structure.

## Note Destinations

- Component-specific observations → `.Vulkan-Encyclopedia/notes/components/<component-name>.md`
- Reusable Vulkan patterns/gotchas → `.Vulkan-Encyclopedia/notes/patterns/<topic>.md`
- Environment-wide architecture/access info → `.Vulkan-Encyclopedia/inventory/*.md`
- Cached official docs → `.Vulkan-Encyclopedia/docs/docs.vulkan.org/spec/latest/...`

## Secrets / Sensitive Data

- Do not store plaintext credentials, API keys, session tokens, private URLs, recovery codes, or other secrets in the encyclopedia notes/inventory tree.
- If a note needs to mention access details, keep it high-level and redact or omit secret material.
- Treat these workspace notes as operational memory, not as a secrets vault.

## Resources

- `scripts/init_workspace.py` — create or repair the `.Vulkan-Encyclopedia/` directory tree.
- `scripts/cache_doc.py` — fetch and cache a consulted official Vulkan docs page under `.Vulkan-Encyclopedia/docs/...`.
- `references/workflow.md` — detailed operating workflow and evidence-handling rules.
- `references/cache-layout.md` — canonical `.Vulkan-Encyclopedia/` directory structure.
- `references/topic-map.md` — useful Vulkan topic groupings for faster authoritative lookup.

## Good Outcomes

- Answer a Vulkan question using cached or freshly checked official docs instead of guesswork.
- Inspect Vulkan code after checking the relevant spec pages and record any new project-specific operational knowledge.
- Build a growing local Vulkan knowledge cache that makes later work faster, safer, and more grounded.
- Turn one-off Vulkan discoveries into durable notes so future work does not rediscover them from scratch.

## Avoid

- Answering Vulkan-specific questions purely from memory when the spec is easy to consult.
- Treating local observed engine/project behavior as if it were guaranteed authoritative Vulkan behavior.
- Dumping large amounts of low-value docs into the workspace without a reason.
- Writing project-specific observations into the official-doc cache tree.
- Making high-confidence claims about synchronization/valid-usage details without checking the spec when exact behavior matters.
