## Description:

Generates Chinese team-building banner slogans from a team or activity description after completing the configured paid order flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liulian822](https://clawhub.ai/user/liulian822)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request concise Chinese slogan text for team-building banners, annual meetings, outdoor events, sales teams, and training activities. The skill includes a paid order flow before returning the generated banner slogan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Poorly scoped payment handling and configurable payee information can route funds incorrectly.

Mitigation: Review the payment flow before installation and verify the configured payee for the intended release.

Risk: Broad credential and network permissions increase exposure if the skill is misconfigured or modified.

Mitigation: Narrow permissions to the minimum required scope before use with real credentials.

Risk: An unpinned payment dependency and inconsistent service identity markers can make payment behavior harder to verify.

Mitigation: Require a pinned trusted payment dependency and fix the service identifier and configuration mismatch before production use.

Risk: The source instructs the agent to disclose thought process during user interaction.

Mitigation: Remove the thought-process disclosure instruction before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liulian822/skills/team-banner)
- [Publisher profile](https://clawhub.ai/user/liulian822)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns payment status and a Chinese banner slogan; order creation stores local order files.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
