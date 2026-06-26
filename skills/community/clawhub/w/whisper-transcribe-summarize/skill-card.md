## Description: <br>
Local Whisper speech-to-text for audio and video files, with transcript cleanup, article-style rewriting, and structured summary guidance while running offline after dependencies and models are available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangjinjin-gitgit](https://clawhub.ai/user/zhangjinjin-gitgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and knowledge workers use this skill to transcribe local audio or video files with Whisper and produce cleaned transcripts plus human-readable rewritten and summary drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The transcription script writes output files and may overwrite an existing transcript path. <br>
Mitigation: Use deliberate output paths and review destination files before running the skill on important media. <br>
Risk: Audio or video transcripts can contain sensitive personal or business information. <br>
Mitigation: Keep generated transcript, rewrite, summary, Markdown, and HTML files in approved local storage and handle them according to the data sensitivity of the source media. <br>
Risk: Whisper model loading can download model files when the requested model is not already cached. <br>
Mitigation: For strict offline use, download and verify the intended Whisper model in advance and run with an explicit model cache directory. <br>
Risk: The rewrite and summary behavior is mostly instruction-driven rather than fully implemented in the bundled scripts. <br>
Mitigation: Review generated cleanup, rewrite, and summary outputs before relying on them, especially where completeness or fidelity to the source matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangjinjin-gitgit/whisper-transcribe-summarize) <br>
- [Publisher profile](https://clawhub.ai/user/zhangjinjin-gitgit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Local text files, Markdown summary files, optional HTML summary output, and concise completion status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local media paths, a Whisper model selection, optional language/task/device settings, and optional output and download directories.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
