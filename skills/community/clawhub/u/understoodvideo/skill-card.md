## Description:

understoodvideo converts a selected local video file or supported public video link into cleaned, ready-to-use text, summaries, subtitles, meeting notes, rewrites, highlights, or translations using a configurable prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, operations teams, and developers use this skill to convert a chosen video or prior task ID into clean transcripts, subtitles, summaries, meeting notes, social-media copy, highlights, scripts, or translations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media, prompt text, task metadata, and possibly local path information may be sent to the provider.

Mitigation: Use the skill only with media and prompts you are approved to share with the provider, especially for confidential recordings, customer data, regulated media, or internal meetings.

Risk: The downloader is not tightly restricted to public video platforms.

Mitigation: Avoid untrusted, internal, authenticated, or private URLs; prefer trusted public video links or local files that are approved for processing.

Risk: Network and upload behavior is broader and less clearly bounded than the skill's safety claims suggest.

Mitigation: Review the skill before installation and monitor its network behavior in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/understoodvideo)
- [GuaiKei service website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown content, with shell commands used to invoke the video-to-text workflow.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; processes one video or prior task ID per invocation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
