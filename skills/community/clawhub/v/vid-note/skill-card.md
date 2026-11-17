## Description:

vid-note converts local videos or public video links into cleaned transcripts and can use a prompt to produce summaries, rewrites, quotes, shot outlines, translations, and other content-ready text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users and content teams use this skill to turn a single video or prior video task into transcripts, summaries, repurposed social copy, meeting notes, course breakdowns, translations, or other structured text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted remote video links may be downloaded and processed through the skill's remote-video workflow.

Mitigation: Use the skill only with trusted videos and URLs, and review it before installation in agents that may receive untrusted links.

Risk: Video content is uploaded for cloud processing, which may be inappropriate for confidential recordings.

Mitigation: Avoid confidential recordings unless the user or organization accepts the cloud-processing model and token-based access requirements.

Risk: The token error path contains promotional contact messaging that may be unsuitable for end-user-facing agent output.

Mitigation: Treat stderr as diagnostic output and review or wrap error handling before exposing messages directly to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/vid-note)
- [Guaikei service site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or user-requested structured Markdown on stdout, with progress and diagnostics on stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and accepts one video file, one public video URL, or one prior task ID plus an optional prompt.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
