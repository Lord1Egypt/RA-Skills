## Description:

This skill helps users extract channel-level and video detail data from a specific YouTube channel via the BrowserAct API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccmagia2-gif](https://clawhub.ai/user/ccmagia2-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content operations teams use this skill to retrieve structured YouTube channel and video metrics for competitor tracking, creator research, reporting, market research, and content strategy analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The BrowserAct API key could be exposed if pasted into an agent conversation.

Mitigation: Configure the key through BROWSERACT_API_KEY or a protected secret mechanism, and rotate any key previously shared in chat.

Risk: The target YouTube channel URL and selected video type are sent to BrowserAct.

Mitigation: Use the skill only when sharing those inputs with BrowserAct is acceptable for the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ccmagia2-gif/skills/youtube-video-api-skill)
- [BrowserAct integrations console](https://www.browseract.com/reception/integrations)
- [BrowserAct workflow API endpoint](https://api.browseract.com/v2/workflow)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal status logs followed by structured YouTube channel and video data as text or JSON returned by the BrowserAct API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and BROWSERACT_API_KEY; accepts a YouTube channel URL and an optional video ordering mode of Latest, Popular, or Earliest.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
