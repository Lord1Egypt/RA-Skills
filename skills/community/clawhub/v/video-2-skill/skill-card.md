## Description: <br>
Video to Skill Extractor helps agents convert authorized technical tutorial videos into reusable AI workflow skill documentation by extracting transcripts, visual evidence, OCR notes, timelines, principles, and generated skill files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacob210](https://clawhub.ai/user/jacob210) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to analyze authorized technical tutorial videos and turn the extracted methodology into reusable OpenClaw or Codex skill documentation. It is suited for workflows that need transcripts, visual/OCR evidence, timeline summaries, evidence maps, and generated Markdown skills rather than a simple video summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may use browser login cookies when downloading videos. <br>
Mitigation: Require explicit user confirmation before any browser-cookie command and use the skill only for content the user is authorized to access. <br>
Risk: Downloaded videos, transcripts, frames, and OCR outputs can contain sensitive or private content. <br>
Mitigation: Avoid sensitive or private videos unless local workspace storage and generated outputs are protected, and do not redistribute video content or full transcripts. <br>
Risk: Installing media, OCR, ASR, and browser automation dependencies globally can affect the host environment. <br>
Mitigation: Install and run dependencies in a virtual environment instead of modifying the global Python environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jacob210/video-2-skill) <br>
- [Publisher profile](https://clawhub.ai/user/jacob210) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, and text files with optional shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces video metadata, raw and cleaned transcripts, visual and OCR notes, a timeline, extracted principles, generated skill Markdown, an evidence map, and a debug report.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
