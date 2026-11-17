## Description:

Create professional, publication-quality technical architecture diagrams using pure SVG in HTML, then render them to high-resolution PNG screenshots with Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujiaming88](https://clawhub.ai/user/wujiaming88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use this skill to create precise system architecture diagrams, component diagrams, flow charts, data-flow diagrams, and module diagrams with legible labels and controlled SVG connections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The screenshot helper can load arbitrary HTTP, HTTPS, or file URLs.

Mitigation: Use it only with local HTML diagram files created for the current task; avoid passing remote URLs or file:// paths that expose unrelated local content.

Risk: Telegram delivery can disclose architecture details to an external service.

Mitigation: Review generated diagrams for sensitive system details before sending them through Telegram or any external channel.

Risk: Generated diagrams may contain incorrect architecture relationships or misleading labels.

Mitigation: Have a knowledgeable reviewer check component names, boundaries, data flows, and connection labels before publishing or sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wujiaming88/skills/svg-architecture-diagram)
- [Publisher Profile](https://clawhub.ai/user/wujiaming88)
- [Design System Reference](references/design-system.md)
- [Hermes Architecture Example](references/example-hermes.html)
- [OpenClaw Architecture Example](references/example-openclaw.html)
- [Screenshot Helper](scripts/screenshot.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, SVG, Python, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local HTML diagram files and high-resolution PNG screenshots when the agent follows the workflow.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
