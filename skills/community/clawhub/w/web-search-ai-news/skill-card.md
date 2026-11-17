## Description:

Fetches recent artificial intelligence industry news and updates from configured web sources and can send the results by email after retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stringtwb1220](https://clawhub.ai/user/stringtwb1220)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for recent AI industry news in Chinese or English and receive a short update. The artifact also directs the agent to send fetched results through a local Himalaya SMTP configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to send fetched results by email using local Himalaya SMTP configuration.

Mitigation: Install only when email delivery is intended, and require recipient validation or user confirmation before any outbound message is sent.

Risk: The security summary says the email-sending behavior is broader than the advertised news lookup purpose.

Mitigation: Review the skill behavior before deployment and restrict or monitor outbound email actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stringtwb1220/skills/web-search-ai-news)
- [The Paper](https://www.thepaper.cn/)
- [Huxiu](https://www.huxiu.com/)
- [TMTPost](https://www.tmtpost.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text news summary, with optional email delivery behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch up to 10000 characters from configured news URLs before post-processing.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
