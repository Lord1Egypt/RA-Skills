## Description:

Collects TikTok public search results, creator posts, and video comments as structured data for competitor and brand analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Creators, brand teams, and analysts use the skill to gather public TikTok search results, creator posts, and comments, then compare content and engagement trends or summarize discussion themes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan had medium confidence because some components were only partly inspected.

Mitigation: Review the skill and its requested behavior before enabling it in a production workflow.

Risk: Search terms and TikTok URLs are sent to the external data service at guaikei.com.

Mitigation: Use non-sensitive inputs and confirm the service is approved for the data in your workflow.

Risk: The scanner notes that timestamps use Beijing time, which can complicate comparisons across time zones.

Mitigation: Check the timestamp convention and convert it before comparing results with other sources.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/tiktok-competitor-radar)
- [Service and API support](https://www.guaikei.com)
- [Usage options](artifact/references/options.md)
- [Release history](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Text, Markdown]

**Output Format:** [Structured JSON results that an agent can summarize as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Searches, creator posts, and video comments; results cover public TikTok data.]

## Skill Version(s):

1.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
