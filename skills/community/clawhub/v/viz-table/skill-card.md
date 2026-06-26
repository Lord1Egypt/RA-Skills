## Description: <br>
Reads CSV or JSON files and generates interactive ECharts HTML charts, including bar, line, pie, and donut charts, then opens the result in a browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charles-lpf](https://clawhub.ai/user/charles-lpf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data-focused users can use this skill to turn local CSV or JSON datasets into interactive HTML charts with summary statistics and a data table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated HTML can include user dataset contents and opens an active local browser page that uses JavaScript formula evaluation. <br>
Mitigation: Review before installing, avoid confidential CSV or JSON inputs, and only use formulas from trusted sources; a safer implementation should replace eval() with a restricted arithmetic parser and make browser opening opt-in. <br>


## Reference(s): <br>
- [Viz Table on ClawHub](https://clawhub.ai/charles-lpf/viz-table) <br>
- [ECharts 5 CDN used by generated HTML](https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with generated HTML and shell command instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces /tmp/viz-table-output.html and may open it in a browser.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
