# Universal Installer: Eight Interfaces + Install Spec Alignment ... Master Plan

**Date:** 2026-04-28
**Owner:** cc-mini
**Status:** in flight
**Trigger:** Parker asked whether the universal-installer docs were aligned. Crystal search confirmed Claude Code Plugin landed in the toolbox in March 2026 as interface #7, and that on April 15 we discussed adding **Remote MCP** as a further new interface. Neither was reflected in the canonical docs at `wip-ldm-os-private/docs/universal-installer/`, and Remote MCP was never written into any spec/code anywhere.

## Goal

Bring the universal-installer to a state where:

- The canonical docs at `wip-ldm-os-private/docs/universal-installer/` (README, SPEC, TECHNICAL) are mutually consistent.
- The spec covers **eight interfaces**, in this canonical order:

  1. CLI
  2. Module
  3. MCP Server (local stdio)
  4. **Remote MCP** (HTTP/SSE or streamable HTTP) ... new
  5. OpenClaw Plugin
  6. Skill
  7. Claude Code Hook
  8. **Claude Code Plugin** ... was already in TECHNICAL.md, missing from SPEC

  Rationale: Remote MCP sits next to local MCP because they are sibling transports of the same protocol. CC Plugin sits last because it bundles the others.

- The Remote MCP **contract** is pinned: *Remote MCP endpoint is declared by package/catalog metadata and registered by `ldm install`.* Anything fuzzier than that is out of spec.
- The **install spec URL** layer (`wip.computer/install/<slug>.txt`) is documented as a first-class concept, distinct from `agent.txt`.
- The **installer** (`ldm install`) actually detects and installs all eight interfaces.
- The **toolbox** SKILL.md and REFERENCE.md match the canonical doc taxonomy.
- Every product that should ship a Remote MCP endpoint is decided and tracked.

## What landed (or is landing in PR #715)

- ✅ Architecture Layers (Interface / Installer / Catalog / Install Spec / Stacks) added to SPEC.md with Parker's acceptance sentence verbatim.
- ✅ Claude Code Plugin added to canonical SPEC.md (was already in TECHNICAL.md from March 14, missing from SPEC). Now numbered as #8 in the canonical order.
- ✅ Install Spec URL section added to SPEC.md: URL convention, behavior contract, tracks (--alpha/--beta/stable), agent.txt distinction, Codex Remote Control as worked example.
- ✅ TECHNICAL.md install prompt template updated from `{product-init} init --dry-run` to `ldm install --dry-run <slug>`.
- ✅ Codex Remote Control added to TECHNICAL.md examples.
- 🟡 (this PR extension) Remote MCP added as #4 (sibling to local MCP) in SPEC.md and TECHNICAL.md, with the contract pinned: declared by package/catalog metadata, registered by `ldm install`.
- 🟡 (sibling PR) Toolbox SKILL.md and REFERENCE.md refreshed to eight interfaces and install-spec URL pointer.

## What still needs doing (separate tickets, linked below)

| Ticket | What | Why it is its own ticket |
|--------|------|-------------------------|
| [Remote MCP detection](2026-04-28--cc-mini--installer-remote-mcp-detection.md) | `detect.mjs` learns to detect a Remote MCP declaration in a repo. | Code change. Needs convention call (where does the URL come from?). |
| [Remote MCP install action](2026-04-28--cc-mini--installer-remote-mcp-install.md) | `install.js` learns to register a Remote MCP endpoint (probably via `.mcp.json` plus optional Claude Desktop connector hint). | Code change. Depends on detection. |
| [Install spec URL publish pipeline](2026-04-28--cc-mini--install-spec-url-publish-pipeline.md) | `wip.computer/install/<slug>.txt` is a stable URL contract. Right now only `wip-ldm-os.txt` and `wip-codex-remote-control.txt` exist; we have no pipeline that takes a SKILL.md (or sibling source) and publishes it to that URL on release. | Infra change. Needs decision on origin (SKILL.md auto-derive vs hand-authored). |
| [CC Plugin detection verified end-to-end](2026-04-28--cc-mini--installer-cc-plugin-detect-verified.md) | The toolbox SPEC says CC Plugin is interface #7. detect.mjs reportedly handles `.claude-plugin/plugin.json`. We have not verified it runs end-to-end against a real plugin in 2026-04. | Verification only, but it gates marketing the seventh interface. |
| [Catalog audit for install-spec URL field](2026-04-28--cc-mini--catalog-install-spec-url-audit.md) | Each `catalog.json` entry should know its install-spec URL. Right now the install spec URLs are implicit via slug. Audit + decide whether we add an explicit field. | Schema decision + audit. |
| [Cardio tracker worked example](2026-04-28--cc-mini--installer-cardio-tracker-worked-example.md) | Full version of the bespoke-composition vision example. Walks "track my RHR for 8 weeks" end-to-end across Memory Crystal context + Woodway Remote MCP + calendar + agent-generated dashboard. The compact sketch in SPEC.md points here. | Documentation/vision-comprehension. Long-form. Anchors the vision-comprehension gate. |

## Why this exists

The universal-installer story drifted because:

- The toolbox SPEC.md (`tools/wip-universal-installer/SPEC.md`) was the original canonical home.
- We later moved canonical to `wip-ldm-os-private/docs/universal-installer/SPEC.md` and left a MOVED notice.
- Subsequent updates (CC Plugin in March, Remote MCP discussion in April) only partially propagated.

This master plan is the single index for getting the spec, the installer code, the toolbox docs, and the publish pipeline back into one shape.

## Definition of done

A new AI reading only `wip-ldm-os-private/docs/universal-installer/SPEC.md` should be able to:

1. Name the eight interfaces in canonical order.
2. State the acceptance sentence: "Use the install spec URL to learn the safe install flow; use catalog to resolve the slug; use `ldm install` with stable/alpha/beta track flags; installer detects and installs the product's declared interfaces; stacks install bundles."
3. State the Remote MCP contract: declared by package/catalog metadata, registered by `ldm install`, no filesystem-sniffing fallback.
4. Distinguish install spec URL from agent.txt.
5. Run `ldm install --dry-run <slug>` against any of our products and see all declared interfaces (including #4 and #8) reported correctly.
6. **Vision-comprehension gate (added 2026-04-28):** articulate why "cardio experiment tracker" is **not** a product category we ship as an app, but a bespoke composition built from agent-native services like treadmill data (Remote MCP), personal context (Memory Crystal), calendar/time semantics, and an agent-generated UI. If a future doc edit breaks this comprehension, the gate catches it. Worked example tracked in [installer-cardio-tracker-worked-example.md](2026-04-28--cc-mini--installer-cardio-tracker-worked-example.md).

When all sub-tickets (including the worked-example ticket) are closed, the master plan moves to `archive/`.

## Related

- Conversation receipts that informed this plan: crystal hits on 2026-03-14 (CC Plugin landed in toolbox as #7) and 2026-04-15 (Remote MCP proposed as #8 but never landed).
- Canonical docs: `docs/universal-installer/{README,SPEC,TECHNICAL}.md`.
- Toolbox source (with MOVED notice): `repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-universal-installer/`.
