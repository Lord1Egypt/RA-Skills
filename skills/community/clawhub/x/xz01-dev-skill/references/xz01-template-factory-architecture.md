# xz01 Template Factory Architecture Notes

Use this reference when the user asks whether the current OpenClaw/Hermes xz01 workflow can support many dual-end download-site templates, or asks for an automatic development + render + validation pipeline.

## Key Assessment

The existing `main → dev → test → rule → main` flow is a good role-separation and quality-gate skeleton, but it is not sufficient by itself for a 60-template xz01 dual-end template factory.

It fits:

- single template development or repair
- dev/test/rule separation
- test failure returning to dev
- rule review after test passes
- final main acceptance

It does not fully fit:

- learning 60 dual-end templates as a corpus
- extracting reusable template/render/data patterns
- learning database schema and route mappings
- automatically planning a new single-type download site
- automatically deploying/rendering PC + mobile output
- batch validation and repair loops across many runs
- final numbered packaging of passed templates

## Required Factory Layers

A complete xz01 automation architecture should add these layers while preserving the existing role boundaries:

1. **Corpus Layer** — store raw 60 template archives, extracted templates, and a manifest.
2. **Learning Layer** — extract template directory structures, page types, components, includes, CSS classes, render tags, data calls, PC/mobile relationships, and common pitfalls.
3. **Database Learning Layer** — extract schema, content/category/download tables, status fields, route map, template bindings, and existing DB routes. Preserve the hard rule: use database routes only; do not create routes from template filenames.
4. **Knowledge Layer** — store extracted patterns in SQLite/JSON (`templates.sqlite`, `db_schema.json`, `route_map.json`, `render_tags.json`, `component_patterns.json`, `validation_rules.json`).
5. **Planning Layer** — convert a user request into `requirement.json` and `plan.json` before dev writes code.
6. **Generation Layer** — dev generates PC + mobile templates from the plan and knowledge base, not from ad hoc context.
7. **Render Layer** — deploy generated templates to the test site, clear runtime cache, render pages, save HTML/DOM/screenshots.
8. **Validation Layer** — test runs static checks, route/data checks, DOM checks, PC/mobile screenshots, AI vision analysis, and AI-vs-DOM anti-hallucination comparison.
9. **Repair Loop** — failed validation generates `repair-task.json`, returns to dev, redeploys, rerenders, and retests until issues are zero.
10. **Rule Review Layer** — rule audits process compliance and durable rule updates.
11. **Packaging Layer** — only fully verified templates are numbered and compressed under `/root/.hermes/workspace/xz01/`.

## Recommended Writable Layout

Keep `/root/.openclaw/` read-only. Put factory state outside OpenClaw:

```text
/root/.hermes/workspace/xz01-factory/
├── corpus/
│   ├── raw/
│   ├── extracted/
│   └── manifest.json
├── knowledge/
│   ├── templates.sqlite
│   ├── db_schema.sql
│   ├── db_schema.json
│   ├── route_map.json
│   ├── component_patterns.json
│   ├── render_tags.json
│   ├── css_tokens.json
│   └── validation_rules.json
├── runs/
│   └── run-0001/
│       ├── requirement.json
│       ├── plan.json
│       ├── generated/
│       ├── deploy-log.json
│       ├── screenshots/
│       ├── validation-report.json
│       ├── repair-history.json
│       └── final-report.md
├── scripts/
│   ├── ingest-templates.js
│   ├── extract-template-patterns.js
│   ├── extract-db-schema.js
│   ├── generate-template-plan.js
│   ├── deploy-render.js
│   ├── validate-dual-end.js
│   ├── compare-with-corpus.js
│   ├── package-passed-template.js
│   └── queue-runner.js
└── reports/
    ├── corpus-summary.md
    ├── learning-report.md
    └── batch-status.md
```

Test-side artifacts should remain under `/www/wwwroot/www.900az.com` unless the user says otherwise, e.g.:

```text
/www/wwwroot/www.900az.com/xz01-runs/
├── screenshots/
├── reports/
├── dom-snapshots/
└── ai-vision/
```

Passed packages go under:

```text
/root/.hermes/workspace/xz01/
```

## Flow Upgrade

Current single-task flow:

```text
user → main → dev → test → rule → main
```

Factory flow:

```text
user request
  ↓
main creates run_id
  ↓
read corpus knowledge + DB route map
  ↓
generate requirement.json + plan.json
  ↓
dev generates PC/mobile templates
  ↓
renderer deploys + clears cache + renders PC/mobile
  ↓
test validates static structure + data + screenshots + AI vision + DOM comparison
  ├── fail → repair-task.json → dev fixes → deploy/render/test again
  └── pass → rule review
                ↓
             main acceptance
                ↓
        numbered package under /root/.hermes/workspace/xz01/
```

## Flow Controller Implication

The current `flow-controller.js` style is single-flow (`/tmp/taskflow-state.json`). For 60-template/batch work, prefer run-scoped state:

```text
/root/.hermes/workspace/xz01-factory/runs/{run_id}/flow.json
/root/.hermes/workspace/xz01-factory/queue.sqlite
```

States should include:

```text
queued → learning → planning → developing → deploying → rendering → validating → repairing → rule_review → packaging → completed
```

A production-grade controller should perform real message delivery confirmation, not merely session-file existence checks, before advancing workflow state.

## Validation Matrix

Test should validate PC and mobile independently:

- HTTP 200 for every existing DB route to be handled
- no invented routes
- template tag closure (`if`, `foreach`, `include`)
- no raw PHP short tags in templates
- include/css/js referenced files exist
- CSS brace balance and no orphan declarations
- HTML/CSS/JS class consistency
- data rendering counts and required fields
- status filters such as `status=1`, `is_hide=0`, `delete_time=0`
- image URL and non-empty alt rules
- mobile has no `target="_blank"`
- no unsafe bulk `uk-cover` usage
- PC and mobile screenshots saved
- AI visual analysis on screenshots
- DOM/Puppeteer extraction used to verify or reject AI hallucinations
- similarity check to avoid copying demo_xz01 or a corpus template too closely

## Output Contracts

Dev output:

- generated file list
- implementation summary
- self-check notes
- paths under the authorized generated/run directory

Renderer output:

- deploy log
- rendered HTML/DOM snapshots
- screenshot paths

Test output:

- validation report JSON
- final report Markdown
- issue list or pass conclusion
- repair-task JSON when failed

Rule output:

- compliance audit
- durable-rule deltas if any
- confirmation that no flow steps were skipped

Main output:

- starts with the required 10-column table in OpenClaw/xz01 context
- short final status and next action/result
