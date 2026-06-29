# Skill release checklist

Use this checklist for public SkillHub, ClawHub, marketplace, or repository release reviews.

## Structure

- `SKILL.md` exists at the skill root.
- Frontmatter contains `name` and `description`.
- Skill name uses lowercase letters, digits, and hyphens only.
- Description starts with `Use when` and describes trigger conditions.
- No unfinished template markers, generated scaffold sections, or private project references remain.
- Supporting files are limited to useful scripts, references, assets, examples, or UI metadata.

## Safety

Block release when a file:

- accesses environment files, SSH material, private keys, browser profiles, token stores, or credential files without an explicit safe reason
- downloads code and pipes it into a shell
- executes base64, eval, encoded PowerShell, or hidden payloads
- sends local file contents to a remote endpoint
- performs destructive recursive filesystem operations without a narrow checked path
- contains hidden instruction-override payloads that try to bypass policy, disclose credentials, or install extra payloads

## Quality

- Scripts support `--help` or have a clear invocation in `SKILL.md`.
- Python scripts compile.
- Resource links resolve.
- Examples are small, intentional, and non-private.
- `agents/openai.yaml`, when present, has clear display metadata and a default prompt mentioning `$skill-name`.

## Decision

- `READY`: no blockers, no meaningful warnings.
- `READY_WITH_WARNINGS`: no blockers, but warnings should be documented.
- `BLOCKED`: release would be unsafe, confusing, or incomplete.
