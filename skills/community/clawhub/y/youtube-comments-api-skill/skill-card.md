## Description:

This skill helps agents extract structured YouTube video list data and comment data through the BrowserAct API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccmagia2-gif](https://clawhub.ai/user/ccmagia2-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and market research users can use this skill to run BrowserAct-based YouTube searches, collect video metadata and public comments, and summarize audience feedback for topics, competitors, or trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a BrowserAct API key and may prompt users to provide it during an agent session.

Mitigation: Configure BROWSERACT_API_KEY through a protected secret or environment setting, and do not paste API keys into chat.

Risk: YouTube search terms are sent to BrowserAct and returned results can include commenter names, channel URLs, and comment text.

Mitigation: Avoid sensitive search terms and handle collected public comment data according to platform terms and privacy expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ccmagia2-gif/skills/youtube-comments-api-skill)
- [BrowserAct API key console](https://www.browseract.com/reception/integrations)
- [BrowserAct workflow API endpoint](https://api.browseract.com/v2/workflow)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Text, JSON, Guidance]

**Output Format:** [Terminal logs followed by BrowserAct result text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and BROWSERACT_API_KEY; accepts keywords, comment limit, and scroll count.]

## Skill Version(s):

1.0.1 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
