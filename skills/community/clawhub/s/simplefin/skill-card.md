## Description: <br>
Connects to bank accounts and fetches balances and transaction history via the SimpleFIN API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eladrave](https://clawhub.ai/user/eladrave) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to connect a SimpleFIN Bridge account, retrieve bank account balances, review recent transactions, and track expenses through an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles SimpleFIN-connected bank balances and transactions. <br>
Mitigation: Install only if the publisher is trusted and the user is comfortable granting the agent access to that financial data. <br>
Risk: The skill stores a reusable SimpleFIN Access URL in plaintext workspace memory. <br>
Mitigation: Prefer a version that uses a secret store and clearly explains how to delete or revoke the saved Access URL. <br>
Risk: The skill runs shell-built curl commands with sensitive URLs. <br>
Mitigation: Prefer a version that validates SimpleFIN HTTPS URLs, avoids shell-built curl commands, and redacts credentials from errors. <br>


## Reference(s): <br>
- [SimpleFIN Developer Guide](references/developer_guide.md) <br>
- [SimpleFIN Bridge](https://bridge.simplefin.org/) <br>
- [SimpleFIN Protocol](https://www.simplefin.org/protocol.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SimpleFIN Access URL or one-time Setup Token; transaction retrieval can be scoped by account and date filters.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
