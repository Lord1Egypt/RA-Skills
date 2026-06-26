## Description: <br>
Smart Charts is an intelligent chart generation and data analysis skill that reads user-supplied CSV, Excel, and JSON files, analyzes data characteristics with LLM assistance, and recommends and generates interactive ECharts visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neuhanli](https://clawhub.ai/user/neuhanli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and data-focused users use Smart Charts to parse tabular files, review recommended analysis directions, and generate interactive charts and concise data summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may execute AI-generated pandas transformation code locally with weak sandboxing. <br>
Mitigation: Keep transform confirmation enabled, inspect generated transform code, and avoid auto_confirm for untrusted data or automated workflows. <br>
Risk: Generated HTML charts can load chart libraries from third-party CDNs. <br>
Mitigation: Use a disposable or controlled environment for sensitive datasets and confirm that outbound CDN loading is acceptable before previewing generated charts. <br>
Risk: The security verdict recommends review before installation. <br>
Mitigation: Review the skill and install dependencies in an isolated environment before using it with production or sensitive data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; generated chart outputs are interactive HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local ECharts HTML files and preview URLs for user-supplied tabular datasets.] <br>

## Skill Version(s): <br>
3.1.6 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
