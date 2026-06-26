# Universal Installer docs: align SPEC, TECHNICAL, README on the eight interfaces + install spec URL

The three docs in `docs/universal-installer/` were drifting and missing two interfaces and the install-spec URL story. This PR aligns them so a new AI can boot from the docs alone and follow Parker's acceptance sentence:

> Use the install spec URL to learn the safe install flow; use catalog to resolve the slug; use `ldm install` with stable/alpha/beta track flags; installer detects and installs the product's declared interfaces; stacks install bundles.

## Canonical interface order (now in the spec)

1. CLI
2. Module
3. MCP Server (local stdio)
4. **Remote MCP** (HTTP/SSE or streamable HTTP) ... new
5. OpenClaw Plugin
6. Skill
7. Claude Code Hook
8. **Claude Code Plugin** ... was already in TECHNICAL, now in SPEC

Local and Remote MCP sit next to each other because they are sibling transports. CC Plugin sits last because it bundles the others.

## Remote MCP contract (pinned)

> Remote MCP endpoint is **declared by package/catalog metadata** and **registered by `ldm install`**.

Convention: `mcp.remote = { url, transport, auth }` in `package.json`. No filesystem-sniffing fallback. The repo opts in by writing the field. The catalog can override `url` if the package ships a placeholder.

Detection and install action are tracked in `ai/product/bugs/installer/` (see Master Plan below). The spec is canonical now; the detector and installer catch up next.

## What changed in this PR

**SPEC.md**
- New **Architecture Layers** section: Interface / Installer / Catalog / Install Spec / Stacks. One table. Acceptance sentence verbatim.
- Renamed Six Interfaces to **Eight**, in the canonical order above.
- Added **#3 MCP Server (local stdio)** clarifier and cross-link to #4.
- Added **#4 Remote MCP** with pinned contract, convention, detection, install, and a "how it differs from #3" table.
- Added **#8 Claude Code Plugin**.
- Renamed "The Reference Installer" to **The Installer**. Added `--alpha` / `--beta` track flag examples.
- New **Install Spec** section: URL convention, behavior contract (check, explain, dry-run, install, update, pair), origin (gen from / mirror of / alongside SKILL.md ... contract is URL+behavior), tracks, **install spec vs `agent.txt`** distinction, `wip-codex-remote-control` as worked example.

**TECHNICAL.md**
- Interface table updated to eight rows with numbering. Local and Remote MCP labeled.
- Added **#4 Remote MCP** section with convention/detection/install/auth and pointers to the implementation tickets.
- Detection table: added Remote MCP row, sharpened MCP row to "local stdio".
- Replaced stale install prompt template (`{product-init} init --dry-run`) with canonical `ldm install --dry-run <slug>`.
- Added Codex Remote Control to examples table.

**README.md (docs/universal-installer/README.md)**
- Pointer line updated to name all eight interfaces and reference the install spec URL convention + tracks.

## Master plan and tickets

Filed under `ai/product/bugs/installer/`:

- [Master plan: eight interfaces alignment](ai/product/bugs/installer/2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md)
- [Remote MCP detection (#4)](ai/product/bugs/installer/2026-04-28--cc-mini--installer-remote-mcp-detection.md)
- [Remote MCP install action (#4)](ai/product/bugs/installer/2026-04-28--cc-mini--installer-remote-mcp-install.md)
- [Install spec URL publish pipeline](ai/product/bugs/installer/2026-04-28--cc-mini--install-spec-url-publish-pipeline.md)
- [CC Plugin (#8) detection verified end-to-end](ai/product/bugs/installer/2026-04-28--cc-mini--installer-cc-plugin-detect-verified.md)
- [Catalog audit for install-spec URL field](ai/product/bugs/installer/2026-04-28--cc-mini--catalog-install-spec-url-audit.md)

The PR delivers the canonical spec language. The tickets carry the implementation work to make Remote MCP, the install-spec publish pipeline, and the catalog field actually exist.

## Sibling PR

`tools/wip-universal-installer/SKILL.md` and `REFERENCE.md` in `wip-ai-devops-toolbox-private` still describe the older six-interface story. Refresh to the eight-interface taxonomy + install-spec URL pointer is a sibling PR (out of scope here).

## Acceptance check

After this PR, a new AI reading only `docs/universal-installer/SPEC.md` should be able to:

1. Name the eight interfaces in canonical order.
2. State the acceptance sentence verbatim (it is in the Architecture Layers section).
3. Distinguish install spec URL from `agent.txt`.
4. State the Remote MCP contract: declared by package/catalog metadata, registered by `ldm install`.
