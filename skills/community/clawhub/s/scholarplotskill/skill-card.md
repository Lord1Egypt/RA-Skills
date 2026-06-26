## Description: <br>
ScholarPlot AI Academic Figure Generator connects via MCP to generate and edit SCI-standard figures, including line charts, bar charts, heatmaps, neural network architectures, and experimental flowcharts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peizhou](https://clawhub.ai/user/peizhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and MCP-compatible agent users use this skill to generate and edit publication-oriented academic figures from natural language prompts and supplied data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Figure prompts, edit instructions, and supplied research data may be sent to figure.thirdme.com through MCP. <br>
Mitigation: Avoid submitting confidential or unpublished data unless the service terms are acceptable for the use case. <br>
Risk: The skill requires an API key tied to user subscription and quota. <br>
Mitigation: Keep the API key private and store it only in the local MCP client configuration. <br>
Risk: Broad or ambiguous edit requests can modify the wrong figure attributes. <br>
Mitigation: Use specific prompts and edit instructions, especially when changing an existing figure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/peizhou/scholarplotskill) <br>
- [ScholarPlot official website](https://figure.thirdme.com) <br>
- [ScholarPlot MCP documentation](https://figure.thirdme.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, code, guidance] <br>
**Output Format:** [Markdown with figure links, metadata summaries, optional figure code, and MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated figure URLs, 300dpi or SVG output metadata, and edit results from the external ScholarPlot MCP service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
