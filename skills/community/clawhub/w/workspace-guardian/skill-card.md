## Description: <br>
Auto-healing and protection for OpenClaw workspaces that validates and repairs common startup, configuration, memory-file, and health-check issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elontools](https://clawhub.ai/user/elontools) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to keep OpenClaw workspaces healthy by creating required workspace memory files, checking OpenClaw configuration, and surfacing common gateway or LLM configuration issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run as a workspace repair helper and repeatedly change local workspace files or OpenClaw configuration. <br>
Mitigation: Review the shell script before enabling startup or heartbeat execution, back up openclaw.json, and require confirmation for configuration edits or gateway restarts. <br>
Risk: The skill may make Markdown files world-readable with chmod 644. <br>
Mitigation: Confirm that world-readable Markdown files are acceptable for the workspace before enabling automatic repairs. <br>


## Reference(s): <br>
- [Workspace Guardian Skill Page](https://clawhub.ai/elontools/workspace-guardian) <br>
- [Common Errors](references/common-errors.md) <br>
- [Health Checks](references/health-checks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and workspace configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace memory files and report OpenClaw configuration health when executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
