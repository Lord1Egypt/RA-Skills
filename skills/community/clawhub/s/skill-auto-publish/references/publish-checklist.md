# Publish Checklist

Run through every item before executing `clawhub publish`. Do not skip items.

---

## Identity & Path

- [ ] Target slug is known.
- [ ] Local source path is known.
- [ ] Source path is verified against `references/local-overrides.md` if slug appears there.
- [ ] SKILL.md exists inside the source path.

---

## Content Requirements

- [ ] Title present in SKILL.md frontmatter.
- [ ] Summary present in SKILL.md frontmatter.
- [ ] `## Activation` section exists with trigger phrases.
- [ ] `## Features` section exists.
- [ ] `## What This Will Not Do` or equivalent boundaries section exists.

---

## Secrets & Privacy

- [ ] No private tokens, API keys, secrets, seed phrases, SSH keys.
- [ ] No local-only credentials or bot tokens.
- [ ] No accidental private local paths (e.g., `/root/.ssh/`, `/root/.hermes/secrets/`).
- [ ] No stale draft notes, personal chat fragments, or raw internal comments.
- [ ] No visible HTML comments (`<!-- ... -->`) — ClawHub does not strip these.

---

## Structure

- [ ] No duplicated major H2 sections (two `## Install` headers, etc.).
- [ ] No HTML comments anywhere in the content.
- [ ] No broken section ordering — section sequence matches intended public page order.

---

## Version & Changelog

- [ ] Version is semver-formatted (e.g., `1.2.3`).
- [ ] For updates: current live version is confirmed via `clawhub inspect <slug>`.
- [ ] New version > current live version (or this is a first publish).
- [ ] Changelog is non-empty.
- [ ] Changelog is specific — not "updated", "fixes", "misc", "minor changes".
- [ ] Changelog has 1–2 concrete sentences describing what changed.

---

## Per-Skill Overrides

- [ ] Slug appears in `references/local-overrides.md` → override path is used.
- [ ] waste-audit: canonical path is `/root/.openclaw/skills/waste-audit/`, first section must be `## Features`.
- [ ] buffett-do: canonical path is `/root/.openclaw/skills/buffett-do/`.
- [ ] skill-release-lifecycle: canonical path is `/root/.hermes/skills/workflow-kits/skill-release-lifecycle/`.
- [ ] clawhub-auto-publish: canonical path is `/root/.hermes/skills/workflow-kits/clawhub-auto-publish/`.

---

## Guardian Review

- [ ] If `GUARDIAN REVIEW: required` in request packet → review status is confirmed completed before publishing.
- [ ] If review is not completed → do NOT publish. Return `NEEDS_INFO`.

---

## CLI Help

- [ ] If command format is uncertain → run `clawhub --help` or `clawhub skill publish --help` first.
- [ ] Do not guess command flags. Verify before running.

---

## Hard Rule

**Any failure = do not publish.** Return `NEEDS_INFO` (missing input) or `BLOCKED` (found a problem) with the exact failed checklist item.