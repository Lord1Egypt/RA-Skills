## Description: <br>
Skill Analyzer evaluates OpenClaw skills for functionality, security, usability, documentation, maintainability, and best practices with weighted quality scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill publishers use this skill to review OpenClaw skill quality before publishing, find improvement opportunities, and support third-party skill security review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The analyzer's quality and security scores are advisory and may miss issues in a skill. <br>
Mitigation: Use the report as triage input, then manually review findings and run appropriate security checks before publishing or deployment. <br>
Risk: The optional report output can write or overwrite the file path provided by the user. <br>
Mitigation: Choose the output path intentionally and avoid pointing it at important existing files. <br>


## Reference(s): <br>
- [Skill Analysis Scoring Rubric](references/scoring_rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, JSON, Files] <br>
**Output Format:** [Plain text console report with optional JSON report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional comparison mode compares two skill directories; optional output mode writes a JSON report to the supplied path.] <br>

## Skill Version(s): <br>
0.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
