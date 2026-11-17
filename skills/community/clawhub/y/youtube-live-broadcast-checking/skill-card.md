## Description:

Checks upcoming live broadcast schedules and current live status for YouTube channels using the YouTube Data API v3.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenho1394](https://clawhub.ai/user/stevenho1394)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage a watchlist of YouTube channels and check live or upcoming broadcasts. It is useful for workflows that need scheduled stream times, active live status, video links, thumbnails, and related channel metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a YouTube Data API key.

Mitigation: Install only in agent environments where providing YOUTUBE_API_KEY is acceptable, and scope or rotate the key according to the operator's Google Cloud policy.

Risk: The watched channel list is stored locally in watchlist.json and persists across agent restarts.

Mitigation: Review the local watchlist file for sensitive channel selections and apply workspace access controls appropriate for the deployment.

Risk: YouTube API quota limits or helper behavior around live/full status and timezone labeling may confuse results.

Mitigation: Monitor YouTube API quota usage, review dependency updates before production use, and verify time-sensitive broadcast results against YouTube when precision matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevenho1394/skills/youtube-live-broadcast-checking)
- [Manifest homepage](https://github.com/StevenHo1394/openclaw/tree/main/skills/youtube-live-broadcast-checking)
- [Manifest issue tracker](https://github.com/StevenHo1394/openclaw/issues)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON-like tool responses containing channel records, broadcast objects, arrays, null values, or error messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include YouTube video URLs, thumbnails, scheduled or actual start timestamps, concurrent viewer counts when available, and local HKT timestamp metadata.]

## Skill Version(s):

1.3.7 (source: server release metadata, package.json, openclaw.plugin.json, clawhub.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
