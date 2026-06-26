**Skill**: [Chezmoi Workflows](../SKILL.md)

## Command Reference

Quick reference for chezmoi commands with expected outputs.

---

## Status Commands

| Command             | Expected Output                                       |
| ------------------- | ----------------------------------------------------- |
| `chezmoi status`    | `M` modified, `A` added, `D` deleted, empty = in sync |
| `chezmoi diff`      | Unified diff, empty = no changes                      |
| `chezmoi managed`   | List of all tracked files                             |
| `chezmoi verify`    | Exit 0 = success, non-zero = drift detected           |
| `chezmoi unmanaged` | Files in target not tracked by chezmoi                |

---

## Tracking Commands

| Command                   | Effect                                         |
| ------------------------- | ---------------------------------------------- |
| `chezmoi add ~/.zshrc`    | Add file to source, auto-commits if configured |
| `chezmoi re-add`          | Re-add all managed files that changed          |
| `chezmoi forget ~/.zshrc` | Stop tracking file (keeps in home)             |

---

## Sync Commands

| Command                  | Effect                                    |
| ------------------------ | ----------------------------------------- |
| `chezmoi apply`          | Deploy source to home directory           |
| `chezmoi apply ~/.zshrc` | Deploy single file                        |
| `chezmoi update`         | Pull from remote + apply (single command) |

---

## Git Commands

All git operations use `chezmoi git --` prefix for portability:

| Command                           | Effect                    |
| --------------------------------- | ------------------------- |
| `chezmoi git -- status`           | Git status of source repo |
| `chezmoi git -- log --oneline -5` | Recent commits            |
| `chezmoi git -- push`             | Push to remote            |
| `chezmoi git -- pull`             | Pull from remote          |
| `chezmoi git -- remote -v`        | Show configured remotes   |

---

## Workflow: Track Changes

```bash
chezmoi status                    # 1. Check what changed
chezmoi diff ~/.zshrc             # 2. Review diff
chezmoi add ~/.zshrc              # 3. Add (auto-commits)
chezmoi git -- push               # 4. Push to remote
```

## Workflow: Sync from Remote

```bash
chezmoi update                    # 1. Pull + apply
chezmoi verify                    # 2. Verify success
```

## Workflow: Push All Changes

```bash
chezmoi re-add                    # 1. Re-add all managed files
chezmoi git -- push               # 2. Push to remote
```

## Workflow: Resolve Conflicts

```bash
/usr/bin/env bash << 'GIT_EOF'
chezmoi git -- status             # 1. Identify conflicts
# Edit conflicted files in $(chezmoi source-path)
chezmoi git -- add <files>        # 2. Stage resolved
chezmoi git -- commit -m "Resolve conflicts"
chezmoi apply                     # 3. Apply to home
chezmoi git -- push               # 4. Push resolution
GIT_EOF
```

---

## Validation Checklist

After major operations:

```bash
chezmoi verify && echo "OK"       # All files match source
chezmoi diff | head               # No unexpected drift
chezmoi git -- status             # No uncommitted changes
```
