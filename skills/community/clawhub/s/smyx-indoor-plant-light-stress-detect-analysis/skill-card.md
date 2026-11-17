## Description:

Analyzes indoor plant images or videos for signs of insufficient or excessive light and suggests care adjustments, optionally considering light sensor readings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Home gardeners and plant-care teams use this skill to assess possible light stress in indoor plants, get lighting suggestions, and retrieve past analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected plant media or submitted URLs are sent to lifeemergence.com cloud services.

Mitigation: Use only media and public URLs you are comfortable sharing with that service; avoid sensitive media and private or internal URLs.

Risk: The skill silently creates or reuses local and remote identity or session state.

Mitigation: Review the workspace data directory for stored identity or token data before and after use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-indoor-plant-light-stress-detect-analysis)
- [API interface reference](artifact/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured text or JSON-like analysis with report links; Markdown links for report history]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can be saved to a local file.]

## Skill Version(s):

1.0.12 (source: ClawHub release metadata; bundled SKILL.md lists 1.0.11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
