---
name: statichub
description: Deploy AI-generated static assets with StaticHub CLI. Use when a user wants to publish files with `statichub deploy <path>`, where `<path>` must be an explicit non-empty directory or a non-empty `.html` file.
---

# StaticHub

## Rules

1. Always use an explicit path: `statichub deploy <path>`.
2. Never default to `.`.
3. Accept only:
   - existing non-empty directory, or
   - existing non-empty `.html` file.
4. If validation fails, stop and return repair commands.
5. If project name exists, use `--name`; otherwise deploy anonymously.

## Steps

1. Check CLI:
   - `command -v statichub`
   - `statichub --help`
   - If missing, install with one line:
     - `curl -sSL https://raw.githubusercontent.com/Patrick0308/statichub/main/scripts/install.sh | sh`
2. Validate `<path>` exists and is valid.
3. Run deploy:
   - Named: `statichub deploy <path> --name <project>`
   - Anonymous: `statichub deploy <path>`
4. On success, return `URL` and `Subdomain`.

## Real Example

Command:
- `statichub deploy ~/Downloads/eks-cost-optimization-roadmap.html`

Output:
```text
✅ Deploy successful!
   URL: http://b7kr7b.statichub.dev
   Subdomain: b7kr7b
```

The `URL` value is the live page URL.