## Description:

Analyzes YouTube channels and videos through YTAPI to explain breakouts, growth, and viral performance, then distills findings into a reusable playbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ytapi](https://clawhub.ai/user/ytapi)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and channel operators use this skill to study YouTube channel and video performance, understand competitor patterns, and turn findings into a reusable video playbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may save an API key for future sessions without clearly explaining or obtaining approval for that lasting access.

Mitigation: Prefer an existing connector or agree on a protected secrets store before saving a key; keep temporary credential files private and remove them.

Risk: Account setup sends an email address and verification code to YTAPI, and analysis uses API credits.

Mitigation: Review the signup details with the user and confirm expected credit use before starting analysis.

## Reference(s):

- [YTAPI documentation](https://docs.ytapi.dev)
- [YTAPI](https://ytapi.dev)
- [Authentication setup](references/auth-setup.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Files]

**Output Format:** [Markdown analysis and a reusable SKILL.md playbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public YouTube data snapshots; private channel analytics such as retention, traffic sources, and revenue are not available.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
