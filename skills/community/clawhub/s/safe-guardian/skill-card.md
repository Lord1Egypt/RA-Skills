## Description: <br>
A safe security layer plugin for OpenClaw that intercepts dangerous tool calls (exec, write, edit) through multi-layer blacklist/whitelist filtering and intent validation with comprehensive audit logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[confidentkai](https://clawhub.ai/user/confidentkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Safe Guardian to screen agent tool calls against blacklist, whitelist, and optional intent checks before execution, and to maintain audit records of allowed and blocked operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default allowlist permits reading /etc/passwd, which may expose sensitive local account data. <br>
Mitigation: Review and narrow the whitelist before installation, and remove the /etc/passwd allow entry unless it is explicitly required. <br>
Risk: Audit logs record tool calls and results in plaintext, which may capture prompts, commands, paths, or credentials. <br>
Mitigation: Enable redaction for sensitive fields, restrict log file permissions, and define a retention policy before using the skill. <br>


## Reference(s): <br>
- [Safe Guardian ClawHub Page](https://clawhub.ai/confidentkai/safe-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured text, JSON configuration, JavaScript code, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces allow/block decisions, reasons, audit log entries, and security report summaries.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
