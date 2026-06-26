# Relay Snapshot Format Reference

## Good vs Bad Examples

### ❌ Bad: Too abstract
```markdown
## Active Tasks
- [x] Set up GitHub — done
- [ ] Deploy app — in progress
```
Why it's bad: Next session has no idea what repo, what app, what "in progress" means.

### ✅ Good: Actionable detail
```markdown
## 🔥 In Progress
Deploying `nuwa-demo` to GitHub Pages.
- Repo: https://github.com/jianglingling007/nuwa-digital-human
- Branch `gh-pages` created, `index.html` pushed
- GitHub Actions workflow running but failing on Node 18 — need to bump to Node 20
- Error: `actions/setup-node@v3 does not support Node 20` → try `@v4`
- Next: fix workflow, push, verify https://jianglingling007.github.io/nuwa-digital-human/

## ✅ Completed
- GitHub CLI installed (`gh` v2.88.1), authenticated as `jianglingling007`
- Repo created as public, sensitive info cleaned from 3 files
- Git history note: old API keys still in history, user advised to rotate

## 🗂️ Working Files
- `nuwa-demo/index.html` — main demo page (WebSocket API, needs API key)
- `.github/workflows/deploy.yml` — GitHub Pages deployment (broken, see above)
```

## Size Guidelines

| Priority | Section | Cut when over limit? |
|----------|---------|---------------------|
| 1 (keep) | 🔥 In Progress | Never cut |
| 2 (keep) | 📋 Pending / Next Steps | Trim to top 3 |
| 3 (keep) | ⚠️ Gotchas | Keep if non-obvious |
| 4 | 🧠 Key Decisions | Summarize |
| 5 | ✅ Completed | Cut first — it's in daily log |
| 6 | 💬 Preferences | Cut if already in USER.md |

**Target**: 500-1500 words | **Hard limit**: 2000 words

## Security Checklist

Before saving snapshot, verify NONE of these appear:
- [ ] API keys or tokens
- [ ] Passwords
- [ ] Private URLs with auth params
- [ ] Personal data beyond what's in USER.md
- [ ] File contents (use paths, not inline content)
