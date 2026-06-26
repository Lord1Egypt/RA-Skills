## Description: <br>
Audit code for "vibe coding sins" — patterns that indicate AI-generated code was accepted without proper review, producing a scored report card with fix suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tkuehnl](https://clawhub.ai/user/tkuehnl) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to audit Python, TypeScript, and JavaScript files or git diffs for code-quality, maintainability, and security patterns associated with insufficiently reviewed AI-generated code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analyzed files may be sent to configured LLM providers when API keys are available. <br>
Mitigation: Avoid running on repositories containing secrets, proprietary code, or regulated data unless provider use is permitted; scope each run to the specific files or diff that need review. <br>
Risk: Generated fix suggestions could be incorrect or inappropriate if applied without review. <br>
Mitigation: Treat fixes as reviewable unified diff suggestions; inspect and test changes before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tkuehnl/vibe-check) <br>
- [README](README.md) <br>
- [Security model](SECURITY.md) <br>
- [Testing plan](TESTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with scorecards, findings, and optional unified diff suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write the report to a user-specified Markdown file when --output is used.] <br>

## Skill Version(s): <br>
0.2.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
