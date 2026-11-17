# Diagram Generator

Diagram Generator is a platform-neutral instruction pack for creating standalone technical system maps. It turns architecture briefs, codebase notes, deployment descriptions, trust-boundary narratives, and process explanations into a single browser-openable HTML file with inline SVG.

The package is designed for agent environments such as Claude, Codex, Cursor, OpenCode, Windsurf, Gemini, GitHub Copilot, CodeBuddy, and Hermes. Shared behavior lives in `resources/`; platform files are intentionally thin adapters that route each platform to the same generation and audit workflow.

## What It Produces

The generator picks one of seven lenses and renders a standalone HTML/SVG map. Below are examples of the lenses in action, each rendered from a short brief and validated with `scripts/check-diagram.mjs`.

> Example images below live in the source repository under `docs/` (referenced by relative path). The `docs/*.png` and `LICENSE` files are part of the source repository; some packaging targets (e.g. SkillHub) strip images and license files from the distributed bundle — view them in the source repository in that case.

### System lens

![System map: an e-commerce platform with clients, API gateway, services, PostgreSQL, Redis, Kafka, object storage, and an OIDC provider](docs/example-system-map.png)

Service relationships, user entry points, storage ownership, external integrations, and operational context.

### Infrastructure lens

![Infrastructure map: multi-region deployment with CDN, global load balancer, two Kubernetes regions, managed database, object storage, and message bus](docs/example-infrastructure-map.png)

Regions, clusters, networks, gateways, managed services, object stores, queues, containers, and deployment placement.

### Trust lens

![Trust map: public clients cross a trust boundary where authentication, token validation, policy, and key management run before private services](docs/example-trust-map.png)

Identity providers, public/private boundaries, privileged operations, secrets, policy checks, token validation, and administrative paths.

### Data movement lens

![Data movement map: Web and IoT producers feed an event stream that fans out to a data warehouse, search index, and object storage](docs/example-data-movement-map.png)

Ingestion, replication, event streams, durable records, transformations, search indexes, exports, and reporting.

### Process lens

![Process map: a CI/CD pipeline from commit through build, test, approval, staging, and production, with a monitoring feedback loop](docs/example-process-map.png)

Ordered interactions, approval chains, incident response, automation pipelines, and sequence-like flows.

Also supported: **implementation maps** (repository-derived stages, script execution chains, generated artifacts) and **deployment placement maps** (workload-to-infra allocation).

## Output Contract

Default output is `html-first`: one standalone `.html` file with:

- inline SVG
- embedded CSS
- no external runtime or network dependency
- SVG download
- PNG download
- PNG copy when the browser supports it
- print/PDF support
- a notes rail for system shape, critical flows, and operational notes

Draw.io XML is optional and should only be requested when editability in draw.io or Confluence draw.io is part of the workflow.

## Directory Layout

```text
diagram-generator/
├── README.md
├── README.en.md
├── SKILL.md
├── SKILL.en.md
├── AGENTS.md
├── GEMINI.md
├── COPILOT-INSTRUCTIONS.md
├── CODEBUDDY.md
├── HERMES.md
├── LICENSE                (repo only — stripped from some distributions)
├── agents/
│   └── openai.yaml
├── resources/
│   ├── generation-rules.md
│   ├── diagram-ir.md
│   └── template.html
├── scripts/
│   └── check-diagram.mjs
├── examples/
│   ├── architecture-brief.md
│   ├── structured-input.yaml
│   ├── codex-cli-example.txt
│   ├── codex-smoke-test-prompt.md
│   ├── drawio-mode-prompt.md
│   └── portable-agent-smoke-test-prompt.md
├── docs/                  (repo only — PNG files are stripped from some distributions)
│   ├── example-system-map.png
│   ├── example-infrastructure-map.png
│   ├── example-trust-map.png
│   ├── example-data-movement-map.png
│   └── example-process-map.png
├── tests/
│   ├── platform-smoke-tests/
│   └── fixtures/
│       ├── example-commerce-system-map.html
│       ├── infrastructure-map.html
│       ├── trust-map.html
│       ├── data-movement-map.html
│       ├── process-map.html
│       ├── deployment-map.html
│       ├── implementation-map.html
│       └── bad-injected-defects.html
└── RELEASE_CHECKLIST.md
```

The CI configuration lives at the repository root (`.github/workflows/ci.yml`) and is not part of this skill's distributed package.

## Installation

Install per platform below. The key is to place this directory in the platform's skills/instruction folder and keep `resources/` accessible.

### Claude

Place or link this directory under a Claude skills folder:

```bash
mkdir -p ~/.claude/skills
ln -s /absolute/path/to/diagram-generator ~/.claude/skills/diagram-generator
```

