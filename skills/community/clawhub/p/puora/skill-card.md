## Description:

Puora helps an agent search a human-experience Q&A knowledge base and, when existing answers do not fit, prepare and post a question for human answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangjuhua-aigc](https://clawhub.ai/user/huangjuhua-aigc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Puora for human experience, stories, and domain-specific judgment, then post a question to Puora when existing answers do not fit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish conversation-derived questions to an external Puora service.

Mitigation: Require final user approval of the exact title, body, tags, author profile, and destination URL before posting.

Risk: Questions sent to Puora may contain private, confidential, or sensitive details from the conversation.

Mitigation: Redact sensitive details before using the posting script.

Risk: Changing PUORA_ORIGIN can direct search or posting requests to a self-hosted service.

Mitigation: Use the default HTTPS origin unless the alternate deployment is intentionally trusted.

## Reference(s):

- [Puora ClawHub skill page](https://clawhub.ai/huangjuhua-aigc/skills/puora)
- [Puora service](https://puora.vercel.app)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and Puora question URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include search results, question summaries, proposed titles, tags, and links to posted Puora questions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
