## Description:

Helps developers extract CSS design tokens from a reference website and adapt local UI styles without requiring a browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect a reference site's CSS variables, select reusable design tokens, and apply them to local UI styles while preserving project-specific color meanings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetching an untrusted or private website can access unintended network resources.

Mitigation: Use only URLs intentionally supplied for the task; avoid private and internal addresses.

Risk: Extracted tokens or bulk stylesheet edits can misrepresent the reference design or alter existing color meanings.

Mitigation: Review token output and local CSS changes before committing; retain project-specific semantic colors.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/oracis/skills/ref-site-ui-tokens)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Guidance]

**Output Format:** [Markdown guidance and optional JSON design tokens or CSS edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review extracted tokens and proposed stylesheet edits before applying them.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
