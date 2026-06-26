## Description: <br>
Skill Orchestrator coordinates skill optimization, task routing, asset management, publishing checks, health monitoring, and audit logging for an organization-level agent skill library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxy0905](https://clawhub.ai/user/dxy0905) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to choose, orchestrate, monitor, optimize, and audit skills across a managed agent skill library. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes guidance for bypassing token redaction for a GitHub personal access token. <br>
Mitigation: Review and remove token-redaction bypass guidance before installation; use scoped credentials from approved secret storage and do not provide raw GitHub PATs during code execution. <br>
Risk: The release includes persistent auto-load guidance that can keep the skill active in future sessions. <br>
Mitigation: Require explicit confirmation before changing auto-load or persistent configuration, and enable auto-load only when ongoing activation is intended. <br>
Risk: The release includes workflows for configuration and publishing changes. <br>
Mitigation: Require confirmation before configuration or publishing actions and run security scanning before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dxy0905/skill-orchestrator-qszf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include skill recommendations, orchestration plans, health reports, audit notes, publishing checklists, and configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
