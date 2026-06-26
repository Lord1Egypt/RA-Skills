## Description: <br>
Turn YouTube videos into dependable markdown transcripts and polished summaries, even when caption coverage is messy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arthurli202602-commits](https://clawhub.ai/user/arthurli202602-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, developers, and operators use this skill to produce durable transcript and summary artifacts from public, private, or caption-poor YouTube videos. It is suited for technical walkthroughs, tutorials, founder content, internal uploads, and batch research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restricted-video cookie options can expose sensitive browsing or account context if used casually. <br>
Mitigation: Use cookie options only when needed and prefer a dedicated or exported cookie file over a primary browser profile. <br>
Risk: Private or sensitive videos may be written to local transcript and summary files or sent through the configured model-based summarization path. <br>
Mitigation: Process highly sensitive private videos only in an appropriate local environment with an acceptable configured OpenClaw model gateway. <br>
Risk: The workflow depends on local third-party tools and a downloaded Whisper model. <br>
Mitigation: Install only after reviewing and accepting the use of yt-dlp, ffmpeg, whisper.cpp, and the required local model file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arthurli202602-commits/youtube-anycaption-summarizer) <br>
- [Metadata homepage](https://github.com/arthurli202602-commits/youtube-anycaption-summarizer) <br>
- [Detailed workflow](references/detailed-workflow.md) <br>
- [Batch input format](references/batch-input-format.md) <br>
- [Batch end-to-end behavior](references/batch-end-to-end-behavior.md) <br>
- [Summary template](references/summary-template.md) <br>
- [Session output template](references/session-output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, JSON workflow metadata, and session-ready completion text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces per-video raw transcript markdown and polished summary markdown; batch runs report successful outputs and failed-video reasons.] <br>

## Skill Version(s): <br>
1.1.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
