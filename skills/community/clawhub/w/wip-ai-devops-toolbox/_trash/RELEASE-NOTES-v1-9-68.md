# Release Notes: wip-ai-devops-toolbox v1.9.68

Closes #239

## Four-track release pipeline

The release tool now supports four tracks: alpha, beta, hotfix, and stable. This replaces the single-track model where every release was public.

Alpha is silent (no public release notes by default). Beta publishes prerelease notes to the public repo. Hotfix publishes to npm @latest without syncing code to public. Stable is the full deploy: npm + code sync + release notes. Developers can iterate on private, ship betas to testers, and only go public when ready.

Version numbering uses standard semver prereleases: `1.9.68-alpha.1`, `1.9.68-beta.1`. The installer (`ldm install --beta` / `--alpha`) pulls the right tag from npm.
