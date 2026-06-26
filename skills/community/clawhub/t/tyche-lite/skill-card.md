## Description: <br>
Tyche Lite processes up to 5 invoices from a CSV, shows payment status, and produces a friendly payment reminder template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Freelancers and small-business users can preview a short invoice list, check paid or overdue status, and draft a friendly reminder for an overdue invoice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice CSV files can contain client names, email addresses, amounts, due dates, and payment status. <br>
Mitigation: Use only CSV files intended for local processing and avoid sharing generated previews that expose client billing details. <br>
Risk: The install command shown in the artifact uses pip with --break-system-packages. <br>
Mitigation: Prefer installing the rich dependency in a virtual environment to avoid modifying system Python. <br>


## Reference(s): <br>
- [Tyche Lite ClawHub page](https://clawhub.ai/occupythemilkyway/tyche-lite) <br>
- [Publisher profile](https://clawhub.ai/user/occupythemilkyway) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads at most 5 invoice rows in Lite mode and renders a local console preview.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
