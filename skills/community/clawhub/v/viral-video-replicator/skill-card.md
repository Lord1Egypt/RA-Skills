## Description:

Viral Video Replicator reverse-engineers reference fashion videos into Seedance 2.0 prompts using frame extraction, speech transcription, vision analysis, and optional face or clothing replacement modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and content teams use this skill to analyze existing fashion short-form videos and generate structured video analysis, Seedance 2.0 replication prompts, transcripts, operating guidance, and replacement summaries for single or batch workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video frames, audio, and transcripts may be sent to Volcano or ByteDance-related services.

Mitigation: Use the skill only with videos and likenesses the user has rights to process, and avoid sensitive or regulated media unless approved for those services.

Risk: The skill asks users to provide reusable API and object-storage credentials.

Mitigation: Use temporary, least-privilege credentials scoped to a dedicated bucket or prefix, avoid pasting long-lived keys into chat, and rotate credentials after use.

Risk: The release security verdict is suspicious.

Mitigation: Review the skill before installing and install only from a pinned, reviewed revision with pinned dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/viral-video-replicator)
- [README](README.md)
- [FFmpeg Frame Extraction](references/frame-extraction.md)
- [ASR Transcription Pipeline](references/asr-pipeline.md)
- [Vision LLM Analysis](references/vision-analysis.md)
- [Reverse Prompt Assembly](references/reverse-prompt.md)
- [Fallbacks](references/fallbacks.md)
- [Volcano Ark console](https://console.volcengine.com/ark)
- [Seed-ASR-2.0 API endpoint](https://openspeech.bytedance.com/api/v3/auc/bigmodel)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON analysis blocks, generated Seedance prompts, transcript text, SOP guidance, and shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mode-specific @image references, replacement summaries, and degraded-mode warnings when services are unavailable.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
