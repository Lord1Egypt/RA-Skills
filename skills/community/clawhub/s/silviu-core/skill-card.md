## Description: <br>
Implements Silviu-specific guardrails and runbooks to enforce validation, prevent common operational errors, and manage browser and GitHub interactions in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unknoOwnd](https://clawhub.ai/user/unknoOwnd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to follow OpenClaw operational guardrails, confirm browser attachment before automation, and verify repository access before cloning or auditing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The repo-audit preflight contacts GitHub or another selected repository host. <br>
Mitigation: Review the repository URL before running connectivity or ls-remote checks. <br>
Risk: The browser attach doctor inspects the active browser tab through OpenClaw browser attachment. <br>
Mitigation: Confirm the active tab is intended for OpenClaw inspection before enabling the browser relay. <br>


## Reference(s): <br>
- [Silviu Core ClawHub Release](https://clawhub.ai/unknoOwnd/silviu-core) <br>
- [Browser Attach Doctor](browser_attach_doctor.md) <br>
- [Repo Audit Preflight](repo_audit_preflight.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only runbooks; no generated files or persistent runtime behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