Then ask:

```text
Use the diagram-generator skill to create a system map from this brief:

[paste brief]
```

### Codex, Cursor, OpenCode, Windsurf

Use `AGENTS.md` as the project instruction source and keep `resources/` available. The adapter points these platforms to the shared files, lens/output-mode selection, placeholder replacement, and the final audit. For Codex skill-style use:

```bash
mkdir -p ~/.codex/skills
ln -s /absolute/path/to/diagram-generator ~/.codex/skills/diagram-generator
```

### Gemini

Use `GEMINI.md` as the Gem or project instruction. Add `resources/generation-rules.md`, `resources/diagram-ir.md`, and `resources/template.html` as project knowledge when direct file access is unavailable.

### GitHub Copilot

Use `COPILOT-INSTRUCTIONS.md` as the custom instruction source, or copy its content into a repository instruction file.

### CodeBuddy

Use `CODEBUDDY.md` as the workspace rule file.

### Hermes

Use `HERMES.md` as the task specification and keep `resources/` available in the workspace.

### Domestic Chinese platforms (Trae, Tongyi, Doubao, etc.)

`AGENTS.md` is a cross-agent convention that domestic platforms can reuse directly: use it as the project-level instruction file, or merge its content into the platform's system-prompt/rules configuration, and keep the `resources/` directory accessible. Chinese trigger phrases (e.g. "帮我画个架构图") are supported, and output language follows user preference.

## Usage Pattern

1. Provide a brief or ask the agent to inspect a codebase.
2. Ask for the lens you want: system, implementation, infrastructure, trust, data movement, deployment, or process.
3. Generate an `html-first` artifact unless draw.io editability is explicitly needed.
4. Ask for a visual audit pass before publishing.

## Smoke Tests

Platform-specific smoke prompts live in `tests/platform-smoke-tests/`.

Use them before publishing or after changing `resources/`:

- `claude.md`
- `codex.md`
- `gemini.md`
- `copilot.md`
- `codebuddy.md`
- `agents.md` for Cursor, OpenCode, Windsurf, and similar agents

Each smoke test checks that the agent uses `html-first`, follows the atlas-style template, keeps draw.io hidden by default, emits a notes rail without placeholder text, and can preserve unrelated content when revising an existing diagram.

## Output Checker

Every generated artifact must pass the zero-dependency validator before it is returned:

```bash
node scripts/check-diagram.mjs <output-file.html>
```

It verifies placeholder removal, notes-rail presence, self-containment, marker integrity, IR geometry (node bounds, overlaps, edge endpoints, region bounds, region containment with a minimum 10px gutter on every side), `data-node-id`/`data-edge-id` cross-checks against the IR, and optional `labelAnchor` overlap checks. Warnings do not block; errors exit 1.

### Error codes

Every checker message carries a stable, machine-greppable code prefix (`[Exxx]` errors, `[Wxxx]` warnings) so callers can classify failures without parsing prose:

| Code | Category | Notes |
|------|----------|-------|
| E001 | Usage | No input path given |
| E002 | IR parse | `#diagram-ir` slot is not valid JSON |
| E003 | Regions | Region ids/bounds/containment violations |
| E004 | IR structure | Missing/duplicate ids, missing nodes/edges arrays |
| E005 | Bounds | Node/region bounds invalid or outside the viewBox |
| E006 | Node overlap | Two node bounds intersect |
| E007 | Edge references | Missing or unknown source/target node |
| E008 | SVG–IR mismatch | `data-node-id`/`data-edge-id` not cross-consistent |
| E009 | Markers | Undefined marker reference or fill mismatch |
| E010 | Placeholder | Template placeholder text still present |
| E011 | Notes rail | `<aside class="notes">` missing |
| E012 | Self-containment | External or relative asset reference |
| E013 | Label anchor | `labelAnchor` invalid or sitting on a node |
| E014 | Connector geometry | Endpoint off-node, path through node, border-hugging |
| E099 | Uncategorized | Any error not yet mapped — report it so it gets a code |
| W001 | Legacy mode | No IR slot found; geometry checks skipped |
| W002 | Revise scope | `mode: revise` without `edit_scope` |
| W003 | Export UI | Optional toolbar / `#system-map` SVG absent |
| W004 | Path syntax | Unsupported SVG path syntax; endpoint geometry unchecked — review manually |

Exit codes: `0` when there are no errors (warnings allowed), `1` when any error exists.

A known-good reference artifact lives at `tests/fixtures/example-commerce-system-map.html` — it renders the Example Prompt brief below and passes the checker with zero errors and zero warnings. CI (repo-root `.github/workflows/ci.yml`) re-runs the checker against it on every push, so keep it green when changing checker rules or the template.

