# Changelog

## [1.0.5]

- References: removed zero-width / format characters (U+200B etc.) from bundled `.md` files that triggered false "unicode control" flags.
- `references/HEADLESS_FRONTENDS.md`: replaced a long JWT example string with a redacted placeholder (scanner "base64 block" false positive).
- `SKILL.md`: shorter, policy-neutral wording around gateway tools; version **1.0.5**.
- Maintainer: `scripts/sanitize_shopware_skill_markdown.py` (runs from `regenerate-shopware-skill-references.sh`) to re-strip invisible Unicode after doc exports.

## [1.0.4]

- `SKILL.md`: native YAML `metadata` (no JSON curly-brace block) for stricter security scanners; plain-Markdown note after frontmatter.
- Earlier 1.0.4: multi-line JSON `metadata` (OpenClaw doc style) to reduce false "base64 block" flags.

## [1.0.3]

- `SKILL.md` cleaned up (removed sections not needed for end users).

## [1.0.2]

- Hand-curated 6.7 examples (`SHOPWARE_67_*`), `CODE_GUIDELINES_ESSENTIALS.md`, index and maintainer wiring.

## [1.0.1]

- Metadata, description, and notes on minimal vs extended tool use.
