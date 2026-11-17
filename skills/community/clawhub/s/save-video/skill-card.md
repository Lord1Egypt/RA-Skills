## Description:

Download and save videos from mainstream websites by extracting a video URL from user input and saving the media locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skill](https://clawhub.ai/user/skill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to download a video from a provided web URL into a local videos directory for later viewing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accepts arbitrary web URLs and makes outbound requests to retrieve remote media.

Mitigation: Use only trusted public video URLs and consider an allowlist of supported video sites before broad use.

Risk: The skill writes downloaded media to local storage.

Mitigation: Run it in a restricted environment and review the local videos directory for storage and content handling expectations.

Risk: The downloader dependency can change behavior across releases if left unpinned.

Mitigation: Pin and review the yt-dlp version before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skill/skills/save-video)
- [Publisher profile](https://clawhub.ai/user/skill)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Plain text status message plus downloaded video file in a local videos directory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the first URL found in the input and saves downloaded media under a local videos directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
