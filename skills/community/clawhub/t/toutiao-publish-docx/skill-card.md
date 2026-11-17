## Description:

Publishes articles to the Toutiao creator backend using a provided cookie header or saved session, with support for title, body, images, and fixed-directory DOCX import.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlesliu-sap](https://clawhub.ai/user/charlesliu-sap)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation agents use this skill to prepare or publish Toutiao articles from text, images, or DOCX files. It is intended for accounts the user is authorized to automate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Toutiao cookie headers that can grant account access.

Mitigation: Treat cookie_header as a password-level secret and use only accounts the user is authorized to automate.

Risk: The workflow can publish content to a live public account.

Mitigation: Require a dry run before enabling publish=true and review the prepared article before posting.

Risk: Documented shell-style command templates include user-controlled title, content, cookie, and path values.

Mitigation: Avoid executing generated command strings through a shell with untrusted values; pass values through structured arguments or carefully escaped environment variables.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command examples and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run guidance by default and optional publish=true behavior.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
