## Description: <br>
Diagnose OpenClaw setup in one command with quick or full checks for Node, npm, gateway, config, workspace, and platform issues while reporting config and workspace file existence only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tommot2](https://clawhub.ai/user/tommot2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose local OpenClaw setup issues, including Node, npm, gateway, configuration, workspace, and platform checks. It helps troubleshoot setup failures quickly and proposes fixes only after showing the planned change and getting user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run local diagnostic commands while troubleshooting setup errors. <br>
Mitigation: Use the quick or full diagnostic scope appropriate to the issue and review the reported commands and results before taking action. <br>
Risk: Fix mode can modify the local OpenClaw setup if the user approves the proposed fix. <br>
Mitigation: Show exactly what will change, get explicit confirmation, apply the fix, and re-run the check to verify the result. <br>
Risk: The skill advertises companion skills as part of a suite. <br>
Mitigation: Assess each companion skill separately before installing it. <br>


## Reference(s): <br>
- [Setup Doctor ClawHub Page](https://clawhub.ai/tommot2/setup-doctor) <br>
- [Node.js](https://nodejs.org) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown diagnostic report with inline shell commands and one-line fix suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Quick check is intended to complete in about 10 seconds; full checks add file existence, workspace, platform, and common pitfall diagnostics.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
