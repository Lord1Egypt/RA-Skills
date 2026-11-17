## Description:

Maintain the GitLab agent profile page and static contribution performance chart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xrowgmbh](https://clawhub.ai/user/xrowgmbh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to update a GitLab agent profile with monthly contribution charts and supporting public records, including anonymized totals for private activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The WebP fallback may download and execute an unpinned npm package while GitLab credentials are available.

Mitigation: Use ImageMagick when available; otherwise verify and pin the WebP package, and avoid exposing the GitLab token during rendering when possible.

Risk: The security scan reports that declared tool scope is missing despite detected capabilities, and some local references were unresolved.

Mitigation: Review the full skill and its references before installation, and grant only the GitLab access needed for the profile update.

## Reference(s):

- [GitLab Agent Profile on ClawHub](https://clawhub.ai/xrowgmbh/skills/xrowgmbh-gitlab-agent-profile)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [Static SVG and WebP charts with JSON contribution records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Charts and records cover the configured number of completed months (12 by default); private activity is represented by anonymized monthly totals.]

## Skill Version(s):

1.147.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