A known-bad fixture lives at `tests/fixtures/bad-injected-defects.html` — the known-good artifact with four injected defects (a template placeholder residue, a node whose bounds leave the viewBox, a region `contains` entry referencing a nonexistent node, and a node sitting flush against its region border). CI asserts the checker rejects it (non-zero exit) and reports all four defect classes; this proves the checker fails closed, not just that it passes a good sample.

## Quality Guidance

These rules keep generated output maintainable and auditable:

- Keep reusable behavior in `resources/generation-rules.md`.
- Keep the planning model in `resources/diagram-ir.md`.
- Keep the HTML/SVG/CSS base in `resources/template.html`.
- Keep platform files short; they should route the agent to the shared resources instead of restating them.
- Keep platform adapters synchronized with `SKILL.md` when required behavior changes.
- Use a two-step workflow for smaller-context models: first normalize the system into actors, components, stores, flows, and risks; then generate the final HTML from that normalized plan.
- For existing-diagram edits, prefer local coordinate and connector changes over full regeneration.
- Treat draw.io XML as an export adapter, not the default rendering target.

## Output Modes

### `html-first`

The default mode. Prioritize visual clarity, readable labels, correct connectors, and a polished standalone HTML artifact.

Prompt:

```text
Create a system map for this platform:

[brief]
```

### `html + drawio xml`

Experimental and opt-in. Use when the user wants a browser-viewable artifact plus model-generated draw.io XML. Import-test the XML in draw.io before relying on it.

Prompt:

```text
Create a system map in html + drawio xml mode:

[brief]
```

### `drawio-first`

Planned. This mode is not production-ready until dedicated mxGraphModel rules, a template, and import validation are included.

## Example Prompt

```text
Create a standalone HTML system map for:

- Web and mobile clients enter through a CDN and API gateway.
- Backend services include users, catalog, orders, payments, and notifications.
- PostgreSQL stores transactional records.
- Redis caches sessions and hot catalog reads.
- Kafka carries order-created and payment-completed events.
- Object storage keeps invoices and exports.
- An external OIDC provider handles identity.
- Everything runs in Kubernetes behind ingress.

Use the default html-first mode. Keep visible text in English.
```

## Design Principles

A diagram should explain behavior, not merely inventory components. Core principles:

- A diagram should explain behavior, not merely inventory components.
- Use one abstraction level per artifact.
- Show ownership boundaries, durable state, async movement, trust controls, and operational watchpoints.
- Keep the main path readable before adding secondary paths.
- Prefer concise labels and put longer explanations in the notes rail.
- Do not rely on external images, fonts, scripts, or build tools.

## Publishing

Before publishing, remove local smoke-test outputs (the checked-in fixture under `tests/fixtures/` stays) and run `RELEASE_CHECKLIST.md`.

## FAQ & Common Pitfalls

The most common issues and how to resolve them.

**Q: The checker reports an edge collinear with a node or region border. What do I do?**
A: Reroute the connector so it exits a node edge perpendicularly and travels in the free space between nodes. Never run a connector along the outer edge of its own source or target node, and avoid segments that share more than ~12 px with any region border.

**Q: A node overlaps a region it should sit inside.**
A: The checker enforces a 10 px gutter between every node and the region border. Shrink the node or expand the region; do not place nodes flush against a border.

**Q: draw.io XML fails to import in draw.io / Confluence.**
A: `html + drawio xml` mode is experimental. Always import-test the XML before relying on it. If editability is not required, use the default `html-first` mode, which is production-ready.

**Q: The generated HTML has leftover placeholder text.**
A: `resources/template.html` uses plain-text placeholders (e.g. `System Map Title`, `One sentence that states...`); all of them must be replaced with concrete content. The checker detects these placeholder strings (E010) and fails on any residue. Do not leave template defaults in a delivered artifact.

**Q: Can I edit an existing diagram instead of regenerating it?**
A: Yes — prefer local coordinate and connector changes over full regeneration. Inspect the current artifact first and preserve unrelated nodes, notes, and color semantics.

**Q: The diagram looks cluttered.**
A: Use the notes rail for longer explanations instead of crowding the canvas. Keep one abstraction level per artifact and put secondary flows behind the main path.

**Q: Which lens should I pick?**
A: System for components/flows, infrastructure for deployment topology, trust for security boundaries, data movement for ingestion/streams, process for ordered pipelines, deployment for workload placement, implementation for code-derived stages. When unsure, start with a system map.

**Q: Why are images and LICENSE missing from my installed copy?**
A: Some distributors (e.g. SkillHub) strip PNG images and standalone LICENSE files from the package for security/format reasons. The canonical images and license are always available in the source GitHub repository.
