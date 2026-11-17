## Description:

A specialized tool for sending quantitative trading signals to the FMZ platform via HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[13290186019](https://clawhub.ai/user/13290186019)

### License/Terms of Use:


## Use Case:

External developers and trading-agent users use this skill to send buy, sell, wait, or close trading signals from an agent to FMZ over HTTP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send live buy, sell, wait, or close trading commands to FMZ.

Mitigation: Install only where live trading authority is intended, and add explicit confirmation or dry-run behavior before buy, sell, or close actions.

Risk: The artifact uses weak scoping for FMZ signal delivery.

Mitigation: Replace the hardcoded UUID with a private deployment secret and avoid broadcast node_id 0 unless broad delivery is intentional.

Risk: A returned status message may be mistaken for accepted trading execution.

Mitigation: Verify FMZ responses before treating a signal as accepted or acted on.

## Reference(s):

- [FMZ Channel API endpoint](https://www.fmz.com/api/v1/channel)
- [ClawHub skill page](https://clawhub.ai/13290186019/skills/send-signal)

## Skill Output:

**Output Type(s):** [API Calls, Text]

**Output Format:** [String status message after a JSON HTTP POST]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends action, symbol, price, and reason fields to FMZ.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
