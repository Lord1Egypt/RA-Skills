## Description:

TingDong turns WeChat, Zhihu, and general webpage article links into AI-generated podcast audio through the TingDong backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentforge-cyber](https://clawhub.ai/user/agentforge-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they explicitly request an audio or podcast version of an article link. The agent submits the URL, polls task status, and returns the generated audio link when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article content and bearer tokens may be sent over the default unencrypted HTTP endpoint.

Mitigation: Use only non-sensitive links or text, avoid private content, and configure a trusted HTTPS backend before sending bearer tokens.

Risk: The artifact includes a monitoring script outside the normal podcast-generation flow.

Mitigation: Treat the monitor script as an operator utility and review it separately before running.

## Reference(s):

- [TingDong ClawHub release](https://clawhub.ai/agentforge-cyber/skills/tingdong)
- [API documentation](references/api_docs.md)
- [Content source strategy](references/content_sources.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown responses with API request guidance, shell command examples, task status JSON, and generated audio links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asynchronous podcast generation; generated audio is returned as a remote MP3 URL when the backend completes processing.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
