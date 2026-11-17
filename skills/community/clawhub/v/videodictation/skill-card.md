## Description:

Transcribes local video files or public video URLs into cleaned text, then uses optional prompts to generate summaries, social posts, quote extracts, meeting notes, course breakdowns, livestream recaps, interview notes, or Chinese-English translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and content teams use this skill to turn one selected video source or prior task ID into a transcript or prompt-shaped derivative text such as summaries, captions, meeting notes, scripts, translations, and content repurposing drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video files, prompts, and some local path metadata are sent to a third-party service.

Mitigation: Use only videos and prompts approved for that service, avoid sensitive or regulated content unless approved, and review service terms before commercial deployment.

Risk: The skill can fetch user-provided URLs from the environment where the agent runs.

Mitigation: Avoid private-network, localhost, metadata-service, sensitive, regulated, or very large URLs; prefer local files that were intentionally selected.

Risk: Local path names may be visible to the service during processing.

Mitigation: Use neutral working paths or filenames when path disclosure would reveal sensitive project, client, or user information.

Risk: Transcripts and prompt-generated derivatives may be inaccurate for noisy, multi-speaker, accented, or specialized content.

Mitigation: Review outputs before relying on them, especially for medical, legal, financial, compliance, or public-facing uses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/videodictation)
- [GuaiKei service website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; command stdout returns plain text or prompt-shaped text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and processes one video source or prior task ID per invocation.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
