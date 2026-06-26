## Description: <br>
Routes requests across finance, e-commerce, media, and office agent teams with a smart switcher and 26 specialized roles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mx6315909](https://clawhub.ai/user/mx6315909) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route natural-language tasks to finance, e-commerce, media, or office agent teams for reports, operational guidance, document handling, and media-processing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill combines automatic routing with web, browser, memory, file, and command-execution capabilities. <br>
Mitigation: Install only with the permissions needed for the task, review planned actions before execution, and prefer sandboxed runs for command or browser workflows. <br>
Risk: Financial ratings, price targets, or portfolio suggestions may be misleading or stale. <br>
Mitigation: Verify recommendations against independent real market data and do not treat generated output as financial advice. <br>
Risk: Office and finance workflows may prompt users to share sensitive account details or private documents. <br>
Mitigation: Redact private information before use and avoid providing credentials, account numbers, or confidential documents unless the execution environment is approved. <br>
Risk: Media-processing workflows can modify or overwrite local files. <br>
Mitigation: Run media tasks on copies, constrain output paths, and confirm overwrite behavior before processing irreplaceable files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mx6315909/xiaodi-multi-team-switcher) <br>
- [README](README.md) <br>
- [Requirements](REQUIREMENTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with occasional inline shell commands or configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference optional API-key environment variables and local media-processing binaries; outputs should be reviewed before acting on financial, business, or file-changing recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
