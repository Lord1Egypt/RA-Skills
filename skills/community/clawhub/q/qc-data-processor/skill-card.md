## Description: <br>
Quality control data analysis MCP server for parsing QC data, running SPC control charts and process capability analysis, fitting reliability distributions, and generating Markdown QC reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daizehua-wq](https://clawhub.ai/user/daizehua-wq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Manufacturing quality engineers and agent developers use this skill to parse CSV or Excel quality data, run SPC and reliability analyses, and generate Markdown QC reports for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server reads local CSV and Excel files that the agent is asked to analyze. <br>
Mitigation: Install it only where the server can access the intended QC files, and avoid pointing it at sensitive unrelated files. <br>
Risk: Production use depends on third-party Python packages for data parsing, numerical analysis, and reliability fitting. <br>
Mitigation: Pin or lock dependencies to reviewed versions before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daizehua-wq/skills/qc-data-processor) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON analysis results and Markdown reports, with configuration and shell command examples in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are text-based; the artifact states that it produces no images or GUI.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
