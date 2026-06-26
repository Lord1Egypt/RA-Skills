## Description: <br>
Read-only Wise API operations for account inspection, FX lookups, recipients, and transfer history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cianweeresinghe-sudo](https://clawhub.ai/user/cianweeresinghe-sudo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect Wise profiles, balances, recipients, transfers, quotes, delivery estimates, and exchange rates without creating or modifying Wise resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose Wise account information accessible to WISE_API_TOKEN. <br>
Mitigation: Use the least-privileged Wise token available and install only where account read access is acceptable. <br>
Risk: Unredacted output may include sensitive personal or financial fields. <br>
Mitigation: Keep the default redaction behavior and use --raw only for a specific, reviewed need. <br>
Risk: Automatic invocation could retrieve account data without deliberate user intent. <br>
Mitigation: Keep implicit invocation disabled, matching the packaged OpenClaw policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cianweeresinghe-sudo/wise-readonly) <br>
- [wise-mcp source reference](https://github.com/Szotasz/wise-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance] <br>
**Output Format:** [JSON responses from read-only Wise API calls, with command guidance in Markdown or inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Profile, recipient, and transfer responses redact common PII fields by default; --raw returns unredacted fields when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.3 (source: .clawhub/config.toml, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
