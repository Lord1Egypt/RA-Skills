## Description:

Use this skill when the user wants a UserLayer report for an App Store or Google Play app, including full analysis, polling, and follow-up questions grounded in real reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[houyongsheng](https://clawhub.ai/user/houyongsheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use UserLayer to start app-review analysis jobs, poll completion status, and ask follow-up questions grounded in cited App Store or Google Play reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A paid UserLayer API key can be sent to any configured API host.

Mitigation: Use only a UserLayer-scoped key with quotas, keep the default host unless a replacement is fully trusted, and review the skill before installation.

Risk: Analyze and query calls transmit app URLs, question text, and analysis identifiers to an external service and may incur charges.

Mitigation: Confirm the data and billing posture before use, keep analysis scope to the needed review count, and monitor returned usage details.

## Reference(s):

- [ClawHub UserLayer Skill](https://clawhub.ai/houyongsheng/skills/userlayer)
- [UserLayer Homepage](https://github.com/houyongsheng/userlayer)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Structured JSON API responses summarized as review-backed analysis and follow-up answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include pain points, user segments, opportunities, cited sources, usage details, analysis identifiers, status values, confidence values, and billing-related usage data.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
