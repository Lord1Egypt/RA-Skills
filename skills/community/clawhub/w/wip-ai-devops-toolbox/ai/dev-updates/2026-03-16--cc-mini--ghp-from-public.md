# GitHub Packages publish from public repo

**Date:** 2026-03-16
**Closes:** #193

## What changed

`deploy-public.sh` now publishes to GitHub Packages from the public repo clone after the npm publish step. Previously, GitHub Packages were only published from the private repo during `wip-release`, so they showed on the private repo's Packages tab. Users couldn't see them.

Now packages show on the public repo's Packages tab where users expect to find them. Uses `gh auth token` for authentication (already available from the gh CLI).

## Why

The Packages tab on public repos was empty. Users visiting wipcomputer/wip-ldm-os or wipcomputer/wip-ai-devops-toolbox saw no packages even though they were published. The packages existed but were linked to the private repo.
