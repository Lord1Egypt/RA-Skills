## Description: <br>
Create professional, publication-quality technical architecture diagrams as inline SVG in HTML and render them to high-resolution PNG screenshots with Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wujiaming88](https://clawhub.ai/user/wujiaming88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, author, and export precise system architecture diagrams, component diagrams, flow charts, and data-flow visualizations with readable labels and controlled connections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The screenshot workflow can render remote URLs if a remote URL is provided. <br>
Mitigation: Prefer local HTML files and avoid passing arbitrary remote URLs to the screenshot script. <br>
Risk: Diagram HTML imports Google Fonts, which may make rendering depend on network access. <br>
Mitigation: Block or remove Google Fonts when fully offline rendering is required. <br>
Risk: Architecture diagrams may contain sensitive system names or implementation details. <br>
Mitigation: Review diagram content before sharing or using Telegram delivery. <br>


## Reference(s): <br>
- [Design System](references/design-system.md) <br>
- [Hermes Architecture Example](references/example-hermes.html) <br>
- [OpenClaw Architecture Example](references/example-openclaw.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with HTML, SVG, Python, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local HTML files and rendered PNG or JPEG diagram assets when the bundled screenshot workflow is used.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
