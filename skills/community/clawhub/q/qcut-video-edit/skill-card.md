## Description:

Run QCut's native TypeScript pipeline CLI for AI content generation, video analysis, transcription, YAML pipelines, ViMax agentic video production, project management, and state-aware editor automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donghaozhang](https://clawhub.ai/user/donghaozhang)

### License/Terms of Use:


## Use Case:

Developers and video automation users use this skill to operate QCut's native pipeline CLI for AI media generation, transcription, video analysis, YAML and ViMax workflows, and state-aware editor control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact QCut automation can modify projects, media, timelines, exports, and local provider key configuration.

Mitigation: Review destructive commands before execution, confirm project and media identifiers, and use dry-run modes where available.

Risk: Paid external AI provider pipelines can process user media and incur cost, especially when confirmations are skipped.

Mitigation: Avoid --no-confirm for paid pipelines, estimate costs first, and verify provider key configuration before running generation or analysis workflows.

Risk: Remotion generation delegates work to another Claude process with broad tool access.

Mitigation: Run generate-remotion only in trusted workspaces and review generated files before adding them to projects or timelines.

## Reference(s):

- [Qcut Video Edit on ClawHub](https://clawhub.ai/donghaozhang/skills/qcut-video-edit)
- [Native Pipeline CLI Skill](artifact/SKILL.md)
- [Native Pipeline CLI - Full Reference](artifact/REFERENCE.md)
- [Native Pipeline CLI - Pipelines, Keys & Project Management](artifact/reference-pipelines.md)
- [Native Pipeline CLI - ViMax Commands](artifact/reference-vimax.md)
- [QCut Editor CLI - Core Commands](artifact/editor-core.md)
- [QCut Editor CLI - Media & Project Commands](artifact/editor-media.md)
- [QCut Editor CLI - Timeline & Editing Commands](artifact/editor-timeline.md)
- [QCut Editor CLI - Export, Recording & Utilities](artifact/editor-output.md)
- [QCut Editor CLI - AI & Analysis Commands](artifact/editor-ai.md)
- [QCut Editor - State Control & Automation](artifact/editor-state-control.md)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may produce JSON envelopes, local media files, exports, project state, or configuration changes when executed in QCut.]

## Skill Version(s):

2026.3.5 (source: server release evidence, released 2026-03-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
