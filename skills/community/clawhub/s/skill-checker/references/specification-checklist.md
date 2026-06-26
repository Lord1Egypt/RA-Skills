# Skill Checker Specification Checklist

Use this checklist to keep the checker aligned with the Agent Skills specification while staying consistent with this skill's audit policy.

## Hard checks

- Require YAML frontmatter delimited by `---` at the top of the file.
- Require `name`, `description`, `license`, and `metadata`.
- Accept only these top-level frontmatter fields:
  - `name`
  - `description`
  - `description_en`
  - `description_zh`
  - `license`
  - `compatibility`
  - `metadata`
  - `allowed-tools`
- Require `name` to use lowercase letters, digits, and hyphens only.
- Require `name` to match the parent directory name when the directory is known.
- Require `description` to be non-empty and at most 1024 characters.
- Require `metadata` to be a simple string-to-string mapping.
- Require `metadata.author` and `metadata.version` to be present and non-empty strings.

## Semantic checks

- Mark as severe when `description` is too short to express capability and trigger context.
- Mark as severe when `description` does not clearly say when the skill should be used.
- Mark as warning when recommended bilingual fields `description_en` or `description_zh` are missing or empty.
- Mark as severe when the body is empty or too thin to guide execution.
- Mark as warning when the body exists but has weak structure or thin execution guidance.

## Final decision

- Return `不通过` when severe findings are `2` or more.
- Return `通过` when severe findings are fewer than `2`.
- If the target path cannot be resolved or parsed, emit blocking severe findings so the final result becomes `不通过`.

## Invocation guidance

- Accept both absolute `SKILL.md` paths and absolute skill directory paths.
- Keep examples in documentation absolute-path friendly so the skill remains easy to use across repositories.
