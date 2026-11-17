## Description:

Monitors official video channels on platforms such as YouTube and Vimeo, identifies new non-Shorts videos from the past week, and generates linked update reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredhnian](https://clawhub.ai/user/fredhnian)

### License/Terms of Use:


## Use Case:

External users, analysts, and content teams use this skill to track recent official video uploads for competitor, brand, or industry channels and produce weekly update reports with links and basic engagement context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some channel pages may require login for complete content, which can prompt users to consider platform credentials.

Mitigation: Use public channel pages when possible and provide credentials only in a trusted environment with a clear need.

Risk: The artifact uses Chinese-only instructions and inconsistent channel-list filenames.

Mitigation: Clarify the channel-list path before use and localize operating instructions for the intended users.

Risk: Regional restrictions and platform handling of Shorts can lead to incomplete or inconsistent monitoring results.

Mitigation: Confirm regional access and video filtering when reviewing missing or unexpected report entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fredhnian/skills/video-channels-update-push)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with channel names, video titles, links, durations, publish dates, view counts, and view-level star ratings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Excludes Shorts and focuses on videos published in the past week.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
