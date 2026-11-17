## Description:

Social Media Scheduler helps users plan social media posts, create content calendars, write captions, generate hashtags, batch content, track ideas, and draft platform-specific text for manual posting while keeping data local.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkpareek0315](https://clawhub.ai/user/mkpareek0315)

### License/Terms of Use:


## Use Case:

External users, creators, marketers, and small teams use this skill to generate social media captions, hashtags, content calendars, draft libraries, content strategy ideas, bios, and performance notes for manual review and posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated drafts, calendars, ideas, and settings are auto-saved locally and may contain brand, campaign, or personal content.

Mitigation: Review local files under ~/.openclaw/social-media-scheduler/ and avoid entering sensitive campaign information unless local storage is acceptable.

Risk: Broad trigger phrases may activate the skill during general social media discussions.

Mitigation: Confirm user intent before creating or saving content when the request is ambiguous.

Risk: The artifact mentions an exec permission for first-run directory creation while server-resolved metadata only lists read and write tools.

Mitigation: Verify the final permission manifest before deployment and create the local data directory through an approved setup path if needed.

Risk: The skill generates social media guidance and trend ideas that may be inaccurate, outdated, or unsuitable for a brand.

Mitigation: Have users review content, hashtags, and platform advice before publishing or relying on performance recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mkpareek0315/skills/social-media-planner)
- [Publisher profile](https://clawhub.ai/user/mkpareek0315)
- [Publisher social profile](https://x.com/Mkpareek19_)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline text examples, JSON snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated content may be saved locally as drafts, calendar entries, ideas, settings, and stats under ~/.openclaw/social-media-scheduler/.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
