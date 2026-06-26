## Description: <br>
Generate self-contained HTML dashboards and visual pages for architecture diagrams, flowcharts, KPI dashboards, data tables, diff reviews, plan reviews, project recaps, and other technical explanations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redf426](https://clawhub.ai/user/redf426) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical teams use Vizboard to turn architecture, plan, diff, recap, dashboard, and table requests into responsive HTML visualizations for review and communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect git history, prior-session context, and memory files while preparing visual reviews, which may expose more local context than expected. <br>
Mitigation: Use it only in workspaces whose context can be reviewed by the agent, provide focused inputs, and avoid running it against sensitive repositories or memory stores. <br>
Risk: The skill may save HTML under the home directory, copy files into the workspace, open a browser, modify verification targets, or load third-party network resources. <br>
Mitigation: Review generated and modified files before relying on them, confirm file writes and browser launches, disable external image generation by default, and prefer bundled or local libraries for exported HTML. <br>


## Reference(s): <br>
- [Vizboard on ClawHub](https://clawhub.ai/redf426/vizboard) <br>
- [CSS Patterns](references/css-patterns.md) <br>
- [Visualization Libraries](references/libraries.md) <br>
- [Responsive Section Navigation](references/responsive-nav.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, files, guidance] <br>
**Output Format:** [Self-contained HTML files with inline CSS and JavaScript, plus brief delivery text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated pages are intended to be responsive and may include Mermaid diagrams, tables, dashboards, or review summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
