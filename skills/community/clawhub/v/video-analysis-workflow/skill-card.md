## Description:

Video Analysis Workflow 视频案例分析助手 helps agents turn local videos or Douyin/Bilibili links into structured video case libraries with storyboard, transcript, case-analysis, and reusable script-template reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siconvip](https://clawhub.ai/user/siconvip)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video planners, marketers, game-operations teams, and AI-assisted creative teams use this skill to analyze reference videos, extract visual rhythm and narration structure, and save reusable case-library assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can download online media and write a structured local video case library.

Mitigation: Use it only with videos the user is authorized to access, follow platform and copyright rules, and choose an approved local output folder.

Risk: Setup guidance references unaudited installation paths, unpinned dependencies, and PowerShell ExecutionPolicy Bypass.

Mitigation: Review or obtain setup scripts from a trusted source, avoid ExecutionPolicy Bypass where possible, pin or review dependencies, and install in an isolated environment.

Risk: Some platform downloads may request browser-cookie access.

Mitigation: Ask for explicit user authorization before reading cookies and restrict cookie use to videos the user is authorized to download.

Risk: Generated transcripts, frames, and reports may contain sensitive or copyrighted source-video content.

Mitigation: Review generated artifacts before sharing, keep Whisper raw outputs for audit, and store case folders according to the user's content-handling rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/siconvip/skills/video-analysis-workflow)
- [Publisher profile](https://clawhub.ai/user/siconvip)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, transcript files, frame images, optional HTML reports, and setup or download commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a per-video case folder containing case analysis, storyboard frames, transcript, script template, Whisper outputs, reusable prompts, and optional HTML.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
