## Description:

Reads article lists and article bodies from a locally running WeWe RSS service for subscribed WeChat Official Accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agasding](https://clawhub.ai/user/agasding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users with a local WeWe RSS service use this skill to locate subscribed WeChat Official Account articles, retrieve article lists, and extract article bodies as readable plain text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can read local WeWe RSS configuration, subscription database entries, cached article content, and localhost service responses.

Mitigation: Run it only where that local WeWe RSS data is intended to be accessible, and review outputs before sharing article content or subscription details.

Risk: The workflow may direct the agent to inspect .env for AUTH_CODE when API requests return 401.

Mitigation: Confirm whether AUTH_CODE exists without printing or pasting it; redact secrets and avoid exposing the full .env file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agasding/skills/wewe-rss-articles)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command and code snippets; extracted article text when the workflow is used by an agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local WeWe RSS API responses and parsed plain text from cached article HTML.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
