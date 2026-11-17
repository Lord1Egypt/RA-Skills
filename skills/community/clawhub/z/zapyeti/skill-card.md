## Description:

Use the ZapYeti API to list debts, track balances, view payoff schedules, log payments, and monitor debt-free progress via api.zapyeti.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djedi](https://clawhub.ai/user/djedi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent interact with ZapYeti debt-management data, including debt lists, payoff progress, payment history, profile data, exports, and plan management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad access to sensitive ZapYeti financial-account data.

Mitigation: Install only when the publisher is trusted, use the narrowest available ZapYeti API key, and review agent actions before execution.

Risk: Exports, deletes, account changes, API-key changes, SimpleFin sync, and social posting can expose or modify sensitive data.

Mitigation: Require explicit user confirmation before running sensitive, destructive, exporting, synchronization, or posting operations.

Risk: The ZapYeti API key may be exposed through command-line process logging or terminal history.

Mitigation: Pass the key through the ZAPYETI_API_KEY environment variable, avoid logging commands that reveal credentials, and rotate the key if exposure is possible.

## Reference(s):

- [ZapYeti API Reference](references/api.md)
- [ZapYeti Homepage](https://zapyeti.com)
- [ZapYeti API Base URL](https://api.zapyeti.com)
- [Declared Source Link](https://github.com/djedi/zapyeti)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZAPYETI_API_KEY; amounts are represented in cents.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
