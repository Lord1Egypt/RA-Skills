## Description: <br>
Research Company helps agents research a company from a URL and produce a professional B2B account research PDF report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TomsTools11](https://clawhub.ai/user/TomsTools11) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, sales teams, business development teams, and analysts use this skill to turn public company information into structured account research and a downloadable PDF report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on public web research that can be incomplete, outdated, or incorrect. <br>
Mitigation: Verify important business claims and cited sources before relying on the generated report. <br>
Risk: The workflow may install ReportLab and write temporary JSON and PDF files in the workspace. <br>
Mitigation: Run it in a trusted workspace and review package installation and output paths before execution. <br>


## Reference(s): <br>
- [Data Schema](references/data-schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/TomsTools11/research-company) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance, structured JSON input, shell commands, and generated PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install ReportLab if missing, write a temporary JSON file, and save a PDF report in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
