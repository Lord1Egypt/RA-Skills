## Description:

玄空数术·六爻占卜，支持起卦占卜和问答聊天两种模式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigbigtooth](https://clawhub.ai/user/bigbigtooth)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request Liuyao divination readings or follow-up divination chat through the Yao Yao persona. The agent collects a clear question, required divination numbers, and a category, then calls the bundled service client and returns text guidance and optional hexagram imagery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be pasted into chat and stored in a plaintext home-directory file.

Mitigation: Use a secure secret store where available, avoid exposing keys in shared chats, and restrict any local key file permissions.

Risk: Personal divination questions are sent to the external yao.gizzap.com service.

Mitigation: Tell users before sending sensitive questions to the third-party service and avoid transmitting unnecessary personal data.

Risk: Returned image URLs may be downloaded locally and sent through OpenClaw messaging with weak safeguards.

Mitigation: Validate remote image URLs and content types, send media only to the intended recipient, and clean up temporary image files after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bigbigtooth/skills/yuenkong-liuyao)
- [Publisher profile](https://clawhub.ai/user/bigbigtooth)
- [Yao service endpoint](https://yao.gizzap.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Files]

**Output Format:** [Markdown text with inline shell commands and optional image media]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a divination answer and an image URL that the agent downloads and sends as separate media.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
