## Description: <br>
Tiger Trading lets agents query Tiger brokerage account balances, positions, and orders, and place or cancel US stock orders with user-provided Tiger credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjpwc](https://clawhub.ai/user/wjpwc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to a Tiger brokerage account for account review, portfolio monitoring, order placement, and order cancellation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use private brokerage credentials to place or cancel orders. <br>
Mitigation: Install only from a trusted publisher, prefer simulated accounts, and require separate human approval before any real order or cancellation. <br>
Risk: Private keys may be exposed if pasted into chat or passed on a command line. <br>
Mitigation: Keep private keys in protected files or a secret manager and avoid sharing key material directly with the agent. <br>
Risk: The skill depends on the external tigeropen package for brokerage API access. <br>
Mitigation: Verify the tigeropen dependency source and version before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wjpwc/tiger-trading) <br>
- [Publisher profile](https://clawhub.ai/user/wjpwc) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell examples plus JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime client returns JSON-like dictionaries for account, balance, position, order, and cancellation operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
