## Description:

YouTube Content Manager Pro helps YouTube creators generate video topics, scripts, title options, SEO descriptions, tags, thumbnail suggestions, publishing records, and analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baolige2023](https://clawhub.ai/user/baolige2023)

### License/Terms of Use:

MIT-0

## Use Case:

External YouTube creators and channel operators use this skill to draft topics, scripts, titles, SEO metadata, thumbnail guidance, and publishing-performance analysis for videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User content may be sent to an undisclosed AI provider.

Mitigation: Disclose the provider and data handling path before use, and avoid confidential channel plans or unpublished scripts until that disclosure is corrected.

Risk: Embedded API keys and a hard-coded Flask secret may expose accounts or sessions.

Mitigation: Remove and rotate embedded keys, store secrets outside the artifact, and configure a deployment-specific Flask secret.

Risk: The web app configuration is unsafe for network exposure.

Mitigation: Disable debug mode and broad host binding, replace unsafe HTML rendering, and complete review before exposing the app to a network.

Risk: Billing behavior and consent screens are unclear.

Mitigation: Correct billing amounts and payment consent screens before charging users.

Risk: Stored publishing records may lack record-level user isolation.

Mitigation: Add per-user record isolation before multi-user or networked deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baolige2023/skills/youtube-content-manager-intl)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Web UI content and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes generated topics, scripts, title options, SEO descriptions, tags, thumbnail guidance, saved publishing records, and analytics summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
