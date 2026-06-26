## Description: <br>
Understand, summarize, translate, and extract key points from YouTube videos using a transcript-first workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benheee](https://clawhub.ai/user/benheee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to help an agent fetch YouTube metadata and subtitles, generate transcripts, summarize or translate video content, produce timestamped notes, and answer questions about a video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs network access to YouTube and creates local briefing, transcript, metadata, and subtitle files. <br>
Mitigation: Install only for agents that need YouTube metadata or subtitle extraction, use a dedicated output directory, and review generated files before sharing. <br>
Risk: The workflow depends on external runtime tools such as yt-dlp, deno, and optionally ffmpeg. <br>
Mitigation: Install runtime dependencies from trusted package sources and verify tool availability before running extraction commands. <br>
Risk: Video understanding may be incomplete or noisy when subtitles are auto-generated, missing, blocked, or only metadata is available. <br>
Mitigation: Report the evidence source used for each answer and avoid claiming full video understanding when transcript coverage is limited. <br>


## Reference(s): <br>
- [Install and Deploy](references/install-and-deploy.md) <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>
- [Deno](https://deno.land/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, JSON] <br>
**Output Format:** [Markdown summaries with optional JSON metadata, plain-text transcripts, and subtitle files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated output should state whether it is based on manual subtitles, auto subtitles, or partial metadata only.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
