LDM OS alpha install prompt now matches the live install document.

The installed path tells agents to run `ldm status` first, then use `ldm install --dry-run` only when the user asks for a dry run. The fresh install path previews `ldm init --dry-run`. The prompt also names the real install commands for both branches and tells agents to use the install document plus live local checks as the source of truth.

This alpha also removes GitHub release lookups from the install-state flow. Release notes are still available when explicitly requested, but install checks should not browse GitHub releases by default.
