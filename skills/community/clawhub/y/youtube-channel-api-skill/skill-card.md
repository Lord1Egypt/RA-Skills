## Description:

This skill helps users automatically extract structured YouTube channel data from keyword-based YouTube search results through the BrowserAct API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccmagia2-gif](https://clawhub.ai/user/ccmagia2-gif)

### License/Terms of Use:


## Use Case:

Developers, analysts, and go-to-market teams can use this skill to find YouTube channels by topic or upload-date filter and collect structured channel information for creator discovery, influencer sourcing, competitor tracking, and market research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube search keywords and filters are sent to BrowserAct under the user's BrowserAct account.

Mitigation: Avoid sensitive private or competitive research terms unless BrowserAct processing is acceptable, and use an appropriately scoped and managed API key.

Risk: The skill cannot run without a valid BROWSERACT_API_KEY.

Mitigation: Confirm the environment variable is configured before execution and stop rather than retrying when authorization is invalid.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ccmagia2-gif/skills/youtube-channel-api-skill)
- [BrowserAct Console](https://www.browseract.com/reception/integrations)
- [BrowserAct Workflow API](https://api.browseract.com/v2/workflow)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and text or JSON-like API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BROWSERACT_API_KEY and accepts keywords plus an optional upload-date filter.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
