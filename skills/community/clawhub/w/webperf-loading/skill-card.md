## Description: <br>
Intelligent loading performance analysis with automated workflows for TTFB investigation, render-blocking detection, script performance attribution, font optimization, resource hints validation, and Chrome DevTools MCP execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nucliweb](https://clawhub.ai/user/nucliweb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and performance engineers use this skill to run Chrome DevTools based audits for page loading bottlenecks, including TTFB, FCP, render-blocking resources, script loading, fonts, images, CSS, service workers, and resource hints. It helps agents turn browser measurements into concise optimization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The snippets inspect page and resource metadata, which can expose sensitive details on banking, admin, internal, or authenticated pages. <br>
Mitigation: Run the skill only on sites the user is authorized to inspect and avoid sensitive authenticated contexts unless the data exposure is acceptable. <br>
Risk: One CSS analysis path can make additional stylesheet requests from the browser. <br>
Mitigation: Use the CSS analysis workflow only where additional browser-side stylesheet requests are acceptable for the target site. <br>


## Reference(s): <br>
- [Script Return Value Schema](references/schema.md) <br>
- [Script Descriptions and Thresholds](references/snippets.md) <br>
- [webperf-snippets repository](https://github.com/nucliweb/webperf-snippets) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript snippets and structured JSON script results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authorized page inspection context through Chrome DevTools MCP.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
