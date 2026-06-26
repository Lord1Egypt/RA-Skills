**Skill**: [Chezmoi Workflows](../SKILL.md)

## Configuration Reference

`~/.config/chezmoi/chezmoi.toml`:

```toml
[edit]
command = "hx"            # Your preferred editor (vim, nvim, code, etc.)
apply = false             # Manual apply after review

[git]
autoadd = true            # Auto-stage changes on chezmoi add
autocommit = true         # Auto-commit on add/apply
autopush = false          # Manual push for review before sync

[add]
secrets = "error"         # Fail-fast on detected secrets
```

**Key Settings**:

| Setting      | Value     | Effect                                                 |
| ------------ | --------- | ------------------------------------------------------ |
| `autocommit` | `true`    | Automatic commits on `chezmoi add` and `chezmoi apply` |
| `autopush`   | `false`   | Manual push allows review before remote sync           |
| `secrets`    | `"error"` | Fail-fast on detected secrets (recommended)            |

---

## Template Handling

Files ending in `.tmpl` in source directory are Go templates.

### 1. Identify Template

```bash
/usr/bin/env bash << 'CONFIGURATION_SCRIPT_EOF'
ls "$(chezmoi source-path)/dot_zshrc.tmpl" 2>/dev/null && echo "Is template"
CONFIGURATION_SCRIPT_EOF
```

### 2. Edit Template

```bash
chezmoi edit ~/.zshrc
```

Or edit source file directly in `$(chezmoi source-path)/`.

### 3. Test Rendering

```bash
/usr/bin/env bash << 'CONFIGURATION_SCRIPT_EOF_2'
chezmoi execute-template < "$(chezmoi source-path)/dot_zshrc.tmpl"
CONFIGURATION_SCRIPT_EOF_2
```

### 4. Apply to Home

```bash
chezmoi apply ~/.zshrc
```

### 5. Commit and Push

```bash
chezmoi git -- add dot_zshrc.tmpl
chezmoi git -- commit -m "Update zshrc template"
chezmoi git -- push
```

---

## Template Variables

Built-in variables available in `.tmpl` files:

| Variable            | Example Value                 | Description         |
| ------------------- | ----------------------------- | ------------------- |
| `.chezmoi.os`       | `darwin`, `linux`             | Operating system    |
| `.chezmoi.arch`     | `arm64`, `amd64`              | CPU architecture    |
| `.chezmoi.homeDir`  | `/Users/user` or `/home/user` | Home directory path |
| `.chezmoi.hostname` | `macbook`                     | Machine hostname    |
| `.chezmoi.username` | `user`                        | Current username    |

Custom variables from `[data]` section:

```toml
[data]
[data.git]
  name = "Your Name"
  email = "you@example.com"
```

Access in templates: `{{ .data.git.name }}`, `{{ .data.git.email }}`

---

## Conditional Templates

OS-specific configuration:

```go-template
{{ if eq .chezmoi.os "darwin" -}}
# macOS-specific config
export HOMEBREW_PREFIX="/opt/homebrew"
{{ else if eq .chezmoi.os "linux" -}}
# Linux-specific config
export HOMEBREW_PREFIX="/home/linuxbrew/.linuxbrew"
{{ end -}}
```

Architecture-specific:

```go-template
{{ if eq .chezmoi.arch "arm64" -}}
# ARM64 config
{{ end -}}
```
