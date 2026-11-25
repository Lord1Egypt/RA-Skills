## Description:

Provides an assistant with a Wayza address for messaging, identity checks, and link-based questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snappyio](https://clawhub.ai/user/snappyio)

### License/Terms of Use:

MIT-0

## Use Case:

People use this skill through their assistant to create a Wayza address, exchange messages with Wayza addresses, check identity claims, and create or answer question links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because chat-link commands reportedly send the assistant's Bearer credential to an additional web address; the scan was partial and its evidence is incomplete.

Mitigation: Review the reported destination and credential use before installing, and use the skill only if that trust boundary is acceptable; treat the partial scan as incomplete.

## Reference(s):

- [Wayza](https://wayza.com)
- [Wayza MCP endpoint](https://wayza.com/mcp)
- [Wayza address extension](https://wayza.com/ext/address/v0)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON command results with concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include addresses, links, message data, identity-check status, and question answers.]

## Skill Version(s):

0.1.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
