## Description: <br>
Local dev environment manager for process management, automatic HTTPS domains, SSL certificates, reverse proxying, and optional AI crash diagnosis from a single binary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danieltamas](https://clawhub.ai/user/danieltamas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to decide when run.dev fits a local development workflow and to get practical installation, configuration, process management, routing, SSL, and troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install path asks users to run a remote install script that can make privileged local system changes. <br>
Mitigation: Inspect the installer and source before running it, confirm the sudoers helper and network changes are narrowly scoped and removable, and prefer building from source when stronger review is needed. <br>
Risk: The tool can modify local hosts entries, install a privileged helper, and configure localhost port forwarding. <br>
Mitigation: Review the planned changes before accepting installation, run health checks after setup, and use the uninstall or cleanup commands to reverse changes when the tool is no longer needed. <br>
Risk: Optional AI crash diagnosis may expose logs that contain secrets, customer data, or proprietary details. <br>
Mitigation: Disable AI features or review logs before diagnosis when sensitive data may be present, and verify what data is sent to the configured local Claude integration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/danieltamas/rundev-local-dev) <br>
- [run.dev website](https://getrun.dev) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include recommendations, command examples, configuration snippets, and risk-aware installation guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
