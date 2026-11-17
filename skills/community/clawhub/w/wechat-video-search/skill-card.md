## Description:

Searches WeChat Channels videos through the TikHub API and returns video links plus basic analysis fields such as likes, duration, and publish time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahsbnb](https://clawhub.ai/user/ahsbnb)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to run keyword searches against TikHub's WeChat Channels endpoint and receive formatted video IDs, titles, authors, like counts, durations, publish times, download URLs, and share URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expose the user's TikHub API token and search activity through normal debug output.

Mitigation: Use only low-privilege TikHub tokens, avoid sensitive searches, do not run this release where stdout or stderr is captured, remove the debug prints, and rotate any token used in a logged environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ahsbnb/skills/wechat-video-search)
- [TikHub WeChat Channels Search Endpoint](https://api.tikhub.dev/api/v1/wechat_channels/fetch_search_latest)
- [TikHub Token Registration](https://user.tikhub.io/register)
- [TikHub API Token Dashboard](https://user.tikhub.io/dashboard/api)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration guidance]

**Output Format:** [Plain text search summaries or raw JSON returned from the TikHub API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TikHub API token; this release may print token and search activity details to stdout or stderr.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
