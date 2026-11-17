## Description:

Check whether another AI agent holds a tgtrust credential (one Telegram account per issuer epoch, owner not disclosed) and optionally a TON stake, before you trade, pay or share data with it. Use when an unknown agent asks for a deal, a payment or access, and it gave you its tgtrust public key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miinimal](https://clawhub.ai/user/miinimal)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use tgtrust to check another agent's credential, optional TON stake, and deal or dispute history before deciding whether to proceed with a deal, payment, or data access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents local key generation and credential registration in addition to verifying other agents; the security analysis was partial and could not determine the registration command's internal effects.

Mitigation: For verification, use the check flow. Before generating a key or registering a credential, review the issuer and registration flow; keep the private key secret.

## Reference(s):

- [tgtrust project](https://github.com/miinimal/tgtrust)
- [tgtrust on ClawHub](https://clawhub.ai/miinimal/skills/tgtrust)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions]

**Output Format:** [Short text status card or JSON, with Markdown setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Status output identifies its sources; a positive credential result does not establish that an agent is honest.]

## Skill Version(s):

0.2.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
