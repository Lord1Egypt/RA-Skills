## Description: <br>
Downloads videos from supported platforms, transcribes them locally, and can combine transcript and key-frame analysis for visual video understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kk-kingkong](https://clawhub.ai/user/kk-kingkong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to download supported public or local videos, create transcripts, query transcript segments, and produce text-plus-visual summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted video links can trigger downloading and analysis, including browser automation and local media processing. <br>
Mitigation: Use only videos the operator is authorized to process, review helper scripts and tool settings before installation, and avoid account-sensitive or private links. <br>
Risk: Transcripts, links, or extracted frames may be sent to third-party services during TikHub or MiniMax-assisted workflows. <br>
Mitigation: Verify API configuration and data handling before use, and do not process confidential, copyrighted, or regulated content unless approved. <br>
Risk: Downloaded media, transcripts, cached models, or frame captures may persist on local storage. <br>
Mitigation: Choose controlled storage locations, use cleanup procedures after processing, and delete generated files that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kk-kingkong/video-download-transcribe) <br>
- [OpenClaw media helper repository](https://github.com/openclaw/openclaw-media) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, Python snippets, JSON examples, transcripts, timestamps, and summary text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May output transcript IDs for long-running jobs, timestamped segments, downloaded media paths, extracted frame analysis, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
3.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
