# Session 2026-05-18 — xz01 skill autopublish correction

## Trigger

After the xz01 search-rule correction, the local skill was patched but not published. The user asked why no xz01 skill release appeared.

## Durable lesson

For this user's xz01 workflow, a skill update is not finished when `SKILL.md` is patched locally. The required completion state is a published ClawHub release.

## Required workflow

1. Patch the umbrella skill (`xz01-dev-skill`) rather than creating a narrow one-off skill.
2. Remove contradictory old wording from both `SKILL.md` and any linked `references/*.md`.
3. Bump the skill semver in `SKILL.md`.
4. Ensure `skill.json` exists and has matching `version`, accurate `description`, and relevant tags.
5. Ensure `_meta.json` exists and has matching `version`, accurate `description`, and a changelog/updated timestamp.
6. Verify version consistency before publish.
7. Run:

```bash
clawhub publish /root/.hermes/skills/devops/xz01-dev-skill \
  --version <new-version> \
  --changelog "<actual user-visible change>"
```

8. Do not ask whether to publish. The user's standing rule is automatic publishing after skill edits.
9. Final reply should include the published version and ClawHub publish ID.

## Example from this session

Published:

```text
xz01-dev-skill@1.0.26
ID: k97eb49gvmn023vdmyd6d4ygtx86zcmx
```

Main content of the release: corrected dual-end search semantics from “remove search box” to “render visual-only search styling, but disable functional search by default.”
