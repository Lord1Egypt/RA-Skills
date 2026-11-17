# Supervised actions

These are operator-approved procedures, not automatic executor features.

## Preconditions

Read applicable project instructions and runtime/deployment documentation. Acquire the dedicated exclusive run marker; preserve any pre-existing marker. Confirm branch, HEAD, upstream, index/worktree status, processes, Git locks, and interrupted operations immediately before each action. Any concurrent change aborts that action.

## ORGANIZE_SAFE

For worktree registration pruning:
- Prove the directory is genuinely absent, not an unavailable mount or inaccessible path.
- Confirm the registration is prunable, unlocked, and has no related activity.
- Preserve administrative metadata and the complete `git worktree prune --dry-run` output.
- Verify every record that a subsequent prune would affect; never assume the command targets one record.
- Run the authorized prune only after backup validation, then inspect registrations again.

For fast-forward:
- Confirm a clean canonical non-runtime source checkout, including no relevant untracked files.
- Confirm unambiguous branch/upstream, successful current fetch, no local commits or divergence, no operations/locks/processes, and no build/deploy/restart/migration implied by updating files.
- Record old/new commits and recovery instructions.
- Apply only `git merge --ff-only` to the verified upstream; verify the post-state.
- Never use this workflow to update a dirty, active, locked, or runtime checkout.

## PREPARE_CLEANUP and backup

Create a new private directory below the operator's approved backup root. Do not reuse an existing directory. Record:
- Sanitized paths, remotes, branch, HEAD, upstream, and porcelain status.
- Binary working-tree and staged diffs.
- Relevant untracked files preserving paths without following symlinks.
- Administrative metadata and dry-run output for pruning.
- Old/new commits and preconditions for fast-forward.
- Manifest, size, covered targets, action log, and recovery instructions.
- SHA256 checksums, validated before action and updated/validated after modifying the action log.

Do not automatically copy ignored sensitive files, databases, uploads, business media, or giant caches. If required evidence cannot be safely preserved, stop the action and explain the gap. Preparation never removes the target. Backups older than 30 days may be flagged for retention review; the auditor never deletes backups.

After each authorized action, verify the exact expected state before considering another action. Release only the current run's marker. Report failures and concurrent changes instead of applying cascading repairs.
