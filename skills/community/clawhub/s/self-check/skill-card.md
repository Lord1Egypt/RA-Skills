## Description: <br>
Checks a local OpenClaw environment for configuration, file integrity, permissions, dependencies, and API-token presence, then reports issues with suggested manual fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solarise94](https://clawhub.ai/user/solarise94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to audit local setup health after environment changes, before troubleshooting, or during periodic checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The report can reveal local setup details, installed skills, enabled services, file paths, permissions, and API-key presence. <br>
Mitigation: Treat generated reports as sensitive and review or redact them before sharing. <br>
Risk: Suggested repair commands may change packages, services, or configuration if copied into a shell. <br>
Mitigation: Run suggested commands only after manual review in the intended OpenClaw environment; the skill does not execute repairs automatically. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/solarise94/self-check) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with inline shell commands for suggested manual repairs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports API-key presence without values and sorts findings by severity.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence; artifact frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
