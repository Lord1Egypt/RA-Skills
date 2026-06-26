## Description: <br>
Runs QCut's native TypeScript pipeline CLI for AI content generation, video analysis, transcription, YAML pipelines, ViMax video production, project management, and deterministic editor automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donghaozhang](https://clawhub.ai/user/donghaozhang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and video automation users use this skill to have an agent operate QCut projects, generate and analyze media, run YAML or ViMax pipelines, transcribe audio, export timelines, and inspect editor state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch QCut and operate local video projects. <br>
Mitigation: Require explicit approval before launching QCut or letting an agent operate local projects. <br>
Risk: The skill can run destructive project, media, and timeline commands. <br>
Mitigation: Back up projects and require explicit approval before delete, overwrite, import, export-state, or timeline mutation commands. <br>
Risk: The skill includes secret-handling workflows for API keys. <br>
Mitigation: Prefer key status checks, avoid exposing key values, and require explicit approval before setting, revealing, or deleting credentials. <br>
Risk: The skill can upload media or prompts to external AI providers. <br>
Mitigation: Avoid confidential media unless provider and persistence risks are acceptable, and require approval before provider-backed analysis, generation, or transcription. <br>
Risk: The skill can enable a notification bridge, record the screen, and capture screenshots. <br>
Mitigation: Require explicit approval before enabling notification forwarding, recording, or screenshot capture, and disable bridges or recordings after the task. <br>


## Reference(s): <br>
- [Qcut Video Edit on ClawHub](https://clawhub.ai/donghaozhang/qcut-video-edit) <br>
- [Native Pipeline CLI Reference](artifact/REFERENCE.md) <br>
- [Native Pipeline CLI - Pipelines, Keys & Project Management](artifact/reference-pipelines.md) <br>
- [Native Pipeline CLI - ViMax Commands](artifact/reference-vimax.md) <br>
- [QCut Editor CLI - Core Commands](artifact/editor-core.md) <br>
- [QCut Editor CLI - Media & Project Commands](artifact/editor-media.md) <br>
- [QCut Editor CLI - Timeline & Editing Commands](artifact/editor-timeline.md) <br>
- [QCut Editor CLI - Export, Recording & Utilities](artifact/editor-output.md) <br>
- [QCut Editor CLI - AI & Analysis Commands](artifact/editor-ai.md) <br>
- [QCut Editor - State Control & Automation](artifact/editor-state-control.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, JSON] <br>
**Output Format:** [Markdown guidance with shell, curl, JSON, and YAML examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Executed QCut commands may produce media files, project state exports, JSON envelopes, transcripts, screenshots, recordings, or rendered video outputs.] <br>

## Skill Version(s): <br>
2026.3.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
