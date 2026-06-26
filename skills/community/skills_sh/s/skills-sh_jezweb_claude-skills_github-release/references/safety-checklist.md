# Safety Checklist

Pre-release safety checks for public repositories.

## Blockers (must pass)

| Check | How | Fail action |
|-------|-----|-------------|
| No secrets in files | `gitleaks detect --no-git --source=.` | Remove secrets, check git history |
| No secrets in git history | `git log -S "sk_" -S "ghp_" -S "PRIVATE KEY"` | BFG Repo-Cleaner |
| LICENSE exists | `ls LICENSE*` | Create MIT or proprietary |
| Remote URL is correct | `git remote -v` | Fix with `git remote set-url` |

## Warnings (should fix)

| Check | How | Recommendation |
|-------|-----|----------------|
| README has Install/Usage/License | `grep -i "## Install\|## Usage" README.md` | Add missing sections |
| .gitignore has essentials | `grep "node_modules\|\.env" .gitignore` | Add missing patterns |
| No personal artifacts | `ls SESSION.md planning/ screenshots/ 2>/dev/null` | Delete or .gitignore |
| Build succeeds | `npm run build` | Fix before release |
| No critical vulnerabilities | `npm audit --audit-level=high` | `npm audit fix` |
| No large files (>1MB) | `find . -size +1M -not -path "*/node_modules/*" -not -path "*/.git/*"` | Git LFS or external storage |

## Common Secret Patterns

| Pattern | Example |
|---------|---------|
| API keys | `sk_live_...`, `ghp_...`, `AKIA...` |
| Tokens | `Bearer eyJ...`, `xoxb-...` |
| Private keys | `-----BEGIN PRIVATE KEY-----` |
| Passwords | `password = "..."`, `DB_PASSWORD=...` |
| Cloudflare | `account_id` in committed wrangler files with real IDs |

## Package.json Fields

For npm packages, verify these fields before publish:

```json
{
  "name": "@scope/package",
  "version": "1.0.0",
  "description": "Clear description",
  "license": "MIT",
  "repository": { "type": "git", "url": "https://github.com/..." },
  "keywords": ["relevant", "terms"]
}
```
