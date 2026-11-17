## Description:

v2t converts local video files or public video URLs into cleaned transcripts and prompt-directed summaries, rewrites, highlights, storyboards, meeting notes, and translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, and developers use this skill to turn a single video URL, local video file, or prior task id into usable transcript text and prompt-shaped content such as summaries, rewrites, quotes, meeting notes, or translations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the selected video, local path metadata, and downloaded remote-link content to a provider cloud workflow.

Mitigation: Use only media approved for third-party processing, and avoid confidential, regulated, or internal videos unless the provider's retention and deletion terms are acceptable.

Risk: Remote URL input may cause the downloader to reach network locations visible from the user's machine.

Mitigation: Process only trusted public video URLs or known local files; do not run the skill on untrusted URLs supplied by other people.

Risk: Transcripts, summaries, and rewrites may be inaccurate when audio is noisy, speakers overlap, accents are strong, or the topic is specialized.

Mitigation: Review outputs before publishing or using them in medical, legal, financial, or other high-impact contexts.

## Reference(s):

- [ClawHub v2t skill page](https://clawhub.ai/engheng-art/skills/v2t)
- [GuaiKei service website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown content from stdout, with shell commands for execution guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; accepts one video URL, local file path, or prior task id plus an optional prompt.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
