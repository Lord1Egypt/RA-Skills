## Description:

Videotocaption helps an agent turn a local video file or public video URL into cleaned transcript text, then optionally use a prompt to summarize, rewrite, extract quotes, create meeting notes, analyze content, or translate the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, and developers use this skill when they need an agent to convert spoken video content into usable text, summaries, captions, social posts, meeting notes, translations, or other prompt-directed written outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video files, public URLs, and prompt content may be sent to the GuaiKei service and associated storage during processing.

Mitigation: Use only videos approved for that transfer, avoid confidential recordings and internal or private URLs, and confirm organizational approval before use.

Risk: Broad URL handling can fetch content from sources that are not appropriate for the user's environment.

Mitigation: Prefer known public video links or local files, and run from a constrained network environment when reviewing or deploying the skill.

Risk: Transcription and prompt-generated outputs can be incomplete or inaccurate for noisy audio, overlapping speakers, accents, specialized terminology, or translation tasks.

Mitigation: Require human review before using outputs in professional, legal, medical, financial, or other high-impact contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/video-to-caption)
- [GuaiKei video text service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or prompt-directed Markdown emitted on stdout; diagnostic progress and errors are emitted separately.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the supplied video and optional prompt; supported tasks include transcription, summaries, rewrites, quote extraction, meeting notes, analysis, and translation.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
