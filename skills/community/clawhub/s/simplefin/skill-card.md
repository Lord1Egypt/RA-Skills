## Description:

Connects to bank accounts and fetches financial transactions via the SimpleFIN API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eladrave](https://clawhub.ai/user/eladrave)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to connect SimpleFIN-backed bank accounts, retrieve balances, review transactions, and track expenses through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive financial balances, transactions, and SimpleFIN access credentials.

Mitigation: Review before installing, avoid exposing full Access URLs in logs or command-line history, and store credentials only in an approved secret store.

Risk: The helper script can turn user-provided SimpleFIN URLs or tokens into shell commands.

Mitigation: Replace shell-based curl calls with a native HTTP client and validate SimpleFIN URLs before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eladrave/skills/simplefin)
- [SimpleFIN Developer Guide](references/developer_guide.md)
- [SimpleFIN Protocol](https://www.simplefin.org/protocol.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Financial account and transaction data should be summarized clearly for the user.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
