## Description:

Track TikTok ad activity and monitor advertiser changes using PipiAds tools for TikTok ad discovery and Facebook-based monitoring workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyanggod](https://clawhub.ai/user/fanyanggod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing analysts use this skill to research TikTok ad activity, inspect advertiser details, and manage ongoing PipiAds monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires sharing a PipiAds API key with the local PipiAds MCP package.

Mitigation: Use a revocable and narrowly scoped API key when available, and remove or rotate the key when the skill is no longer needed.

Risk: Installing and running the PipiAds MCP package through npm introduces local package execution risk.

Mitigation: Install only if comfortable running the package locally, keep the npm environment controlled, and remove the global package when finished.

Risk: PipiAds API calls and monitor workflows can consume account credits or create ongoing monitoring tasks.

Mitigation: Prefer narrow TikTok searches, review monitor-task changes, and monitor credit usage during normal operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fanyanggod/skills/tiktok-ad-tracker-monitor)
- [PipiAds homepage](https://www.pipiads.com)
- [PipiSpy API key and billing portal](https://www.pipispy.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline tool names, setup commands, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PIPIADS_API_KEY environment variable and npm installation of the PipiAds MCP package.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
