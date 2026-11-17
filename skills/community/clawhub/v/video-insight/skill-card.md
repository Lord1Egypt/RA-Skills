## Description:

Cross-platform video transcript extraction and optional AI summarization for YouTube and Bilibili. GPU auto-detect. Transcript-first with opt-in LLM summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huuuwnnn-droid](https://clawhub.ai/user/huuuwnnn-droid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract transcripts, metadata, and optional keyframes from YouTube or Bilibili videos, then optionally request a transcript summary. It supports single-video, channel-scan, and batch workflows where video content needs to be converted into agent-readable text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use browser cookies when video access fails, which can expose private or account-restricted video access.

Mitigation: Avoid private or account-restricted videos unless the browser-cookie fallback is removed or made explicitly opt-in.

Risk: Optional summarization can send full transcripts to a configured LLM endpoint.

Mitigation: Do not use summarization with sensitive transcripts unless the endpoint is trusted and uses safe transport.

Risk: Network and credential handling requires review before installation and use.

Mitigation: Review configuration before installing, avoid setting LLM_API_URL alongside OPENCLAW_GATEWAY_TOKEN, and prefer an isolated virtual environment with pinned dependencies.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, files]

**Output Format:** [JSON object with transcript text, timestamps, metadata, optional keyframe file paths, and optional Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is transcript-first and does not call an LLM unless summarization is explicitly enabled.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
