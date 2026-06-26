# Review Closeout

Use this after normal build/test/browser/playtest proof when the user opted in.

## Startup Consent

AutoReview and ClawPatch are optional debug tools, not idea-selection tools.

- AutoReview: structured code review helper from OpenClaw agent-skills, https://github.com/openclaw/agent-skills/tree/main/skills/autoreview, credited to OpenClaw agent-skills.
- ClawPatch: npm `clawpatch` automated code review/fix CLI, https://www.npmjs.com/package/clawpatch. npm metadata has listed maintainer `steipete`; refresh npm metadata before install and use the refreshed metadata as current truth.

If the tool is missing and installs are not approved, record the skipped tool in `context.md`.

## Order

1. Run normal proof first.
2. Run opted-in AutoReview if available.
3. Verify each finding in source before fixing.
4. Fix accepted findings inside the generated project.
5. Rerun proof.
6. Run opted-in ClawPatch if available.
7. Verify each ClawPatch finding before fixing.
8. Fix manually, or run `clawpatch fix` inside an enforced project-only write boundary.
9. Rerun proof and review until clean, rejected with reasons, or blocked by the unattended budget.

## AutoReview

Use an isolated git repo rooted at the generated project when needed:

```bash
git init
git add -N .
<autoreview-helper> --mode local
```

Commits require a user request.

## ClawPatch

Check the installed CLI help before assuming command flags. Prefer the installed command surface.

Typical flow:

```bash
clawpatch init
clawpatch map --source auto
clawpatch review --json
clawpatch report --json
clawpatch next --json
```

If `next` is not available, use `report --json` or `show` to inspect findings. If `--reasoning-effort` is available and useful, it may be used.

Run `clawpatch fix` when writes are already contained to the generated project. In broader write scopes, treat ClawPatch as review-only and have the main agent apply fixes manually.
