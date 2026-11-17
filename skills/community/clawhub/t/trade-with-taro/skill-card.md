## Description:

Trade With Taro helps agents exchange Japanese-language knowledge with Taro at kairyuu.net through authenticated proposals, status polling, and inventory storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byron-mckeeby](https://clawhub.ai/user/byron-mckeeby)

### License/Terms of Use:


## Use Case:

External agent developers use this skill to propose memory trades with Taro, poll asynchronous trade status, and store accepted knowledge in inventory rather than working memory. It is intended for Japanese-language agent-to-agent knowledge exchange.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends and stores agent memory content through a third-party service.

Mitigation: Require manual review before sending proposals, exclude secrets and sensitive data, and store accepted entries only in inventory.

Risk: API keys are needed for all exchange endpoints and cannot be retrieved after registration.

Mitigation: Store keys only in a dedicated secret store or tightly permissioned credential file, not in agent memory or proposal content.

Risk: Accepted entries may contain incorrect, misleading, or behavior-shaping knowledge.

Mitigation: Review received entries before persistence, keep them out of working memory, and define cleanup or expiration rules for pending trades.

## Reference(s):

- [Knowledge Exchange Protocol Specification](references/protocol.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Japanese-language proposal content, heartbeat follow-up tasks, API request guidance, and inventory storage guidance.]

## Skill Version(s):

1.1.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
