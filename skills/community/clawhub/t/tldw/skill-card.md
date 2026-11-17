## Description:

Extracts YouTube video transcripts and provides concise summaries highlighting main points, arguments, and conclusions without watching the full video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vovavvk](https://clawhub.ai/user/vovavvk)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Users and agents use this skill when a YouTube URL needs to be summarized from available captions, especially for educational, news, documentary, or reference videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser cookies can grant access to a YouTube account if exposed.

Mitigation: Use the skill with public videos when possible; if cookies are needed, avoid primary-account exports, store cookie files outside shared directories, and delete them after use.

Risk: Part of the download flow disables TLS certificate verification.

Mitigation: Fix certificate verification before using cookies or running the skill on untrusted networks.

Risk: Caption text and video metadata are cached locally.

Mitigation: Review and clear the cache when transcripts or metadata should not remain on disk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vovavvk/skills/tldw)
- [Attribution](artifact/ATTRIBUTION.md)
- [Original TL;DW project](https://github.com/stong/tldw)
- [Original TL;DW website](https://tldw.tube)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summaries with optional JSON transcript metadata and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces transcript-based summaries from YouTube captions; cached caption and metadata files may be created locally.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
