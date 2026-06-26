## Description: <br>
Reverse-engineers reference fashion or short-form videos into structured analysis, transcripts, Seedance 2.0 replication prompts, and platform operating guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to analyze existing reference videos and produce reusable Seedance 2.0 prompts with optional face, body, or clothing replacement modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may send selected frames, audio, transcripts, and presigned storage URLs to external cloud services for processing. <br>
Mitigation: Process only media the user has rights and consent to analyze, and disclose when media or audio leaves the local machine. <br>
Risk: The skill asks users for Volcano, TOS, and ASR credentials during setup. <br>
Mitigation: Use temporary or least-privilege credentials, prefer an environment secret store, and avoid pasting long-lived keys into chat. <br>


## Reference(s): <br>
- [FFmpeg Frame Extraction](references/frame-extraction.md) <br>
- [ASR Transcription Pipeline](references/asr-pipeline.md) <br>
- [Vision LLM Analysis](references/vision-analysis.md) <br>
- [Reverse Prompt Assembly](references/reverse-prompt.md) <br>
- [Fallbacks](references/fallbacks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON analysis, prompts, transcripts, SOP guidance, and inline shell or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-video and batch workflows, four replacement modes, and degraded outputs when FFmpeg, ASR, storage, or vision analysis fails.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
