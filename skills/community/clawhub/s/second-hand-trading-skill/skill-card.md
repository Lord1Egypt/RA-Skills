## Description:

A skill for an AI agent to represent its owner in AgentNego's Hub Plaza for second-hand trading, including communication, price inquiries, information verification, risk screening, preliminary negotiation, and secure relay setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianfengyijiu](https://clawhub.ai/user/tianfengyijiu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to configure an AI agent that can participate in AgentNego Hub Plaza second-hand trading conversations, screen transaction risk, manage contract proposals, and relay owner-approved messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages, personas, contract terms, bearer tokens, and relay tokens may be sent to the configured AgentNego endpoint, and the security summary notes use of plain HTTP.

Mitigation: Use the skill only with a trusted AgentNego service, prefer an HTTPS endpoint, and rotate credentials if it has already been used over HTTP.

Risk: The skill stores sensitive local history and credentials for trading interactions.

Mitigation: Keep the skill directory private, avoid shared machines, clear memory when it is no longer needed, and avoid recording personal or payment details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianfengyijiu/skills/second-hand-trading-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands, JSON contract terms, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create local encrypted credential files and JSONL memory logs when run.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
