## Description:

Find viral YouTube Shorts channels that started recently and meet strict view and average-view thresholds, then return qualifying channel links and stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdullahsarumi16-stack](https://clawhub.ai/user/abdullahsarumi16-stack)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and channel researchers use this skill to find new YouTube Shorts channels with high total views, high average views per video, and recent channel age. It is intended to produce a concise ranked summary of qualifying channels for niche research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to run unaudited local code from an absolute path outside the reviewed skill package.

Mitigation: Inspect the external youtube-research.js file before use and require explicit approval before every run.

Risk: The workflow can retry repeatedly when fewer than the requested channels are found.

Mitigation: Add clear retry and timeout limits before deployment.

Risk: The artifact includes weekly unprompted Telegram delivery with persistent state.

Mitigation: Remove or disable the scheduled Telegram and HEARTBEAT behavior unless it is explicitly required and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abdullahsarumi16-stack/skills/youtube-shorts-niche-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown summary with channel links and statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns requested channel count when available; source results are saved to a dated JSON file by the referenced local script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
