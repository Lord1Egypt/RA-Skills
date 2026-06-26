# Shopify Theme Deployment

Complete workflow for pushing theme changes to Shopify stores. Includes pre-flight checks, artifact scanning, and post-deployment verification.

## Deployment Workflow

**Order:** Pre-flight → Artifact Scan → Push → Post-Push Verify → Report

If any check fails, **STOP** and report the failure. Never push with known issues.

---

## Step 0: Pre-Flight Checks

Run these checks before pushing to avoid common failures.

### 1. Confirm Target Theme

Read `package.json` scripts for `theme:push` — extract the `--theme` ID.

```bash
grep 'theme:push' package.json
```

**Example:**
```json
{
  "scripts": {
    "theme:push": "shopify theme push --theme 123456789"
  }
}
```

**If no `--theme` flag:** The push targets the **dev theme**. Confirm with the user before proceeding.

**Get theme ID from CLI:**
```bash
shopify theme list
```

Output:
```
 ID           Name            Role
 ───────────  ──────────────  ──────────
 123456789    Development     development
 987654321    Production      live
```

### 2. Check for `.env.local` Token

Verify `SHOPIFY_CLI_THEME_TOKEN` is set in `.env.local`:

```bash
grep SHOPIFY_CLI_THEME_TOKEN .env.local
```

If missing or empty, the push will fail with 401 Unauthorized.

**Generate a new token:**
1. Open Shopify Admin → Apps → Develop apps
2. Create app with `write_themes` scope
3. Copy API token
4. Add to `.env.local`:
   ```
   SHOPIFY_CLI_THEME_TOKEN=shpat_xxxxxxxxxxxxx
   ```

### 3. Check for Conflicting Dev Server

If `shopify theme dev` is running, concurrent pushes can conflict.

Check if port 9292 is in use:

```bash
lsof -i :9292 2>/dev/null | grep LISTEN
```

If running, warn the user to stop the dev server first:

```bash
# Stop dev server (Ctrl+C in the terminal running it)
```

### 4. Git Status

Show uncommitted changes so the user knows what's on disk vs in Git.

```bash
git status --short
```

**Important:** Theme push sends FILES on disk, not Git state. Uncommitted changes **WILL** be pushed.

If there are uncommitted changes:
- Ask user: "You have uncommitted changes. Push anyway?"
- If no, prompt to commit first

---

## Step 1: Artifact Scan

Scan for debug/QA artifacts that shouldn't go to production.

### 1. Block Labels (QA Markers)

```bash
grep -rn 'salmon-block-label\|block-label' snippets/ templates/ sections/ --include='*.liquid' | head -10
```

Block labels are visual QA markers (salmon-colored boxes). Usually should be removed before production.

### 2. Console Logs in JavaScript

```bash
grep -rn 'console\.log' assets/ --include='*.js' | head -10
```

Console logs can leak sensitive data and slow down production code.

### 3. TODO/FIXME/HACK Comments

```bash
grep -rn 'TODO\|FIXME\|HACK' snippets/ templates/ sections/ --include='*.liquid' | head -10
```

These indicate incomplete work. Review before pushing.

### 4. Hardcoded Localhost URLs

```bash
grep -rn 'localhost\|127\.0\.0\.1' snippets/ templates/ sections/ assets/ --include='*.liquid' --include='*.js' | head -5
```

Localhost URLs will break in production.

### Report Findings

Present findings but **don't auto-block**. User decides if these are intentional (e.g., block labels kept for QA on dev theme).

**Example Report:**
```
⚠️ Artifact Scan Results:
  - 3 console.log statements in assets/theme.js
  - 2 TODO comments in sections/product-template.liquid
  - No localhost URLs found

Proceed with push? (y/n)
```

---

## Step 2: Push to Shopify

Use the project's npm script (handles dotenv + theme ID):

```bash
npm run theme:push
```

**If no npm script exists, construct the command:**

```bash
dotenv -e .env.local -- shopify theme push --theme <THEME_ID>
```

### Common Flags

| Flag | Purpose |
|------|---------|
| `--theme <ID>` | Target specific theme (required) |
| `--allow-live` | Allow pushing to live theme (requires confirmation) |
| `--only <glob>` | Push specific files only (e.g., `--only 'snippets/*'`) |
| `--ignore <glob>` | Skip specific files (e.g., `--ignore 'config/settings_data.json'`) |
| `--nodelete` | Don't delete remote files missing locally |

### Pushing to Live Theme

**NEVER** add `--allow-live` without explicit user confirmation.

Confirm with user:
```
🚨 WARNING: You are about to push to the LIVE theme.
This will immediately affect customer-facing pages.

Target theme: Production (ID: 987654321)
Continue? (yes/no)
```

Only proceed if user types `yes` (exact match).

---

## Step 3: Settings Data Warning

