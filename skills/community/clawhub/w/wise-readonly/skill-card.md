## Description:

Read-only Wise API operations for account inspection, FX lookups, recipients, and transfer history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cianweeresinghe-sudo](https://clawhub.ai/user/cianweeresinghe-sudo)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to inspect Wise profiles, balances, recipients, transfers, quotes, delivery estimates, and exchange rates without creating or changing Wise resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Wise API token that can expose read-only account data.

Mitigation: Install only when that access is acceptable, store the token securely, and grant the narrowest Wise access available.

Risk: Raw output may contain personal or bank-account details.

Mitigation: Keep default redaction enabled, use --raw only for a specific need, and avoid sharing raw responses.

## Reference(s):

- [Wise API endpoint](https://api.wise.com)
- [wise-mcp source reference](https://github.com/Szotasz/wise-mcp)
- [ClawHub skill page](https://clawhub.ai/cianweeresinghe-sudo/skills/wise-readonly)
- [ClawHub publisher profile](https://clawhub.ai/user/cianweeresinghe-sudo)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [JSON responses and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profile, recipient, and transfer responses are PII-redacted by default unless raw output is explicitly requested.]

## Skill Version(s):

1.0.3 (source: server release metadata and ClawHub config)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
