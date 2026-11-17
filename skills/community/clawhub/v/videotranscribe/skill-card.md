## Description:

videotranscribe turns a local video file or public video URL into a cleaned transcript, and can use a custom prompt to summarize, translate, extract highlights, create meeting notes, or draft social-media copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, content teams, and developers use this command skill to transcribe public or local videos and generate downstream summaries, translations, meeting notes, highlights, and creator copy from the transcript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos, downloaded URL content, prompts, and resulting transcripts are sent to the GuaiKei remote service.

Mitigation: Use the skill only when the user accepts remote processing; avoid sensitive or confidential media unless the service has been approved for that data.

Risk: A supplied HTTP(S) URL can be fetched from the user's environment before upload.

Mitigation: Use trusted local files or clearly public video URLs, and avoid running the skill on cloud hosts or internal networks where URLs could reach metadata services, localhost, or private systems.

Risk: Deletion and privacy claims depend on provider controls rather than locally enforceable behavior.

Mitigation: Treat retention and deletion statements as third-party promises and review provider terms before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/videotranscribe)
- [GuaiKei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown on stdout, depending on the prompt.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; accepts one local video file, one public HTTP(S) video URL, or a prior task ID plus an optional prompt.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
