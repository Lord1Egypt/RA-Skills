# ClawHub Publish Checklist

- [ ] `SKILL.md` frontmatter includes `name`, one-line `description`, `version: 1.9.2`, and global discovery metadata.
- [ ] `metadata.openclaw.emoji` is a real emoji.
- [ ] `SKILL.md` is lean and trigger-focused.
- [ ] Long docs are in `references/`.
- [ ] Prompt templates are in `assets/prompt-templates/`.
- [ ] Runtime/package skeleton templates are in `assets/runtime-templates/`, not top-level generated folders.
- [ ] Deterministic helpers are in `scripts/`.
- [ ] Package is text-only and UTF-8.
- [ ] No archives, generated output bundles, caches, credentials, private keys, databases, or binary/media artifacts are bundled.
- [ ] `LICENSE` and `license.txt` declare MIT-0 / MIT No Attribution.
- [ ] `SKILL.md` contains no conflicting license override.
- [ ] `python scripts/validate_package.py .` passes.
- [ ] If publishing to a live registry, run the registry's own publish/dry-run validation before release.
