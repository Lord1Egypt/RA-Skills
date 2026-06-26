## Description: <br>
Cross-platform video transcript extraction and optional AI summarization for YouTube and Bilibili. GPU auto-detect. Transcript-first with opt-in LLM summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huuuwnnn-droid](https://clawhub.ai/user/huuuwnnn-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to extract transcripts, metadata, optional keyframes, and optional summaries from YouTube and Bilibili videos for review, analysis, and channel monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bilibili fallback behavior may access local Chrome browser cookies when standard downloads fail. <br>
Mitigation: Review or disable the browser-cookie retry before deployment, and run the skill only in an environment where that browser session access is acceptable. <br>
Risk: Video transcripts and metadata are cached under ~/.cache/video-insight by default. <br>
Mitigation: Use --no-cache for sensitive videos, configure a controlled cache directory when needed, and clear cached transcript files after use. <br>
Risk: Optional LLM summarization sends transcript content to the configured LLM endpoint. <br>
Mitigation: Use --summarize only with a trusted endpoint and token setup, and keep the default transcript-only workflow for sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huuuwnnn-droid/video-insight) <br>
- [Publisher profile](https://clawhub.ai/user/huuuwnnn-droid) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON to stdout or file, with optional Markdown summary text and optional keyframe image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcript-first by default; optional LLM summarization requires a trusted OpenAI-compatible endpoint or OpenClaw Gateway token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
