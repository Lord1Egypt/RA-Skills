# Local Resource Allocation

Use this policy when the source material includes a skill package, plugin, agent bundle, workflow folder, or zip with local files such as `references/`, `assets/`, `scripts/`, `templates/`, examples, indexes, manifests, configuration, or release metadata.

## Core rule

Bundled local resources are resources, not automatic agents.

Do not create an agent merely because a package contains a folder, file type, policy document, asset collection, script, template, index, example, or release note. Create an agent only when there is an accountable role that owns decisions, outputs, approvals, side effects, or gates. Otherwise assign the resource to an existing agent as owned, shared, restricted, advisory, tool-only, evidence-only, visual-only, template-only, data/index-only, or packaging-only.

## Required classification

For each meaningful resource group, classify:

| Field | Meaning |
|---|---|
| `resource` | File, folder, package area, or resource group. |
| `resource_class` | policy/reference, script/tool, asset library, template, example, data/index, config, release metadata, state/memory, credential-sensitive, unknown. |
| `original_role` | What the source workflow appears to use it for. |
| `owner_agent` | Agent accountable for using or maintaining it. |
| `access_level` | owned, shared, restricted, read-only, approval-required, forbidden, deferred. |
| `evidence_status` | authoritative evidence, derived evidence, advisory reference, style/visual-only, tool-only, template-only, example-only, packaging-only, unknown. |
| `allowed_use` | What the new team may use it for. |
| `forbidden_use` | What the new team must not infer or do from it. |
| `gate` | Reviewer, validator, approval, or safety gate before use. |
| `migration_action` | keep, split, merge, wrap as tool, copy as asset, expose as shared reference, restrict, archive, remove, or defer. |

## Evidence boundary

Separate evidence from presentation aids.

- A source document, verified dataset, schema, or run output may be authoritative evidence only when the original workflow treats it as such.
- A style guide, icon set, design board, example output, retrieval index, sample prompt, or visual library may guide presentation, candidate diversity, or vocabulary, but must not justify domain facts, scientific claims, compliance conclusions, user decisions, arrows, labels, metrics, or tool actions.
- A script may be a tool for deterministic execution or validation, but its existence does not make its output trusted unless the team assigns an owner and a gate.
- A template may define format, not truth.
- Release metadata may guide packaging and compatibility, not runtime task decisions.

## Role guidance

Assign local resources by accountable use:

| Resource pattern | Typical owner |
|---|---|
| Workflow rules, process references, SOPs | Orchestrator, Source Mapper, or domain producer |
| Source documents and evidence corpora | Data Collector, Evidence Verifier, or Domain Analyst |
| Validation scripts, state helpers, deterministic checkers | Tool/State Guard or QA Reviewer |
| Prompt templates and output templates | Composer, Prompt Builder, or Runtime Adapter |
| Style boards, icons, design patterns, media assets | Designer, Prompt Builder, or Presentation Agent |
| Examples and sample outputs | Training/reference owner or QA Reviewer |
| Manifests, package metadata, release checks | Runtime Adapter or Release Reviewer |
| Credentials, secrets, environment files | Security/Tool Policy owner; restrict or exclude by default |

## Meta-team work order

When local resources are present, the S2T meta-team should include an Source Mapper work order that answers:

1. Which resource groups exist?
2. Which are runtime-critical, advisory, optional, or release-only?
3. Which resources are evidence versus presentation aids?
4. Which agent owns each resource after restructuring?
5. Which resources need gates before use?
6. Which resources must not be copied into deployable artifacts?
7. Which resources should remain bundled rather than loaded into prompt context?

## Output requirement

Include a `Local resource allocation map` unless the user explicitly asks for only a minimal draft or the source has no meaningful bundled resources.

Use the output contract in `references/output-contracts.md`.

For `Delivery: package`, emit machine-readable `local-resource-allocation.map.json`, `source-resource-manifest.json`, and `docs/local-resource-allocation-map.md`. If runtime-critical source resources are not bundled, the generated package must record the accessible `source_root` or block target-team execution until the resources are restored. A package that silently drops source `references/`, `scripts/`, `templates/`, `assets/`, examples, indexes, agents, or release metadata fails the package release gate.
