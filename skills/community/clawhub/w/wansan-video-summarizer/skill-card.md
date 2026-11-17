## Description:

Multi-platform video transcript extraction and AI-powered summarization for YouTube, Bilibili, channel scans, and daily video digests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcdowell8023](https://clawhub.ai/user/mcdowell8023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to extract video transcripts, summarize individual videos, scan channels, and generate scheduled video digest outputs for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcript excerpts may be sent to configured LLM services or Pollinations.

Mitigation: Use the skill only with public or non-sensitive videos unless the configured LLM endpoint is trusted for that content.

Risk: Bilibili mode may allow yt-dlp to use Chrome browser cookies.

Mitigation: Avoid Bilibili mode unless cookie use is intended; prefer an isolated environment or a dedicated browser profile.

Risk: Certificate checking may be disabled during Bilibili video retrieval.

Mitigation: Review and remove the no-certificate-check behavior before use in production or sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcdowell8023/skills/wansan-video-summarizer)
- [Publisher profile](https://clawhub.ai/user/mcdowell8023)
- [Author-provided repository metadata](https://github.com/mcdowell8023/oc-youtube-summarizer)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
- [innertube](https://github.com/tombulled/innertube)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [JSON files containing video metadata, transcript status, markdown summaries, run statistics, and optional extracted frame paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text-only, automatic frame insertion, and AI-assisted frame review modes; output path is configurable.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
