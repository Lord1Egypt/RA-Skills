## Description:

Authorization middleware that enforces Avatar Mandates, uses a local LLM to approve or deny sub-agent actions, and sends email alerts for denied actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced users use this skill to simulate an authorization gate for sub-agent actions against a pre-generated Avatar Mandate, with local LLM review and email alerting for denials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored SMTP app passwords may expose email account access if workspace files are compromised.

Mitigation: Use a dedicated, low-privilege email app password, restrict the account's purpose, and rotate or delete the credential after use.

Risk: Prompt-based LLM approval may produce incorrect decisions and is not a technical firewall.

Mitigation: Keep hard permission boundaries and human approval for physical, financial, account, or safety-critical actions.

Risk: Alert emails may contain sensitive operational context.

Mitigation: Avoid placing secrets or unnecessary personal data in reviewed action context and use trusted email retention controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-digital-avatar)
- [Space2.world homepage](https://space2.world)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Interactive console text, configuration prompts, and JSON approval decisions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate an override prompt for subordinate agents and send denial alert emails when SMTP is configured.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
