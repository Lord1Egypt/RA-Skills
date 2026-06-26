**Skill**: [Chezmoi Workflows](../SKILL.md)

## First-Time Setup

### 1. Detect Current State

```bash
command -v chezmoi || echo "NOT INSTALLED"
chezmoi source-path 2>/dev/null || echo "NOT INITIALIZED"
chezmoi git -- remote -v 2>/dev/null || echo "NO REMOTE"
```

### 2. Install

```bash
/usr/bin/env bash << 'SETUP_EOF'
# macOS
brew install chezmoi

# Linux
sh -c "$(curl -fsLS get.chezmoi.io)"
SETUP_EOF
```

### 3. Initialize

**Fresh start:**

```bash
chezmoi init
```

**Clone existing repo:**

```bash
chezmoi init git@github.com:<username>/dotfiles.git
chezmoi apply
```

---

## Remote Configuration

### Create Private Repository

```bash
/usr/bin/env bash << 'GIT_EOF'
# Using gh CLI (recommended)
gh repo create dotfiles --private --source="$(chezmoi source-path)" --push

# Or manually after creating repo on github.com:
chezmoi git -- remote add origin git@github.com:<username>/dotfiles.git
chezmoi git -- push -u origin main
GIT_EOF
```

### Change Remote

```bash
chezmoi git -- remote -v                                               # View current
chezmoi git -- remote set-url origin git@github.com:<username>/<repo>.git
chezmoi git -- push -u origin main
```

---

## Custom Source Directory

Default: `~/.local/share/chezmoi`

To use custom location:

```bash
/usr/bin/env bash << 'VALIDATE_EOF'
# 1. Move existing source
mv "$(chezmoi source-path)" ~/path/to/dotfiles

# 2. Update config
cat >> ~/.config/chezmoi/chezmoi.toml << 'EOF'
sourceDir = "~/path/to/dotfiles"
EOF

# 3. Verify
chezmoi source-path
VALIDATE_EOF
```

---

## Multi-Account SSH

For users with multiple GitHub accounts, configure SSH to select account by directory pattern:

```ssh-config
# ~/.ssh/config

# Default account
Host github.com
    HostName github.com
    IdentityFile ~/.ssh/id_ed25519_default

# Override for specific directory pattern
Match host github.com exec "pwd | grep -qE '/(personal|private)/'"
    IdentityFile ~/.ssh/id_ed25519_personal
```

---

## Recommended Configuration

`~/.config/chezmoi/chezmoi.toml`:

```toml
[edit]
command = "hx"            # Or vim, nvim, code, etc.
apply = false             # Manual apply after review

[git]
autoadd = true            # Auto-stage on chezmoi add
autocommit = true         # Auto-commit on add/apply
autopush = false          # Manual push for review

[add]
encrypt = false           # Set true for age/gpg encryption
secrets = "error"         # Fail-fast on detected secrets

[data]
[data.git]
  name = "Your Name"
  email = "you@example.com"
```

---

## Show Current Setup

```bash
chezmoi source-path
chezmoi git -- remote -v
chezmoi git -- status --short
chezmoi managed | wc -l
cat ~/.config/chezmoi/chezmoi.toml 2>/dev/null || echo "Using defaults"
```

---

## Migration: Change GitHub Account

```bash
# 1. Switch gh CLI account
gh auth switch -u <new-account>

# 2. Create new private repo
gh repo create dotfiles --private

# 3. Update remote
chezmoi git -- remote set-url origin git@github.com:<new-account>/dotfiles.git

# 4. Push history (force required for new empty repo)
chezmoi git -- push -u origin main --force

# 5. (Optional) Delete old repo
gh auth switch -u <old-account>
gh repo delete <old-account>/dotfiles --yes
```

**Note**: Force push is safe here because the new repo is empty. Never force push to a repo with existing history unless intentional.

---

## Troubleshooting

### No remote configured

```bash
chezmoi git -- remote add origin git@github.com:<username>/dotfiles.git
chezmoi git -- push -u origin main
```

### Permission denied (publickey)

```bash
ssh -T git@github.com                  # Check which account is active
```

If wrong account, configure SSH Match directives or use HTTPS:

```bash
chezmoi git -- remote set-url origin https://github.com/<username>/dotfiles.git
```

### Source directory not found

```bash
/usr/bin/env bash << 'CONFIG_EOF'
grep sourceDir ~/.config/chezmoi/chezmoi.toml
ls -la "$(chezmoi source-path)" || echo "Directory missing"
CONFIG_EOF
```
