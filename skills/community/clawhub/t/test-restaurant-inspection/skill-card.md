## Description:

Automates restaurant inspections by using Ezviz devices to capture camera images, manage a restaurant-focused Ezviz AI agent, and analyze the images for food safety, hygiene, and compliance signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsygcn](https://clawhub.ai/user/wsygcn)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and developers use this skill to run automated AI-assisted restaurant inspections across one or more Ezviz camera devices. It supports food safety, hygiene, staff compliance, audit, and multi-site monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Ezviz API credentials that can capture camera images and create or use Ezviz AI agents.

Mitigation: Store credentials in environment variables or a secrets manager, use least-privilege Ezviz credentials, and rotate credentials regularly.

Risk: Restaurant camera imagery and device identifiers are sent to Ezviz services for AI analysis.

Mitigation: Confirm privacy, consent, and compliance obligations before use, and run the skill only against authorized devices and locations.

Risk: Automatic agent management may create a restaurant-focused Ezviz AI agent when no matching agent exists.

Mitigation: Confirm account permissions and agent quotas before deployment, and review created agents during operational rollout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wsygcn/skills/test-restaurant-inspection)
- [Ezviz token API documentation](https://open.ys7.com/help/81)
- [Ezviz device capture API documentation](https://open.ys7.com/help/687)
- [Ezviz AI analysis API documentation](https://open.ys7.com/help/5006)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Console text with JSON analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Ezviz app credentials and one or more Ezviz device serials; captured images are sent to Ezviz services for analysis.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
