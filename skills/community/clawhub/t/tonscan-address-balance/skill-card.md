## Description: <br>
Look up TON blockchain wallet balances, address information, and token holdings using the free TonScan API with no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariusfeldmann](https://clawhub.ai/user/mariusfeldmann) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users and developers use this skill to check TON wallet balances, address status, and token-related account details through TonScan, including converting nanotons to TON for readable reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried TON wallet addresses are sent to TonScan; addresses are public, but the fact that a specific address was queried may still be visible to that external service. <br>
Mitigation: Use the skill only for addresses the user intends to check and disclose TonScan use when query privacy matters. <br>
Risk: The skill relies on a free public API that may rate limit requests or become temporarily unavailable. <br>
Mitigation: For repeated lookups, add retry and backoff behavior and verify important balances against another trusted source when availability or accuracy is critical. <br>


## Reference(s): <br>
- [TonScan address information API](https://api.tonscan.com/api/bt/getAddressInformation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell, Python, and JavaScript examples; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public TonScan API responses and converts balances from nanotons to TON for display.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
