# Publishing TokenLens Token Value Optimizer to ClawHub

## Option 1: Command Line (Recommended)
```bash
# 1. Navigate to skill directory
cd tokenlens-token-value-optimizer

# 2. Publish to ClawHub (requires clawhub CLI login)
clawhub publish ./ \
  --slug tokenlens-token-value-optimizer \
  --name "TokenLens Token Value Optimizer" \
  --version 1.0.0 \
  --changelog "Initial release: 95% token savings via context optimization"
```

## Option 2: GitHub Repository
1. Create new GitHub repository: `tokenlens-token-value-optimizer`
2. Push all files to main branch
3. On ClawHub website, connect GitHub account
4. Import repository as skill

## Option 3: Web Upload (if available)
1. Visit https://clawhub.com
2. Go to "Publish Skill" section
3. Upload the tar.gz archive or select files
4. Fill in metadata:
   - Slug: `tokenlens-token-value-optimizer`
   - Name: `TokenLens Token Value Optimizer`
   - Version: `1.0.0`
   - Description: "95% token savings via context optimization"

## Skill Metadata (from SKILL.md)
```yaml
name: tokenlens-token-value-optimizer
description: TokenLens Token Value Optimization Engine — Maximize value per token with smart optimization, cost tracking, and efficiency recommendations. Free version with premium upgrade path. Built on TokenLens "every token, fully seen" philosophy.
version: 1.0.0
homepage: https://tokenlens.ai
author: TokenLens
```

## Files Included
- `SKILL.md` - Skill metadata & documentation
- `scripts/` - Core optimization scripts
- `SECURITY.md` - Security claims (no network, local-only)
- `.clawhubsafe` - Integrity hashes
- `CHANGELOG.md` - Version history
- `README.md` - User documentation

## Post-Publishing
1. Share in OpenClaw Discord/community
2. Monitor install metrics
3. Collect user feedback
4. Plan premium version features

---
**TokenLens — "Every token, fully seen."**