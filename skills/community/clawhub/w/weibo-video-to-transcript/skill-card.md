## Description:

Turns local video files or supported public video links into transcripts, summaries, rewritten copy, subtitles, quotes, and other prompt-driven text outputs through GuaiKei's cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, content operators, and agents use this skill to run a Node.js command that transcribes a single local video or public video URL and optionally asks for summaries, rewritten social copy, quotes, dialogue extraction, meeting notes, or translation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos and downloaded URL content are sent to GuaiKei's cloud service and any presigned storage endpoint it provides.

Mitigation: Avoid confidential media unless the operator accepts that cloud processing path and has reviewed the service's data handling expectations.

Risk: URL downloading and remote upload handling create network-safety review needs.

Mitigation: Use trusted public URLs and avoid untrusted media sources until URL filtering, download size limits, media validation, and upload-host allowlisting are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/weibo-video-to-transcript)
- [GuaiKei service website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown content on stdout, with progress and errors on stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; processes one video source or one prior task ID per command.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
