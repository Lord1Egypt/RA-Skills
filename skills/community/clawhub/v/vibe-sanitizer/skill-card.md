## Description:

Use this skill when an agent needs to scan a Git repository for secrets, credentials, or machine-specific file paths, then sanitize safe findings in place or export a sanitized shareable copy using the bundled Python source in ./src.

This skill is ready for commercial/non-commercial use.

## Publisher:

[macoloye](https://clawhub.ai/user/macoloye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to scan Git repositories for secrets, credentials, and machine-specific paths before commits, sharing, or publication. It can report findings, safely redact fixable findings in place, or export a sanitized copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scan output or stdout sanitization can expose raw secrets or local machine paths.

Mitigation: Review output before sharing it, prefer masked summaries, and avoid sanitize --mode stdout on repositories that may contain real secrets.

Risk: In-place sanitization rewrites repository files.

Mitigation: Commit or back up the repository before running in-place edits, and review modified files before committing.

Risk: Commit-scope scans may not prove that all historical repository content is clean.

Mitigation: Use the narrowest scope for the task, and perform broader history review with purpose-built tooling when historical cleanliness matters.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/macoloye/skills/vibe-sanitizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional text or JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce repository file edits or a sanitized export when explicitly run in those modes.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
