## Description:

Zoho Desk API integration with managed OAuth. Manage support tickets, track conversations, list departments and agents, handle contacts and organizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Support teams and operators use this skill to work with Zoho Desk from an agent chat, including listing tickets, reading conversations, creating support tickets, and looking up contacts, agents, departments, roles, organizations, and tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to enable an unpinned third-party plugin that handles OAuth-backed Zoho Desk support data.

Mitigation: Install only if you trust ClawLink and the ClawHub plugin source, review OAuth scopes during connection, and use the least-privileged Zoho account available.

Risk: The skill can support write actions such as ticket creation, bulk task updates, and department-logo changes.

Mitigation: Confirm write actions carefully before execution, especially bulk updates and changes that affect department assets.

## Reference(s):

- [Zoho Desk API Documentation](https://www.zoho.com/desk/developer-help/api/)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/zoho-desk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose read or write Zoho Desk tool calls through the ClawLink plugin; write actions should be confirmed before execution.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
