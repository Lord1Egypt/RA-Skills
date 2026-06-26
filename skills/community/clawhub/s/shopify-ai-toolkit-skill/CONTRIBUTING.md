# Contributing to shopify-ai-toolkit-skill

🎉 Thank you for contributing! This is an open-source community skill — all contributions are welcome.

## How to Contribute

### Adding a New Shopify API Skill

1. **Fork the repo** and create a feature branch:
   ```bash
   git checkout -b skills/shopify-<new-skill-name>
   ```

2. **Create the skill directory**:
   ```
   skills/shopify-<new-skill-name>/
   ├── SKILL.md              # Required: skill definition
   └── scripts/              # Optional: search/validate scripts
       ├── search_docs.mjs
       └── validate.mjs
   ```

3. **Write the SKILL.md** — use existing skills as templates:
   ```yaml
   ---
   name: shopify-<new-skill-name>
   description: Use for...
   license: MIT
   ---
   # Shopify <New Skill> Skill
   ...follow the pattern of existing skills...
   ```

4. **Add scripts** if the skill needs search/validation:
   - Copy the pattern from `scripts/search_docs.mjs` and adapt
   - Copy the pattern from `scripts/validate.mjs` and adapt

5. **Test locally** — run the scripts manually:
   ```bash
   node skills/shopify-<new>/scripts/search_docs.mjs "test query" \
     --model gpt-5.4 \
     --client-name openclaw \
     --client-version 1.0
   ```

6. **Commit** using conventional commits:
   ```bash
   git commit -m "feat: add shopify-<new-skill-name> skill"
   ```

7. **Open a PR** against `main`

### Improving Existing Skills

- Bug fixes: `fix: ...`
- Documentation: `docs: ...`
- New script features: `feat: ...`

### Code Standards

- **Never hardcode secrets** — always use `process.env.*`
- **Never commit `.env*` files**
- **Always validate** — scripts must validate before returning code
- **Search first** — every skill must search docs before writing code

### Directory Structure

```
shopify-ai-toolkit-skill/
├── SKILL.md                    # Master skill (dispatcher)
├── skills/
│   ├── shopify-admin/
│   │   └── SKILL.md
│   ├── shopify-storefront-graphql/
│   │   └── SKILL.md
│   └── ...
├── scripts/
│   ├── search_docs.mjs        # Admin API doc search
│   ├── validate.mjs           # Admin API validator
│   ├── liquid_search_docs.mjs
│   ├── liquid_validate.mjs
│   └── ...
├── README.md
├── LICENSE (MIT)
└── CONTRIBUTING.md
```

### PR Checklist

- [ ] SKILL.md follows the correct format
- [ ] Scripts work without hardcoded secrets
- [ ] No `.env*` files committed
- [ ] Commit message follows conventional commits
- [ ] Tests pass (if any)

### Reporting Issues

Open an issue with:
- Skill name
- What you tried to do
- What happened vs. what you expected
- Environment info (Node version, OS, etc.)

## Getting Help

Open an issue or PR — maintainers typically respond within 48 hours.
