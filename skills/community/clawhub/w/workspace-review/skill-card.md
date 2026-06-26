## Description: <br>
Audit workspace structure and memory files against OpenClaw conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ortegarod](https://clawhub.ai/user/ortegarod) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw workspace maintainers use this skill to audit workspace structure, memory hygiene, git status, and misplaced files against OpenClaw conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review output can reveal private file names, git status, memory organization, and possible secret locations. <br>
Mitigation: Keep generated workspace review reports private and share only after removing sensitive paths, git details, and secret-location hints. <br>
Risk: The skill inspects local workspace structure and memory files, which may contain private or sensitive information. <br>
Mitigation: Install and run it only in workspaces the user is comfortable auditing locally. <br>


## Reference(s): <br>
- [Workspace Review package page](https://clawhub.ai/ortegarod/workspace-review) <br>
- [OpenClaw Workspace Conventions](references/openclaw-conventions.md) <br>
- [Workspace Review Checklist](references/checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with status sections and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports passing checks, warnings, issues, and recommendations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
