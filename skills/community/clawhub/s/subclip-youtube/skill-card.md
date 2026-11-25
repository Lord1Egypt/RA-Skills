## Description:

Upload exported files or timeline segments to YouTube, manage connected channels, videos, native schedules, comments, playlists, captions, thumbnails and Analytics reports through Subclip MCP. Use for YouTube actions and clip batches, without creating upload projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prosamik](https://clawhub.ai/user/prosamik)

### License/Terms of Use:

MIT-0

## Use Case:

External channel owners and video teams use this skill to publish exported videos or selected timeline segments, manage YouTube channel content, and review channel analytics. It also guides agents through confirmation and publication-status checks for channel changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review has medium confidence and is partial because a local reference could not be resolved; the skill can also upload or change YouTube content.

Mitigation: Review the proposed action and follow the skill's confirmation requirements before uploads, posts, or channel changes.

## Reference(s):

- [YouTube Data API: videos.update](https://developers.google.com/youtube/v3/docs/videos/update)
- [YouTube Analytics API: reports.query](https://developers.google.com/youtube/analytics/reference/reports/query)
- [YouTube Help: Add a related video to your YouTube Short](https://support.google.com/youtube/answer/14075157)
- [YouTube Help: Share links with your audience](https://support.google.com/youtube/answer/13748639)

## Skill Output:

**Output Type(s):** [Guidance, Text, Reports]

**Output Format:** [Natural-language guidance and YouTube status or Analytics results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can initiate YouTube publishing and channel-management actions after the user confirms the exact action.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
