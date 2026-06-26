# v1.8.2: Clean up release notes after release

RELEASE-NOTES files were piling up in the repo root. `wip-release` consumed them for the GitHub release and CHANGELOG but never cleaned up.

Now after consuming the file, `wip-release` moves all `RELEASE-NOTES-v*.md` files to `_trash/` as part of the version bump commit. We never delete anything.

`deploy-public.sh` also now excludes `_trash/` so these files stay private.
