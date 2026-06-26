## Description: <br>
Search, register, and manage domain names via unhuman.domains. Pay with bitcoin using agent-wallet. Use when the user wants to find available domains, register a new domain, manage DNS records, update nameservers, or renew a domain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satbot-mdk](https://clawhub.ai/user/satbot-mdk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to search for domain availability, register domains, manage DNS records and nameservers, recover management tokens, and renew domains through the unhuman CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domain-management actions can register, renew, or change real domains, DNS records, and nameservers. <br>
Mitigation: Confirm every registration, renewal, nameserver change, DNS update, and generated DNS record JSON with the user before execution. <br>
Risk: Using the --wallet flag can trigger a real bitcoin payment through agent-wallet. <br>
Mitigation: Use --wallet only after explicit user confirmation for autonomous payment and confirm the wallet is running with sufficient balance. <br>
Risk: Management tokens and wallet secrets are stored locally and can control domains or funds. <br>
Mitigation: Keep ~/.unhuman/tokens.json and ~/.agent-wallet/ secrets private and avoid exposing them in prompts, logs, or shared files. <br>


## Reference(s): <br>
- [unhuman.domains](https://unhuman.domains) <br>
- [unhuman npm package](https://www.npmjs.com/package/unhuman) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can request machine-readable JSON output from the unhuman CLI.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
