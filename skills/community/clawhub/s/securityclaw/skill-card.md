## Description: <br>
SecurityClaw audits OpenClaw skill directories for prompt injection, exfiltration, supply-chain, and unsafe tool-use indicators, with optional quarantine and owner-action guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mallen-lbx](https://clawhub.ai/user/mallen-lbx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill owners use SecurityClaw to scan OpenClaw skills before installation or review, generate findings, quarantine suspicious folders, and decide whether to delete, report, allow, or scan all skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may contain excerpts from scanned skill files and should be treated as potentially sensitive. <br>
Mitigation: Review and store JSON reports as local sensitive artifacts, and avoid sharing them without removing secrets or private content. <br>
Risk: Quarantine mode temporarily moves flagged skills out of the active skills directory. <br>
Mitigation: Start with the read-only scan and use --quarantine only when the installer or owner is comfortable moving flagged skill folders. <br>
Risk: Dynamic analysis of unknown skills can expose secrets, config, filesystem state, or network access if run without isolation. <br>
Mitigation: Run optional dynamic checks only after owner approval in an OS-level sandbox with no network egress, read-only real filesystems, and no access to OpenClaw config or secrets. <br>


## Reference(s): <br>
- [SecurityClaw ClawHub page](https://clawhub.ai/mallen-lbx/securityclaw) <br>
- [SecurityClaw rule catalog](references/rules.md) <br>
- [Sandboxing strategy](references/sandboxing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and local JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only scan by default; quarantine mode moves flagged skill directories when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
