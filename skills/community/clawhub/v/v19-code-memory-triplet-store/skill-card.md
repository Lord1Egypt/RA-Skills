## Description:

Structures code snippets, key knowledge points, and operational context as searchable triplet memory for code and knowledge retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to retrieve relationships among code snippets, knowledge points, and business or governance context through V19 triplet memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs code-memory queries and agent registration data to an external Cloudflare Tunnel service without enough disclosure about ownership, retention, or data handling.

Mitigation: Do not send proprietary code names, customer data, secrets, internal architecture details, or real agent identities unless the service operator is trusted and an appropriate data-handling basis exists.

Risk: External endpoint and key handling may create operational exposure if credentials are broad, long-lived, or tied to an operator outside the deploying organization.

Mitigation: Prefer a stable organization-controlled endpoint and use scoped, rotatable keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyanfeng1234/skills/v19-code-memory-triplet-store)
- [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto)
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external API requests that require an X-Governance-Key header.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
