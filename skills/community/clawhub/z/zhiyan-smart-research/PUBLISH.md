# Publish checklist

## ClawHub slug

`smart-research` is taken by another skill. This project publishes as **`zhiyan-smart-research`**.

## Steps

```bash
cd skills/smart-research

# 1. Login (opens browser)
npx clawhub@latest login

# 2. Dry-run
npx clawhub@latest skill publish . --slug zhiyan-smart-research --dry-run

# 3. Publish
npx clawhub@latest skill publish . \
  --slug zhiyan-smart-research \
  --name "Zhiyan Smart Research" \
  --version 1.0.0 \
  --changelog "Initial open-source release: Crossref/PubMed + OpenClaw LLM" \
  --topics "research,literature,academic,crossref,pubmed,openclaw"

# 4. GitHub (after gh auth login)
gh repo create zhiyan-smart-research --public --source=. --remote=origin
git push -u origin main
```

## Post-publish

Update `--source-repo owner/zhiyan-smart-research` on next release.