`config/settings_data.json` contains merchant-specific theme editor state:
- Section order and visibility
- Customized settings values
- Block configurations

**Pushing this file overwrites merchant customizations.**

**Recommendation:** Always ignore settings_data.json unless intentionally resetting theme editor state:

```bash
npm run theme:push -- --ignore 'config/settings_data.json'
```

**When to push settings_data.json:**
- Fresh theme setup (no merchant customizations yet)
- Intentional reset to default state
- Deploying to a new environment

---

## Step 4: Post-Push Verify

After push completes:

### 1. Check Exit Code

Non-zero exit code = partial failure. Report which files failed.

```bash
if [ $? -ne 0 ]; then
  echo "⚠️ Push completed with errors. Check output above."
fi
```

### 2. Provide Preview URL

Generate preview URL for the target theme:

**Development Theme:**
```
https://your-store.myshopify.com/?preview_theme_id=<THEME_ID>
```

**Live Theme:**
```
https://your-store.myshopify.com
```

**Example:**
```
✅ Push complete!
Preview your changes:
https://example.myshopify.com/?preview_theme_id=123456789
```

### 3. Verify Key Pages

Open these pages in preview mode to verify nothing broke:
- Homepage
- Product page
- Collection page
- Cart

**Automated Check (optional):**
```bash
# Check if theme is accessible (requires curl)
curl -I "https://your-store.myshopify.com/?preview_theme_id=<THEME_ID>" | grep "200 OK"
```

---

## Common Failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| 401 Unauthorized | Token missing/expired in `.env.local` | Regenerate token in Shopify admin → Apps → API credentials |
| 403 Forbidden | Token lacks `write_themes` scope | Recreate token with correct scopes |
| "Theme not found" | Wrong theme ID in `--theme` flag | Run `shopify theme list` to get correct ID |
| Partial sync errors | File too large or invalid Liquid | Check error output for specific files, fix syntax |
| Conflict with dev server | `theme:dev` running concurrently | Stop dev server (`Ctrl+C`), then push |
| `settings_data.json` overwritten | Pushed local config over merchant config | Use `--ignore 'config/settings_data.json'` |
| Files not syncing | Network timeout or API rate limit | Wait 1 minute, retry |

---

## Deployment Report

After successful push, generate a report:

```
✅ Deployment Report
───────────────────────────────────────
Target Theme: Development (ID: 123456789)
Files Pushed: All files (or specific if --only used)
Warnings:
  - 2 console.log statements in assets/theme.js (consider removing)
  - settings_data.json pushed (merchant customizations overwritten)
Preview URL: https://example.myshopify.com/?preview_theme_id=123456789
Next Steps:
  - Test key pages in preview
  - Run performance audit (Lighthouse)
  - Notify stakeholders
```

---

## Rollback Strategy

If the push breaks something:

### 1. Revert to Previous Version

Pull the previous theme version from Git:

```bash
git checkout <previous-commit>
npm run theme:push
```

### 2. Restore from Shopify Backup

Shopify doesn't auto-backup themes. Use Git or manually export before major changes:

```bash
# Export current theme before big changes
shopify theme pull --theme <THEME_ID> --path ./backup-$(date +%Y%m%d)
```

### 3. Rollback Live Theme

If the live theme is broken, publish a previous stable theme:

```bash
shopify theme publish --theme <PREVIOUS_THEME_ID>
```

---

## CI/CD Integration

Automate deployment with GitHub Actions or similar:

**Example `.github/workflows/deploy.yml`:**
```yaml
name: Deploy Theme

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install Shopify CLI
        run: npm install -g @shopify/cli @shopify/theme

      - name: Run Theme Check
        run: shopify theme check

      - name: Deploy to Development
        env:
          SHOPIFY_CLI_THEME_TOKEN: ${{ secrets.SHOPIFY_CLI_THEME_TOKEN }}
        run: shopify theme push --theme ${{ secrets.DEV_THEME_ID }} --ignore 'config/settings_data.json'
```

**Required Secrets:**
- `SHOPIFY_CLI_THEME_TOKEN` — API token with `write_themes` scope
- `DEV_THEME_ID` — Target theme ID

---

## Best Practices

✅ **DO:**
- Always run `shopify theme check` before pushing
- Test in development theme before pushing to live
- Ignore `settings_data.json` unless intentionally resetting
- Use `--nodelete` flag to prevent accidental file deletion
- Commit changes to Git before pushing
- Generate preview URL for QA
- Document what changed in commit messages

❌ **DON'T:**
- Push to live without testing in dev first
- Skip artifact scan (console.logs, TODOs, localhost URLs)
- Push with Theme Check errors
- Use `--allow-live` without explicit confirmation
- Push during high-traffic periods (minimize risk)
- Ignore exit codes (partial failures can break things)

---

**Last Updated:** 2026-03-13
