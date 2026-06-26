## Description: <br>
Security Audit Assistant generates lightweight security baseline reports and remediation commands for OpenClaw-managed servers, focusing on SSH, firewall, update, password, logging, and file-permission checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huoxinjiang](https://clawhub.ai/user/huoxinjiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
DevOps teams, system administrators, and small business operators use this skill to review OpenClaw-managed Linux nodes for common security baseline gaps and to produce human-readable findings with proposed shell remediation commands. Reviewers should confirm results before relying on the report because server security evidence says the current scanner may report success without real node checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server security evidence says the scanner appears to be a mock that can report success without actually checking the server. <br>
Mitigation: Install only after source review and non-production testing; do not rely on reports until the command runner performs real OpenClaw node execution. <br>
Risk: Generated remediation commands can change SSH, firewall, package, logging, and file-permission settings. <br>
Mitigation: Review each command, confirm it matches the target operating system and maintenance window, and keep rollback access before applying sudo fixes. <br>
Risk: Documented CLI options and export formats may not match implemented behavior. <br>
Mitigation: Verify supported arguments and output formats in a test OpenClaw environment before scheduling audits or integrating the output into compliance workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huoxinjiang/security-audit-assistant) <br>
- [CIS Benchmark Summary](references/cis-benchmark-summary.md) <br>
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON] <br>
**Output Format:** [Human-readable security audit report with remediation commands; documented JSON export for integrations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include pass/fail counts, risk categories, actual values when available, and suggested remediation commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
