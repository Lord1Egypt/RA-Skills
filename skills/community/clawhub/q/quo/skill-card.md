## Description:

Helps agents access a connected Quo business phone account to manage calls, messages, contacts, and conversations through Maton.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Business phone users and their agents can retrieve calls, messages, contacts, recordings, and transcripts, and perform approved Quo actions or set up optional automations through Maton.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting Maton to Quo can expose business phone records and account data.

Mitigation: Approve only needed connections and scopes; prefer OAuth through the CLI over raw API keys.

Risk: Write actions, hosted functions, and triggers can send messages or process ongoing event data.

Mitigation: Review the target and behavior, and obtain explicit approval before writes or unattended automations.

Risk: Webhook or destination configuration can disclose records or event data to other hosts.

Mitigation: Use third-party destinations only when the host is trusted and the user understands what data will be shared.

## Reference(s):

- [Quo skill on ClawHub](https://clawhub.ai/byungkyu/skills/quo)
- [Maton homepage](https://maton.ai)
- [Quo API introduction](https://www.quo.com/docs/mdx/api-reference/introduction)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance, CLI commands, and summarized API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may contain sensitive phone records, messages, contacts, or recordings.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
