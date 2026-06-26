## Description: <br>
Generate self-contained HTML pages that visually explain systems, code changes, plans, data, and complex tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bengii](https://clawhub.ai/user/bengii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical teams use this skill to turn architecture explanations, diff reviews, implementation plans, project recaps, and larger comparison tables into browser-viewable HTML reports or slide decks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can include sensitive repository context or session notes. <br>
Mitigation: Review and sanitize generated HTML before sharing it outside the local environment. <br>
Risk: Optional image generation and fact-check workflows may read repository files or modify target documents. <br>
Mitigation: Approve those workflows only for repositories and files the agent is allowed to inspect or edit, and review resulting changes. <br>
Risk: Local server cleanup scripts may affect Python HTTP server processes on common development ports. <br>
Mitigation: Check the intended port or process before running cleanup or stop scripts in a shared development environment. <br>


## Reference(s): <br>
- [Visual Explainer README](README.md) <br>
- [CSS Patterns](references/css-patterns.md) <br>
- [Libraries](references/libraries.md) <br>
- [Responsive Navigation](references/responsive-nav.md) <br>
- [Slide Patterns](references/slide-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/bengii/visual-explainer) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated HTML, Mermaid, CSS, JavaScript, and shell commands when serving or opening reports is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces self-contained browser-viewable HTML files and optional slide-deck HTML; may open local files in a browser or run local serving scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
