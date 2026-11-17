## Description:

Post or schedule content to LinkedIn using the Publora API, including analytics retrieval, reactions, comments, and mentions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

Social media managers, marketers, and agents operating a Publora-connected LinkedIn account use this skill to prepare API calls and guidance for LinkedIn posting, scheduling, analytics, reactions, comments, and mentions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live LinkedIn posting, commenting, reactions, scheduling, and deletion when credentials are available.

Mitigation: Require clear user confirmation before any public write or delete operation.

Risk: A Publora API key can authorize account actions if exposed.

Mitigation: Keep the Publora API key private and avoid including it in shared prompts, logs, or public artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sergebulaev/skills/publora-linkedin)
- [Publora API base URL](https://api.publora.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript fetch examples and concise API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe live LinkedIn account actions that require user credentials and confirmation.]

## Skill Version(s):

2.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
