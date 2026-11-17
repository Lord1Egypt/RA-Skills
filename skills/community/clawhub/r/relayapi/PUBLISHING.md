# Publishing the RelayAPI OpenClaw Skill to ClawHub

## Prerequisites

- Node.js 18+
- A ClawHub account (GitHub account at least 1 week old)
- The `clawhub` CLI installed: `npm install -g clawhub`

> **Note:** The `clawhub publish` command only uploads the specified skill directory contents, so the rest of the monorepo is not exposed.

## Steps

### 1. Authenticate with ClawHub

```bash
clawhub login
```

This opens a browser for GitHub-based authentication. For CI/CD, use token-based auth:

```bash
clawhub login --token <your-token>
```

Verify your identity:

```bash
clawhub whoami
```

### 2. First-time publish

```bash
clawhub publish ./packages/integrations/openclaw \
  --slug relayapi \
  --name "RelayAPI" \
  --version 1.0.0 \
  --changelog "Initial release — unified social media API skill" \
  --tags latest
```

### 3. Subsequent updates

For incremental updates, use `clawhub sync` which auto-detects changes:

```bash
PUBLISH_ROOT="$(mktemp -d)"
cp -R ./packages/integrations/openclaw "$PUBLISH_ROOT/RelayAPI"

clawhub sync \
  --root "$PUBLISH_ROOT/RelayAPI" \
  --bump patch \
  --changelog "Description of changes" \
  --tags latest

rm -rf "$PUBLISH_ROOT"
```

ClawHub derives the slug and display name used by `sync` from the skill directory name. The temporary `RelayAPI` directory produces the `relayapi` slug with the correct product casing; syncing the repository's `openclaw` directory directly would try to use the reserved `openclaw` slug.

Bump options: `patch` (0.0.x), `minor` (0.x.0), `major` (x.0.0).

Preview before publishing:

```bash
PUBLISH_ROOT="$(mktemp -d)"
cp -R ./packages/integrations/openclaw "$PUBLISH_ROOT/RelayAPI"
clawhub sync --root "$PUBLISH_ROOT/RelayAPI" --dry-run
rm -rf "$PUBLISH_ROOT"
```

### 4. CI/CD automation

Add `CLAWHUB_TOKEN` as a GitHub Actions secret, then the workflow at `.github/workflows/publish-integrations.yml` handles publishing automatically on push to `main`.

For non-interactive CI environments, use:

```bash
PUBLISH_ROOT="$(mktemp -d)"
cp -R ./packages/integrations/openclaw "$PUBLISH_ROOT/RelayAPI"
clawhub --no-input sync --root "$PUBLISH_ROOT/RelayAPI" --all --bump patch --tags latest
rm -rf "$PUBLISH_ROOT"
```

### 5. Verify publication

```bash
clawhub search relayapi
```

Or visit https://clawhub.com and search for "relayapi".

### 6. Managing the skill

```bash
# Delete (soft-delete, recoverable)
clawhub delete relayapi --yes

# Restore
clawhub undelete relayapi --yes

# Transfer ownership
clawhub transfer
```

## Important Notes

- Skills are typically listed within 24-48 hours after first publish
- The review checks for complete metadata, clear instructions, and basic quality
- All published skills use the MIT-0 license
- Slug must match: `^[a-z0-9][a-z0-9-]*$`
- Keep the `version` field in `SKILL.md` frontmatter in sync with published versions
