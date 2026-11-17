## Description:

Monitors XPeng vehicle data across China and Europe, including delivery lead times and daily European BEV registrations and sales.

This skill is ready for commercial/non-commercial use.

## Publisher:

[svenzhexu](https://clawhub.ai/user/svenzhexu)

### License/Terms of Use:

MIT-0

## Use Case:

Drivers, analysts, and XPeng market observers use it to check China vehicle delivery wait times by model and configuration and review European BEV registration trends, including twelve-month comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The current workflow requests website passwords in chat or command-line arguments and includes saved website session cookies.

Mitigation: Avoid supplying a password through this workflow. Ask the publisher to remove bundled sessions, use user-controlled authentication, and provide clear deletion and expiration controls for any cached sessions.

## Reference(s):

- [XPeng official store API](https://store.xiaopeng.com)
- [XPENG Europe daily registration data](https://eu-evs.com/brands/XPENG/ALL_DAILY/Models-Daily/Year/${year})
- [ClawHub skill page](https://clawhub.ai/svenzhexu/skills/xpeng-monitor)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Analysis]

**Output Format:** [Markdown tables and summaries, or structured JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Vehicle delivery lead times and registration/sales figures, including daily and monthly comparisons.]

## Skill Version(s):

1.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
