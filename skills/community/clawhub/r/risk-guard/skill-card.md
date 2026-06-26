## Description: <br>
Risk Guard helps OpenClaw users diagnose common false failures and enforce confirmation before high-risk operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengpengliu1212-art](https://clawhub.ai/user/pengpengliu1212-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run local Windows diagnostics for tool execution, gateway status, port health, lock files, node process counts, and workspace paths. It also provides risk-level guidance so agents ask for confirmation before destructive or irreversible actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security verdict is suspicious because the diagnostic script can delete old workspace .lock and .tmp files by default. <br>
Mitigation: Review before installing, prefer running diagnostics with --dry-run first, and use a version where cleanup requires explicit confirmation or a cleanup flag. <br>
Risk: The skill performs local Windows process, port, localhost health, and workspace inspections that may expose environment-specific operational details in logs or reports. <br>
Mitigation: Run only in trusted local workspaces, review generated risk_guard.log and risk_guard_last.json before sharing, and avoid publishing local paths or process details. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pengpengliu1212-art/risk-guard) <br>
- [Published Skill URL in artifact metadata](https://clawhub.ai/skills/risk-guard) <br>
- [Local gateway health endpoint](http://127.0.0.1:18789/health) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell command examples and diagnostic text or JSON report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-only diagnostic flow; the bundled script can run in dry-run mode and may write local log and report files under the detected OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
