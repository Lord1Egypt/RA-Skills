---
name: chezmoi-workflows
description: Dotfile backup and sync with chezmoi. TRIGGERS - chezmoi, dotfiles, sync dotfiles, backup configs, cross-machine sync.
allowed-tools: Read, Edit, Bash
---

# Chezmoi Workflows

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## When to Use This Skill

Use this skill when:

- Backing up dotfiles to Git repository
- Syncing configuration files across machines
- Tracking changes to shell configs, editor settings, or other dotfiles
- Managing templated configurations with chezmoi
- Troubleshooting dotfile drift between source and target

## Architecture

| Component  | Location                         | Purpose                               |
| ---------- | -------------------------------- | ------------------------------------- |
| **Source** | `$(chezmoi source-path)`         | Git repository with dotfile templates |
| **Target** | `~/`                             | Home directory (deployed files)       |
| **Remote** | GitHub (private recommended)     | Cross-machine sync and backup         |
| **Config** | `~/.config/chezmoi/chezmoi.toml` | User preferences and settings         |

---

## 1. Status Check

```bash
chezmoi source-path                    # Show source directory
chezmoi git -- remote -v               # Show GitHub remote
chezmoi status                         # Show drift between source and target
chezmoi managed | wc -l                # Count tracked files
```

---

## 2. Track File Changes

After editing a config file, add it to chezmoi:

```bash
chezmoi status                         # 1. Verify file shows as modified
chezmoi diff ~/.zshrc                  # 2. Review changes
chezmoi add ~/.zshrc                   # 3. Add to source (auto-commits if configured)
chezmoi git -- log -1 --oneline        # 4. Verify commit created
chezmoi git -- push                    # 5. Push to remote
```

---

## 3. Track New File

Add a previously untracked config file:

```bash
chezmoi add ~/.config/app/config.toml  # 1. Add file to source
chezmoi managed | grep app             # 2. Verify in managed list
chezmoi git -- push                    # 3. Push to remote
```

---

## 4. Sync from Remote

Pull changes from GitHub and apply to home directory:

```bash
chezmoi update                         # 1. Pull + apply (single command)
chezmoi verify                         # 2. Verify all files match source
chezmoi status                         # 3. Confirm no drift
```

---

## 5. Push All Changes

Bulk sync all modified tracked files to remote:

```bash
chezmoi status                         # 1. Review all drift
chezmoi re-add                         # 2. Re-add all managed files (auto-commits)
chezmoi git -- push                    # 3. Push to remote
```

---

## 6. First-Time Setup

### Install chezmoi

```bash
brew install chezmoi                   # macOS
```

### Initialize (fresh start)

```bash
/usr/bin/env bash << 'CONFIG_EOF'
chezmoi init                           # Create empty source
chezmoi add ~/.zshrc ~/.gitconfig      # Add first files
gh repo create dotfiles --private --source="$(chezmoi source-path)" --push
CONFIG_EOF
```

### Initialize (clone existing)

```bash
chezmoi init git@github.com:<user>/dotfiles.git
chezmoi apply                          # Deploy to home directory
```

---

## 7. Configure Source Directory

Move source to custom location (e.g., for multi-account SSH):

```bash
/usr/bin/env bash << 'SKILL_SCRIPT_EOF'
mv "$(chezmoi source-path)" ~/path/to/dotfiles
SKILL_SCRIPT_EOF
```

Edit `~/.config/chezmoi/chezmoi.toml`:

```toml
sourceDir = "~/path/to/dotfiles"
```

Verify:

```bash
chezmoi source-path                    # Should show new location
```

---

## 8. Change Remote

Switch to different GitHub account or repository:

```bash
chezmoi git -- remote -v                                              # View current
chezmoi git -- remote set-url origin git@github.com:<user>/<repo>.git # Change
chezmoi git -- push -u origin main                                    # Push to new remote
```

---

## 9. Resolve Merge Conflicts

```bash
/usr/bin/env bash << 'GIT_EOF'
chezmoi git -- status                  # 1. Identify conflicted files
chezmoi git -- diff                    # 2. Review conflicts
# Manually edit files in $(chezmoi source-path)
chezmoi git -- add <resolved-files>    # 3. Stage resolved files
chezmoi git -- commit -m "Resolve merge conflict"
chezmoi apply                          # 4. Apply to home directory
chezmoi git -- push                    # 5. Push resolution
GIT_EOF
```

---

## 10. Validation (SLO)

After major operations, verify system state:

```bash
chezmoi verify                         # Exit 0 = all files match source
chezmoi diff                           # Empty = no drift
chezmoi managed                        # Lists all tracked files
chezmoi git -- log --oneline -3        # Recent commit history
```

---

## 11. Forget (Untrack) a File

Stop tracking a file without deleting it from home directory:

