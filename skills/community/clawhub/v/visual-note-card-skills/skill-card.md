## Description:

Generate professional Chinese visual note cards as single-page HTML infographics with automatic PNG export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beilunyang](https://clawhub.ai/user/beilunyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, analysts, and content teams use this skill to turn topics, articles, or concepts into structured Chinese visual note cards for sharing, presentation, or print.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated cards may contact Google Fonts and cdnjs when opened.

Mitigation: Review generated HTML before sharing sensitive content, and replace or remove third-party CDN references when offline or internal-only delivery is required.

Risk: The PNG renderer runs Chromium with sandboxing disabled.

Mitigation: Run the renderer in an isolated environment and avoid feeding untrusted HTML into the rendering script.

Risk: Generated cards include mandatory repository attribution by default.

Mitigation: Review attribution requirements before producing unbranded deliverables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beilunyang/skills/visual-note-card-skills)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- [OpenClaw](https://openclaw.ai/)
- [html2canvas CDN](https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Guidance]

**Output Format:** [Self-contained HTML and PNG image files with concise Markdown delivery notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output includes both HTML and PNG; HTML-only output is supported when requested.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
