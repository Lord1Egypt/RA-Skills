# Guided Intake

Use guided intake when the user's goal, source material, risk boundaries, or package target is unclear.

## Required intake topics

1. Source material: `<SOURCE_SKILL_ZIP>`, folder path, generated package, registry manifest, or pasted workflow.
2. Route: `source-to-team`, `brief-to-team`, or `guided-to-team`.
3. Delivery: `design` or `package`.
4. Target runtime: `codex` when deployable artifacts are requested.
5. Architecture method: framework-neutral agent architecture relationship graph with profile-based agents by default.
6. Model invocation policy: OpenAI Codex is the default runner; direct API calls are only an explicitly labeled API-run role simulation or API-service follow-up.
7. Human-interaction execution mode before source conversion starts: preserve source human-interaction steps, selectively preserve/convert them, or fully automate with audit. Default to preserving source human-interaction steps.
8. Required user input nodes: which source steps must pause for user settings, selections, approvals, or terminal/new-request decisions.
9. Agent count: prefer 5-6 top-level agents; justify fewer or more.
10. Independent gates: which outputs require a separate reviewer/verifier.
11. Local resources: files, tools, prompts, templates, scripts, docs, data, credentials-sensitive items, and package metadata.
12. Design-continuation needs: Codex/OpenAI registration/use guidance, API-service runner prompt, API-runner role simulation, Hermes profile conversion, OpenClaw profile conversion, or all of these. Package-end prompts remain Codex-only.

## Delivery selection

| User wants | Use |
|---|---|
| Understand and redesign source | `Delivery: design` |
| Check design consistency | Use the design quality gate inside `Delivery: design` |
| Generate Codex target-team artifacts | `Delivery: package` |
| Check package completeness/packageability | Use the package release gate inside `Delivery: package` |
| Install/register/use after package | Keep `Delivery: package`; provide Codex-only package-end prompt templates and manifest-scoped guidance. |
| Compare or review quality | Use design review or package release review sections; do not expose a separate validation delivery. |
| Restore from previous metadata | Treat the capsule/package as `source-to-team` source material and choose `design` or `package`. |

## Guided-to-team closeout

Use `Route: guided-to-team` for this path. Package output must include design intermediate results, `design-output.zip`, entry-agent startup welcome page, generated target-team agents/functions, profile artifacts, Codex artifacts, usage guide, package release gate, and Codex-only package-end prompt templates.
