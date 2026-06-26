## Description: <br>
Extract, transcribe, clean, segment, and analyze long-form content from URLs, local media files, existing transcripts, and pasted text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengjl19](https://clawhub.ai/user/chengjl19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn articles, social posts, podcasts, videos, local media, transcript files, or pasted text into usable text, cleaned transcripts, rough speaker segmentation, and analytical insight memos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup scripts may modify the host system by installing ffmpeg through available package managers. <br>
Mitigation: Review scripts before installation and confirm dependency installation manually where possible. <br>
Risk: The runtime may clone, build, and download unpinned whisper.cpp components and ggml model files. <br>
Mitigation: Run the skill in a disposable or sandboxed environment and verify downloaded dependencies before relying on outputs. <br>
Risk: Media acquisition and transcription workflows may create persistent transcript, cache, model, and runtime files. <br>
Mitigation: Use the provided runtime status and cleanup scripts after large jobs, and avoid processing sensitive media outside an approved environment. <br>


## Reference(s): <br>
- [Insight Quality](references/insight-template.md) <br>
- [Invocation Examples](references/invocation-examples.md) <br>
- [Speaker Segmentation](references/speaker-segmentation.md) <br>
- [Transcript Cleaning](references/transcript-cleaning.md) <br>
- [Workflow](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown responses with optional transcript and memo files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create raw transcript, cleaned transcript, rough speaker transcript, and insight memo artifacts for long-form sources.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
