## Description: <br>
Video clip editing skill for automatically analyzing video content and generating CapCut draft templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[riclinccc](https://clawhub.ai/user/riclinccc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn source videos into narrated highlight clips, dialogue jump cuts, subtitles, and CapCut/JianYing draft files. It is suited for workflows that need an agent to plan clips, request approval, and then generate aligned video, audio, subtitle, and draft outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can alter the host Python environment during dependency installation. <br>
Mitigation: Review before installing, use an isolated virtual environment or container, and preinstall pinned dependencies instead of allowing runtime package installation. <br>
Risk: Video-derived data, transcripts, frames, and narration text may be sent to configured cloud providers. <br>
Mitigation: Run it only on media and text approved for those providers, and require explicit confirmation before cloud processing. <br>
Risk: The workflow can save generated media and CapCut/JianYing draft files. <br>
Mitigation: Require explicit confirmation before saving drafts or outputs, and review generated files before importing or publishing them. <br>


## Reference(s): <br>
- [CapCut MCP Server Reference](references/capcut-mcp.md) <br>
- [vectcut-api Reference](references/vectcut-api.md) <br>
- [FFmpeg Download](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; generated workflow artifacts include MP3, SRT, MP4, and JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow expects explicit user approval before generating files and enforces timing alignment between narration audio, video clips, subtitles, and draft_content.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
