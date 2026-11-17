## Description:

Extracts public x.com and twitter.com tweet content without API credentials by guiding an agent through browser-based capture and structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunhualiao](https://clawhub.ai/user/chunhualiao)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to extract text, author details, timestamps, media links, engagement metrics, and thread context from public x.com or twitter.com status URLs. It can optionally guide media download when the user requests it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags loosely scoped URL and download handling for browser and file-writing actions.

Mitigation: Use only explicit public x.com or twitter.com status URLs, confirm media downloads with the user, and constrain downloads to a controlled output folder.

Risk: Protected, age-restricted, controversial, or login-required tweets may fail or expose incomplete data.

Mitigation: Report inaccessible content clearly and avoid attempts to bypass access controls or credential requirements.

Risk: X.com layout changes can break selectors or produce incomplete extraction.

Mitigation: Check the selector reference and report which fields were successfully extracted when extraction is partial.

## Reference(s):

- [X.com Content Selectors](references/selectors.md)
- [X Extract on ClawHub](https://clawhub.ai/chunhualiao/skills/x-extract)

## Skill Output:

**Output Type(s):** [markdown, shell commands, files, guidance]

**Output Format:** [Structured Markdown with optional shell command snippets and downloaded media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires public tweet URLs and browser tool access; media download writes files only when requested.]

## Skill Version(s):

1.0.0 (source: skill.yml, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
