## Description:

Uses a cookie or saved session to publish articles to the Toutiao creator backend, with support for title, body, images, and fixed-directory docx import.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlesliu-sap](https://clawhub.ai/user/charlesliu-sap)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and automation agents use this skill to prepare or publish Toutiao articles from text, images, or a docx file. It is intended for workflows where the user supplies account session access and wants controlled article posting through the Toutiao backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act as a logged-in Toutiao account and may publish content if configured to do so.

Mitigation: Install only in trusted environments, keep publishing disabled unless intentional, and review generated commands before execution.

Risk: The skill handles cookie_header values that are password-equivalent account secrets.

Mitigation: Use a protected secret channel, avoid placing cookies in ordinary prompts or logs, and rotate the session if exposure is suspected.

Risk: Text-substituted shell commands can expose secrets or run with unintended arguments.

Mitigation: Execute commands with structured arguments and verify title, content, image paths, docx wait time, and publish flags before running.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command examples that use account cookies or saved sessions; review secret handling before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
