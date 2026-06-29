# Restructuring Method

## Method

1. Start in Team Bootstrap Mode.
2. Collect representative tasks or a skill description.
3. Record execution path. Default to `direct-skill`; only run meta-team execution preflight when the user explicitly selects `meta-team-first`.
4. Inventory existing assets.
5. Classify bundled local resources by intended use, evidence status, owner, access level, and forbidden use.
6. Extract the original workflow.
7. Classify skills by category, risk, output type, and reuse mode.
8. Identify responsibilities that must be independent.
9. Design 2-3 alternative structures only when useful: compact, default 5-6, and strongly justified expanded.
10. Choose a recommended team and justify the top-level agent count.
11. Assign skills and local resources to agents.
12. Generate the Agent Architecture Map.
13. Generate the Workflow Orchestration Map.
14. Generate the Control-Flow & Resume Contract and canonical agent independence contracts.
15. Adapt to target runtime.
16. Generate registration package when deployable artifacts are requested.
17. Design baseline-vs-team evaluation.
18. Iterate until accepted or stopped.

## Non-negotiable separations

- If data accuracy matters: data collector != data verifier.
- If delivery risk matters: content producer != independent reviewer.
- If execution has side effects: executor != execution approver.

## Agent count rule

Keep top-level agents manageable. Prefer 5-6 agents for nontrivial systems. Use fewer only with a low-risk consolidation rationale. Use more only with strong requirements such as hard isolation, independent gates, separate credentials/workspaces, side effects, or multiple regulated domains. Put smaller capabilities into skills owned by those agents.

## Local resource rule

Do not create an agent merely because a source package contains a local folder, reference file, asset collection, template, example, index, or release artifact. Assign those resources to accountable agents as owned, shared, restricted, advisory, tool-only, evidence-only, visual-only, template-only, data/index-only, or packaging-only resources. Preserve evidence boundaries: a style library, example, icon set, or design board may influence presentation, but must not become proof for domain facts or decisions unless the source skill explicitly defines it as authoritative evidence.
