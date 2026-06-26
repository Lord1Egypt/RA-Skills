# Stop publishing GitHub Packages from private repos

**Date:** 2026-03-16
**Closes:** #53, #143

## What changed

wip-release no longer publishes to GitHub Packages. That step is now handled exclusively by deploy-public.sh, which publishes from the public repo clone.

## Why

Publishing from private repos ties the package to the private repo. The public repo's Packages tab shows "No packages published" even though 23 versions exist. Users can't see the packages where they expect to find them.

deploy-public.sh already has the GitHub Packages publish step (added in v1.9.34). This change removes the duplicate publish from wip-release so there's one path: always from the public repo.

## What still needs to happen

The existing packages on GitHub Packages are still tied to private repos. They need to be deleted from the org packages page (web UI, needs delete:packages scope). Then the next deploy-public.sh run will republish them tied to the public repos.

This affects all repos, not just LDM OS. Every repo with a private/public pair has this issue.
