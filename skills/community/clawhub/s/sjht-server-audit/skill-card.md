## Description: <br>
Audits remote servers over SSH and generates structured reports covering system inventory, running services, open ports, web and database configuration, and SSH, firewall, SELinux, process, and cron security signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aowind](https://clawhub.ai/user/aowind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system administrators use this skill to inspect servers they administer, summarize service exposure and host configuration, and produce a Markdown audit report with security findings and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit can collect sensitive details about a remote host and save them locally. <br>
Mitigation: Treat reports and temporary audit output as sensitive, store them in protected locations, and delete them when no longer needed. <br>
Risk: Running SSH-based audits against the wrong host can create unauthorized access or scanning concerns. <br>
Mitigation: Confirm the target host and account before execution and run the skill only against servers you administer or are authorized to assess. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aowind/sjht-server-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with shell command snippets and summarized audit findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive host inventory, open ports, service names, SSH settings, cron entries, and process data.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
