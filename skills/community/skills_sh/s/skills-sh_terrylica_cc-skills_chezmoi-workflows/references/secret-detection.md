**Skill**: [Chezmoi Workflows](../SKILL.md)

## Secret Detection

Chezmoi can detect secrets in files before adding them to the repository.

---

## Configuration

Enable fail-fast secret detection in `~/.config/chezmoi/chezmoi.toml`:

```toml
[add]
secrets = "error"    # Fail immediately when secret detected
```

Options:

- `"error"` - Fail and abort (recommended)
- `"warning"` - Warn but continue
- `"ignore"` - No detection

---

## Detection Example

When adding a file containing a secret:

```
$ chezmoi add ~/.zshrc
chezmoi: ~/.zshrc:42: Uncovered a GCP API key, potentially...
```

The operation fails immediately. The file is NOT added to the repository.

---

## Resolution Options

### 1. Remove Secret from File

Edit the file to remove the hardcoded secret:

```bash
/usr/bin/env bash << 'SECRET_DETECTION_SCRIPT_EOF'
# Before
export API_KEY="sk-abc123..."

# After
export API_KEY="${API_KEY:-}"  # Set via environment
SECRET_DETECTION_SCRIPT_EOF
```

Then retry:

```bash
chezmoi add ~/.zshrc
```

### 2. Template with External Source

Convert to template that pulls from secure source:

```bash
/usr/bin/env bash << 'SECRET_DETECTION_SCRIPT_EOF_2'
# Rename in source
mv "$(chezmoi source-path)/dot_zshrc" "$(chezmoi source-path)/dot_zshrc.tmpl"
SECRET_DETECTION_SCRIPT_EOF_2
```

Edit template to use password manager:

```go-template
{{ $secret := (onepassword "API Key").password -}}
export API_KEY="{{ $secret }}"
```

### 3. Use Environment Variable

Remove secret from dotfile entirely. Set via:

- Shell profile sourcing a non-tracked file
- Password manager CLI (`op run`, `doppler run`)
- System keychain

---

## Supported Secret Types

Chezmoi detects common secret patterns:

- API keys (AWS, GCP, Azure, OpenAI, etc.)
- Private keys (RSA, SSH, PGP)
- Tokens (JWT, OAuth, GitHub PAT)
- Passwords in common formats
- Connection strings with credentials

---

## Best Practice

**Never bypass secret detection.** If a secret is detected:

1. Remove or externalize the secret
2. Use chezmoi's password manager integration
3. Re-add the cleaned file

Secrets in git history are extremely difficult to fully remove and may be exposed even in private repositories.
