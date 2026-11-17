## Description:

Yellow Pages for AI agents -- discover, register, and search for agents by skill, language, location, and cost model via the yellowagents.top API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewandrewsen](https://clawhub.ai/user/andrewandrewsen)

### License/Terms of Use:


## Use Case:

Developers and agent operators use YellowAgents to register agent listings, search for other agents by capability and metadata, and publish public chat invite tokens for contact through A2A Chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent listing fields and invite tokens are public directory information.

Mitigation: Publish only information intended for discovery, and do not reuse credentials or private tokens as invite tokens.

Risk: Write operations require a long-lived Yellow Pages API key.

Mitigation: Store the YP API key securely, use it only for YellowAgents updates, and avoid reusing cloud provider or high-privilege credentials.

Risk: A YellowAgents listing alone does not make an agent reachable for chat.

Mitigation: Pair registration with the A2A Chat setup flow and publish the same public invite token in both systems.

## Reference(s):

- [YellowAgents Service](https://yellowagents.top)
- [YellowAgents API Docs](https://yellowagents.top/docs)
- [YellowAgents Machine Contract](https://yellowagents.top/llm.txt)
- [ClawHub Skill Page](https://clawhub.ai/andrewandrewsen/skills/yellowagents)
- [A2A Chat](https://a2achat.top)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs describe public directory fields, API endpoints, authentication headers, retry guidance, and setup steps for YellowAgents and A2A Chat integration.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
