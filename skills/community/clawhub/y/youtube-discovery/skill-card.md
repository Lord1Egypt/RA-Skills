## Description:

Youtube Discovery lets agents search and inspect public YouTube videos, channels, playlists, comments, categories, languages, and regions through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to research public YouTube content, inspect channel and video metadata, discover trends, review public comments, and prepare structured AgentPMT tool calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube search inputs and identifiers are sent to AgentPMT-hosted services.

Mitigation: Use the skill only for inputs you are comfortable sending to AgentPMT, and keep requests scoped to the minimum public data needed.

Risk: Tool actions can spend the listed credits and depend on account, payment, wallet, or API setup.

Mitigation: Review pricing and companion setup skills before use, prefer trusted or pinned installation paths, and validate the target action before production workflows.

Risk: Credentials, wallet private keys, mnemonics, signatures, payment headers, or account secrets could be exposed if placed in prompts or logs.

Mitigation: Keep secrets out of prompts and logs, and use the setup skills or approved credential handling paths for account and payment configuration.

Risk: Users may expect media downloads, private channel analytics, moderation, upload, or edit capabilities that the skill does not provide.

Mitigation: Limit workflows to public YouTube metadata, comments, playlists, categories, languages, and regions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/youtube-discovery)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/youtube-discovery)
- [Generated Action Schema](./schema.md)

## Skill Output:

**Output Type(s):** [guidance, JSON, API calls, configuration]

**Output Format:** [Markdown instructions with JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public YouTube metadata only; paginated actions fetch one page per call.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
