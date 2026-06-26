## Description: <br>
Free Security & Health Audit. Your OpenClaw deserves a check-up. This skill performs a non-invasive scan to detect security risks, outdated software, and misconfigurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bamontejano](https://clawhub.ai/user/bamontejano) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run read-only OpenClaw host security and health checks. It helps inspect audit findings, update status, firewall configuration, open ports, OS version, running services, and a system health score without changing the host. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect local ports, firewall status, update state, operating system details, running services, and other host diagnostics. <br>
Mitigation: Use it only on machines where sharing diagnostic information with the agent session is acceptable. <br>
Risk: The artifact promotes paid Pro hardening features that are separate from the free read-only release. <br>
Mitigation: Treat any automated fixes or Pro hardening behavior as outside the scope of this free Skill Card. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown health-check report with inline command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only diagnostic output; no file output is specified.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
