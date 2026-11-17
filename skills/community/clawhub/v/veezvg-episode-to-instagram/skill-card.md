## Description:

Full pipeline to turn a video podcast episode into Instagram content (carousel posts, quote cards, and Reels). Transcribes the episode, extracts key quotes with timestamps, pulls video frames, generates aesthetic carousel slides, and posts to Instagram via browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veezvg](https://clawhub.ai/user/veezvg)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, social media operators, and developers use this skill to convert long-form podcast or video episodes into Instagram-ready transcripts, content plans, carousel slides, Reel clips, captions, previews, and posting drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive media and can upload audio for transcription.

Mitigation: Use only trusted local media and confirm that audio may be sent to OpenAI before running transcription.

Risk: The skill automates a logged-in Instagram browser session and can publish content.

Mitigation: Inspect generated previews and captions, keep the browser CDP port inaccessible to untrusted users, and do not run posting commands with --post without explicit final approval.

Risk: Untrusted content-plan JSON or an unsafe working directory could affect generated outputs or local files.

Mitigation: Review content-plan JSON before use and run the skill in a non-sensitive working directory.

Risk: Preview screenshots are written under /tmp.

Mitigation: Avoid including sensitive content in previews or clear temporary screenshots after review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/veezvg/skills/veezvg-episode-to-instagram)
- [Instagram](https://www.instagram.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON content plans, shell commands, generated media files, captions, and preview screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are staged in an episode working directory and may include transcript JSON/text, content-plan JSON, extracted PNG frames, carousel slide images, Reel clips, captions, and Instagram draft previews.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
