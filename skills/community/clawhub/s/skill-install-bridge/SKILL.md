---
name: skill-install-bridge
description: Generate install commands, GitHub README snippets, website cards, and copy text for a published ClawHub or Codex skill.
version: 0.1.0
homepage: https://clawhub.ai/zack-dev-cm/skill-install-bridge
license: MIT
user-invocable: true
metadata: {"openclaw":{"skillKey":"skill-install-bridge","requires":{"anyBins":["python3","python"]}}}
---

# Skill Install Bridge

Use this skill when a builder needs one clean install surface for a published skill.

## When To Use

- A ClawHub skill is published and needs README, landing page, or docs install copy.
- A builder wants one command, one card, and one short explanation users can understand.
- A skill launch needs consistent links across GitHub, X, Substack, and websites.
- A landing page needs a compact install block before the Chrome Web Store or ClawHub link is final.

## Workflow

1. Collect the skill slug, display name, owner handle, version, and public URL.
2. Run the bundled script:

```bash
python3 scripts/install_bridge.py \
  --slug skill-package-doctor \
  --name "Skill Package Doctor" \
  --owner zack-dev-cm \
  --version 0.1.1 \
  --out-dir install-bridge
```

3. Review the generated Markdown, HTML, JSON, and social post text.
4. If you intentionally replace existing snippets, add `--force`.
5. Replace placeholders before publishing. Do not invent install commands.
6. Put the Markdown snippet in GitHub and the HTML card on landing pages.
7. Use the short social text for launch posts or comments.
8. Read `references/source-manifest.json` only when you need package provenance.

## Review Rules

- Keep wording simple enough for a non-technical user.
- Use the real ClawHub CLI command: `npx --yes clawhub@0.9.0 install <slug>`.
- Include a no-install fallback: inspect the skill page and copy the usage prompt.
- Do not claim downloads, stars, ratings, or review status unless provided.
- Keep snippets short, copyable, and safe to paste into GitHub.
- If the slug is missing or invalid, stop and ask for it.
- Refuse accidental overwrites unless the user explicitly chooses `--force`.

## Output

Return:

- install command
- README Markdown snippet path
- landing-page HTML snippet path
- JSON metadata path
- short social launch copy
- missing fields or trust warnings

## Stop Conditions

Do not generate launch-ready install copy when:

- the slug is missing or not slug-shaped
- the URL is not HTTPS
- the version is unknown and the user asks for version-specific copy
- the package has not been published or cannot be inspected
