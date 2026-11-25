## Description:

An agent skill for configuring and running a business WhatsApp virtual attendant that answers from business knowledge and hands conversations to a person when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turbo-notify](https://clawhub.ai/user/turbo-notify)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners, managers, and operators use this skill to set up and manage a Turbo Notify WhatsApp attendant, prepare customer replies from approved business knowledge, and hand conversations off to a person when needed. The Turbo Notify MCP server must be connected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted contact names may block legitimate replies and leave conversations in handoff.

Mitigation: Review the attendant queue for unexpected handoffs; an authorized administrator can assess and resume affected conversations.

Risk: The security scan did not fully inspect all components and partly analyzed a security-relevant expression in references/privacy.md; its guidance also flags undeclared tool scope.

Mitigation: Before installation, review the connected MCP permissions and the privacy reference, and consider the scan limitations when deciding whether to enable the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/turbo-notify/skills/turbo-notify-virtual-attendant)
- [Project homepage](https://github.com/turbo-notify/agent-skills)

## Skill Output:

**Output Type(s):** [Text, Guidance, API calls, Shell commands, Configuration]

**Output Format:** [Conversational text, JSON tool results, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Customer replies use the configured business knowledge and may be handed off for human review.]

## Skill Version(s):

0.3.0 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
