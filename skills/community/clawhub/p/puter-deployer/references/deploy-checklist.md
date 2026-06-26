# Puter Deploy Checklist

## Inputs required
- Local project path
- Build command
- Build output directory (e.g. `dist`, `build`, `out`)
- Target Puter app/site identifier
- Expected post-deploy URL

## Standard runbook

1. `cd <project>`
2. `puter whoami`
3. `npm ci` (or project package manager)
4. `npm run build`
5. `test -f <output>/index.html`
6. Deploy with puter-cli (project-specific command)
7. Verify:
   - `curl -I <url>`
   - `curl -s <url> | head`
8. Report:
   - deployed URL
   - timestamp
   - source commit
   - rollback command

## Rollback template

Redeploy prior known-good build artifact:

- Artifact path: `<prev_artifact_dir>`
- Commit: `<prev_commit>`
- Command: `<same deploy command using prev artifact>`
