## Description: <br>
Validator Agent runs an eight-round validation pipeline for TypeScript and Solidity projects before publish, merge, dependency updates, or deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[up2itnow](https://clawhub.ai/user/up2itnow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and release engineers use this skill as a quality gate for TypeScript or Solidity projects, running compile, lint, tests, audit, type coverage, documentation, changelog, and final summary checks before publishing or merging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local project commands such as package scripts and audit commands. <br>
Mitigation: Use it only on trusted repositories, review package scripts and dependencies before execution, and confirm the exact project path. <br>
Risk: The generated report filename may include a project name supplied by the workspace context. <br>
Mitigation: Sanitize or simplify the report filename if the project name contains path separators or shell characters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/up2itnow/validator-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown validation report with command outputs and a pass, warn, or block verdict] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact describes saving a report to ops/reports/validator-YYYY-MM-DD-HH-[project].md.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