```bash
chezmoi managed | grep config.local     # 1. Confirm file is tracked
chezmoi forget --force ~/.config/app/config.local.toml  # 2. Remove from source (--force skips TTY prompt)
chezmoi git -- push                     # 3. Push removal to remote
ls ~/.config/app/config.local.toml      # 4. Verify file still exists in home
```

**When to use**: Machine-specific configs, files with secrets that shouldn't be synced, files accidentally added.

---

## 12. Template Management

Create OS/architecture-conditional configs using Go templates:

### Convert existing file to template

```bash
chezmoi add --template ~/.config/app/config.toml  # 1. Add as template (creates .tmpl suffix in source)
chezmoi edit ~/.config/app/config.toml             # 2. Edit template in $EDITOR (helix)
chezmoi diff ~/.config/app/config.toml             # 3. Preview what would change
chezmoi apply ~/.config/app/config.toml            # 4. Apply rendered template to home
```

### Common template patterns

```
# OS-conditional block
{{ if eq .chezmoi.os "darwin" -}}
export HOMEBREW_PREFIX="/opt/homebrew"
{{ else if eq .chezmoi.os "linux" -}}
export HOMEBREW_PREFIX="/home/linuxbrew/.linuxbrew"
{{ end -}}

# Architecture-conditional
{{ if eq .chezmoi.arch "arm64" -}}
ARCH="aarch64"
{{ else -}}
ARCH="x86_64"
{{ end -}}

# Custom data from chezmoi.toml [data] section
git_name = "{{ .git.name }}"
git_email = "{{ .git.email }}"

# 1Password secret (requires op CLI)
api_key = {{ onepasswordRead "op://Vault/Item/Field" }}
```

### Verify template renders correctly

```bash
chezmoi execute-template < "$(chezmoi source-path)/dot_config/app/config.toml.tmpl"
chezmoi cat ~/.config/app/config.toml   # Show rendered output without applying
```

---

## 13. Safe Update (Diff Before Apply)

Pull from remote with review step — safer than blind `chezmoi update`:

```bash
chezmoi git -- pull                    # 1. Pull source changes only (no apply)
chezmoi diff                           # 2. Review what WOULD change in home directory
chezmoi apply --dry-run --verbose      # 3. Dry run — shows actions without executing
chezmoi apply                          # 4. Apply after review
chezmoi status                         # 5. Confirm clean state
```

**When to use**: When pulling changes made on another machine, or after a long gap between syncs. Avoids surprise overwrites of local edits.

---

## 14. Doctor (Diagnostic)

Troubleshoot chezmoi setup and environment:

```bash
chezmoi doctor                         # Full diagnostic — checks all components
```

**Key fields to verify**:

| Check        | Expected                                       | Meaning if failing                 |
| ------------ | ---------------------------------------------- | ---------------------------------- |
| config-file  | `found ~/.config/chezmoi/chezmoi.toml`         | Config missing or wrong path       |
| source-dir   | `~/own/dotfiles is a git working tree (clean)` | Source dirty or not a git repo     |
| git-command  | `found /opt/homebrew/bin/git`                  | Git not installed                  |
| edit-command | `found /opt/homebrew/bin/hx`                   | Editor not configured              |
| 1password    | `found /opt/homebrew/bin/op`                   | 1Password CLI needed for templates |
| age/gpg      | `info` = optional                              | Only needed for encrypted files    |

```bash
chezmoi doctor | grep -v "^ok"         # Show only warnings and errors
```

---

## Reference

- [Setup Guide](./references/setup.md) - Installation, multi-account GitHub, migration
- [Prompt Patterns](./references/prompt-patterns.md) - Detailed workflow examples
- [Configuration](./references/configuration.md) - chezmoi.toml settings, templates
- [Secret Detection](./references/secret-detection.md) - Handling detected secrets

**Chezmoi docs**: <https://www.chezmoi.io/reference/>

---

## Troubleshooting

| Issue              | Cause                      | Solution                                       |
| ------------------ | -------------------------- | ---------------------------------------------- |
| chezmoi not found  | Not installed              | Install via `brew install chezmoi`             |
| Source path empty  | Not initialized            | Run `chezmoi init`                             |
| Git remote not set | Missing GitHub repo        | Run `chezmoi git -- remote add origin URL`     |
| Apply fails        | Template error             | Check template syntax with `chezmoi diff`      |
| Merge conflicts    | Diverged source and target | Use `chezmoi merge` to resolve                 |
| Secrets detected   | Plain text credentials     | Use chezmoi templates with 1Password/Doppler   |
| forget needs TTY   | Interactive confirmation   | Use `chezmoi forget --force <path>`            |
| Template not found | Missing `.tmpl` suffix     | Use `chezmoi add --template` to create `.tmpl` |


## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
