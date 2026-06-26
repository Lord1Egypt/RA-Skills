# Hermes-native xz01 factory first-run pattern

This reference captures the durable workflow learned from the first Hermes-native xz01 prototype run. It is not a one-off task log; use it as a starter pattern for future xz01 automation work.

## Context

The user corrected that OpenClaw runtime mechanisms (`sessions_send`, `agent:dev:main`, OpenClaw `flow-controller.js`) do not map to Hermes. For Hermes work, OpenClaw is a read-only standards/corpus source. New automation state and generated files belong under Hermes-owned paths.

## Correct first-run approach

When the user asks whether to keep discussing or “直接开发第一套给我看下”, act and produce a small end-to-end prototype rather than only listing caveats.

Recommended minimal first-run sequence:

1. Treat `/root/.openclaw` as read-only reference.
2. Create a Hermes factory run directory, e.g.:
   - `/root/.hermes/workspace/xz01-factory/runs/run-0001/`
   - generated template root: `generated/public/themes/default/`
   - reports: `reports/`
3. Write a minimal `state.json` and `requirement.json` for traceability.
4. Use `delegate_task` for a short dev-worker implementation task, or a long-running explicit `hermes` / `claude` worker if the implementation is large.
5. Generate only into the Hermes factory run directory; do not deploy or overwrite production themes in the prototype step.
6. Run deterministic static validation before reporting.
7. Report what exists, what was validated, and what remains before production deployment.

## Minimal output shape

```text
/root/.hermes/workspace/xz01-factory/runs/run-0001/
├── state.json
├── requirement.json
├── generated/public/themes/default/
│   ├── DEV_SUMMARY.md
│   ├── cms/index.html
│   ├── mobile/index.html
│   └── common_cms/
│       ├── common/_head.html
│       ├── pc/_header.html
│       ├── pc/_footer.html
│       ├── pc/assets/css/style.css
│       ├── pc/assets/js/style.js
│       ├── mobile/_header.html
│       ├── mobile/_footer.html
│       ├── mobile/assets/css/style.css
│       └── mobile/assets/js/style.js
└── reports/basic-validation.json
```

## Static validation checklist for prototype

Before telling the user the prototype is ready, verify at least:

- no writes under `/root/.openclaw`
- no production deploy unless explicitly requested
- no raw PHP template tags (`<?php`, `<?=`, `<?`)
- mobile templates contain no `target` / `_blank`
- no `href="#"`
- no `uk-cover` attributes
- no `limit="0"` / `getAllData({limit: 0})`
- CSS brace counts are balanced
- all `{include file="./themes/default/..."}` targets exist
- referenced local CSS/JS assets exist under the generated template root
- HTML class names used by the prototype have CSS definitions, or intentional exceptions are documented

## Prototype vs production boundary

A prototype-ready result is not production-ready. Before packaging/deployment, continue with:

1. renderer script: deploy to a safe test theme or staging path, clear cache, render PC/mobile
2. screenshot capture for both devices
3. AI visual analysis with DOM/Puppeteer anti-hallucination check
4. data-render verification against real DB/route map
5. repair loop until issues are zero
6. rule review
7. numbered package under `/root/.hermes/workspace/xz01/`

## Reporting preference

For this user, first line must remain the 10-column table for xz01/template status reports. Keep the prose concise and action-oriented; if a safe prototype can be built without production side effects, build it rather than asking whether to proceed.
