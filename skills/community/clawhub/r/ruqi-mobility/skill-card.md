## Description:

RuQi Mobility helps agents assist with ride hailing, price estimates, order tracking, driver location checks, route planning, cancellation, and nearby searches for RuQi trips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruqi](https://clawhub.ai/user/ruqi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage RuQi ride-hailing workflows, including phone verification login, address resolution, fare estimates, order creation after user confirmation, tracking, cancellation, and route lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real ride-account credentials, phone numbers, and precise home/work locations.

Mitigation: Do not store tokens, phone numbers, or saved places in plaintext; use a managed secret store and require explicit user consent before saving locations.

Risk: Order tracking can send ride details and screenshots to an external messaging target.

Mitigation: Require explicit opt-in for each messaging target, verify the recipient before sending, and disable screenshots or minimize trip data when screenshots are not required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruqi/skills/ruqi-mobility)
- [RuQi Mobility homepage](https://www.ruqimobility.com)
- [RuQi mini app download link](https://web.ruqimobility.com/ruqi/index.html#/download?to=service&pagePath=pages%2Findex%2Findex&toPlatform=miniApp&skipType=3)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start background order polling and send trip notifications with screenshots through OpenClaw when configured.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
