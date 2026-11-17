## Description:

This skill helps agents extract structured data from YouTube search results using BrowserAct's YouTube Search API workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccmagia2-gif](https://clawhub.ai/user/ccmagia2-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content teams use this skill to search YouTube by keyword and retrieve structured video, Shorts, channel, or playlist result data for research, monitoring, and reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The BrowserAct bearer token could be exposed if pasted into chat or logs.

Mitigation: Set BROWSERACT_API_KEY through a protected environment or secret manager and avoid sharing the token in conversation.

Risk: YouTube search terms and retrieved result data are sent to BrowserAct for processing.

Mitigation: Use the skill only for queries and data that are appropriate to send to BrowserAct.

Risk: The script polls an external workflow until completion and may run longer than expected.

Mitigation: Monitor terminal status output and stop the process manually if polling runs too long.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ccmagia2-gif/skills/youtube-search-api-skill)
- [BrowserAct API key setup](https://www.browseract.com/reception/integrations)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal logs followed by structured YouTube search result text from the BrowserAct API response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and BROWSERACT_API_KEY; can poll for several minutes and retries failed non-authorization runs once.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
