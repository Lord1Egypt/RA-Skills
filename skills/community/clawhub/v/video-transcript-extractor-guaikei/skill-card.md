## Description:

Extracts and refines video or audio transcripts from local media files or public video links, with optional prompts for summaries, rewrites, highlights, scene breakdowns, and translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, content teams, and developers use this skill to convert completed videos or audio files into reusable transcripts and prompt-shaped outputs such as summaries, meeting notes, marketing drafts, highlights, and translations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary web URLs and upload resulting media to GuaiKei and its storage provider.

Mitigation: Use it only with trusted public videos or local media intended for that service, and do not provide localhost, private-network, cloud metadata, or sensitive internal URLs.

Risk: Task IDs may allow reuse of previously processed media outputs.

Mitigation: Treat task IDs as sensitive and avoid sharing logs or saved task state with untrusted parties.

Risk: Automatic-deletion and retention claims are service-provider assurances that are not independently verified in the evidence.

Mitigation: Avoid submitting sensitive media unless the service provider's retention and privacy terms have been independently reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/video-transcript-extractor-guaikei)
- [GuaiKei website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown-style prose emitted to stdout, with progress and logs emitted separately.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; accepts video source, task ID, and optional prompt inputs.]

## Skill Version(s):

1.0.0 (source: package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
